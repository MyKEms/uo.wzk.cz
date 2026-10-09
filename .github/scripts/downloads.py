#!/usr/bin/env python3
"""Downloads for uo.wzk.cz live in Cloudflare R2, not in git.

The bucket `uo-wzk-cz-files` is served at https://files.uo.wzk.cz/<key>. This repo
only keeps the inventory: downloads/manifest.tsv (key, size, sha256, content type)
and downloads/removed.txt (keys that must never be served again). The master copy
of the files is kept outside the repo (MASTER below = a local directory mirroring
the bucket).

  python3 .github/scripts/downloads.py manifest MASTER   # rebuild manifest.tsv from MASTER
  python3 .github/scripts/downloads.py upload MASTER     # put new/changed objects to R2 (wrangler)
  python3 .github/scripts/downloads.py remove KEY        # delete from R2 + manifest, add to removed.txt
  python3 .github/scripts/downloads.py verify [--deep]   # live: every object served, right size/type
                                                          #   (--deep also downloads and checks sha256);
                                                          #   removed keys must 404
  python3 .github/scripts/downloads.py legacy BASE_URL   # live: BASE_URL/files/<key> 301s to R2

upload/remove need wrangler credentials (`npx wrangler login` or CLOUDFLARE_API_TOKEN).
"""
import hashlib
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANIFEST = os.path.join(ROOT, "downloads", "manifest.tsv")
REMOVED = os.path.join(ROOT, "downloads", "removed.txt")
BUCKET = "uo-wzk-cz-files"
FILES = "https://files.uo.wzk.cz"
WRANGLER = os.environ.get("WRANGLER", "npx --yes wrangler@4.145.0").split()
CACHE_CONTROL = "public, max-age=604800"
HEADER = ["key", "size", "sha256", "content_type"]

# Same types Cloudflare Pages served for these files before the move to R2
TYPES = {
    ".zip": "application/zip",
    ".rar": "application/vnd.rar",
    ".7z": "application/x-7z-compressed",
    ".exe": "application/octet-stream",
    ".pdf": "application/pdf",
    ".swf": "application/x-shockwave-flash",
    ".txt": "text/plain; charset=utf-8",
}
UA = {"User-Agent": "Mozilla/5.0 (uo.wzk.cz downloads check)"}


def url(key):
    return FILES + "/" + urllib.parse.quote(key)


def load_manifest():
    rows = {}
    with open(MANIFEST, encoding="utf-8") as f:
        assert next(f).rstrip("\n").split("\t") == HEADER, "unexpected manifest header"
        for line in f:
            key, size, sha, ctype = line.rstrip("\n").split("\t")
            rows[key] = {"size": int(size), "sha256": sha, "content_type": ctype}
    return rows


def save_manifest(rows):
    with open(MANIFEST, "w", encoding="utf-8") as f:
        f.write("\t".join(HEADER) + "\n")
        for key in sorted(rows):
            r = rows[key]
            f.write(f"{key}\t{r['size']}\t{r['sha256']}\t{r['content_type']}\n")


def load_removed():
    if not os.path.isfile(REMOVED):
        return []
    lines = (l.strip() for l in open(REMOVED, encoding="utf-8"))
    return [l for l in lines if l and not l.startswith("#")]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def content_type(path):
    ext = os.path.splitext(path)[1].lower()
    if ext not in TYPES:
        sys.exit(f"{path}: no content type for {ext!r} — add it to TYPES")
    if ext == ".txt":
        try:
            open(path, "rb").read().decode("utf-8")
        except UnicodeDecodeError:
            return "text/plain; charset=windows-1250"  # old Czech changelogs
    return TYPES[ext]


def scan(master):
    rows = {}
    for d, _, fs in os.walk(master):
        for fn in fs:
            if fn.startswith("."):
                continue
            p = os.path.join(d, fn)
            key = os.path.relpath(p, master).replace(os.sep, "/")
            rows[key] = {"size": os.path.getsize(p), "sha256": sha256(p), "content_type": content_type(p)}
    return rows


def cmd_manifest(master):
    rows = scan(master)
    bad = sorted(set(rows) & set(load_removed()))
    if bad:
        sys.exit("removed keys present in master copy: " + ", ".join(bad))
    save_manifest(rows)
    print(f"{MANIFEST}: {len(rows)} objects, {sum(r['size'] for r in rows.values()) / 1e6:.0f} MB")


