"""coverage_report.py — do muc do bao phu dap an + giai thich sau khi noi vao UI."""
import glob
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

ak = json.load(open("scripts/data/answer_key.json", encoding="utf-8"))
ex = json.load(open("scripts/data/explanations.json", encoding="utf-8"))

tot_q = graded = with_ex = 0
listen_q = listen_graded = 0
no_ans = []

for f in sorted(glob.glob("public/lessons_json/lesson_*.json")):
    j = json.load(open(f, encoding="utf-8"))
    lid = str(j["lesson_id"])
    prac = j.get("practice", {})
    # Listening nam o CAP BAI HOC (j["listening"]), khong phai practice.listening.
    # Loader gop ca hai, nhung JSON goc chi co o cap bai.
    lst = j.get("listening", {}) or {}
    if not lst.get("part3") and not lst.get("part4"):
        lst = prac.get("listening", {}) or lst

    nums = []
    # Part 1 (chi co anh)
    p1 = lst.get("part1")
    if p1:
        nums.append(p1.get("question_num", 1))
    lnums = []
    for k in ("part2", "part3", "part4"):
        for q in lst.get(k, []) or []:
            nums.append(q["number"])
            lnums.append(q["number"])
    for q in prac.get("part5", []) or []:
        nums.append(q["number"])
    for q in (prac.get("part6") or {}).get("questions", []) or []:
        nums.append(q["number"])
    for b in prac.get("part7", []) or []:
        for q in b.get("questions", []) or []:
            nums.append(q["number"])

    tk = ak.get(lid, {}).get("word_practice", {})
    for n in nums:
        tot_q += 1
        if str(n) in tk and tk[str(n)]:
            graded += 1
        else:
            no_ans.append((lid, n))
        if str(n) in ex.get(lid, {}):
            with_ex += 1
    for n in lnums:
        listen_q += 1
        if str(n) in tk and tk[str(n)]:
            listen_graded += 1

print("TONG SO CAU HOI trong app        : %d" % tot_q)
print("  cham duoc (co dap an Answer Key): %d  (%.1f%%)" % (graded, graded / tot_q * 100))
print("  co giai thich                   : %d  (%.1f%%)" % (with_ex, with_ex / tot_q * 100))
print()
print("Listening Part 2-4               : %d cau" % listen_q)
print("  cham duoc                      : %d  (%.1f%%)" % (listen_graded, listen_graded / listen_q * 100))
print()
print("So cau CHUA co dap an            : %d" % len(no_ans))
if no_ans:
    print("  chi tiet (bai, cau):", no_ans)
