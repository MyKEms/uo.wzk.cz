#!/usr/bin/env python3
"""Site checks for uo.wzk.cz — run after `hugo --minify` (expects ./public).

  python3 .github/scripts/check_site.py            # all blocking checks
  python3 .github/scripts/check_site.py external   # external link report (non-blocking)

Blocking checks:
  frontmatter  every post has title/slug/description, known categories and source
  downloads    every /files/ link in content exists in static/
  orphans      every file in static/files/ is linked from some post (unlinked
               downloads were how risky cheat tools slipped onto the site)
  internal     every internal href/src in the built HTML resolves in public/
  seo          every indexable page has a <title>, meta description and canonical
  size         no file over Cloudflare Pages' 25 MB limit
"""
import html
import os
import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT = os.path.join(ROOT, "content", "posts")
STATIC = os.path.join(ROOT, "static")
PUBLIC = os.path.join(ROOT, "public")
SITE = "https://uo.wzk.cz"

CATEGORIES = {"Graphics", "Client", "Server", "Sphere", "GM", "UOKR", "Tutorials", "News"}
SOURCES = {None, "manawydan", "toolbox", "ultima-cz"}
MAX_BYTES = 25 * 1024 * 1024

errors = []


def err(check, msg):
    errors.append(f"[{check}] {msg}")


