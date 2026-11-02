# Renders every SVG in a folder to a PNG next to it (3x scale), using headless Chrome.
# Usage from the repository root: powershell -File docs/phase45/diagrams/render-svg.ps1 -Dir docs/phase45/images
param([string]$Dir, [string[]]$Only)
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$work = Join-Path $env:TEMP "svgrender"
New-Item -ItemType Directory -Force $work | Out-Null
Get-ChildItem $Dir -Filter *.svg | Where-Object { -not $Only -or $Only -contains $_.BaseName } | ForEach-Object {
  $svg = Get-Content $_.FullName -Raw
  if ($svg -match 'width="(\d+)" height="(\d+)"') { $w = $Matches[1]; $h = $Matches[2] } else { throw "no size in $($_.Name)" }
  Copy-Item $_.FullName (Join-Path $work "d.svg") -Force
  $html = "<!doctype html><html><head><style>html,body{margin:0;padding:0;background:#fff}</style></head><body><img src='d.svg' width='$w' height='$h' style='display:block'></body></html>"
  Set-Content -Path (Join-Path $work "d.html") -Value $html -Encoding UTF8
  $png = Join-Path $work "d.png"
  Remove-Item $png -ErrorAction SilentlyContinue
  $args = @("--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=3", "--window-size=$w,$h", "--user-data-dir=$env:TEMP\clprof", "--screenshot=$png", "file:///$($work -replace '\\','/')/d.html")
  Start-Process -FilePath $chrome -ArgumentList $args -Wait | Out-Null
  $out = [System.IO.Path]::ChangeExtension($_.FullName, ".png")
  Copy-Item $png $out -Force
  "rendered $([System.IO.Path]::GetFileName($out))"
}
