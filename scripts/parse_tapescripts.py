"""Tach tapescript thanh loi thoai tung bai (task-10).

Chay: py -3.11 scripts/parse_tapescripts.py

MUC DICH: sinh scripts/data/tapescripts.json de UI giai thich tung cau Listening
(Part 3 Conversation / Part 4 Talk). Moi bai co 3 cau P3 (cau 4-6) va 3 cau P4
(cau 7-9).

-----------------------------------------------------------------------------
CAU TRUC THAT CUA FILE OCR (da kiem chung bang cach dem tren ca 33 file)
-----------------------------------------------------------------------------
Sach in tapescript thanh 2 COT. MinerU cat theo TRANG, nen mot bai bi xe lam doi:
phan Part 3 nam o cuoi trang truoc, phan Part 4 tran sang dau trang sau.

Da dem duoc tren 33 file:
    49 khoi "Part 3" + 49 khoi "Part 4" = 98 khoi
    48 marker "LESSON N"  (N = 3..50)

Trong 1 trang, thu tu vat ly luon la:
        [P4 cua bai TRUOC]  ...  LESSON N  ...  [P3 cua bai N]

Vi du file 341 (trang dau tien):
        dong  3 : Part 3: Conversation     <- KHONG co LESSON truoc -> bai 2
        dong 15 : Part 4: Talk             <- bai 2
        dong 31 : LESSON 3
        dong 52 : Part 3: Conversation     <- bai 3

-----------------------------------------------------------------------------
QUY TAC GAN BAI (chinh xac, khong suy dien bua)
-----------------------------------------------------------------------------
    1. P3 nam NGAY SAU "LESSON N" tren cung trang   -> bai N
    2. P3 o DAU trang, truoc marker dau tien         -> bai (P3 ke tiep co marker) - 1
    3. P4 LUON thuoc ve P3 NGAY TRUOC no             -> bai cua P3 do

Bai 1 va bai 2 KHONG co marker LESSON. Da xac minh bang NOI DUNG (khong doan):
khoi P3 dau tien cua file 341 noi "With a new store opening across the street ...
I'll call a photographer" -> khop bai 2 Marketing:
    cau 4 "Why does the store need to be more competitive?"
    cau 6 "Who will the woman call?"  dap an "A photographer"
Va P4 ngay sau ("To attract new customers ... our workshop this afternoon") khop
bai 2 cau 9 "Where will the listeners be this afternoon?".
=> Bai 1 nam TRUOC do (trang 329), KHONG co trong 33 file nay.
=> De TRONG bai 1 va bao ro. KHONG bia.
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TS_DIR = os.path.join(ROOT, "extracted_data", "mineru_md", "tapescripts")
OUT_PATH = os.path.join(ROOT, "scripts", "data", "tapescripts.json")
LESSONS_JSON = os.path.join(ROOT, "public", "lessons_json")

# "Part 3:" / "Pan 3:" (OCR nham P-a-n) — cung chap nhan "PART 3."
P3_RE = re.compile(r"^\s*(?:Pan|Part)\s*3\s*[:.]", re.I)
P4_RE = re.compile(r"^\s*(?:Pan|Part)\s*4\s*[:.]", re.I)
LESSON_RE = re.compile(r"^\s*LESSON\s+([0-9OIl]+)", re.I)
# "Numbers 4 through 6 relate to the following conversation."
RANGE_RE = re.compile(
    r"(?:Numbers|Questions)\s+([0-9OIl]+)\s+through\s+([0-9OIl]+)", re.I)

# Dong huong dan / tieu de phan -> khong phai loi thoai.
INSTR_RE = re.compile(
    r"^Part\s*[1-7]\s*[:.]"
    r"|^Pan\s*[1-7]\s*[:.]"
    r"|^(?:Numbers?|Questions?)\s+[0-9OIl]+\s+through\s+[0-9OIl]+\s+relate"
    r"|^conversation\.?$"
    r"|^talk\.?$"
    r"|^recording\.?$"
    r"|^directions\s*:",
    re.I,
)
# Dong rac cua trang (dinh trang, ten sach, tieu de phan khac).
NOISE_RE = re.compile(
    r"^\s*[0-9]{2,3}\s*$"
    r"|^\s*[0-9]{2,3}\s+600\s+ESSENT"
    r"|^\s*600\s+ESSENT"
    r"|^\s*(?:APPENDIX|ANSWER KEY|CONTENTS)\s*$"
    r"|^\s*Number\s+[0-9]+\s*\.\s*$"
    r"|^\s*\(\s*[A-D]\s*\)\s*$"
    r"|^\s*[A-D]\s*\.\s*$"
    r"|^\s*[WwMm]\s*[:.]\s*$",
    re.I,
)


def fix_num(tok):
    """Chuan hoa token so co the bi OCR nham (IO->10, l->1, O->0)."""
    t = (tok or "").strip()
    subs = {"IO": "10", "lO": "10", "I0": "10", "1O": "10", "l0": "10",
            "II": "11", "ll": "11", "Il": "11", "lI": "11",
            "li": "11", "Li": "11", "LI": "11"}
    if t in subs:
        t = subs[t]
    if not t.isdigit():
        t = "".join({"l": "1", "I": "1", "i": "1",
                     "O": "0", "o": "0"}.get(c, c) for c in t)
    return int(t) if t.isdigit() else None


def clean_block(lines):
    """Bo dong huong dan / dinh trang, giu NGUYEN loi thoai.

    Khong tu them chu nao. Chi chuan hoa nhan nguoi noi bi OCR hong.

    CA BIET (file 363 dong 70-75): sau khi phan Talk ket thuc, OCR lot vao 3 nhan
    phuong an tranh anh roi 3 CAU TRA LOI cua Part 2 Question-Response:
        (A) (3) (C)
        Yes, I reserved your flight.
        No, just beverages and a snack.
        Their service is all right.
    Day KHONG phai loi thoai Part 4. Nhan biet: mot CUM >=2 nhan phuong an lien
    nhau, va MOI dong ngay sau do deu la cau tra loi ngan ket thuc bang dau cau.
    Cat bo tu cum nhan do tro di.
    """
    # KHONG cat tai cum nhan phuong an!
    #
    # Da thu va BI SAI: trong file 342, bai 4 co "Part 3: Conversation" (dong 24)
    # nhung ngay sau lai la vat lieu Part 1 Photo: "(A) (B) (C) (D)" roi 4 cau mo
    # ta tranh. Loi thoai THAT cua Part 3 nam SAU do (dong 47-56). Neu cat tai cum
    # nhan phuong an thi se mat luon loi thoai that (da bi loi nay: 10 bai bi rong).
    #
    # Cach dung: BO cac DONG chi gom nhan phuong an, va bo cac cau mo ta tranh
    # (cau ngan, khong co nhan nguoi noi, nam ngay sau cum nhan) — nhung GIU lai
    # phan con lai cua khoi.
    opt_re = re.compile(r"^[\[\(]\s*[A-D3]\s*[\]\)]$")

    kept = []
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if INSTR_RE.match(s) or NOISE_RE.match(s):
            continue
        # dong chi gom nhan nguoi noi hoac ky tu rac
        if re.fullmatch(r"[\[\(]?\s*[WwMmVIviNn]{1,3}\s*[\]\)]?[.:]?", s):
            continue
        # dong chi gom nhan phuong an tranh anh
        if opt_re.match(s):
            continue
        kept.append(s)

    text = " ".join(kept)
    # Nhan nguoi noi bi OCR hong. Da liet ke TAT CA bien the trong 33 file:
    #   [M] x58, [W] x37, [M) x5, [VV] x1, [W) x1, va "[VVI" (THIEU dau dong,
    #   OCR dinh lien voi tu sau: "[VVI What an inspired idea").
    # Vi vay dau dong phai TUY CHON khi phia sau la khoang trang.
    text = re.sub(r"[\[\(]\s*(?:VV|VI|V|Wl|W1|W|N)\s*[Il1]?\s*[\]\)]?(?=\s|$)",
                  "[W]", text)
    text = re.sub(r"[\[\(]\s*M\s*[Il1]?\s*[\]\)]?(?=\s|$)", "[M]", text)
    # Nhan phuong an tranh anh con sot.
    text = re.sub(r"\(\s*[A-D3]\s*\)", " ", text)
    text = re.sub(r"\b[Vv]{2}\b", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def collect_blocks():
    """Doc 33 file theo thu tu trang -> list khoi theo thu tu vat ly.

    Moi khoi: dict(kind, page, line, body, rng, after_lesson)
      after_lesson = so bai cua marker LESSON gan nhat TRUOC khoi nay TRONG CUNG TRANG.

    CA BIET (da gap o file 373 = bai 50): hai tieu de "Part 3" va "Part 4" in
    LIEN NHAU, roi ca hai phan noi dung moi nam sau do:

        Part 3: Conversation
        Part 4: Talk
        Questions 7 through 9 relate ...      <- P4 (range 7-9)
        ... loi thoai cua Talk ...
        Numbers 4 through 6 relate ...        <- P3 (range 4-6)
        ... loi thoai cua Conversation ...

    Trong truong hop nay, gan theo RANGE trong cau huong dan (4-6 = P3, 7-9 = P4)
    chu khong theo thu tu tieu de. Xu ly o buoc tach than.
    """
    files = sorted(glob.glob(os.path.join(TS_DIR, "*_tapescripts.md")))
    blocks = []
    for p in files:
        page = os.path.basename(p).split("_")[0]
        with open(p, encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()

        marks = []
        for i, l in enumerate(lines):
            m = LESSON_RE.match(l)
            if m:
                n = fix_num(m.group(1))
                if n and 1 <= n <= 50:
                    marks.append((i, "LESSON", n))
                continue
            if P3_RE.match(l):
                marks.append((i, "P3", None))
            elif P4_RE.match(l):
                marks.append((i, "P4", None))

        # Cat file thanh cac "doan" theo marker, roi xu ly tung doan.
        lesson_so_far = None
        for j, (i, kind, num) in enumerate(marks):
            end = marks[j + 1][0] if j + 1 < len(marks) else len(lines)
            if kind == "LESSON":
                lesson_so_far = num
                continue
            body_lines = lines[i + 1:end]

            # Tim cac cau huong dan co range trong doan nay.
            found = []
            for k, bl in enumerate(body_lines):
                mm = RANGE_RE.search(bl)
                if mm:
                    a, b = fix_num(mm.group(1)), fix_num(mm.group(2))
                    if a and b:
                        found.append((k, a, b))

            # Truong hop 2 tieu de lien nhau: doan cua P3 chua CA noi dung P3 lan P4.
            # Nhan biet: co >= 2 range, va range dau la 4-6 (P3) con range sau 7-9.
            if len(found) >= 2 and found[0][1] == 4 and found[1][1] == 7:
                # range 4-6 -> P3 (phan conversation), range 7-9 -> P4 (phan talk)
                k_p3 = found[0][0]
                k_p4 = found[1][0]
                # phan Talk (P4) nam giua k_p4 va k_p3 (vi P4 in truoc), phan
                # Conversation (P3) nam sau k_p3.
                p4_lines = body_lines[k_p4:k_p3] if k_p4 < k_p3 else body_lines[k_p4:]
                p3_lines = body_lines[k_p3:] if k_p4 < k_p3 else body_lines[k_p4:]
                blocks.append(dict(kind="P4", page=page, line=i + 1,
                                   body=clean_block(p4_lines), rng=(7, 9),
                                   after_lesson=lesson_so_far))
                blocks.append(dict(kind="P3", page=page, line=i + 1,
                                   body=clean_block(p3_lines), rng=(4, 6),
                                   after_lesson=lesson_so_far))
                continue

            rng = (found[0][1], found[0][2]) if found else None
            blocks.append(dict(kind=kind, page=page, line=i + 1,
                               body=clean_block(body_lines), rng=rng,
                               after_lesson=lesson_so_far, _raw_lines=body_lines))

        # --- Xu ly sau khi doc het 1 file: hai tieu de P3/P4 in LIEN NHAU ---
        # Neu khoi P3 rong (tieu de P3 dung ngay truoc tieu de P4) va khoi P4 ngay
        # sau do chua CA hai phan noi dung (2 range), thi tach lai theo range:
        #   4-6 -> Conversation (P3),  7-9 -> Talk (P4)
        fixed = []
        for k, b in enumerate(blocks):
            if (b["page"] == page and b["kind"] == "P3" and not b["body"]
                    and k + 1 < len(blocks)
                    and blocks[k + 1]["page"] == page
                    and blocks[k + 1]["kind"] == "P4"):
                nb = blocks[k + 1]
                raw = nb.get("_raw_lines")
                if not raw:
                    fixed.append(b)
                    continue
                found = []
                for t, bl in enumerate(raw):
                    mm = RANGE_RE.search(bl)
                    if mm:
                        a, bb = fix_num(mm.group(1)), fix_num(mm.group(2))
                        if a and bb:
                            found.append((t, a, bb))
                if len(found) >= 2 and found[0][1] == 7 and found[1][1] == 4:
                    t_p4, t_p3 = found[0][0], found[1][0]
                    fixed.append(dict(kind="P4", page=page, line=nb["line"],
                                      body=clean_block(raw[t_p4:t_p3]),
                                      rng=(7, 9), after_lesson=b["after_lesson"]))
                    fixed.append(dict(kind="P3", page=page, line=b["line"],
                                      body=clean_block(raw[t_p3:]),
                                      rng=(4, 6), after_lesson=b["after_lesson"]))
                    nb["_skip"] = True
                    continue
            fixed.append(b)
        blocks = [b for b in fixed if not b.get("_skip")]
    return blocks


def assign(blocks):
    """Gan tung khoi ve bai 1..50. Tra ve (lessons, notes).

    lessons[lid] = {"part3": str, "part4": str, "note": str}
    """
    notes = []
    p3_blocks = [b for b in blocks if b["kind"] == "P3"]

    # Buoc 1: P3 nam sau marker tren cung trang -> bai cua marker.
    for b in p3_blocks:
        if b["after_lesson"] is not None:
            b["lesson"] = b["after_lesson"]

    # Buoc 2: P3 dau trang khong co marker -> bai (P3 ke tiep da biet) - 1.
    for idx, b in enumerate(p3_blocks):
        if "lesson" in b:
            continue
        nxt = next((p3_blocks[k] for k in range(idx + 1, len(p3_blocks))
                    if "lesson" in p3_blocks[k]), None)
        if nxt:
            b["lesson"] = nxt["lesson"] - 1
            notes.append(
                "P3 %s:%d khong co marker -> gan bai %d (suy tu P3 ke tiep la bai %d)"
                % (b["page"], b["line"], b["lesson"], nxt["lesson"]))
        else:
            # P3 CUOI CUNG khong co marker: day la bai CUOI (50). Marker "LESSON 50"
            # nam o trang truoc (ngoai file hien tai), nen khong the suy tu "P3 ke
            # tiep". Kiem chung: file 373 chua Part 3 (range 4-6) + Part 4 (range 7-9)
            # cua bai Pharmacy, va bai 50 la bai cuoi sach.
            b["lesson"] = 50
            notes.append(
                "P3 %s:%d khong co marker va la P3 cuoi cung -> gan bai 50 "
                "(bai cuoi sach; marker LESSON 50 nam o trang truoc)"
                % (b["page"], b["line"]))

    # Buoc 3: P4 thuoc ve P3 cua CUNG BAI.
    #
    # Binh thuong P4 nam ngay SAU P3 (P3 cuoi trang, P4 dau trang sau), nen "P3
    # ngay truoc" la dung. NHUNG co truong hop P4 bi dat TRUOC P3 trong danh sach
    # khoi (ca biet: 2 tieu de in lien nhau, xem collect_blocks - file 373).
    # Xu ly: neu P4 dung ngay TRUOC mot P3 va ca hai deu chua co bai, gan P4 cho
    # chinh P3 do.
    last_p3 = None
    for idx, b in enumerate(blocks):
        if b["kind"] == "P3":
            last_p3 = b
            continue
        # P4: mac dinh lay bai cua P3 NGAY TRUOC (P3 cuoi trang -> P4 dau trang sau).
        #
        # CA BIET (file 373): 2 tieu de P3/P4 in LIEN NHAU nen P4 dung TRUOC P3 cua
        # chinh no. Dau hieu CHINH XAC, khong the nham:
        #   - P4 nay la P4 CUOI CUNG trong danh sach, VA
        #   - P3 ngay sau no la P3 CUOI CUNG, VA
        #   - P4 do khong co P3 nao truoc do cung trang (tuc la P4 "mo coi").
        # Khi do bai cua P3 ngay sau chinh la bai cua P4 nay.
        nxt = next((blocks[k] for k in range(idx + 1, len(blocks))
                    if blocks[k]["kind"] == "P3"), None)
        p4_total = sum(1 for x in blocks if x["kind"] == "P4")
        p4_seen = sum(1 for x in blocks[:idx + 1] if x["kind"] == "P4")
        p3_total = sum(1 for x in blocks if x["kind"] == "P3")
        p3_seen = sum(1 for x in blocks[:idx] if x["kind"] == "P3")
        inverted_pair = (
            nxt is not None
            and idx + 1 < len(blocks) and blocks[idx + 1] is nxt
            and nxt.get("lesson") is not None
            and p4_seen == p4_total and p3_seen + 1 == p3_total
        )
        if inverted_pair:
            b["lesson"] = nxt["lesson"]
        elif last_p3 is not None and last_p3.get("lesson") is not None:
            b["lesson"] = last_p3["lesson"]
        else:
            b["lesson"] = nxt.get("lesson") if nxt else None

    # Buoc 4: gom theo bai. Neu 1 bai co nhieu khoi cung loai (OCR cat lam nhieu
    # manh), NOI lai theo thu tu vat ly thay vi bo manh ngan.
    lessons = {}
    for b in blocks:
        lid = b.get("lesson")
        if not lid or lid < 1 or lid > 50:
            continue
        rec = lessons.setdefault(lid, {
            "part3": [], "part4": [], "ranges3": [], "ranges4": [],
            "pages3": [], "pages4": [], "notes": []})
        key = "part3" if b["kind"] == "P3" else "part4"
        if b["body"]:
            rec[key].append(b["body"])
        if b["rng"]:
            rec["ranges%s" % key[-1]].append(b["rng"])
        rec["pages%s" % key[-1]].append(b["page"])

    for lid, rec in lessons.items():
        for key in ("part3", "part4"):
            if len(rec[key]) > 1:
                rec["notes"].append(
                    "%s gom %d manh (OCR cat), da noi lai" % (key, len(rec[key])))
            rec[key] = " ".join(rec[key]).strip()
        rec["rng3"] = rec["ranges3"][0] if rec["ranges3"] else None
        rec["rng4"] = rec["ranges4"][0] if rec["ranges4"] else None
    return lessons, notes


def json_counts(lid):
    """So cau P3/P4 thuc co trong public/lessons_json/lesson_NN.json."""
    p = os.path.join(LESSONS_JSON, "lesson_%02d.json" % lid)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        li = json.load(f).get("listening") or {}
    return len(li.get("part3") or []), len(li.get("part4") or [])


def main():
    files = sorted(glob.glob(os.path.join(TS_DIR, "*_tapescripts.md")))
    if not files:
        print("LOI: khong tim thay file tapescript nao trong %s" % TS_DIR)
        return 1

    blocks = collect_blocks()
    lessons, notes = assign(blocks)
    n3 = sum(1 for b in blocks if b["kind"] == "P3")
    n4 = sum(1 for b in blocks if b["kind"] == "P4")

    out = {}
    for lid in range(1, 51):
        rec = lessons.get(lid)
        out[str(lid)] = {
            "lesson_id": lid,
            "part3": rec["part3"] if rec else "",
            "part4": rec["part4"] if rec else "",
        }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print("=== BAO CAO PARSE TAPESCRIPT ===")
    print("  so file doc          : %d" % len(files))
    print("  so khoi P3 / P4      : %d / %d" % (n3, n4))
    print("  so bai co tapescript : %d / 50"
          % sum(1 for v in out.values() if v["part3"] or v["part4"]))
    print("  -> da ghi %s" % os.path.relpath(OUT_PATH, ROOT))

    print("\n--- DOI CHIEU: tapescript noi bao nhieu cau vs JSON co bao nhieu ---")
    print("  %-5s %-11s %-11s %-22s %s"
          % ("bai", "ts P3/P4", "json P3/P4", "range trong tapescript", "ket luan"))
    mismatch, empty, norange = [], [], []
    for lid in range(1, 51):
        rec = lessons.get(lid)
        jc = json_counts(lid)
        ts3 = len(rec["part3"].split()) if rec and rec["part3"] else 0
        ts4 = len(rec["part4"].split()) if rec and rec["part4"] else 0
        # Chi so sanh khi JSON co cau hoi that.
        j3, j4 = jc if jc else (0, 0)
        if not rec or (not rec["part3"] and not rec["part4"]):
            if j3 or j4:
                empty.append(lid)
                verdict = "THIEU TAPESCRIPT (json co %d/%d cau)" % (j3, j4)
            else:
                verdict = "khong co bai listening -> bo qua"
            print("  %-5d %-11s %-11s %-22s %s"
                  % (lid, "-", "%d/%d" % (j3, j4), "-", verdict))
            continue
        r3, r4 = rec["rng3"], rec["rng4"]
        n_r3 = (r3[1] - r3[0] + 1) if r3 else None
        n_r4 = (r4[1] - r4[0] + 1) if r4 else None
        rg = "%s / %s" % (("%d-%d" % r3) if r3 else "-",
                          ("%d-%d" % r4) if r4 else "-")
        verdict = []
        if n_r3 is not None and j3 and n_r3 != j3:
            verdict.append("P3 LECH (ts noi %d, json co %d)" % (n_r3, j3))
        if n_r4 is not None and j4 and n_r4 != j4:
            verdict.append("P4 LECH (ts noi %d, json co %d)" % (n_r4, j4))
        if j3 and n_r3 is None:
            norange.append(lid)
        if not verdict:
            verdict.append("khop")
        else:
            mismatch.append(lid)
        print("  %-5d %-11s %-11s %-22s %s"
              % (lid, "%d/%d" % (ts3, ts4), "%d/%d" % (j3, j4), rg,
                 "; ".join(verdict)))

    empty3 = [l for l in range(1, 51) if not out[str(l)]["part3"]]
    empty4 = [l for l in range(1, 51) if not out[str(l)]["part4"]]
    both = [l for l in range(1, 51)
            if not out[str(l)]["part3"] and not out[str(l)]["part4"]]

    print("\n--- TONG KET ---")
    print("  bai co tapescript            : %d / 50"
          % sum(1 for v in out.values() if v["part3"] or v["part4"]))
    print("  bai KHONG co tapescript      : %d %s" % (len(both), both))
    print("  bai co listening ma thieu ts : %d %s" % (len(empty), empty))
    print("  bai lech so cau              : %d %s" % (len(mismatch), mismatch))
    print("  khoi P3 rong                 : %d %s" % (len(empty3), empty3))
    print("  khoi P4 rong                 : %d %s" % (len(empty4), empty4))

    if notes:
        print("\n--- GHI CHU KHI GAN BAI ---")
        for n in notes:
            print("  * %s" % n)

    return 1 if (mismatch or empty or empty3 or empty4) else 0


if __name__ == "__main__":
    sys.exit(main())
