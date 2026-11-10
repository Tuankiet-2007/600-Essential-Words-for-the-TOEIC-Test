/**
 * TAB 2 — Cloze-Context Flashcards ("Flashcard Ngữ Cảnh").
 *
 * CORE PRODUCT PRINCIPLE — CONTEXT-FIRST:
 * The FRONT blanks the target word out of a real in-book sentence, so the
 * learner must infer the word from context. The BACK restores the full
 * sentence with the target bolded plus its Vietnamese translation, and adds
 * the Vietnamese meaning, USE box (structures, prepositions, collocations, tip),
 * and the full word-family table (book + extended POS forms).
 *
 * Keys: Space flips · 1/2/3/4 grade recall and advance.
 *
 * Owned by: vocab-dev. Imports only the frozen shared APIs.
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { ArrowRight, BookOpen, CheckCircle2, Eye, Layers, RotateCcw, Shuffle, Sparkles, Volume2 } from 'lucide-react';
import { Badge, Button, Card, EmptyState, Highlighted, ProgressBar, SectionTitle, useSpeech, useToast } from '../components/ui.jsx';
import { makeCloze } from '../lib/assets.js';
import { familiesForEntry } from '../lib/lessonLoader.js';
import { GRADES, recordReview } from '../lib/srs.js';
import { markWordLearned } from '../lib/storage.js';
import { useApp } from '../lib/store.jsx';
import { WORD_FAMILY_LABEL, WORD_FAMILY_ORDER } from '../lib/types.js';

/* ---------------- local helpers (tab-private) ---------------- */

function lessonWords(lesson) {
  return (lesson?.words_to_learn || []).map((w) => w?.word).filter(Boolean);
}

function familiesFor(entry, lesson) {
  return familiesForEntry(entry, lesson);
}

function combinedFamiliesFor(entry, lesson) {
  const bookRows = familiesFor(entry, lesson);
  const extraRows = Array.isArray(entry?.extra_families) ? entry.extra_families : [];
  const seenKey = new Set(
    bookRows.map((r) => `${String(r.pos || '').toLowerCase().trim()}|${String(r.word || '').toLowerCase().trim()}`),
  );
  const seenWord = new Set(bookRows.map((r) => String(r.word || '').toLowerCase().trim()));
  const merged = [...bookRows];

  for (const r of extraRows) {
    if (!r || !r.word) continue;
    const wLower = String(r.word).toLowerCase().trim();
    const pLower = String(r.pos || '').toLowerCase().trim();
    const key = `${pLower}|${wLower}`;
    if (seenKey.has(key) || seenWord.has(wLower)) continue;
    seenKey.add(key);
    seenWord.add(wLower);
    merged.push({
      ...r,
      pos_source: r.pos_source || 'extended',
    });
  }
  return merged;
}

/** Buckets in WORD_FAMILY_ORDER; empty bucket -> em dash in the UI. */
function familyBuckets(rows) {
  const byPos = {};
  for (const r of rows || []) {
    const pos = String(r.pos || '').toLowerCase().trim();
    const key = WORD_FAMILY_ORDER.includes(pos)
      ? pos
      : pos.startsWith('adj')
        ? 'adjective'
        : pos.startsWith('adv')
          ? 'adverb'
          : pos.startsWith('n')
            ? 'noun'
            : pos.startsWith('v')
              ? 'verb'
              : null;
    if (!key) continue;
    (byPos[key] = byPos[key] || []).push(r);
  }
  return WORD_FAMILY_ORDER.map((pos) => ({ pos, rows: byPos[pos] || [] }));
}

