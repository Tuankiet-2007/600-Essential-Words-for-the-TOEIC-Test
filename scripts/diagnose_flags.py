"""Chan doan cac bai bi canh bao: parser sot hay MinerU bo sot?

Voi moi bai, in:
  - tu nao con thieu vi du / word-family
  - neu word-family thieu: grep Markdown goc xem co tu cung goc khong
    (co -> parser doc sai dinh dang; khong -> MinerU bo that, can doc anh scan)
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_mineru_local as r  # noqa: E402

FLAGGED = [11, 12, 15, 20, 21, 22, 24, 26, 27, 31, 33, 36, 37, 39]


def stem_of(w):
    w = w.lower().split()[0]
    for suf in ("ations", "ation", "ments", "ment", "ings", "ing",
                "able", "ible", "ally", "edly", "ance", "ence",
                "ity", "ies", "ive", "ous", "ate", "ed", "ly", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


for lid in FLAGGED:
    path = os.path.join(r.OUT_DIR, f"lesson_{lid:02d}.json")
    if not os.path.isfile(path):
        continue
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    words = d.get("words_to_learn") or []
    print(f"=== L{lid:02d} ({len(words)} tu) ===")

    # Tu thieu vi du
    for w in words:
        ne = len(w.get("examples") or [])
        nf = len(w.get("word_family") or [])
        marks = []
        if ne < 2:
            marks.append(f"{ne}vi du")
        if nf < 3:
            marks.append(f"{nf}fam")
        if marks:
            print(f"  [{w['word']}] {', '.join(marks)}")
            # grep md goc xem co tu cung goc trong word_families.md khong
            st = stem_of(w["word"])
            fam_md = r.read_md(lid, "word_families") or ""
            hits = re.findall(rf"\b{re.escape(st)}\w*", fam_md, re.I)
            hits = sorted(set(h.lower() for h in hits))
            if hits:
                print(f"      -> md CO '{st}*': {hits}  (parser doc sot)")
            else:
                print(f"      -> md KHONG co '{st}*'  (MinerU bo sot -> can doc scan)")

    if len(words) != 12:
        print(f"  !! so tu = {len(words)}")
    ctx = d.get("words_in_context") or {}
    if len(ctx.get("word_bank") or []) != 12:
        print(f"  !! word_bank = {ctx.get('word_bank')}")
    print()
