/**
 * FROZEN CONTRACT — Spaced Repetition scheduling (SM-2 with 4-button grading).
 *
 * Grades (matching the 1-2-3-4 keyboard shortcuts in Tab 2 / Tab 3):
 *   1 = Again  (quên hoàn toàn)
 *   2 = Hard   (nhớ mang máng)
 *   3 = Good   (nhớ được)
 *   4 = Easy   (quá dễ)
 */
import { loadSrs, saveSrs, srsKey } from './storage.js';

export const GRADES = {
  1: { id: 1, label: 'Again', vi: 'Quên', quality: 1, color: 'rose' },
  2: { id: 2, label: 'Hard', vi: 'Khó', quality: 3, color: 'amber' },
  3: { id: 3, label: 'Good', vi: 'Được', quality: 4, color: 'emerald' },
  4: { id: 4, label: 'Easy', vi: 'Dễ', quality: 5, color: 'sky' },
};

const DAY_MS = 24 * 60 * 60 * 1000;
const MIN_EASE = 1.3;

/** @returns {import('./storage.js').SrsCard} */
export function freshCard() {
  return { ease: 2.5, interval: 0, reps: 0, due: new Date().toISOString(), lapses: 0, lastGrade: 0 };
}

/**
 * SM-2 update. Pure function — same inputs always give the same card.
 * @param {import('./storage.js').SrsCard} card
 * @param {number} grade 1..4
 * @param {Date} [now]
 * @returns {import('./storage.js').SrsCard}
 */
export function review(card, grade, now = new Date()) {
  const c = { ...freshCard(), ...(card || {}) };
  const g = GRADES[grade] || GRADES[3];
  const q = g.quality;

  let { ease, interval, reps, lapses } = c;

  if (q < 3) {
    // Failed recall: reset repetitions, relearn tomorrow.
    reps = 0;
    lapses += 1;
    interval = 1;
    ease = Math.max(MIN_EASE, ease - 0.2);
  } else {
    reps += 1;
    if (reps === 1) interval = 1;
    else if (reps === 2) interval = 6;
    else interval = Math.round(interval * ease);
    // Easiness adjustment per SM-2 formula.
    ease = ease + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02));
    ease = Math.max(MIN_EASE, ease);
    if (grade === 4) interval = Math.round(interval * 1.3); // Easy bonus
    if (grade === 2) interval = Math.max(1, Math.round(interval * 0.6)); // Hard penalty
  }

  interval = Math.max(1, Math.min(interval, 365));
  const due = new Date(now.getTime() + interval * DAY_MS);

  return { ease: Number(ease.toFixed(3)), interval, reps, due: due.toISOString(), lapses, lastGrade: grade };
}

/** True when a card is due for review right now. */
export function isDue(card, now = new Date()) {
  if (!card) return true;
  return new Date(card.due).getTime() <= now.getTime();
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
  const next = review(all[key], grade);
  all[key] = { ...next, word, lessonId, ...extra };
  saveSrs(all);
  return all[key];
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
