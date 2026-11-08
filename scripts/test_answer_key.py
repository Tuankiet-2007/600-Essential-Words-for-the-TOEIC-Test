"""Kiem thu bo chuan hoa OCR cua parse_answer_key.py (task-8).

Chay: py -3.11 scripts/test_answer_key.py

Moi assertion in PASS/FAIL; exit 1 neu co FAIL.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARSER = os.path.join(ROOT, "scripts", "parse_answer_key.py")
OUT = os.path.join(ROOT, "scripts", "data", "answer_key.json")
LESSONS_JSON = os.path.join(ROOT, "public", "lessons_json")

results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print("  [%s] %s%s" % ("PASS" if cond else "FAIL", name,
                           (" — " + detail) if detail else ""), flush=True)


def load():
    spec = importlib.util.spec_from_file_location("pak", PARSER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load()

    # ---------------------------------------------------------------
    print("\n=== 1. Chuan hoa so thu tu ===", flush=True)
    cases = [
        ("IO", 10), ("lO", 10), ("I0", 10), ("1O", 10), ("l0", 10),
        ("IO.", 10), ("li", 11), ("II", 11), ("ll", 11), ("lI", 11),
        ("i", 1), ("l", 1), ("I", 1), ("1", 1),
        ("l2", 12), ("I3", 13), ("14", 14), ("23", 23),
    ]
    for raw, want in cases:
        got = m.fix_num(raw)
        check("fix_num(%r) == %d" % (raw, want), got == want, "nhan duoc %r" % got)
    check("fix_num('') is None", m.fix_num("") is None)
    # 'l.c' la CA MOT MUC (so + dau + dap an), khong phai token so -> phai qua
    # split_entries moi tach duoc. Kiem tra o phan 2 ben duoi.
    check("fix_num('l.c') is None (day la ca nguyen muc, khong phai token so)",
          m.fix_num("l.c") is None)

    # ---------------------------------------------------------------
    print("\n=== 2. Tach muc Word Practice (dap an A-D) ===", flush=True)
    # Cac chuoi nhieu OCR DUNG NHU trong task mo ta.
    abc_cases = [
        ("IO. A", 10, "A"),
        ("l.c", 1, "C"),
        ("I.A", 1, "A"),
        ("14B", 14, "B"),
        ("18. c", 18, "C"),
        ("16,A", 16, "A"),
        ("17 D", 17, "D"),
        ("7-A", 7, "A"),
        ("i. B", 1, "B"),
        ("22.A", 22, "A"),
    ]
    for raw, want_n, want_v in abc_cases:
        got, _ = m.split_entries(raw, "abc")
        check("split(%r)[%d] == %r" % (raw, want_n, want_v),
              got.get(want_n) == want_v, "nhan duoc %r" % got)

    # Nhieu muc tren 1 dong, gom ca nhieu OCR tron lan.
    line = ("Word Practice: 1. D 2. B 3. B 4. C 5. D 6. C 7. A 8. D "
            "9. A IO. B 11. C 12. B 13. A 14. A 15. D 16. A 17 D "
            "18. C 19. B 20. B 21. C 22. D 23. A")
    got, _ = m.split_entries(line.replace("Word Practice: ", ""), "abc")
    check("cau day du 23 muc 1..23",
          sorted(got.keys()) == list(range(1, 24)),
          "thieu %s" % [n for n in range(1, 24) if n not in got])
    check("muc 17 = 'D' (dang '17 D' khong co dau cham)", got.get(17) == "D")
    check("muc 10 = 'B' (dang 'IO. B')", got.get(10) == "B")

    # Khong duoc nham chu 'l' trong tu thuong thanh so 1.
    wic = ("1. proofed 2. revision 3. beforehand 4. assemble 5. folding "
           "6. courier 7. express 8. registered 9. layout 10. mention "
           "11. complicated 12. petition")
    got_w, _ = m.split_entries(wic, "word")
    check("WIC 12 muc, khong nham 'l' trong 'layout' thanh so 1",
          sorted(got_w.keys()) == list(range(1, 13)),
          "nhan duoc %s" % sorted(got_w.keys()))
    check("WIC muc 9 == 'layout' (khong bi cat thanh 'ayout')",
          got_w.get(9) == "layout", "nhan duoc %r" % got_w.get(9))
    check("WIC muc 6 == 'courier' (tu bat dau bang 'c')", got_w.get(6) == "courier")

    wic_l = ("1. recognizes 2. contributions 3. achievements/merits "
             "4. promotions 5. merits/achievements 6. loyalty 7. obvious "
             "8. look to 9. productivity IO. value 11. look forward 12. dedicate")
    got_l, _ = m.split_entries(wic_l, "word")
    check("WIC khong nham 'l' trong 'loyalty' thanh so 1",
          sorted(got_l.keys()) == list(range(1, 13)),
          "nhan duoc %s" % sorted(got_l.keys()))
    check("WIC muc 6 == 'loyalty'", got_l.get(6) == "loyalty")

    # ---------------------------------------------------------------
    print("\n=== 3. Ca OCR da xac minh (L05 21->11, L27 15.8, L44 orphan) ===", flush=True)
    check("fix_num('21') == 21 (tang chuan hoa, viec doi 21->11 do _post_fix)",
          m.fix_num("21") == 21)
    got8, orph8 = m.split_entries("15.8 16. D", "abc")
    check("'15.8' -> muc 15 = 'B' (OCR doc B thanh 8)", got8.get(15) == "B",
          "nhan duoc %r" % got8)
    check("'15.8' danh dau __OCR_8__ de ghi warning",
          any(o.startswith("__OCR_") for o in orph8), "orphans=%s" % orph8)
    got_orph, orph = m.split_entries("i. B 2. C 3. C C 5. B", "abc")
    check("'3. C C 5. B' -> muc 1..3,5 va 1 gia tri mo coi 'C'",
          got_orph.get(1) == "B" and orph == ["C"], "orphans=%s" % orph)

    # ---------------------------------------------------------------
    print("\n=== 4. File JSON ket qua ===", flush=True)
    check("scripts/data/answer_key.json ton tai", os.path.isfile(OUT))
    if not os.path.isfile(OUT):
        return finish()
    with open(OUT, encoding="utf-8") as f:
        data = json.load(f)

    check("co dung 50 bai", len(data) == 50, "nhan duoc %d" % len(data))
    check("khoa ngoai la chuoi '1'..'50'",
          sorted(data.keys(), key=int) == [str(i) for i in range(1, 51)])

    load_fail = []
    for lid in range(1, 51):
        r = data.get(str(lid))
        if not r:
            load_fail.append(lid)
            continue
        if r.get("lesson_id") != lid:
            load_fail.append(lid)
        for k in ("words_in_context", "word_practice", "title", "warnings"):
            if k not in r:
                load_fail.append(lid)
    check("moi bai co lesson_id dung + du 4 truong", not load_fail,
          "bai loi: %s" % load_fail)

    # Title phai khop JSON bai hoc.
    bad_title = []
    for lid in range(1, 51):
        p = os.path.join(LESSONS_JSON, "lesson_%02d.json" % lid)
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as f:
                want = json.load(f).get("title", "")
            if data[str(lid)]["title"] != want:
                bad_title.append((lid, data[str(lid)]["title"], want))
    check("title khop voi public/lessons_json", not bad_title, str(bad_title))

    # ---------------------------------------------------------------
    print("\n=== 5. Do day du: 12 WIC + 23 WP ===", flush=True)
    n_wic_ok = n_wp_ok = 0
    incomplete = []
    for lid in range(1, 51):
        r = data[str(lid)]
        wic, wp = r["words_in_context"], r["word_practice"]
        miss_w = [n for n in range(1, 13) if str(n) not in wic]
        miss_p = [n for n in range(1, 24) if str(n) not in wp]
        if not miss_w:
            n_wic_ok += 1
        if not miss_p:
            n_wp_ok += 1
        if miss_w or miss_p:
            incomplete.append((lid, miss_w, miss_p))
    check("WIC: ca 50 bai du 12/12", n_wic_ok == 50,
          "%d/50 bai du" % n_wic_ok)
    check("WP: 49/50 bai du 23/23 (L08 thieu 5,6 do OCR xoa han)",
          n_wp_ok == 49, "%d/50 bai du" % n_wp_ok)
    check("chi L08 thieu WP, dung muc [5,6]",
          incomplete == [(8, [], [5, 6])], str(incomplete))

    # Moi dap an WP phai la 1 chu A-D.
    bad = [(lid, k, v) for lid in range(1, 51)
           for k, v in data[str(lid)]["word_practice"].items() if v not in ("A", "B", "C", "D")]
    check("moi dap an WP la 1 chu A-D", not bad, str(bad[:5]))

    # Khong co gia tri rong / rac.
    empty = [(lid, k) for lid in range(1, 51)
             for k, v in data[str(lid)]["words_in_context"].items() if not v.strip()]
    check("khong co WIC rong", not empty, str(empty[:5]))

    # ---------------------------------------------------------------
    print("\n=== 6. Ca L37 (dap an cat qua ranh gioi trang) ===", flush=True)
    r37 = data["37"]
    check("L37 'Airlines' co du 23 WP (bug cat trang da sua)",
          len(r37["word_practice"]) == 23,
          "nhan duoc %d" % len(r37["word_practice"]))
    check("L37 WP muc 1 == 'D' (dong dau trang 336)",
          r37["word_practice"].get("1") == "D",
          "nhan duoc %r" % r37["word_practice"].get("1"))
    check("L37 WP muc 23 == 'C'", r37["word_practice"].get("23") == "C")
    check("L37 WIC du 12", len(r37["words_in_context"]) == 12)

    return finish()


def finish():
    failed = [n for n, ok in results if not ok]
    total = len(results)
    print("\n=== KET QUA: %d/%d PASS ===" % (total - len(failed), total), flush=True)
    if failed:
        for n in failed:
            print("  FAIL: %s" % n, flush=True)
        return 1
    print("  Tat ca assertion deu PASS.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
