#!/usr/bin/env bash
set -euo pipefail

out_dmg="${1:-Cursed-McDonalds-macOS.dmg}"

app_path="$(find dist -maxdepth 3 -name 'Cursed McDonalds.app' -print -quit)"
if [[ -z "${app_path}" ]]; then
  echo "ERROR: Could not find 'Cursed McDonalds.app' under dist/"
  exit 1
fi

staging="$(mktemp -d)"
cleanup() {
  rm -rf "${staging}"
}
trap cleanup EXIT

cp -R "${app_path}" "${staging}/"

rm -f "${out_dmg}"
hdiutil create -volname "Cursed McDonalds" -srcfolder "${staging}" -ov -format UDZO "${out_dmg}"
echo "Created ${out_dmg}"
