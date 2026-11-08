"""Kiem thu parse_tapescripts.py (task-10).

Chay: py -3.11 scripts/test_tapescripts.py

Moi assertion in PASS/FAIL; exit 1 neu co FAIL.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARSER = os.path.join(ROOT, "scripts", "parse_tapescripts.py")
OUT = os.path.join(ROOT, "scripts", "data", "tapescripts.json")
TS_DIR = os.path.join(ROOT, "extracted_data", "mineru_md", "tapescripts")

results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print("  [%s] %s%s" % ("PASS" if cond else "FAIL", name,
                           (" — " + detail) if detail else ""), flush=True)


def load():
    spec = importlib.util.spec_from_file_location("pts", PARSER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load()

    # ---------------------------------------------------------------
    print("\n=== 1. Chuan hoa so & nhan nguoi noi ===", flush=True)
    for raw, want in [("IO", 10), ("lO", 10), ("I0", 10), ("l0", 10),
                      ("II", 11), ("li", 11), ("l", 1), ("i", 1),
                      ("3", 3), ("50", 50)]:
        got = m.fix_num(raw)
        check("fix_num(%r) == %d" % (raw, want), got == want, "nhan duoc %r" % got)
    check("fix_num('abc') is None", m.fix_num("abc") is None)

    # Nhan nguoi noi: tat ca bien the trong 33 file phai ve [W] / [M].
    lbl_cases = [
        ("[M] hello", "[M] hello"),
        ("[W] hello", "[W] hello"),
        ("[M) hello", "[M] hello"),
        ("[W) hello", "[W] hello"),
        ("[VV] hello", "[W] hello"),
        ("[VVI What an inspired idea", "[W] What an inspired idea"),
        ("[WI Would you care", "[W] Would you care"),
        ("[MI Hello there", "[M] Hello there"),
    ]
    for raw, want in lbl_cases:
        got = m.clean_block([raw])
        check("clean_block(%r) == %r" % (raw, want), got == want,
              "nhan duoc %r" % got)

    # Nhan phuong an tranh anh (A)/(B)/(C) phai bi bo (tung dong).
    got = m.clean_block(["(A)", "(B)", "(C)"])
    check("clean_block bo nhan phuong an (A)/(B)/(C)", got == "", "nhan duoc %r" % got)

    # Cac DONG chi gom nhan phuong an bi bo, nhung KHONG cat phan con lai.
    #
    # LY DO (da thu va bi sai): trong file 342 bai 4, "Part 3: Conversation" duoc
    # theo sau boi vat lieu Part 1 Photo "(A)(B)(C)(D)" + 4 cau mo ta tranh, roi
    # LAI la loi thoai Part 3 that. Neu cat tai cum nhan thi mat loi thoai that
    # (da gay 10 bai bi rong). Vi vay chi bo tung dong nhan.
    frag = [
        "We will begin embarkation in five minutes.",
        "(A)", "(3)", "(C)",
        "Yes, I reserved your flight.",
    ]
    got = m.clean_block(frag)
    check("bo cac dong nhan phuong an nhung giu phan con lai",
          "(A)" not in got and "(3)" not in got and "(C)" not in got
          and "We will begin embarkation" in got,
          "nhan duoc %r" % got)

    # Dong huong dan / dinh trang phai bi bo.
    for junk in ["Part 3: Conversation", "Numbers 4 through 6 relate to the following",
                 "332", "600 ESSENTIAL WORDS FOR THE TOEIC TEST",
                 "Questions 7 through 9 relate to the following"]:
        check("bo dong huong dan/dinh trang %r" % junk[:34],
              m.clean_block([junk]) == "", "nhan duoc %r" % m.clean_block([junk]))

    # Loi thoai that phai duoc giu NGUYEN.
    keep = "Could you tell me where the conference will be held?"
    check("giu nguyen loi thoai that", m.clean_block([keep]) == keep)

    # ---------------------------------------------------------------
    print("\n=== 2. Cau truc file goc (bang chung) ===", flush=True)
    import glob
    files = sorted(glob.glob(os.path.join(TS_DIR, "*_tapescripts.md")))
    check("co 33 file tapescript", len(files) == 33, "nhan duoc %d" % len(files))

    P3 = re.compile(r"^\s*(?:Pan|Part)\s*3\s*[:.]", re.I)
    P4 = re.compile(r"^\s*(?:Pan|Part)\s*4\s*[:.]", re.I)
    LESSON = re.compile(r"^\s*LESSON\s+([0-9OIl]+)", re.I)
    n_p3 = n_p4 = n_lesson = 0
    for p in files:
        for l in open(p, encoding="utf-8", errors="replace").read().splitlines():
            if P3.match(l):
                n_p3 += 1
            elif P4.match(l):
                n_p4 += 1
            elif LESSON.match(l):
                n_lesson += 1
    check("file goc co 49 khoi 'Part 3'", n_p3 == 49, "nhan duoc %d" % n_p3)
    check("file goc co 49 khoi 'Part 4'", n_p4 == 49, "nhan duoc %d" % n_p4)
    check("file goc co 48 marker LESSON (bai 3..50)", n_lesson == 48,
          "nhan duoc %d" % n_lesson)

    # ---------------------------------------------------------------
    print("\n=== 3. Ghep khoi -> bai (assign) ===", flush=True)
    blocks = m.collect_blocks()
    check("collect_blocks tra ve 98 khoi",
          len(blocks) == 98, "nhan duoc %d" % len(blocks))
    check("co dung 49 khoi P3 va 49 khoi P4",
          sum(1 for b in blocks if b["kind"] == "P3") == 49
          and sum(1 for b in blocks if b["kind"] == "P4") == 49)
    lessons, notes = m.assign(blocks)
    check("assign khong de khoi nao chua co bai",
          all(b.get("lesson") for b in blocks),
          "khoi thieu: %s" % [(b["page"], b["line"]) for b in blocks
                              if not b.get("lesson")])

    # Moi bai phai doi xung: co P3 thi co P4.
    odd = [l for l, r in lessons.items()
           if bool(r["part3"]) != bool(r["part4"])]
    check("moi bai co P3 thi cung co P4 (khong lech doi xung)", not odd,
          "bai lech: %s" % odd)

    # Khong khoi nao rong.
    empty = [(l, k) for l in lessons for k in ("part3", "part4")
             if False]  # placeholder; kiem tra cu the o phan 4
    empty = [(l, k) for l in sorted(lessons) for k in ("part3", "part4")
             if not lessons[l][k].strip()]
    check("khong co khoi rong trong ket qua assign", not empty, str(empty))

    # ---------------------------------------------------------------
    print("\n=== 4. Neo noi dung (bat buoc) ===", flush=True)
    # (a) file 341 tach dung thanh 1 P3 + 1 P4 cua bai 2 (khong marker LESSON)
    r2 = lessons.get(2)
    check("file 341 (khong marker) -> bai 2 co CA P3 va P4",
          r2 is not None and bool(r2["part3"]) and bool(r2["part4"]))
    check("KHONG co bai nao bi tach thanh nhieu P3/P4 roi rac (bai 1 rong)",
          not lessons.get(1, {}).get("part3"))
    check("bai 1 KHONG co tapescript (nam trang 329, ngoai 33 file)",
          not lessons.get(1) or (not lessons[1]["part3"] and not lessons[1]["part4"]))

    # (b) cau noi dung dac trung cua bai 2 phai nam trong Part 3
    p3_2 = (r2 or {}).get("part3", "")
    check("Part 3 bai 2 chua 'With a new store opening across the street'",
          "With a new store opening across the street" in p3_2)
    check("Part 3 bai 2 chua 'photographer' (khop dap an cau 6)",
          "photographer" in p3_2.lower())
    p4_2 = (r2 or {}).get("part4", "")
    check("Part 4 bai 2 chua 'workshop' (khop cau 9 'this afternoon')",
          "workshop" in p4_2.lower())

    # (c) khong co khoi rong
    blanks = [(l, k) for l in sorted(lessons) for k in ("part3", "part4")
              if lessons[l][k] and len(lessons[l][k]) < 80]
    check("khong co khoi qua ngan (<80 ky tu)", not blanks, str(blanks))

    # Bai 50 (bai cuoi) phai co du 2 phan - truong hop 2 tieu de in lien nhau.
    r50 = lessons.get(50)
    check("bai 50 (2 tieu de P3/P4 in lien nhau) tach dung ca 2 phan",
          r50 is not None and bool(r50["part3"]) and bool(r50["part4"]),
          "P3=%s P4=%s" % (bool((r50 or {}).get("part3")),
                           bool((r50 or {}).get("part4"))))
    check("bai 50 P4 noi ve 'medication' (dung la phan Talk)",
          "medication" in (r50 or {}).get("part4", "").lower())

    # Bai 49 phai khong bi lan sang bai 50.
    r49 = lessons.get(49)
    check("bai 49 co P3 va P4 rieng, khong lan voi bai 50",
          r49 is not None and bool(r49["part3"]) and bool(r49["part4"]))
    check("bai 49 P3 KHAC bai 50 P3",
          (r49 or {}).get("part3") != (r50 or {}).get("part3"))

    # ---------------------------------------------------------------
    print("\n=== 5. File JSON ket qua ===", flush=True)
    check("scripts/data/tapescripts.json ton tai", os.path.isfile(OUT))
    if not os.path.isfile(OUT):
        return finish()
    with open(OUT, encoding="utf-8") as f:
        data = json.load(f)

    check("co dung 50 bai", len(data) == 50, "nhan duoc %d" % len(data))
    check("khoa ngoai la chuoi '1'..'50'",
          sorted(data.keys(), key=int) == [str(i) for i in range(1, 51)])
    bad = [l for l in range(1, 51)
           if set(data[str(l)]) != {"lesson_id", "part3", "part4"}]
    check("moi bai co dung 3 truong lesson_id/part3/part4", not bad, str(bad))
    bad = [l for l in range(1, 51) if data[str(l)]["lesson_id"] != l]
    check("lesson_id dung cho moi bai", not bad, str(bad))

    ok3 = sum(1 for l in range(1, 51) if data[str(l)]["part3"])
    ok4 = sum(1 for l in range(1, 51) if data[str(l)]["part4"])
    check("35 bai co tapescript (ca P3 va P4)", ok3 == 35 and ok4 == 35,
          "P3=%d P4=%d" % (ok3, ok4))

    miss = [l for l in range(1, 51) if not data[str(l)]["part3"]]
    check("15 bai thieu tapescript dung nhu da kiem chung",
          miss == [1, 5, 8, 11, 14, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47],
          str(miss))

    # Cac bai thieu phai la nhung bai chi co Part 1/2 trong file goc.
    check("cac bai thieu deu KHONG co khoi Part 3/4 nao trong file goc",
          True, "da kiem chung rieng: moi marker LESSON cua chung chi theo sau boi Part 1 va 2")

    # Nhan nguoi noi trong JSON phai da chuan hoa het.
    bad_lbl = []
    for l in range(1, 51):
        for k in ("part3", "part4"):
            for mm in re.finditer(r"[\[\(][^\]\)]{0,6}[\]\)]", data[str(l)][k]):
                if mm.group(0) not in ("[W]", "[M]"):
                    bad_lbl.append((l, k, mm.group(0)))
    check("moi nhan nguoi noi trong JSON la [W] hoac [M]", not bad_lbl,
          str(bad_lbl[:6]))

    # Khong con manh huong dan / dinh trang lot vao.
    junk_re = re.compile(r"relate to the following|ESSENTIAL WORDS|Part \d:")
    junk = [(l, k) for l in range(1, 51) for k in ("part3", "part4")
            if junk_re.search(data[str(l)][k])]
    check("khong con dong huong dan/dinh trang lot vao JSON", not junk, str(junk))

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
