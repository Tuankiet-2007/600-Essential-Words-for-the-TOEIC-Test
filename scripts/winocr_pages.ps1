# OCR cac trang con thieu bang Windows.Media.Ocr (WinRT) — nhanh, khong can GPU.
#
# Trang can OCR:
#   1. 37 trang "listening practice" ma MinerU tra ve rong (scan co san)
#   2. 4 trang Answer Key (trang 333-336)      -> dap an toan sach
#   3. 33 trang Listening Tapescripts (341-373) -> loi thoai that
#
# Ket qua ghi ve dung cho ban convert doc:
#   extracted_data/mineru_md/lesson_NN/listening_practice.md
#   extracted_data/mineru_md/answer_key/NNN_answer_key.md
#   extracted_data/mineru_md/tapescripts/NNN_tapescripts.md
#
# Dung: nhap doi scripts\RUN_WINOCR.bat  (hoac: powershell -File scripts\winocr_pages.ps1)

param(
  [ValidateSet('all', 'listening', 'answerkey', 'tapescripts')]
  [string]$Only = 'all',
  [switch]$Force
)

$ErrorActionPreference = 'Stop'
$ROOT = Split-Path -Parent $PSScriptRoot

Add-Type -AssemblyName System.Runtime.WindowsRuntime

$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and
    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
  })[0]
function Await($WinRtTask, $ResultType) {
  $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
  $netTask = $asTask.Invoke($null, @($WinRtTask))
  $netTask.Wait(-1) | Out-Null
  $netTask.Result
}

$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Storage.StorageFile, Windows.Foundation, ContentType = WindowsRuntime]

$avail = [Windows.Media.Ocr.OcrEngine]::AvailableRecognizerLanguages
if ($avail.Count -eq 0) { Write-Error 'Khong co ngon ngu OCR nao duoc cai dat'; exit 1 }
$lang = $avail | Where-Object { $_.LanguageTag -like 'en*' } | Select-Object -First 1
if (-not $lang) { $lang = $avail[0] }
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($lang)
if (-not $engine) { Write-Error 'Khong tao duoc OcrEngine'; exit 1 }
Write-Host "OCR engine: $($lang.LanguageTag) (max image $($engine.MaxImageDimension)px)"

function Ocr-Page([string]$ImagePath, [string]$OutPath) {
  if ((Test-Path $OutPath) -and -not $Force) {
    $existing = (Get-Item $OutPath).Length
    if ($existing -gt 50) { return 'skip (da co)' }
  }
  $path = (Resolve-Path $ImagePath).Path
  $file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($path)) ([Windows.Storage.StorageFile])
  $stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
  $decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
  $bitmap = Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
  $result = Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
  $lines = @($result.Lines | ForEach-Object { $_.Text })
  $dir = Split-Path -Parent $OutPath
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
  [System.IO.File]::WriteAllLines($OutPath, $lines)
  return "$($lines.Count) dong"
}

$jobs = @()

if ($Only -in 'all', 'listening') {
  # 1) Trang listening con rong cua tung bai
  $scans = Get-ChildItem -Path (Join-Path $ROOT 'extracted_data\lesson_page_scans') -Directory |
           Where-Object { $_.Name -match '^lesson_\d+$' } | Sort-Object Name
  foreach ($dir in $scans) {
    $lid = [int]($dir.Name -replace 'lesson_', '')
    $mdPath = Join-Path $ROOT "extracted_data\mineru_md\lesson_$($lid.ToString('00'))\listening_practice.md"
    $needOcr = $true
    if ((Test-Path $mdPath) -and (Get-Item $mdPath).Length -gt 50) { $needOcr = $false }
    if ($needOcr) {
      $scan = Get-ChildItem $dir.FullName -Filter '*_listening_practice.png' | Select-Object -First 1
      if ($scan) {
        $jobs += , @{ kind = 'listening'; lid = $lid; img = $scan.FullName; out = $mdPath }
      }
    }
  }
}

if ($Only -in 'all', 'answerkey') {
  $d = Join-Path $ROOT 'extracted_data\lesson_page_scans\answer_key'
  if (Test-Path $d) {
    foreach ($f in (Get-ChildItem $d -Filter '*.png' | Sort-Object Name)) {
      $jobs += , @{ kind = 'answerkey'; img = $f.FullName;
                    out = Join-Path $ROOT "extracted_data\mineru_md\answer_key\$($f.Name -replace '\.png$', '.md')" }
    }
  }
}

if ($Only -in 'all', 'tapescripts') {
  $d = Join-Path $ROOT 'extracted_data\lesson_page_scans\tapescripts'
  if (Test-Path $d) {
    foreach ($f in (Get-ChildItem $d -Filter '*.png' | Sort-Object Name)) {
      $jobs += , @{ kind = 'tapescripts'; img = $f.FullName;
                    out = Join-Path $ROOT "extracted_data\mineru_md\tapescripts\$($f.Name -replace '\.png$', '.md')" }
    }
  }
}

Write-Host "Can OCR $($jobs.Count) trang"
$done = 0; $fail = 0
foreach ($j in $jobs) {
  try {
    $r = Ocr-Page -ImagePath $j.img -OutPath $j.out
    $done++
    $label = if ($j.lid) { "L$($j.lid.ToString('00'))" } else { Split-Path -Leaf $j.img }
    Write-Host ("  [{0}] {1}: {2}" -f $j.kind, $label, $r)
  } catch {
    $fail++
    Write-Host ("  [LOI] {0}: {1}" -f $j.img, $_.Exception.Message)
  }
}
Write-Host "Xong: $done OK, $fail loi"
if ($fail -gt 0) { exit 1 }
