/**
 * TAB 1 — Deep Context Vocabulary ("Học Từ Vựng").
 *
 * CORE PRODUCT PRINCIPLE — CONTEXT-FIRST:
 * A target word is NEVER rendered bare. Every word card ships with
 *   1. its English and Vietnamese definitions,
 *   2. its USE box (structures, prepositions, TOEIC collocations, usage tip),
 *   3. its real in-book example sentences (with the target bolded + VI translation), and
 *   4. its word-family table (book rows + extended POS forms, each with an example).
 *
 * Owned by: vocab-dev. Imports only the frozen shared APIs.
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { ArrowRight, BookOpenCheck, Check, CheckCircle2, Eye, EyeOff, Layers, ListChecks, Sparkles, Volume2, X } from 'lucide-react';
import { Badge, Button, Card, EmptyState, Highlighted, SectionTitle, useSpeech, useToast } from '../components/ui.jsx';
import { useApp } from '../lib/store.jsx';
import { familiesForEntry, groupFamilyRows, normalizeFamilyRows } from '../lib/lessonLoader.js';
import { markWordLearned } from '../lib/storage.js';
import { freshCard, loadSrs, saveSrs, srsKey } from '../lib/srs.js';
import { WORD_FAMILY_LABEL, WORD_FAMILY_ORDER } from '../lib/types.js';

/* ---------------- local helpers (tab-private) ---------------- */

/** All target words of a lesson — fed to <Highlighted/> so hits are never hand-rolled. */
function lessonWords(lesson) {
  return (lesson?.words_to_learn || []).map((w) => w?.word).filter(Boolean);
}

/**
 * Map word -> its family rows from the book (entry or lesson-level), plus
 * extended word-family rows (`entry.extra_families`) without duplicating words.
 */
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

/** Group family rows into WORD_FAMILY_ORDER buckets; a form with no row is null. */
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
    // Multiple noun rows are legitimate (provider + provision); keep them all.
    (byPos[key] = byPos[key] || []).push(r);
  }
  return WORD_FAMILY_ORDER.map((pos) => ({ pos, rows: byPos[pos] || [] }));
}

/** True when the progress map marks this word learned. */
function pickLearned(progress, lessonId, word) {
  if (!lessonId || !word) return false;
  const lessonKey = `L${String(lessonId).padStart(2, '0')}`;
  const words = progress?.[lessonKey]?.words || {};
  const srsK = `${lessonKey}:${String(word).toLowerCase()}`;
  if (typeof words[srsK] === 'boolean') return words[srsK];
  for (const [k, v] of Object.entries(words)) {
    if (String(k).toLowerCase().endsWith(`:${String(word).toLowerCase()}`)) return Boolean(v);
  }
  return false;
}

/* ---------------- sub-components ---------------- */

/**
 * Framed USE box: prepositions badges, grammatical structures, TOEIC collocations, and usage tip.
 */
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
    <div className="mt-3 rounded-2xl border-2 border-[#bde3ff] bg-[#f3faff] p-3">
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
            Cụm từ thường gặp (Collocations)
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

