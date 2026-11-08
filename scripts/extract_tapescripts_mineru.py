"""Trich xuat va OCR 34 trang Listening Tapescripts (PDF trang 340..373).

Quy trinh:
1. Dung pypdf + pick_full_page_scan trich xuat 34 trang scan toan trang
   (340..373) ra extracted_data/reference_scans/tapescript_p{340..373}.png.
2. Thu goi mineru-kit.exe tren 1 trang (hoac tat ca neu truyen --mineru-all).
   Neu MinerU bi chan boi sandbox (PermissionError: [WinError 5] tren named pipe)
   hoac truyen --fallback-ocr, chuyen ngay sang pipeline:
   Column-Aware Split + Word-Coordinate Line Reconstruction voi Windows.Media.Ocr:
   - Tim ranh trang doc (vertical whitespace gutter) giua cot 1 va cot 2.
   - Cat moi trang thanh 2 anh cot (Left Column, Right Column).
   - Chay Windows.Media.Ocr lay toa do tung tu (X, Y, W, H, Text).
   - Gom dong theo tung cot dua tren tam Y (vertical center) va sap xep X tang dan,
     giup giu nguyen nhan [M]/[W] va (A)/(B)/(C)/(D) dung dau moi dong!
   - Luu 34 file Markdown chuan thu tu doc vao:
     extracted_data/mineru_md/tapescripts_full/{340..373}_tapescripts.md
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys
from PIL import Image
import pypdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH = os.path.join(ROOT, "600 est_.pdf")
REF_SCANS_DIR = os.path.join(ROOT, "extracted_data", "reference_scans")
MINERU_OUT_DIR = os.path.join(ROOT, "extracted_data", "mineru_md", "tapescripts_mineru")
FULL_OUT_DIR = os.path.join(ROOT, "extracted_data", "mineru_md", "tapescripts_full")
TEMP_COLS_DIR = os.path.join(FULL_OUT_DIR, "_temp_cols")

TOOL_ROOT = r"D:\CODE\vibecode\TOOL\mineru"
MINERU_KIT = os.path.join(TOOL_ROOT, ".venv", "Scripts", "mineru-kit.exe")

TAPESCRIPT_PAGES = list(range(340, 374))  # 340..373 inclusive (34 pages)


def pick_full_page_scan(page) -> Image.Image | None:
    """Chon anh scan toan trang (dien tich pixel lon nhat) tu trang PDF."""
    best, best_area = None, -1
    for im in page.images:
        try:
            pil = Image.open(io.BytesIO(im.data))
        except Exception:
            continue
        w, h = pil.size
        area = w * h
        if area > best_area and w >= 800 and h >= 800:
            best, best_area = pil, area
    if best is not None:
        return best

    for im in page.images:
        try:
            pil = Image.open(io.BytesIO(im.data))
        except Exception:
            continue
        area = pil.size[0] * pil.size[1]
        if area > best_area:
            best, best_area = pil, area
    return best


def extract_scans(force: bool = False) -> list[tuple[int, str]]:
    """Dam bao 34 file tapescript_p{340..373}.png co mat trong reference_scans."""
    os.makedirs(REF_SCANS_DIR, exist_ok=True)
    need_extract = [
        p for p in TAPESCRIPT_PAGES
        if force or not os.path.isfile(os.path.join(REF_SCANS_DIR, f"tapescript_p{p}.png"))
    ]
    if need_extract:
        print(f"Trich xuat {len(need_extract)} trang scan tu {os.path.basename(PDF_PATH)}...")
        reader = pypdf.PdfReader(PDF_PATH)
        for p_num in need_extract:
            pil_scan = pick_full_page_scan(reader.pages[p_num - 1])
            if pil_scan is None:
                raise RuntimeError(f"Khong tim thay anh scan tren trang PDF {p_num}")
            out_png = os.path.join(REF_SCANS_DIR, f"tapescript_p{p_num}.png")
            pil_scan.save(out_png)
            print(f"  [OK] Da luu tapescript_p{p_num}.png ({pil_scan.size[0]}x{pil_scan.size[1]})")
    else:
        print(f"Da co du 34 anh scan tapescript_p340..373.png trong {REF_SCANS_DIR}.")

    return [
        (p, os.path.join(REF_SCANS_DIR, f"tapescript_p{p}.png"))
        for p in TAPESCRIPT_PAGES
    ]


def mineru_env() -> dict[str, str]:
    env = dict(os.environ)
    env["MINERU_HOME"] = os.path.join(TOOL_ROOT, "home")
    env["MINERU_MODEL_VLM_ENGINE"] = "llama-cpp"
    env["UV_CACHE_DIR"] = os.path.join(TOOL_ROOT, ".cache", "uv")
    env["UV_PYTHON_INSTALL_DIR"] = os.path.join(TOOL_ROOT, ".python")
    env["HF_HOME"] = os.path.join(TOOL_ROOT, ".cache", "huggingface")
    env["MODELSCOPE_CACHE"] = os.path.join(TOOL_ROOT, ".cache", "modelscope")
    env["VIRTUAL_ENV"] = os.path.join(TOOL_ROOT, ".venv")
    venv_scripts = os.path.join(TOOL_ROOT, ".venv", "Scripts")
    tmp = os.path.join(TOOL_ROOT, ".tmp")
    os.makedirs(tmp, exist_ok=True)
    env["TMP"] = tmp
    env["TEMP"] = tmp
    env["PATH"] = venv_scripts + os.pathsep + env.get("PATH", "")
    return env


def strip_base64(md_text: str) -> str:
    cleaned = re.sub(r"!\[[^\]]*\]\(data:image/[^)]*\)", "", md_text)
    cleaned = re.sub(r"data:image/[a-zA-Z+]+;base64,[A-Za-z0-9+/=\s]+", "", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned


def try_mineru_page(page_num: int, img_path: str, tier: str = "standard") -> tuple[bool, str]:
    """Thu chay mineru-kit.exe tren 1 trang. Tra ve (thanh_cong, thong_bao)."""
    if not os.path.isfile(MINERU_KIT):
        return False, f"Khong tim thay {MINERU_KIT}"
    os.makedirs(MINERU_OUT_DIR, exist_ok=True)
    target = os.path.join(MINERU_OUT_DIR, f"{page_num}_tapescripts.md")
    if os.path.isfile(target) and os.path.getsize(target) > 100:
        return True, f"Da co san {target}"

    r = subprocess.run(
        [MINERU_KIT, "parse", img_path, "-o", target, "--tier", tier],
        cwd=TOOL_ROOT,
        env=mineru_env(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0 or not os.path.isfile(target):
        out_tail = "\n".join((r.stdout or "").strip().splitlines()[-6:])
        return False, out_tail

    with open(target, encoding="utf-8", errors="replace") as f:
        cleaned = strip_base64(f.read())
    with open(target, "w", encoding="utf-8") as f:
        f.write(cleaned)
    if len(cleaned) < 100:
        return False, "MinerU tra ve < 100 ky tu"
    return True, f"OK ({len(cleaned)} chars)"


def find_column_gutter(pil_img: Image.Image) -> int:
    """Tim toa do X cua ranh trang doc giua 2 cot van ban.

    Quet vung X trong [0.43 * W, 0.57 * W] va Y trong [0.14 * H, 0.92 * H]
    (bo qua tieu de dau trang nhu LISTENING TAPESCRIPTS hay 600 ESSENTIAL WORDS).
    Chon cua so 9px co it diem den nhat, uu tien gan giua trang (0.50 * W).
    """
    gray = pil_img.convert("L")
    w, h = gray.size
    x_min = int(w * 0.43)
    x_max = int(w * 0.57)
    y_min = int(h * 0.14)
    y_max = int(h * 0.92)

    crop = gray.crop((x_min, y_min, x_max, y_max))
    cw, ch = crop.size
    raw = crop.tobytes()

    # Dem so pixel toi (< 180) tren moi cot x
    col_dark = [0] * cw
    for y in range(ch):
        row_off = y * cw
        for x in range(cw):
            if raw[row_off + x] < 180:
                col_dark[x] += 1

    # Cua so truot 9px de chon tam ranh trang rong
    half_win = 4
    center_x = cw // 2
    best_x = center_x
    best_score = float("inf")
    for x in range(half_win, cw - half_win):
        dark_sum = sum(col_dark[x - half_win : x + half_win + 1])
        # Phat nhe do lech khoi tam trang de neu ca vung deu trang thi chon dung giua ranh
        dist_penalty = abs(x - center_x) * 0.05
        score = dark_sum + dist_penalty
        if score < best_score:
            best_score = score
            best_x = x

    return x_min + best_x


def reconstruct_lines_from_words(words: list[dict]) -> list[str]:
    """Gom danh sach tu co toa do {x, y, w, h, t} trong 1 cot thanh cac dong chuan.

    Vi sao khong dung luon OcrResult.Lines cua Windows.Media.Ocr?
    Vi Windows.Media.Ocr phan vung layout (block segmentation) truoc: khi [M]/[W]
    hoac (A)/(B)/(C)/(D) nam thang hang ben trai, WinOCR hay tach chung thanh
    1 block rieng roi day xuong hoac len truoc phan loi thoai!
    Khi gom dong truc tiep bang toa do Y cua tung tu trong 1 cot don, [M]/[W] va
    (A)/(B)/(C)/(D) co cung Y voi cau thoai nen LUON nam dung dau dong do!
    """
    if not words:
        return []

    # Tinh chieu cao trung vi cua tu de lam nguong gom dong
    heights = sorted(w["h"] for w in words if w["h"] > 4)
    med_h = heights[len(heights) // 2] if heights else 18.0
    y_tol = max(8.0, med_h * 0.55)

    # Sap xep tu theo tam Y (cy = y + h/2)
    items = []
    for w in words:
        cy = w["y"] + w["h"] * 0.5
        items.append((cy, w["x"], w["w"], w["h"], w["t"]))
    items.sort(key=lambda it: (it[0], it[1]))

    # Gom cac tu co cy gan nhau vao cung 1 dong ngang
    line_clusters: list[list[tuple[float, float, float, float, str]]] = []
    for it in items:
        cy = it[0]
        if not line_clusters:
            line_clusters.append([it])
            continue
        # So voi trung binh cy cua dong hien tai (chi tinh cac tu gan X hoac toan dong)
        cur = line_clusters[-1]
        avg_cy = sum(x[0] for x in cur) / len(cur)
        if abs(cy - avg_cy) <= y_tol:
            cur.append(it)
        else:
            line_clusters.append([it])

    lines_out: list[str] = []
    for cluster in line_clusters:
        # Sap xep cac tu trong dong tu trai sang phai theo X
        cluster.sort(key=lambda it: it[1])
        line_text = " ".join(it[4] for it in cluster).strip()
        if line_text:
            lines_out.append(line_text)
    return lines_out


def run_column_split_winocr(scans: list[tuple[int, str]], force: bool = False) -> None:
    """Cat 2 cot cho 34 trang va chay Windows.Media.Ocr lay toa do tu."""
    os.makedirs(FULL_OUT_DIR, exist_ok=True)
    os.makedirs(TEMP_COLS_DIR, exist_ok=True)

    # Neu co file MinerU hop le trong MINERU_OUT_DIR va khong force, uu tien dung
    pages_to_ocr: list[tuple[int, str, str, int]] = []
    for page_num, img_path in scans:
        mineru_md = os.path.join(MINERU_OUT_DIR, f"{page_num}_tapescripts.md")
        full_md = os.path.join(FULL_OUT_DIR, f"{page_num}_tapescripts.md")
        if os.path.isfile(mineru_md) and os.path.getsize(mineru_md) > 200 and not force:
            with open(mineru_md, encoding="utf-8", errors="replace") as f:
                content = f.read()
            with open(full_md, "w", encoding="utf-8") as f:
                f.write(content)
            continue

        pil_img = Image.open(img_path)
        w, h = pil_img.size
        gutter_x = find_column_gutter(pil_img)

        # Cat cot 1 (trai) va cot 2 (phai), them 4px dem an toan quanh ranh trang
        col1_img = pil_img.crop((0, 0, min(w, gutter_x + 4), h))
        col2_img = pil_img.crop((max(0, gutter_x - 4), 0, w, h))

        c1_path = os.path.join(TEMP_COLS_DIR, f"p{page_num}_col1.png")
        c2_path = os.path.join(TEMP_COLS_DIR, f"p{page_num}_col2.png")
        col1_img.save(c1_path)
        col2_img.save(c2_path)
        pages_to_ocr.append((page_num, c1_path, c2_path, gutter_x))

    if not pages_to_ocr:
        print("Tat ca 34 trang da co san Markdown tu MinerU.")
        return

    print(f"Chay Column-Aware Windows.Media.Ocr tren {len(pages_to_ocr)} trang (68 cot)...")

    # Tao danh sach file anh de PowerShell OCR 1 lan duy nhat (nhanh, khong khoi tao lai WinRT)
    jobs_json_path = os.path.join(TEMP_COLS_DIR, "ocr_jobs.json")
    results_json_path = os.path.join(TEMP_COLS_DIR, "ocr_results.json")
    ps_script_path = os.path.join(TEMP_COLS_DIR, "run_ocr_words.ps1")

    img_list = []
    for page_num, c1_path, c2_path, _ in pages_to_ocr:
        full_img_path = os.path.join(REF_SCANS_DIR, f"tapescript_p{page_num}.png")
        img_list.append({"key": f"{page_num}_full", "path": full_img_path})
        img_list.append({"key": f"{page_num}_1", "path": c1_path})
        img_list.append({"key": f"{page_num}_2", "path": c2_path})

    with open(jobs_json_path, "w", encoding="utf-8") as f:
        json.dump(img_list, f, indent=2)

    ps_code = r"""
