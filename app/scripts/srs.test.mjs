import test from 'node:test';
import assert from 'node:assert/strict';
import { calculateNextDueDate, getEffectiveDayString, isDue, recordReview, review } from '../src/lib/srs.js';
import { loadSrs, saveSrs, importAllData } from '../src/lib/storage.js';
import { buildQuizSession, aggregateQuestionResults } from '../src/lib/recallSession.js';
import { readFileSync } from 'node:fs';

process.env.TZ = 'Asia/Ho_Chi_Minh';
function memoryStorage() {
  const values = new Map();
  globalThis.localStorage = {
    getItem: (key) => values.get(key) ?? null,
    setItem: (key, value) => values.set(key, String(value)),
    removeItem: (key) => values.delete(key),
  };
  return values;
}

test('15 words produce exactly 30 unique base/context questions', () => {
  const records = Array.from({ length: 15 }, (_, i) => ({ lessonId: 1, entry: { word: `word${i}`, definition_en: `Definition ${i}`, srs_sentence: { en: 'Please use ______ here.', answer: `word${i}` } } }));
  const built = buildQuizSession(records, { sessionId: 'fifteen', random: () => 0.5 });
  assert.equal(built.complete, true);
  assert.equal(built.questions.length, 30);
  assert.equal(new Set(built.questions.map((q) => q.uid)).size, 30);
  for (const key of built.words) assert.deepEqual(built.questions.filter((q) => q.wordKey === key).map((q) => q.type).sort(), ['base_word', 'context_word']);
});

test('missing context is reported rather than a complete one-question session', () => {
  const built = buildQuizSession([{ lessonId: 1, entry: { word: 'demo', definition_en: 'a demonstration' } }]);
  assert.equal(built.complete, false);
  assert.ok(built.missing.some((item) => item.reason === 'missing_context_candidate'));
});

test('duplicate result UID does not complete a pair prematurely', () => {
  const base = { uid: 'b', wordKey: '1:demo', type: 'base_word', isCorrect: true };
  const first = aggregateQuestionResults([base, base]);
  assert.equal(first[0].complete, false);
  assert.equal(first[0].items.length, 1);
  const paired = aggregateQuestionResults([base, { uid: 'c', wordKey: '1:demo', type: 'context_word', isCorrect: false }]);
  assert.equal(paired[0].complete, true);
  assert.equal(paired[0].grade, 1);
});

test('corpus coverage explicitly reports missing definitions without incomplete pairs', () => {
  const records = [];
  for (let i = 1; i <= 50; i += 1) {
    const lesson = JSON.parse(readFileSync(new URL(`../../public/lessons_json/lesson_${String(i).padStart(2, '0')}.json`, import.meta.url), 'utf8'));
    for (const entry of lesson.words_to_learn) records.push({ lessonId: i, lessonObj: lesson, entry });
  }
  const built = buildQuizSession(records, { sessionId: 'corpus', random: () => 0.5 });
  assert.deepEqual(built.missing, [{ wordKey: '31:secure', reason: 'missing_definition_en' }]);
  assert.equal(built.complete, false);
  assert.equal(built.questions.length, (records.length - 1) * 2);
  assert.equal(built.words.length, records.length - 1);
});

test('one study day from before 04:00 ends at the next study boundary', () => {
  const now = new Date('2026-11-16T01:00:00+07:00');
  assert.equal(getEffectiveDayString(now), '2026-11-15');
  assert.equal(calculateNextDueDate(1, now), new Date('2026-11-16T04:00:00+07:00').toISOString());
});

test('day review becomes due at the 04:00 boundary', () => {
  const card = { due: '2026-11-16T04:00:00+07:00' };
  assert.equal(isDue(card, new Date('2026-11-16T03:59:00+07:00')), false);
  assert.equal(isDue(card, new Date('2026-11-16T04:00:00+07:00')), true);
});