/** A single in-book example with a hide/show Vietnamese toggle. */
function ExampleBlock({ label, example, words, onToggleVi, viVisible = true }) {
  const [showVi, setShowVi] = useState(Boolean(viVisible));
  const hasVi = Boolean(example?.vi);

  const toggle = () => {
    const next = !showVi;
    setShowVi(next);
    onToggleVi?.(next);
  };

  if (!example?.en) return null;

  return (
    <div className="rounded-xl border-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] px-3 py-2">
      <div className="flex items-start gap-2">
        <span className="mt-0.5 shrink-0 rounded-lg bg-[var(--color-duo-green-light)] px-1.5 py-0.5 text-[10px] font-extrabold uppercase text-[var(--color-duo-green-dark)]">
          {label}
        </span>
        <p className="min-w-0 flex-1 text-[13.5px] leading-relaxed text-[var(--color-duo-ink)]">
          <Highlighted text={example.en} words={words} />
        </p>
      </div>

      {hasVi ? (
        <div className="mt-1.5 flex items-start gap-2 pl-1">
          <button
            type="button"
            onClick={toggle}
            aria-expanded={showVi}
            className="mt-0.5 inline-flex shrink-0 items-center gap-1 rounded-lg px-1.5 py-0.5 text-[10.5px] font-bold text-[var(--color-duo-muted)] transition-colors hover:bg-[var(--color-duo-line)] hover:text-[var(--color-duo-ink)]"
          >
            {showVi ? <EyeOff className="h-3 w-3" /> : <Eye className="h-3 w-3" />}
            {showVi ? 'Ẩn dịch' : 'Hiện dịch'}
          </button>
          {showVi ? (
            <p className="min-w-0 flex-1 text-[12.5px] italic leading-relaxed text-[var(--color-duo-gray)]">
              {example.vi}
            </p>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}

/** Word-family table: Verb / Noun / Adj / Adv, combining book rows + extended forms. */
function WordFamilyTable({ rows, words }) {
  const buckets = useMemo(() => familyBuckets(rows), [rows]);

  return (
    <div className="mt-3">
      <p className="mb-1 text-[11px] font-semibold uppercase tracking-wide text-slate-400">
        Họ từ (word family)
      </p>
      <div className="overflow-hidden rounded-2xl border-2 border-[var(--color-duo-line)]">
        {/* Header row */}
        <div className="grid grid-cols-1 divide-y divide-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] sm:grid-cols-4 sm:divide-x sm:divide-y-0">
          {WORD_FAMILY_ORDER.map((pos) => (
            <div
              key={pos}
              className="px-2.5 py-1.5 text-[11px] font-extrabold uppercase tracking-wide text-[var(--color-duo-gray)]"
            >
              {WORD_FAMILY_LABEL[pos]}
            </div>
          ))}
        </div>

        {/* Body is a grid (not table cells) so each POS can stack multiple forms. */}
        <div className="grid grid-cols-1 divide-y divide-[var(--color-duo-line)] sm:grid-cols-4 sm:divide-x sm:divide-y-0">
          {buckets.map(({ pos, rows: cellRows }) => (
            <div key={pos} className="min-w-0 px-2.5 py-2">
              {cellRows.length ? (
                <ul className="space-y-2">
                  {cellRows.map((r, i) => (
                    <li key={i}>
                      <p className="break-words text-[13px] font-extrabold text-[var(--color-duo-green-dark)]">
                        {r.word}
                        {r.pos_source === 'derived' ? (
                          <span className="ml-1 inline-block whitespace-nowrap align-middle text-[9.5px] font-bold uppercase text-[var(--color-duo-orange)]">
                            suy ra
                          </span>
                        ) : r.pos_source === 'extended' ? (
                          <span className="ml-1 inline-block whitespace-nowrap rounded bg-sky-100 dark:bg-sky-950/70 dark:border dark:border-sky-800 px-1 py-0.5 align-middle text-[9px] font-bold uppercase text-sky-700 dark:text-sky-300">
                            mở rộng
                          </span>
                        ) : null}
                      </p>
                      {r.example ? (
                        <p className="mt-0.5 text-[12px] leading-relaxed text-[var(--color-duo-gray)]">
                          <Highlighted text={r.example} words={words} />
                        </p>
                      ) : (
                        <p className="mt-0.5 text-[12px] italic text-[var(--color-duo-muted)]">
                          Chưa có câu ví dụ trong sách.
                        </p>
                      )}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="select-none text-[15px] font-medium text-[var(--color-duo-muted)]" aria-label="Không có dữ liệu">
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

/** One vocabulary card — context-first, never a bare word. */
function WordCard({ entry, lesson, index, words, learned, onToggleLearned, onSpeak, speechSupported }) {
  const familyRows = useMemo(() => combinedFamiliesFor(entry, lesson), [entry, lesson]);
  const hasContext = Boolean(
    entry?.examples?.length ||
      entry?.collocations?.length ||
      entry?.usage ||
      familyRows.length,
  );
  const exampleCount = (entry?.examples || []).length;

  return (
    <Card
      id={`word-${encodeURIComponent(String(entry?.word || '').toLowerCase().trim())}`}
      className="flex h-full flex-col p-4 transition-all duration-300"
    >
      {/* --- head: word + pos + ipa + pronounce --- */}
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-[var(--color-duo-green)] text-[11px] font-extrabold text-white shadow-[0_2px_0_0_var(--color-duo-green-dark)]">
              {index + 1}
            </span>
            <h4 className="break-words text-lg font-extrabold tracking-tight text-[var(--color-duo-ink)]">
              {entry.word}
            </h4>
            {entry.pos ? <Badge tone="violet">{entry.pos}</Badge> : null}
          </div>
          {entry.ipa ? (
            <p className="mt-0.5 font-mono text-[12.5px] text-[var(--color-duo-gray)]">
              {entry.ipa}
            </p>
          ) : null}
        </div>

        <Button
          size="icon"
          variant="secondary"
          disabled={!speechSupported}
          onClick={() => onSpeak(entry.word)}
          title={
            speechSupported
              ? `Nghe phát âm US-English: ${entry.word}`
              : 'Trình duyệt không hỗ trợ đọc tiếng Anh (Web Speech API)'
          }
          aria-label={`Phát âm ${entry.word}`}
          className="shrink-0"
        >
          <Volume2 className="h-4 w-4 text-[var(--color-duo-blue)]" />
        </Button>
      </div>

      {/* --- definitions (EN + prominent VI) --- */}
      <div className="mt-2.5 space-y-1.5 rounded-xl border-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] px-3 py-2">
        <p className="text-[13.5px] font-bold leading-snug text-[var(--color-duo-ink)]">
          <span className="mr-1.5 inline-flex items-center rounded-md bg-slate-200 px-1.5 py-0.5 text-[10px] font-extrabold uppercase text-slate-700">
            EN
          </span>
          {entry.definition_en}
        </p>
        <p className="text-[14px] font-extrabold leading-snug text-[var(--color-duo-green-dark)]">
          <span className="mr-1.5 inline-flex items-center rounded-md bg-[var(--color-duo-green-light)] px-1.5 py-0.5 text-[10px] font-extrabold uppercase text-[var(--color-duo-green-dark)]">
            VI
          </span>
          {entry.definition_vi}
        </p>
      </div>

      {/* --- USE box: structures, prepositions, collocations, tip --- */}
      <UsageBox usage={entry.usage} collocations={entry.collocations} />

      {/* --- both in-book examples, target bolded, each with a VI toggle --- */}
      <div className="mt-3 space-y-2">
        <p className="text-[11px] font-extrabold uppercase tracking-wide text-[var(--color-duo-muted)]">
          Ví dụ trong sách ({exampleCount})
        </p>
        {(entry.examples || []).map((ex, i) => (
          <ExampleBlock
            key={i}
            label={String.fromCharCode(97 + i)}
            example={ex}
            words={words}
            viVisible={true}
          />
        ))}
        {!entry.examples?.length ? (
          <p className="rounded-xl border-2 border-dashed border-[var(--color-duo-line-strong)] px-3 py-2 text-[12.5px] italic text-[var(--color-duo-muted)]">
            Sách không có câu ví dụ cho từ này.
          </p>
        ) : null}
      </div>

      {/* --- word family table (book + extended POS forms) --- */}
      <WordFamilyTable rows={familyRows} words={words} />

      {/* --- learned toggle --- */}
      <div className="mt-auto pt-3.5">
        <Button
          variant={learned ? 'success' : 'secondary'}
          size="md"
          onClick={() => onToggleLearned(entry.word, !learned)}
          className="w-full"
          aria-pressed={learned}
        >
          {learned ? <Check className="h-4 w-4" /> : <CheckCircle2 className="h-4 w-4" />}
          {learned ? 'Đã học' : 'Đánh dấu đã học'}
        </Button>
        {!hasContext ? (
          <p className="mt-1 text-center text-[10.5px] font-semibold text-[var(--color-duo-orange)]">
            Thiếu dữ liệu ngữ cảnh cho từ này.
          </p>
        ) : null}
      </div>
    </Card>
  );
}

/* ---------------- main tab ---------------- */

export default function Tab1Vocabulary({ lesson }) {
  const { lessonId: storeLessonId, progress, setProgress, pendingScrollWord, setPendingScrollWord, setTab } = useApp();
  const { speak, supported: speechSupported } = useSpeech();
  const { show, node: toastNode } = useToast();

  const lessonId = lesson?.lesson_id ?? storeLessonId;
  const words = useMemo(() => lessonWords(lesson), [lesson]);
  const entries = useMemo(() => lesson?.words_to_learn || [], [lesson]);

  const [filter, setFilter] = useState('all'); // all | learning | learned

  useEffect(() => {
    if (!pendingScrollWord || !entries.length) return;
    setFilter('all');
    const target = String(pendingScrollWord).toLowerCase().trim();
    const timer = setTimeout(() => {
      const el = document.getElementById(`word-${encodeURIComponent(target)}`);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.classList.add('ring-4', 'ring-[var(--color-duo-green)]', 'shadow-xl');
        setTimeout(() => {
          el.classList.remove('ring-4', 'ring-[var(--color-duo-green)]', 'shadow-xl');
        }, 2500);
      }
      if (setPendingScrollWord) setPendingScrollWord(null);
    }, 250);
    return () => clearTimeout(timer);
  }, [pendingScrollWord, entries, setPendingScrollWord]);

  const isLearned = useCallback(
    (w) => pickLearned(progress, lessonId, w),
    [progress, lessonId],
  );

  const learnedCount = useMemo(
    () => entries.filter((e) => isLearned(e.word)).length,
    [entries, isLearned],
  );

  const handleToggleLearned = useCallback(
    (word, next) => {
      const map = markWordLearned(lessonId, word, next);
      setProgress({ ...map });

      // Khởi tạo thẻ SRS đồng bộ nếu người học tự đánh dấu đã học
      if (next) {
        try {
          const allSrs = loadSrs();
          const key = srsKey(lessonId, word);
          if (!allSrs[key]) {
            allSrs[key] = {
              ...freshCard(),
              word,
              lessonId,
              lastGrade: 3,
              interval: 1,
              reps: 1,
            };
            saveSrs(allSrs);
          }
        } catch {
          /* ignore */
        }
      }

      show(next ? `Đã đánh dấu: ${word}` : `Bỏ đánh dấu: ${word}`, next ? 'emerald' : 'brand');
    },
    [lessonId, setProgress, show],
  );

  const handleSpeak = useCallback(
    (text) => {
      speak(text);
    },
    [speak],
  );

  /* --- null-safe empty state (App passes lesson={null} when not extracted) --- */
  if (!lesson || !entries.length) {
    return (
      <EmptyState
        icon={Layers}
        title="Chưa có dữ liệu từ vựng"
        description={
          lesson
            ? 'Bài học này chưa có danh sách words_to_learn trong tệp JSON.'
            : 'Bài học chưa được trích xuất. Hãy chạy OCR để sinh lessons_json/lesson_XX.json rồi chọn lại bài.'
        }
      />
    );
  }

  const shown = entries.filter((e) =>
    filter === 'learned' ? isLearned(e.word) : filter === 'learning' ? !isLearned(e.word) : true,
  );

  return (
    <div className="space-y-4">
      {toastNode}

      <SectionTitle
        icon={BookOpenCheck}
        title="Vocabulary (Sổ tay từ vựng)"
        right={
          <div className="flex flex-wrap items-center gap-2">
            <Button
              size="sm"
              variant="primary"
              onClick={() => setTab?.('flashcard')}
              className="gap-1.5 shadow-xs"
              title="Chuyển sang Flashcard (Tab 2) để tiếp cận và học từ mới theo chuẩn Anki"
            >
              <Sparkles className="h-3.5 w-3.5" />
              <span>Luyện Flashcard (Tab 2)</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </Button>
            <Badge tone={learnedCount === entries.length ? 'emerald' : 'brand'}>
              {learnedCount}/{entries.length} đã học
            </Badge>
            <div className="flex gap-1.5 rounded-2xl border-2 border-[var(--color-duo-line)] bg-white p-1">
              {[
                { id: 'all', label: 'Tất cả' },
                { id: 'learning', label: 'Chưa học' },
                { id: 'learned', label: 'Đã học' },
              ].map((f) => (
                <button
                  key={f.id}
                  type="button"
                  onClick={() => setFilter(f.id)}
                  className={`rounded-xl px-3 py-1.5 text-xs font-extrabold uppercase tracking-wide transition-colors ${
                    filter === f.id
                      ? 'bg-[var(--color-duo-blue)] text-white'
                      : 'text-[var(--color-duo-gray)] hover:bg-[var(--color-duo-bg-soft)]'
                  }`}
                >
                  {f.label}
                </button>
              ))}
            </div>
          </div>
        }
      />

      {!speechSupported ? (
        <p className="rounded-xl bg-[#fff4cc] px-3 py-2 text-[12px] font-semibold text-[#8a6d00]">
          Trình duyệt hiện tại không hỗ trợ Web Speech API — nút phát âm sẽ bị vô hiệu hóa.
        </p>
      ) : null}

      {shown.length ? (
        <div className="space-y-4">
          <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
            {shown.map((entry) => (
              <WordCard
                key={entry.id ?? entry.word}
                entry={entry}
                lesson={lesson}
                index={entries.indexOf(entry)}
                words={words}
                learned={isLearned(entry.word)}
                onToggleLearned={handleToggleLearned}
                onSpeak={handleSpeak}
                speechSupported={speechSupported}
              />
            ))}
          </div>

          {/* Banner chuyển tiếp sang Tab 2 Flashcard */}
          <Card className="flex flex-wrap items-center justify-between gap-3 p-4 border-2 border-[var(--color-duo-blue)] bg-[var(--color-duo-blue-light)]/40 dark:bg-slate-800/80">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[var(--color-duo-blue)] text-white shadow-xs">
                <Sparkles className="h-5 w-5" />
              </div>
              <div>
                <h4 className="text-sm font-black text-slate-900 dark:text-white">
                  Bắt đầu nạp từ vào trí nhớ qua Flashcard?
                </h4>
                <p className="text-xs font-semibold text-slate-500 dark:text-slate-400">
                  Lướt nhanh 12 từ với câu đục lỗ ngữ cảnh, nghe audio và tự lượng giá để kích hoạt chu kỳ SM-2.
                </p>
              </div>
            </div>
            <Button
              variant="primary"
              size="md"
              onClick={() => setTab?.('flashcard')}
              className="gap-2"
            >
              <span>Vào Flashcard ngay</span>
              <ArrowRight className="h-4 w-4" />
            </Button>
          </Card>
        </div>
      ) : (
        <EmptyState
          icon={ListChecks}
          title={filter === 'learned' ? 'Chưa đánh dấu từ nào' : 'Bạn đã học hết từ của bài này'}
          description={
            filter === 'learned'
              ? 'Bấm "Đánh dấu đã học" trên từng thẻ để theo dõi tiến độ.'
              : 'Chuyển sang bộ lọc "Đã học" để xem lại.'
          }
          action={
            <Button variant="primary" size="sm" onClick={() => setFilter('all')}>
              <X className="h-3.5 w-3.5" />
              Xem tất cả
            </Button>
          }
        />
      )}
    </div>
  );
}
