# uo.wzk.cz — Claude Code Instructions

## What is this

Ultima Online tools archive by MyKE. Hugo static site hosted on Cloudflare Pages. Migrated from WordPress in March 2026. This is a frozen archive site — last content update was 2017.

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

- `partials/footer.html` — clean footer "© YYYY MyKE" + Cloudflare analytics (removed Hugo/panr attribution)
- `partials/logo.html` — custom logo with UO image + text (overrides theme's escaped logoText)
- `_default/_markup/render-image.html` — resolves page bundle images to absolute paths

## Custom styling

- `static/style.css` — UO background wallpaper, semi-transparent content area, logo styling (loaded automatically by Terminal theme if file exists)
- `static/images/background.jpg` — UO wallpaper from original WordPress site
- `static/images/logo.jpg` — UO logo from original WordPress site

## Downloadable files

27 ZIP files in `static/files/`. Posts reference them as `/files/filename.zip`. These are UO game tools archived from the original site.

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

## Important notes

- The `wp-export/` directory contains original WordPress export data and conversion scripts — it's gitignored
- Theme is a git submodule — always clone with `--recurse-submodules`
- This site is essentially frozen/archival — new content is unlikely
- Images were unwrapped from clickable links to avoid 404s on listing pages
- Categories: Graphics (11), Client (2), GM (2), RunUO (1), Sphere (1)
