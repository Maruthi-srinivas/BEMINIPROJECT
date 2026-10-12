# Expands scripts/d13_offline_bundle.json into repo paths. Run: powershell -File scripts/d13_offline_materialize.ps1
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$bundle = Join-Path $PSScriptRoot 'd13_offline_bundle.json'
if (-not (Test-Path $bundle)) { throw "Missing bundle: run generator or add d13_offline_bundle.json" }
$obj = Get-Content $bundle -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($p in $obj.PSObject.Properties) {
  $dest = Join-Path $root $p.Name
  $parent = Split-Path -Parent $dest
  if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
  [System.IO.File]::WriteAllText($dest, [string]$p.Value, [System.Text.UTF8Encoding]::new($false))
}
Write-Host ("Wrote {0} files" -f $obj.PSObject.Properties.Count)