/** Fisher–Yates copy. */
function shuffled(arr) {
  const out = [...arr];
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

/* ---------------- sub-components ---------------- */

function UsageBox({ usage, collocations }) {
  const structures = Array.isArray(usage?.structures) ? usage.structures : [];
  const preps = Array.isArray(usage?.prepositions) ? usage.prepositions : [];
  const cols = Array.isArray(usage?.collocations) && usage.collocations.length
    ? usage.collocations
    : Array.isArray(collocations)
      ? collocations
      : [];
  const tip = usage?.tip || '';

  if (!structures.length && !preps.length && !cols.length && !tip) return null;

  return (
    <div className="rounded-2xl border-2 border-[#bde3ff] bg-[#f3faff] p-3">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <span className="inline-flex items-center gap-1.5 text-[11px] font-extrabold uppercase tracking-wide text-[#0b6ea8]">
          <span className="rounded-md bg-[#0b6ea8] px-1.5 py-0.5 text-[10px] text-white">USE</span>
          Cách dùng &amp; Cụm từ đi kèm
        </span>
        {preps.length ? (
          <div className="flex flex-wrap items-center gap-1">
            <span className="text-[10.5px] font-bold text-[var(--color-duo-gray)]">Giới từ:</span>
            {preps.map((p, i) => (
              <span
                key={i}
                className="inline-flex items-center rounded-md border border-[#7cc4fa] bg-white px-1.5 py-0.5 font-mono text-[11px] font-extrabold text-[#0b6ea8]"
              >
                {p}
              </span>
            ))}
          </div>
        ) : null}
      </div>

      {structures.length ? (
        <div className="mt-2">
          <p className="mb-1 text-[10.5px] font-extrabold uppercase tracking-wide text-[var(--color-duo-gray)]">
            Cấu trúc sử dụng
          </p>
          <div className="flex flex-wrap gap-1.5">
            {structures.map((s, i) => (
              <span
                key={i}
                className="inline-flex items-center rounded-lg border border-[#cbe7ff] bg-white px-2 py-1 font-mono text-[11.5px] font-bold text-[var(--color-duo-ink)]"
              >
                {s}
              </span>
            ))}
          </div>
        </div>
      ) : null}

      {cols.length ? (
        <div className="mt-2">
          <p className="mb-1 text-[10.5px] font-extrabold uppercase tracking-wide text-[var(--color-duo-gray)]">
            Cụm từ thường gặp
          </p>
          <div className="flex flex-wrap gap-1.5">
            {cols.map((c, i) => (
              <span
                key={i}
                className="inline-flex items-center rounded-lg bg-[var(--color-duo-blue-light)] px-2 py-1 font-mono text-[11.5px] font-semibold text-[#0b6ea8]"
              >
                {c}
              </span>
            ))}
          </div>
        </div>
      ) : null}

      {tip ? (
        <p className="mt-2 rounded-lg bg-white/80 px-2.5 py-1.5 text-[12px] font-medium leading-relaxed text-[var(--color-duo-ink)] ring-1 ring-[#cbe7ff]">
          <span className="font-extrabold text-[#0b6ea8]">Mẹo TOEIC: </span>
          {tip}
        </p>
      ) : null}
    </div>
  );
}

/** Verb/Noun/Adj/Adv table; em dash when the form has no data. */
function WordFamilyTable({ rows, words, className = '' }) {
  const buckets = useMemo(() => familyBuckets(rows), [rows]);
  return (
    <div className={className}>
      <p className="mb-1 text-[11px] font-extrabold uppercase tracking-wide text-[var(--color-duo-muted)]">
        Họ từ (word family)
      </p>
      <div className="overflow-hidden rounded-2xl border-2 border-[var(--color-duo-line)]">
        <div className="grid grid-cols-1 divide-y divide-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] sm:grid-cols-4 sm:divide-x sm:divide-y-0">
          {WORD_FAMILY_ORDER.map((pos) => (
            <div
              key={pos}
              className="px-2 py-1 text-[10.5px] font-extrabold uppercase tracking-wide text-[var(--color-duo-gray)]"
            >
              {WORD_FAMILY_LABEL[pos]}
            </div>
          ))}
        </div>
        <div className="grid grid-cols-1 divide-y divide-[var(--color-duo-line)] bg-white sm:grid-cols-4 sm:divide-x sm:divide-y-0">
          {buckets.map(({ pos, rows: cellRows }) => (
            <div key={pos} className="min-w-0 px-2 py-1.5">
              {cellRows.length ? (
                <ul className="space-y-1.5">
                  {cellRows.map((r, i) => (
                    <li key={i}>
                      <p className="break-words text-[12.5px] font-extrabold text-[var(--color-duo-green-dark)]">
                        {r.word}
                        {r.pos_source === 'derived' ? (
                          <span className="ml-1 align-middle text-[9px] font-bold uppercase text-[var(--color-duo-orange)]">
                            suy ra
                          </span>
                        ) : r.pos_source === 'extended' ? (
                          <span className="ml-1 rounded bg-sky-100 px-1 py-0.5 align-middle text-[8.5px] font-bold uppercase text-sky-700">
                            mở rộng
                          </span>
                        ) : null}
                      </p>
                      {r.example ? (
                        <p className="mt-0.5 text-[11.5px] leading-relaxed text-[var(--color-duo-gray)]">
                          <Highlighted text={r.example} words={words} />
                        </p>
                      ) : (
                        <p className="mt-0.5 text-[11.5px] italic text-[var(--color-duo-muted)]">
                          Chưa có ví dụ trong sách.
                        </p>
                      )}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="select-none text-[14px] font-medium text-[var(--color-duo-muted)]" aria-label="Không có dữ liệu">
                  —
                </p>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ---------------- main tab ---------------- */

export default function Tab2Flashcards({ lesson }) {
  const { lessonId: storeLessonId, setProgress, setTab, openSrsReview } = useApp();
  const { speak, supported: speechSupported } = useSpeech();
  const { show, node: toastNode } = useToast();

  const lessonId = lesson?.lesson_id ?? storeLessonId;
  const entries = useMemo(() => lesson?.words_to_learn || [], [lesson]);
  const words = useMemo(() => lessonWords(lesson), [lesson]);

  /**
   * Deck state is keyed by lesson so a lesson switch resets during render
   * Hỗ trợ Re-queue theo chuẩn Anki và tập hợp passedSet đếm từ hoàn thành.
   */
  const deckKey = entries.map((e) => e?.id ?? e?.word).join('|');
  const [deck, setDeck] = useState(() => ({
    key: deckKey,
    order: entries.map((_, i) => i),
    pos: 0,
    flipped: false,
    graded: 0,
    passedSet: new Set(),
    lastGrade: null,
  }));

  const freshDeck = (order) => ({
    key: deckKey,
    order,
    pos: 0,
    flipped: false,
    graded: 0,
    passedSet: new Set(),
    lastGrade: null,
  });

  // Render-phase reset: React re-renders immediately with the derived state.
  const state = deck.key === deckKey ? deck : freshDeck(entries.map((_, i) => i));
  if (deck.key !== deckKey) setDeck(state);

  const { order, pos, flipped, graded: gradedCount, passedSet, lastGrade } = state;
  const setFlipped = useCallback((v) => setDeck((d) => ({ ...d, flipped: typeof v === 'function' ? v(d.flipped) : v })), []);
  const setPos = useCallback((v) => setDeck((d) => ({ ...d, pos: typeof v === 'function' ? v(d.pos) : v })), []);

  const totalInQueue = order.length;
  const totalUnique = entries.length;
  const isFinished = totalUnique > 0 && (pos >= totalInQueue || passedSet.size >= totalUnique);
  const cardIndex = (!isFinished && totalInQueue && pos < totalInQueue) ? order[pos] : -1;
  const entry = cardIndex >= 0 ? entries[cardIndex] : null;

  /** First in-book example, cloze-blanked on the front, full on the back. */
  const primary = entry?.examples?.[0] || null;
  const clozeText = primary && entry ? makeCloze(primary.en, entry.word) : '';
  const familyRows = useMemo(() => combinedFamiliesFor(entry, lesson), [entry, lesson]);
  const frontCollocations = entry?.usage?.collocations?.length
    ? entry.usage.collocations
    : entry?.collocations || [];

  const flip = useCallback(() => setFlipped((f) => !f), [setFlipped]);

  const restart = useCallback(
    (shuffle) => {
      setDeck(freshDeck(shuffle ? shuffled(entries.map((_, i) => i)) : entries.map((_, i) => i)));
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [entries, deckKey],
  );

  /**
   * Grade via SM-2:
   * 1. Kích hoạt First-Touch: Tự động đánh dấu từ đã học trong progress
   * 2. Ghi nhận chu kỳ SM-2 vào toeic_srs
   * 3. Cơ chế Re-queue Anki: Bấm Again (1) -> thẻ tự động đẩy về cuối hàng đợi
   */
  const grade = useCallback(
    (g) => {
      if (!entry) return;

      // 1. First-Touch sync sang progress
      try {
        const nextProg = markWordLearned(lessonId, entry.word, true);
        if (setProgress) setProgress({ ...nextProg });
      } catch {
        /* ignore */
      }

      // 2. SM-2 update
      recordReview(lessonId, entry.word, g);

      // 3. Re-queue logic
      setDeck((d) => {
        const nextOrder = [...d.order];
        const nextPassed = new Set(d.passedSet);

        if (g === 1) {
          // Again: Chèn lại vào cuối hàng đợi phiên học
          nextOrder.push(cardIndex);
          show(`Cần nhớ lại: "${entry.word}" (sẽ xuất hiện lại ở cuối)`, 'rose');
        } else {
          // Hard / Good / Easy: Ghi nhận đã vượt qua từ này
          nextPassed.add(cardIndex);
          const meta = GRADES[g];
          show(`${meta.label} · ${meta.vi} — ${entry.word}`, meta.color === 'amber' ? 'brand' : 'emerald');
        }

        return {
          ...d,
          order: nextOrder,
          passedSet: nextPassed,
          lastGrade: g,
          graded: d.graded + 1,
          flipped: false,
          pos: d.pos + 1,
        };
      });
    },
    [entry, lessonId, cardIndex, setProgress, show],
  );

  /* ---- keyboard shortcuts: Tab (lật & đọc), Enter (tiếp tục), R (đọc từ), E (đọc ví dụ), Space, 1/2/3/4 ---- */
  useEffect(() => {
    const onKey = (e) => {
      const tag = e.target?.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || e.target?.isContentEditable) return;

      // Phím Tab: vừa lật vừa phát âm từ vựng
      if (e.key === 'Tab') {
        e.preventDefault();
        flip();
        if (entry?.word) speak(entry.word);
        return;
      }

      // Phím Enter: tiếp tục chuyển sang thẻ tiếp theo
      if (e.key === 'Enter') {
        e.preventDefault();
        setFlipped(false);
        setPos((p) => (total ? (p + 1) % total : 0));
        return;
      }

      // Phím R: phát âm từ vựng (Shift + R để đọc câu ví dụ)
      if (e.key === 'r' || e.key === 'R') {
        e.preventDefault();
        if (e.shiftKey && primary?.en) {
          speak(primary.en);
        } else if (entry?.word) {
          speak(entry.word);
        }
        return;
      }

      // Phím E: phát âm câu ví dụ
      if (e.key === 'e' || e.key === 'E') {
        e.preventDefault();
        if (primary?.en) speak(primary.en);
        return;
      }

      // Phím mũi tên: Thẻ sau / Thẻ trước
      if (e.key === 'ArrowRight') {
        e.preventDefault();
        setFlipped(false);
        setPos((p) => (total ? (p + 1) % total : 0));
        return;
      }
      if (e.key === 'ArrowLeft') {
        e.preventDefault();
        setFlipped(false);
        setPos((p) => (total ? (p - 1 + total) % total : 0));
        return;
      }

      // Phím Space: lật mặt thẻ
      if (e.code === 'Space' || e.key === ' ') {
        e.preventDefault();
        flip();
        return;
      }

      // Phím 1, 2, 3, 4: chấm điểm SRS
      if (['1', '2', '3', '4'].includes(e.key)) {
        e.preventDefault();
        grade(Number(e.key));
        return;
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [flip, grade, entry, primary, speak, setFlipped, setPos, totalInQueue]);

  /* --- null-safe empty state --- */
  if (!lesson || !entries.length) {
    return (
      <EmptyState
        icon={Layers}
        title="Chưa có flashcard"
        description={
          lesson
            ? 'Bài học này chưa có danh sách words_to_learn trong tệp JSON.'
            : 'Bài học chưa được trích xuất. Hãy chạy OCR để sinh lessons_json/lesson_XX.json rồi chọn lại bài.'
        }
      />
    );
  }

  const passedCount = passedSet.size;
  const progressPct = totalUnique ? Math.round((passedCount / totalUnique) * 100) : 0;

  return (
    <div className="space-y-4">
      {toastNode}

      <SectionTitle
        icon={Sparkles}
        title="Flashcard"
        right={
          <div className="flex flex-wrap items-center gap-2">
            <Badge tone={passedCount === totalUnique ? 'emerald' : 'brand'}>
              {passedCount}/{totalUnique} từ đã thuộc
            </Badge>
            <Badge tone="slate">Lượt chấm: {gradedCount}</Badge>
            <Button size="sm" variant="secondary" onClick={() => restart(true)} title="Xáo trộn bộ thẻ">
              <Shuffle className="h-3.5 w-3.5" />
              Xáo trộn
            </Button>
            <Button size="sm" variant="ghost" onClick={() => restart(false)} title="Bắt đầu lại từ thẻ 1">
              <RotateCcw className="h-3.5 w-3.5" />
              Bắt đầu lại
            </Button>
          </div>
        }
      />

      <div className="mx-auto max-w-3xl">
        <div className="mb-1.5 flex items-center justify-between text-[11px] font-extrabold uppercase tracking-wide text-[var(--color-duo-gray)]">
          <span>Tiến độ bài học (First-Touch)</span>
          <span className="tabular-nums text-[var(--color-duo-green-dark)]">
            {passedCount}/{totalUnique} từ đã qua · {progressPct}%
          </span>
        </div>
        <ProgressBar value={passedCount} max={Math.max(totalUnique, 1)} />
      </div>

      {/* MÀN HÌNH HOÀN THÀNH PHIÊN FLASHCARD (NẾU ĐÃ PASS HẾT TẤT CẢ TỪ) */}
      {isFinished ? (
        <Card className="mx-auto max-w-2xl p-7 text-center">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-[var(--color-duo-green)] text-white shadow-[0_4px_0_0_var(--color-duo-green-dark)]">
            <CheckCircle2 className="h-8 w-8" />
          </div>
          <h3 className="mt-4 text-2xl font-black text-slate-900 dark:text-white">
            Hoàn thành xuất sắc bộ thẻ Bài {String(lessonId).padStart(2, '0')}!
          </h3>
          <p className="mt-2 text-sm font-semibold text-slate-600 dark:text-slate-300">
            Bạn đã tiếp cận và tự đánh giá đầy đủ {totalUnique}/{totalUnique} từ vựng mục tiêu theo chuẩn Anki.
            Trạng thái <span className="text-emerald-600 font-bold">"Đã học"</span> đã được kích hoạt đồng bộ vào Sổ tay và Lịch ôn tập SM-2.
          </p>

          <div className="mt-6 flex flex-wrap justify-center gap-3">
            <Button
              variant="primary"
              size="md"
              onClick={() => {
                if (openSrsReview) {
                  openSrsReview({ filter: 'lesson', lessonId });
                } else if (setTab) {
                  setTab('srs');
                }
              }}
              className="gap-2"
            >
              <span>Gõ từ ôn tập (Active Recall)</span>
              <ArrowRight className="h-4 w-4" />
            </Button>
            <Button
              variant="secondary"
              size="md"
              onClick={() => setTab?.('vocab')}
              className="gap-2"
            >
              <BookOpen className="h-4 w-4" />
              <span>Xem Sổ tay từ vựng</span>
            </Button>
            <Button
              variant="ghost"
              size="md"
              onClick={() => restart(false)}
              className="gap-2"
            >
              <RotateCcw className="h-4 w-4" />
              <span>Luyện lại bộ thẻ</span>
            </Button>
          </div>
        </Card>
      ) : entry ? (
        <>
          {/* ---------- FLIP CARD ---------- */}
          <div className="flip-scene mx-auto h-[560px] w-full max-w-3xl">
        <div className={`flip-inner ${flipped ? 'is-flipped' : ''}`}>
          {/* ================= FRONT ================= */}
          <div className="flip-face front">
            <Card className="flex h-full flex-col overflow-hidden p-5">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <h4 className="break-words text-2xl font-extrabold tracking-tight text-[var(--color-duo-ink)]">
                      {entry.word}
                    </h4>
                    {entry.pos ? <Badge tone="violet">{entry.pos}</Badge> : null}
                  </div>
                  {entry.ipa ? (
                    <p className="mt-0.5 font-mono text-[13px] text-[var(--color-duo-gray)]">
                      {entry.ipa}
                    </p>
                  ) : null}
                </div>
                <Button
                  size="icon"
                  variant="secondary"
                  disabled={!speechSupported}
                  onClick={() => speak(entry.word)}
                  aria-label={`Phát âm ${entry.word}`}
                  title={speechSupported ? `Nghe phát âm: ${entry.word}` : 'Không hỗ trợ Web Speech API'}
                >
                  <Volume2 className="h-4 w-4 text-[var(--color-duo-blue)]" />
                </Button>
              </div>

              <div className="mt-4 flex-1">
                <p className="mb-1.5 text-[11px] font-extrabold uppercase tracking-wide text-[var(--color-duo-muted)]">
                  Điền từ còn thiếu vào chỗ trống {String.fromCharCode(97)}
                </p>
                {primary ? (
                  <p className="rounded-2xl bg-[var(--color-duo-bg-soft)] px-3.5 py-3 text-[15px] font-medium leading-relaxed text-[var(--color-duo-ink)] ring-2 ring-inset ring-[var(--color-duo-line)]">
                    <ClozeText text={clozeText} />
                  </p>
                ) : (
                  <p className="rounded-xl border-2 border-dashed border-[var(--color-duo-line-strong)] px-3 py-2 text-[13px] italic text-[var(--color-duo-muted)]">
                    Sách không có câu ví dụ cho từ này — bấm Space để xem nghĩa và cụm từ.
                  </p>
                )}

                {frontCollocations.length ? (
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {frontCollocations.map((c, i) => (
                      <span
                        key={i}
                        className="inline-flex items-center rounded-lg bg-[var(--color-duo-blue-light)] px-2 py-1 font-mono text-[11.5px] font-semibold text-[#0b6ea8]"
                      >
                        {c}
                      </span>
                    ))}
                  </div>
                ) : null}
              </div>

              <div className="mt-4 flex items-center justify-between gap-3 border-t-2 border-[var(--color-duo-line)] pt-3.5">
                <p className="text-[12px] font-medium text-[var(--color-duo-gray)]">
                  Nhấn{' '}
                  <kbd className="rounded-lg border-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] px-1.5 py-0.5 font-mono text-[11px] font-bold">
                    Space
                  </kbd>{' '}
                  để lật thẻ
                </p>
                <Button variant="primary" size="sm" onClick={flip}>
                  <Eye className="h-3.5 w-3.5" />
                  Xem đáp án
                </Button>
              </div>
            </Card>
          </div>

          {/* ================= BACK ================= */}
          <div className="flip-face back">
            <Card className="flex h-full flex-col overflow-auto p-5">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <h4 className="break-words text-xl font-extrabold tracking-tight text-[var(--color-duo-ink)]">
                      {entry.word}
                    </h4>
                    {entry.pos ? <Badge tone="violet">{entry.pos}</Badge> : null}
                    {entry.ipa ? (
                      <span className="font-mono text-[12.5px] text-[var(--color-duo-gray)]">
                        {entry.ipa}
                      </span>
                    ) : null}
                  </div>
                  <p className="mt-1 text-[13.5px] font-bold leading-snug text-[var(--color-duo-ink)]">
                    <span className="mr-1.5 inline-flex items-center rounded-md bg-slate-200 px-1.5 py-0.5 text-[10px] font-extrabold uppercase text-slate-700">
                      EN
                    </span>
                    {entry.definition_en}
                  </p>
                  <p className="mt-1 text-[14px] font-extrabold leading-snug text-[var(--color-duo-green-dark)]">
                    <span className="mr-1.5 inline-flex items-center rounded-md bg-[var(--color-duo-green-light)] px-1.5 py-0.5 text-[10px] font-extrabold uppercase text-[var(--color-duo-green-dark)]">
                      VI
                    </span>
                    {entry.definition_vi}
                  </p>
                </div>
                <Button
                  size="icon"
                  variant="secondary"
                  disabled={!speechSupported}
                  onClick={() => speak(entry.word)}
                  aria-label={`Phát âm ${entry.word}`}
                >
                  <Volume2 className="h-4 w-4 text-[var(--color-duo-blue)]" />
                </Button>
              </div>

              <div className="mt-3 flex-1 space-y-3 overflow-auto pr-0.5">
                {primary ? (
                  <div className="rounded-xl border-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] px-3 py-2">
                    <p className="text-[14px] leading-relaxed text-[var(--color-duo-ink)]">
                      <Highlighted text={primary.en} words={words} />
                    </p>
                    {primary.vi ? (
                      <p className="mt-1 text-[12.5px] italic leading-relaxed text-[var(--color-duo-gray)]">
                        {primary.vi}
                      </p>
                    ) : null}
                  </div>
                ) : null}

                {entry.examples?.length > 1 ? (
                  <div className="space-y-2">
                    <p className="text-[11px] font-extrabold uppercase tracking-wide text-[var(--color-duo-muted)]">
                      Ví dụ khác trong sách
                    </p>
                    {entry.examples.slice(1).map((ex, i) => (
                      <div
                        key={i}
                        className="rounded-xl border-2 border-[var(--color-duo-line)] px-3 py-2"
                      >
                        <p className="text-[13px] leading-relaxed text-[var(--color-duo-ink)]">
                          <Highlighted text={ex.en} words={words} />
                        </p>
                        {ex.vi ? (
                          <p className="mt-0.5 text-[12px] italic text-[var(--color-duo-gray)]">
                            {ex.vi}
                          </p>
                        ) : null}
                      </div>
                    ))}
                  </div>
                ) : null}

                <UsageBox usage={entry.usage} collocations={entry.collocations} />
                <WordFamilyTable rows={familyRows} words={words} />
              </div>

              {/* grade buttons */}
              <div className="mt-3 border-t-2 border-[var(--color-duo-line)] pt-3">
                <p className="mb-2 text-center text-[11.5px] font-semibold text-[var(--color-duo-gray)]">
                  Chấm mức độ nhớ (phím <span className="font-mono">1</span>–
                  <span className="font-mono">4</span>) — thẻ tiếp theo tự động
                </p>
                <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
                  {Object.values(GRADES).map((g) => (
                    <Button
                      key={g.id}
                      size="sm"
                      variant={
                        g.id === 1 ? 'danger' : g.id === 2 ? 'amber' : g.id === 3 ? 'success' : 'primary'
                      }
                      onClick={() => grade(g.id)}
                      className="!normal-case flex-col gap-0 py-1.5 !tracking-normal"
                    >
                      <span className="text-[12px] font-extrabold">
                        <span className="mr-1 opacity-70">{g.id}</span>
                        {g.label}
                      </span>
                      <span className="text-[10.5px] font-semibold opacity-80">{g.vi}</span>
                    </Button>
                  ))}
                </div>
                {lastGrade ? (
                  <p className="mt-2 text-center text-[11.5px] font-semibold text-[var(--color-duo-gray)]">
                    Thẻ vừa chấm:{' '}
                    <span className="font-extrabold text-[var(--color-duo-ink)]">
                      {GRADES[lastGrade].label}
                    </span>{' '}
                    · {GRADES[lastGrade].vi}
                  </p>
                ) : null}
              </div>
            </Card>
          </div>
        </div>
      </div>

        {/* ---------- grade row also reachable before flipping ---------- */}
        <div className="mx-auto flex max-w-3xl flex-wrap items-center justify-between gap-3">
          <p className="text-[11.5px] font-semibold text-[var(--color-duo-muted)]">
            Phím tắt: <kbd className="rounded border border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] px-1.5 py-0.5 font-mono text-[10.5px]">Tab</kbd> Lật &amp; Đọc · <kbd className="rounded border border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] px-1.5 py-0.5 font-mono text-[10.5px]">Enter</kbd> Tiếp tục · <kbd className="rounded border border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] px-1.5 py-0.5 font-mono text-[10.5px]">R</kbd> Đọc từ · <kbd className="rounded border border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] px-1.5 py-0.5 font-mono text-[10.5px]">1-4</kbd> Chấm điểm
          </p>
          <div className="flex gap-2.5">
            <Button
              size="sm"
              variant="secondary"
              onClick={() => {
                setFlipped(false);
                setPos((p) => (totalInQueue ? (p - 1 + totalInQueue) % totalInQueue : 0));
              }}
            >
              ← Thẻ trước
            </Button>
            <Button
              size="sm"
              variant="secondary"
              onClick={() => {
                setFlipped(false);
                setPos((p) => (totalInQueue ? (p + 1) % totalInQueue : 0));
              }}
            >
              Thẻ sau →
            </Button>
          </div>
        </div>
      </>
    ) : null}
  </div>
);
}

/** Render a cloze string, styling the blank and highlighting any other target words. */
function ClozeText({ text }) {
  const parts = String(text ?? '').split(/(_{3,})/g);
  return (
    <>
      {parts.map((p, i) =>
        /^_{3,}$/.test(p) ? (
          <span key={i} className="cloze-blank">
            {p}
          </span>
        ) : (
          <span key={i}>{p}</span>
        ),
      )}
    </>
  );
}
