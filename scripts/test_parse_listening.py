"""Regression test cho parse_listening() trong run_mineru_local.py.

Muc dich: khoa lai hop dong du lieu moi cua phan Listening —
`listening.part3` / `listening.part4` phai duoc suy ra TU TIEU DE
"Part 3"/"Part 4" trong Markdown, khong phai tu khoang so cau hoi
(4..6 => part3, 7..9 => part4) nhu app tung phai tu doan.

Chay:
    py -3.11 scripts/test_parse_listening.py

Khong goi Mang/MinerU: chi doc file .md nho da co san tren dia.
"""

from __future__ import annotations

import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARSER = os.path.join(ROOT, "scripts", "run_mineru_local.py")
MD_ROOT = os.path.join(ROOT, "extracted_data", "mineru_md")

results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}"
          + (f" — {detail}" if detail else ""), flush=True)


def load_parser():
    """Nap run_mineru_local.py theo duong dan.

    Dung importlib de khong phu thuoc sys.path; module chi dinh nghia ham va
    hang so o cap cao nen import khong chay OCR / khong cham toi file nang.
    """
    spec = importlib.util.spec_from_file_location("run_mineru_local", PARSER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_listening(lid):
    p = os.path.join(MD_ROOT, f"lesson_{lid:02d}", "listening_practice.md")
    if not os.path.isfile(p):
        return ""
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def nums(qs):
    return [q["number"] for q in qs]


def main():
    mod = load_parser()

    print("\n=== lesson_01: nhom theo tieu de Part (khong theo khoang so) ===", flush=True)
    md1 = read_listening(1)
    check("lesson_01 doc duoc listening_practice.md", bool(md1.strip()),
          f"{len(md1)} ky tu")
    if not md1.strip():
        return finish()

    lis = mod.parse_listening(md1)

    for key in ("questions", "instructions", "tapescript", "parts", "part3", "part4"):
        check(f"lesson_01 co khoa '{key}'", key in lis)

    p3, p4, flat = lis.get("part3", []), lis.get("part4", []), lis.get("questions", [])

    # 1. Nhom dung theo tieu de: Part 3 in ra 4,6,5 (KHONG sap xep lai).
    check("lesson_01 part3 numbers == [4, 6, 5]", nums(p3) == [4, 6, 5],
          f"nhan duoc {nums(p3)}")
    check("lesson_01 part4 numbers == [7, 8, 9]", nums(p4) == [7, 8, 9],
          f"nhan duoc {nums(p4)}")

    # 2. Moi cau hoi Part 3/4 co du 4 lua chon A-D.
    for label, group in (("part3", p3), ("part4", p4)):
        bad = [q["number"] for q in group
               if [o["label"] for o in q.get("options", [])] != ["A", "B", "C", "D"]]
        check(f"lesson_01 {label}: moi cau co du lua chon A-D", not bad,
              f"thieu o cau {bad}" if bad else f"{len(group)} cau")
        empty = [q["number"] for q in group
                 if any(not o["text"].strip() for o in q["options"])]
        check(f"lesson_01 {label}: khong co lua chon rong", not empty,
              f"rong o cau {empty}" if empty else "")

    # 3. `questions` van la danh sach phang tuong thich nguoc.
    check("lesson_01 flat questions == part3 + part4",
          [q["number"] for q in flat] == nums(p3) + nums(p4),
          f"flat={nums(flat)} part3+part4={nums(p3) + nums(p4)}")
    check("lesson_01 flat questions khop tung object voi part3+part4",
          flat == p3 + p4)

    # 4. Metadata `parts` giu nguyen.
    check("lesson_01 parts metadata co Part 1..4",
          [p["part"] for p in lis.get("parts", [])] == [1, 2, 3, 4],
          f"nhan duoc {[p['part'] for p in lis.get('parts', [])]}")

    # 5. Cac kieu tieu de MinerU khac nhau (nhan manh / do sau #).
    print("\n=== Kieu tieu de Part khac nhau ===", flush=True)
    heads = [
        "## Part 3 Conversation",
        "**Part 3 Conversation**",
        "Part 3 Conversation",
        "### Part 3 Conversation",
        "_Part 3 Conversation_",
        "__Part 3 Conversation__",
        "##   Part   3   Conversation  ",
        "Part 3: Conversation",
    ]
    body = ("\n".join([
        "4. What problem do the speakers have?",
        "(A) One.", "(B) Two.", "(C) Three.", "(D) Four.",
        "6. What does the woman suggest?",
        "(A) One.", "(B) Two.", "(C) Three.", "(D) Four.",
        "5. When will the contract run out?",
        "(A) One.", "(B) Two.", "(C) Three.", "(D) Four.",
        "## Part 4 Talk",
        "7. Who is talking?",
        "(A) One.", "(B) Two.", "(C) Three.", "(D) Four.",
    ]))
    for h in heads:
        got = mod.parse_listening(h + "\n" + body)
        check(f"tieu de {h!r} -> part3 [4,6,5]", nums(got["part3"]) == [4, 6, 5],
              f"nhan duoc {nums(got['part3'])}")

    # 6. Trang chi co Part 1 (khong co chu) -> part3/part4 rong, KHONG bia.
    print("\n=== Trang Part 1-only ===", flush=True)
    photo = mod.parse_listening("## Part 1 Photo\n\n![](_page_0_Picture_0.jpeg)\n")
    check("Part 1-only -> questions rong", photo["questions"] == [])
    check("Part 1-only -> part3 == []", photo["part3"] == [])
    check("Part 1-only -> part4 == []", photo["part4"] == [])
    check("Markdown rong -> part3/part4 == []",
          mod.parse_listening("")["part3"] == []
          and mod.parse_listening("")["part4"] == [])
    check("Markdown rong -> co du khoa part3/part4",
          set(("part3", "part4")) <= set(mod.parse_listening("").keys()))

    # 7. Cau hoi TRUOC moi tieu de Part (trang loi) khong crash va chi nam
    #    trong danh sach phang.
    print("\n=== Trang loi: cau hoi truoc tieu de Part ===", flush=True)
    malformed = ("1. A question with no Part heading.\n"
                 "(A) One.\n(B) Two.\n\n"
                 "## Part 3 Conversation\n"
                 "4. Real part 3 question.\n(A) One.\n(B) Two.\n(C) Three.\n(D) Four.\n")
    got = mod.parse_listening(malformed)
    check("trang loi: khong crash", isinstance(got, dict))
    check("trang loi: cau 1 chi nam o danh sach phang",
          [q["number"] for q in got["questions"]] == [1, 4],
          f"flat={nums(got['questions'])}")
    check("trang loi: part3 chi co cau 4", nums(got["part3"]) == [4])
    check("trang loi: part4 rong", got["part4"] == [])

    # 8. Tat ca 50 bai deu phai co Part 3 + Part 4.
    #
    #    TRUOC DAY ky vong la 13 bai / 37 bai, vi 37 trang "listening_practice"
    #    bi extract nham thanh ANH PART 1 PHOTO (~300x312px) thay vi ca trang
    #    (~1456x2000px) — xem extract_pdf_assets.py::pick_full_page_scan(). OCR
    #    mot buc anh chup anh thi khong co chu, nen 37 bai trong nhu "sach khong
    #    in Part 3/Part 4", trong khi sach in rat ro.
    #
    #    Sau khi sua extraction va OCR lai 37 trang, CA 50 bai deu co du lieu.
    #    Ky vong cu 13/37 la DA LOI THOI va duoc thay bang ky vong dung duoi day.
    print("\n=== Toan bo 50 bai ===", flush=True)
    with_text, photo_only = [], []
    for lid in range(1, 51):
        md = read_listening(lid)
        r = mod.parse_listening(md)
        if not r["questions"]:
            photo_only.append(lid)
            continue
        with_text.append(lid)
        check(f"lesson_{lid:02d}: flat == part3 + part4",
              [q["number"] for q in r["questions"]]
              == nums(r["part3"]) + nums(r["part4"]),
              f"flat={nums(r['questions'])} split={nums(r['part3']) + nums(r['part4'])}")

    check("ca 50 bai deu co cau hoi listening", len(with_text) == 50,
          f"{len(with_text)} bai: {with_text}")
    check("khong con bai nao bi coi la 'chi co anh'", len(photo_only) == 0,
          f"con thieu: {photo_only}")

    for lid in with_text:
        r = mod.parse_listening(read_listening(lid))
        check(f"lesson_{lid:02d}: moi cau deu nam trong part3 hoac part4",
              len(r["part3"]) + len(r["part4"]) == len(r["questions"]),
              f"part3={len(r['part3'])} part4={len(r['part4'])} flat={len(r['questions'])}")
        # Moi bai phai co dung 3 cau Part 3 (cau 4-6) va 3 cau Part 4 (cau 7-9).
        check(f"lesson_{lid:02d}: Part 3 co dung 3 cau", len(r["part3"]) == 3,
              f"{nums(r['part3'])}")
        check(f"lesson_{lid:02d}: Part 4 co dung 3 cau", len(r["part4"]) == 3,
              f"{nums(r['part4'])}")
        check(f"lesson_{lid:02d}: Part 3 gom cau 4,5,6",
              sorted(nums(r["part3"])) == [4, 5, 6], f"{nums(r['part3'])}")
        check(f"lesson_{lid:02d}: Part 4 gom cau 7,8,9",
              sorted(nums(r["part4"])) == [7, 8, 9], f"{nums(r['part4'])}")
    return finish()


def finish():
    failed = [n for n, ok_, _ in results if not ok_]
    total = len(results)
    print(f"\n=== KET QUA: {total - len(failed)}/{total} PASS ===", flush=True)
    if failed:
        for n in failed:
            print(f"  FAIL: {n}", flush=True)
        return 1
    print("  Tat ca assertion deu PASS.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
