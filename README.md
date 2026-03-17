# uo.wzk.cz

Ultima Online tools archive by MyKE. Migrated from WordPress to Hugo static site, hosted on Cloudflare Pages.

## Stack

| Component | Choice |
|-----------|--------|
| SSG | [Hugo](https://gohugo.io/) (extended) |
| Theme | [Terminal](https://github.com/panr/hugo-theme-terminal) |
| Hosting | [Cloudflare Pages](https://pages.cloudflare.com/) |
| CI/CD | GitHub Actions → Cloudflare Pages |

## Prerequisites

- [Hugo extended](https://gohugo.io/installation/) (v0.158.0+)
- Git

```bash
# macOS
brew install hugo
```

## Local Development

```bash
# Clone with submodules (theme)
git clone --recurse-submodules https://github.com/MyKEms/uo.wzk.cz.git
cd uo.wzk.cz

# Start dev server with drafts
hugo server -D

# Site available at http://localhost:1313/
```

## Creating a New Post

```bash
hugo new posts/my-new-tool/index.md
```

Add images into the post directory and downloadable files into `static/files/`.

## Deployment

Deployment is fully automated via GitHub Actions.

**Push to `main` → GitHub Actions builds Hugo → deploys to Cloudflare Pages**

```bash
git add .
git commit -m "Add new tool"
git push
# Auto-deploys in ~30 seconds
```

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `CLOUDFLARE_API_TOKEN` | API token with Cloudflare Pages edit permission |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account ID |

### Cloudflare Pages Project

- Project name: `uo-wzk-cz`
- Production URL: https://uo-wzk-cz.pages.dev
- Custom domain: `uo.wzk.cz` (to be configured)

## URL Structure

URLs match the original WordPress permalink structure:

```
/tool-slug/            → tool pages (flat, no date prefix)
/categories/           → category listing
```

## Project Structure

```
uo.wzk.cz/
├── config/_default/          # hugo.toml, params.toml, menus.toml
├── content/posts/slug/       # Page bundles (index.md + images)
├── layouts/
│   ├── _default/_markup/     # Image render hook
│   └── partials/             # Custom logo partial
├── static/
│   ├── files/                # Downloadable ZIPs (27 tools)
│   ├── images/               # Background wallpaper, UO logo
│   ├── style.css             # Custom CSS (background, logo)
│   └── _redirects            # Cloudflare Pages redirects
├── themes/terminal/          # Theme (git submodule)
├── .github/workflows/        # CI/CD
└── wp-export/                # Original WP export data (gitignored)
```

## Migration Notes

- Migrated from WordPress (17 posts, 5 comments, 27 downloadable ZIPs)
- Content exported via WordPress REST API, converted with custom Python script
- Images downloaded into page bundles, ZIPs into `static/files/`
- UO background wallpaper and logo preserved from original site
- Historical comments preserved as static blockquote sections
- Original export data kept in `wp-export/` (gitignored)
