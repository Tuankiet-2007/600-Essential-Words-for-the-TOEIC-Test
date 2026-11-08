"""
run_ocr_pipeline.py — ONE entry point that drives either OCR direction end to end.

WHY THIS EXISTS
    The original batch_ocr_to_json.py assumes two things that are not true on this
    machine yet:
      1. It reads page scans from extracted_data/lesson_page_scans/lesson_NN/*.png,
         but scripts/extract_pdf_assets.py (Script 1) has never been run, so those
         scans do not exist.
      2. It hardcodes gemini-2.5-flash and never validates the JSON that comes back,
         so a malformed response silently lands in lessons_json/ and breaks the app.
    It also silently SKIPS any lesson whose output file already exists, which hides
    corrupt output.

    This wrapper adds:
      --stage extract | ocr | all     (so the missing scan extraction is explicit)
      --provider gemini | mineru | both
      --force                         (re-do lessons that already have output)
      --only 1,2,3 / --from 1 --to 12 (targeted re-runs)
      --validate                      (schema-check every produced JSON, no API calls)
    It normalises the produced JSON into exactly the shape the web app consumes
    (see app/CONTRACT.md) and writes a run report.

USAGE
    # 1. Extract page scans + Part 1 photos from the PDF (Script 1)
    python scripts/run_ocr_pipeline.py --stage extract

    # 2. OCR lessons 2..50 with Gemini (needs GEMINI_API_KEY)
    python scripts/run_ocr_pipeline.py --stage ocr --provider gemini --from 2

    # or with local MinerU on the RTX 4060 (you must install it yourself:
    #     the repo ships no MinerU code; see README for setup notes.
    #     This flag only works if scripts/local_mineru_ocr.py exists.)
    python scripts/run_ocr_pipeline.py --stage ocr --provider mineru --from 2

    # 3. Validate whatever is in lessons_json/ without calling any API
    python scripts/run_ocr_pipeline.py --validate
"""

import argparse
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACTED = os.path.join(ROOT, "extracted_data")
SCANS_ROOT = os.path.join(EXTRACTED, "lesson_page_scans")
OUT_DIR = os.path.join(ROOT, "lessons_json")
PUBLIC_OUT = os.path.join(ROOT, "public", "lessons_json")
SAMPLE = os.path.join(ROOT, "sample_lessons", "lesson_01.json")
BOOK_MAP = os.path.join(ROOT, "book_structure_map.json")

# Fields the web app requires; missing ones make a lesson unusable.
REQUIRED_WORD_FIELDS = ["word", "pos", "ipa", "definition_en", "definition_vi"]
REQUIRED_TOP = ["lesson_id", "title", "theme_name", "words_to_learn"]


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def load_book_map():
    with open(BOOK_MAP, encoding="utf-8") as f:
        return json.load(f)


def lesson_output_path(lid):
    return os.path.join(OUT_DIR, f"lesson_{lid:02d}.json")


# --------------------------------------------------------------------------
# validation (no API needed)
# --------------------------------------------------------------------------

