# uo.wzk.cz — Claude Code Instructions

## What is this

Combined Ultima Online tools archive merging four sources:
- **uo.wzk.cz** — MyKE's UO tools collection (migrated from WordPress, March 2026)
- **ultima.manawydan.cz** — RadstaR's comprehensive UO tools archive (2004-2016), cached by Golfin on UO Erebor servers, merged March 2026
- **ultima.cz** — Czech UO community tutorials (2003-2014), cached March 2026
- **[UO FreeShard Community Tool Box](https://archive.org/details/UOFreeShardCommunityToolBoxLastUpdate03.31.2019)** — archive.org collection of 160+ UO shard development tools (Public Domain, 2019), merged March 2026

Hugo static site hosted on Cloudflare Pages. Maintained as a resource for [UO Erebor](https://uoerebor.cz/) shard development. 188 published posts (+7 drafts). Site title: **Ultima Online Tools Archive** (short: UO Tools Archive).

## Tech stack

- **SSG**: Hugo extended (v0.158.0+)
- **Theme**: [Terminal](https://github.com/panr/hugo-theme-terminal) (vendored in `themes/terminal/`)
- **Hosting**: Cloudflare Pages (project: `uo-wzk-cz`)
- **CI/CD**: GitHub Actions — `validate.yml` (PRs + called by deploy), `deploy.yml` (validate → build → deploy, pinned wrangler), `links.yml` (weekly external link report). All checks live in `.github/scripts/check_site.py` — run it locally after `hugo --minify`.
- **Analytics**: Cloudflare Web Analytics (JS snippet in footer partial)
- **License**: CC BY-NC 4.0
- **Repo**: https://github.com/MyKEms/uo.wzk.cz

## Key configuration

- **Config**: Split config in `config/_default/` — `hugo.toml`, `params.toml`, `menus.toml`
- **baseURL**: `https://uo.wzk.cz/` — do NOT change to relative `/` or RSS feeds break
- **Permalinks**: `/:slug/` — flat URLs matching old WordPress structure, do not change
- **Content section**: `content/posts/` (plural — Terminal theme default)
- **Page bundles**: Each post is `content/posts/slug/index.md` + images
- **Theme**: Dark theme (`themeColor = "dark"`)

## Custom layout overrides (in `layouts/`)

- `_default/baseof.html` — SEO `<title>` patterns, `<main>` landmark
- `partials/head.html` — replaces theme head: meta description (front matter `description` → summary fallback), canonical, OG/Twitter (`images/og-image.jpg`), single fingerprinted CSS bundle (theme CSS + `assets/site.css`, relative URL)
- `partials/schema.html` — JSON-LD: WebSite, SoftwareApplication (tools) / TechArticle (tutorials), BreadcrumbList
- `index.html` + `content/_index.md` — home: intro, category cards, recently added (no pagination)
- `_default/term.html`, `_default/terms.html`, `_default/list.html` — single-page compact lists (no pagination; old `/page/N` URLs 301 via `static/_redirects`); `/tags/` splits Authors vs Archive sources
- `partials/post-row.html`, `partials/source-badge.html` — shared list row + MW/UCZ/TB badge
- `404.html` — helpful 404 with links
- `index.llms.txt` → `/llms.txt` (AEO: every tool with its description, by category); `robots.txt` → Sitemap line
- `partials/footer.html` — footer "© YYYY MyKE" + About/All tools/RSS/GitHub/license links + Cloudflare analytics + disclaimer partial
- `partials/logo.html` — custom logo with UO image + text (overrides theme's escaped logoText)
- `partials/disclaimer.html` — site-wide archive disclaimer banner
- `_default/single.html` — breadcrumbs, source badge, "Related tools" (Hugo related content by category/tags) (`params.source: manawydan`, `ultima-cz`, or `toolbox`)
- `_default/archive-page.html` — archive grouped by year/month (used by `content/archive.md`)
- `_default/sitemap-page.html` — all tools index by category (used by `content/sitemap.md`)
- `_default/_markup/render-image.html` — resolves page bundle images, adds width/height and a fallback alt (`<title> screenshot`)

## Custom styling

- `assets/site.css` — (bundled + fingerprinted by head.html) UO background wallpaper (WebP + JPEG fallback), semi-transparent content area, logo styling, archive disclaimer, source badge, UO-style bullet points compact lists, category cards, breadcrumbs, related tools
- `static/images/background.webp` / `background.jpg` — UO wallpaper (1920px, from original WordPress site)
- `static/images/og-image.jpg` — 1200×630 social share image; `static/favicon.png`, `static/apple-touch-icon.png` — gold "UO" icon
- `static/images/logo.jpg` — UO logo from original WordPress site
- `static/images/bod.gif` — UO bullet point icon from Manawydan
- `static/images/mw_logo.jpg` — Manawydan logo (used on about page)

## Downloadable files

- **Original (uo.wzk.cz)**: 27 ZIP files in `static/files/`. Posts reference them as `/files/filename.zip`.
- **Manawydan archive**: ~170 files in `static/files/manawydan/` with subdirectories by author (arya/, kons/, orbsydia/, punt/, radstar/, ravenal/, runuo/, sphere/, uokr/, vd/). Posts reference them as `/files/manawydan/...`. Total ~172MB.
- **Toolbox archive**: 60 files in `static/files/toolbox/`. Posts reference them as `/files/toolbox/filename.zip`. Total ~132MB. Files over 25MB (Cloudflare Pages limit) are hosted on Cloudflare R2 — see R2 section below.

### Large files (Cloudflare R2)

7 tools exceed Cloudflare Pages' 25MB per-file limit and need R2 hosting:
- OrionUO-master.zip (27MB), JustUO.zip (77MB), polserver-master.zip (101MB)
- Sphere.zip (128MB), ASSORTED SCRIPTS.zip (65MB), UOCartographer.zip (29MB), Remote Control.zip (75MB)
- R2 bucket: `uo-wzk-cz-files`, public URL: `https://files.uo.wzk.cz/toolbox/`
- R2 free tier: 10GB storage, free egress

## Deployment

Push to `main` or `dev` triggers GitHub Actions → Hugo build → Cloudflare Pages deploy (~30s).

- **`main`** (production) → `uo.wzk.cz` (also `uo-wzk-cz.pages.dev`)
- **`dev`** (preview) → `dev.uo-wzk-cz.pages.dev`

Cloudflare Pages production branch is set to `main` in the dashboard. The `--branch` flag in the workflow tells Cloudflare which environment to deploy to.

### GitHub Secrets required

- `CLOUDFLARE_API_TOKEN` — Cloudflare API token with Pages edit permission
- `CLOUDFLARE_ACCOUNT_ID` — Cloudflare account ID

## Local development

```bash
git clone --recurse-submodules https://github.com/MyKEms/uo.wzk.cz.git
cd uo.wzk.cz
hugo server -D
# http://localhost:1313/
```

## Content structure

- **188 published posts** in `content/posts/` (6 original + 103 Manawydan + 7 ultima.cz + 72 Toolbox) + 7 drafts
- **Every post needs a `description:`** (50–170 chars, English, starts with what the tool is) — CI fails otherwise. All front matter is YAML.
- **Standalone pages**: `content/about.md`, `content/archive.md`, `content/sitemap.md`, `content/security.md` (abuse/security reporting; linked from footer, disclaimer, About)
- **Security policy**: `SECURITY.md` (GitHub) + `/security/` (web) + `static/.well-known/security.txt` (RFC 9116 — **renew `Expires` yearly**, currently 2027-09-30). Reports go to GitHub private vulnerability reporting or issues; every report is reviewed manually.
- **Categories** (CI-enforced list): Graphics, Client, GM, Server, Sphere, UOKR, Tutorials, News — each has `content/categories/<name>/_index.md` with an SEO description. A post may have two (e.g. Tutorials + Sphere).
- **Tags**: Author names (RadstaR, Arya, Kons, Orbsydia, Punt, Ravenal, VD, Lynx, M@B, Marty, Aramis) + "Manawydan Archive" + "ultima.cz Archive" + "Toolbox Archive" (tags are authors/sources only — no platform tags like RunUO)
- **Source badges**: `params.source: manawydan` shows green "MW" badge, `params.source: ultima-cz` shows brown "UCZ" badge, `params.source: toolbox` shows blue "TB" badge
- **Navigation**: Home, All Tools, Categories, Authors, Tutorials, Archive, About (7 items, `showMenuItems = 7`)

## Quarantine & removed downloads

- `quarantine/` holds files pulled from the site because antivirus/Netcraft flags them (cheats, bots, UOAM.zip — Bitdefender deletes it on checkout). It is outside `static/`, so it is **never deployed**. Their posts are `draft: true`.
- **Never put a download in `static/files/` without linking it from a published post** — CI's orphan check fails on unlinked files (drafts don't count), because unlinked files are still public.
- TDVPatchmaker was removed entirely (Netcraft/Cloudflare abuse report 871959ba769f7534, Sep 2026).

## Important notes

- The `wp-export/` directory contains original WordPress export data and conversion scripts — it's gitignored
- The `mw-export/` directory contains Manawydan source HTML and conversion scripts — it's gitignored
- Theme is vendored (not a submodule) — no special clone flags needed
- This site is essentially frozen/archival — new content is unlikely
- Images were unwrapped from clickable links to avoid 404s on listing pages
- Manawydan posts use date 2012-01-01 (archive date), tutorials use 2010-01-01
- Toolbox Archive posts use date 2019-03-31 (ISO archive date)
- CSS is referenced by relative fingerprinted URL, so the `dev` preview shows its own CSS
- UO bullet icons (bod.gif) are inlined as base64 in assets/site.css for the top navigation
- **After every content or structural change, update README.md and CLAUDE.md** to keep post counts, author lists, and documentation in sync
