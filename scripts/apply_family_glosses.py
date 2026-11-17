"""Apply curated short Vietnamese family meanings without changing source sentences.
Run from repository root: python scripts/apply_family_glosses.py
The four curated JSON files are the maintained source; no network translation.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = ['family_gloss_01_13.json', 'family_gloss_14_26.json', 'family_gloss_27_38.json', 'family_gloss_39_50.json']

def load_glosses():
    result = {}
    for name in SOURCE_FILES:
        values = json.loads((ROOT / 'scripts/data' / name).read_text(encoding='utf-8'))
        for key, value in values.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f'Invalid meaning: {key}')
            if key in result and result[key] != value:
                raise ValueError(f'Conflicting meaning: {key}')
            result[key] = value.strip()
    return result

def enrich_node(node, lid, glosses):
    count = 0
    if isinstance(node, list):
        return sum(enrich_node(row, lid, glosses) for row in node)
    if not isinstance(node, dict):
        return 0
    if node.get('word'):
        key = f"{lid}|{node.get('pos', '')}|{node['word']}"
        if key not in glosses:
            fallback = f"{lid}||{node['word']}"
            if fallback not in glosses:
                raise ValueError(f'Missing family meaning: {key}')
            key = fallback
        node['meaning_vi'] = glosses[key]
        node['meaning_vi_source'] = 'curated-vietnamese'
        count += 1
    for key in ('value', 'members', 'words', 'forms', 'rows'):
        if isinstance(node.get(key), list):
            count += enrich_node(node[key], lid, glosses)
    return count

def enrich_lesson(data, lid, glosses):
    count = enrich_node(data.get('word_families', []), lid, glosses)
    for word in data.get('words_to_learn', []):
        count += enrich_node(word.get('extra_families', []), lid, glosses)
        if word.get('word_family'):
            count += enrich_node(word['word_family'], lid, glosses)
    return count

def main():
    glosses = load_glosses()
    planned = []
    for folder in ('lessons_json', 'public/lessons_json'):
        for path in sorted((ROOT / folder).glob('lesson_*.json')):
            data = json.loads(path.read_text(encoding='utf-8'))
            count = enrich_lesson(data, data['lesson_id'], glosses)
            planned.append((path, data, count))
    # Sample fallback uses the same maintained lesson-1 dictionary.
    for folder in ('sample_lessons', 'public/sample_lessons'):
        for path in sorted((ROOT / folder).glob('lesson_*.json')):
            data = json.loads(path.read_text(encoding='utf-8'))
            count = enrich_lesson(data, data['lesson_id'], glosses)
            planned.append((path, data, count))
    # Validate the entire corpus before modifying any files.
    for path, data, _ in planned:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Applied {len(glosses)} curated meanings to {len(planned)} lesson files; {sum(c for _, _, c in planned)} family rows.')

if __name__ == '__main__':
    main()