param([string]$JobsPath, [string]$OutPath)
$ErrorActionPreference = 'Stop'
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
$lang = $avail | Where-Object { $_.LanguageTag -like 'en*' } | Select-Object -First 1
if (-not $lang) { $lang = $avail[0] }
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($lang)

$jobs = Get-Content -Raw -Encoding UTF8 $JobsPath | ConvertFrom-Json
$outMap = @{}

foreach ($j in $jobs) {
    $file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($j.path)) ([Windows.Storage.StorageFile])
    $stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
    $decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
    $bitmap = Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
    $res = Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
    $words = New-Object System.Collections.Generic.List[object]
    foreach ($ln in $res.Lines) {
        foreach ($w in $ln.Words) {
            $r = $w.BoundingRect
            $words.Add(@{
                x = [Math]::Round($r.X, 1)
                y = [Math]::Round($r.Y, 1)
                w = [Math]::Round($r.Width, 1)
                h = [Math]::Round($r.Height, 1)
                t = $w.Text
            })
        }
    }
    $outMap[$j.key] = $words
    $stream.Dispose()
}

$json = $outMap | ConvertTo-Json -Depth 5 -Compress
[System.IO.File]::WriteAllText($OutPath, $json, [System.Text.Encoding]::UTF8)
"""
    with open(ps_script_path, "w", encoding="utf-8") as f:
        f.write(ps_code)

    r = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            ps_script_path,
            "-JobsPath",
            jobs_json_path,
            "-OutPath",
            results_json_path,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0 or not os.path.isfile(results_json_path):
        raise RuntimeError(f"PowerShell WinOCR that bai:\n{r.stdout}")

    with open(results_json_path, encoding="utf-8-sig") as f:
        ocr_data = json.load(f)

    for page_num, c1_path, c2_path, gutter_x in pages_to_ocr:
        w_full = ocr_data.get(f"{page_num}_full", [])
        w1 = list(ocr_data.get(f"{page_num}_1", []))
        w2 = list(ocr_data.get(f"{page_num}_2", []))

        col2_x_off = max(0, gutter_x - 4)
        for wf in w_full:
            cx = wf["x"] + wf["w"] * 0.5
            if cx < gutter_x:
                target_list = w1
                cand = dict(wf)
            else:
                target_list = w2
                cand = dict(wf, x=round(wf["x"] - col2_x_off, 1))

            # Kiem tra xem tu nay da co trong ket qua OCR cot chua
            cand_cy = cand["y"] + cand["h"] * 0.5
            already = False
            for wc in target_list:
                wc_cy = wc["y"] + wc["h"] * 0.5
                if abs(cand_cy - wc_cy) <= max(10.0, min(cand["h"], wc["h"]) * 0.6):
                    ox = min(cand["x"] + cand["w"], wc["x"] + wc["w"]) - max(cand["x"], wc["x"])
                    if ox > -3.0:
                        already = True
                        break
            if not already:
                target_list.append(cand)

        lines1 = reconstruct_lines_from_words(w1)
        lines2 = reconstruct_lines_from_words(w2)

        out_md = os.path.join(FULL_OUT_DIR, f"{page_num}_tapescripts.md")
        combined = lines1 + [""] + lines2
        with open(out_md, "w", encoding="utf-8") as f:
            f.write("\n".join(combined) + "\n")

        # Xoa file anh cot tam de giu thu muc gon gang
        for p_tmp in (c1_path, c2_path):
            if os.path.isfile(p_tmp):
                os.remove(p_tmp)

    for p_tmp in (jobs_json_path, results_json_path, ps_script_path):
        if os.path.isfile(p_tmp):
            os.remove(p_tmp)
    try:
        os.rmdir(TEMP_COLS_DIR)
    except OSError:
        pass

    print(f"Hoan tat xuat 34 file Markdown chuan 2 cot vao {FULL_OUT_DIR}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mineru-all", action="store_true", help="Chay MinerU tren ca 34 trang")
    ap.add_argument("--fallback-ocr", action="store_true", help="Chay thang Column-Aware WinOCR")
    ap.add_argument("--force", action="store_true", help="Ghi de file da co")
    args = ap.parse_args()

    scans = extract_scans(force=args.force)

    if not args.fallback_ocr:
        print("Thu goi mineru-kit.exe tren trang 340...")
        ok_test, msg = try_mineru_page(scans[0][0], scans[0][1])
        if ok_test:
            print(f"  [OK] MinerU chay duoc: {msg}")
            if args.mineru_all:
                for p_num, img_path in scans[1:]:
                    ok_p, msg_p = try_mineru_page(p_num, img_path)
                    print(f"  Trang {p_num}: {'OK' if ok_p else 'LOI'} - {msg_p}")
        else:
            print(f"  [THONG BAO] MinerU bi chan hoac loi trong sandbox:\n{msg}")
            print("  -> Chuyen sang pipeline Column-Aware Split + Word-Coordinate WinOCR...")

    run_column_split_winocr(scans, force=args.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
