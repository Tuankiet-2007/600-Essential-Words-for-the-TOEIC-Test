/**
 * FROZEN CONTRACT — Spaced Repetition scheduling (SM-2 with 4-button grading).
 *
 * Grades (matching the 1-2-3-4 keyboard shortcuts in Tab 2 / Tab 3):
 *   1 = Again  (quên hoàn toàn)
 *   2 = Hard   (nhớ mang máng)
 *   3 = Good   (nhớ được)
 *   4 = Easy   (quá dễ)
 */
import { loadSrs, saveSrs, srsKey, normalizeSrsCard } from './storage.js';
export { loadSrs, saveSrs, srsKey };

export const GRADES = {
  1: { id: 1, label: 'Again', vi: 'Quên', quality: 1, color: 'rose' },
  2: { id: 2, label: 'Hard', vi: 'Khó', quality: 3, color: 'amber' },
  3: { id: 3, label: 'Good', vi: 'Được', quality: 4, color: 'emerald' },
  4: { id: 4, label: 'Easy', vi: 'Dễ', quality: 5, color: 'sky' },
};

const MIN_EASE = 1.3;

export const CUTOFF_HOUR = 4; // Mốc chuyển ngày theo chuẩn Anki: 04:00 AM

/**
 * Trả về chuỗi ngày YYYY-MM-DD theo mốc chuyển ngày 04:00 AM.
 * Nếu thời gian hiện tại từ 00:00 đến 03:59, ngày hiệu dụng sẽ thuộc về ngày hôm trước.
 * @param {Date|string} dateInput
 * @param {number} cutoffHour
 * @returns {string} định dạng YYYY-MM-DD
 */