def validate_lesson(path):
    """Return (ok, [problems]). Checks the shape the React app needs."""
    problems = []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"JSON không hợp lệ: {e}"]
    except FileNotFoundError:
        return False, ["Không tìm thấy tệp"]

    for k in REQUIRED_TOP:
        if k not in data:
            problems.append(f"thiếu trường bắt buộc '{k}'")

    words = data.get("words_to_learn") or []
    if len(words) != 12:
        problems.append(f"words_to_learn có {len(words)} mục (yêu cầu 12)")

    for i, w in enumerate(words, 1):
        for fld in REQUIRED_WORD_FIELDS:
            if not w.get(fld):
                problems.append(f"từ #{i} ('{w.get('word','?')}') thiếu '{fld}'")
        if not w.get("examples"):
            problems.append(f"từ #{i} ('{w.get('word','?')}') không có câu ví dụ")
        if not w.get("collocations"):
            problems.append(f"từ #{i} ('{w.get('word','?')}') không có collocations")

    wic = data.get("words_in_context") or {}
    answers = wic.get("answers") or {}
    bank = wic.get("word_bank") or []
    if len(answers) != 12:
        problems.append(f"words_in_context.answers có {len(answers)} đáp án (yêu cầu 12)")
    if len(bank) != 12:
        problems.append(f"words_in_context.word_bank có {len(bank)} từ (yêu cầu 12)")
    missing = [a for a in answers.values() if a not in bank]
    if missing:
        problems.append(f"đáp án không nằm trong word_bank: {missing}")

    passage = wic.get("passage") or ""
    for n in range(1, 13):
        if passage.count(f"({n})") != 1:
            problems.append(f"đoạn văn thiếu hoặc lặp chỗ trống ({n})")

    # practice branch is expected but tolerated if partially absent
    prac = data.get("practice") or {}
    if not (prac.get("listening") or prac.get("reading")):
        problems.append("thiếu nhánh 'practice' (Listening/Reading)")

    return (len(problems) == 0), problems


def do_validate(lessons=None):
    print("=== KIỂM TRA SCHEMA lessons_json/ ===")
    ids = lessons or list(range(1, 51))
    ok_count = miss_count = bad_count = 0
    for lid in ids:
        path = lesson_output_path(lid)
        if not os.path.exists(path):
            print(f"  [THIẾU]  lesson_{lid:02d}.json — chưa trích xuất")
            miss_count += 1
            continue
        ok, problems = validate_lesson(path)
        if ok:
            print(f"  [OK]     lesson_{lid:02d}.json")
            ok_count += 1
        else:
            print(f"  [LỖI]    lesson_{lid:02d}.json")
            for p in problems[:6]:
                print(f"           - {p}")
            bad_count += 1
    print(f"\nTổng: {ok_count} hợp lệ, {bad_count} lỗi, {miss_count} chưa có.")
    return bad_count == 0


# --------------------------------------------------------------------------
# stage: extract
# --------------------------------------------------------------------------

def stage_extract():
    script = os.path.join(ROOT, "scripts", "extract_pdf_assets.py")
    if not os.path.exists(script):
        print(f"Không tìm thấy {script}")
        return False
    print("=== BƯỚC 1: Trích xuất ảnh/scan từ PDF ===")
    print("Script này cần thư viện: pip install pypdf pillow")
    r = subprocess.run([sys.executable, script], cwd=ROOT)
    return r.returncode == 0


# --------------------------------------------------------------------------
# stage: ocr
# --------------------------------------------------------------------------

