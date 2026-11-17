/**
 * Tab 3 — Ôn Tập Giãn Cách & Ghi nhớ chủ động (SRS + Active Recall).
 * Thiết kế tối giản Duolingo:
 *   - Vừa khít 1 màn hình khi làm bài (không phải kéo lên kéo xuống).
 *   - Chỉ khi bấm Kiểm tra mà sai thì mới mở rộng phần lý thuyết của từ bên dưới để xem lại.
 *   - Tự động chấm điểm SRS theo 3 mức: 0 sai (Grade 4), sai 1 (Grade 3), sai ≥ 2 (Grade 1).
 *   - Câu hỏi được sinh RANDOM SHUFFLE: Mỗi từ chỉ có đúng 2 câu:
 *       1. Câu 1: Nghĩa tiếng Anh → Gõ từ gốc.
 *       2. Câu 2: Câu tùy biến → Lấy random 1 câu từ kho câu ngữ cảnh (chia từ / họ từ).
 */
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  AlertCircle,
  ArrowRight,
  BookOpen,
  Brain,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  HelpCircle,
  Keyboard,
  RotateCcw,
  Sparkles,
  Volume2,
  XCircle,
} from 'lucide-react';
import {
  Badge,
  Button,
  Card,
  EmptyState,
  Highlighted,
  ProgressBar,
  useSpeech,
} from '../components/ui.jsx';
import { highlightWord, makeCloze } from '../lib/assets.js';
import { THEMES, lessonTitle } from '../data/curriculum.js';
import { derivePos, familiesForEntry, loadLesson, normalizePosKey } from '../lib/lessonLoader.js';
import { isDue, recordReview } from '../lib/srs.js';
import { loadSrs, markWordLearned, srsKey } from '../lib/storage.js';
import { useApp } from '../lib/store.jsx';
import { WORD_FAMILY_LABEL, WORD_FAMILY_ORDER } from '../lib/types.js';
import { buildQuizSession as buildRecallSession } from '../lib/recallSession.js';

/* ------------------------------------------------------------------ */
/* Helpers                                                             */
/* ------------------------------------------------------------------ */

