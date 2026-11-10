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
import { loadProgress, loadSrs, markWordLearned, srsKey } from '../lib/storage.js';
import { useApp } from '../lib/store.jsx';
import { WORD_FAMILY_LABEL, WORD_FAMILY_ORDER } from '../lib/types.js';

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

function buildQuizSession(wordRecords) {
  const questions = [];

  for (const rec of wordRecords || []) {
    const { entry, lessonId, lessonObj } = rec;
    if (!entry?.word) continue;

    const examples = (entry.examples || []).filter((e) => e?.en);
    const defEn = entry.definition_en || 'Please deduce the base word from context';
    const clozeDefEn = makeCloze(defEn, entry.word, '______');
    const defVi = entry.definition_vi || examples[0]?.vi || '';

    // CÂU 1: Gõ từ gốc từ nghĩa tiếng Anh
    const acceptedBase = [entry.word];
    if (norm(entry.word) === 'canceled') acceptedBase.push('cancelled');
    if (norm(entry.word) === 'cancelled') acceptedBase.push('canceled');

    questions.push({
      uid: `q-base-${lessonId}-${entry.word}-${Math.random().toString(36).slice(2, 6)}`,
      type: 'base_word',
      lessonId,
      entry,
      lessonObj,
      promptEn: clozeDefEn,
      hintVi: defVi,
      pos: entry.pos || '',
      answer: entry.word,
      accepted: acceptedBase,
    });

    // CÂU 2: Câu tùy biến (chọn ngẫu nhiên 1 câu từ kho câu)
    const candidates = [];

    // 1. Câu srs_sentence (câu đặc trưng bắt buộc chia thì/họ từ)
    if (entry.srs_sentence?.en && entry.srs_sentence?.answer) {
      const s = entry.srs_sentence;
      const ans = String(s.answer).trim();
      const raw = String(s.en).trim();
      const cloze = /_{3,}/.test(raw)
        ? raw.replace(/_{3,}/g, '______')
        : makeCloze(raw, ans, '______');
      candidates.push({
        promptEn: cloze,
        fullEn: /_{3,}/.test(raw) ? raw.replace(/_{3,}/g, ans) : raw,
        hintVi: s.vi || defVi,
        answer: ans,
        accepted: [ans],
        posHint: s.pos_hint || entry.pos || '',
      });
    }

    // 2. Câu ví dụ trong sách
    for (const ex of examples) {
      const segs = highlightWord(ex.en, [entry.word]);
      const hit = segs.find((s) => s.hit);
      if (hit) {
        const cloze = segs.map((s) => (s.hit ? '______' : s.text)).join('');
        candidates.push({
          promptEn: cloze,
          fullEn: ex.en,
          hintVi: ex.vi || defVi,
          answer: hit.text.trim(),
          accepted: [hit.text.trim()],
          posHint: entry.pos || '',
        });
      }
    }

    // 3. Câu trong bảng họ từ
    const families = collectEntryFamilies(entry, lessonObj);
    for (const fam of families) {
      if (fam.word && fam.example) {
        const segs = highlightWord(fam.example, [fam.word]);
        const hit = segs.find((s) => s.hit);
        if (hit) {
          const cloze = segs.map((s) => (s.hit ? '______' : s.text)).join('');
          candidates.push({
            promptEn: cloze,
            fullEn: fam.example,
            hintVi: fam.vi || defVi,
            answer: hit.text.trim(),
            accepted: [hit.text.trim(), fam.word],
            posHint: fam.pos || '',
          });
        }
      }
    }

    // Bốc ngẫu nhiên 1 câu tùy biến cho từ này
    if (candidates.length > 0) {
      const picked = candidates[Math.floor(Math.random() * candidates.length)];
      questions.push({
        uid: `q-custom-${lessonId}-${entry.word}-${Math.random().toString(36).slice(2, 6)}`,
        type: 'custom_sentence',
        lessonId,
        entry,
        lessonObj,
        promptEn: picked.promptEn,
        hintVi: picked.hintVi,
        pos: picked.posHint || entry.pos || '',
        answer: picked.answer,
        accepted: picked.accepted,
      });
    }
  }

  // Shuffle ngẫu nhiên toàn bộ danh sách câu hỏi
  for (let i = questions.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [questions[i], questions[j]] = [questions[j], questions[i]];
  }

  return questions;
}

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
}) {
  const { entry, lessonId, lessonObj } = item;
  const [value, setValue] = useState('');
  const [state, setState] = useState('answering'); // answering | correct | wrong
  const [wrongCount, setWrongCount] = useState(0);
  const [showTheory, setShowTheory] = useState(false);
  const [feedbackMsg, setFeedbackMsg] = useState('');
  const inputRef = useRef(null);
  const theoryRef = useRef(null);
  const { speak } = useSpeech();

  useEffect(() => {
    setValue('');
    setState('answering');
    setWrongCount(0);
    setShowTheory(false);
    setFeedbackMsg('');
    setTimeout(() => inputRef.current?.focus(), 50);
  }, [item.uid]);

  const handleCheck = () => {
    if (!norm(value) || state === 'correct') return;

    const ok = matchesAny(value, item.accepted);

    if (ok) {
      setState('correct');
      setFeedbackMsg('Chính xác tuyệt đối!');
      speak(item.answer);

      // Gửi kết quả câu hỏi lên Tab3Srs để thực hiện Session-level Aggregation
      onReviewed?.({ uid: item.uid, item, isCorrect: true, wrongCount });
    } else {
      const nextWrong = wrongCount + 1;
      setWrongCount(nextWrong);

      if (nextWrong === 1) {
        // Sai lần 1: cho cơ hội gõ lại
        setFeedbackMsg('Chưa chính xác, hãy thử lại một lần nữa!');
        setValue('');
        inputRef.current?.focus();
      } else {
        // Sai từ lần 2 trở lên: tính là quên và mở rộng lý thuyết bên dưới
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
      e.stopPropagation();
      if (state === 'answering') {
        handleCheck();
      } else {
        onNext?.();
      }
    }
  };

  // Phím tắt khi đã trả lời xong câu hỏi (Enter để tiếp tục, R/E để nghe phát âm)
  useEffect(() => {
    const onKey = (e) => {
      if (state === 'answering') return;
      if (e.key === 'Enter') {
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
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
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
          {item.hintVi ? (
            <p className="mt-2 border-t border-[var(--color-duo-blue)]/20 pt-2 text-xs font-bold text-slate-600 sm:text-sm">
              <span className="text-[#0b6ea8]">Gợi ý:</span> {item.hintVi}
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
                          <td className="py-1.5 font-black text-slate-800 dark:text-slate-100">{f.word}</td>
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
    openLesson,
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

  // Nạp 50 bài cho global
  useEffect(() => {
    const targetIds = Array.from({ length: 50 }, (_, i) => i + 1);
    const missing = targetIds.filter((id) => !allLessonsMap[id]);
    if (!missing.length) return;

    let cancelled = false;
    Promise.all(
      missing.map(async (id) => {
        const res = await loadLesson(id);
        return res.status === 'loaded' && res.lesson ? [id, res.lesson] : null;
      }),
    ).then((entries) => {
      if (cancelled) return;
      const valid = entries.filter(Boolean);
      if (valid.length) {
        setAllLessonsMap((prev) => ({ ...prev, ...Object.fromEntries(valid) }));
      }
    });

    return () => {
      cancelled = true;
    };
  }, [allLessonsMap]);

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
    const now = new Date();
    const srsMap = srs || {};

    const dueList = [];
    const learnedList = [];

    for (const rec of allWordRecords) {
      const key = srsKey(rec.lessonId, rec.entry.word);
      const card = srsMap[key];
      const marked = isWordMarkedLearned(progress, rec.lessonId, rec.entry.word);
      if (card && isDue(card, now)) dueList.push(rec);
      if (card || marked) learnedList.push(rec);
    }

    if (poolFilter === 'lesson') {
      const lid = Number(selectedLessonId) || 1;
      const inLesson = allWordRecords.filter((r) => r.lessonId === lid);
      return inLesson.length ? inLesson : allWordRecords.slice(0, 12);
    }

    if (poolFilter === 'theme') {
      const theme = THEMES.find((t) => t.theme_id === Number(selectedThemeId)) || THEMES[0];
      const inTheme = allWordRecords.filter((r) => theme.lessons.includes(r.lessonId));
      return inTheme.length ? inTheme : allWordRecords.slice(0, 12);
    }

    if (poolFilter === 'learned') {
      return learnedList.length ? learnedList : allWordRecords.slice(0, 12);
    }

    // poolFilter === 'due'
    if (dueList.length > 0) return dueList;
    if (learnedList.length > 0) return learnedList;
    return allWordRecords.slice(0, 12);
  }, [allWordRecords, poolFilter, selectedLessonId, selectedThemeId, srs, progress]);

  // Tạo câu hỏi Random (Shuffle) mỗi lần thay đổi tập từ hoặc bấm làm lại
  const [quizQuestions, setQuizQuestions] = useState([]);
  const [sessionTracker, setSessionTracker] = useState({});

  const initQuiz = useCallback(() => {
    if (!activeWordRecords.length) return;
    const qList = buildQuizSession(activeWordRecords);
    setQuizQuestions(qList);
    setCursor(0);
    setSessionResults([]);
    setSessionTracker({});
    setFinished(false);
  }, [activeWordRecords]);

  useEffect(() => {
    initQuiz();
  }, [initQuiz]);

  const allWordsList = useMemo(() => activeWordRecords.map((r) => r.entry.word), [activeWordRecords]);

  const currentQuestion = quizQuestions[cursor] || null;

  const handleNext = () => {
    if (cursor + 1 < quizQuestions.length) {
      setCursor((c) => c + 1);
    } else {
      // Đảm bảo an toàn: Chốt SM-2 cho bất kỳ từ nào đã làm bài nếu chưa được ghi
      setSessionTracker((prev) => {
        const next = { ...prev };
        for (const [, rec] of Object.entries(next)) {
          if (!rec.recorded && rec.answeredQuestions?.length > 0) {
            const finalGrade = rec.totalErrors <= 1 ? 3 : 1;
            try {
              recordReview(rec.lessonId, rec.word, finalGrade, { source: 'active_recall_end' });
              if (finalGrade >= 3) {
                markWordLearned(rec.lessonId, rec.word, true);
              }
            } catch {
              /* ignore */
            }
            rec.recorded = true;
          }
        }
        return next;
      });
      setFinished(true);
    }
  };

  /**
   * Session-level Aggregation theo chuẩn Anki:
   * Gom toàn bộ kết quả các câu hỏi của cùng một từ trong phiên,
   * sau đó chốt 1 điểm SM-2 duy nhất cho từ đó, loại bỏ triệt để lỗi ghi đè 2 lần.
   */
  const handleReviewed = useCallback((res) => {
    const { item, isCorrect, wrongCount } = res;
    if (!item?.entry?.word) return;

    const wKey = srsKey(item.lessonId, item.entry.word);

    setSessionTracker((prev) => {
      const prevRecord = prev[wKey] || {
        lessonId: item.lessonId,
        word: item.entry.word,
        totalErrors: 0,
        answeredQuestions: [],
        recorded: false,
      };

      const updated = {
        ...prevRecord,
        totalErrors: prevRecord.totalErrors + (isCorrect ? wrongCount : 2),
        answeredQuestions: [
          ...prevRecord.answeredQuestions,
          { uid: item.uid, type: item.type, isCorrect, wrongCount },
        ],
      };

      // Đếm tổng số câu hỏi được tạo cho từ này trong bộ câu hỏi phiên hiện tại
      const totalQuestionsForThisWord = quizQuestions.filter(
        (q) => q.lessonId === item.lessonId && q.entry.word === item.entry.word,
      ).length;

      // Khi người học đã trả lời xong toàn bộ câu hỏi của từ này -> CHỐT ĐIỂM SM-2 DUY NHẤT
      if (!updated.recorded && updated.answeredQuestions.length >= totalQuestionsForThisWord) {
        let finalGrade = 3; // Mặc định Good

        // Đúng tuyệt đối không sai lần nào ở tất cả các câu hỏi của từ này
        if (
          updated.totalErrors === 0 &&
          updated.answeredQuestions.every((q) => q.isCorrect && q.wrongCount === 0)
        ) {
          finalGrade = 4; // Easy
        } else if (
          updated.totalErrors <= 1 &&
          updated.answeredQuestions.every((q) => q.isCorrect)
        ) {
          finalGrade = 3; // Good
        } else {
          finalGrade = 1; // Again
        }

        try {
          recordReview(item.lessonId, item.entry.word, finalGrade, {
            source: 'active_recall_session',
            errors: updated.totalErrors,
          });
          if (finalGrade >= 3) {
            markWordLearned(item.lessonId, item.entry.word, true);
          }
        } catch {
          /* ignore */
        }

        updated.recorded = true;
      }

      return { ...prev, [wKey]: updated };
    });

    setSessionResults((prev) => [...prev, res]);
  }, [quizQuestions]);

  return (
    <div className="space-y-3">
      {/* THANH ĐIỀU KHIỂN & BỘ LỌC TỐI GIẢN */}
      <div className="flex flex-wrap items-center justify-between gap-2 rounded-2xl border-2 border-[var(--color-duo-line)] bg-white px-3.5 py-2">
        <div className="flex items-center gap-2">
          {/* Dropdown bộ lọc tối giản */}
          <select
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
                {cursor + 1}/{quizQuestions.length}
              </span>
              <div className="w-20 sm:w-28">
                <ProgressBar value={cursor + 1} max={quizQuestions.length} tone="emerald" />
              </div>
            </div>
          )}

          <button
            type="button"
            onClick={initQuiz}
            title="Làm lại từ đầu (Xáo trộn câu hỏi)"
            className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-700"
          >
            <RotateCcw className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* MÀN HÌNH HOÀN THÀNH HOẶC CÂU HỎI */}
      {finished ? (
        <Card className="p-6 text-center">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-[var(--color-duo-green)] text-white shadow-[0_4px_0_0_var(--color-duo-green-dark)]">
            <CheckCircle2 className="h-8 w-8" />
          </div>
          <h3 className="mt-4 text-xl font-black text-slate-900">Hoàn thành phiên ôn tập!</h3>
          <p className="mt-1 text-xs font-semibold text-slate-500">
            Hệ thống đã tự động cập nhật chu kỳ trí nhớ SM-2 cho toàn bộ các từ vừa ôn.
          </p>

          <div className="mt-5 flex justify-center gap-3">
            <Button variant="primary" onClick={initQuiz}>
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
        />
      ) : (
        <Card className="p-8 text-center">
          <p className="text-sm font-bold text-slate-500">Đang chuẩn bị câu hỏi...</p>
        </Card>
      )}
    </div>
  );
}
