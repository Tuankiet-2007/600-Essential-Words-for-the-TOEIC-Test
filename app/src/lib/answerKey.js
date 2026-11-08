/**
 * Answer key + per-question explanations (book-sourced).
 *
 * VI SAO CO MODULE RIENG
 * ----------------------
 * Dap an cua sach KHONG nam trong lesson_NN.json — chung duoc in o phan
 * "Answer Key" o cuoi sach. Script scripts/parse_answer_key.py doc 4 trang
 * Answer Key do va sinh ra scripts/data/answer_key.json; script
 * scripts/build_explanations.py sinh scripts/data/explanations.json.
 *
 * Hai file do duoc copy vao public/answers/ khi build/publish, nen trinh duyet
 * chi can fetch MOT lan cho ca 50 bai (khong phai fetch 50 lan).
 *
 * TAT CA du lieu o day deu co nguon that:
 *   - answer_key.json   : chep tu Answer Key sach in.
 *   - explanations.json : sinh tu du lieu cua chinh bai hoc (dinh nghia sach in,
 *                         bang ho tu, vi tri cho trong, bai doc, tapescript).
 *                         Cho nao khong du bang chung thi ghi ro la "can nghe
 *                         audio", KHONG bia ly do.
 *
 * API:
 *   await loadAnswers()              -> { "1": {...}, ... }
 *   await loadExplanations()         -> { "1": {"10": {...}, ...}, ... }
 *   answerFor(answers, lessonId, n)  -> "A" | null
 *   explanationFor(exps, lessonId, n)
 */

const BASE = import.meta.env.BASE_URL || './';
const cleanBase = BASE.endsWith('/') ? BASE : BASE + '/';

const ANSWERS_URL = `${cleanBase}answers/answer_key.json`;
const EXPLANATIONS_URL = `${cleanBase}answers/explanations.json`;
const TAPESCRIPTS_FULL_URL = `${cleanBase}answers/tapescripts_full.json`;
const TAPESCRIPTS_URL = `${cleanBase}answers/tapescripts.json`;
const VOCAB_ENRICHMENT_URL = `${cleanBase}answers/vocab_enrichment.json`;

let answersPromise = null;
let explanationsPromise = null;
let tapescriptsPromise = null;
let vocabEnrichmentPromise = null;

/** Fetch + cache a JSON file; resolves to {} when absent (never throws). */
async function fetchJsonOnce(url) {
  try {
    const res = await fetch(url, { cache: 'no-cache' });
    if (!res.ok) return {};
    const ctype = res.headers.get('content-type') || '';
    /*
     * SPA fallback: Vite tra index.html voi HTTP 200 cho file khong ton tai.
     * Doc nham HTML se nem loi JSON.parse -> phai chan truoc.
     */
    if (ctype.includes('text/html')) return {};
    const raw = await res.text();
    if (raw.trimStart().startsWith('<')) return {};
    const data = JSON.parse(raw);
    return data && typeof data === 'object' ? data : {};
  } catch {
    return {};
  }
}

export function loadAnswers() {
  if (!answersPromise) answersPromise = fetchJsonOnce(ANSWERS_URL);
  return answersPromise;
}

export function loadExplanations() {
  if (!explanationsPromise) explanationsPromise = fetchJsonOnce(EXPLANATIONS_URL);
  return explanationsPromise;
}

/** Chuuan hoa 1 chu cai dap an; tra null khi khong co. */
export function normalizeKeyLetter(raw) {
  const s = String(raw ?? '').trim().toUpperCase();
  const m = s.match(/[A-D]/);
  return m ? m[0] : null;
}

/**
 * Dap an cua cau `num` trong bai `lessonId`, hoac null neu Answer Key khong co.
 * Tra null chu KHONG tra chuoi rong, de noi goi phan biet "chua co dap an" voi
 * "dap an la chuoi rong".
 */
export function answerFor(answers, lessonId, num) {
  if (!answers || num === null || num === undefined) return null;
  const bucket = answers[String(Number(lessonId))];
  if (!bucket) return null;
  const wp = bucket.word_practice;
  if (!wp) return null;
  return normalizeKeyLetter(wp[String(Number(num))]);
}

/** Giai thich cua cau `num`, hoac null. */
export function explanationFor(explanations, lessonId, num) {
  if (!explanations || num === null || num === undefined) return null;
  const bucket = explanations[String(Number(lessonId))];
  if (!bucket) return null;
  return bucket[String(Number(num))] || null;
}

export function loadTapescripts() {
  if (!tapescriptsPromise) {
    tapescriptsPromise = (async () => {
      const full = await fetchJsonOnce(TAPESCRIPTS_FULL_URL);
      if (full && Object.keys(full).length > 0) return full;
      return fetchJsonOnce(TAPESCRIPTS_URL);
    })();
  }
  return tapescriptsPromise;
}

export function tapescriptFor(tapescripts, lessonId) {
  if (!tapescripts || lessonId === null || lessonId === undefined) return null;
  const bucket = tapescripts[String(Number(lessonId))];
  if (!bucket || typeof bucket !== 'object') return null;
  const p1 = String(bucket.part1 || '').trim();
  const p2 = String(bucket.part2 || '').trim();
  const p3 = String(bucket.part3 || '').trim();
  const p4 = String(bucket.part4 || '').trim();
  const sections = [];
  if (p1) sections.push(`=== Part 1: Photo ===\n${p1}`);
  if (p2) sections.push(`=== Part 2: Question-Response ===\n${p2}`);
  if (p3) sections.push(`=== Part 3: Conversation (Câu 4–6) ===\n${p3}`);
  if (p4) sections.push(`=== Part 4: Talk (Câu 7–9) ===\n${p4}`);
  const fullText = sections.join('\n\n');
  if (!fullText) return null;
  return {
    lesson_id: Number(lessonId),
    part1: p1,
    part2: p2,
    part3: p3,
    part4: p4,
    fullText,
  };
}

export function loadVocabEnrichment() {
  if (!vocabEnrichmentPromise) {
    vocabEnrichmentPromise = fetchJsonOnce(VOCAB_ENRICHMENT_URL);
  }
  return vocabEnrichmentPromise;
}

export function enrichmentFor(enrichmentMap, lessonId, word) {
  if (!enrichmentMap || !word) return null;
  const key = String(word).trim().toLowerCase();
  const byLesson = enrichmentMap[String(Number(lessonId))];
  if (byLesson && byLesson[key]) return byLesson[key];
  if (enrichmentMap.words && enrichmentMap.words[key]) return enrichmentMap.words[key];
  return enrichmentMap[key] || null;
}
