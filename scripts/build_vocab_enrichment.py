"""build_vocab_enrichment.py — Merge vocabulary enrichment data across all 50 lessons.

Updates:
  - scripts/data/vocab_enrichment.json
  - public/answers/vocab_enrichment.json
  - lessons_json/lesson_01.json .. lesson_50.json (ONLY words_to_learn enrichment fields & examples[].vi)
  - public/lessons_json/lesson_01.json .. lesson_50.json (ONLY words_to_learn enrichment fields & examples[].vi)

Usage:
  py -3.11 scripts/build_vocab_enrichment.py
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from vocab_data_batch1 import BATCH_DATA as B1
from vocab_data_batch2 import BATCH_DATA as B2
from vocab_data_batch3 import BATCH_DATA as B3
from vocab_data_batch4 import BATCH_DATA as B4
from vocab_data_batch5 import BATCH_DATA as B5


def merge_batches():
    merged = {}
    for batch in (B1, B2, B3, B4, B5):
        for lid, words_map in batch.items():
            merged[str(int(lid))] = words_map
    return merged


def enrich_lesson_file(path, lid_str, lesson_enrichment):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    words = data.get("words_to_learn", [])
    for w in words:
        word_key = w.get("word", "")
        info = lesson_enrichment.get(word_key)
        if not info:
            # Fallback case-insensitive match
            for k, v in lesson_enrichment.items():
                if k.strip().lower() == word_key.strip().lower():
                    info = v
                    break
        if not info:
            raise ValueError(f"Missing enrichment for Lesson {lid_str} word '{word_key}' in {path}")

        w["definition_vi"] = info["definition_vi"]
        w["collocations"] = info.get("collocations") or info["usage"].get("collocations", [])
        w["usage"] = info["usage"]
        w["extra_families"] = info["extra_families"]
        w["srs_sentence"] = info["srs_sentence"]
        w["needs_translation"] = False

        examples_vi = info.get("examples_vi", [])
        for idx, ex in enumerate(w.get("examples", [])):
            if idx < len(examples_vi) and examples_vi[idx]:
                ex["vi"] = examples_vi[idx]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return len(words)


def verify_lesson_file(path, lid):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    words = data.get("words_to_learn", [])
    if not words:
        raise AssertionError(f"Lesson {lid} has no words_to_learn in {path}")
    for w in words:
        word = w.get("word", "")
        assert w.get("definition_vi", "").strip(), f"L{lid:02d} '{word}': empty definition_vi"
        for idx, ex in enumerate(w.get("examples", [])):
            if ex.get("en", "").strip():
                assert ex.get("vi", "").strip(), f"L{lid:02d} '{word}' ex#{idx}: empty vi"
        usage = w.get("usage") or {}
        assert usage.get("structures"), f"L{lid:02d} '{word}': empty usage.structures"
        assert isinstance(usage.get("prepositions"), list), f"L{lid:02d} '{word}': usage.prepositions is not list"
        assert usage.get("collocations"), f"L{lid:02d} '{word}': empty usage.collocations"
        assert usage.get("tip", "").strip(), f"L{lid:02d} '{word}': empty usage.tip"
        extra = w.get("extra_families")
        assert isinstance(extra, list) and len(extra) > 0, f"L{lid:02d} '{word}': empty extra_families"
        for ef in extra:
            assert ef.get("pos") in ("verb", "noun", "adjective", "adverb"), f"L{lid:02d} '{word}': invalid pos {ef.get('pos')}"
            assert ef.get("word", "").strip(), f"L{lid:02d} '{word}': empty extra_family word"
            assert ef.get("example", "").strip(), f"L{lid:02d} '{word}': empty extra_family example"
        srs = w.get("srs_sentence") or {}
        assert "_____" in srs.get("en", ""), f"L{lid:02d} '{word}': srs_sentence.en missing _____"
        assert srs.get("answer", "").strip(), f"L{lid:02d} '{word}': empty srs_sentence.answer"
        assert srs.get("base_word", "").strip(), f"L{lid:02d} '{word}': empty srs_sentence.base_word"
        assert srs.get("pos_hint", "").strip(), f"L{lid:02d} '{word}': empty srs_sentence.pos_hint"
        assert srs.get("vi", "").strip(), f"L{lid:02d} '{word}': empty srs_sentence.vi"


def main():
    enrichment = merge_batches()
    assert len(enrichment) == 50, f"Expected 50 lessons in enrichment, got {len(enrichment)}"

    out_scripts = os.path.join(ROOT, "scripts", "data", "vocab_enrichment.json")
    out_public = os.path.join(ROOT, "public", "answers", "vocab_enrichment.json")
    os.makedirs(os.path.dirname(out_scripts), exist_ok=True)
    os.makedirs(os.path.dirname(out_public), exist_ok=True)

    with open(out_scripts, "w", encoding="utf-8") as f:
        json.dump(enrichment, f, ensure_ascii=False, indent=2)
    with open(out_public, "w", encoding="utf-8") as f:
        json.dump(enrichment, f, ensure_ascii=False, indent=2)

    total_words = 0
    for lid in range(1, 51):
        lid_str = str(lid)
        lesson_enrichment = enrichment[lid_str]
        p1 = os.path.join(ROOT, "lessons_json", f"lesson_{lid:02d}.json")
        p2 = os.path.join(ROOT, "public", "lessons_json", f"lesson_{lid:02d}.json")

        c1 = enrich_lesson_file(p1, lid_str, lesson_enrichment)
        c2 = enrich_lesson_file(p2, lid_str, lesson_enrichment)
        assert c1 == c2, f"Mismatch word count in L{lid:02d}: {c1} vs {c2}"
        verify_lesson_file(p1, lid)
        verify_lesson_file(p2, lid)
        total_words += c1

    print(f"SUCCESS: Enriched and verified all 50 lessons ({total_words} words total).")
    print(f"  - {out_scripts}")
    print(f"  - {out_public}")
    print(f"  - lessons_json/lesson_01..50.json")
    print(f"  - public/lessons_json/lesson_01..50.json")


if __name__ == "__main__":
    main()
