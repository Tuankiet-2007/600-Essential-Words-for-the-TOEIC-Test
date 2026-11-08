"""Vá dữ liệu mà MinerU bỏ sót, đối chiếu trực tiếp với ảnh scan.

MinerU đôi khi bỏ nguyên một nhóm word-family mà KHÔNG báo lỗi: JSON vẫn hợp lệ,
chỉ thiếu dòng. Tự động đoán là sai — cách duy nhất đúng là mở ảnh scan trang đó
ra đọc rồi ghi lại.

Mỗi mục dưới đây đều đã được đối chiếu với ảnh scan tương ứng. Ghi rõ ảnh nào để
người sau kiểm tra lại được.

Dùng:
    python scripts/patch_missing.py            # chỉ vá lessons_json/
    python scripts/patch_missing.py --dry-run  # xem sẽ vá gì
"""
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "lessons_json")
PUBLIC_OUT = os.path.join(ROOT, "public", "lessons_json")

# ---------------------------------------------------------------------------
# Du lieu vá tay. Moi muc ghi ro: bai nao, nhom nao, doc tu anh scan nao.
#
# Bai 8 — anh: extracted_data/lesson_page_scans/lesson_08/059_word_families.png
#   Trang co 6 bang word-family. MinerU bo hoan toan bang thu 3
#   (expose / exposure / exposed) — khong co chu 'expos' nao trong Markdown.
#   Doc lai truc tiep tu anh:
#     expose    | As a matter of company policy, we try to expose all managers
#               | to the challenging work of telephone sales through hands-on
#               | experience.
#     exposure  | Exposure to the elements will corrode the container for the
#               | sensor.
#     exposed   | Mr. Lee was exposed to Chinese business practices during his
#               | three-year assignment as a manager in Beijing.
# ---------------------------------------------------------------------------
PATCHES = {
    8: [
        {
            "stem": "expose",
            "rows": [
                {
                    "word": "expose",
                    "example": (
                        "As a matter of company policy, we try to expose all "
                        "managers to the challenging work of telephone sales "
                        "through hands-on experience."
                    ),
                },
                {
                    "word": "exposure",
                    "example": (
                        "Exposure to the elements will corrode the container "
                        "for the sensor."
                    ),
                },
                {
                    "word": "exposed",
                    "example": (
                        "Mr. Lee was exposed to Chinese business practices "
                        "during his three-year assignment as a manager in "
                        "Beijing."
                    ),
                },
            ],
        },
    ],
}


def apply_patch(lesson, patch):
    """Chen cac dong con thieu vao dung nhom cua `stem`.

    Tra ve so dong da them. Goi duoc tu noi khac (convert_available_lessons).
    """
    words = lesson.get("words_to_learn") or []
    target = None
    for w in words:
        if w.get("word", "").lower() == patch["stem"].lower():
            target = w
            break
    if target is None:
        return 0, f"khong tim thay tu goc '{patch['stem']}'"

    fam = target.setdefault("word_family", [])
    have = {r.get("word", "").lower() for r in fam}
    added = []
    for row in patch["rows"]:
        if row["word"].lower() in have:
            continue
        # Dong tu goc phai dung dau nhom.
        if row["word"].lower() == patch["stem"].lower() and fam:
            fam.insert(0, {"pos": "", "word": row["word"], "example": row["example"]})
        else:
            fam.append({"pos": "", "word": row["word"], "example": row["example"]})
        added.append(row["word"])
    return len(added), (f"them {added}" if added else "da co du, bo qua")


def apply_all_patches(lesson, lid):
    """Ap dung moi ban va cho bai `lid`. Tra ve (so_dong_them, [thong_bao])."""
    total = 0
    msgs = []
    for p in PATCHES.get(lid, []):
        n, msg = apply_patch(lesson, p)
        total += n
        msgs.append(f"{p['stem']} -> {msg}")
    n2, msg2 = adopt_orphan_examples(lesson, lid)
    total += n2
    if msg2:
        msgs.append(msg2)
    return total, msgs


