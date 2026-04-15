#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

NAME="Cursed McDonalds"

# Keep PyInstaller cache/config inside the project (sandbox-friendly).
export PYINSTALLER_CONFIG_DIR="$PWD/.pyinstaller"

ICON_PNG=""
if [[ -f "Cursed McDonalds 1/Cursed McDonalds Logo.png" ]]; then
  ICON_PNG="Cursed McDonalds 1/Cursed McDonalds Logo.png"
fi

PYI_ARGS=(--noconfirm --clean --windowed --name "$NAME" --add-data "Cursed McDonalds 1:Cursed McDonalds 1" opener.py)
if [[ -n "$ICON_PNG" ]]; then
  PYI_ARGS=(--icon "$ICON_PNG" "${PYI_ARGS[@]}")
fi

python3 -m PyInstaller "${PYI_ARGS[@]}"
echo "Built: dist/$NAME/"

