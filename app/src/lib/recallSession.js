/* Pure Active Recall session helpers. No storage, React, or clock side effects. */

const clean = (value) => String(value ?? '').trim();
const keyOf = (record) => `${record?.lessonId ?? ''}:${clean(record?.entry?.word).toLowerCase()}`;

function cloze(sentence, answer) {
  const text = clean(sentence);
  const word = clean(answer);
  if (!text || !word) return '';
  if (/_{3,}/.test(text)) return text.replace(/_{3,}/g, '______');
  const escaped = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return text.replace(new RegExp(`\\b${escaped}\\b`, 'i'), '______');
}

function candidateFor(record) {
  const entry = record?.entry || {};
  const base = clean(entry.word);
  const out = [];
  const add = (sourceKind, source, answer, vi = '', pos = '') => {
    const ans = clean(answer);
    const raw = clean(source);
    const promptEn = cloze(raw, ans);
    if (!raw || !ans || !promptEn || (!/_{3,}/.test(raw) && promptEn === raw)) return;
    out.push({ sourceKind, sourceId: `${record.lessonId}:${base}:${sourceKind}:${out.length}`, sourceLessonId: record.lessonId, source: raw, promptEn, fullEn: raw.replace(/_{3,}/g, ans), answer: ans, accepted: [ans], hintVi: vi || '', posHint: pos || entry.pos || '' });
  };
  if (entry.srs_sentence?.en && entry.srs_sentence?.answer) add('srs_sentence', entry.srs_sentence.en, entry.srs_sentence.answer, entry.srs_sentence.vi, entry.srs_sentence.pos_hint);
  for (const ex of Array.isArray(entry.examples) ? entry.examples : []) {
    if (ex?.en && base && new RegExp(`\\b${base.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i').test(ex.en)) add('example', ex.en, base, ex.vi, entry.pos);
  }
  for (const fam of Array.isArray(entry.extra_families) ? entry.extra_families : []) {
    if (fam?.example && fam?.word) add('word_family', fam.example, fam.word, fam.vi, fam.pos);
  }
  return out;
}

export function buildQuizSession(wordRecords = [], { sessionId = 'session', random = Math.random } = {}) {
  const questions = [];
  const words = [];
  const missing = [];
  const seen = new Set();
  for (const record of wordRecords) {
    const word = clean(record?.entry?.word);
    if (!word) continue;
    const wordKey = keyOf(record);
    if (seen.has(wordKey)) continue;
    seen.add(wordKey);
    const entry = record.entry;
    const definition = clean(entry.definition_en);
    if (!definition) missing.push({ wordKey, reason: 'missing_definition_en' });
    const candidates = candidateFor(record);
    if (!candidates.length) missing.push({ wordKey, reason: 'missing_context_candidate' });
    if (!definition || !candidates.length) continue;
    const accepted = [word];
    if (word.toLowerCase() === 'canceled') accepted.push('cancelled');
    if (word.toLowerCase() === 'cancelled') accepted.push('canceled');
    questions.push({ uid: `base:${wordKey}:${sessionId}`, wordKey, type: 'base_word', ...record, promptEn: cloze(definition, word), hintVi: '', pos: entry.pos || '', answer: word, accepted });
    const picked = candidates[Math.floor(random() * candidates.length)];
    questions.push({ uid: `context:${wordKey}:${sessionId}`, wordKey, type: 'context_word', ...record, ...picked, pos: picked.posHint || entry.pos || '', sourceKind: picked.sourceKind });
    words.push(wordKey);
  }
  for (let i = questions.length - 1; i > 0; i -= 1) { const j = Math.floor(random() * (i + 1)); [questions[i], questions[j]] = [questions[j], questions[i]]; }
  return { sessionId, questions, words, missing, complete: missing.length === 0 };
}

export function aggregateQuestionResults(results = []) {
  const byWord = new Map();
  const seenUids = new Set();
  for (const result of results) {
    if (!result?.uid || !result.wordKey || seenUids.has(result.uid)) continue;
    seenUids.add(result.uid);
    const key = result.wordKey;
    if (!byWord.has(key)) byWord.set(key, []);
    byWord.get(key).push(result);
  }
  return [...byWord].map(([wordKey, items]) => ({ wordKey, items, complete: items.length === 2 && items.some((x) => x.type === 'base_word') && items.some((x) => x.type === 'context_word'), grade: items.some((x) => !x.isCorrect) ? 1 : 3 }));
}
