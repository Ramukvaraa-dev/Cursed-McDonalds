#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

NAME="Cursed McDonalds"

# Keep PyInstaller cache/config inside the project (sandbox-friendly).
export PYINSTALLER_CONFIG_DIR="$PWD/.pyinstaller"

ICON_ICNS=""
if [[ -f "packaging/macos/CursedMcDonalds.icns" ]]; then
  ICON_ICNS="packaging/macos/CursedMcDonalds.icns"
fi

PYI_ARGS=(--noconfirm --clean --windowed --name "$NAME" --add-data "Cursed McDonalds 1:Cursed McDonalds 1" opener.py)
if [[ -n "$ICON_ICNS" ]]; then
  PYI_ARGS=(--icon "$ICON_ICNS" "${PYI_ARGS[@]}")
fi

python3 -m PyInstaller "${PYI_ARGS[@]}"
echo "Built: dist/$NAME.app"