function norm(s) {
  return String(s ?? '')
    .replace(/[’‘`]/g, "'")
    .replace(/[“”]/g, '"')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/[.,;:!?]+$/, '')
    .toLowerCase();
}

function matchesAny(input, accepted) {
  const v = norm(input);
  if (!v) return false;
  return (accepted || []).some((a) => norm(a) === v);
}

function isWordMarkedLearned(progress, lessonId, word) {
  if (!lessonId || !word) return false;
  const lKey = `L${String(lessonId).padStart(2, '0')}`;
  const wordsMap = progress?.[lKey]?.words || {};
  const sKey = srsKey(lessonId, word);
  if (typeof wordsMap[sKey] === 'boolean') return wordsMap[sKey];
  if (typeof wordsMap[word] === 'boolean') return wordsMap[word];
  const lower = String(word).toLowerCase();
  for (const [k, v] of Object.entries(wordsMap)) {
    if (String(k).toLowerCase() === lower || String(k).toLowerCase().endsWith(`:${lower}`)) {
      return Boolean(v);
    }
  }
  return false;
}

function collectEntryFamilies(entry, lessonObj) {
  const baseRows = familiesForEntry(entry, lessonObj);
  const extraRows = Array.isArray(entry?.extra_families) ? entry.extra_families : [];
  const merged = [...baseRows];
  const seen = new Set(merged.map((r) => norm(r.word)));
  for (const ex of extraRows) {
    if (!ex?.word || seen.has(norm(ex.word))) continue;
    seen.add(norm(ex.word));
    const normP = normalizePosKey(ex.pos) || derivePos(ex.word);
    merged.push({
      pos: normP,
      word: ex.word,
      example: ex.example || '',
      vi: ex.vi || '',
      meaning_vi: ex.meaning_vi || '',
      root: entry?.word || '',
      pos_source: ex.pos ? 'book' : 'derived',
    });
  }
  return merged.sort(
    (a, b) => WORD_FAMILY_ORDER.indexOf(a.pos) - WORD_FAMILY_ORDER.indexOf(b.pos),
  );
}

/* ------------------------------------------------------------------ */
/* Sinh tập câu hỏi Random: Mỗi từ đúng 2 câu & Shuffle               */
/* ------------------------------------------------------------------ */

/* ------------------------------------------------------------------ */
/* Card Câu Hỏi Tối Giản Vừa Khít 1 Màn Hình                            */
/* ------------------------------------------------------------------ */

function CompactQuizCard({
  item,
  index,
  total,
  allWords,
  onReviewed,
  onNext,
  savedResult,
}) {
  const { entry, lessonId, lessonObj } = item;
  const [value, setValue] = useState('');
  const [state, setState] = useState('answering'); // answering | correct | wrong
  const [wrongCount, setWrongCount] = useState(0);
  const [showTheory, setShowTheory] = useState(false);
  const [feedbackMsg, setFeedbackMsg] = useState('');
  const inputRef = useRef(null);
  const answeredRef = useRef(false);
  const wrongRef = useRef(0);
  const continueBtnRef = useRef(null);
  const theoryRef = useRef(null);
  const { speak } = useSpeech();

  useEffect(() => {
    answeredRef.current = Boolean(savedResult);
    wrongRef.current = savedResult?.wrongCount || 0;
    setValue(savedResult ? item.answer : '');
    setState(savedResult ? (savedResult.isCorrect ? 'correct' : 'wrong') : 'answering');
    setWrongCount(savedResult?.wrongCount || 0);
    setShowTheory(Boolean(savedResult && !savedResult.isCorrect));
    setFeedbackMsg(savedResult ? (savedResult.isCorrect ? 'Đúng' : `Đáp án: ${item.answer}`) : '');
    const timer = setTimeout(() => inputRef.current?.focus(), 60);
    return () => clearTimeout(timer);
  }, [item.uid, savedResult, item.answer]);

  // Tự động focus vào nút "TIẾP TỤC" khi hoàn thành câu hỏi (đúng hoặc sai 2 lần)
  useEffect(() => {
    if (state !== 'answering') {
      const timer = setTimeout(() => {
        continueBtnRef.current?.focus();
      }, 50);
      return () => clearTimeout(timer);
    }
  }, [state]);

  const handleCheck = () => {
    if (!norm(value) || state !== 'answering' || answeredRef.current) return;

    const ok = matchesAny(value, item.accepted);

    if (ok) {
      answeredRef.current = true;
      setState('correct');
      setFeedbackMsg('Chính xác tuyệt đối!');
      speak(item.answer);

      // Gửi kết quả câu hỏi lên Tab3Srs để thực hiện Session-level Aggregation
      onReviewed?.({ uid: item.uid, item, isCorrect: true, wrongCount });
    } else {
      const nextWrong = wrongRef.current + 1;
      wrongRef.current = nextWrong;
      setWrongCount(nextWrong);

      if (nextWrong === 1) {
        // Sai lần 1: cho cơ hội gõ lại
        setFeedbackMsg('Chưa chính xác, hãy thử lại một lần nữa!');
        setValue('');
        inputRef.current?.focus();
      } else {
        // Sai từ lần 2 trở lên: tính là quên và mở rộng lý thuyết bên dưới
        answeredRef.current = true;
        setState('wrong');
        setFeedbackMsg(`Đáp án đúng: ${item.answer}`);
        setShowTheory(true);
        speak(item.answer);

        // Gửi kết quả câu hỏi lên Tab3Srs để thực hiện Session-level Aggregation
        onReviewed?.({ uid: item.uid, item, isCorrect: false, wrongCount: nextWrong });

        // Tự cuộn nhẹ xuống xem lý thuyết nếu cần
        setTimeout(() => {
          theoryRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
      }
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (state === 'answering') {
        handleCheck();
      } else {
        onNext?.();
      }
    }
  };

  // Phím tắt khi đã trả lời xong câu hỏi (Enter / Space để tiếp tục, R/E để nghe phát âm)
  useEffect(() => {
    const onKey = (e) => {
      if (state === 'answering') return;
      if (e.key === 'Enter' || (e.key === ' ' && document.activeElement !== continueBtnRef.current)) {
        e.preventDefault();
        onNext?.();
      } else if (e.key === 'r' || e.key === 'R') {
        e.preventDefault();
        speak(item.answer || entry.word);
      } else if (e.key === 'e' || e.key === 'E') {
        e.preventDefault();
        const sentence = item.fullEn || item.promptEn || '';
        if (sentence) speak(sentence.replace(/_{3,}/g, item.answer));
      }
    };
    window.addEventListener('keydown', onKey, true);
    return () => window.removeEventListener('keydown', onKey, true);
  }, [state, item, entry, speak, onNext]);

  const families = useMemo(() => collectEntryFamilies(entry, lessonObj), [entry, lessonObj]);

  return (
    <div className="space-y-4">
      {/* VÙNG 1 MÀN HÌNH CHÍNH (COMPACT CARD) */}
      <Card className="overflow-hidden p-5 sm:p-6 duo-card">
        {/* Câu hỏi: Định nghĩa EN hoặc Câu khoét lỗ */}
        <div className="rounded-2xl border-2 border-[var(--color-duo-blue)] bg-[var(--color-duo-blue-light)]/45 p-4 sm:p-5">
          <div className="flex items-center justify-between gap-2">
            <span className="text-xs font-black uppercase tracking-wider text-[#0b6ea8]">
              {item.type === 'base_word' ? 'Nghĩa Tiếng Anh (Gõ từ gốc)' : 'Điền từ vào câu'}
            </span>
            <span className="rounded-lg bg-white px-2.5 py-0.5 text-xs font-black text-[#0b6ea8] shadow-xs">
              {item.pos || 'vocab'}
            </span>
          </div>

          <p className="mt-2 text-lg font-black leading-snug text-slate-900 sm:text-xl">
            {item.promptEn}
          </p>

          {/* Nghĩa Tiếng Việt gợi ý ngay bên dưới */}
          {(item.hintVi || entry.definition_vi) ? (
            <p className="mt-2 border-t border-[var(--color-duo-blue)]/20 pt-2 text-xs font-bold text-slate-600 sm:text-sm">
              <span className="text-[#0b6ea8]">Nghĩa:</span> {item.hintVi || entry.definition_vi}
            </p>
          ) : null}
        </div>

        {/* Ô nhập câu trả lời & Nút kiểm tra */}
        <div className="mt-4">
          <div className="flex gap-2">
            <input
              ref={inputRef}
              type="text"
              value={value}
              onChange={(e) => setValue(e.target.value)}
              onKeyDown={handleKeyDown}
              readOnly={state !== 'answering'}
              placeholder={
                item.type === 'base_word' ? 'Gõ từ gốc...' : 'Gõ từ đúng dạng ngữ cảnh...'
              }
              className={`flex-1 rounded-2xl border-2 px-4 py-3 text-base font-extrabold outline-none transition-all placeholder:text-[var(--color-duo-muted)] ${
                state === 'correct'
                  ? 'border-[var(--color-duo-green)] bg-emerald-50 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-200'
                  : state === 'wrong'
                    ? 'border-[var(--color-duo-red)] bg-rose-50 text-rose-800 dark:bg-rose-950/40 dark:text-rose-200'
                    : 'border-[var(--color-duo-line)] bg-white text-[var(--color-duo-ink)] focus:border-[var(--color-duo-blue)] dark:bg-slate-800 dark:text-slate-100'
              }`}
            />

            {state === 'answering' ? (
              <Button
                variant="primary"
                onClick={handleCheck}
                disabled={!value.trim()}
                className="shrink-0 px-5 !text-sm font-black uppercase tracking-wider"
              >
                Kiểm tra
              </Button>
            ) : (
              <Button
                ref={continueBtnRef}
                variant={state === 'correct' ? 'primary' : 'secondary'}
                onClick={onNext}
                title="Bấm Enter hoặc click để tiếp tục"
                className="shrink-0 px-5 !text-sm font-black uppercase tracking-wider"
              >
                Tiếp tục →
              </Button>
            )}
          </div>

          {/* Phản hồi kết quả */}
          {feedbackMsg && (
            <div
              className={`mt-2.5 flex items-center justify-between rounded-xl px-3.5 py-2 text-xs font-black ${
                state === 'correct'
                  ? 'bg-emerald-100 text-emerald-900 dark:bg-emerald-950/60 dark:text-emerald-200'
                  : state === 'wrong'
                    ? 'bg-rose-100 text-rose-900 dark:bg-rose-950/60 dark:text-rose-200'
                    : 'bg-amber-100 text-amber-900 dark:bg-amber-950/60 dark:text-amber-200'
              }`}
            >
              <div className="flex items-center gap-2">
                {state === 'correct' ? (
                  <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-600 dark:text-emerald-400" />
                ) : state === 'wrong' ? (
                  <XCircle className="h-4 w-4 shrink-0 text-rose-600 dark:text-rose-400" />
                ) : (
                  <AlertCircle className="h-4 w-4 shrink-0 text-amber-600 dark:text-amber-400" />
                )}
                <span>{feedbackMsg}</span>
              </div>

              {state !== 'answering' && (
                <button
                  type="button"
                  onClick={() => speak(item.answer)}
                  className="inline-flex items-center gap-1 text-[11px] font-bold text-slate-700 dark:text-slate-300 hover:underline"
                >
                  <Volume2 className="h-3.5 w-3.5" />
                  Phát âm
                </button>
              )}
            </div>
          )}
        </div>
      </Card>

      {/* KHỐI LÝ THUYẾT: CHỈ MỞ RỘNG KHI SAI (KÉO XUỐNG XEM LẠI) */}
      {showTheory && (
        <div ref={theoryRef} className="space-y-3 pt-1 animate-in fade-in duration-300">
          <div className="flex items-center justify-between px-1">
            <span className="text-xs font-black uppercase tracking-wider text-[var(--color-duo-gray)]">
              Lý thuyết &amp; Ngữ cảnh của từ
            </span>
            <button
              type="button"
              onClick={() => setShowTheory((p) => !p)}
              className="text-xs font-bold text-slate-500 hover:text-slate-800"
            >
              {showTheory ? 'Thu gọn ▲' : 'Xem lại lý thuyết ▼'}
            </button>
          </div>

          <Card className="p-4 sm:p-5">
            <div className="flex flex-wrap items-baseline justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-3">
              <div className="flex items-baseline gap-2.5">
                <h4 className="text-xl font-black text-slate-900 dark:text-slate-100">{entry.word}</h4>
                {entry.pos && <Badge tone="violet">{entry.pos}</Badge>}
                {entry.ipa && (
                  <span className="font-mono text-xs text-slate-400">{entry.ipa}</span>
                )}
              </div>
              <Button size="sm" variant="ghost" onClick={() => speak(entry.word)}>
                <Volume2 className="h-4 w-4 text-[var(--color-duo-green-dark)]" />
                Nghe từ gốc
              </Button>
            </div>

            <div className="mt-3 space-y-1.5 text-xs sm:text-sm">
              <p className="font-semibold text-slate-800 dark:text-slate-200">
                <span className="font-black text-slate-400">EN:</span> {entry.definition_en}
              </p>
              {entry.definition_vi && (
                <p className="font-bold text-emerald-700 dark:text-emerald-400">
                  <span className="font-black text-slate-400">VI:</span> {entry.definition_vi}
                </p>
              )}
            </div>

            {/* Các câu ví dụ trong sách */}
            {(entry.examples || []).length > 0 && (
              <div className="mt-4 border-t border-slate-100 dark:border-slate-800 pt-3">
                <p className="mb-2 text-[11px] font-black uppercase tracking-wider text-slate-400">
                  Câu ví dụ thực tế:
                </p>
                <ul className="space-y-2 text-xs sm:text-sm">
                  {entry.examples.map((ex, i) => (
                    <li key={i} className="rounded-lg bg-[var(--color-duo-bg-soft)] p-2.5">
                      <div className="flex items-start justify-between gap-2">
                        <Highlighted text={ex.en} words={allWords} />
                        <button
                          type="button"
                          onClick={() => speak(ex.en)}
                          className="shrink-0 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200"
                          title="Phát âm câu"
                        >
                          <Volume2 className="h-3.5 w-3.5" />
                        </button>
                      </div>
                      {ex.vi && <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">{ex.vi}</p>}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Bảng họ từ mở rộng */}
            {families.length > 0 && (
              <div className="mt-4 border-t border-slate-100 dark:border-slate-800 pt-3">
                <p className="mb-2 text-[11px] font-black uppercase tracking-wider text-slate-400">
                  Gia đình từ (Word Family):
                </p>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead>
                      <tr className="border-b border-slate-200 dark:border-slate-700 text-slate-400">
                        <th className="py-1 font-bold">Từ loại</th>
                        <th className="py-1 font-bold">Từ</th>
                        <th className="py-1 font-bold">Ví dụ</th>
                      </tr>
                    </thead>
                    <tbody>
                      {families.map((f, i) => (
                        <tr key={i} className="border-b border-slate-100 dark:border-slate-800/60">
                          <td className="py-1.5 font-bold text-sky-700 dark:text-sky-400">
                            {WORD_FAMILY_LABEL[f.pos] || f.pos}
                          </td>
                          <td className="py-1.5 font-black text-slate-800 dark:text-slate-100">{f.word}{f.meaning_vi && <span className="mt-0.5 block font-medium text-slate-600 dark:text-slate-300">{f.meaning_vi}</span>}</td>
                          <td className="py-1.5 text-slate-600 dark:text-slate-300">{f.example || '—'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </Card>
        </div>
      )}
    </div>
  );
}
/* ------------------------------------------------------------------ */
/* Component chính: Tab3Srs                                            */
/* ------------------------------------------------------------------ */

export default function Tab3Srs({
  lesson = null,
  globalMode = false,
  initialFilter = null,
  initialThemeId = null,
  initialLessonId = null,
}) {
  const {
    lessonId: ctxLessonId,
    lesson: ctxLesson,
    progress,
    srs,
    dueWordKeys,
    srsNow,
  } = useApp();

  const [poolFilter, setPoolFilter] = useState(
    () => initialFilter || (globalMode ? 'due' : 'lesson'),
  );
  const [selectedThemeId, setSelectedThemeId] = useState(() => Number(initialThemeId) || 1);
  const [selectedLessonId, setSelectedLessonId] = useState(
    () => Number(initialLessonId) || Number(lesson?.lesson_id) || Number(ctxLessonId) || 1,
  );
  const [cursor, setCursor] = useState(0);
  const [sessionResults, setSessionResults] = useState([]);
  const [finished, setFinished] = useState(false);

  const effectiveSingleLesson = lesson || ctxLesson;
  const [allLessonsMap, setAllLessonsMap] = useState(() => {
    if (effectiveSingleLesson?.lesson_id) {
      return { [effectiveSingleLesson.lesson_id]: effectiveSingleLesson };
    }
    return {};
  });

  useEffect(() => {
    if (initialFilter) setPoolFilter(initialFilter);
  }, [initialFilter]);

  useEffect(() => {
    if (initialThemeId) {
      setSelectedThemeId(Number(initialThemeId));
      setPoolFilter('theme');
    }
  }, [initialThemeId]);

  useEffect(() => {
    if (initialLessonId) {
      setSelectedLessonId(Number(initialLessonId));
      setPoolFilter('lesson');
    }
  }, [initialLessonId]);

  // Nạp bài hiện tại
  useEffect(() => {
    if (effectiveSingleLesson?.words_to_learn) {
      const id = Number(effectiveSingleLesson.lesson_id || ctxLessonId || 1);
      setAllLessonsMap((prev) => (prev[id] ? prev : { ...prev, [id]: effectiveSingleLesson }));
    }
  }, [effectiveSingleLesson, ctxLessonId]);

  const [loadState, setLoadState] = useState('loading');
  useEffect(() => {
    let cancelled = false;
    setLoadState('loading');
    Promise.all(Array.from({ length: 50 }, (_, i) => loadLesson(i + 1)))
      .then((results) => {
        if (cancelled) return;
        if (results.some((result) => result.status !== 'loaded' || !result.lesson)) {
          setLoadState('error');
          return;
        }
        setAllLessonsMap(Object.fromEntries(results.map((result, i) => [i + 1, result.lesson])));
        setLoadState('ready');
      }).catch(() => { if (!cancelled) setLoadState('error'); });
    return () => { cancelled = true; };
  }, []);
  // Toàn bộ từ vựng đã tải
  const allWordRecords = useMemo(() => {
    const list = [];
    const sortedIds = Object.keys(allLessonsMap)
      .map(Number)
      .sort((a, b) => a - b);
    for (const lid of sortedIds) {
      const lObj = allLessonsMap[lid];
      for (const entry of lObj?.words_to_learn || []) {
        if (entry?.word) {
          list.push({ lessonId: lid, lessonObj: lObj, entry });
        }
      }
    }
    return list;
  }, [allLessonsMap]);

  // Tập từ vựng tham gia phiên ôn tập
  const activeWordRecords = useMemo(() => {
    const now = srsNow || new Date();
    const srsMap = srs || {};

    const dueList = [];
    const learnedList = [];

    for (const rec of allWordRecords) {
      const key = srsKey(rec.lessonId, rec.entry.word);
      const card = srsMap[key];
      const marked = isWordMarkedLearned(progress, rec.lessonId, rec.entry.word);
      if (dueWordKeys ? dueWordKeys.includes(key) : card && isDue(card, now)) dueList.push(rec);
      if (card || marked) learnedList.push(rec);
    }

    if (poolFilter === 'lesson') {
      const lid = Number(selectedLessonId) || 1;
      const inLesson = allWordRecords.filter((r) => r.lessonId === lid);
      return inLesson;
    }

    if (poolFilter === 'theme') {
      const theme = THEMES.find((t) => t.theme_id === Number(selectedThemeId)) || THEMES[0];
      const inTheme = allWordRecords.filter((r) => theme.lessons.includes(r.lessonId));
      return inTheme;
    }

    if (poolFilter === 'learned') {
      return learnedList;
    }

    // poolFilter === 'due'
    return dueList;
  }, [allWordRecords, poolFilter, selectedLessonId, selectedThemeId, srs, progress, dueWordKeys, srsNow]);

  const [quizQuestions, setQuizQuestions] = useState([]);
  const [sessionTracker, setSessionTracker] = useState({});
  const [sessionError, setSessionError] = useState('');
  const [coverageMissing, setCoverageMissing] = useState([]);
  const [saving, setSaving] = useState(false);
  const sessionRef = useRef(null);
  const resultsRef = useRef(new Map());
  const committedRef = useRef(new Set());
  const nextRef = useRef(null);
  const draftScope = `${poolFilter}:${selectedLessonId}:${selectedThemeId}`;
  const draftKey = `toeic600.recallDraft:${draftScope}`;
  const initQuiz = useCallback((restore = false) => {
    if (loadState !== 'ready' || saving) return;
    if (restore) {
      try {
        const draft = JSON.parse(localStorage.getItem(draftKey) || 'null');
        const current = loadSrs();
        if (draft?.schema === 1 && Array.isArray(draft.questions) && draft.questions.length > 0 && draft.session.scope === draftKey && !draft.finished &&
          Object.entries(draft.session.versions).every(([key, version]) => {
            const card = current[key];
            const reviewId = `${draft.session.sessionId}:${draft.questions.find((q) => srsKey(q.lessonId, q.entry.word) === key)?.wordKey}`;
            return (card?.version || 0) === version || card?.processedReviewIds?.includes(reviewId);
          })) {
          sessionRef.current = draft.session;
          resultsRef.current = new Map(draft.results.map((result) => [result.uid, result]));
          committedRef.current = new Set(draft.committed);
          nextRef.current = null;
          setQuizQuestions(draft.questions);
          setCursor(Math.min(draft.cursor, draft.questions.length - 1));
          setSessionResults(draft.results);
          setSessionTracker(Object.fromEntries(draft.committed.map((key) => [key, true])));
          setCoverageMissing([]);
          setSessionError('');
          setFinished(false);
          return;
        }
      } catch { /* Invalid draft never changes the saved review cards. */ }
    }
    const sessionId = globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random()}`;
    const records = activeWordRecords.map((rec) => ({ ...rec, entry: { ...rec.entry, extra_families: collectEntryFamilies(rec.entry, rec.lessonObj) } }));
    const built = buildRecallSession(records, { sessionId });
    sessionRef.current = { sessionId, scope: draftKey, versions: Object.fromEntries(records.map((rec) => [srsKey(rec.lessonId, rec.entry.word), (srs || {})[srsKey(rec.lessonId, rec.entry.word)]?.version || 0])) };
    resultsRef.current = new Map();
    committedRef.current = new Set();
    nextRef.current = null;
    setCoverageMissing(built.missing);
    setSessionError('');
    setQuizQuestions(built.complete ? built.questions : []);
    setCursor(0);
    setSessionResults([]);
    setSessionTracker({});
    setFinished(false);
  }, [activeWordRecords, loadState, srs, saving, draftKey]);

  // Freeze the session once ready; review events must not rebuild its snapshot.
  useEffect(() => {
    initQuiz(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [loadState, poolFilter, selectedLessonId, selectedThemeId]);

  useEffect(() => {
    if (!sessionRef.current || sessionRef.current.scope !== draftKey || !quizQuestions.length) return;
    try {
      localStorage.setItem(draftKey, JSON.stringify({ schema: 1, session: sessionRef.current, questions: quizQuestions,
        results: sessionResults, committed: Object.keys(sessionTracker), cursor, finished }));
    } catch { setSessionError('Không lưu được phiên đang học. Kiểm tra dung lượng trình duyệt.'); }
  }, [draftKey, quizQuestions, sessionResults, sessionTracker, cursor, finished]);

  useEffect(() => {
    const invalidate = (event) => {
      if (event.type === 'storage' && event.key !== null && event.key !== 'toeic600.srs') return;
      if (event.type !== 'storage' && event.detail?.kind !== 'reset') return;
      try {
        const current = loadSrs();
        const invalid = event.detail?.kind === 'reset' || Object.entries(sessionRef.current?.versions || {}).some(([key, version]) => {
          const card = current[key];
          return (card?.version || 0) !== version && !card?.processedReviewIds?.some((id) => id.startsWith(`${sessionRef.current.sessionId}:`));
        });
        if (!invalid) return;
        localStorage.removeItem(draftKey);
        sessionRef.current = null;
        setQuizQuestions([]);
        setSessionError('Dữ liệu đã thay đổi ở nơi khác. Bắt đầu phiên mới để tiếp tục.');
      } catch (error) { setSessionError(error.message); }
    };
    window.addEventListener('storage', invalidate);
    window.addEventListener('toeic600:state-changed', invalidate);
    return () => {
      window.removeEventListener('storage', invalidate);
      window.removeEventListener('toeic600:state-changed', invalidate);
    };
  }, [draftKey]);

  const allWordsList = useMemo(() => quizQuestions.map((q) => q.entry.word), [quizQuestions]);
  const currentQuestion = quizQuestions[cursor] || null;
  const totalWords = new Set(quizQuestions.map((q) => q.wordKey)).size;
  const completedWords = Object.keys(sessionTracker).length;
  const handleNext = () => {
    if (saving || sessionError || !currentQuestion || !resultsRef.current.has(currentQuestion.uid) || nextRef.current === currentQuestion.uid) return;
    nextRef.current = currentQuestion.uid;
    if (cursor + 1 < quizQuestions.length) setCursor(cursor + 1);
    else setFinished(true);
  };

  const commitPair = async (item, results) => {
    if (!item || results.length !== 2 || results.some((result) => !result)) return;
    const activeSession = sessionRef.current;
    const wordKey = item.wordKey;
    if (committedRef.current.has(wordKey)) return;
    committedRef.current.add(wordKey);
    setSaving(true);
    try {
      const grade = results.every((r) => r.isCorrect) ? 3 : 1;
      const commit = () => {
        if (sessionRef.current !== activeSession) throw new Error('Phiên đã thay đổi, hãy mở lại phiên ôn.');
        // Lesson/theme/learned sessions are explicit, schedule-neutral practice.
        if (poolFilter === 'due') {
          recordReview(item.lessonId, item.entry.word, grade, { source: 'active_recall_session', reviewId: `${sessionRef.current.sessionId}:${wordKey}`, expectedVersion: sessionRef.current.versions[srsKey(item.lessonId, item.entry.word)] });
        }
        if (poolFilter === 'due' && grade >= 3) markWordLearned(item.lessonId, item.entry.word, true);
      };
      if (globalThis.navigator?.locks?.request) await navigator.locks.request('toeic600:srs', commit);
      else commit();
      window.dispatchEvent(new Event('toeic600:state-changed'));
      const updatedCard = poolFilter === 'due' ? loadSrs()[srsKey(item.lessonId, item.entry.word)] : null;
      setSessionTracker((prev) => ({ ...prev, [wordKey]: { grade, due: updatedCard?.due || null, word: item.entry.word } }));
      setSessionError('');
    } catch (error) {
      committedRef.current.delete(wordKey);
      setSessionError(`Chưa lưu kết quả: ${error.message || 'Lỗi lưu dữ liệu'}`);
    } finally { setSaving(false); }
  };

  const handleReviewed = (res) => {
    const item = quizQuestions.find((q) => q.uid === res.uid);
    if (!item || item.uid !== currentQuestion?.uid || resultsRef.current.has(item.uid)) return;
    const result = { ...res, item, wordKey: item.wordKey, type: item.type };
    resultsRef.current.set(item.uid, result);
    setSessionResults([...resultsRef.current.values()]);
    const pair = quizQuestions.filter((q) => q.wordKey === item.wordKey);
    const results = pair.map((q) => resultsRef.current.get(q.uid));
    if (pair.length === 2 && results.every(Boolean)) void commitPair(item, results);
  };
  return (
    <div className="space-y-3">
      {/* THANH ĐIỀU KHIỂN & BỘ LỌC TỐI GIẢN */}
      <div className="flex flex-wrap items-center justify-between gap-2 rounded-2xl border-2 border-[var(--color-duo-line)] bg-white px-3.5 py-2">
        <div className="flex items-center gap-2">
          {/* Dropdown bộ lọc tối giản */}
          <select
            disabled={saving}
            value={poolFilter}
            onChange={(e) => setPoolFilter(e.target.value)}
            className="rounded-xl border-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] px-2.5 py-1 text-xs font-black text-slate-800 outline-none focus:border-[var(--color-duo-blue)]"
          >
            <option value="due">Cần ôn hôm nay (SRS)</option>
            <option value="learned">Tất cả từ đã học</option>
            <option value="lesson">Theo Bài học</option>
            <option value="theme">Theo Chủ đề</option>
          </select>

          {poolFilter === 'lesson' && (
            <select
              value={selectedLessonId}
              onChange={(e) => setSelectedLessonId(Number(e.target.value))}
              className="rounded-xl border-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] px-2 py-1 text-xs font-bold text-slate-800 outline-none"
            >
              {Array.from({ length: 50 }, (_, i) => i + 1).map((id) => (
                <option key={id} value={id}>
                  Bài {String(id).padStart(2, '0')}: {lessonTitle(id)}
                </option>
              ))}
            </select>
          )}

          {poolFilter === 'theme' && (
            <select
              value={selectedThemeId}
              onChange={(e) => setSelectedThemeId(Number(e.target.value))}
              className="rounded-xl border-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] px-2 py-1 text-xs font-bold text-slate-800 outline-none"
            >
              {THEMES.map((t) => (
                <option key={t.theme_id} value={t.theme_id}>
                  Chủ đề {t.theme_id}: {t.theme_name}
                </option>
              ))}
            </select>
          )}
        </div>

        <div className="flex items-center gap-3">
          {/* Tiến độ câu hỏi */}
          {quizQuestions.length > 0 && !finished && (
            <div className="flex items-center gap-2">
              <span className="text-xs font-black tabular-nums text-slate-700">
                Đã kiểm tra {completedWords}/{totalWords} từ · Câu {cursor + 1}/{quizQuestions.length}
                <span className="block">Đã trả lời {sessionResults.length}/{quizQuestions.length} câu</span>
              </span>
              <div className="w-20 sm:w-28">
                <ProgressBar value={completedWords} max={totalWords} tone="emerald" />
              </div>
            </div>
          )}

          <button
            type="button"
            disabled={saving || loadState !== 'ready'}
            onClick={() => initQuiz(false)}
            title="Bắt đầu phiên mới"
            className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-700"
          >
            <RotateCcw className="h-4 w-4" />
          </button>
        </div>
      </div>

      {poolFilter !== 'due' && <p className="text-xs font-semibold text-slate-500">Luyện thêm · Không thay đổi lịch SRS</p>}
      {saving && <p role="status" className="text-sm font-semibold">Đang lưu...</p>}
      {poolFilter === 'due' && currentQuestion && sessionTracker[currentQuestion.wordKey]?.due && (
        <p role="status" className="text-xs font-semibold text-slate-500">Ôn lại {sessionTracker[currentQuestion.wordKey].word}: {new Date(sessionTracker[currentQuestion.wordKey].due).toLocaleString('vi-VN', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' })}</p>
      )}
      {sessionError && <Card className="p-4"><p role="alert">{sessionError}</p><Button disabled={saving} onClick={() => { const pair = quizQuestions.filter((q) => q.wordKey === currentQuestion?.wordKey); void commitPair(currentQuestion, pair.map((q) => resultsRef.current.get(q.uid))); }}>Thử lưu lại</Button></Card>}
      {/* MÀN HÌNH HOÀN THÀNH HOẶC CÂU HỎI */}
      {finished ? (
        <Card className="p-6 text-center">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-[var(--color-duo-green)] text-white shadow-[0_4px_0_0_var(--color-duo-green-dark)]">
            <CheckCircle2 className="h-8 w-8" />
          </div>
          <h3 className="mt-4 text-xl font-black text-slate-900">Hoàn thành phiên ôn tập!</h3>
          <p className="mt-1 text-xs font-semibold text-slate-500">
            Đã kiểm tra {completedWords}/{totalWords} từ · Đã trả lời {sessionResults.length}/{quizQuestions.length} câu.
            {poolFilter === 'due' ? ' Kết quả đã được lưu.' : ' Luyện thêm không thay đổi lịch SRS.'}
            {poolFilter === 'due' && Object.values(sessionTracker).some((result) => result.grade === 1) && ' Các từ chưa nhớ đã được hẹn học lại; phiên hoàn tất không có nghĩa đã hết từ cần ôn.'}
          </p>

          <div className="mt-5 flex justify-center gap-3">
            <Button variant="primary" onClick={() => initQuiz(false)}>
              <RotateCcw className="h-4 w-4" />
              Luyện tiếp lượt mới
            </Button>
          </div>
        </Card>
      ) : currentQuestion ? (
        <CompactQuizCard
          key={currentQuestion.uid}
          item={currentQuestion}
          index={cursor}
          total={quizQuestions.length}
          allWords={allWordsList}
          onReviewed={handleReviewed}
          onNext={handleNext}
          savedResult={resultsRef.current.get(currentQuestion.uid)}
        />
      ) : (
        <Card className="p-8 text-center">
          <p role={loadState === 'error' || coverageMissing.length ? 'alert' : 'status'} className="text-sm font-bold text-slate-500">
            {loadState === 'loading' ? 'Đang tải đủ 50 bài học...' : loadState === 'error' ? 'Không tải được đầy đủ bài học. Vui lòng tải lại trang.' : coverageMissing.length ? `Phiên chưa đủ dữ liệu: ${coverageMissing.length} mục thiếu định nghĩa hoặc câu ngữ cảnh.` : poolFilter === 'due' ? 'Bạn đã hoàn thành các từ đến hạn. Có thể chọn bài học để luyện thêm.' : 'Không có từ trong bộ lọc này.'}
          </p>
          {coverageMissing.length > 0 && <ul className="mt-3 text-sm">{coverageMissing.map((missing) => <li key={`${missing.wordKey}:${missing.reason}`}>{missing.wordKey}: {missing.reason === 'missing_definition_en' ? 'Thiếu định nghĩa tiếng Anh' : 'Thiếu câu ngữ cảnh'}</li>)}</ul>}
        </Card>
      )}
    </div>
  );
}