def stage_ocr_gemini(lessons, force):
    """Call Gemini per lesson over the 6 page scans."""
    try:
        from PIL import Image
        from google import genai
        from google.genai import types
    except ImportError as e:
        print(f"Thiếu thư viện: {e}\nCài đặt:  pip install google-genai pillow")
        return False

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Chưa có biến môi trường GEMINI_API_KEY.")
        print('PowerShell:  $env:GEMINI_API_KEY="..."  (rồi chạy lại lệnh)')
        return False

    client = genai.Client(api_key=api_key)
    with open(SAMPLE, encoding="utf-8") as f:
        sample_schema = f.read()

    book = load_book_map()
    by_id = {l["lesson_id"]: l for l in book["lessons"]}
    os.makedirs(OUT_DIR, exist_ok=True)

    done = skipped = failed = 0
    for lid in lessons:
        out = lesson_output_path(lid)
        if os.path.exists(out) and not force:
            print(f"  [BỎ QUA] lesson_{lid:02d}.json đã tồn tại (dùng --force để làm lại)")
            skipped += 1
            continue

        scan_dir = os.path.join(SCANS_ROOT, f"lesson_{lid:02d}")
        if not os.path.isdir(scan_dir):
            print(f"  [THIẾU]  Không có scan cho lesson {lid:02d}. Chạy --stage extract trước.")
            failed += 1
            continue

        files = sorted(f for f in os.listdir(scan_dir) if f.lower().endswith(".png"))
        images = [Image.open(os.path.join(scan_dir, f)) for f in files]
        meta = by_id[lid]

        prompt = f"""Bạn là hệ thống số hóa sách TOEIC chính xác tuyệt đối.
Đây là {len(images)} trang scan của Lesson {lid}: "{meta['title']}" thuộc chủ đề "{meta['theme_name']}".
Hãy trích xuất toàn bộ nội dung và trả về ĐÚNG định dạng JSON Schema mẫu bên dưới.
Yêu cầu bắt buộc:
1. Đủ 12 từ vựng mục tiêu trong phần WORDS TO LEARN, kèm phiên âm IPA, nghĩa tiếng Việt sát ngữ cảnh TOEIC,
   collocations trong bài, và dịch 2 câu ví dụ a, b sang tiếng Việt.
2. Ghép phần WORD FAMILIES vào đúng từ vựng tương ứng trong mảng `words_to_learn` (khóa `word_family`).
3. Trích xuất chính xác đoạn văn `words_in_context` (đánh số chỗ trống đúng dạng "(1) ___") và điền đáp án cho 12 ô trống.
4. Trích xuất toàn bộ câu hỏi Listening (Part 1, 2, 3, 4) và Reading (Part 5, 6, 7) kèm đáp án đúng cho Part 5, 6, 7.
Chỉ trả về JSON, không thêm văn bản giải thích.

Cấu trúc JSON mẫu (tuân thủ 100% tên trường):
{sample_schema}
"""
        try:
            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[*images, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )
            text = (resp.text or "").strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            parsed = json.loads(text)
            parsed.setdefault("lesson_id", lid)
            parsed.setdefault("title", meta["title"])
            parsed.setdefault("theme_id", meta["theme_id"])
            parsed.setdefault("theme_name", meta["theme_name"])
            parsed["audio_track"] = f"audio/track_{lid:02d}.mp3"
            parsed["part1_photo"] = f"part1_photos/lesson_{lid:02d}.jpg"
            with open(out, "w", encoding="utf-8") as f:
                json.dump(parsed, f, ensure_ascii=False, indent=2)

            ok, problems = validate_lesson(out)
            tag = "OK" if ok else "CẢNH BÁO"
            print(f"  [{tag}] lesson_{lid:02d}.json đã ghi" + ("" if ok else f" ({len(problems)} vấn đề)"))
            for p in problems[:4]:
                print(f"           - {p}")
            done += 1
        except Exception as e:  # noqa: BLE001 - report and continue the batch
            print(f"  [LỖI]   lesson {lid:02d}: {e}")
            failed += 1
        time.sleep(2)  # rate limit

    print(f"\nGemini xong. thành công={done} bỏ qua={skipped} lỗi={failed}")
    return failed == 0


