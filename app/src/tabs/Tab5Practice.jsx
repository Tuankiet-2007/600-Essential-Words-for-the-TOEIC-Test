/**
 * TAB 5 — "Luyện Đề & Audio" (Book Practice, TOEIC Parts 1-7).
 *
 * Layout: a sticky AudioPlayer on top, then the Listening block (Parts 1-4,
 * questions 1-9) and the Reading block (Parts 5-7, questions 10-23), then one
 * big "Nộp bài & Chấm điểm" button and a per-section ScoreSummary.
 *
 * Truthfulness rules baked in (the book data really is this incomplete):
 *   - Part 1 JSON carries only `{question_num, photo}`: the four A/B/C/D option
 *     TEXTS are spoken on the audio, so we render the photo + four selection
 *     buttons and a Vietnamese note instead of inventing options.
 *   - Part 2 JSON carries only `{question_num, options:["A","B","C"]}`: A/B/C
 *     buttons with the (absent) text kept hidden until the learner submits.
 *   - Listening answers live in the book's Answer Key, not the lesson JSON. The
 *     key is now parsed from the book's own Answer Key pages, so Parts 1-4 are
 *     graded against the real answer instead of being self-marked. Only the few
 *     entries whose OCR could not be recovered stay ungraded, and those say so.
 *   - Part 6's passage already contains literal `[16] [17] [18]` markers; the
 *     passage is rendered verbatim and each marker is wired to its question.
 *
 * Owned by: practice-dev. This file is the ONLY file this task may write.
 */
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  BookOpen,
  CircleCheck,
  CircleX,
  Clock,
  Eye,
  EyeOff,
  FileText,
  Gauge,
  Headphones,
  History,
  Image as ImageIcon,
  Info,
  Lightbulb,
  ListChecks,
  Pause,
  PenLine,
  Play,
  RotateCcw,
  RotateCw,
  Send,
  Timer,
  Trash2,
  Trophy,
  Volume2,
} from 'lucide-react';
import {
  Badge,
  Button,
  Card,
  EmptyState,
  Highlighted,
  ProgressBar,
  SectionTitle,
} from '../components/ui.jsx';
import { audioUrlFor, photoUrlFor } from '../lib/assets.js';
import {
  answerFor,
  explanationFor,
  loadAnswers,
  loadExplanations,
  loadTapescripts,
  tapescriptFor,
} from '../lib/answerKey.js';
import { recordReview } from '../lib/srs.js';
import {
  clearHistory,
  deleteHistoryItem,
  loadHistory,
  markWordLearned,
  pushHistory,
} from '../lib/storage.js';
import { useApp } from '../lib/store.jsx';

/* ------------------------------------------------------------------ */
/* Local constants & pure helpers (tab-private, never shared)          */
/* ------------------------------------------------------------------ */

const CHOICE_LETTERS = ['A', 'B', 'C', 'D'];
const SPEEDS = [0.8, 1.0, 1.2, 1.5];

/** Section keys used by the answer map and the score summary. */
const SEC_LISTENING = 'listening';
const SEC_PART5 = 'part5';
const SEC_PART6 = 'part6';
const SEC_PART7 = 'part7';

const SECTION_META = [
  { key: SEC_LISTENING, label: 'Listening (Part 1-4)', hint: 'Câu 1-9' },
  { key: SEC_PART5, label: 'Part 5 — Điền vào chỗ trống', hint: 'Câu 10-15' },
  { key: SEC_PART6, label: 'Part 6 — Đọc hiểu đoạn văn', hint: 'Câu 16-18' },
  { key: SEC_PART7, label: 'Part 7 — Đọc hiểu tài liệu', hint: 'Câu 19-23' },
];

// Copied locally because the frozen contract does not export the mapping.
const PASSAGE_TYPE_LABEL = {
  letter: 'Thư',
  form: 'Biểu mẫu',
  memo: 'Bản ghi nhớ',
  email: 'Email',
  notice: 'Thông báo',
  article: 'Bài báo',
};

const LISTENING_MISSING_ANSWER_NOTE =
  'Câu này chưa có đáp án: bản OCR của trang Answer Key không đọc được mục tương ứng. Bạn hãy tự đối chiếu với Answer Key trong sách.';

const TAPESCRIPT_ABSENT = 'Chưa có tapescript cho bài này';

/**
 * renderExplain — chuyen chuoi giai thich (co the chua <b>/<i>) thanh React node.
 *
 * AN TOAN: KHONG dung dangerouslySetInnerHTML voi HTML tho. Giai thich do
 * scripts/build_explanations.py sinh ra va chi dung 2 the <b> (nhan manh) va
 * <i> (dinh nghia sach in). Ham nay tu tach chuoi va tu dung <strong>/<em>,
 * nen moi thu khac deu bi coi la VAN BAN thuong — khong the tiem HTML la.
 */
function renderExplain(text) {
  if (!text) return null;
  const parts = String(text).split(/(<b>.*?<\/b>|<i>.*?<\/i>)/g).filter(Boolean);
  return parts.map((chunk, i) => {
    if (chunk.startsWith('<b>') && chunk.endsWith('</b>')) {
      return <strong key={i}>{chunk.slice(3, -4)}</strong>;
    }
    if (chunk.startsWith('<i>') && chunk.endsWith('</i>')) {
      return <em key={i}>{chunk.slice(3, -4)}</em>;
    }
    return <span key={i}>{chunk}</span>;
  });
}

/**
 * Tieu de chuan TOEIC cho tung part — chi dung khi sach khong in tieu de
 * (`listening.parts` thieu hoac `title` rong). Khong bao gio bia tieu de khac.
 */
const TOEIC_PART_TITLE = { 1: 'Photo', 2: 'Question—Response', 3: 'Conversation', 4: 'Talk' };

/** Nhan tieng Viet ngan cho tung part trong thanh phu cua tieu de muc. */
const PART_TITLE_VI = { 1: 'Part 1', 2: 'Part 2', 3: 'Part 3', 4: 'Part 4' };

/** All target words of a lesson — the only input given to <Highlighted/>. */
function lessonWords(lesson) {
  return (lesson?.words_to_learn || [])
    .map((w) => w?.word)
    .filter((w) => typeof w === 'string' && w.trim());
}

/** "A", "b ", "A." -> "A"; null when it cannot be read as a choice letter. */
function normalizeLetter(value) {
  if (value === null || value === undefined) return null;
  const m = String(value).trim().toUpperCase().match(/^([A-D])\b/);
  return m ? m[1] : null;
}

function lettersOf(options) {
  return Object.keys(options || {}).filter((k) => /^[A-D]$/.test(k));
}

