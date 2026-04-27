<div align="center">

# Cursed McDonalds

![Cursed McDonalds Logo](Cursed%20McDonalds%201/Cursed%20McDonalds%20Logo.png)

[![Build (Windows + macOS)](https://github.com/Ramukvaraa-dev/Cursed-McDonalds/actions/workflows/build.yml/badge.svg)](https://github.com/Ramukvaraa-dev/Cursed-McDonalds/actions/workflows/build.yml)
[![Quality](https://github.com/Ramukvaraa-dev/Cursed-McDonalds/actions/workflows/quality.yml/badge.svg)](https://github.com/Ramukvaraa-dev/Cursed-McDonalds/actions/workflows/quality.yml)

Pygame story game with a launcher and a playable Level 1.

</div>

A choose-your-story game called Cursed McDonalds with a launcher (`opener.py`) and Level 1 in `Cursed McDonalds 1/`.

## Table of contents

- [Downloads](#downloads)
- [Run from source](#run-from-source)
- [Project layout](#project-layout)
- [Controls](#controls)
- [Roadmap](#roadmap)
- [Docs](#docs)
- [Contributing](#contributing)
- [Security](#security)
- [Changelog](#changelog)

## Downloads

Grab the latest builds from GitHub **Releases**:

- Windows installer: `Cursed-McDonalds-Setup-windows.exe`
- macOS installer: `Cursed-McDonalds-macOS.dmg`
- Portable builds:
  - Windows: `Cursed-McDonalds-windows.zip`
  - macOS: `Cursed-McDonalds-macOS.zip`

If there isn’t a Release yet, open GitHub **Actions** → **Build (Windows + macOS)** and download the artifacts.

## Run from source

Requirements: Python 3.11+ (recommended).

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
python opener.py
```

## Project layout

- `opener.py`: launcher (main entry point for dev)
- `Cursed McDonalds 1/`: Level 1 game code/assets
- `installer/`: Windows/macOS installer build scripts
- `.github/workflows/`: CI (build + quality checks)

## Controls

- Mouse: click buttons
- Keyboard:
  - `Enter`: start / launch Level 1 (when available)
  - `Esc`: back / quit

## Roadmap

- Levels 2–10 (currently “Coming soon” in the level select UI)
- Save/load and settings menu
- More reliable cross-platform packaging

## Docs

- Architecture: `docs/ARCHITECTURE.md`
- Releasing: `docs/RELEASING.md`

## Contributing

PRs and issues are welcome. See `CONTRIBUTING.md`.

## Security

See `SECURITY.md`.

## Changelog

See `CHANGELOG.md`.
