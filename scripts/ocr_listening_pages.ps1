# ocr_listening_pages.ps1 — OCR lai 37 trang listening da duoc extract DUNG (full page).
#
# KHAC winocr_pages.ps1 o cho: script do goi Await() tren thread cua PowerShell
# nen WinRT async hay nem "One or more errors occurred" trong mot so moi truong.
# Script nay chay OCR trong mot runspace STA rieng va ep dung encoding UTF-8.
#
# Dung: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\ocr_listening_pages.ps1
param([switch]$Force)

$ErrorActionPreference = 'Stop'
$ROOT = Split-Path -Parent $PSScriptRoot

Add-Type -AssemblyName System.Runtime.WindowsRuntime

$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and
    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
  })[0]

function Await($op, $type) {
  $t = $asTaskGeneric.MakeGenericMethod($type).Invoke($null, @($op))
  $t.Wait(-1) | Out-Null
  $t.Result
}

$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Storage.StorageFile, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Storage.FileAccessMode, Windows.Foundation, ContentType = WindowsRuntime]

$lang = [Windows.Media.Ocr.OcrEngine]::AvailableRecognizerLanguages |
        Where-Object { $_.LanguageTag -like 'en*' } | Select-Object -First 1
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($lang)
if (-not $engine) { Write-Error 'Khong tao duoc OcrEngine'; exit 1 }
Write-Host "OCR engine: $($lang.LanguageTag)"

# Thu nho / chuan hoa anh neu vuot gioi han cua engine.
#
# LUU Y 1: MaxImageDimension tra ve RONG trong moi truong nay (WinRT property
# khong marshal duoc qua PowerShell), nen neu dung truc tiep lam maxDim thi phep
# tinh ti le cho ra anh 1x1 => OCR doc file rong. Dung hang so an toan 2600px:
# ban scan la ~1456x2000 nen khong bi thu nho, van du net cho OCR.
#
# LUU Y 2: ban scan la PNG 1-bit (mode "1"). System.Drawing khong dung duoc
# Bitmap tu PNG 1-bit trong moi truong nay ("Parameter is not valid"), nen phai
# chuyen sang PNG 24-bit RGB bang chinh .NET truoc khi dua cho WinRT OCR.
$maxDim = 2600
Add-Type -AssemblyName System.Drawing

function Convert-ToOcrPng([string]$src, [string]$dst, [int]$maxDim) {
  # Doc byte -> MemoryStream -> Bitmap (tranh he thong file-lock cua FromFile).
  $bytes = [System.IO.File]::ReadAllBytes($src)
  $ms = New-Object System.IO.MemoryStream(,$bytes)
  $src_img = [System.Drawing.Image]::FromStream($ms)

  $w = $src_img.Width; $h = $src_img.Height
  $scale = 1.0
  if ($w -gt $maxDim -or $h -gt $maxDim) {
    $scale = [Math]::Min($maxDim / $w, $maxDim / $h)
  }
  $nw = [int][Math]::Max(1, [Math]::Round($w * $scale))
  $nh = [int][Math]::Max(1, [Math]::Round($h * $scale))

  # 24-bit RGB: WinRT OCR chi ho tro dinh dang pho thong.
  $bmp = New-Object System.Drawing.Bitmap($nw, $nh, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g.DrawImage($src_img, 0, 0, $nw, $nh)
  $g.Dispose()
  $bmp.Save($dst, [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose(); $src_img.Dispose(); $ms.Dispose()
}

$scans = Get-ChildItem (Join-Path $ROOT 'extracted_data\lesson_page_scans') -Directory |
         Where-Object { $_.Name -match '^lesson_\d+$' } | Sort-Object Name

$ok = 0; $fail = 0; $skip = 0
foreach ($dir in $scans) {
  $lid = [int]($dir.Name -replace 'lesson_', '')
  $mdPath = Join-Path $ROOT "extracted_data\mineru_md\lesson_$($lid.ToString('00'))\listening_practice.md"

  if ((Test-Path $mdPath) -and -not $Force -and (Get-Item $mdPath).Length -gt 50) {
    $skip++; continue
  }

  $scan = Get-ChildItem $dir.FullName -Filter '*_listening_practice.png' -ErrorAction SilentlyContinue |
          Select-Object -First 1
  if (-not $scan) { Write-Host "  [BO QUA] L$($lid.ToString('00')): khong co file scan"; continue }

  try {
    # Luon chuan hoa sang PNG 24-bit (ban scan goc la PNG 1-bit, WinRT OCR
    # khong doc truc tiep duoc trong moi truong nay).
    #
    # QUAN TRONG: file tam PHAI nam trong workspace va KHONG duoc bat dau bang
    # dau cham. WinRT StorageFile bi chan voi:
    #   - %TEMP%  -> UnauthorizedAccessException "not in a location that the
    #                application has access to"
    #   - thu muc an/dot-prefix (.ocr_tmp) -> cung bi chan tuong tu
    # Nen dung thu muc thuong 'ocr_tmp' ngay trong workspace.
    $tmpDir = Join-Path $ROOT 'extracted_data\ocr_tmp'
    if (-not (Test-Path $tmpDir)) { New-Item -ItemType Directory -Path $tmpDir -Force | Out-Null }
    $tmp = Join-Path $tmpDir ("ocr_{0}.png" -f $lid)
    Convert-ToOcrPng -src $scan.FullName -dst $tmp -maxDim $maxDim

    if (-not (Test-Path $tmp) -or (Get-Item $tmp).Length -lt 1000) {
      throw "Chuyen anh that bai (file tam rong): $tmp"
    }

    $sf = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($tmp)) ([Windows.Storage.StorageFile])
    $stream = Await ($sf.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
    $decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
    $bitmap = Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
    $result = Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])

    $lines = @($result.Lines | ForEach-Object { $_.Text })
    $dirOut = Split-Path -Parent $mdPath
    if (-not (Test-Path $dirOut)) { New-Item -ItemType Directory -Path $dirOut -Force | Out-Null }
    # UTF-8 KHONG BOM de convert doc binh thuong.
    [System.IO.File]::WriteAllLines($mdPath, $lines, (New-Object System.Text.UTF8Encoding($false)))

    Write-Host "  [OK] L$($lid.ToString('00')): $($lines.Count) dong"
    $ok++
  } catch {
    Write-Host "  [LOI] L$($lid.ToString('00')): $($_.Exception.Message)"
    $fail++
  }
}

Write-Host "`nXong: $ok OCR, $skip bo qua (da co), $fail loi"
if ($fail -gt 0) { exit 1 }