function hasText(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

/**
 * Doc mot mang `parts` cua sach -> Map(so part -> tieu de sach in).
 *
 * JSON OCR dat o CAP BAI HOC (lesson.listening.parts) trong khi loader lai
 * expose qua practice.listening.parts — noi goi da gom san ca hai duong nen o
 * day chi can chuan hoa mot mang. Part nao khong co tieu de that thi KHONG dua
 * vao map — noi goi se tu roi ve tieu de chuan TOEIC.
 *
 * @param {unknown} list
 * @returns {Map<number, string>}
 */
function bookPartTitles(list) {
  const map = new Map();
  if (!Array.isArray(list)) return map;
  for (const entry of list) {
    const n = Number(entry?.part);
    const title = typeof entry?.title === 'string' ? entry.title.trim() : '';
    if (Number.isFinite(n) && n >= 1 && n <= 4 && title) map.set(n, title);
  }
  return map;
}

/**
 * So thu tu cau theo DUNG thu tu in trong sach (khong sap xep lai).
 * Tra ve '' khi khong doc duoc so nao.
 */
function printedOrder(items) {
  return (Array.isArray(items) ? items : [])
    .map((it) => Number(it?.question_num))
    .filter((n) => Number.isFinite(n))
    .join(', ');
}

/** true khi day cau in ra KHONG tang dan (vd lesson_01: 4, 6, 5). */
function isOutOfAscendingOrder(items) {
  const nums = (Array.isArray(items) ? items : [])
    .map((it) => Number(it?.question_num))
    .filter((n) => Number.isFinite(n));
  return nums.some((n, i) => i > 0 && n < nums[i - 1]);
}

function formatTime(seconds) {
  if (!Number.isFinite(seconds) || seconds < 0) return '0:00';
  const total = Math.floor(seconds);
  const m = Math.floor(total / 60);
  const s = total % 60;
  return `${m}:${String(s).padStart(2, '0')}`;
}

function scoreSentence(sc) {
  if (!sc) return '';
  if (sc.total === 0) return 'Chưa có câu nào để chấm';
  return `${sc.correct}/${sc.total} câu đúng`;
}

function clamp01(n) {
  if (!Number.isFinite(n) || n <= 0) return 0;
  return n >= 1 ? 1 : n;
}

function formatDateTime(iso) {
  if (!iso) return '—';
  try {
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return String(iso);
    const pad = (v) => String(v).padStart(2, '0');
    return `${pad(d.getDate())}/${pad(d.getMonth() + 1)}/${d.getFullYear()} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
  } catch {
    return String(iso);
  }
}

/**
 * Tach loi thoai theo luot nguoi noi ([M], [W], [M1], [W1]...) de doc ro rang.
 */
function splitSpeakerTurns(raw) {
  const s = String(raw || '').trim();
  if (!s) return [];
  const normalized = s.replace(/\s*(?=\[(?:M|W|M\d|W\d)\])/g, '\n');
  return normalized
    .split(/\n+/)
    .map((line) => line.trim())
    .filter(Boolean);
}

/* ------------------------------------------------------------------ */
/* Subcomponents                                                       */
/* ------------------------------------------------------------------ */

/** Legend explaining <mark class="vocab-hit"> inside passages and questions. */
function VocabLegend() {
  return null;
}

/* ---------------- Sticky audio player ---------------- */

function AudioPlayer({
  lessonId,
  title,
  subtitle,
  audioUrl,
  tapescriptOpen,
  onTapescriptToggle,
  historyCount = 0,
  historyOpen = false,
  onHistoryToggle,
}) {
  const audioRef = useRef(null);
  const wantsAutoplayRef = useRef(false);

  const [isPlaying, setIsPlaying] = useState(false);
  const [current, setCurrent] = useState(0);
  const [duration, setDuration] = useState(0);
  const [speed, setSpeed] = useState(1);
  const [failed, setFailed] = useState(false);

  /* Transport state is reset by remounting on lesson change — the parent gives
     this component a `key={audioUrl}`, so no reset effect is needed here. */

  /* Apply the chosen playback rate. */
  useEffect(() => {
    const el = audioRef.current;
    if (el) el.playbackRate = speed;
  }, [speed, audioUrl]);

  const togglePlay = useCallback(() => {
    const el = audioRef.current;
    if (!el) return;
    if (el.paused) {
      wantsAutoplayRef.current = true;
      const p = el.play();
      if (p && typeof p.catch === 'function') {
        p.catch(() => {
          wantsAutoplayRef.current = false;
          setIsPlaying(false);
        });
      }
    } else {
      wantsAutoplayRef.current = false;
      el.pause();
    }
  }, []);

  const nudge = useCallback((delta) => {
    const el = audioRef.current;
    if (!el) return;
    const limit = Number.isFinite(el.duration) && el.duration > 0 ? el.duration : Infinity;
    const next = Math.min(Math.max(0, (el.currentTime || 0) + delta), limit);
    try {
      el.currentTime = next;
    } catch {
      /* seeking before metadata is ready — ignore */
    }
    setCurrent(next);
  }, []);

  const seekTo = useCallback(
    (e) => {
      const ratio = clamp01(Number(e.target.value) / 100);
      nudge(ratio * duration - current);
    },
    [current, duration, nudge],
  );

  const progressPct = duration > 0 ? clamp01(current / duration) * 100 : 0;

  return (
    <div className="sticky top-0 z-30 -mx-1 mb-5 rounded-xl border border-[var(--color-duo-line)] bg-[var(--color-duo-bg)]/95 px-3 py-3 shadow-sm backdrop-blur supports-[backdrop-filter]:bg-[var(--color-duo-bg)]/80">
      <div className="flex flex-wrap items-center gap-2">
        <span className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-brand-50 text-brand-700">
          <Volume2 className="h-4 w-4" />
        </span>

        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-semibold text-slate-900">
            {title ? `Bài ${lessonId}: ${title}` : `Bài ${lessonId}`}
          </p>
          <p className="truncate text-[11px] text-slate-500">{subtitle}</p>
        </div>

        <div className="flex flex-wrap items-center gap-1.5">
          <Button
            size="icon"
            variant="secondary"
            onClick={() => nudge(-5)}
            aria-label="Tua lại 5 giây"
            title="Tua lại 5 giây"
          >
            <RotateCcw className="h-4 w-4" />
          </Button>

          <Button
            size="icon"
            variant="primary"
            onClick={togglePlay}
            aria-label={isPlaying ? 'Tạm dừng' : 'Phát'}
            title={isPlaying ? 'Tạm dừng' : 'Phát'}
          >
            {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
          </Button>

          <Button
            size="icon"
            variant="secondary"
            onClick={() => nudge(5)}
            aria-label="Tua tới 5 giây"
            title="Tua tới 5 giây"
          >
            <RotateCw className="h-4 w-4" />
          </Button>

          <div className="ml-1 flex items-center gap-1" role="group" aria-label="Tốc độ phát">
            <Gauge className="h-3.5 w-3.5 text-slate-400" />
            {SPEEDS.map((s) => (
              <button
                key={s}
                type="button"
                onClick={() => setSpeed(s)}
                aria-pressed={speed === s}
                className={`rounded-md px-2 py-1 text-xs font-semibold transition-colors ${
                  speed === s
                    ? 'bg-brand-600 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {s}x
              </button>
            ))}
          </div>

          <Button
            size="sm"
            variant={tapescriptOpen ? 'primary' : 'secondary'}
            onClick={onTapescriptToggle}
            aria-expanded={tapescriptOpen}
            title="Xem tapescript (lời thoại của bài nghe)"
          >
            {tapescriptOpen ? <EyeOff className="h-3.5 w-3.5" /> : <Eye className="h-3.5 w-3.5" />}
            Tapescript
          </Button>

          {onHistoryToggle ? (
            <Button
              size="sm"
              variant={historyOpen ? 'primary' : 'secondary'}
              onClick={onHistoryToggle}
              aria-expanded={historyOpen}
              title="Xem lịch sử làm bài và xem lại đáp án"
            >
              <History className="h-3.5 w-3.5" />
              Lịch sử ({historyCount})
            </Button>
          ) : null}
        </div>
      </div>

      {/* Transport row */}
      <div className="mt-2.5 flex items-center gap-3">
        <span className="w-10 shrink-0 text-right font-mono text-[11px] text-slate-500">
          {formatTime(current)}
        </span>
        <input
          type="range"
          min="0"
          max="100"
          step="0.1"
          value={progressPct}
          onChange={seekTo}
          aria-label="Tiến trình audio"
          className="h-1.5 w-full cursor-pointer appearance-none rounded-full bg-slate-200 accent-brand-600"
        />
        <span className="w-10 shrink-0 font-mono text-[11px] text-slate-500">
          {formatTime(duration)}
        </span>
        <span className="hidden shrink-0 items-center gap-1 text-[11px] text-slate-400 sm:flex">
          <Timer className="h-3 w-3" />
          {speed}x
        </span>
      </div>

      {/* The media element itself lives inside this sticky shell on purpose:
          it is styled invisible so the branded transport above is the only UI. */}
      <audio
        ref={audioRef}
        key={audioUrl}
        src={audioUrl}
        preload="metadata"
        className="hidden"
        onLoadedMetadata={(e) => {
          const el = e.currentTarget;
          el.playbackRate = speed;
          setDuration(Number.isFinite(el.duration) ? el.duration : 0);
          if (wantsAutoplayRef.current) {
            const p = el.play();
            if (p && typeof p.catch === 'function') p.catch(() => setIsPlaying(false));
          }
        }}
        onTimeUpdate={(e) => setCurrent(e.currentTarget.currentTime || 0)}
        onDurationChange={(e) =>
          setDuration(Number.isFinite(e.currentTarget.duration) ? e.currentTarget.duration : 0)
        }
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
        onEnded={() => {
          setIsPlaying(false);
          wantsAutoplayRef.current = false;
        }}
        onError={() => {
          setFailed(true);
          setIsPlaying(false);
        }}
      />

      {failed ? (
        <p className="mt-2 rounded-lg bg-rose-50 px-3 py-2 text-xs text-rose-700">
          Không tải được file audio của bài này. Hãy chắc chắn file tồn tại tại{' '}
          <code className="font-mono">{audioUrl}</code> trong thư mục <code>public/</code>.
        </p>
      ) : null}
    </div>
  );
}

/* ---------------- Tapescript panel ---------------- */

const TAPESCRIPT_PARTS = [
  { key: 'part1', label: 'Part 1: Photo', hint: 'Câu 1', tone: 'sky' },
  { key: 'part2', label: 'Part 2: Question-Response', hint: 'Câu 2–3', tone: 'violet' },
  { key: 'part3', label: 'Part 3: Conversation', hint: 'Câu 4–6', tone: 'brand' },
  { key: 'part4', label: 'Part 4: Talk', hint: 'Câu 7–9', tone: 'emerald' },
];