def front_matter(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = m.group(1) if m else ""

    def scalar(key):
        m = re.search(rf"^\s*{key}:\s*\"?(.*?)\"?\s*$", fm, re.M)
        return m.group(1) if m else None

    def listval(key):
        m = re.search(rf"^{key}:\s*\n((?:\s+-\s.*\n?)+)", fm, re.M)
        return [x.strip()[1:].strip().strip('"') for x in m.group(1).splitlines()] if m else []

    return text, scalar, listval


def is_draft(path):
    return re.search(r"^draft:\s*true\s*$", open(path, encoding="utf-8").read(), re.M) is not None


def posts():
    """Published posts only — drafts are not built, so their links don't count."""
    for slug in sorted(os.listdir(CONTENT)):
        f = os.path.join(CONTENT, slug, "index.md")
        if os.path.isfile(f) and not is_draft(f):
            yield slug, f


def check_frontmatter():
    for slug, f in posts():
        _, scalar, listval = front_matter(f)
        for key in ("title", "slug", "description"):
            if not scalar(key):
                err("frontmatter", f"{slug}: missing {key}")
        d = scalar("description") or ""
        if d and not 50 <= len(d) <= 170:
            err("frontmatter", f"{slug}: description length {len(d)} (want 50–170)")
        cats = listval("categories")
        if not cats:
            err("frontmatter", f"{slug}: no category")
        for c in cats:
            if c not in CATEGORIES:
                err("frontmatter", f"{slug}: unknown category {c!r}")
        if scalar("source") not in SOURCES:
            err("frontmatter", f"{slug}: unknown source {scalar('source')!r}")


def linked_files():
    """All /files/ URLs linked from content: [x](/files/..), [x](</files/..>), href="/files/..", absolute or relative."""
    linked = set()
    pattern = re.compile(r"(?:\]\(<?|href=\")(?:" + re.escape(SITE) + r")?(/files/[^)>\s\"]+)")
    for d, _, fs in os.walk(os.path.join(ROOT, "content")):
        for fn in fs:
            if fn.endswith(".md") and not is_draft(os.path.join(d, fn)):
                text = open(os.path.join(d, fn), encoding="utf-8").read()
                linked.update(urllib.parse.unquote(u) for u in pattern.findall(text))
    return linked


def check_downloads_and_orphans():
    linked = linked_files()
    for u in sorted(linked):
        if not os.path.isfile(os.path.join(STATIC, u.lstrip("/"))):
            err("downloads", f"broken download link {u}")
    for d, _, fs in os.walk(os.path.join(STATIC, "files")):
        for fn in fs:
            rel = "/" + os.path.relpath(os.path.join(d, fn), STATIC)
            if fn != ".DS_Store" and rel not in linked:
                err("orphans", f"{rel} is not linked from any post — link it or delete it")


def html_pages():
    for d, _, fs in os.walk(PUBLIC):
        if os.sep + "files" in d[len(PUBLIC):]:
            continue  # archived third-party HTML inside downloads
        for fn in fs:
            if fn.endswith(".html"):
                p = os.path.join(d, fn)
                yield "/" + os.path.relpath(p, PUBLIC), open(p, encoding="utf-8", errors="ignore").read()


def check_internal_and_seo():
    for rel, s in html_pages():
        if 'http-equiv="refresh"' in s or "http-equiv=refresh" in s:
            continue
        for u in re.findall(r'(?:href|src)=("[^"]*"|[^ >]+)', s):
            u = html.unescape(u.strip('"'))
            if u.startswith(SITE):
                u = u[len(SITE):] or "/"
            if not u.startswith("/") or u.startswith(("//", "/cdn-cgi")):
                continue
            path = urllib.parse.unquote(u.split("#")[0].split("?")[0])
            f = os.path.join(PUBLIC, path.lstrip("/"))
            if not (os.path.isfile(f) or os.path.isfile(os.path.join(f, "index.html"))):
                err("internal", f"{rel}: broken link {path}")
        if rel == "/404.html" or re.search(r"<meta name=robots content=\"?noindex", s):
            continue
        if not re.search(r"<title>[^<]+</title>", s):
            err("seo", f"{rel}: missing <title>")
        m = re.search(r'<meta name=description content="?([^">]*)', s)
        if not m or len(m.group(1).strip()) < 50:
            err("seo", f"{rel}: missing or too short meta description")
        if "rel=canonical" not in s:
            err("seo", f"{rel}: missing canonical")


def check_size():
    for base in (STATIC, PUBLIC):
        for d, _, fs in os.walk(base):
            for fn in fs:
                p = os.path.join(d, fn)
                if os.path.getsize(p) > MAX_BYTES:
                    err("size", f"{os.path.relpath(p, ROOT)} exceeds 25 MB (host it on R2)")


def check_external():
    urls = set()
    for _, s in html_pages():
        for u in re.findall(r'href=("https?://[^"]+"|https?://[^ >]+)', s):
            u = html.unescape(u.strip('"'))
            if not u.startswith(SITE):
                urls.add(u)

    def probe(u):
        for method in ("HEAD", "GET"):
            try:
                req = urllib.request.Request(u, method=method, headers={"User-Agent": "Mozilla/5.0 (uo.wzk.cz link check)"})
                with urllib.request.urlopen(req, timeout=20) as r:
                    return u, r.status
            except urllib.error.HTTPError as e:
                if method == "GET":
                    return u, e.code
            except Exception as e:  # DNS, TLS, timeout
                if method == "GET":
                    return u, type(e).__name__
        return u, "?"

    with ThreadPoolExecutor(8) as ex:
        results = sorted(ex.map(probe, urls))
    bad = [(u, s) for u, s in results if not (isinstance(s, int) and s < 400) and s not in (401, 403, 429)]
    print(f"Checked {len(results)} external links, {len(bad)} problems")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    lines = ["## External link report", "", f"{len(results)} links checked, {len(bad)} problems", ""]
    lines += [f"- `{s}` {u}" for u, s in bad]
    print("\n".join(lines[4:]))
    if summary:
        open(summary, "a").write("\n".join(lines) + "\n")


def main():
    if sys.argv[1:] == ["external"]:
        check_external()
        return 0
    if not os.path.isdir(PUBLIC):
        print("public/ missing — run `hugo --minify` first")
        return 2
    check_frontmatter()
    check_downloads_and_orphans()
    check_internal_and_seo()
    check_size()
    for e in errors:
        print(e)
    print(f"{len(errors)} problem(s)" if errors else "All checks passed")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
