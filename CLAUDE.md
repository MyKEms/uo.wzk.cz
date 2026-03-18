# uo.wzk.cz — Claude Code Instructions

## What is this

Combined Ultima Online tools archive merging two sources:
- **uo.wzk.cz** — MyKE's UO tools collection (migrated from WordPress, March 2026)
- **ultima.manawydan.cz** — RadstaR's comprehensive UO tools archive (2004-2016), cached by Golfin on UO Erebor servers, merged March 2026

Hugo static site hosted on Cloudflare Pages. Maintained as a resource for [UO Erebor](http://uoerebor.cz/) shard development. ~108 posts total.

## Tech stack

- **SSG**: Hugo extended (v0.158.0+)
- **Theme**: [Terminal](https://github.com/panr/hugo-theme-terminal) (git submodule in `themes/terminal/`)
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
- `_default/single.html` — overrides theme single.html to show "Manawydan Archive" source badge on posts with `params.source: manawydan`
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

- **108 posts** in `content/posts/` (17 original + 86 new from Manawydan + 4 tutorials + 1 news)
- **Standalone pages**: `content/about.md`, `content/archive.md`, `content/sitemap.md`
- **Categories**: Graphics, Client, GM, Server, Sphere, UOKR, Tutorials, News
- **Tags**: Author names (RadstaR, Arya, Kons, Orbsydia, Punt, Ravenal, VD) + "Manawydan Archive"
- Posts from Manawydan have `params.source: manawydan` in frontmatter (shows badge on page)
- **Navigation**: Home, All Tools, Categories, Authors, Tutorials, Archive, About (7 items, `showMenuItems = 7`)

## Important notes

- The `wp-export/` directory contains original WordPress export data and conversion scripts — it's gitignored
- The `mw-export/` directory contains Manawydan source HTML and conversion scripts — it's gitignored
- Theme is a git submodule — always clone with `--recurse-submodules`
- This site is essentially frozen/archival — new content is unlikely
- Images were unwrapped from clickable links to avoid 404s on listing pages
- Manawydan posts use date 2012-01-01 (archive date), tutorials use 2010-01-01
- The `dev` preview loads CSS from production (due to `baseURL`), so CSS-only changes are not visible on dev — must merge to `main` to verify
- UO bullet icons (bod.gif) are inlined as base64 in style.css for the top navigation