function TapescriptPanel({ available, tapescriptObj, text, words }) {
  const partBlocks = useMemo(() => {
    if (!tapescriptObj || typeof tapescriptObj !== 'object') return [];
    return TAPESCRIPT_PARTS.filter((p) => hasText(tapescriptObj[p.key])).map((p) => ({
      ...p,
      content: String(tapescriptObj[p.key]).trim(),
      lines: splitSpeakerTurns(tapescriptObj[p.key]),
    }));
  }, [tapescriptObj]);

  return (
    <div className="mb-5 rounded-xl border border-slate-200 bg-white shadow-sm">
      <div className="flex items-center justify-between gap-3 border-b border-slate-200 px-4 py-2.5">
        <SectionTitle
          icon={FileText}
          title="Tapescript"
          subtitle="Lời thoại của phần nghe (tự động tô vàng từ vựng trọng tâm)"
          right={
            available ? (
              <Badge tone="emerald">Có dữ liệu</Badge>
            ) : (
              <Badge tone="amber">Chưa có dữ liệu</Badge>
            )
          }
        />
      </div>
      <div className="px-4 py-3">
        {available ? (
          partBlocks.length > 0 ? (
            <div className="grid gap-3">
              {partBlocks.map((blk) => (
                <div
                  key={blk.key}
                  className="rounded-xl border border-slate-200 bg-slate-50/70 p-3.5"
                >
                  <div className="mb-2 flex items-center justify-between gap-2">
                    <Badge tone={blk.tone}>{blk.label}</Badge>
                    <span className="text-xs font-semibold text-slate-500">{blk.hint}</span>
                  </div>
                  <div className="space-y-1.5 text-sm leading-relaxed text-slate-700">
                    {blk.lines.map((line, idx) => {
                      const speakerMatch = line.match(/^(\[(?:M|W|M\d|W\d)\])\s*(.*)$/);
                      if (speakerMatch) {
                        return (
                          <p key={idx} className="whitespace-pre-line">
                            <span className="mr-1.5 inline-block rounded bg-brand-100 px-1.5 py-0.5 font-mono text-xs font-bold text-brand-800">
                              {speakerMatch[1]}
                            </span>
                            <Highlighted text={speakerMatch[2]} words={words} />
                          </p>
                        );
                      }
                      return (
                        <p key={idx} className="whitespace-pre-line">
                          <Highlighted text={line} words={words} />
                        </p>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="whitespace-pre-line text-sm leading-relaxed text-slate-700">
              <Highlighted text={tapescriptObj?.fullText || text} words={words} />
            </p>
          )
        ) : (
          <div className="rounded-lg border border-dashed border-slate-300 bg-slate-50 px-4 py-6 text-center">
            <p className="text-sm font-medium text-slate-600">{TAPESCRIPT_ABSENT}</p>
            <p className="mt-1 text-xs text-slate-500">
              Dữ liệu OCR của bài này chưa có phần lời thoại. Bạn vẫn có thể làm bài và tự đối
              chiếu với phần Answer Key / Tapescript ở cuối sách giấy.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

/* ---------------- Practice History panel ---------------- */

function PracticeHistoryPanel({
  lessonId,
  historyList,
  lessonHistory,
  filterMode,
  onFilterChange,
  onReviewAttempt,
  onDeleteItem,
  onClearLesson,
  onClearAll,
}) {
  const displayed = filterMode === 'all' ? historyList : lessonHistory;

  return (
    <Card className="mb-5 overflow-hidden" flat>
      <div className="flex flex-wrap items-center justify-between gap-3 border-b-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] px-4 py-3">
        <div className="flex items-center gap-2.5">
          <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand-50 text-brand-700">
            <History className="h-5 w-5" />
          </span>
          <div>
            <h3 className="text-sm font-extrabold text-[var(--color-duo-ink)]">
              Lịch sử làm bài (Practice History)
            </h3>
            <p className="text-xs font-medium text-[var(--color-duo-gray)]">
              Lưu tự động mỗi lần nộp bài · Xem lại đáp án đã chọn hoặc tùy biến xóa từng lần làm
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="inline-flex rounded-xl border border-slate-200 bg-white p-0.5">
            <button
              type="button"
              onClick={() => onFilterChange('lesson')}
              className={`rounded-lg px-2.5 py-1 text-xs font-bold transition-colors ${
                filterMode === 'lesson'
                  ? 'bg-brand-600 text-white'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              Bài học này (Bài {lessonId}) ({lessonHistory.length})
            </button>
            <button
              type="button"
              onClick={() => onFilterChange('all')}
              className={`rounded-lg px-2.5 py-1 text-xs font-bold transition-colors ${
                filterMode === 'all'
                  ? 'bg-brand-600 text-white'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              Tất cả các bài ({historyList.length})
            </button>
          </div>

          {lessonHistory.length > 0 ? (
            <Button
              size="sm"
              variant="secondary"
              onClick={onClearLesson}
              title={`Xóa toàn bộ lịch sử làm bài của Bài ${lessonId}`}
            >
              <Trash2 className="h-3.5 w-3.5" />
              Xóa lịch sử bài này
            </Button>
          ) : null}

          {historyList.length > 0 ? (
            <Button
              size="sm"
              variant="danger"
              onClick={onClearAll}
              title="Xóa toàn bộ lịch sử làm bài của tất cả các bài"
            >
              <Trash2 className="h-3.5 w-3.5" />
              Xóa toàn bộ lịch sử
            </Button>
          ) : null}
        </div>
      </div>

      <div className="px-4 py-3">
        {displayed.length === 0 ? (
          <p className="rounded-xl border border-dashed border-slate-200 bg-slate-50 px-4 py-5 text-center text-xs font-medium text-slate-500">
            {filterMode === 'lesson'
              ? `Chưa có lịch sử làm bài nào cho Bài ${lessonId}. Hãy chọn đáp án và bấm “Nộp bài & Chấm điểm” để lưu kết quả.`
              : 'Chưa có lịch sử làm bài nào được lưu trên máy bạn.'}
          </p>
        ) : (
          <div className="grid gap-2.5">
            {displayed.map((item, idx) => {
              const keyId = item.id || item.at || String(idx);
              const total = Number(item.total) || 0;
              const correct = Number(item.correct) || 0;
              const pct = total > 0 ? Math.round((correct / total) * 100) : 0;
              const badgeTone = pct >= 80 ? 'emerald' : pct >= 50 ? 'amber' : 'rose';
              const isCurrentLesson = Number(item.lessonId) === Number(lessonId);
              const canReview =
                isCurrentLesson &&
                item.userAnswers &&
                typeof item.userAnswers === 'object' &&
                Object.keys(item.userAnswers).length > 0;
              const sc = item.scores && typeof item.scores === 'object' ? item.scores : null;

              return (
                <div
                  key={keyId}
                  className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 shadow-xs"
                >
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="inline-flex items-center gap-1 text-xs font-bold text-slate-700">
                        <Clock className="h-3.5 w-3.5 text-slate-400" />
                        {formatDateTime(item.at)}
                      </span>
                      <span className="text-xs font-extrabold text-slate-900">
                        Bài {item.lessonId}
                        {item.lessonTitle ? `: ${item.lessonTitle}` : ''}
                      </span>
                      <Badge tone={badgeTone}>
                        {correct}/{total} câu đúng · {pct}%
                      </Badge>
                    </div>

                    {sc ? (
                      <div className="mt-1 flex flex-wrap gap-x-3 gap-y-1 text-[11px] font-medium text-slate-500">
                        {sc[SEC_LISTENING] ? (
                          <span>
                            Listening: <strong>{sc[SEC_LISTENING].correct}/{sc[SEC_LISTENING].total}</strong>
                          </span>
                        ) : null}
                        {sc[SEC_PART5] ? (
                          <span>
                            Part 5: <strong>{sc[SEC_PART5].correct}/{sc[SEC_PART5].total}</strong>
                          </span>
                        ) : null}
                        {sc[SEC_PART6] ? (
                          <span>
                            Part 6: <strong>{sc[SEC_PART6].correct}/{sc[SEC_PART6].total}</strong>
                          </span>
                        ) : null}
                        {sc[SEC_PART7] ? (
                          <span>
                            Part 7: <strong>{sc[SEC_PART7].correct}/{sc[SEC_PART7].total}</strong>
                          </span>
                        ) : null}
                      </div>
                    ) : null}
                  </div>

                  <div className="flex items-center gap-2">
                    {canReview ? (
                      <Button
                        size="sm"
                        variant="secondary"
                        onClick={() => onReviewAttempt(item)}
                        title="Tải lại các đáp án đã chọn trong lần làm này và xem giải thích"
                      >
                        <Eye className="h-3.5 w-3.5" />
                        Xem lại bài làm
                      </Button>
                    ) : !isCurrentLesson ? (
                      <span className="text-[11px] italic text-slate-400">
                        Mở Bài {item.lessonId} để xem lại
                      </span>
                    ) : null}

                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => onDeleteItem(item.id || item.at)}
                      aria-label="Xóa lần làm bài này"
                      title="Xóa lần làm bài này"
                    >
                      <Trash2 className="h-4 w-4 text-rose-600" />
                      Xóa
                    </Button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </Card>
  );
}

/* ---------------- Choice primitives ---------------- */

/**
 * One selectable answer row.
 * @param {object} props
 * @param {boolean} props.revealText Part 2 keeps the option text hidden until submit.
 */
function OptionButton({
  letter,
  text,
  selected,
  onSelect,
  revealText = true,
  disabled = false,
  correctLetter = null,
  showVerdict = false,
}) {
  const hasOptionText = hasText(text);
  const isCorrect = normalizeLetter(correctLetter) === letter;

  /*
   * Thẻ lựa chọn kiểu Duolingo — 4 trạng thái màu:
   *   thường  : trắng, viền xám, bóng cứng 2px
   *   hover   : nền xanh dương nhạt
   *   đã chọn : viền + nền xanh dương nhạt
   *   đúng    : viền xanh lá + nền #D7FFB8
   *   sai     : viền đỏ + nền #FFDFE0
   * Class nằm trong index.css (.duo-choice*) nên SSR render ra markup ổn định.
   */
  const tone = showVerdict
    ? isCorrect
      ? 'duo-choice-correct'
      : selected
        ? 'duo-choice-wrong'
        : ''
    : selected
      ? 'duo-choice-selected'
      : '';

  return (
    <button
      type="button"
      disabled={disabled}
      onClick={() => onSelect(letter)}
      aria-pressed={selected}
      className={`duo-choice ${tone}`}
    >
      <span className="duo-choice-badge">{letter}</span>

      {!revealText ? (
        <span className="text-xs italic opacity-60">
          Nội dung lựa chọn chỉ nghe được trong audio
        </span>
      ) : hasOptionText ? (
        <span className="min-w-0 flex-1">{text}</span>
      ) : (
        <span className="text-xs italic opacity-60">
          (Chưa có nội dung lựa chọn trong dữ liệu)
        </span>
      )}

      {showVerdict && isCorrect ? (
        <CircleCheck className="ml-auto h-5 w-5 shrink-0" />
      ) : null}
      {showVerdict && !isCorrect && selected ? (
        <CircleX className="ml-auto h-5 w-5 shrink-0" />
      ) : null}
    </button>
  );
}

/** A question block: stem, options, verdict line and a missing-answer note. */
function QuestionCard({
  questionNum,
  stemNode,
  options,
  selected,
  onSelect,
  graded,
  answer,
  hasAnswer,
  helpNote,
  revealText = true,
  explanation = null,
  children,
}) {
  const letters = lettersOf(options);
  const chosen = normalizeLetter(selected);
  const correct = normalizeLetter(answer);
  const isCorrect = graded && hasAnswer && chosen !== null && chosen === correct;

  return (
    <Card className="p-5">
      <div className="mb-3 flex items-center gap-2">
        <span className="inline-flex h-7 min-w-7 items-center justify-center rounded-xl bg-[var(--color-duo-green)] px-2 text-xs font-extrabold text-white shadow-[0_2px_0_0_var(--color-duo-green-dark)]">
          {questionNum}
        </span>
        {graded && hasAnswer ? (
          isCorrect ? (
            <Badge tone="emerald">
              <CircleCheck className="h-3 w-3" /> Đúng
            </Badge>
          ) : (
            <Badge tone="rose">
              <CircleX className="h-3 w-3" /> {chosen ? 'Sai' : 'Chưa chọn'}
            </Badge>
          )
        ) : null}
        {graded && !hasAnswer ? <Badge tone="amber">Tự chấm theo Answer Key</Badge> : null}
      </div>

      {stemNode ? (
        <div className="mb-4 text-[15px] font-semibold leading-relaxed text-[var(--color-duo-ink)]">
          {stemNode}
        </div>
      ) : null}

      {letters.length ? (
        <div className="grid gap-2.5">
          {letters.map((letter) => (
            <OptionButton
              key={letter}
              letter={letter}
              text={options?.[letter]}
              selected={chosen === letter}
              onSelect={onSelect}
              revealText={revealText}
              correctLetter={graded ? answer : null}
              showVerdict={graded && hasAnswer}
            />
          ))}
        </div>
      ) : (
        <p className="rounded-xl bg-[var(--color-duo-bg-soft)] px-3 py-2 text-xs font-medium text-[var(--color-duo-gray)]">
          Câu này chưa có dữ liệu lựa chọn trong bài học.
        </p>
      )}

      {children}

      {graded && hasAnswer ? (
        <p className="mt-3 text-xs font-bold text-[#3f7d00]">
          Đáp án đúng: <span className="font-extrabold">{correct}</span>
          {hasText(options?.[correct]) ? ` — ${options[correct]}` : ''}
          {chosen === null ? ' · Bạn chưa chọn đáp án cho câu này.' : ''}
        </p>
      ) : null}

      {graded && !hasAnswer ? (
        <p className="mt-3 rounded-xl bg-[#fff4cc] px-3 py-2 text-xs font-semibold text-[#8a6d00]">
          {LISTENING_MISSING_ANSWER_NOTE}
        </p>
      ) : null}

      {/*
        Giai thich tung cau: chi hien SAU KHI nop bai (giong Duolingo — khong
        de lo dap an khi dang lam). explanation = { why, option_notes, evidence,
        source } do scripts/build_explanations.py sinh ra tu du lieu that.
      */}
      {graded && explanation ? (
        <div className="duo-explain">
          <div className="duo-explain-head">
            <Lightbulb className="h-4 w-4" />
            <span>Giải thích câu này</span>
          </div>

          <div className="duo-explain-why">{renderExplain(explanation.why)}</div>

          {explanation.evidence ? (
            <div className="duo-explain-evidence">
              <span className="duo-explain-evidence-tag">
                {explanation.source === 'tapescript' ? 'Lời thoại trong sách' : 'Dẫn chứng trong bài đọc'}
              </span>
              <span className="italic">“{explanation.evidence}”</span>
            </div>
          ) : null}

          {explanation.option_notes && Object.keys(explanation.option_notes).length ? (
            <div className="duo-explain-notes">
              <p className="duo-explain-notes-title">Vì sao các phương án khác không đúng</p>
              <ul>
                {Object.entries(explanation.option_notes)
                  .sort(([a], [b]) => a.localeCompare(b))
                  .map(([lab, note]) => (
                    <li key={lab}>
                      <span className="duo-explain-lab">{lab}</span>
                      <span>{renderExplain(note.replace(/^\([A-D]\)\s*/, ''))}</span>
                    </li>
                  ))}
              </ul>
            </div>
          ) : null}
        </div>
      ) : null}

      {helpNote ? (
        <p className="mt-2 text-[11px] font-medium text-[var(--color-duo-muted)]">{helpNote}</p>
      ) : null}
    </Card>
  );
}

/** Compact chip strip for the Part 2 questions (A/B/C only, no text). */
function Part2Picker({ questionNum, letters, selected, onSelect, graded }) {
  return (
    <div className="flex items-center gap-2">
      <span className="inline-flex h-7 min-w-7 items-center justify-center rounded-xl bg-[var(--color-duo-green)] px-2 text-xs font-extrabold text-white shadow-[0_2px_0_0_var(--color-duo-green-dark)]">
        {questionNum}
      </span>
      {letters.map((letter) => {
        const active = normalizeLetter(selected) === letter;
        return (
          <button
            key={letter}
            type="button"
            onClick={() => onSelect(letter)}
            aria-pressed={active}
            className={`h-10 w-10 rounded-2xl border-2 text-sm font-extrabold transition-all ${
              active
                ? 'border-[var(--color-duo-blue)] bg-[var(--color-duo-blue)] text-white shadow-[0_3px_0_0_var(--color-duo-blue-dark)]'
                : 'border-[var(--color-duo-line)] bg-white text-[var(--color-duo-gray)] shadow-[0_3px_0_0_var(--color-duo-line)] hover:border-[var(--color-duo-blue)] hover:text-[var(--color-duo-blue)]'
            }`}
          >
            {letter}
          </button>
        );
      })}
      {graded ? (
        <span className="text-xs font-semibold text-[var(--color-duo-gray)]">
          {normalizeLetter(selected) ? `Bạn chọn ${normalizeLetter(selected)}` : 'Bạn chưa chọn'}
        </span>
      ) : null}
    </div>
  );
}

/* ---------------- Listening sections ---------------- */

function Part1({ data, selected, onSelect, graded, photoUrl }) {
  // Hooks must run unconditionally, before the missing-data branch below.
  // `imgFailed` is keyed to the current photo URL so a failed image of another
  // lesson can never leak into this one — no reset effect required.
  const [failedSrc, setFailedSrc] = useState(null);
  const imgFailed = failedSrc === photoUrl;

  if (!data) {
    return (
      <Card className="p-4">
        <p className="text-sm text-slate-500">
          Chưa có dữ liệu Part 1 (câu 1) cho bài này.
        </p>
      </Card>
    );
  }

  const questionNum = data.question_num ?? 1;

  return (
    <Card className="p-4">
      <div className="mb-3 flex items-center gap-2">
        <span className="inline-flex h-6 min-w-6 items-center justify-center rounded-md bg-slate-900 px-1.5 text-xs font-bold text-white">
          {questionNum}
        </span>
        <Badge tone="sky">Part 1 — Mô tả tranh</Badge>
        {graded ? <Badge tone="amber">Tự chấm theo Answer Key</Badge> : null}
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <figure className="overflow-hidden rounded-xl border border-slate-200 bg-slate-50">
          {imgFailed ? (
            <div className="flex h-44 flex-col items-center justify-center gap-2 px-4 text-center">
              <ImageIcon className="h-8 w-8 text-slate-300" />
              <p className="text-xs text-slate-500">
                Không tải được ảnh của bài này. Kiểm tra file <code>{photoUrl}</code> trong thư mục{' '}
                <code>public/part1_photos/</code>.
              </p>
            </div>
          ) : (
            <img
              src={photoUrl}
              alt={`Ảnh minh họa cho câu ${questionNum}`}
              loading="lazy"
              className="h-auto max-h-80 w-full object-contain"
              onError={() => setFailedSrc(photoUrl)}
            />
          )}
          <figcaption className="border-t border-slate-200 bg-white px-3 py-2 text-[11px] text-slate-500">
            Ảnh minh họa câu {questionNum} · {data.photo || photoUrl}
          </figcaption>
        </figure>

        <div>
          <p className="mb-2 text-sm text-slate-700">
            Chọn mô tả đúng nhất với bức ảnh (A/B/C/D).
          </p>

          <div className="grid gap-1.5">
            {CHOICE_LETTERS.map((letter) => (
              <OptionButton
                key={letter}
                letter={letter}
                text={null}
                selected={normalizeLetter(selected) === letter}
                onSelect={onSelect}
                revealText={false}
              />
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
}

/**
 * Mot part NGHE hien thi thanh mot MUC RIENG: badge "Part N — <tieu de sach>"
 * + khoang cau hoi cua part do.
 *
 * - `partNum` / `title`: tieu de lay tu `listening.parts` cua sach, roi ve tieu
 *   chuan TOEIC khi sach khong in tieu de.
 * - `emptyNote`: cau tieng Viet noi DUNG su that cua bai (khac nhau giua bai
 *   chi co anh Part 1 va bai thieu du lieu).
 * - Thu tu cau giu NGUYEN nhu sach in; hien ghi chu khi thu tu khong tang dan.
 */
function Part3({ items, answers, onSelect, graded, words, partNum = 3, title, emptyNote }) {
  const list = Array.isArray(items) ? items : [];
  const range = partNum === 4 ? 'câu 7-9' : 'câu 4-6';
  const heading = `Part ${partNum} — ${title} (${range})`;

  if (!list.length) {
    return (
      <Card className="p-4">
        <div className="mb-2 flex items-center gap-2">
          <Badge tone="sky">{heading}</Badge>
        </div>
        <p className="text-sm text-slate-500">{emptyNote}</p>
      </Card>
    );
  }

  const order = printedOrder(list);
  const shuffled = isOutOfAscendingOrder(list);

  return (
    <div className="grid gap-3">
      <div className="flex flex-wrap items-center gap-2">
        <Badge tone="sky">{heading}</Badge>
        {graded ? <Badge tone="amber">Tự chấm theo Answer Key</Badge> : null}
        <span className="text-xs text-slate-500">{list.length} câu</span>
      </div>

      {list.map((item) => {
        const num = item.question_num;
        const options = item.options || {};
        const answer = item.answer;
        return (
          <QuestionCard
            key={num}
            questionNum={num}
            stemNode={
              hasText(item.question) ? (
                <Highlighted text={item.question} words={words} />
              ) : (
                <span className="italic text-slate-400">
                  (Câu hỏi không có nội dung trong dữ liệu — nghe trong audio)
                </span>
              )
            }
            options={options}
            selected={answers[num]}
            onSelect={(letter) => onSelect(num, letter)}
            graded={graded}
            answer={answer}
            hasAnswer={Boolean(normalizeLetter(answer))}
            explanation={item.explanation}
            helpNote={
              hasText(item.transcript) || hasText(item.group)
                ? [item.group, item.transcript].filter(hasText).join(' · ')
                : null
            }
          />
        );
      })}
    </div>
  );
}

function ListeningSection({
  lessonId,
  listening,
  answers,
  onSelect,
  graded,
  words,
  tapescriptOpen,
  parts = [],
}) {
  const { part1, part2, part3, part4 } = listening;
  const part2Items = part2.length
    ? part2.map((p, i) => ({ ...p, question_num: p.question_num ?? 2 + i }))
    : [2, 3].map((n) => ({ question_num: n, options: ['A', 'B', 'C'] }));

  /*
   * Tieu de lay tu chinh metadata cua sach (`listening.parts`), roi ve tieu de
   * chuan TOEIC khi sach khong in. Thanh phu cua tieu de muc cung duoc SUY RA
   * tu day thay vi hard-code "Part 1 · Part 2 · Part 3 · Part 4".
   */
  const partList = Array.isArray(parts) ? parts : [];
  const bookTitles = useMemo(() => bookPartTitles(partList), [partList]);
  const titleOf = (n) => bookTitles.get(n) || TOEIC_PART_TITLE[n] || `Part ${n}`;

  const partSubtitle = useMemo(() => {
    const nums = [1, 2, 3, 4];
    const hasAllTitles = nums.every((n) => bookTitles.has(n));
    if (hasAllTitles) {
      // Sach co day du 4 tieu de -> in dung tieu de sach, ngan gon.
      return nums.map((n) => `Part ${n} ${bookTitles.get(n)}`).join(' · ');
    }
    return nums.map((n) => PART_TITLE_VI[n]).join(' · ');
  }, [bookTitles]);

  /*
   * Su that cua du lieu: 13/50 bai co chu phan nghe, 37 bai con lai trang
   * luyen nghe CHI co anh Part 1 (file listening_practice.md rong 0 byte).
   * Vi vay cau trong state phai noi ro nguyen nhan, khong ham y "loi du lieu".
   */
  const hasAnyListeningText = Boolean(part3.length || part4.length);
  const photoOnlyNote = hasAnyListeningText
    ? ''
    : 'Bài này trang luyện nghe chỉ có ảnh Part 1 — sách không in câu hỏi Part 3/Part 4.';

  return (
    <section className="mb-6">
      <SectionTitle
        icon={Headphones}
        title="Listening (1-9)"
        right={<Badge tone="sky">9 câu</Badge>}
      />

      <div className="grid gap-4">
        <Part1
          data={part1}
          selected={answers[part1?.question_num ?? 1]}
          onSelect={(letter) => onSelect(part1?.question_num ?? 1, letter)}
          graded={graded}
          photoUrl={photoUrlFor(lessonId)}
        />

        {/* Part 2 — text intentionally hidden until submit */}
        <Card className="p-4">
          <div className="mb-2 flex items-center gap-2">
            <Badge tone="violet">Part 2 — Hỏi &amp; Đáp</Badge>
            {graded ? <Badge tone="amber">Tự chấm theo Answer Key</Badge> : null}
          </div>
          <p className="mb-3 text-sm text-slate-700">
            Nghe câu hỏi và chọn câu trả lời đúng (A/B/C).
          </p>

          <div className="grid gap-3">
            {part2Items.map((item) => (
              <Part2Picker
                key={item.question_num}
                questionNum={item.question_num}
                letters={lettersOf(item.options).length ? lettersOf(item.options) : ['A', 'B', 'C']}
                selected={answers[item.question_num]}
                onSelect={(letter) => onSelect(item.question_num, letter)}
                graded={graded}
              />
            ))}
          </div>

          {/*
            Chi hien canh bao khi THUC SU thieu dap an. Truoc day dong nay hien
            vo dieu kien, nen sau khi noi Answer Key vao van bao "chua co dap an"
            ngay duoi mot cau DA duoc cham — vua sai vua lam nguoi hoc hoang mang.
          */}
          {graded && part2.some((q) => !normalizeLetter(q.answer)) ? (
            <p className="mt-2 text-xs font-medium text-amber-800">{LISTENING_MISSING_ANSWER_NOTE}</p>
          ) : null}
        </Card>

        {/* Part 3 — Conversation: mot muc RIENG, dung tieu de sach in. */}
        <Part3
          items={part3}
          answers={answers}
          onSelect={onSelect}
          graded={graded}
          words={words}
          partNum={3}
          title={titleOf(3)}
          emptyNote={photoOnlyNote}
        />
        {/* Part 4 — Talk: mot muc RIENG, dung tieu de sach in. */}
        <Part3
          items={part4}
          answers={answers}
          onSelect={onSelect}
          graded={graded}
          words={words}
          partNum={4}
          title={titleOf(4)}
          emptyNote={photoOnlyNote}
        />
      </div>
    </section>
  );
}

/* ---------------- Reading sections ---------------- */

function Part5({ items, answers, onSelect, graded, words }) {
  return (
    <section className="mb-6">
      <SectionTitle
        icon={PenLine}
        title="PART 5 — Điền vào chỗ trống (Câu 10-15)"
        subtitle="Chọn từ đúng để hoàn thành câu"
        right={<Badge tone="brand">{items.length} câu</Badge>}
      />

      {items.length ? (
        <div className="grid gap-3">
          {items.map((item) => {
            const num = item.question_num;
            const answer = item.answer;
            return (
              <QuestionCard
                key={num}
                questionNum={num}
                stemNode={
                  <p className="whitespace-pre-line leading-relaxed">
                    <Highlighted text={item.sentence || ''} words={words} />
                  </p>
                }
                options={item.options || {}}
                selected={answers[num]}
                onSelect={(letter) => onSelect(num, letter)}
                graded={graded}
                answer={answer}
                hasAnswer={Boolean(normalizeLetter(answer))}
                explanation={item.explanation}
              />
            );
          })}
        </div>
      ) : (
        <EmptyState
          icon={PenLine}
          title="Chưa có dữ liệu Part 5"
          description="Bài học này chưa có phần Part 5 (câu 10-15) trong dữ liệu."
        />
      )}
    </section>
  );
}

/**
 * Renders the Part 6 passage EXACTLY as stored, keeping the literal [16]/[17]/[18]
 * markers in their original positions, and attaches each question's options to
 * the matching marker (as a sub-card under the paragraph that contains it).
 */
function Part6({ data, answers, onSelect, graded, words }) {
  const questions = useMemo(
    () => (Array.isArray(data?.questions) ? data.questions : []),
    [data],
  );

  const passage = typeof data?.passage === 'string' ? data.passage : '';

  /** Split the passage so each [NN] marker becomes its own segment. */
  const segments = useMemo(() => {
    if (!passage) return [];
    const re = /\[(\d{1,3})\]/g;
    const out = [];
    let last = 0;
    let m;
    while ((m = re.exec(passage)) !== null) {
      if (m.index > last) out.push({ kind: 'text', text: passage.slice(last, m.index) });
      out.push({ kind: 'blank', num: Number(m[1]), raw: m[0] });
      last = m.index + m[0].length;
      if (m[0].length === 0) re.lastIndex += 1;
    }
    if (last < passage.length) out.push({ kind: 'text', text: passage.slice(last) });
    return out;
  }, [passage]);

  if (!data) {
    return (
      <section className="mb-6">
        <SectionTitle icon={BookOpen} title="PART 6 — Đọc hiểu đoạn văn (Câu 16-18)" />
        <EmptyState
          icon={BookOpen}
          title="Chưa có dữ liệu Part 6"
          description="Bài học này chưa có đoạn văn và câu hỏi Part 6 trong dữ liệu."
        />
      </section>
    );
  }

  const markers = segments.filter((s) => s.kind === 'blank');
  const matched = new Set();

  return (
    <section className="mb-6">
      <SectionTitle
        icon={BookOpen}
        title="PART 6 — Đọc hiểu đoạn văn (Câu 16-18)"
        subtitle={hasText(data.title) ? data.title : undefined}
        right={<Badge tone="brand">{questions.length} câu</Badge>}
      />

      <Card className="mb-3 p-4">
        <p className="mb-3 text-xs text-slate-500">
          Đoạn văn được giữ nguyên như trong sách. Các ô <strong>[16] [17] [18]</strong> là vị trí
          cần điền; lựa chọn của từng câu nằm ngay bên dưới đoạn chứa ô đó.
        </p>
        <div className="whitespace-pre-line text-sm leading-relaxed text-slate-800">
          {segments.length ? (
            segments.map((seg, i) => {
              if (seg.kind === 'text') {
                return <Highlighted key={i} text={seg.text} words={words} />;
              }
              const q = questions.find((item) => Number(item.question_num) === seg.num);
              const chosen = q ? normalizeLetter(answers[q.question_num]) : null;
              return (
                <span key={i} className="inline-flex items-center gap-1 align-baseline">
                  <span
                    className={`cloze-blank ${
                      graded && q
                        ? chosen && normalizeLetter(q.answer) === chosen
                          ? '!border-emerald-500 !text-emerald-700'
                          : '!border-rose-500 !text-rose-700'
                        : ''
                    }`}
                  >
                    {seg.raw}
                  </span>
                  {q && graded ? (
                    <span className="text-[11px] font-bold text-emerald-700">
                      = {normalizeLetter(q.answer) || '?'}
                    </span>
                  ) : null}
                </span>
              );
            })
          ) : (
            <span className="italic text-slate-400">(Đoạn văn trống)</span>
          )}
        </div>
      </Card>

      <div className="grid gap-3">
        {questions.length ? (
          questions.map((q) => {
            matched.add(Number(q.question_num));
            return (
              <QuestionCard
                key={q.question_num}
                questionNum={q.question_num}
                stemNode={
                  <span className="text-slate-600">
                    Chọn từ thích hợp để điền vào ô <strong>[{q.question_num}]</strong>.
                  </span>
                }
                options={q.options || {}}
                selected={answers[q.question_num]}
                onSelect={(letter) => onSelect(q.question_num, letter)}
                graded={graded}
                answer={q.answer}
                hasAnswer={Boolean(normalizeLetter(q.answer))}
                explanation={q.explanation}
              />
            );
          })
        ) : (
          <p className="rounded-lg bg-slate-50 px-3 py-2 text-sm text-slate-500">
            Chưa có câu hỏi cho Part 6.
          </p>
        )}
      </div>

      {markers.some((m) => !matched.has(m.num)) ? (
        <p className="mt-2 rounded-lg bg-amber-50 px-3 py-2 text-xs text-amber-800">
          Một số ô trong đoạn văn (
          {markers
            .filter((m) => !matched.has(m.num))
            .map((m) => m.raw)
            .join(', ')}
          ) chưa có câu hỏi tương ứng trong dữ liệu.
        </p>
      ) : null}
    </section>
  );
}

/** One document (letter / form / memo / email) styled by its `type`. */
function PassageDocument({ passage, index }) {
  const type = String(passage?.type || '').toLowerCase();
  const label = PASSAGE_TYPE_LABEL[type] || (type ? type.toUpperCase() : 'TÀI LIỆU');

  const bodyFont = type === 'form' || type === 'memo' ? 'font-mono' : '';

  return (
    <Card className="mb-3 overflow-hidden">
      <div className="flex items-center justify-between gap-2 border-b border-slate-200 bg-slate-50 px-4 py-2">
        <Badge tone={type === 'form' ? 'violet' : type === 'letter' ? 'brand' : 'slate'}>
          Tài liệu {index + 1} · {label}
        </Badge>
      </div>

      {hasText(passage?.header) ? (
        <div className="border-b border-slate-200 bg-white px-4 py-3">
          <p className="whitespace-pre-line text-sm font-semibold leading-relaxed text-slate-900">
            {passage.header}
          </p>
        </div>
      ) : null}

      <div className="px-4 py-3">
        {hasText(passage?.body) ? (
          <p
            className={`whitespace-pre-line text-sm leading-relaxed text-slate-700 ${bodyFont}`}
          >
            {passage.body}
          </p>
        ) : (
          <p className="text-sm italic text-slate-400">(Tài liệu trống)</p>
        )}
      </div>
    </Card>
  );
}

function Part7SplitView({ data, answers, onSelect, graded, words }) {
  const passages = Array.isArray(data?.passages) ? data.passages : [];
  const questions = Array.isArray(data?.questions) ? data.questions : [];

  return (
    <section className="mb-6">
      <SectionTitle
        icon={ListChecks}
        title="PART 7 — Đọc hiểu tài liệu (Câu 19-23)"
        subtitle="Màn hình chia đôi: bên trái là tài liệu, bên phải là câu hỏi"
        right={<Badge tone="brand">{questions.length} câu</Badge>}
      />

      {passages.length || questions.length ? (
        <div className="grid gap-4 lg:grid-cols-2">
          {/* LEFT — documents */}
          <div className="split-pane lg:max-h-[36rem] lg:overflow-y-auto lg:pr-3">
            <div className="mb-2 flex items-center gap-2">
              <FileText className="h-4 w-4 text-brand-600" />
              <h4 className="text-sm font-bold text-slate-800">Tài liệu</h4>
              <Badge tone="slate">{passages.length} văn bản</Badge>
            </div>
            {passages.length ? (
              passages.map((p, i) => <PassageDocument key={i} passage={p} index={i} />)
            ) : (
              <Card className="p-4">
                <p className="text-sm text-slate-500">Chưa có tài liệu cho Part 7.</p>
              </Card>
            )}
          </div>

          {/* RIGHT — questions */}
          <div className="split-pane lg:max-h-[36rem] lg:overflow-y-auto lg:border-l lg:border-slate-200 lg:pl-4">
            <div className="mb-2 flex items-center gap-2">
              <ListChecks className="h-4 w-4 text-brand-600" />
              <h4 className="text-sm font-bold text-slate-800">Câu hỏi</h4>
              <Badge tone="slate">{questions.length} câu</Badge>
            </div>
            {questions.length ? (
              <div className="grid gap-3">
                {questions.map((q) => (
                  <QuestionCard
                    key={q.question_num}
                    questionNum={q.question_num}
                    stemNode={<Highlighted text={q.question || ''} words={words} />}
                    options={q.options || {}}
                    selected={answers[q.question_num]}
                    onSelect={(letter) => onSelect(q.question_num, letter)}
                    graded={graded}
                    answer={q.answer}
                    hasAnswer={Boolean(normalizeLetter(q.answer))}
                    explanation={q.explanation}
                  />
                ))}
              </div>
            ) : (
              <Card className="p-4">
                <p className="text-sm text-slate-500">Chưa có câu hỏi cho Part 7.</p>
              </Card>
            )}
          </div>
        </div>
      ) : (
        <EmptyState
          icon={ListChecks}
          title="Chưa có dữ liệu Part 7"
          description="Bài học này chưa có tài liệu và câu hỏi Part 7 trong dữ liệu."
        />
      )}
    </section>
  );
}

/* ---------------- Score summary ---------------- */

function ScoreSummary({ scores, unanswered, totalChosen, gradedAnswerCount, onReset }) {
  const totalCorrect = SECTION_META.reduce((sum, s) => sum + (scores[s.key]?.correct || 0), 0);
  const totalGraded = SECTION_META.reduce((sum, s) => sum + (scores[s.key]?.total || 0), 0);
  const pct = totalGraded > 0 ? Math.round((totalCorrect / totalGraded) * 100) : 0;

  const tone = pct >= 80 ? 'emerald' : pct >= 50 ? 'amber' : 'rose';
  const headline =
    pct >= 80 ? 'Xuất sắc!' : pct >= 50 ? 'Khá tốt — cố thêm nhé!' : 'Cần ôn lại phần này.';

  return (
    <Card className="mb-5 overflow-hidden" flat>
      <div className="flex flex-wrap items-center justify-between gap-3 border-b-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] px-4 py-3.5">
        <div className="flex items-center gap-2.5">
          <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-[#fff4cc] text-[var(--color-duo-yellow-dark)]">
            <Trophy className="h-5 w-5" />
          </span>
          <div>
            <h3 className="text-base font-extrabold text-[var(--color-duo-ink)]">
              Kết quả bài luyện
            </h3>
            <p className="text-xs font-semibold text-[var(--color-duo-gray)]">{headline}</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge tone={tone}>
            {totalCorrect}/{totalGraded} câu có đáp án · {pct}%
          </Badge>
          <Button size="sm" variant="secondary" onClick={onReset}>
            Làm lại
          </Button>
        </div>
      </div>

      <div className="px-4 py-4">
        <ProgressBar value={totalCorrect} max={Math.max(totalGraded, 1)} tone={tone} />

        <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {SECTION_META.map((s) => {
            const sc = scores[s.key] || { correct: 0, total: 0 };
            const sectionPct = sc.total > 0 ? Math.round((sc.correct / sc.total) * 100) : 0;
            return (
              <div
                key={s.key}
                className="rounded-2xl border-2 border-[var(--color-duo-line)] bg-white px-3 py-3 shadow-[0_2px_0_0_var(--color-duo-line)]"
              >
                <p className="text-xs font-extrabold uppercase tracking-wide text-[var(--color-duo-ink)]">
                  {s.label}
                </p>
                <p className="text-[11px] font-medium text-[var(--color-duo-muted)]">{s.hint}</p>
                <p className="mt-1 text-sm font-extrabold text-[var(--color-duo-ink)]">
                  {scoreSentence(sc)}
                </p>
                {sc.total > 0 ? (
                  <ProgressBar
                    value={sc.correct}
                    max={sc.total}
                    tone={sectionPct >= 80 ? 'emerald' : sectionPct >= 50 ? 'amber' : 'brand'}
                    className="mt-2 !h-3"
                  />
                ) : null}
              </div>
            );
          })}
        </div>

        <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-[11px] font-semibold text-[var(--color-duo-gray)]">
          <span>
            Bạn đã chọn <strong>{totalChosen}</strong> đáp án.
          </span>
          <span>
            <strong>{unanswered}</strong> câu chưa chọn.
          </span>
          <span>
            <strong>{gradedAnswerCount}</strong> câu có đáp án trong dữ liệu (đã chấm tự động).
          </span>
        </div>

        <p className="mt-3 rounded-xl bg-[#fff4cc] px-3 py-2 text-xs font-semibold text-[#8a6d00]">
          Điểm phía trên chỉ tính các câu đã có đáp án trong Answer Key của sách. Phần Listening
          (câu 1-9) nay đã được chấm tự động theo Answer Key; chỉ một vài câu mà bản OCR không đọc
          được đáp án mới không được tính.
        </p>

        <p className="mt-2 text-[11px] font-medium text-[var(--color-duo-muted)]">
          Kết quả đã được lưu vào lịch sử luyện tập và cập nhật lịch ôn tập giãn cách (SRS) trên
          máy bạn.
        </p>
      </div>
    </Card>
  );
}

/* ------------------------------------------------------------------ */
/* Main tab                                                            */
/* ------------------------------------------------------------------ */

/**
 * @param {{lesson?: import('../lib/types.js').Lesson|null}} props
 */
export default function Tab5Practice({ lesson }) {
  const { lessonId } = useApp();

  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [tapescriptOpen, setTapescriptOpen] = useState(false);
  const [historyList, setHistoryList] = useState(() => loadHistory());
  const [historyOpen, setHistoryOpen] = useState(false);
  const [historyFilter, setHistoryFilter] = useState('lesson');
  const isReviewingRef = useRef(false);

  /*
   * Answer Key + giai thich + tapescript cua sach. Cac file nay duoc fetch MOT lan
   * cho ca 50 bai (module answerKey.js tu cache), nen doi bai khong ton them request.
   */
  const [keyData, setKeyData] = useState({ answers: {}, explanations: {}, tapescripts: {} });
  useEffect(() => {
    let alive = true;
    Promise.all([loadAnswers(), loadExplanations(), loadTapescripts()]).then(([a, e, t]) => {
      if (alive) setKeyData({ answers: a, explanations: e, tapescripts: t || {} });
    });
    return () => {
      alive = false;
    };
  }, []);

  const id = Number(lesson?.lesson_id ?? lessonId ?? 1);
  const words = useMemo(() => lessonWords(lesson), [lesson]);

  const lessonHistory = useMemo(
    () =>
      (Array.isArray(historyList) ? historyList : []).filter(
        (item) => Number(item?.lessonId) === id,
      ),
    [historyList, id],
  );

  /* Tapescript: uu tien tapescripts_full.json / tapescripts.json qua tapescriptFor, roi fallback ve lesson. */
  const tapescriptObj = useMemo(() => {
    const fromKey = tapescriptFor(keyData.tapescripts, id);
    if (fromKey) return fromKey;
    const raw = lesson?.practice?.tapescript ?? lesson?.tapescript ?? null;
    if (!raw) return null;
    if (typeof raw === 'string' && raw.trim()) {
      return {
        lesson_id: id,
        part1: '',
        part2: '',
        part3: '',
        part4: '',
        fullText: raw.trim(),
      };
    }
    if (typeof raw === 'object') {
      const p1 = String(raw.part1 || '').trim();
      const p2 = String(raw.part2 || '').trim();
      const p3 = String(raw.part3 || '').trim();
      const p4 = String(raw.part4 || '').trim();
      const joined = Object.entries(raw)
        .map(([k, v]) => (v ? `[${k}] ${v}` : ''))
        .filter(Boolean)
        .join('\n\n');
      if (!joined) return null;
      return {
        lesson_id: id,
        part1: p1,
        part2: p2,
        part3: p3,
        part4: p4,
        fullText: joined,
      };
    }
    return null;
  }, [keyData.tapescripts, id, lesson]);

  const tapescript = tapescriptObj?.fullText ?? null;
  const hasTapescript = hasText(tapescript);

  const audioUrl = useMemo(() => audioUrlFor(id), [id]);

  /**
   * Dap an dung cua mot cau: UU TIEN Answer Key cua sach, sau do moi den
   * `answer` nhung san trong lesson JSON.
   *
   * VI SAO UU TIEN ANSWER KEY: `answer` trong JSON do OCR sinh ra va chi xuat
   * hien o mot so bai; Answer Key la phan sach IN RO o cuoi sach (trang 330+)
   * nen dang tin hon. Voi Part 1-4 thi JSON khong he co `answer` — truoc day
   * chung bi gan null va nguoi hoc phai tu cham; nay da cham duoc that.
   */
  const expectedFor = useCallback(
    (num, fallback = null) => {
      const fromKey = answerFor(keyData.answers, id, num);
      return fromKey || normalizeLetter(fallback);
    },
    [keyData.answers, id],
  );

  /**
   * Gan dap an + giai thich vao TUNG cau hoi ngay khi lap rap du lieu.
   *
   * Lam o day (mot cho duy nhat) thay vi rai rac trong tung component Part, nho
   * vay moi Part tu dong nhan duoc dap an that ma khong phai sua 4 noi.
   * `item.answer` co san trong JSON van duoc ton trong lam phuong an du phong.
   */
  const withKey = useCallback(
    (q) => {
      if (!q || q.question_num === undefined || q.question_num === null) return q;
      const num = Number(q.question_num);
      return {
        ...q,
        answer: expectedFor(num, q.answer),
        explanation: explanationFor(keyData.explanations, id, num),
      };
    },
    [expectedFor, keyData.explanations, id],
  );

  const listening = useMemo(
    () => ({
      /*
       * Part 1 trong sach chi la ANH + 4 lua chon doc trong audio (scan khong
       * co chu). JSON nen khong co part1 — nhung anh part1_photos/lesson_NN.jpg
       * luon co, nen tu tao {question_num: 1} de hien anh + nut A/B/C/D tu
       * cham, thay vi bao "Chua co du lieu" trong khi anh van dang ton tai.
       */
      part1: withKey(lesson?.practice?.listening?.part1 ?? { question_num: 1 }),
      part2: Array.isArray(lesson?.practice?.listening?.part2)
        ? lesson.practice.listening.part2.map(withKey)
        : [],
      part3: Array.isArray(lesson?.practice?.listening?.part3)
        ? lesson.practice.listening.part3.map(withKey)
        : [],
      part4: Array.isArray(lesson?.practice?.listening?.part4)
        ? lesson.practice.listening.part4.map(withKey)
        : [],
      /*
       * Tieu de Part 1-4 do sach in (`listening.parts`). Loader giu lai o
       * practice.listening.parts; JSON OCR lai dat o lesson.listening.parts —
       * doc ca hai de chiu duoc moi hinh dang.
       */
      parts: Array.isArray(lesson?.practice?.listening?.parts)
        ? lesson.practice.listening.parts
        : Array.isArray(lesson?.listening?.parts)
          ? lesson.listening.parts
          : [],
    }),
    [lesson, withKey],
  );

  const reading = useMemo(() => {
    const raw5 = lesson?.practice?.reading?.part5;
    const raw6 = lesson?.practice?.reading?.part6 ?? null;
    const raw7 = lesson?.practice?.reading?.part7 ?? null;
    return {
      part5: Array.isArray(raw5) ? raw5.map(withKey) : [],
      part6:
        raw6 && Array.isArray(raw6.questions)
          ? { ...raw6, questions: raw6.questions.map(withKey) }
          : raw6,
      /*
       * Part7 co the la MOT object {passages, questions} hoac mot MANG cac block
       * nhu vay (JSON OCR doi hinh dang tuy bai). Chuan hoa ve object de
       * Part7SplitView luon doc duoc `data.questions`.
       */
      part7: Array.isArray(raw7)
        ? {
            passages: raw7.flatMap((b) => (Array.isArray(b?.passages) ? b.passages : [])),
            questions: raw7
              .flatMap((b) => (Array.isArray(b?.questions) ? b.questions : []))
              .map(withKey),
          }
        : raw7 && Array.isArray(raw7.questions)
          ? { ...raw7, questions: raw7.questions.map(withKey) }
          : raw7,
    };
  }, [lesson, withKey]);

  /** Re-answering after a submit re-opens grading so the summary stays in sync. */
  const select = useCallback((num, letter) => {
    if (num === null || num === undefined) return;
    setAnswers((prev) => ({ ...prev, [num]: letter }));
    setSubmitted(false);
  }, []);

  /* Keep a flat view of every question for grading + totals. */
  const allQuestions = useMemo(() => {
    const rows = [];

    const p1 = listening.part1;
    if (p1) {
      const n = p1.question_num ?? 1;
      rows.push({ num: n, section: SEC_LISTENING, answer: expectedFor(n) });
    }

    const p2 = listening.part2.length
      ? listening.part2.map((p, i) => ({ ...p, question_num: p.question_num ?? 2 + i }))
      : [2, 3].map((n) => ({ question_num: n }));

    for (const p of p2)
      rows.push({ num: p.question_num, section: SEC_LISTENING, answer: expectedFor(p.question_num) });
    for (const p of listening.part3)
      rows.push({ num: p.question_num, section: SEC_LISTENING, answer: expectedFor(p.question_num) });
    for (const p of listening.part4)
      rows.push({ num: p.question_num, section: SEC_LISTENING, answer: expectedFor(p.question_num) });

    for (const p of reading.part5)
      rows.push({ num: p.question_num, section: SEC_PART5, answer: expectedFor(p.question_num, p.answer) });

    const p6Questions = Array.isArray(reading.part6?.questions) ? reading.part6.questions : [];
    for (const q of p6Questions)
      rows.push({ num: q.question_num, section: SEC_PART6, answer: expectedFor(q.question_num, q.answer) });

    const p7Questions = Array.isArray(reading.part7?.questions) ? reading.part7.questions : [];
    for (const q of p7Questions)
      rows.push({ num: q.question_num, section: SEC_PART7, answer: expectedFor(q.question_num, q.answer) });

    return rows;
  }, [listening, reading, expectedFor]);

  const scores = useMemo(() => {
    const out = {
      [SEC_LISTENING]: { correct: 0, total: 0 },
      [SEC_PART5]: { correct: 0, total: 0 },
      [SEC_PART6]: { correct: 0, total: 0 },
      [SEC_PART7]: { correct: 0, total: 0 },
    };
    for (const q of allQuestions) {
      const expected = normalizeLetter(q.answer);
      if (!expected) continue;
      const bucket = out[q.section];
      bucket.total += 1;
      if (normalizeLetter(answers[q.num]) === expected) bucket.correct += 1;
    }
    return out;
  }, [allQuestions, answers]);

  const chosenCount = useMemo(
    () => allQuestions.filter((q) => normalizeLetter(answers[q.num])).length,
    [allQuestions, answers],
  );

  const stats = useMemo(() => {
    let gradedTotal = 0;
    let gradedCorrect = 0;
    for (const q of allQuestions) {
      const expected = normalizeLetter(q.answer);
      if (!expected) continue;
      gradedTotal += 1;
      if (normalizeLetter(answers[q.num]) === expected) gradedCorrect += 1;
    }
    return {
      gradedTotal,
      gradedCorrect,
      unanswered: allQuestions.length - chosenCount,
      totalQuestions: allQuestions.length,
    };
  }, [allQuestions, answers, chosenCount]);

  /* On submit: unlock the tapescript, save the attempt, feed the SRS. */
  useEffect(() => {
    if (!submitted || !lesson) return;
    if (isReviewingRef.current) {
      isReviewingRef.current = false;
      return;
    }
    try {
      for (const q of allQuestions) {
        const expected = normalizeLetter(q.answer);
        // Only questions with a known answer can drive SRS/progress honestly.
        if (!expected) continue;
        const chosen = normalizeLetter(answers[q.num]);
        const correct = chosen === expected;
        // Touch every target word so the lesson shows up in progress + review.
        for (const w of lesson.words_to_learn || []) {
          if (!w?.word) continue;
          markWordLearned(id, w.word, true);
          recordReview(id, w.word, correct ? 3 : 1, { source: 'practice' });
        }
      }
      const nextHist = pushHistory({
        type: 'practice',
        lessonId: id,
        lessonTitle: lesson?.title || '',
        correct: stats.gradedCorrect,
        total: stats.gradedTotal,
        chosen: chosenCount,
        scores,
        userAnswers: { ...answers },
      });
      setHistoryList(nextHist);
    } catch {
      /* storage is best-effort — never let it break the UI */
    }
    // Intentionally runs once per submit action.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [submitted]);

  const reset = useCallback(() => {
    setAnswers({});
    setSubmitted(false);
    setTapescriptOpen(false);
  }, []);

  const handleReviewAttempt = useCallback((item) => {
    if (!item?.userAnswers || typeof item.userAnswers !== 'object') return;
    isReviewingRef.current = true;
    setAnswers({ ...item.userAnswers });
    setSubmitted(true);
    setTapescriptOpen(true);
  }, []);

  const handleDeleteHistoryItem = useCallback((idOrAt) => {
    if (!idOrAt) return;
    setHistoryList(deleteHistoryItem(idOrAt));
  }, []);

  const handleClearLessonHistory = useCallback(() => {
    setHistoryList(clearHistory(id));
  }, [id]);

  const handleClearAllHistory = useCallback(() => {
    setHistoryList(clearHistory(null));
  }, []);

  /* ---- Null / missing guards ---- */

  if (!lesson) {
    return (
      <div>
        <EmptyState
          icon={Headphones}
          title="Chưa có dữ liệu bài học"
          description="Bài học này chưa được trích xuất. Hãy chọn một bài khác ở thanh bên trái, hoặc chạy OCR để tạo file lessons_json tương ứng."
        />
      </div>
    );
  }

  const hasAnyPractice = Boolean(
    listening.part1 ||
      listening.part2.length ||
      listening.part3.length ||
      listening.part4.length ||
      reading.part5.length ||
      reading.part6 ||
      reading.part7,
  );

  const subtitle = [lesson.theme_name, `Luyện đề 7 phần · ${stats.totalQuestions} câu`]
    .filter(Boolean)
    .join(' · ');

  return (
    <div>
      <AudioPlayer
        key={audioUrl}
        lessonId={id}
        title={lesson.title || ''}
        subtitle={subtitle}
        audioUrl={audioUrl}
        tapescriptOpen={tapescriptOpen}
        onTapescriptToggle={() => setTapescriptOpen((v) => !v)}
        historyCount={lessonHistory.length}
        historyOpen={historyOpen}
        onHistoryToggle={() => setHistoryOpen((v) => !v)}
      />

      {historyOpen ? (
        <PracticeHistoryPanel
          lessonId={id}
          historyList={historyList}
          lessonHistory={lessonHistory}
          filterMode={historyFilter}
          onFilterChange={setHistoryFilter}
          onReviewAttempt={handleReviewAttempt}
          onDeleteItem={handleDeleteHistoryItem}
          onClearLesson={handleClearLessonHistory}
          onClearAll={handleClearAllHistory}
        />
      ) : null}

      {!hasAnyPractice ? (
        <EmptyState
          icon={BookOpen}
          title="Bài học này chưa có phần luyện đề"
          description="Dữ liệu bài học hiện chỉ có từ vựng. Bạn vẫn có thể nghe audio ở thanh trên, hoặc chuyển sang tab khác để học từ vựng và flashcard."
        />
      ) : (
        <>
          <VocabLegend words={words} />

          {tapescriptOpen ? (
            <TapescriptPanel
              available={hasTapescript}
              tapescriptObj={tapescriptObj}
              text={tapescript}
              words={words}
            />
          ) : null}

          <ListeningSection
            lessonId={id}
            listening={listening}
            answers={answers}
            onSelect={select}
            graded={submitted}
            words={words}
            tapescriptOpen={tapescriptOpen}
            parts={listening.parts}
          />

          <hr className="my-6 border-slate-200" />

          <SectionTitle
            icon={BookOpen}
            title="Reading (10-23)"
            right={<Badge tone="brand">14 câu</Badge>}
          />

          <Part5
            items={reading.part5}
            answers={answers}
            onSelect={select}
            graded={submitted}
            words={words}
          />

          <Part6
            data={reading.part6}
            answers={answers}
            onSelect={select}
            graded={submitted}
            words={words}
          />

          <Part7SplitView
            data={reading.part7}
            answers={answers}
            onSelect={select}
            graded={submitted}
            words={words}
          />

          {/*
            Feedback banner kiểu Duolingo: sau khi nộp bài, hiện thanh cố định ở
            ĐÁY màn hình với icon tròn, tiêu đề đậm và nút TIẾP TỤC bên phải.
            Ẩn khi chưa nộp để không che nội dung đang làm.
          */}
          {submitted ? (() => {
            const fbPct = stats.gradedTotal
              ? Math.round((stats.gradedCorrect / stats.gradedTotal) * 100)
              : 0;
            const fbOk = fbPct >= 50;
            return (
              <div className={`duo-feedback ${fbOk ? 'duo-feedback-correct' : 'duo-feedback-wrong'}`}>
                <div className="mx-auto flex max-w-5xl items-center gap-3 px-4 py-3">
                  <span className="duo-feedback-icon">
                    {fbOk ? <CircleCheck className="h-7 w-7" /> : <CircleX className="h-7 w-7" />}
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="duo-feedback-title">
                      {fbPct >= 80 ? 'Tuyệt vời!' : fbOk ? 'Khá tốt!' : 'Chưa đúng'}
                    </p>
                    <p className="text-xs font-semibold text-[var(--color-duo-ink)]">
                      Bạn đúng {stats.gradedCorrect}/{stats.gradedTotal} câu có đáp án · {fbPct}%
                    </p>
                  </div>
                  <Button
                    variant={fbOk ? 'success' : 'danger'}
                    size="md"
                    className="shrink-0"
                    onClick={() => {
                      document
                        .getElementById('tab5-score-summary')
                        ?.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }}
                  >
                    Tiếp tục
                  </Button>
                </div>
              </div>
            );
          })() : null}

          {submitted ? (
            <div id="tab5-score-summary">
              <ScoreSummary
                scores={scores}
                unanswered={stats.unanswered}
                totalChosen={chosenCount}
                gradedAnswerCount={stats.gradedTotal}
                onReset={reset}
              />
            </div>
          ) : null}

          {!historyOpen && historyList.length > 0 ? (
            <PracticeHistoryPanel
              lessonId={id}
              historyList={historyList}
              lessonHistory={lessonHistory}
              filterMode={historyFilter}
              onFilterChange={setHistoryFilter}
              onReviewAttempt={handleReviewAttempt}
              onDeleteItem={handleDeleteHistoryItem}
              onClearLesson={handleClearLessonHistory}
              onClearAll={handleClearAllHistory}
            />
          ) : null}

          {/* Sticky action bar — the single submit button of the whole tab. */}
          <div className="sticky bottom-0 z-20 mt-5 rounded-2xl border-2 border-[var(--color-duo-line)] bg-white/95 px-4 py-3.5 shadow-[0_-2px_0_0_var(--color-duo-line)] backdrop-blur supports-[backdrop-filter]:bg-white/85">
            <div className="mb-3">
              <div className="mb-1.5 flex items-center justify-between text-[11px] font-extrabold uppercase tracking-wide text-[var(--color-duo-gray)]">
                <span>Tiến độ làm bài</span>
                <span className="tabular-nums text-[var(--color-duo-green-dark)]">
                  {chosenCount}/{stats.totalQuestions} câu
                </span>
              </div>
              <ProgressBar value={chosenCount} max={Math.max(stats.totalQuestions, 1)} />
            </div>
            <div className="flex flex-wrap items-center justify-between gap-3">
              <p className="text-xs font-semibold text-[var(--color-duo-gray)]">
                Đã chọn <strong className="text-[var(--color-duo-ink)]">{chosenCount}</strong>/
                {stats.totalQuestions} câu · {stats.gradedTotal} câu có đáp án để chấm tự động.
              </p>
              <div className="flex items-center gap-2.5">
                <Button variant="secondary" size="sm" onClick={reset}>
                  Xoá lựa chọn
                </Button>
                <Button
                  variant="primary"
                  size="lg"
                  onClick={() => {
                    isReviewingRef.current = false;
                    setSubmitted(true);
                    setTapescriptOpen(true);
                  }}
                >
                  <Send className="h-4 w-4" />
                  Nộp bài &amp; Chấm điểm
                </Button>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
