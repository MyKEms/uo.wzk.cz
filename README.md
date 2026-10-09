# uo.wzk.cz

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

Ultima Online tools archive — the largest Czech collection of UO development resources. Combines four sources:

- **uo.wzk.cz** — MyKE's UO tools collection (2009-2017)
- **ultima.manawydan.cz** — RadstaR's UO tools archive (2004-2016), cached by Golfin on UO Erebor servers
- **ultima.cz** — Czech UO community tutorials (2003-2014) by Lynx, M@B, Marty, Aramis
- **[UO FreeShard Community Tool Box](https://archive.org/details/UOFreeShardCommunityToolBoxLastUpdate03.31.2019)** — archive.org collection of 160+ UO tools (2019; marked Public Domain by the uploader — each tool keeps its own license)

Maintained as a resource for [UO Erebor](https://uoerebor.cz/) shard development.

**Live site:** https://uo.wzk.cz/

## Content

- **188 tool/tutorial posts** — map editors, graphics tools, animation convertors, server emulators, client assistants, GM tools, scripting utilities
- **~290 download files** (~1.6 GB) — original archives preserved as-is, served from Cloudflare R2 (`files.uo.wzk.cz`), **not stored in this repository**
- **11 Czech tutorials** — items, animations, buildings, verdata/MUL files, map generation, building philosophy
- **Categories:** Graphics, Client, GM, Server, Sphere, UOKR, Tutorials, News
- **Author tags:** RadstaR, Arya, Orbsydia, Punt, Kons, Ravenal, VD, Lynx, M@B, Marty, Aramis
- **Sources:** Posts tagged by origin — MW (Manawydan Archive), UCZ (ultima.cz Archive), TB (Toolbox Archive)

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

**Checks:** after `hugo --minify`, run `python3 .github/scripts/check_site.py` (same checks as CI).

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
│   ├── posts/slug/index.md       # Page bundles (188 published posts + 7 drafts)
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
│   ├── images/                   # Background, logos, bod.gif bullet icon
│   └── _redirects                # Legacy, pagination and /files/* → R2 redirects
├── downloads/
│   ├── manifest.tsv              # Inventory of R2 objects: key, size, sha256, content type
│   └── removed.txt               # Keys pulled for security/on request (must stay 404)
├── themes/terminal/              # Theme (vendored)
├── .github/workflows/            # CI/CD
├── wp-export/                    # WordPress export data (gitignored)
└── mw-export/                    # Manawydan source HTML (gitignored)
```

## Downloads (Cloudflare R2)

Downloads are third-party archives, so they are kept **out of git**: the repository holds only
the site and an inventory. Files live in the R2 bucket `uo-wzk-cz-files`, served at
`https://files.uo.wzk.cz/<key>` (keys: `<name>`, `manawydan/<author>/<name>`, `toolbox/<name>`).
Posts link the R2 URL directly; old `https://uo.wzk.cz/files/<key>` links 301 to it.

```bash
D=.github/scripts/downloads.py
python3 $D manifest ~/path/to/master   # rebuild downloads/manifest.tsv from the local master copy
python3 $D upload ~/path/to/master     # upload new/changed objects (needs `npx wrangler login`)
python3 $D remove toolbox/x.zip        # delete from R2, drop from manifest, add to removed.txt
python3 $D verify --deep               # live: every object served with the right size, type, sha256
python3 $D legacy https://uo.wzk.cz    # live: every old /files/ URL 301s to R2
```

CI checks every download link against the manifest, that every object is linked from a published
post, and that no archive or executable is committed. The weekly link report also runs `verify`.

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
4. **March 2026** — UO FreeShard Community Tool Box merge (+69 tools from archive.org ISO, 62 download files)

### Sources

- WordPress content exported via REST API, converted with Python script (`wp-export/`, gitignored)
- Manawydan content parsed from HTTrack mirror HTML pages (`mw-export/`, gitignored)
- Manawydan archive originally cached from `eranova.cz/ultima_manawydan/` by Golfin (2020)
- ultima.cz tutorials fetched and converted to Hugo posts with original screenshots
- Toolbox Archive sourced from [archive.org ISO](https://archive.org/details/UOFreeShardCommunityToolBoxLastUpdate03.31.2019) (2019; marked Public Domain by the uploader)

## Contributing

Found a broken link or want to add a missing tool? Open an [issue](https://github.com/MyKEms/uo.wzk.cz/issues) or submit a pull request. The validation workflow checks that the Hugo build succeeds and every download link is in `downloads/manifest.tsv`. New downloads are uploaded to R2 by the maintainer — attach the file to an issue instead of committing it.

## Credits

- **MyKE** — Archive maintainer, UO Erebor admin
- **RadstaR** — Manawydan tools archive creator
- **Golfin** — Preserved the Manawydan cache on UO Erebor servers
- **Tool authors** — Arya, Orbsydia, Punt, Kons, Ravenal, VD, and many others

## License

Site code and original content: [CC BY-NC 4.0](LICENSE). Third-party tools and downloads remain the property of their respective authors; they are not part of this repository and are not covered by its license.

## Security & abuse reports

See [SECURITY.md](SECURITY.md). Found a harmful download or have a removal request? [Report it privately](https://github.com/MyKEms/uo.wzk.cz/security/advisories/new) or [open an issue](https://github.com/MyKEms/uo.wzk.cz/issues/new) — every report is reviewed manually.
