$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$project = Split-Path -Parent $root

Set-Location $project

$name = "Cursed McDonalds"
$dataArg = "Cursed McDonalds 1;Cursed McDonalds 1"

# Keep PyInstaller cache/config inside the project (sandbox-friendly).
$env:PYINSTALLER_CONFIG_DIR = Join-Path $project ".pyinstaller"

$iconIco = Join-Path $project "Cursed McDonalds 1\Cursed McDonalds Logo.ico"
if (-not (Test-Path $iconIco)) {
  $iconIco = ""
}

$args = @(
  "--noconfirm",
  "--clean",
  "--windowed",
  "--name", $name,
  "--add-data", $dataArg,
  "opener.py"
)

if ($iconIco -ne "") {
  $args = @("--icon", $iconIco) + $args
}

python -m PyInstaller @args

Write-Host "Built: dist\\$name\\"

