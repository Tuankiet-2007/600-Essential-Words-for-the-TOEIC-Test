"""validate_explanations.py — chan chat luong giai thich (chay trong CI).

Script nay KHONG sinh du lieu, chi KIEM TRA scripts/data/explanations.json.
Muc dich: bat lai dung nhung loi da tung xay ra, de khong tai dien:

  1. Giai thich rong / qua ngan -> nguoi hoc khong hoc duoc gi.
  2. Giai thich khong neu dap an -> khong doi chieu duoc voi Answer Key.
  3. Cau "vo nghia" lap lai y nguyen cho moi cau (loi cu: "can NGHE audio de tu
     danh gia" xuat hien o moi cau nghe, khong mang thong tin nao).
  4. KHONG co option_notes -> mat phan "vi sao phuong an khac sai".
  5. pos_needed mau thuan voi tu loai cua dap an -> giai thich SAI ngu phap.
  6. option_notes rong nghia.

Chay: py -3.11 scripts/validate_explanations.py
Exit 0 = dat, 1 = co loi.
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "scripts", "data", "explanations.json")
PUBLIC = os.path.join(ROOT, "public", "lessons_json")

# Cau khang dinh SAI da tung co trong ban cu — khong duoc xuat hien lai.
BANNED_PHRASES = [
    "cần NGHE audio để tự đánh giá",  # cau vo nghia lap lai
]

MIN_WHY = 60  # ky tu toi thieu cho mot giai thich co ich

failures = []
passes = 0


def check(name, ok, detail=""):
    global passes
    if ok:
        passes += 1
        print("PASS  %s%s" % (name, ("  " + detail) if detail else ""))
    else:
        failures.append("%s%s" % (name, ("  " + detail) if detail else ""))
        print("FAIL  %s%s" % (name, ("  " + detail) if detail else ""))


if not os.path.isfile(EX):
    print("LOI: thieu %s" % EX)
    sys.exit(1)

ex = json.load(open(EX, encoding="utf-8"))

total = 0
empty = []
short = []
no_answer_stmt = []
banned = []
no_notes = []
weak_note = []
pos_conflict = []

for lid, bucket in ex.items():
    path = os.path.join(PUBLIC, "lesson_%s.json" % str(lid).zfill(2))
    lesson = json.load(open(path, encoding="utf-8")) if os.path.isfile(path) else {}

    # map so cau -> cau hoi Part 5 (de doi chieu pos)
    p5 = {str(q["number"]): q for q in lesson.get("practice", {}).get("part5", []) or []}

    for num, e in bucket.items():
        total += 1
        why = e.get("why", "") or ""

        if not why.strip():
            empty.append((lid, num))
            continue
        if len(why) < MIN_WHY:
            short.append((lid, num, len(why)))
        if "Đáp án đúng là" not in why:
            no_answer_stmt.append((lid, num))
        for phrase in BANNED_PHRASES:
            if phrase in why:
                banned.append((lid, num, phrase))

        notes = e.get("option_notes") or {}
        if not notes:
            no_notes.append((lid, num))
        else:
            for lab, note in notes.items():
                # note phai giai thich duoc ly do, khong chi lap lai phuong an
                if len(note) < 25:
                    weak_note.append((lid, num, lab, note))

        # pos_needed phai khop tu loai cua dap an (neu ca hai deu xac dinh)
        need = e.get("pos_needed") or ""
        if need and num in p5:
            m = re.search(r"là <b>(động từ|danh từ|tính từ|trạng từ)</b>", why)
            if m:
                got = {"động từ": "verb", "danh từ": "noun",
                       "tính từ": "adjective", "trạng từ": "adverb"}[m.group(1)]
                if got != need:
                    chosen = ""
                    for o in p5[num].get("options", []):
                        if o["label"] == e["answer"]:
                            chosen = o["text"]
                    pos_conflict.append((lid, num, chosen, need, got))

print("=" * 72)
print("TONG KET: %d giai thich trong %d bai" % (total, len(ex)))
print("=" * 72)

check("khong co giai thich rong", not empty, str(empty[:5]))
check("khong co giai thich qua ngan (<%d ky tu)" % MIN_WHY, not short, str(short[:5]))
check("moi giai thich deu neu ro dap an", not no_answer_stmt, str(no_answer_stmt[:5]))
check("khong con cau vo nghia bi cam", not banned, str(banned[:3]))
check("moi giai thich deu co option_notes", not no_notes, str(no_notes[:5]))
check("moi option_note deu co ly do that", not weak_note, str(weak_note[:3]))
check("pos_needed khong mau thuan voi dap an", not pos_conflict, str(pos_conflict[:5]))

print()
if failures:
    print("KET QUA: KHONG DAT — %d assertion that bai." % len(failures))
    sys.exit(1)
print("KET QUA: DAT — %d/%d assertion PASS." % (passes, passes))
sys.exit(0)
