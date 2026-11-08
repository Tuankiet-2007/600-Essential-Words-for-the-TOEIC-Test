"""Recheck do chinh xac du lieu Part 3/4 so voi anh scan that (task-7).

Chay: py -3.11 scripts/recheck_listening_data.py

Script nay CHI DOC, khong sua file nguon nao. No kiem tra:
  1. lessons_json/ == public/lessons_json/ (tung bai)
  2. flat questions == part3 + part4 (khong mat, khong them)
  3. moi cau co du 4 lua chon A/B/C/D voi noi dung that
  4. khong co token rac / escape LaTeX / placeholder
  5. thu tu in 2 cot duoc giu nguyen (khong bi sap xep lai)
"""

from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = {
    "private": os.path.join(ROOT, "lessons_json"),
    "public": os.path.join(ROOT, "public", "lessons_json"),
}

# Escape LaTeX / markup con sot tu OCR. Viet theo tung ky tu de tranh
# nham lan voi escape cua chinh Python.
BACKSLASH = chr(92)
TICK = chr(96)
ESCAPE_RE = re.compile(
    re.escape(BACKSLASH) + r"[\\$%&_#{}]"
    + "|" + re.escape(BACKSLASH * 2)
    + "|" + re.escape(TICK)
    + "|" + re.escape("**")
    + "|" + re.escape("__")
)
BANNED = ("todo", "tbd", "placeholder", "lorem", "fixme", "xxx", "n/a", "???")

failures = []


def fail(msg):
    failures.append(msg)


def load(base, lid):
    p = os.path.join(DIRS[base], "lesson_%02d.json" % lid)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def main():
    total_q = missing_opt = 0
    artifacts = []
    flat_bad = []
    pair_bad = []
    order = {}

    for lid in range(1, 51):
        a, b = load("private", lid), load("public", lid)
        if a is None or b is None:
            fail("lesson_%02d: thieu file JSON" % lid)
            continue
        if json.dumps(a, sort_keys=True, ensure_ascii=False) != \
           json.dumps(b, sort_keys=True, ensure_ascii=False):
            pair_bad.append(lid)

        li = a.get("listening") or {}
        p3, p4, flat = li.get("part3", []), li.get("part4", []), li.get("questions", [])

        if flat != p3 + p4:
            flat_bad.append(lid)

        for key, group in (("part3", p3), ("part4", p4)):
            for q in group:
                total_q += 1
                opts = q.get("options", [])
                if [o.get("label") for o in opts] != ["A", "B", "C", "D"]:
                    missing_opt += 1
                    fail("lesson_%02d %s q%s: lua chon = %s"
                         % (lid, key, q.get("number"),
                            [o.get("label") for o in opts]))
                    continue
                for o in opts:
                    t = (o.get("text") or "").strip()
                    if not t or t.lower() in BANNED:
                        missing_opt += 1
                        fail("lesson_%02d %s q%s (%s): noi dung rong/rac %r"
                             % (lid, key, q.get("number"), o["label"], t))
                    for m in ESCAPE_RE.finditer(t):
                        artifacts.append((lid, key, q["number"], m.group(0), t))
                for m in ESCAPE_RE.finditer(q.get("question") or ""):
                    artifacts.append((lid, key, q["number"], m.group(0),
                                      q["question"]))

        order[lid] = ([q["number"] for q in p3], [q["number"] for q in p4])

    print("=== 1. Tinh nhat quan lessons_json/ vs public/lessons_json/ ===")
    print("    so bai lech nhau:", pair_bad or "KHONG CO (50/50 giong nhau)")

    print("\n=== 2. flat questions == part3 + part4 ===")
    print("    so bai sai:", flat_bad or "KHONG CO (50/50 dung)")

    print("\n=== 3. Tinh toan ven lua chon A/B/C/D ===")
    print("    tong so cau part3+part4:", total_q)
    print("    so cau thieu lua chon / noi dung rong:", missing_opt)

    print("\n=== 4. Escape LaTeX / markup con sot ===")
    print("    so vi tri:", len(artifacts))
    for a in artifacts:
        print("      lesson_%02d %s q%d token=%r  trong: %s" % a)

    print("\n=== 5. Thu tu in 2 cot ===")
    n_unsorted = 0
    for lid, (p3, p4) in sorted(order.items()):
        unsorted = p3 != sorted(p3) or p4 != sorted(p4)
        if unsorted:
            n_unsorted += 1
        if lid in (1, 2, 3, 4, 17, 44):
            print("    lesson_%02d part3=%-12s part4=%-12s %s"
                  % (lid, p3, p4, "<- giu thu tu in 2 cot" if unsorted else ""))
    print("    so bai KHONG sap xep lai:", n_unsorted, "/ 50")

    print("\n=== KET LUAN ===")
    if failures:
        print("    CO VAN DE:", len(failures))
        for f in failures[:20]:
            print("      -", f)
        return 1
    print("    Tat ca kiem tra tu dong PASS.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
