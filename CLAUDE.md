# uo.wzk.cz — Claude Code Instructions

## What is this

Combined Ultima Online tools archive merging two sources:
- **uo.wzk.cz** — MyKE's UO tools collection (migrated from WordPress, March 2026)
- **ultima.manawydan.cz** — RadstaR's comprehensive UO tools archive (2004-2016), cached by Golfin on UO Erebor servers, merged March 2026

Hugo static site hosted on Cloudflare Pages. This is a frozen archive site — ~107 tool/tutorial posts total.

## Tech stack

- **SSG**: Hugo extended (v0.158.0+)
- **Theme**: [Terminal](https://github.com/panr/hugo-theme-terminal) (git submodule in `themes/terminal/`)
- **Hosting**: Cloudflare Pages (project: `uo-wzk-cz`)
- **CI/CD**: GitHub Actions (`.github/workflows/deploy.yml`) — push to `main` auto-deploys
- **Analytics**: Cloudflare Web Analytics (JS snippet in footer partial)
- **Repo**: https://github.com/MyKEms/uo.wzk.cz (private)

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

Push to `main` triggers GitHub Actions → Hugo build → Cloudflare Pages deploy (~30s).

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

- **107 posts** in `content/posts/` (17 original + 86 new from Manawydan + 4 tutorials)
- **1 standalone page**: `content/about.md` — archive info and credits
- **Categories**: Graphics, Client, GM, Server, Sphere, UOKR, Tutorials
- **Tags**: Author names (RadstaR, Arya, Kons, Orbsydia, Punt, Ravenal, VD) + "Manawydan Archive"
- Posts from Manawydan have `params.source: manawydan` in frontmatter (shows badge on page)

## Important notes

- The `wp-export/` directory contains original WordPress export data and conversion scripts — it's gitignored
- The `mw-export/` directory contains Manawydan source HTML and conversion scripts — it's gitignored
- Theme is a git submodule — always clone with `--recurse-submodules`
- This site is essentially frozen/archival — new content is unlikely
- Images were unwrapped from clickable links to avoid 404s on listing pages
- Manawydan posts use date 2012-01-01 (archive date), tutorials use 2010-01-01
