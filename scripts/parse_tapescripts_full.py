"""Parse day du 50 bai Listening Tapescripts (Part 1, Part 2, Part 3, Part 4)
tu 34 file Markdown da tach 2 cot (extracted_data/mineru_md/tapescripts_full/340..373_tapescripts.md).

Chay:
    py -3.11 scripts/parse_tapescripts_full.py

Ket qua ghi ra:
    - scripts/data/tapescripts_full.json
    - public/answers/tapescripts_full.json
"""

from __future__ import annotations

import glob
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TS_FULL_DIR = os.path.join(ROOT, "extracted_data", "mineru_md", "tapescripts_full")
OUT_DATA_PATH = os.path.join(ROOT, "scripts", "data", "tapescripts_full.json")
OUT_PUBLIC_PATH = os.path.join(ROOT, "public", "answers", "tapescripts_full.json")

PREVIOUSLY_MISSING_16 = [1, 5, 8, 11, 14, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50]

# Dong tieu de / chan trang can loai bo
PAGE_NOISE_RE = re.compile(
    r"^\s*\d{3}\s+600\s+ESSENT"
    r"|^\s*(?:600|OO)\s+E"
    r"|^\s*APPENDIX\s+\d{3}\s*$"
    r"|^\s*\d{3}\s*$"
    r"|^\s*Appe\s*$"
    r"|^\s*»ldix\s*$"
    r"|^\s*Tapescript\s+for\s+the\s+Listening"
    r"|^\s*I?\s*Comprehension\s+Exercises\s*$",
    re.I,
)

# Sua mot so loi nhan dang chu pho bien cua Windows OCR tren font in sach
OCR_WORD_FIXES = [
    (r"\bpleaSe\b", "please"),
    (r"\bwitl\b", "will"),
    (r"\brealty\b", "really"),
    (r"\bfeltow\b", "fellow"),
    (r"\bPersonnei\b", "Personnel"),
    (r"\bThe tast provision\b", "The last provision"),
    (r"\bI'm not sure t can\b", "I'm not sure I can"),
    (r"\beat on the(?=\s+\[)", "eat on the trip."),
    (r"\bI like to(?=\s+\[)", "I like to laugh."),
    (r"\bsame old boring(?=\s+\[)", "same old boring stuff."),
    (r"Administrators emphasize the importance of\s*$", "Administrators emphasize the importance of rest."),
    (r"•", " "),
]


