"""Sinh bang kiem tra Part 3 / Part 4 Listening sau khi chay lai converter.

Kiem tra:
  1. MOI bai (50) phai co listening.part3 va listening.part4 (key ton tai,
     o CAP CAO NHAT `lesson.listening` — noi lessonLoader.js doc).
  2. Bang: Lesson | has text | part3 count | part4 count | part3 numbers | part4 numbers
  3. listening.questions (flat) == part3 + part4: cung so cau, cung thu tu,
     va cung NOI DUNG (so sanh ca object, khong chi so hieu cau hoi).
  4. Ghim THU TU IN cua ca 50 bai (21 bai in Part 3 khong tang dan) — day la
     bang chung parser tach theo TIEU DE Part chu khong theo khoang so.
  5. Doi chieu scripts/reports/baseline_before_part_fix.json, BAT KY hoi quy nao o
     words / examples / family / bank / blanks / listening_questions deu bi flag.
  6. Ky vong: CA 50 bai deu co part3=3 & part4=3.
     (Ky vong cu 13/37 da loi thoi — xem chu thich o EXPECTED_WITH_QUESTIONS.)

Chay:  py -3.11 scripts/reports/verify_listening_parts.py
Thoat khac 0 neu co bat ky assertion nao that bai.
Ghi bang ra: scripts/reports/listening_parts_report.md
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PUBLIC_OUT = os.path.join(ROOT, "public", "lessons_json")
REPORT_DIR = os.path.join(ROOT, "scripts", "reports")
BASELINE = os.path.join(REPORT_DIR, "baseline_before_part_fix.json")
REPORT_MD = os.path.join(REPORT_DIR, "listening_parts_report.md")

N_LESSONS = 50

# KY VONG HIEN TAI (task-5, sau khi sua goc `pick_full_page_scan` chon anh scan
# theo DIEN TICH PIXEL thay vi so byte):
# CA 50 bai deu co cau hoi Part 3/Part 4, part3=3 & part4=3.
# Ky vong cu (13 bai co cau hoi / 37 bai 0-0) da LOI THOI: 37 bai kia tung bi OCR
# rong vi anh scan bi luu nham thanh anh Part 1 Photo (~300x312px) thay vi ca
# trang (~1456x2000px). Da OCR lai 37 trang, gio deu co du lieu that.
EXPECTED_WITH_QUESTIONS = list(range(1, N_LESSONS + 1))
EXPECTED_PART3 = 3
EXPECTED_PART4 = 3

# Ghim THU TU IN trong sach. Day moi la thu phan biet "cat theo tieu de Part"
# voi "cat theo khoang so cau hoi": so luong 3/3 giong nhau o CA HAI cach, chi
# thu tu moi khac. Neu cat theo khoang so thi MOI bai deu ra 4,5,6 / 7,8,9.
#
# 21/50 bai in Part 3 KHONG tang dan (4,6,5). Ghim het 21 bai, khong chi vai
# bai dai dien — day la hoi quy that su, khong duoc noi long.
NON_ASCENDING_PART3 = [1, 3, 4, 6, 10, 12, 13, 15, 19, 20, 29, 30, 31,
                       33, 34, 36, 40, 43, 44, 45, 49]
# 1 bai in Part 4 khong tang dan: lesson_03 -> 7,9,8.
NON_ASCENDING_PART4 = {3: [7, 9, 8]}

ORDER_PINS = {
    lid: {
        "part3": [4, 6, 5] if lid in NON_ASCENDING_PART3 else [4, 5, 6],
        "part4": NON_ASCENDING_PART4.get(lid, [7, 8, 9]),
    }
    for lid in range(1, N_LESSONS + 1)
}

REGRESSION_FIELDS = ("words", "examples", "family", "bank", "blanks",
                     "listening_questions")

problems = []      # assertion that bai -> exit non-zero
warnings = []      # canh bao khong phai assertion that bai


def fail(msg):
    problems.append(msg)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def measure(d):
    """Cac chi so dung chung cho ca snapshot va ban hien tai."""
    words = d.get("words_to_learn") or []
    ctx = d.get("words_in_context") or {}
    lis = d.get("listening") or {}
    return {
        "words": len(words),
        "examples": sum(len(w.get("examples") or []) for w in words),
        "family": sum(len(w.get("word_family") or []) for w in words),
        "bank": len(ctx.get("word_bank") or []),
        "blanks": len(ctx.get("blanks") or []),
        "listening_questions": len(lis.get("questions") or []),
    }


def nums(seq):
    return [q.get("number") for q in seq]


def main():
    # ---------------------------------------------------------------- du lieu
    lessons = {}
    for lid in range(1, N_LESSONS + 1):
        p = os.path.join(PUBLIC_OUT, f"lesson_{lid:02d}.json")
        if not os.path.isfile(p):
            fail(f"L{lid:02d}: THIEU file {os.path.relpath(p, ROOT)}")
            continue
        try:
            lessons[lid] = load_json(p)
        except Exception as e:                                  # noqa: BLE001
            fail(f"L{lid:02d}: JSON khong doc duoc ({e})")

    if len(lessons) != N_LESSONS:
        fail(f"Chi doc duoc {len(lessons)}/{N_LESSONS} file JSON")

    baseline = None
    if os.path.isfile(BASELINE):
        baseline = load_json(BASELINE)
    else:
        fail(f"Khong thay baseline: {os.path.relpath(BASELINE, ROOT)} "
             "(chay scripts/reports/snapshot_baseline.py truoc)")

    # ------------------------------------------------------------- kiem tra
    rows = []
    with_text, without_text = [], []
    flat_ne_part = []
    regressions = []

    for lid in sorted(lessons):
        d = lessons[lid]
        # (c) app/src/lib/lessonLoader.js doc `lesson.listening` o CAP CAO NHAT.
        # part3/part4 phai nam o do, khong duoc chi nam trong practice.listening.
        tl_lis = d.get("listening")
        if not isinstance(tl_lis, dict):
            fail(f"L{lid:02d}: khong co TOP-LEVEL 'listening' object "
                 "(lessonLoader.js doc lesson.listening truoc)")
            continue
        if not ("part3" in tl_lis and "part4" in tl_lis):
            nested = (d.get("practice") or {}).get("listening") or {}
            if "part3" in nested or "part4" in nested:
                fail(f"L{lid:02d}: part3/part4 chi nam trong practice.listening "
                     "-> app se KHONG doc duoc")
        lis = tl_lis

        has_p3 = "part3" in lis
        has_p4 = "part4" in lis
        if not has_p3:
            fail(f"L{lid:02d}: THIEU key listening.part3")
        if not has_p4:
            fail(f"L{lid:02d}: THIEU key listening.part4")

        p3 = lis.get("part3") if isinstance(lis.get("part3"), list) else []
        p4 = lis.get("part4") if isinstance(lis.get("part4"), list) else []
        flat = lis.get("questions") if isinstance(lis.get("questions"), list) else []

        # 3. flat == part3 + part4 (cung so, cung thu tu)
        expect_flat = nums(p3) + nums(p4)
        if nums(flat) != expect_flat:
            flat_ne_part.append(lid)
            fail(f"L{lid:02d}: flat listening.questions != part3+part4 "
                 f"(flat={nums(flat)} vs part3+part4={expect_flat})")
        # So sanh sau hon ca noi dung cau hoi, khong chi so hieu.
        if json.dumps(flat, ensure_ascii=False, sort_keys=True) != \
           json.dumps(p3 + p4, ensure_ascii=False, sort_keys=True):
            flat_ne_part.append(lid)
            fail(f"L{lid:02d}: noi dung part3+part4 KHAC flat questions "
                 "(cung so nhung khac du lieu)")

        text_len = len((lis.get("instructions") or "").strip())
        if flat:
            with_text.append(lid)
        else:
            without_text.append(lid)

        rows.append({
            "lesson": lid,
            "has_text": bool(flat),
            "text_len": text_len,
            "part3": len(p3),
            "part4": len(p4),
            "p3_numbers": nums(p3),
            "p4_numbers": nums(p4),
            "flat": nums(flat),
            "keys": sorted(lis.keys()),
        })

        # 4. regression vs baseline
        if baseline and f"{lid:02d}" in baseline.get("lessons", {}):
            base = baseline["lessons"][f"{lid:02d}"]
            cur = measure(d)
            for f in REGRESSION_FIELDS:
                if base.get(f) != cur.get(f):
                    direction = "GIAM" if (cur.get(f) or 0) < (base.get(f) or 0) else "TANG"
                    regressions.append({
                        "lesson": lid, "field": f,
                        "before": base.get(f), "after": cur.get(f),
                        "direction": direction})

    # ------------------------------------------- ky vong: CA 50 bai deu co
    if with_text != EXPECTED_WITH_QUESTIONS:
        extra = [x for x in with_text if x not in EXPECTED_WITH_QUESTIONS]
        miss = [x for x in EXPECTED_WITH_QUESTIONS if x not in with_text]
        fail(f"Danh sach bai co cau hoi SAI: co {len(with_text)} bai "
             f"(ky vong {len(EXPECTED_WITH_QUESTIONS)}); thua={extra} thieu={miss}")

    for r in rows:
        if r["part3"] != EXPECTED_PART3 or r["part4"] != EXPECTED_PART4:
            fail(f"L{r['lesson']:02d}: part3={r['part3']} part4={r['part4']}, "
                 f"ky vong {EXPECTED_PART3}/{EXPECTED_PART4} — "
                 f"xem _raw.listening_practice")
        if not r["has_text"]:
            fail(f"L{r['lesson']:02d}: KHONG co cau hoi nao "
                 "(sach co in Part 3/Part 4 cho ca 50 bai)")
        elif r["text_len"] == 0:
            warnings.append(f"L{r['lesson']:02d}: co cau hoi nhung instructions rong")

    # Regression: giam la loi, tang chi la canh bao (thong tin).
    for g in regressions:
        if g["direction"] == "GIAM":
            fail(f"HOI QUY L{g['lesson']:02d}.{g['field']}: "
                 f"{g['before']} -> {g['after']} (GIAM)")
        else:
            warnings.append(f"L{g['lesson']:02d}.{g['field']}: "
                            f"{g['before']} -> {g['after']} (tang)")

    # ------------------------------------------- ghim THU TU IN (order pins)
    pin_results = []
    for lid, want in sorted(ORDER_PINS.items()):
        if lid not in lessons:
            continue
        lis = lessons[lid].get("listening") or {}
        got3 = nums(lis.get("part3") or [])
        got4 = nums(lis.get("part4") or [])
        ok = got3 == want["part3"] and got4 == want["part4"]
        pin_results.append({"lesson": lid, "want3": want["part3"],
                            "got3": got3, "want4": want["part4"],
                            "got4": got4, "ok": ok})
        if not ok:
            fail(f"L{lid:02d}: THU TU IN SAI — part3 {got3} (ky vong "
                 f"{want['part3']}), part4 {got4} (ky vong {want['part4']})")

    # ------------------------------- moi bai phai co markdown nghe khong rong
    # L17 tung la file 9 byte chi chua rac OCR "!IITIIP"; sau khi OCR lai 37 trang
    # gio la du lieu THAT (Part 3: 4,5,6 / Part 4: 7,8,9). Khong con file rac.
    md_empty = []
    for lid in range(1, N_LESSONS + 1):
        p = os.path.join(ROOT, "extracted_data", "mineru_md",
                         f"lesson_{lid:02d}", "listening_practice.md")
        if not os.path.isfile(p) or os.path.getsize(p) == 0:
            md_empty.append(lid)
    if md_empty:
        fail(f"{len(md_empty)} bai khong co listening_practice.md (hoac rong): "
             f"{md_empty} — khong the sinh Part 3/4 tu file rong")

    # ------------------------------------------------------------- in stdout
    print("=== KIEM TRA PART 3 / PART 4 LISTENING (task-4 + task-5) ===")
    hdr = (f"{'Lesson':<8}{'has text':<10}{'part3':>6}{'part4':>6}  "
           f"{'part3 numbers':<18}{'part4 numbers':<18}")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"L{r['lesson']:02d}     "
              f"{('yes' if r['has_text'] else 'no'):<10}"
              f"{r['part3']:>6}{r['part4']:>6}  "
              f"{str(r['p3_numbers']):<18}{str(r['p4_numbers']):<18}")

    print()
    print(f"Bai co cau hoi   : {len(with_text)}/{N_LESSONS} -> {with_text}")
    print(f"Bai khong cau hoi: {len(without_text)}/{N_LESSONS}")
    print(f"File md nghe rong: {len(md_empty)} bai"
          + (f" -> {md_empty}" if md_empty else " (ca 50 bai deu co markdown that)"))
    ok50 = sum(1 for r in rows
               if r["part3"] == EXPECTED_PART3 and r["part4"] == EXPECTED_PART4)
    print(f"50/50 check      : {ok50}/{N_LESSONS} bai part3=3 & part4=3")
    print(f"flat == p3+p4    : "
          f"{N_LESSONS - len(set(flat_ne_part))}/{N_LESSONS}"
          + (f"  (SAI o {sorted(set(flat_ne_part))})" if flat_ne_part else ""))
    ok_pins = sum(1 for pr in pin_results if pr["ok"])
    print(f"\nGhim thu tu in   : {ok_pins}/{len(pin_results)} OK "
          "(chung minh cat theo TIEU DE, khong theo khoang so)")
    print(f"  {len(NON_ASCENDING_PART3)} bai in Part 3 khong tang dan: "
          f"{NON_ASCENDING_PART3}")
    print(f"  Part 4 khong tang dan: L03 -> [7, 9, 8]")
    for pr in pin_results:
        if not pr["ok"] or pr["lesson"] in (1, 3):
            print(f"  L{pr['lesson']:02d}  part3 {pr['got3']} (ky vong {pr['want3']}) "
                  f"part4 {pr['got4']} (ky vong {pr['want4']})  "
                  f"{'OK' if pr['ok'] else 'SAI'}")
    print(f"Top-level listening.part3/part4 co mat: "
          f"{N_LESSONS - len([p for p in problems if 'THIEU key' in p or 'TOP-LEVEL' in p])}"
          f"/{N_LESSONS}")

    if baseline:
        tot = {f: sum(measure(d).get(f, 0) for d in lessons.values())
               for f in REGRESSION_FIELDS}
        btot = {f: sum(v.get(f, 0) for v in baseline["lessons"].values())
                for f in REGRESSION_FIELDS}
        print("\nTong so sanh baseline (before -> after):")
        for f in REGRESSION_FIELDS:
            flag = "" if tot[f] == btot[f] else "   <-- KHAC"
            print(f"  {f:<20}{btot[f]:>7} -> {tot[f]:>7}{flag}")
        if regressions:
            print(f"\n{len(regressions)} chenh lech theo tung bai:")
            for g in regressions:
                print(f"  L{g['lesson']:02d}.{g['field']}: {g['before']} -> "
                      f"{g['after']} ({g['direction']})")
        else:
            print("\nKhong co hoi quy: moi chi so words/examples/family/bank/"
                  "blanks/listening_questions deu bang baseline.")

    if warnings:
        print(f"\nCANH BAO ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    print()
    if problems:
        print(f"KET QUA: THAT BAI ({len(problems)} loi)")
        for p in problems:
            print(f"  [X] {p}")
    else:
        print("KET QUA: DAT — tat ca assertion deu qua.")

    # ------------------------------------------------------------- ghi .md
    os.makedirs(REPORT_DIR, exist_ok=True)
    L = []
    L.append("# Bao cao kiem tra Listening Part 3 / Part 4\n")
    L.append("Sinh boi `scripts/reports/verify_listening_parts.py` (task-4, cap nhat task-5).\n")
    L.append(f"- Ket qua: **{'DAT' if not problems else 'THAT BAI'}** "
             f"({len(problems)} loi, {len(warnings)} canh bao)")
    L.append(f"- Bai co cau hoi Part 3/4: **{len(with_text)}/{N_LESSONS}**")
    L.append(f"- 50/50 (part3=3, part4=3): **{ok50}/{N_LESSONS}**")
    L.append(f"- flat `listening.questions` == part3 + part4: "
             f"**{N_LESSONS - len(set(flat_ne_part))}/{N_LESSONS}**")
    L.append(f"- Ghim thu tu in: **{ok_pins}/{len(pin_results)} OK**\n")
    L.append("## Thay doi ky vong o task-5\n")
    L.append("Ky vong cu (13 bai co cau hoi, 37 bai 0/0, rieng L17 la file rac) "
             "da **LOI THOI**. Nguyen nhan goc: `scripts/extract_pdf_assets.py` "
             "chon anh scan bang `max(pg.images, key=lambda x: len(x.data))` — chon "
             "anh NHIEU BYTE NHAT. Anh Part 1 Photo nhung trong trang la JPEG nen "
             "nang hon ban scan toan trang (TIFF), nen 37/50 trang "
             "`listening_practice` bi luu nham thanh anh Part 1 Photo (~300x312px) "
             "thay vi ca trang (~1456x2000px). OCR mot anh chup anh -> khong chu -> "
             "rong.")
    L.append("- Da sua `pick_full_page_scan()` chon theo DIEN TICH PIXEL "
             "(>=800x800); ca 300 trang scan dung kich thuoc.")
    L.append("- Da OCR lai 37 trang (`scripts/ocr_missing_listening.py`, 37/37 OK).")
    L.append("- Ket qua: **ca 50 bai** deu co part3=3 & part4=3; khong con bai 0/0.")
    L.append(f"- `lesson_17` gio la du lieu THAT (markdown {os.path.getsize(os.path.join(ROOT, 'extracted_data', 'mineru_md', 'lesson_17', 'listening_practice.md'))} bytes), "
             "khong con la file rac 9 byte. Da bo ghi chu cu va bo check doi 37 bai 0/0.\n")
    L.append("Cac check THAT SU van giu nguyen, khong noi long: "
             "flat == part3+part4 (so sanh ca noi dung, khong chi so hieu), "
             "ghim thu tu in, top-level `listening.part3/part4`, "
             "va doi chieu hoi quy voi baseline.\n")
    L.append("## Ghim thu tu in (bang chung cat theo TIEU DE Part)\n")
    L.append("So luong 3/3 khong phan biet duoc \"cat theo tieu de\" voi \"cat theo "
             "khoang so cau hoi\" — chi THU TU moi phan biet duoc. Neu cat theo "
             "khoang so thi MOI bai deu ra 4,5,6 / 7,8,9.\n")
    L.append(f"- {len(NON_ASCENDING_PART3)}/50 bai in Part 3 khong tang dan "
             f"(4,6,5): {NON_ASCENDING_PART3}")
    L.append("- 1/50 bai in Part 4 khong tang dan: lesson_03 -> 7,9,8\n")
    L.append("| Lesson | part3 in ra | part3 ky vong | part4 in ra | part4 ky vong | ket qua |")
    L.append("|---:|---|---|---|---|---|")
    for pr in pin_results:
        L.append(f"| L{pr['lesson']:02d} | {pr['got3']} | {pr['want3']} | "
                 f"{pr['got4']} | {pr['want4']} | {'OK' if pr['ok'] else 'SAI'} |")
    L.append("")
    L.append("`lessonLoader.js` doc `lesson.listening` o CAP CAO NHAT "
             "(`const rawListening = lesson.listening || practice.listening || {}`) "
             "va uu tien `part3`/`part4` khi co; chi khi thieu moi roi ve cach cat "
             "theo khoang so 4-6 / 7-9. Vi vay JSON publish phai co part3/part4 o "
             "CAP CAO NHAT — da assert o tren.\n")
    L.append("## Bang chi tiet\n")
    L.append("| Lesson | has text | part3 count | part4 count | part3 numbers | part4 numbers |")
    L.append("|---:|:---:|---:|---:|---|---|")
    for r in rows:
        L.append(f"| L{r['lesson']:02d} | {'yes' if r['has_text'] else 'no'} | "
                 f"{r['part3']} | {r['part4']} | {r['p3_numbers']} | {r['p4_numbers']} |")
    if baseline:
        L.append("\n## Doi chieu baseline (`baseline_before_part_fix.json`)\n")
        L.append("| Chi so | before | after | chenh lech |")
        L.append("|---|---:|---:|---|")
        for f in REGRESSION_FIELDS:
            diff = tot[f] - btot[f]
            L.append(f"| {f} | {btot[f]} | {tot[f]} | "
                     f"{'khong doi' if diff == 0 else ('%+d' % diff)} |")
        L.append("")
        if regressions:
            L.append("| Lesson | Chi so | before | after | huong |")
            L.append("|---:|---|---:|---:|---|")
            for g in regressions:
                L.append(f"| L{g['lesson']:02d} | {g['field']} | {g['before']} | "
                         f"{g['after']} | {g['direction']} |")
        else:
            L.append("Khong co hoi quy nao.")
    if problems:
        L.append("\n## Loi (assertion that bai)\n")
        for p in problems:
            L.append(f"- [X] {p}")
    if warnings:
        L.append("\n## Canh bao\n")
        for w in warnings:
            L.append(f"- {w}")
    L.append("")
    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"\nDa ghi bao cao: {os.path.relpath(REPORT_MD, ROOT)}")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
