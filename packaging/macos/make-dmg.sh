#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

NAME="Cursed McDonalds"
APP="dist/$NAME.app"
DMG="dist/$NAME.dmg"

if [[ ! -d "$APP" ]]; then
  echo "Missing app: $APP (run packaging/macos/build.sh first)" >&2
  exit 1
fi

rm -f "$DMG"

TMP_DIR="$(mktemp -d)"
cp -R "$APP" "$TMP_DIR/"
ln -s /Applications "$TMP_DIR/Applications"

hdiutil create -volname "$NAME" -srcfolder "$TMP_DIR" -ov -format UDZO "$DMG" >/dev/null
rm -rf "$TMP_DIR"

echo "Wrote: $DMG"

