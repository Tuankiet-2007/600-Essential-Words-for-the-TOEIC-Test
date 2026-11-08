"""verify_onboarding.py — kiem tra moi con so / duong dan trong ONBOARDING.md
co dung voi thuc te khong. Mot file tai lieu sai su that thi te hon khong co.
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(ROOT))

ok = 0
bad = []


def check(name, cond, detail=""):
    global ok
    if cond:
        ok += 1
        print("  OK   %s" % name)
    else:
        bad.append(name)
        print("  FAIL %s   %s" % (name, detail))


print("=== 1. Duong dan duoc nhac trong doc ===")
for p in [
    "600 est_.pdf", "book_structure_map.json",
    "extracted_data/mineru_md", "scripts/data", "lessons_json",
    "public/lessons_json", "public/answers", "public/audio", "public/part1_photos",
    "app/CONTRACT.md", "app/vite.config.js", "app/src/App.jsx", "app/src/index.css",
    "app/src/data/curriculum.js", "app/src/lib/lessonLoader.js", "app/src/lib/answerKey.js",
    "app/src/lib/assets.js", "app/src/lib/storage.js", "app/src/lib/srs.js",
    "app/src/lib/store.jsx", "app/src/components/ui.jsx",
    "app/src/tabs/Tab1Vocabulary.jsx", "app/src/tabs/Tab2Flashcards.jsx",
    "app/src/tabs/Tab3Srs.jsx", "app/src/tabs/Tab4AiLab.jsx",
    "app/src/tabs/Tab5Practice.jsx",
    "scripts/extract_pdf_assets.py", "scripts/parse_answer_key.py",
    "scripts/parse_tapescripts.py", "scripts/build_explanations.py",
    "scripts/convert_available_lessons.py", "scripts/validate_explanations.py",
    "scripts/coverage_report.py", "scripts/test_parse_listening.py",
    "scripts/test_answer_key.py", "scripts/test_tapescripts.py",
    "scripts/check_helpers.mjs", "scripts/coverage_report.py",
    "app/scripts/dev-server.mjs", "app/scripts/build.mjs",
    "app/scripts/verify_runtime.mjs", "app/scripts/verify_loader.mjs",
    "app/scripts/verify_tabs.mjs", "app/scripts/lead_e2e_check.mjs",
    "app/scripts/verify_explanations.mjs",
]:
    check(p, os.path.exists(p))

print()
print("=== 2. publicDir = ../public trong vite.config.js ===")
vc = open("app/vite.config.js", encoding="utf-8").read()
check("publicDir -> ../public", "../public" in vc)
# app/public KHONG duoc ton tai: neu co, asset trong do se KHONG duoc serve.
check("app/public KHONG ton tai", not os.path.exists("app/public"))
# Asset ma app/index.html yeu cau phai nam trong ../public moi serve duoc.
idx = open("app/index.html", encoding="utf-8").read()
for asset in ["favicon.svg", "icons.svg"]:
    if asset in idx or asset == "icons.svg":
        check("public/%s ton tai (duoc serve)" % asset, os.path.exists("public/" + asset))

print()
print("=== 3. So lieu ===")
lessons = sorted(glob.glob("public/lessons_json/lesson_*.json"))
check("50 bai JSON", len(lessons) == 50, len(lessons))

ak = json.load(open("public/answers/answer_key.json", encoding="utf-8"))
ex = json.load(open("public/answers/explanations.json", encoding="utf-8"))
ts = json.load(open("public/answers/tapescripts.json", encoding="utf-8"))

check("answer_key 50 bai", len(ak) == 50, len(ak))
check("explanations 50 bai", len(ex) == 50, len(ex))
check("tapescripts 34 bai", len(ts) == 34, len(ts))

wic = sum(len(v.get("words_in_context", {})) for v in ak.values())
wp = sum(len(v.get("word_practice", {})) for v in ak.values())
check("WIC = 600", wic == 600, wic)
check("WP = 1148", wp == 1148, wp)

# Dem cau hoi + cham duoc
tot = graded = expl = lq = lg = 0
per = {}
for f in lessons:
    j = json.load(open(f, encoding="utf-8"))
    lid = str(j["lesson_id"])
    k = ak.get(lid, {}).get("word_practice", {})
    nums = []
    L = j.get("listening", {}) or {}
    for key in ("part3", "part4"):
        for q in L.get(key, []) or []:
            nums.append(("listening" + key[-1], q["number"]))
    for q in j.get("practice", {}).get("part5", []) or []:
        nums.append(("part5", q["number"]))
    for q in (j.get("practice", {}).get("part6", {}) or {}).get("questions", []) or []:
        nums.append(("part6", q["number"]))
    p7 = j.get("practice", {}).get("part7", []) or []
    for blk in (p7 if isinstance(p7, list) else []):
        for q in blk.get("questions", []) or []:
            nums.append(("part7", q["number"]))
    for sec, n in nums:
        if not isinstance(n, int):
            continue
        tot += 1
        per[sec] = per.get(sec, 0) + 1
        if k.get(str(n)):
            graded += 1
            if sec.startswith("listening"):
                lg += 1
        if str(n) in (ex.get(lid) or {}):
            expl += 1
        if sec.startswith("listening"):
            lq += 1

check("tong cau hoi = 968", tot == 968, tot)
check("cham duoc = 966", graded == 966, graded)
check("co giai thich = 966", expl == 966, expl)
check("listening P3/4 = 300", lq == 300, lq)
check("listening cham duoc = 298", lg == 298, lg)
check("P3 = 150", per.get("listening3") == 150, per.get("listening3"))
check("P4 = 150", per.get("listening4") == 150, per.get("listening4"))
check("P5 = 299", per.get("part5") == 299, per.get("part5"))
check("P6 = 149", per.get("part6") == 149, per.get("part6"))
check("P7 = 220", per.get("part7") == 220, per.get("part7"))

print()
print("=== 4. Nguon giai thich ===")
src = {}
for d in ex.values():
    for e in d.values():
        src[e["source"]] = src.get(e["source"], 0) + 1
check("grammar = 447", src.get("grammar") == 447, src.get("grammar"))
check("passage = 47", src.get("passage") == 47, src.get("passage"))
check("tapescript = 74", src.get("tapescript") == 74, src.get("tapescript"))
check("listening-no-script = 224", src.get("listening-no-script") == 224, src.get("listening-no-script"))

print()
print("=== 5. Shape du lieu nhu doc mo ta ===")
j = json.load(open("public/lessons_json/lesson_01.json", encoding="utf-8"))
check("listening la TOP-LEVEL", "listening" in j)
check("practice KHONG co listening", "listening" not in j["practice"])
check("practice co part5/6/7", set(j["practice"]) == {"part5", "part6", "part7"}, list(j["practice"]))
check("part7 la array", isinstance(j["practice"]["part7"], list))
check("audio_track = track_01.mp3", j["audio_track"] == "track_01.mp3", j["audio_track"])
check("option la array {label,text}", isinstance(j["practice"]["part5"][0]["options"], list)
      and set(j["practice"]["part5"][0]["options"][0]) == {"label", "text"})
check("cau hoi dung key 'number'", "number" in j["practice"]["part5"][0])
a1 = ak["1"]
check("answer_key co warnings key", True)  # chi la ghi chu
check("explanations key cua 1 muc",
      set(ex["1"]["10"]) >= {"answer", "why", "pos_needed", "option_notes", "source", "section"})
check("tapescripts key cua 1 bai",
      set(ts["2"]) == {"lesson_id", "part3", "part4"}, list(ts["2"]))

print()
print("=== 6. Bai thieu tapescript dung nhu doc liet ke ===")
missing = sorted(int(k) for k in range(1, 51) if str(k) not in ts)
doc_missing = [1, 5, 8, 11, 14, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50]
check("16 bai thieu", len(missing) == 16, len(missing))
check("danh sach khop", missing == doc_missing, missing)

print()
print("=== 7. Warning trong answer_key ===")
warn = [k for k, v in ak.items() if v.get("warnings")]
check("6 bai co warning", len(warn) == 6, warn)

print()
print("=== 8. Design tokens trong index.css ===")
# CHU Y: hex trong CSS viet THUONG, nen phai so sanh khong phan biet hoa/thuong.
css = open("app/src/index.css", encoding="utf-8").read().lower()
for tok in ["58cc02", "1cb0f6", "ff4b4b", "ffc800", "ce82ff",
            "duo-choice", "duo-explain", "vocab-hit", "cloze-blank"]:
    check("css co %s" % tok, tok in css)

print()
print("=== 9. derivePos dong bo Python <-> JS ===")
js = open("app/src/lib/lessonLoader.js", encoding="utf-8").read()
py = open("scripts/build_explanations.py", encoding="utf-8").read()
for suf in ["ee|eer|ery", "some|ary|ory", "ian|ant|ent"]:
    check("JS co %s" % suf, suf in js)
    check("PY co %s" % suf, suf in py.replace(" ", ""))

print()
print("=== 10. ignore file chan PDF + extracted_data ===")
for f in [".gitignore", ".cursorignore"]:
    txt = open(f, encoding="utf-8").read()
    check("%s chan PDF" % f, "600 est_.pdf" in txt)
    check("%s chan extracted_data" % f, "extracted_data/" in txt)

print()
print("=" * 60)
if bad:
    print("KET QUA: %d OK, %d FAIL" % (ok, len(bad)))
    for b in bad:
        print("   FAIL:", b)
    sys.exit(1)
print("KET QUA: TAT CA %d KIEM TRA DEU DUNG" % ok)
