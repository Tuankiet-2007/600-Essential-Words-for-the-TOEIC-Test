/**
 * QuickDictionaryModal.jsx — Cửa sổ Từ điển & Tra từ nhanh (Phong cách Duolingo).
 *
 * Tính năng:
 * - Tra cứu tức thì (0ms) trong bộ dữ liệu 600 từ vựng TOEIC (kèm từ loại, nghĩa tiếng Việt, bài học).
 * - Tự động dịch nhanh (Google Dịch / AI) cho bất kỳ từ hoặc cụm từ tiếng Anh nào ngoài sách.
 * - Phát âm US-English chuẩn (Web Speech API).
 * - Bấm vào từ TOEIC sẽ nhảy trực tiếp tới bài học và vị trí từ đó.
 * - Hỗ trợ phím tắt: nhấn 'D' ở bất kỳ đâu để bật, 'Esc' để đóng.
 */
import { useEffect, useMemo, useRef, useState } from 'react';
import {
  BookOpen,
  ExternalLink,
  Loader2,
  Search,
  Sparkles,
  Volume2,
  X,
} from 'lucide-react';
import { ALL_WORDS } from '../data/allWords.js';
import { useApp } from '../lib/store.jsx';
import { useSpeech } from './ui.jsx';
import { translateSelection } from './AnnotatableText.jsx';

