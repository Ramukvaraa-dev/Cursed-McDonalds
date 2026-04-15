<div align="center">

# Cursed McDonalds

![Cursed McDonalds Logo](Cursed%20McDonalds%201/Cursed%20McDonalds%20Logo.png)

[![Build Windows EXE](https://github.com/Ramukvaraa-dev/Cursed-McDonald/actions/workflows/build-windows-exe.yml/badge.svg)](https://github.com/Ramukvaraa-dev/Cursed-McDonald/actions/workflows/build-windows-exe.yml)
[![Build macOS DMG](https://github.com/Ramukvaraa-dev/Cursed-McDonald/actions/workflows/build-macos-dmg.yml/badge.svg)](https://github.com/Ramukvaraa-dev/Cursed-McDonald/actions/workflows/build-macos-dmg.yml)

</div>

Pygame story game with a launcher (`opener.py`) and Level 1 in `Cursed McDonalds 1/`.

## Download (recommended)

- **Releases**: publish `dist/` artifacts there (best “click to download” experience).
- **GitHub Actions (no local setup)**:
  - Windows: Actions → **Build Windows EXE** → downloads `Cursed McDonalds.exe`
  - macOS: Actions → **Build macOS DMG** → downloads `Cursed McDonalds.dmg`

## Run from source (dev)

1. Install deps: `python3 -m pip install -r requirements.txt`
2. Start: `python3 opener.py`

## Controls

- Mouse: click buttons
- Keyboard:
  - `Enter`: Start / launch Level 1 (when available)
  - `Esc`: Back / quit

## Levels

- Level Select shows Levels 1–10.
- Only **Level 1** is playable right now. Hover Levels 2–10 to see “Coming soon”.

## Build installers (bundles Python)

See `packaging/README.md` for Windows/macOS/Linux builds and installer options.

## Making a Release (maintainers)

1. Run the GitHub Actions builds (Windows EXE, macOS DMG).
2. Download the artifacts from the workflow run.
3. Create a GitHub Release and upload the artifacts (this becomes your “click to download” link).

## Contributing

PRs and issues are welcome. See `CONTRIBUTING.md`.

## Security

See `SECURITY.md`.