export function getEffectiveDayString(dateInput = new Date(), cutoffHour = CUTOFF_HOUR) {
  const d = new Date(dateInput);
  if (Number.isNaN(d.getTime())) throw new Error('Ngày học không hợp lệ.');

  // Lùi lại số giờ tương ứng với cutoffHour
  d.setHours(d.getHours() - cutoffHour);

  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * Tính toán ngày đáo hạn mới đảm bảo neo vào mốc cutoff 04:00 AM.
 * @param {number} interval Số ngày giãn cách
 * @param {Date} now
 * @returns {string} ISO Date string
 */
export function calculateNextDueDate(interval, now = new Date()) {
  if (!Number.isFinite(interval) || interval < 0) throw new Error('Khoảng ôn không hợp lệ.');
  const target = new Date(now);
  getEffectiveDayString(target); // Validate before mutating.
  if (target.getHours() < CUTOFF_HOUR) target.setDate(target.getDate() - 1);
  target.setHours(CUTOFF_HOUR, 0, 0, 0);
  target.setDate(target.getDate() + Math.round(interval));
  return target.toISOString();
}

/** @returns {import('./storage.js').SrsCard} */
export function freshCard(now = new Date()) {
  return {
    ease: 2.5, interval: 0, reps: 0, due: new Date(now).toISOString(),
    lapses: 0, lastGrade: 0, state: 'new', learningStep: 0,
    version: 0, schedulerVersion: 'sm2-stages-v2',
  };
}

/**
 * SM-2 update. Pure function — same inputs always give the same card.
 * @param {import('./storage.js').SrsCard} card
 * @param {number} grade 1..4
 * @param {Date} [now]
 * @returns {import('./storage.js').SrsCard}
 */
export function review(card, grade, now = new Date()) {
  const at = new Date(now);
  getEffectiveDayString(at);
  if (!Number.isInteger(grade) || !GRADES[grade]) throw new Error('Điểm ôn phải từ 1 đến 4.');
  const c = card ? normalizeSrsCard(card) : freshCard(at);
  const state = c.state || (c.reps > 0 || c.interval > 0 ? 'review' : 'new');
  // Practice before the due time is intentionally schedule-neutral, including failures.
  if (state !== 'new' && !isDue(c, at)) return { ...c };
  const common = { ...c, lastGrade: grade, lastReviewedAt: at.toISOString(), schedulerVersion: 'sm2-stages-v2' };
  if (state === 'new' || state === 'learning' || state === 'relearning') {
    if (grade !== 4 && (grade !== 3 || (c.learningStep || 0) < 1)) {
      const minutes = grade === 1 ? 1 : 10;
      return { ...common, state: state === 'relearning' ? state : 'learning', learningStep: grade === 1 ? 0 : 1,
        due: new Date(at.getTime() + minutes * 60000).toISOString() };
    }
    const interval = state === 'relearning' ? Math.max(1, Math.round(c.interval * 0.5)) : grade === 4 ? 4 : 1;
    return { ...common, state: 'review', learningStep: 0, interval, reps: c.reps + 1,
      due: calculateNextDueDate(interval, at) };
  }
  let { ease, interval, reps, lapses } = c;
  if (grade === 1) {
    return { ...common, state: 'relearning', learningStep: 0, reps: 0, lapses: lapses + 1,
      ease: Math.max(MIN_EASE, ease - 0.2), due: new Date(at.getTime() + 60000).toISOString() };
  }
  reps += 1;
  if (grade === 2) {
    interval = Math.max(interval + 1, Math.round(interval * 1.2));
    ease = Math.max(MIN_EASE, ease - 0.15);
  } else {
    interval = reps === 1 ? 1 : reps === 2 ? 6 : Math.round(Math.max(1, interval) * ease);
    if (grade === 4) { interval = Math.round(interval * 1.3); ease += 0.1; }
  }
  interval = Math.max(1, Math.min(interval, 365));
  return { ...common, state: 'review', learningStep: 0, ease: Number(ease.toFixed(3)), interval, reps, lapses,
    due: calculateNextDueDate(interval, at) };
}

/**
 * True when a card is due for review right now based on 04:00 AM cutoff.
 * Thẻ đến hạn khi ngày đáo hạn hiệu dụng <= ngày hôm nay hiệu dụng.
 */
export function isDue(card, now = new Date()) {
  if (!card || !card.due) return true;
  if (card.state === 'learning' || card.state === 'relearning') {
    const due = new Date(card.due).getTime();
    const current = new Date(now).getTime();
    if (!Number.isFinite(due) || !Number.isFinite(current)) throw new Error('Ngày ôn không hợp lệ.');
    return due <= current;
  }
  const todayDayKey = getEffectiveDayString(now, CUTOFF_HOUR);
  const cardDueDayKey = getEffectiveDayString(new Date(card.due), CUTOFF_HOUR);
  return cardDueDayKey <= todayDayKey;
}

/**
 * Persist one review result.
 * @param {number} lessonId
 * @param {string} word
 * @param {number} grade
 */
export function recordReview(lessonId, word, grade, extra = {}) {
  const all = loadSrs();
  const key = srsKey(lessonId, word);
  const previous = all[key];
  const { reviewId, expectedVersion, ...metadata } = extra;
  if (reviewId !== undefined && (typeof reviewId !== 'string' || !reviewId.trim())) throw new Error('Review ID không hợp lệ.');
  if (reviewId && previous?.processedReviewIds?.includes(reviewId)) return previous;
  const version = previous?.version || 0;
  if (expectedVersion !== undefined && expectedVersion !== version) {
    const error = new Error('Thẻ đã thay đổi. Vui lòng tải lại trạng thái ôn.');
    error.code = 'SRS_VERSION_CONFLICT';
    throw error;
  }
  const now = new Date();
  const next = review(previous, grade, now);
  const id = reviewId || `review:${now.getTime()}:${Math.random().toString(36).slice(2)}`;
  const practice = previous && !isDue(previous, now);
  const log = { id, at: now.toISOString(), grade, source: metadata.source || 'review', practice: Boolean(practice),
    before: previous ? { state: previous.state || 'review', interval: previous.interval, reps: previous.reps, due: previous.due } : null,
    after: { state: next.state, interval: next.interval, reps: next.reps, due: next.due }, schedulerVersion: 'sm2-stages-v2' };
  // Metadata cannot override scheduling or the durable transaction fields.
  const safeMetadata = Object.fromEntries(Object.entries(metadata).filter(([field]) => ![
    'ease', 'interval', 'reps', 'due', 'lapses', 'lastGrade', 'state', 'learningStep',
    'lastReviewedAt', 'schedulerVersion', 'version', 'processedReviewIds', 'reviewLog',
  ].includes(field)));
  all[key] = { ...previous, ...next, ...safeMetadata, word, lessonId, version: version + 1,
    processedReviewIds: [...(previous?.processedReviewIds || []), id],
    reviewLog: [...(previous?.reviewLog || []), log].slice(-100) };
  const saved = saveSrs(all);
  return saved[key];
}

/** All stored cards for one lesson. */
export function cardsForLesson(lessonId) {
  const all = loadSrs();
  const prefix = `L${String(lessonId).padStart(2, '0')}:`;
  return Object.entries(all)
    .filter(([k]) => k.startsWith(prefix))
    .map(([k, v]) => ({ key: k, ...v }));
}

/** Build a study queue for a lesson, due-first then unseen. */
export function buildQueue(lessonId, words, now = new Date()) {
  const all = loadSrs();
  const due = [];
  const fresh = [];
  const later = [];
  for (const w of words || []) {
    const card = all[srsKey(lessonId, w.word)];
    if (!card) fresh.push({ word: w, card: null });
    else if (isDue(card, now)) due.push({ word: w, card });
    else later.push({ word: w, card });
  }
  return [...due, ...fresh, ...later];
}

export default { GRADES, review, isDue, recordReview, cardsForLesson, buildQueue, freshCard };
