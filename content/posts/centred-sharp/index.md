---
title: "CentrED#"
date: 2026-02-07T00:00:00
slug: "centred-sharp"
draft: false
categories:
  - "Graphics"
tags:
  - "kaczy93"
---

CentrED# is a complete C# rewrite of the original [CentrED](/centred/) map editor for Ultima Online, created by kaczy93. It is the recommended modern alternative to both CentrED and [CentrED+](/centred-plus/).

## Features

- Client/Server map editor (same architecture as original CentrED)
- Cross-platform: **Windows**, **Linux**, **macOS** (including Apple Silicon)
- Built on .NET — no legacy FreePascal/Lazarus dependencies
- Active development (722 commits, v0.6.11.30 as of February 2026)
- MIT license
- Acknowledges work from ServUO, ModernUO, ClassicUO, and UOFiddler

## Downloads

Latest release: **v0.6.11.30** (February 7, 2026)

Download from GitHub Releases — files are too large to host here (~26-32 MB each):

| File | Size |
|------|------|
| [CentrED-Windows-x64](https://github.com/kaczy93/centredsharp/releases/latest) | 26 MB |
| [CentrED-Linux-x64](https://github.com/kaczy93/centredsharp/releases/latest) | 26 MB |
| [CentrED-macOS-arm64](https://github.com/kaczy93/centredsharp/releases/latest) | 27 MB |
| [Cedserver-Windows-x64](https://github.com/kaczy93/centredsharp/releases/latest) | 32 MB |
| [Cedserver-Linux-x64](https://github.com/kaczy93/centredsharp/releases/latest) | 32 MB |
| [Cedserver-macOS-arm64](https://github.com/kaczy93/centredsharp/releases/latest) | 30 MB |

## Building from Source

Requires .NET 10 SDK.

```bash
git clone --recursive https://github.com/kaczy93/centredsharp.git
cd centredsharp
dotnet build
```

## Links

- [Homepage](https://kaczy93.github.io/centredsharp/)
- [GitHub](https://github.com/kaczy93/centredsharp)
- [Discord](https://discord.com/invite/zpNCv36fQ8)
- [Releases](https://github.com/kaczy93/centredsharp/releases)

## History

CentrED# is a ground-up rewrite — not a fork of the original CentrED (Lazarus/FreePascal by Andreas Schneider) or CentrED+ (uoquint.ru, now compromised). It is the most actively maintained CentrED variant available.

**Note:** This program does not distribute any copyrighted game assets. A legally obtained copy of the Ultima Online Classic Client is required.
