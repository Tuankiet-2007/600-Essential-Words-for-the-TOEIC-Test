import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSONS_DIR = os.path.join(ROOT, "public", "lessons_json")
SCRATCH_DIR = r"C:\Users\LEGION\.gemini\antigravity\brain\dd06d532-873e-4cf4-997f-622fdb86edbc\scratch"
os.makedirs(SCRATCH_DIR, exist_ok=True)

def main():
    batches = [
        (1, 10, "batch_1.json"),
        (11, 20, "batch_2.json"),
        (21, 30, "batch_3.json"),
        (31, 40, "batch_4.json"),
        (41, 50, "batch_5.json"),
    ]
    for start, end, fname in batches:
        out = {}
        for lid in range(start, end + 1):
            path = os.path.join(LESSONS_DIR, f"lesson_{lid:02d}.json")
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            words_info = []
            for w in data.get("words_to_learn", []):
                words_info.append({
                    "id": w.get("id"),
                    "word": w.get("word"),
                    "pos": w.get("pos"),
                    "definition_en": w.get("definition_en"),
                    "examples": [ex.get("en", "") for ex in w.get("examples", [])],
                    "book_word_family": [r.get("word", "") for r in w.get("word_family", []) if isinstance(r, dict)],
                })
            out[str(lid)] = {
                "lesson_id": lid,
                "title": data.get("title", ""),
                "theme_name": data.get("theme_name", ""),
                "words": words_info,
                "lesson_word_families": data.get("word_families", []),
            }
        out_path = os.path.join(SCRATCH_DIR, fname)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