# ---------------------------------------------------------------------------
# Muc tu bi MinerU bo MAT DONG TIEU DE nhung 2 cau vi du van con trong
# words_to_learn.md. Truong hop nay khoi phuc duoc TRUNG THUC: cac cau vi du la
# van ban that cua sach, chi thieu dong "N. tu loai, dinh nghia".
#
# Bai 31 — muc 10 'secure': md nhay tu muc 9 sang muc 11, nhung giua do con
#   nguyen 2 cau 'a. ... secure reservations ...' / 'b. The hostess secured ...'.
#   => nhan lai thanh muc 10, dinh nghia de trong (khong bia) + needs_review.
# ---------------------------------------------------------------------------
ORPHANS = {
    31: {
        "number": 10,
        "word": "secure",
        "pos": "v.",
        # nguyen van 2 cau trong md (da doi chieu)
        "examples": [
            "Despite the popularity of the restaurant, Max was able to secure "
            "reservations for this evening.",
            "The hostess secured us another chair, so we could eat together.",
        ],
        "source": "extracted_data/mineru_md/lesson_31/words_to_learn.md",
    },
}


def adopt_orphan_examples(lesson, lid):
    """Chen lai muc tu bi mat dong tieu de nhung con vi du."""
    spec = ORPHANS.get(lid)
    if not spec:
        return 0, ""
    words = lesson.get("words_to_learn") or []
    if any(w.get("word", "").lower() == spec["word"].lower() for w in words):
        return 0, f"{spec['word']} da co, bo qua"

    entry = {
        "id": spec["number"],
        "word": spec["word"],
        "pos": spec["pos"],
        "ipa": "",
        # Khong bia dinh nghia: de trong va danh dau can bo sung.
        "definition_en": "",
        "definition_vi": "",
        "examples": [{"en": e, "vi": ""} for e in spec["examples"]],
        "word_family": [],
        "needs_translation": True,
        "needs_review": True,
        "recovered_from": spec["source"],
    }
    words.append(entry)
    # Sap lai theo so thu tu trong sach.
    words.sort(key=lambda w: w.get("id") or 99)
    for i, w in enumerate(words, 1):
        w["id"] = i
    return 1, f"khoi phuc muc tu '{spec['word']}' (con vi du, thieu tieu de)"


def main():
    dry = "--dry-run" in sys.argv
    for lid, patches in sorted(PATCHES.items()):
        path = os.path.join(OUT_DIR, f"lesson_{lid:02d}.json")
        if not os.path.isfile(path):
            print(f"L{lid:02d}: chua co JSON, bo qua")
            continue
        with open(path, encoding="utf-8") as f:
            lesson = json.load(f)

        before = sum(len(w.get("word_family") or [])
                     for w in lesson.get("words_to_learn") or [])
        for p in patches:
            n, msg = apply_patch(lesson, p)
            print(f"L{lid:02d}: {p['stem']} -> {msg}")
        after = sum(len(w.get("word_family") or [])
                    for w in lesson.get("words_to_learn") or [])

        if dry:
            print(f"L{lid:02d}: {before} -> {after} dong (dry-run, khong ghi)")
            continue

        lesson.setdefault("_meta", {})["patched"] = True
        lesson["_meta"]["patch_note"] = (
            "Mot so dong duoc doc lai tu anh scan vi MinerU bo sot"
        )
        with open(path, "w", encoding="utf-8") as f:
            json.dump(lesson, f, ensure_ascii=False, indent=2)
        os.makedirs(PUBLIC_OUT, exist_ok=True)
        shutil.copy2(path, os.path.join(PUBLIC_OUT, f"lesson_{lid:02d}.json"))
        print(f"L{lid:02d}: {before} -> {after} dong  (da ghi + publish)")


if __name__ == "__main__":
    main()
