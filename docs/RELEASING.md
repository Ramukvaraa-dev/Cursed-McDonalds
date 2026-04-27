# Releasing

Releases are created from version tags in the form `vX.Y.Z` (example: `v1.2.3`).

## Steps

1. Update `CHANGELOG.md` (move items from `[Unreleased]` into a new version section).
2. Create and push a tag:

   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

3. GitHub Actions workflow **Build (Windows + macOS)** runs and publishes a GitHub Release with:
   - Windows installer (`.exe`) + portable zip
   - macOS dmg + portable zip