def head(key):
    req = urllib.request.Request(url(key), method="HEAD", headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, int(r.headers.get("Content-Length", -1)), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return e.code, -1, ""


def cmd_upload(master):
    rows = load_manifest()
    local = scan(master)
    if set(local) != set(rows):
        sys.exit("master copy and manifest differ — run `manifest` first and review the diff")
    for key, r in rows.items():
        if local[key] != r:
            sys.exit(f"{key}: master copy does not match manifest")

    def todo(key):
        status, size, ctype = head(key)
        return key if (status, size, ctype) != (200, rows[key]["size"], rows[key]["content_type"]) else None

    with ThreadPoolExecutor(8) as ex:
        pending = [k for k in ex.map(todo, sorted(rows)) if k]
    print(f"{len(rows) - len(pending)} up to date, {len(pending)} to upload")

    def put(key):
        cmd = WRANGLER + ["r2", "object", "put", f"{BUCKET}/{key}", "--remote",
                          "--file", os.path.join(master, key),
                          "--content-type", rows[key]["content_type"],
                          "--cache-control", CACHE_CONTROL]
        p = subprocess.run(cmd, capture_output=True, text=True)
        return key, p.returncode, (p.stderr or p.stdout).strip().splitlines()[-1:] if p.returncode else ""

    failed = 0
    with ThreadPoolExecutor(4) as ex:
        for key, rc, out in ex.map(put, pending):
            print(("ok    " if rc == 0 else "FAIL  ") + key, *out)
            failed += rc != 0
    return 1 if failed else 0


def cmd_remove(key):
    rows = load_manifest()
    if key not in rows:
        sys.exit(f"{key} is not in the manifest")
    subprocess.run(WRANGLER + ["r2", "object", "delete", f"{BUCKET}/{key}", "--remote"], check=True)
    del rows[key]
    save_manifest(rows)
    with open(REMOVED, "a", encoding="utf-8") as f:
        f.write(key + "\n")
    print(f"removed {key} — now unlink or draft the post that links it")


def get_sha256(key):
    h = hashlib.sha256()
    with urllib.request.urlopen(urllib.request.Request(url(key), headers=UA), timeout=300) as r:
        for chunk in iter(lambda: r.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def cmd_verify(deep):
    rows = load_manifest()
    errors = []

    def check(key):
        r = rows[key]
        status, size, ctype = head(key)
        if status != 200:
            return f"{key}: HTTP {status}"
        if size != r["size"]:
            return f"{key}: size {size}, manifest {r['size']}"
        if ctype != r["content_type"]:
            return f"{key}: content type {ctype!r}, manifest {r['content_type']!r}"
        if deep and get_sha256(key) != r["sha256"]:
            return f"{key}: sha256 mismatch"
        return None

    def check_removed(key):
        status = head(key)[0]
        return None if status == 404 else f"removed {key}: HTTP {status} (want 404)"

    with ThreadPoolExecutor(8) as ex:
        errors += [e for e in ex.map(check, sorted(rows)) if e]
        errors += [e for e in ex.map(check_removed, load_removed()) if e]
    for e in errors:
        print(e)
    print(f"{len(rows)} objects{' (deep)' if deep else ''}, {len(load_removed())} removed keys: "
          + (f"{len(errors)} problem(s)" if errors else "all OK"))
    return 1 if errors else 0


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **kw):
        return None


def cmd_legacy(base):
    """Old /files/<key> URLs (bookmarks, forum posts) must 301 to the R2 object."""
    base = base.rstrip("/")
    opener = urllib.request.build_opener(NoRedirect)
    rows = load_manifest()

    def location(key):
        req = urllib.request.Request(base + "/files/" + urllib.parse.quote(key), method="HEAD", headers=UA)
        try:
            with opener.open(req, timeout=30) as r:
                return r.status, r.headers.get("Location")
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get("Location")

    def check(key):
        status, loc = location(key)
        ok = status == 301 and urllib.parse.unquote(loc or "") == FILES + "/" + key
        return None if ok else f"/files/{key}: {status} → {loc}"

    with ThreadPoolExecutor(8) as ex:
        errors = [e for e in ex.map(check, sorted(rows)) if e]
    for e in errors:
        print(e)
    print(f"{len(rows)} legacy URLs on {base}: " + (f"{len(errors)} problem(s)" if errors else "all 301 → R2"))
    return 1 if errors else 0


def main():
    a = sys.argv[1:]
    if a[:1] == ["manifest"] and len(a) == 2:
        return cmd_manifest(a[1])
    if a[:1] == ["upload"] and len(a) == 2:
        return cmd_upload(a[1])
    if a[:1] == ["remove"] and len(a) == 2:
        return cmd_remove(a[1])
    if a[:1] == ["verify"] and a[1:] in ([], ["--deep"]):
        return cmd_verify(a[1:] == ["--deep"])
    if a[:1] == ["legacy"] and len(a) == 2:
        return cmd_legacy(a[1])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
