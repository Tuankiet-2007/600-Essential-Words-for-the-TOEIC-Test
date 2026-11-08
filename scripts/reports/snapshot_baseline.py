"""Chup lai trang thai public/lessons_json/ TRUOC khi va parse_listening (task-1).

Muc dich: co moc "before" de so sanh sau khi chay lai converter, phat hien hoi quy
o cac phan KHONG lien quan (so tu, vi du, word-family, word_bank, blanks).

Chay:  py -3.11 scripts/reports/snapshot_baseline.py [--out <path>]
Mac dinh ghi: scripts/reports/baseline_before_part_fix.json
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PUBLIC_OUT = os.path.join(ROOT, "public", "lessons_json")
DEFAULT_OUT = os.path.join(ROOT, "scripts", "reports", "baseline_before_part_fix.json")

FIELDS = ("words", "examples", "family", "bank", "blanks",
          "listening_questions", "listening_instructions")


def snapshot_lesson(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
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
        "listening_instructions": len((lis.get("instructions") or "").strip()),
        # Chi ghi nhan su TON TAI cua part3/part4 (day chinh la thu task-1 se doi).
        "has_part3_key": "part3" in lis,
        "has_part4_key": "part4" in lis,
        "listening_keys": sorted(lis.keys()),
        "question_numbers": [q.get("number") for q in (lis.get("questions") or [])],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()

    lessons = {}
    missing = []
    for lid in range(1, 51):
        p = os.path.join(PUBLIC_OUT, f"lesson_{lid:02d}.json")
        if not os.path.isfile(p):
            missing.append(lid)
            continue
        lessons[f"{lid:02d}"] = snapshot_lesson(p)

    with_text = [lid for lid, s in lessons.items() if s["listening_questions"] > 0]

    data = {
        "_what": ("Baseline cua public/lessons_json/ chup TRUOC khi sua "
                  "parse_listening de xuat part3/part4 (task-1)."),
        "_generated_by": "scripts/reports/snapshot_baseline.py",
        "source_dir": "public/lessons_json",
        "lesson_count": len(lessons),
        "missing_lessons": missing,
        "lessons_with_listening_text": sorted(with_text),
        "lessons_with_listening_text_count": len(with_text),
        "fields": list(FIELDS),
        "lessons": lessons,
    }

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)

    print(f"Snapshot {len(lessons)} bai -> {os.path.relpath(args.out, ROOT)}")
    if missing:
        print(f"THIEU file: {missing}", file=sys.stderr)
    print(f"Co text nghe: {len(with_text)} bai {sorted(with_text)}")
    print("Tong: " + ", ".join(
        f"{k}={sum(s[k] for s in lessons.values())}"
        for k in ("words", "examples", "family", "bank", "blanks", "listening_questions")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
