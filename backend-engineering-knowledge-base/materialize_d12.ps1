# Materialize D12-T001..D12-T031 notes and supporting files.
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$gen = Join-Path $root "_generators\generate_d12_security.py"
python $gen
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "D12 materialization complete."
