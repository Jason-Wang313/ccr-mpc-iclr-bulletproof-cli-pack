param(
    [switch]$NoSmoke
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir
$ArgsList = @("--root", $Root)
if (-not $NoSmoke) {
    $ArgsList += "--smoke"
}

python (Join-Path $ScriptDir "verify_pack.py") @ArgsList