test('same review ID cannot advance a card twice', () => {
  memoryStorage();
  recordReview(1, 'demo', 3, { reviewId: 'pair:test:demo' });
  const before = JSON.stringify(loadSrs());
  recordReview(1, 'demo', 3, { reviewId: 'pair:test:demo' });
  assert.equal(JSON.stringify(loadSrs()), before);
});

test('malformed backup is rejected before it replaces saved SRS', () => {
  memoryStorage();
  recordReview(1, 'demo', 3, { reviewId: 'valid' });
  const before = JSON.stringify(loadSrs());
  assert.throws(() => importAllData({ data: { srs: { 'L01:demo': { ease: 'bad', interval: 'bad', reps: 'bad', due: 'invalid' } } } }));
  assert.equal(JSON.stringify(loadSrs()), before);
});

test('learning steps use timestamps and early practice cannot graduate a card', () => {
  const now = new Date('2026-11-16T12:00:00+07:00');
  const first = review(null, 3, now);
  assert.equal(first.state, 'learning');
  assert.equal(isDue(first, new Date(now.getTime() + 9 * 60000)), false);
  assert.deepEqual(review(first, 3, new Date(now.getTime() + 60000)), first);
  const graduated = review(first, 3, new Date(now.getTime() + 10 * 60000));
  assert.equal(graduated.state, 'review');
  assert.equal(graduated.interval, 1);
  assert.equal(graduated.reps, 1);
});

test('review failure enters relearning and hard does not shrink interval', () => {
  const now = new Date('2026-11-16T12:00:00+07:00');
  const card = { ease: 1.3, interval: 10, reps: 5, lapses: 0, lastGrade: 3, due: '2026-11-15T04:00:00+07:00', state: 'review' };
  const failed = review(card, 1, now);
  assert.equal(failed.state, 'relearning');
  assert.equal(failed.lapses, 1);
  assert.equal(isDue(failed, now), false);
  assert.ok(review(card, 2, now).interval > card.interval);
});

test('stale expected version cannot overwrite a newer review', () => {
  memoryStorage();
  recordReview(1, 'demo', 3, { reviewId: 'v1', expectedVersion: 0 });
  assert.throws(() => recordReview(1, 'demo', 3, { reviewId: 'v2', expectedVersion: 0 }), { code: 'SRS_VERSION_CONFLICT' });
});

test('corrupted JSON is preserved and blocks overwriting SRS', () => {
  const values = memoryStorage();
  values.set('toeic600.srs', '{broken');
  assert.throws(loadSrs);
  assert.throws(() => recordReview(1, 'demo', 3));
  assert.equal(values.get('toeic600.srs'), '{broken');
});

test('legacy numeric strings normalize without concatenating repetitions', () => {
  memoryStorage();
  saveSrs({ 'L01:demo': { ease: '2.5', interval: '6', reps: '2', lapses: '0', lastGrade: '3', due: '2026-11-15T04:00:00+07:00' } });
  const card = loadSrs()['L01:demo'];
  assert.equal(card.reps, 2);
  assert.equal(review(card, 3, new Date('2026-11-16T12:00:00+07:00')).reps, 3);
});

test('review metadata cannot override the schedule or erase processed IDs', () => {
  memoryStorage();
  const first = recordReview(1, 'demo', 3, { reviewId: 'meta1', source: 'flashcard', errors: 1 });
  const second = recordReview(1, 'demo', 3, { reviewId: 'meta2', source: 'active-recall', errors: 2, interval: 999, due: 'bad', processedReviewIds: [] });
  assert.equal(second.source, 'active-recall');
  assert.equal(second.errors, 2);
  assert.equal(second.interval, first.interval);
  assert.equal(second.due, first.due);
  assert.deepEqual(second.processedReviewIds, ['meta1', 'meta2']);
});

test('quota errors do not report a successful review', () => {
  memoryStorage();
  globalThis.localStorage.setItem = () => { throw new Error('quota exceeded'); };
  assert.throws(() => recordReview(1, 'demo', 3, { reviewId: 'quota' }));
  assert.deepEqual(loadSrs(), {});
});