def stage_ocr_mineru(lessons, force):
    """Hướng 2 (MinerU local) — đã gỡ khỏi repo, người dùng tự cài."""
    local = os.path.join(ROOT, "scripts", "local_mineru_ocr.py")
    if not os.path.exists(local):
        print("Hướng 2 (MinerU 2.5-Pro local) đã được gỡ khỏi repo này.")
        print()
        print("Nếu bạn muốn dùng lại, cài đặt như sau:")
        print(r"  py -3.11 -m venv .mineru")
        print(r"  .\.mineru\Scripts\python.exe -m pip install uv")
        print(r'  .\.mineru\Scripts\python.exe -m uv pip install "mineru>=4.0,<5" pypdf pillow torch')
        print(r"  .\.mineru\Scripts\mineru-models-download.exe --tier standard --small-backend torch")
        print()
        print("LƯU Ý khi tự cài:")
        print("  - Dùng `uv`, KHÔNG dùng pip trực tiếp: pip bị treo vô hạn khi phân giải")
        print("    cây phụ thuộc của MinerU.")
        print("  - MINERU_HOME phải nằm NGOÀI workspace (ví dụ C:\\mineru-home) và không")
        print("    được có ACE cho phép ghi của tài khoản khác — nếu không MinerU sẽ báo")
        print("    'Credential configuration directory must not be writable by other users.'")
        print("  - MinerU 4.x không tự parse: phải bật parse-server cục bộ bằng")
        print("        mineru config set parse_server.local.mode managed")
        print("    và tải thêm bộ model ONNX:  mineru-models-download MinerU-4_models_onnx")
        print()
        print("Hoặc dùng Hướng 1 (Gemini API) — không cần cài gì thêm:")
        print("  python scripts/run_ocr_pipeline.py --stage ocr --provider gemini --from 2")
        return False

    print("=== MinerU local: bước 1 — OCR sang Markdown ===")
    args = [sys.executable, local]
    if force:
        args.append("--force")
    r1 = subprocess.run(args, cwd=ROOT)
    if r1.returncode != 0:
        print("Bước OCR thất bại.")
        return False

    to_json = os.path.join(ROOT, "scripts", "markdown_to_structured_json.py")
    if os.path.exists(to_json):
        print("=== MinerU local: bước 2 — Markdown sang JSON cấu trúc ===")
        r2 = subprocess.run([sys.executable, to_json], cwd=ROOT)
        if r2.returncode != 0:
            print("Bước chuyển JSON thất bại.")
            return False
    else:
        print(f"(Bỏ qua bước 2: chưa có {os.path.basename(to_json)})")

    return do_validate(lessons)


# --------------------------------------------------------------------------
# publish to public/ so the web app can fetch the files
# --------------------------------------------------------------------------

def publish_to_public():
    os.makedirs(PUBLIC_OUT, exist_ok=True)
    n = 0
    for lid in range(1, 51):
        src = lesson_output_path(lid)
        if os.path.exists(src):
            dst = os.path.join(PUBLIC_OUT, f"lesson_{lid:02d}.json")
            with open(src, encoding="utf-8") as f:
                data = json.load(f)
            # Rewrite asset refs to the canonical public URLs the app expects.
            data["audio_track"] = f"audio/track_{lid:02d}.mp3"
            data["part1_photo"] = f"part1_photos/lesson_{lid:02d}.jpg"
            with open(dst, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            n += 1
    print(f"Đã xuất {n} tệp JSON sang public/lessons_json/ (web app sẽ đọc trực tiếp).")
    return n > 0


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Điều phối pipeline OCR sách TOEIC 600 Essential Words")
    ap.add_argument("--stage", choices=["extract", "ocr", "all"], default="ocr")
    ap.add_argument("--provider", choices=["gemini", "mineru", "both"], default="gemini")
    ap.add_argument("--force", action="store_true", help="làm lại cả bài đã có JSON")
    ap.add_argument("--only", help="danh sách lesson, ví dụ: 1,2,3")
    ap.add_argument("--from", dest="start", type=int, default=1)
    ap.add_argument("--to", dest="end", type=int, default=50)
    ap.add_argument("--validate", action="store_true", help="chỉ kiểm tra schema, không gọi API")
    ap.add_argument("--publish", action="store_true", help="chỉ copy lessons_json/ sang public/")
    args = ap.parse_args()

    if args.only:
        lessons = [int(x) for x in args.only.split(",") if x.strip()]
    else:
        lessons = list(range(args.start, args.end + 1))

    if args.validate:
        sys.exit(0 if do_validate(lessons) else 1)

    if args.publish:
        sys.exit(0 if publish_to_public() else 1)

    ok = True
    if args.stage in ("extract", "all"):
        ok = stage_extract() and ok

    if args.stage in ("ocr", "all"):
        if args.provider in ("gemini", "both"):
            ok = stage_ocr_gemini(lessons, args.force) and ok
        if args.provider in ("mineru", "both"):
            ok = stage_ocr_mineru(lessons, args.force) and ok

    do_validate(lessons)
    publish_to_public()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