def clean_ocr_typos(text: str) -> str:
    for pat, repl in OCR_WORD_FIXES:
        text = re.sub(pat, repl, text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def normalize_speaker_tags(text: str) -> str:
    """Chuan hoa nhan nguoi noi [M] / [W] bi OCR doc nham ([MI, [WI, [VV], [MJ...)."""
    # Chuan hoa [W]
    text = re.sub(
        r"[\[\(]\s*(?:VV|VI|V|Wl|W1|WI|W)\s*[Il1J]?\s*[\]\)]?(?=\s|$)",
        "[W]",
        text,
    )
    # Chuan hoa [M]
    text = re.sub(
        r"[\[\(]\s*M\s*[Il1J]?\s*[\]\)]?(?=\s|$)",
        "[M]",
        text,
    )
    return text


def split_sentences(text: str) -> list[str]:
    """Tach van ban thanh cac cau ket thuc bang ., ?, ! (khong cat sau Mr., Ms., Dr., U.S.)."""
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    # Tach sau dau . ? ! khi khong phai Mr./Ms./Mrs./Dr.
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9(\[\"'])", text)
    out = []
    for p in parts:
        p = p.strip()
        if p:
            out.append(p)
    return out


def format_part1(raw: str) -> str:
    """Chuan hoa Part 1: Photo thanh:
    Number 1. Look at the picture marked Number 1.
    (A) ...
    (B) ...
    (C) ...
    (D) ...
    """
    lines = [
        ln.strip()
        for ln in raw.splitlines()
        if ln.strip() and not PAGE_NOISE_RE.match(ln.strip())
    ]
    joined = clean_ocr_typos(" ".join(lines))
    # Bo cau huong dan dau Part 1
    body = re.sub(
        r"^.*?(?:Look\s+at\s+the\s+picture\s+marked\s+number\s+1\s*\.?)\s*",
        "",
        joined,
        flags=re.I,
    ).strip()

    # Bo cac nhan (A)/(B)/(C)/(D) cu de tach thanh 4 cau roi gan lai (A)..(D) dong nhat
    body_no_labels = re.sub(r"\(\s*[A-D0-9]\s*\)\s*", "", body)
    sents = split_sentences(body_no_labels)

    letters = ["A", "B", "C", "D"]
    if len(sents) == 4:
        opts = [f"({letters[i]}) {sents[i]}" for i in range(4)]
    else:
        # Du phong: tach theo nhan (A)..(D) hoac tung dong
        opts = []
        for idx, s in enumerate(sents[:4]):
            lbl = letters[idx] if idx < 4 else "D"
            opts.append(f"({lbl}) {s}")

    return "Number 1. Look at the picture marked Number 1.\n" + "\n".join(opts)


def format_part2_question(q_num: int, raw_block: str) -> str:
    """Chuan hoa 1 cau hoi trong Part 2 (Number 2 hoac Number 3):
    Number N. <Cau hoi>
    (A) <Lua chon A>
    (B) <Lua chon B>
    (C) <Lua chon C>
    """
    # Bo nhan (A)/(B)/(C) de tach thanh 4 cau: 1 cau hoi + 3 cau tra loi
    cleaned = re.sub(r"\(\s*[A-D0-9]\s*\)\s*", "", raw_block).strip()
    sents = split_sentences(cleaned)

    if len(sents) >= 4:
        # Doi khi cau hoi hoac 1 dap an gom 2 cau ngan; uu tien neu co dau ? o cau dau
        q_sent = sents[0]
        rem = sents[1:]
        if len(rem) == 3:
            a_sent, b_sent, c_sent = rem[0], rem[1], rem[2]
        else:
            # Dung vi tri (A), (B), (C) trong raw_block neu > 4 cau
            a_sent, b_sent, c_sent = rem[0], rem[1], " ".join(rem[2:])
    elif len(sents) == 3:
        q_sent = sents[0]
        a_sent = sents[1]
        b_sent = sents[2]
        c_sent = ""
    else:
        return f"Number {q_num}. {cleaned}"

    out_lines = [f"Number {q_num}. {q_sent}"]
    if a_sent:
        out_lines.append(f"(A) {a_sent}")
    if b_sent:
        out_lines.append(f"(B) {b_sent}")
    if c_sent:
        out_lines.append(f"(C) {c_sent}")
    return "\n".join(out_lines)


def format_part2(raw: str) -> str:
    """Chuan hoa Part 2: Question-Response (Number 2 va Number 3)."""
    lines = [
        ln.strip()
        for ln in raw.splitlines()
        if ln.strip() and not PAGE_NOISE_RE.match(ln.strip())
    ]
    joined = clean_ocr_typos(" ".join(lines))
    # Bo dong huong dan "Numbers 2 and 3..." neu co
    joined = re.sub(
        r"^Numbers?\s+2\s+and\s+3[^\n.]*\.\s*",
        "",
        joined,
        flags=re.I,
    ).strip()

    m = re.search(
        r"Number\s*2\s*[.:]?\s*(.*?)\s*Number\s*3\s*[.:]?\s*(.*)",
        joined,
         flags=re.I | re.S,
    )
    if not m:
        return joined

    q2_raw, q3_raw = m.group(1).strip(), m.group(2).strip()
    return format_part2_question(2, q2_raw) + "\n" + format_part2_question(3, q3_raw)


def format_part3(raw: str) -> str:
    """Chuan hoa Part 3: Conversation (giu nhan [M]/[W], moi luot thoai 1 dong)."""
    lines = [
        ln.strip()
        for ln in raw.splitlines()
        if ln.strip() and not PAGE_NOISE_RE.match(ln.strip())
    ]
    joined = clean_ocr_typos(" ".join(lines))
    # Bo cau huong dan dau Part 3
    joined = re.sub(
        r"^(?:Numbers?|Questions?)\s+[0-9OIl]+\s+through\s+[0-9OIl]+\s+relate\s+to\s+the\s+following\s+conversation\s*\.?\s*",
        "",
        joined,
        flags=re.I,
    ).strip()

    joined = normalize_speaker_tags(joined)
    # Xuong dong truoc moi nhan [M] hoac [W] de de doc
    joined = re.sub(r"\s+(?=\[[MW]\])", "\n", joined)
    return joined.strip()


def format_part4(raw: str) -> str:
    """Chuan hoa Part 4: Talk."""
    lines = [
        ln.strip()
        for ln in raw.splitlines()
        if ln.strip() and not PAGE_NOISE_RE.match(ln.strip())
    ]
    joined = clean_ocr_typos(" ".join(lines))
    # Bo cau huong dan dau Part 4
    joined = re.sub(
        r"^(?:Numbers?|Questions?)\s+[0-9OIl]+\s+through\s+[0-9OIl]+\s+relate\s+to\s+the\s+following\s+(?:recording|talk|conversation)\s*\.?\s*",
        "",
        joined,
        flags=re.I,
    ).strip()
    joined = normalize_speaker_tags(joined)
    return joined.strip()


def parse_all_lessons() -> dict[str, dict]:
    files = sorted(glob.glob(os.path.join(TS_FULL_DIR, "*_tapescripts.md")))
    if len(files) < 34:
        raise RuntimeError(
            f"Tim thay {len(files)} file trong {TS_FULL_DIR} (can du 34 trang 340..373)"
        )

    all_lines: list[str] = []
    for p in files:
        with open(p, encoding="utf-8", errors="replace") as f:
            for ln in f.read().splitlines():
                s = ln.strip()
                if not s or PAGE_NOISE_RE.match(s):
                    continue
                all_lines.append(s)

    full_text = "\n".join(all_lines)
    chunks = re.split(r"(?m)^LESSON\s+(\d+)\s*$", full_text)

    lessons_out: dict[str, dict] = {}
    for i in range(1, len(chunks), 2):
        lid = int(chunks[i])
        body = chunks[i + 1]

        m1 = re.search(
            r"(?ms)^(?:Part|Pan)\s*1\b[^\n]*\n(.*?)(?=^(?:Part|Pan)\s*2\b)",
            body,
            re.I,
        )
        m2 = re.search(
            r"(?ms)^(?:Part|Pan)\s*2\b[^\n]*\n(.*?)(?=^(?:Part|Pan)\s*3\b)",
            body,
            re.I,
        )
        m3 = re.search(
            r"(?ms)^(?:Part|Pan)\s*3\b[^\n]*\n(.*?)(?=^(?:Part|Pan)\s*4\b)",
            body,
            re.I,
        )
        m4 = re.search(
            r"(?ms)^(?:Part|Pan)\s*4\b[^\n]*\n(.*)",
            body,
            re.I,
        )

        p1 = format_part1(m1.group(1)) if m1 else ""
        p2 = format_part2(m2.group(1)) if m2 else ""
        p3 = format_part3(m3.group(1)) if m3 else ""
        p4 = format_part4(m4.group(1)) if m4 else ""

        lessons_out[str(lid)] = {
            "lesson_id": lid,
            "part1": p1,
            "part2": p2,
            "part3": p3,
            "part4": p4,
        }

    return lessons_out


def main() -> int:
    out = parse_all_lessons()

    os.makedirs(os.path.dirname(OUT_DATA_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(OUT_PUBLIC_PATH), exist_ok=True)

    with open(OUT_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    shutil.copyfile(OUT_DATA_PATH, OUT_PUBLIC_PATH)

    c_p1 = sum(1 for k in range(1, 51) if out.get(str(k), {}).get("part1"))
    c_p2 = sum(1 for k in range(1, 51) if out.get(str(k), {}).get("part2"))
    c_p3 = sum(1 for k in range(1, 51) if out.get(str(k), {}).get("part3"))
    c_p4 = sum(1 for k in range(1, 51) if out.get(str(k), {}).get("part4"))
    c_all = sum(
        1
        for k in range(1, 51)
        if all(out.get(str(k), {}).get(p) for p in ("part1", "part2", "part3", "part4"))
    )
    c_prev16 = sum(
        1
        for k in PREVIOUSLY_MISSING_16
        if all(out.get(str(k), {}).get(p) for p in ("part1", "part2", "part3", "part4"))
    )

    print("=== BAO CAO PARSE TAPESCRIPTS FULL (PART 1..4) ===")
    print(f"  Tong so bai co du 4 phan (Part 1..4): {c_all} / 50")
    print(f"  Part 1 (Photo)                      : {c_p1} / 50")
    print(f"  Part 2 (Question-Response)          : {c_p2} / 50")
    print(f"  Part 3 (Conversation)               : {c_p3} / 50")
    print(f"  Part 4 (Talk)                       : {c_p4} / 50")
    print(f"  16 bai tung bi thieu truoc day      : {c_prev16} / 16 da khôi phuc du 4 phan")
    print(f"  -> Da ghi: {os.path.relpath(OUT_DATA_PATH, ROOT)}")
    print(f"  -> Da ghi: {os.path.relpath(OUT_PUBLIC_PATH, ROOT)}")

    return 0 if c_all == 50 else 1


if __name__ == "__main__":
    sys.exit(main())
