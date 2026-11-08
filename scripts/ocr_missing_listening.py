"""ocr_missing_listening.py — OCR lai cac trang listening da duoc extract DUNG (full page).

BOI CANH / VI SAO CAN SCRIPT NAY
--------------------------------
`extract_pdf_assets.py` truoc day chon anh scan bang:
    full_scan = max(pg.images, key=lambda x: len(x.data))
tuc la chon anh co NHIEU BYTE NHAT. Nhung anh Part 1 Photo nhung trong trang la
JPEG nen nang hon ban scan toan trang (TIFF). Ket qua: 37/50 trang
"listening_practice" bi luu nham thanh ANH PART 1 PHOTO (~300x312 px) thay vi ca
trang (~1456x2000 px).

MinerU OCR mot buc anh chup buc anh -> khong co chu -> tra ve rong. Vi vay 37 bai
mat TOAN BO cau hoi Part 3/Part 4 du sach in rat ro (xem anh scan trang Part 3
Conversation / Part 4 Talk).

Da sua `extract_pdf_assets.py::pick_full_page_scan()` de chon theo DIEN TICH
PIXEL. Script nay lam buoc tiep theo: OCR lai 37 trang do bang MinerU.

CACH DUNG
---------
    py -3.11 scripts/ocr_missing_listening.py [--force] [--only 2,4,5]

Ghi ket qua ve:
    extracted_data/mineru_md/lesson_NN/listening_practice.md
(tuc la dung noi `convert_available_lessons.py` doc.)

LUU Y MOI TRUONG
----------------
MinerU can ghi lock/model cache trong thu muc cai dat cua no
(TOOL_ROOT\\home\\models\\.locks) — nam NGOAI workspace. Trong sandbox
workspace-write, buoc nay se bi chan voi [WinError 5] Access is denied. Hay chay
lenh nay voi quyen rong hon.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCANS = os.path.join(ROOT, "extracted_data", "lesson_page_scans")
MD_ROOT = os.path.join(ROOT, "extracted_data", "mineru_md")
STAGE = os.path.join(ROOT, "extracted_data", "ocr_stage")
TOOL_ROOT = r"D:\CODE\vibecode\TOOL\mineru"
MINERU_KIT = os.path.join(TOOL_ROOT, ".venv", "Scripts", "mineru-kit.exe")


def mineru_env():
    """Moi truong y het cac file .cmd cua ban cai MinerU."""
    env = dict(os.environ)
    env["MINERU_HOME"] = os.path.join(TOOL_ROOT, "home")
    env["MINERU_MODEL_VLM_ENGINE"] = "llama-cpp"
    env["UV_CACHE_DIR"] = os.path.join(TOOL_ROOT, ".cache", "uv")
    env["UV_PYTHON_INSTALL_DIR"] = os.path.join(TOOL_ROOT, ".python")
    env["HF_HOME"] = os.path.join(TOOL_ROOT, ".cache", "huggingface")
    env["MODELSCOPE_CACHE"] = os.path.join(TOOL_ROOT, ".cache", "modelscope")
    env["VIRTUAL_ENV"] = os.path.join(TOOL_ROOT, ".venv")
    tmp = os.path.join(TOOL_ROOT, ".tmp")
    os.makedirs(tmp, exist_ok=True)
    env["TMP"] = tmp
    env["TEMP"] = tmp
    env["PATH"] = os.path.join(TOOL_ROOT, ".venv", "Scripts") + os.pathsep + env.get("PATH", "")
    return env


def need_ocr(lid):
    """True khi trang listening cua bai nay CHUA co chu (<=50 byte)."""
    md = os.path.join(MD_ROOT, f"lesson_{lid:02d}", "listening_practice.md")
    return not os.path.isfile(md) or os.path.getsize(md) <= 50


def scan_path(lid):
    d = os.path.join(SCANS, f"lesson_{lid:02d}")
    if not os.path.isdir(d):
        return None
    for f in sorted(os.listdir(d)):
        if f.endswith("_listening_practice.png"):
            return os.path.join(d, f)
    return None


def strip_base64(text):
    """Bo anh base64 nhung trong Markdown (khong mat chu nao)."""
    text = re.sub(r"!\[[^\]]*\]\(data:image[^)]*\)", "", text, flags=re.S)
    text = re.sub(r"data:image/[a-zA-Z+]+;base64,[A-Za-z0-9+/=\s]+", "", text)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="OCR lai ca 50 bai, khong chi nhung bai con thieu")
    ap.add_argument("--only", default="",
                    help="Chi dinh danh sach bai, vd: 2,4,5")
    args = ap.parse_args()

    if args.only:
        ids = [int(x) for x in args.only.split(",") if x.strip()]
    else:
        ids = [lid for lid in range(1, 51) if args.force or need_ocr(lid)]

    if not ids:
        print("Khong co bai nao can OCR (tat ca da co chu).")
        return 0
    if not os.path.isfile(MINERU_KIT):
        print(f"LOI: khong thay mineru-kit tai {MINERU_KIT}")
        return 1
    print(f"Can OCR {len(ids)} trang listening: {ids}")

    # ---- 1. Stage anh -----------------------------------------------------
    if os.path.isdir(STAGE):
        shutil.rmtree(STAGE)
    os.makedirs(STAGE, exist_ok=True)
    staged = {}
    for lid in ids:
        src = scan_path(lid)
        if not src:
            print(f"  [BO QUA] L{lid:02d}: khong thay anh scan")
            continue
        dst = os.path.join(STAGE, f"lesson_{lid:02d}_listening.png")
        shutil.copy2(src, dst)
        staged[lid] = dst
    print(f"Da stage {len(staged)} anh -> {os.path.relpath(STAGE, ROOT)}")

    # ---- 2. OCR tung trang ------------------------------------------------
    env = mineru_env()
    results = {}
    for lid in sorted(staged):
        img = staged[lid]
        tmp_out = os.path.join(STAGE, f"out_{lid:02d}.md")
        try:
            p = subprocess.run(
                [MINERU_KIT, "parse", img, "-o", tmp_out, "--tier", "standard"],
                cwd=TOOL_ROOT, env=env, timeout=600,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace",
            )
        except subprocess.TimeoutExpired:
            print(f"  [LOI] L{lid:02d}: qua thoi gian cho")
            continue

        if not os.path.isfile(tmp_out):
            tail = (p.stdout or "").strip().splitlines()[-2:]
            print(f"  [LOI] L{lid:02d}: khong tao duoc file")
            for ln in tail:
                print(f"        {ln[:150]}")
            continue

        text = strip_base64(open(tmp_out, encoding="utf-8", errors="replace").read()).strip()
        n_parts = len(re.findall(r"Part\s*[34]\b", text))
        if len(text) < 40:
            print(f"  [CANH BAO] L{lid:02d}: chi {len(text)} ky tu chu")
            continue
        results[lid] = text
        print(f"  [OK] L{lid:02d}: {len(text)} ky tu, {n_parts} tieu de Part 3/4")

    # ---- 3. Ghi ket qua ---------------------------------------------------
    written = 0
    for lid, text in results.items():
        d = os.path.join(MD_ROOT, f"lesson_{lid:02d}")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "listening_practice.md"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(text + "\n")
        written += 1

    print(f"\nDa ghi {written}/{len(staged)} file Markdown.")
    if written < len(staged):
        print("Mot so trang that bai — KHONG am tham bo qua.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
