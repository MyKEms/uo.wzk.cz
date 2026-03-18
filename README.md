# uo.wzk.cz

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

Ultima Online tools archive — the largest Czech collection of UO development resources. Combines two archived sites:

- **uo.wzk.cz** — MyKE's UO tools collection (2009-2017)
- **ultima.manawydan.cz** — RadstaR's UO tools archive (2004-2016), cached by Golfin on UO Erebor servers
- **ultima.cz** — Czech UO community tutorials (2003-2014) by Lynx, M@B, Marty, Aramis

Maintained as a resource for [UO Erebor](http://uoerebor.cz/) shard development.

**Live site:** https://uo.wzk.cz/

## Content

- **115 tool/tutorial posts** — map editors, graphics tools, animation convertors, server emulators, GM tools
- **~200 download files** (~200 MB) — original archives preserved as-is
- **11 Czech tutorials** — items, animations, buildings, verdata/MUL files, map generation, building philosophy
- **Categories:** Graphics, Client, GM, Server, Sphere, UOKR, Tutorials, News
- **Author tags:** RadstaR, Arya, Orbsydia, Punt, Kons, Ravenal, VD, Lynx, M@B, Marty, Aramis
- **Sources:** Posts tagged by origin — MW (Manawydan Archive), UCZ (ultima.cz Archive)

## Stack

| Component | Choice |
|-----------|--------|
| SSG | [Hugo](https://gohugo.io/) (extended, v0.158.0+) |
| Theme | [Terminal](https://github.com/panr/hugo-theme-terminal) (vendored) |
| Hosting | [Cloudflare Pages](https://pages.cloudflare.com/) |
| CI/CD | GitHub Actions (direct Hugo + Wrangler, no third-party actions) |
| Analytics | Cloudflare Web Analytics |

## Local Development

```bash
git clone https://github.com/MyKEms/uo.wzk.cz.git
cd uo.wzk.cz

# Start dev server with drafts
hugo server -D

# Site available at http://localhost:1313/
```

**Prerequisites:** [Hugo extended](https://gohugo.io/installation/) (v0.158.0+), Git

```bash
# macOS
brew install hugo
```

## Deployment

Push to `main` or `dev` triggers GitHub Actions → Hugo build → Cloudflare Pages deploy (~30s).

| Branch | Environment | URL |
|--------|------------|-----|
| `main` | Production | https://uo.wzk.cz/ |
| `dev` | Preview | https://dev.uo-wzk-cz.pages.dev/ |

**Note:** The `dev` preview loads CSS from production (due to `baseURL`), so CSS changes are only visible after merging to `main`.

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `CLOUDFLARE_API_TOKEN` | API token with Cloudflare Pages edit permission |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account ID |

## Project Structure

```
uo.wzk.cz/
├── config/_default/              # hugo.toml, params.toml, menus.toml
├── content/
│   ├── posts/slug/index.md       # Page bundles (108 tool/tutorial posts)
│   ├── about.md                  # About/credits page
│   ├── archive.md                # Archive by date
│   └── sitemap.md                # All tools by category
├── layouts/
│   ├── _default/
│   │   ├── list.html             # Compact post listing (title + category)
│   │   ├── single.html           # Post page with source badge
│   │   ├── archive-page.html     # Archive by year/month
│   │   ├── sitemap-page.html     # Tools index by category
│   │   └── _markup/              # Image render hook
│   └── partials/
│       ├── footer.html           # Footer + analytics + disclaimer
│       ├── logo.html             # Custom logo
│       └── disclaimer.html       # Archive disclaimer banner
├── static/
│   ├── files/                    # Original downloads (27 ZIPs)
│   ├── files/manawydan/          # Manawydan downloads (~170 files, 172MB)
│   │   ├── arya/                 #   by author subdirectories
│   │   ├── kons/
│   │   ├── orbsydia/
│   │   ├── punt/
│   │   ├── radstar/
│   │   ├── ravenal/
│   │   ├── runuo/
│   │   ├── sphere/
│   │   ├── uokr/
│   │   └── vd/
│   ├── images/                   # Background, logos, bod.gif bullet icon
│   └── style.css                 # Custom CSS
├── themes/terminal/              # Theme (vendored)
├── .github/workflows/            # CI/CD
├── wp-export/                    # WordPress export data (gitignored)
└── mw-export/                    # Manawydan source HTML (gitignored)
```

## URL Structure

Flat URLs matching the original WordPress permalink structure:

```
/tool-slug/            → tool pages
/categories/           → category listing
/tags/                 → author listing
/sitemap/              → all tools by category
/archive/              → all posts by date
/about/                → credits and info
```

## Migration History

1. **March 2026** — WordPress → Hugo migration (17 posts, 27 ZIPs)
2. **March 2026** — Manawydan archive recovery and merge (+86 tools, +4 tutorials, ~170 download files)
3. **March 2026** — ultima.cz tutorials cached (+7 tutorials with screenshots)

### Sources

- WordPress content exported via REST API, converted with Python script (`wp-export/`, gitignored)
- Manawydan content parsed from HTTrack mirror HTML pages (`mw-export/`, gitignored)
- Manawydan archive originally cached from `eranova.cz/ultima_manawydan/` by Golfin (2020)
- ultima.cz tutorials fetched and converted to Hugo posts with original screenshots

## Contributing

Found a broken link or want to add a missing tool? Open an [issue](https://github.com/MyKEms/uo.wzk.cz/issues) or submit a pull request. The validation workflow will check that the Hugo build succeeds and all download links are valid.

## Credits

- **MyKE** — Archive maintainer, UO Erebor admin
- **RadstaR** — Manawydan tools archive creator
- **Golfin** — Preserved the Manawydan cache on UO Erebor servers
- **Tool authors** — Arya, Orbsydia, Punt, Kons, Ravenal, VD, and many others

## License

Site code and original content: [CC BY-NC 4.0](LICENSE). Third-party tools and downloads remain the property of their respective authors.