export default function QuickDictionaryModal() {
  const {
    dictionaryOpen,
    dictionaryWord,
    closeDictionary,
    openLesson,
    settings,
  } = useApp();
  const { speak, supported: speechSupported } = useSpeech();

  const [query, setQuery] = useState('');
  const [onlineResult, setOnlineResult] = useState('');
  const [loadingOnline, setLoadingOnline] = useState(false);
  const inputRef = useRef(null);

  // Khi mở modal, nạp từ ban đầu (nếu có) và focus vào input
  useEffect(() => {
    if (dictionaryOpen) {
      const initial = (dictionaryWord || '').trim();
      setQuery(initial);
      setOnlineResult('');
      setLoadingOnline(false);
      setTimeout(() => {
        if (inputRef.current) {
          inputRef.current.focus();
          if (initial) {
            inputRef.current.select();
          }
        }
      }, 50);
    }
  }, [dictionaryOpen, dictionaryWord]);

  // Đóng modal khi nhấn Escape
  useEffect(() => {
    if (!dictionaryOpen) return;
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        closeDictionary();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [dictionaryOpen, closeDictionary]);

  // Tìm kiếm tức thì trong 600 từ TOEIC
  const matchedCurated = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return [];
    return ALL_WORDS.filter(
      (item) =>
        item.word.toLowerCase().includes(q) ||
        (item.defVi && item.defVi.toLowerCase().includes(q)),
    ).slice(0, 8);
  }, [query]);

  // Nếu không khớp từ TOEIC chính xác, gọi dịch trực tuyến
  useEffect(() => {
    const clean = query.trim();
    if (!clean) {
      setOnlineResult('');
      setLoadingOnline(false);
      return;
    }

    // Nếu từ khớp chính xác trong từ điển nội bộ thì không cần gọi mạng
    const exactMatch = ALL_WORDS.find(
      (w) => w.word.toLowerCase() === clean.toLowerCase(),
    );
    if (exactMatch) {
      setOnlineResult('');
      setLoadingOnline(false);
      return;
    }

    let active = true;
    setLoadingOnline(true);
    const timer = setTimeout(async () => {
      try {
        const res = await translateSelection(clean, settings);
        if (active) {
          setOnlineResult(res);
          setLoadingOnline(false);
        }
      } catch {
        if (active) {
          setOnlineResult('Không thể tra từ lúc này.');
          setLoadingOnline(false);
        }
      }
    }, 280);

    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, [query, settings]);

  if (!dictionaryOpen) return null;

  const handleJumpToLesson = (lessonId, word) => {
    closeDictionary();
    openLesson(lessonId, 'vocab', word);
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in duration-150"
      onClick={(e) => {
        if (e.target === e.currentTarget) closeDictionary();
      }}
    >
      <div className="flex w-full max-w-lg flex-col overflow-hidden rounded-2xl border-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg)] shadow-2xl text-[var(--color-duo-ink)] max-h-[85vh]">
        {/* Header */}
        <div className="flex items-center justify-between border-b-2 border-[var(--color-duo-line)] px-4 py-3 bg-[var(--color-duo-bg-soft)]">
          <div className="flex items-center gap-2">
            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-[var(--color-duo-green-light)] text-[var(--color-duo-green-dark)] shadow-2xs">
              <BookOpen className="h-4 w-4" />
            </span>
            <h3 className="text-sm font-black uppercase tracking-wider text-[var(--color-duo-ink)]">
              Từ Điển TOEIC &amp; Tra Cứu
            </h3>
          </div>
          <button
            type="button"
            onClick={closeDictionary}
            className="rounded-lg p-1 text-[var(--color-duo-muted)] hover:bg-[var(--color-duo-line)] hover:text-[var(--color-duo-ink)] transition-colors"
            title="Đóng (Esc)"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Ô tìm kiếm */}
        <div className="p-3.5 border-b border-[var(--color-duo-line)]">
          <div className="relative">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--color-duo-muted)]" />
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Nhập từ hoặc cụm từ tiếng Anh..."
              className="w-full rounded-xl border-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg)] pl-9 pr-9 py-2 text-sm font-bold text-[var(--color-duo-ink)] outline-none focus:border-[var(--color-duo-green)] transition-colors placeholder:text-[var(--color-duo-muted)] placeholder:font-normal"
            />
            {query ? (
              <button
                type="button"
                onClick={() => {
                  setQuery('');
                  inputRef.current?.focus();
                }}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 rounded-full p-0.5 text-[var(--color-duo-muted)] hover:text-[var(--color-duo-ink)]"
                title="Xóa ô tìm kiếm"
              >
                <X className="h-4 w-4" />
              </button>
            ) : null}
          </div>
        </div>

        {/* Nội dung kết quả */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {/* 1. Kết quả từ bộ từ vựng 600 từ TOEIC */}
          {matchedCurated.length > 0 && (
            <div>
              <p className="mb-2 text-[11px] font-black uppercase tracking-wider text-[var(--color-duo-green-dark)]">
                Từ vựng trong 600 Essential Words ({matchedCurated.length})
              </p>
              <div className="space-y-2">
                {matchedCurated.map((item) => (
                  <div
                    key={`${item.lessonId}-${item.word}`}
                    className="flex items-start justify-between gap-3 rounded-xl border-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] p-3 transition hover:border-[var(--color-duo-green)]"
                  >
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="text-sm font-black text-[var(--color-duo-ink)]">
                          {item.word}
                        </span>
                        {item.pos && (
                          <span className="rounded-md bg-purple-100 dark:bg-purple-900/40 px-1.5 py-0.5 text-[10px] font-black text-purple-700 dark:text-purple-300">
                            {item.pos}
                          </span>
                        )}
                        <span className="rounded-md bg-[var(--color-duo-bg)] px-1.5 py-0.5 text-[10px] font-black text-[var(--color-duo-muted)] border border-[var(--color-duo-line)]">
                          Lesson {String(item.lessonId).padStart(2, '0')}
                        </span>
                      </div>
                      <p className="mt-1 text-xs font-bold text-[var(--color-duo-green-dark)] leading-snug">
                        {item.defVi}
                      </p>
                    </div>

                    <div className="flex items-center gap-1 shrink-0">
                      {speechSupported && (
                        <button
                          type="button"
                          onClick={() => speak(item.word)}
                          className="rounded-lg p-1.5 text-[var(--color-duo-blue)] hover:bg-[var(--color-duo-blue-light)]/40 transition-colors"
                          title="Nghe phát âm"
                        >
                          <Volume2 className="h-4 w-4" />
                        </button>
                      )}
                      <button
                        type="button"
                        onClick={() => handleJumpToLesson(item.lessonId, item.word)}
                        className="rounded-lg p-1.5 text-[var(--color-duo-green-dark)] hover:bg-[var(--color-duo-green-light)]/40 transition-colors"
                        title="Mở trong bài học"
                      >
                        <ExternalLink className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 2. Dịch nghĩa trực tuyến / từ ngoài bộ 600 từ */}
          {query.trim() && (
            <div>
              <p className="mb-2 text-[11px] font-black uppercase tracking-wider text-sky-600 dark:text-sky-400">
                Nghĩa tra nhanh
              </p>
              <div className="rounded-xl border-2 border-sky-200 dark:border-sky-900/60 bg-sky-50/60 dark:bg-sky-950/30 p-3">
                <div className="flex items-center justify-between gap-2 mb-1.5">
                  <span className="text-xs font-black text-sky-900 dark:text-sky-200">
                    “{query.trim()}”
                  </span>
                  {speechSupported && (
                    <button
                      type="button"
                      onClick={() => speak(query.trim())}
                      className="rounded-md p-1 text-sky-600 hover:bg-sky-100 dark:hover:bg-sky-900/50"
                      title="Nghe phát âm"
                    >
                      <Volume2 className="h-4 w-4" />
                    </button>
                  )}
                </div>

                {loadingOnline ? (
                  <div className="flex items-center gap-2 py-1 text-xs text-slate-500 font-medium">
                    <Loader2 className="h-3.5 w-3.5 animate-spin text-sky-600" />
                    <span>Đang tra cứu nghĩa…</span>
                  </div>
                ) : onlineResult ? (
                  <p className="text-xs font-bold text-sky-950 dark:text-sky-100 leading-relaxed">
                    {onlineResult}
                  </p>
                ) : matchedCurated.length === 0 ? (
                  <p className="text-xs text-slate-400 font-medium italic">
                    Nhập từ để xem nghĩa dịch.
                  </p>
                ) : null}
              </div>
            </div>
          )}

          {/* Khi chưa nhập gì */}
          {!query.trim() && (
            <div className="py-8 text-center">
              <Sparkles className="mx-auto h-8 w-8 text-[var(--color-duo-muted)] mb-2" />
              <p className="text-xs font-bold text-[var(--color-duo-ink)]">
                Tra cứu nhanh toàn bộ 600 từ vựng TOEIC &amp; dịch trực tiếp
              </p>
              <p className="mt-1 text-[11px] text-[var(--color-duo-muted)]">
                Gõ từ vựng tiếng Anh bất kỳ để xem nghĩa tiếng Việt và cách phát âm.
              </p>
              <div className="mt-3 flex flex-wrap justify-center gap-1.5">
                {['contract', 'market', 'assure', 'cancel', 'abide by'].map((w) => (
                  <button
                    key={w}
                    type="button"
                    onClick={() => setQuery(w)}
                    className="rounded-lg border border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] px-2 py-1 text-xs font-bold text-[var(--color-duo-muted)] hover:text-[var(--color-duo-green-dark)] hover:border-[var(--color-duo-green)]"
                  >
                    {w}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between border-t border-[var(--color-duo-line)] px-4 py-2.5 bg-[var(--color-duo-bg-soft)] text-[11px] text-[var(--color-duo-muted)]">
          <span>
            Mẹo: Nhấn phím <kbd className="rounded border border-[var(--color-duo-line)] bg-[var(--color-duo-bg)] px-1.5 py-0.5 font-mono text-[10px] font-bold text-[var(--color-duo-ink)]">D</kbd> bất kỳ lúc nào để mở Từ điển
          </span>
          <button
            type="button"
            onClick={closeDictionary}
            className="rounded-lg bg-[var(--color-duo-line)] px-2.5 py-1 text-xs font-bold text-[var(--color-duo-ink)] hover:opacity-80"
          >
            Đóng
          </button>
        </div>
      </div>
    </div>
  );
}
