# Contributing

Thanks for your interest in contributing!

## Quick start

1. Fork the repo
2. Create a branch
3. Make changes
4. Open a PR

## Local dev

- Install deps: `python3 -m pip install -r requirements.txt`
- Run: `python3 opener.py`

## Packaging / releases

Packaging scripts live in `packaging/`.

- Windows one-file EXE: `packaging/windows/build-onefile.ps1`
- macOS app + dmg: `packaging/macos/build.sh`, `packaging/macos/make-dmg.sh`

## PR guidelines

- Keep PRs focused (one feature/fix at a time).
- Prefer readable UI/layout changes over “clever” code.
- If you touch packaging, update `packaging/README.md`.

