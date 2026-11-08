/**
 * Sidebar / Dashboard — 10 themes -> 50 lessons + 10 Word Reviews, with progress.
 * Owned by the Lead.
 */
import { useMemo, useState } from 'react';
import {
  BarChart3,
  BookOpen,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  CircleDashed,
  GraduationCap,
  Layers,
  RefreshCw,
  Search,
  Settings,
  X,
} from 'lucide-react';
import { THEMES, lessonTitle, TOTAL_WORDS } from '../data/curriculum.js';
import { Badge, Button, ProgressBar } from './ui.jsx';
import { srsKey } from '../lib/storage.js';
import { isDue } from '../lib/srs.js';
import { useApp } from '../lib/store.jsx';

function lessonStats(progress, lessonId) {
  const key = `L${String(lessonId).padStart(2, '0')}`;
  const entry = progress[key];
  const learned = entry?.words
    ? Object.values(entry.words).filter(Boolean).length
    : 0;
  return { learned, done: learned >= 12 };
}

export default function Sidebar({ open, onClose }) {
  const {
    lessonId,
    setLessonId,
    lessonIndex,
    progress,
    srs,
    refreshIndex,
    setTab,
    reviewThemeId,
    setReviewThemeId,
    activeView,
    setActiveView,
    openDashboard,
    openSettings,
  } = useApp();
  const [expanded, setExpanded] = useState(() => new Set([1]));
  const [query, setQuery] = useState('');
  const [busy, setBusy] = useState(false);

  const { learnedTotal, availableCount, dueCount } = useMemo(() => {
    let learned = 0;
    for (const k of Object.keys(progress || {})) {
      const w = progress[k]?.words;
      if (w) learned += Object.values(w).filter(Boolean).length;
    }
    const available = lessonIndex
      ? Object.values(lessonIndex).filter(Boolean).length
      : 0;
    const now = new Date();
    const srsCards = Object.values(srs || {});
    const due = srsCards.filter((c) => isDue(c, now)).length;
    return { learnedTotal: learned, availableCount: available, dueCount: due };
  }, [progress, lessonIndex, srs]);

  const toggle = (id) =>
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });

  const onRescan = async () => {
    setBusy(true);
    try {
      await refreshIndex(true);
    } finally {
      setBusy(false);
    }
  };

  const matches = (id, title) => {
    const q = query.trim().toLowerCase();
    if (!q) return true;
    return String(id).includes(q) || title.toLowerCase().includes(q);
  };

  return (
    <>
      {open ? (
        <button
          type="button"
          aria-label="Đóng menu mục lục"
          className="fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-xs transition-opacity duration-200"
          onClick={onClose}
        />
      ) : null}

      <aside
        className={`fixed inset-y-0 left-0 z-50 flex w-72 max-w-[85vw] flex-col border-r-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg)] shadow-2xl transition-transform duration-300 ease-in-out ${
          open ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand */}
        <div className="border-b-2 border-[var(--color-duo-line)] px-3.5 py-3">
          <div className="flex items-center justify-between gap-2">
            <button
              type="button"
              onClick={() => {
                openDashboard?.();
                onClose?.();
              }}
              className="group flex flex-1 items-center gap-2.5 text-left transition-transform active:scale-95"
              title="Về Dashboard"
            >
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[var(--color-duo-green)] text-white shadow-[0_3px_0_0_var(--color-duo-green-dark)] group-hover:brightness-105">
                <GraduationCap className="h-5 w-5" />
              </div>
              <div className="min-w-0">
                <h1 className="truncate text-base font-black tracking-wider text-[var(--color-duo-green-dark)]">
                  600 WORDS
                </h1>
              </div>
            </button>

            <button
              type="button"
              onClick={onClose}
              aria-label="Đóng mục lục"
              title="Đóng mục lục"
              className="flex h-8 w-8 items-center justify-center rounded-lg border border-[var(--color-duo-line)] text-slate-500 hover:bg-[var(--color-duo-bg-soft)] hover:text-[var(--color-duo-ink)]"
            >
              <X className="h-4 w-4" />
            </button>
          </div>

          {/* Overall progress */}
          <div className="mt-3">
            <div className="mb-1 flex items-center justify-between text-[10px] font-black uppercase tracking-wider text-[var(--color-duo-gray)]">
              <span>Tiến độ</span>
              <span className="tabular-nums text-[var(--color-duo-green-dark)]">
                {learnedTotal}/{TOTAL_WORDS}
              </span>
            </div>
            <ProgressBar value={learnedTotal} max={TOTAL_WORDS} tone="emerald" />
          </div>

          <div className="mt-2.5 flex gap-1.5">
            <div className="relative flex-1">
              <Search className="pointer-events-none absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-[var(--color-duo-muted)]" />
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Tìm bài..."
                className="w-full rounded-xl border-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] py-1.5 pl-7 pr-2 text-xs font-semibold text-[var(--color-duo-ink)] outline-none transition-colors placeholder:text-[var(--color-duo-muted)] focus:border-[var(--color-duo-blue)] focus:bg-[var(--color-duo-bg)]"
              />
            </div>
            <Button
              size="sm"
              variant="secondary"
              onClick={onRescan}
              disabled={busy}
              title="Quét lại"
            >
              <RefreshCw className={`h-3 w-3 ${busy ? 'animate-spin' : ''}`} />
            </Button>
          </div>
        </div>

        {/* Theme tree */}
        <nav className="flex-1 overflow-y-auto px-2.5 py-3">
          {THEMES.map((theme) => {
            const isOpen = expanded.has(theme.theme_id);
            const themeLearned = theme.lessons.reduce(
              (sum, id) => sum + lessonStats(progress, id).learned,
              0,
            );
            const themeMax = theme.lessons.length * 12;
            const visibleLessons = theme.lessons.filter((id) => matches(id, lessonTitle(id)));

            if (!visibleLessons.length) return null;

            return (
              <div key={theme.theme_id} className="mb-1.5">
                <button
                  type="button"
                  onClick={() => toggle(theme.theme_id)}
                  className="duo-nav-item"
                >
                  {isOpen ? (
                    <ChevronDown className="h-4 w-4 shrink-0" />
                  ) : (
                    <ChevronRight className="h-4 w-4 shrink-0" />
                  )}
                  <span className="min-w-0 flex-1">
                    <span className="block truncate">{theme.theme_name}</span>
                    <span className="mt-1.5 block">
                      <ProgressBar
                        value={themeLearned}
                        max={themeMax}
                        tone={themeLearned >= themeMax ? 'emerald' : 'brand'}
                      />
                    </span>
                  </span>
                  <span className="shrink-0 text-[10px] tabular-nums text-[var(--color-duo-muted)]">
                    {themeLearned}/{themeMax}
                  </span>
                </button>

                {isOpen ? (
                  <div className="ml-3 border-l-2 border-[var(--color-duo-line)] pl-2">
                    {visibleLessons.map((id) => {
                      const title = lessonTitle(id);
                      const exists = lessonIndex ? lessonIndex[id] : true;
                      const { learned, done } = lessonStats(progress, id);
                      const active =
                        activeView === 'lesson' && !reviewThemeId && id === lessonId;
                      return (
                        <button
                          key={id}
                          type="button"
                          onClick={() => {
                            setReviewThemeId(null);
                            setActiveView?.('lesson');
                            setLessonId(id);
                            setTab('vocab');
                            onClose?.();
                          }}
                          className={`duo-nav-item mb-1 !normal-case !tracking-normal ${
                            active ? 'duo-nav-item-active' : ''
                          }`}
                        >
                          <span
                            className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-[11px] font-extrabold tabular-nums ${
                              active
                                ? 'bg-[var(--color-duo-blue)] text-white'
                                : done
                                  ? 'bg-[var(--color-duo-green)] text-white'
                                  : 'bg-[var(--color-duo-bg-soft)] text-[var(--color-duo-gray)]'
                            }`}
                          >
                            {String(id).padStart(2, '0')}
                          </span>
                          <span className="min-w-0 flex-1">
                            <span className="block truncate text-[12.5px] font-bold">
                              {title}
                            </span>
                            {!exists ? (
                              <span className="text-[10px] font-bold text-[var(--color-duo-orange)]">
                                Chưa trích xuất
                              </span>
                            ) : null}
                          </span>
                          {done ? (
                            <CheckCircle2 className="h-4 w-4 shrink-0 text-[var(--color-duo-green)]" />
                          ) : exists && learned > 0 ? (
                            <span className="shrink-0 text-[10px] font-bold tabular-nums text-[var(--color-duo-muted)]">
                              {learned}/12
                            </span>
                          ) : !exists ? (
                            <CircleDashed className="h-4 w-4 shrink-0 text-[var(--color-duo-orange)]" />
                          ) : null}
                        </button>
                      );
                    })}

                    {/* Word Review for this theme — trang on tap gop 60 tu */}
                    <button
                      type="button"
                      onClick={() => {
                        setActiveView?.('lesson');
                        setReviewThemeId(theme.review_id);
                        onClose?.();
                      }}
                      className="duo-nav-item !normal-case !tracking-normal hover:!bg-[#f3e5ff] hover:!text-[#7c3aad]"
                    >
                      <Layers className="h-4 w-4 shrink-0 text-[var(--color-duo-purple)]" />
                      <span className="flex-1 truncate text-[12px] font-bold text-[#7c3aad]">
                        Word Review {theme.review_id}
                      </span>
                      <Badge tone="violet">{theme.lessons.length} bài</Badge>
                    </button>
                  </div>
                ) : null}
              </div>
            );
          })}
        </nav>

        <div className="border-t-2 border-[var(--color-duo-line)] px-3 py-3">
          <div className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-wide text-[var(--color-duo-muted)]">
            <BookOpen className="h-3.5 w-3.5" />
            <span>50 Lessons · 10 Themes · 10 Word Reviews</span>
          </div>
        </div>
      </aside>
    </>
  );
}

export { lessonStats, srsKey };
