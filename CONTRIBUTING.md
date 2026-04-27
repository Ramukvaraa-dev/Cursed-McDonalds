# Contributing

Thanks for your interest in contributing!

## Code of Conduct

By participating, you agree to follow `CODE_OF_CONDUCT.md`.

## Quick start (PRs)

1. Fork the repo
2. Create a branch
3. Make changes
4. Open a PR

## Local dev

- Install deps: `python3 -m pip install -r requirements.txt`
- Run: `python3 opener.py`

## Filing issues

- Use the issue templates (bug report / feature request) when possible.
- Include your OS + Python version and clear reproduction steps.

## Packaging / releases

Builds are produced via GitHub Actions (`.github/workflows/build.yml`) on version tags like `v1.2.3`.

If you change packaging/release automation, please update `README.md` accordingly.

## PR guidelines

- Keep PRs focused (one feature/fix at a time).
- Prefer readable UI/layout changes over “clever” code.
- If you add new dependencies, update `requirements.txt`.

## Style and quality

- Keep changes compatible with Python 3.11+.
- Run `python -m compileall .` before opening a PR.
- If you run the “Quality” workflow locally, use `ruff` (optional).
