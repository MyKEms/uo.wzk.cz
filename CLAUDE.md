# uo.wzk.cz — Claude Code Instructions

## What is this

Combined Ultima Online tools archive merging four sources:
- **uo.wzk.cz** — MyKE's UO tools collection (migrated from WordPress, March 2026)
- **ultima.manawydan.cz** — RadstaR's comprehensive UO tools archive (2004-2016), cached by Golfin on UO Erebor servers, merged March 2026
- **ultima.cz** — Czech UO community tutorials (2003-2014), cached March 2026
- **[UO FreeShard Community Tool Box](https://archive.org/details/UOFreeShardCommunityToolBoxLastUpdate03.31.2019)** — archive.org collection of 160+ UO shard development tools (Public Domain, 2019), merged March 2026

Hugo static site hosted on Cloudflare Pages. Maintained as a resource for [UO Erebor](http://uoerebor.cz/) shard development. ~185 posts total.

## Tech stack

- **SSG**: Hugo extended (v0.158.0+)
- **Theme**: [Terminal](https://github.com/panr/hugo-theme-terminal) (vendored in `themes/terminal/`)
- **Hosting**: Cloudflare Pages (project: `uo-wzk-cz`)
- **CI/CD**: GitHub Actions — `deploy.yml` (build + deploy) and `validate.yml` (build + link checks on PRs)
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

- `partials/footer.html` — clean footer "© YYYY MyKE" + Cloudflare analytics + disclaimer partial
- `partials/logo.html` — custom logo with UO image + text (overrides theme's escaped logoText)
- `partials/disclaimer.html` — site-wide archive disclaimer banner
- `_default/single.html` — overrides theme single.html to show source badges on posts (`params.source: manawydan`, `ultima-cz`, or `toolbox`)
- `_default/list.html` — compact post listing (title + category badge, no images/summaries)
- `_default/archive-page.html` — archive grouped by year/month (used by `content/archive.md`)
- `_default/sitemap-page.html` — all tools index by category (used by `content/sitemap.md`)
- `_default/_markup/render-image.html` — resolves page bundle images to absolute paths

## Custom styling

- `static/style.css` — UO background wallpaper, semi-transparent content area, logo styling, archive disclaimer, source badge, UO-style bullet points (loaded automatically by Terminal theme if file exists)
- `static/images/background.jpg` — UO wallpaper from original WordPress site
- `static/images/logo.jpg` — UO logo from original WordPress site
- `static/images/bod.gif` — UO bullet point icon from Manawydan
- `static/images/mw_logo.jpg` — Manawydan logo (used on about page)

## Downloadable files

- **Original (uo.wzk.cz)**: 27 ZIP files in `static/files/`. Posts reference them as `/files/filename.zip`.
- **Manawydan archive**: ~170 files in `static/files/manawydan/` with subdirectories by author (arya/, kons/, orbsydia/, punt/, radstar/, ravenal/, runuo/, sphere/, uokr/, vd/). Posts reference them as `/files/manawydan/...`. Total ~172MB.
- **Toolbox archive**: 62 ZIP files in `static/files/toolbox/`. Posts reference them as `/files/toolbox/filename.zip`. Total ~132MB. Files over 25MB (Cloudflare Pages limit) are hosted on Cloudflare R2 — see R2 section below.

### Large files (Cloudflare R2)

7 tools exceed Cloudflare Pages' 25MB per-file limit and need R2 hosting:
- OrionUO-master.zip (27MB), JustUO.zip (77MB), polserver-master.zip (101MB)
- Sphere.zip (128MB), ASSORTED SCRIPTS.zip (65MB), UOCartographer.zip (29MB), Remote Control.zip (75MB)
- R2 bucket: `uo-wzk-cz-files`, public URL: `https://files.uo.wzk.cz/toolbox/` (also `https://pub-79b5028945c441d990e0babe712bcbb6.r2.dev/toolbox/`)
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

- **185 posts** in `content/posts/` (6 original + 103 from Manawydan + 7 ultima.cz tutorials + 69 from Toolbox Archive)
- **Standalone pages**: `content/about.md`, `content/archive.md`, `content/sitemap.md`
- **Categories**: Graphics, Client, GM, Server, Sphere, UOKR, Tutorials, News
- **Tags**: Author names (RadstaR, Arya, Kons, Orbsydia, Punt, Ravenal, VD, Lynx, M@B, Marty, Aramis) + "Manawydan Archive" + "ultima.cz Archive" + "Toolbox Archive" + "RunUO"
- **Source badges**: `params.source: manawydan` shows green "MW" badge, `params.source: ultima-cz` shows brown "UCZ" badge, `params.source: toolbox` shows blue "TB" badge
- **Navigation**: Home, All Tools, Categories, Authors, Tutorials, Archive, About (7 items, `showMenuItems = 7`)

## Important notes

- The `wp-export/` directory contains original WordPress export data and conversion scripts — it's gitignored
- The `mw-export/` directory contains Manawydan source HTML and conversion scripts — it's gitignored
- Theme is vendored (not a submodule) — no special clone flags needed
- This site is essentially frozen/archival — new content is unlikely
- Images were unwrapped from clickable links to avoid 404s on listing pages
- Manawydan posts use date 2012-01-01 (archive date), tutorials use 2010-01-01
- Toolbox Archive posts use date 2019-03-31 (ISO archive date)
- The `dev` preview loads CSS from production (due to `baseURL`), so CSS-only changes are not visible on dev — must merge to `main` to verify
- UO bullet icons (bod.gif) are inlined as base64 in style.css for the top navigation
- **After every content or structural change, update README.md and CLAUDE.md** to keep post counts, author lists, and documentation in sync
