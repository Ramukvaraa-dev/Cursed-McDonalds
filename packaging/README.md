# Packaging / Installers

This project uses **PyInstaller** to bundle a Python runtime + dependencies so players do **not** need to install Python.

In general, build on the target OS:
- Windows builds on Windows
- macOS builds on macOS
- Linux builds on Linux

## Prereqs

- Python 3.10+ recommended
- `pip`

Install build deps:
- `python -m pip install -r requirements-build.txt`

## Build outputs

- macOS: `dist/Cursed McDonalds.app` (and optionally `dist/Cursed McDonalds.dmg`)
- Windows: `dist\Cursed McDonalds.exe` (one-file) or `dist\Cursed McDonalds\` (folder)
- Linux: `dist/Cursed McDonalds/` (folder)

## macOS

Build `.app`:
- `bash packaging/macos/build.sh`

Create `.dmg`:
- `bash packaging/macos/make-dmg.sh`

Optional: generate an `.icns` icon (requires `sips` + `iconutil` which ship with macOS):
- `bash packaging/macos/make-icns.sh`

## Windows

Folder build:
- `powershell -ExecutionPolicy Bypass -File packaging/windows/build.ps1`

One-file exe:
- `powershell -ExecutionPolicy Bypass -File packaging/windows/build-onefile.ps1`

Optional installer (Inno Setup):
- Open `packaging/windows/installer.iss` in Inno Setup and build.

## Linux

Build:
- `bash packaging/linux/build.sh`

Optional AppImage notes:
- `packaging/linux/appimage/README.md`

