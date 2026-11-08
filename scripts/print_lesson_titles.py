"""Print the authoritative lesson titles from book_structure_map.json."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(ROOT, "book_structure_map.json"), encoding="utf-8") as f:
    d = json.load(f)

rows = []
for l in d["lessons"]:
    rows.append((l["lesson_id"], l["theme_id"], l["theme_name"], l["title"]))

for lid, tid, theme, title in rows:
    print(f"{lid:2d} | theme {tid:2d} | {theme:24s} | {title}")

# Emit a JS object literal ready to paste into curriculum.js
print("\n--- JS ---")
print("export const LESSON_TITLES = {")
line = "  "
for lid, _tid, _theme, title in rows:
    piece = f"{lid}: {json.dumps(title, ensure_ascii=False)}, "
    if len(line) + len(piece) > 96:
        print(line.rstrip())
        line = "  "
    line += piece
if line.strip():
    print(line.rstrip())
print("};")
