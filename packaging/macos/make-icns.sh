#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

SRC="Cursed McDonalds 1/Cursed McDonalds Logo.png"
OUT_DIR="packaging/macos/AppIcon.iconset"
OUT_ICNS="packaging/macos/CursedMcDonalds.icns"

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

if [[ ! -f "$SRC" ]]; then
  echo "Missing source image: $SRC" >&2
  exit 1
fi

for size in 16 32 64 128 256 512; do
  sips -z "$size" "$size" "$SRC" --out "$OUT_DIR/icon_${size}x${size}.png" >/dev/null
  sips -z "$((size*2))" "$((size*2))" "$SRC" --out "$OUT_DIR/icon_${size}x${size}@2x.png" >/dev/null
done

iconutil -c icns "$OUT_DIR" -o "$OUT_ICNS"
echo "Wrote: $OUT_ICNS"

