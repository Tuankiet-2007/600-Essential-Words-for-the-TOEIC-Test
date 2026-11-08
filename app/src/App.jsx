/**
 * App shell: sidebar + per-unit header + 5 tabs.
 * Owned by the Lead. Tab switching is intentionally unconditional so that
 * every tab stays mounted and reachable even while lesson data is missing.
 */
import { lazy, Suspense, useEffect, useState } from 'react';
import {
  FileAudio,
  FileQuestion,
  Home,
  Layers,
  LayoutDashboard,
  Menu,
  Moon,
  Settings,
  Sparkles,
  Sun,
  Wand2,
} from 'lucide-react';
import Sidebar from './components/Sidebar.jsx';
import ReviewView from './components/ReviewView.jsx';
import DashboardView from './components/DashboardView.jsx';
import SettingsView from './components/SettingsView.jsx';
import AnnotatableContainer, { HighlightToggleBar } from './components/AnnotatableText.jsx';
import { Badge, Button, Card, EmptyState, Spinner, TabBar } from './components/ui.jsx';
import { AppProvider, useApp } from './lib/store.jsx';
import { LESSON_STATUS } from './lib/types.js';
import { audioUrlFor, photoUrlFor } from './lib/assets.js';
import { LESSON_TITLES, themeForLesson } from './data/curriculum.js';

const SrsStandaloneView = lazy(() => import('./components/SrsStandaloneView.jsx'));
const Tab1Vocabulary = lazy(() => import('./tabs/Tab1Vocabulary.jsx'));
const Tab2Flashcards = lazy(() => import('./tabs/Tab2Flashcards.jsx'));
const Tab3Srs = lazy(() => import('./tabs/Tab3Srs.jsx'));
const Tab4AiLab = lazy(() => import('./tabs/Tab4AiLab.jsx'));
const Tab5Practice = lazy(() => import('./tabs/Tab5Practice.jsx'));

const TABS = [
  { id: 'vocab', label: 'Học Từ Vựng', icon: Layers },
  { id: 'flashcard', label: 'Flashcard Ngữ Cảnh', icon: Wand2 },
  { id: 'ai', label: 'AI Sentence Lab', icon: Wand2 },
  { id: 'practice', label: 'Luyện Đề & Audio', icon: FileAudio },
];

function LessonHeader() {
  const { lesson, lessonState, lessonId, lessonIndex } = useApp();
  const theme = themeForLesson(lessonId);
  const title = lesson?.title || LESSON_TITLES[lessonId] || `Lesson ${lessonId}`;
  const exists = lessonIndex
    ? lessonIndex[lessonId] !== false
    : lessonState.status === LESSON_STATUS.LOADED;

  return (
    <Card className="mb-4 flex flex-wrap items-center justify-between gap-3 px-4 py-3">
      <div className="min-w-0">
        <div className="flex flex-wrap items-center gap-2">
          <Badge tone="brand">Lesson {String(lessonId).padStart(2, '0')}</Badge>
          {theme ? <Badge tone="slate">{theme.theme_name}</Badge> : null}
          {exists ? (
            <Badge tone="emerald">Đã trích xuất</Badge>
          ) : (
            <Badge tone="amber">Chưa trích xuất</Badge>
          )}
        </div>
        <h2 className="mt-1.5 truncate text-xl font-bold text-slate-900">{title}</h2>
        <p className="text-xs text-slate-500">
          {lesson ? `${lesson.words_to_learn.length} từ vựng mục tiêu · ` : ''}
          <span className="font-mono">{audioUrlFor(lessonId)}</span>
        </p>
      </div>
      <div className="flex items-center gap-2.5">
        <img
          src={photoUrlFor(lessonId)}
          alt={`Part 1 cho lesson ${lessonId}`}
          className="h-12 w-16 rounded-lg border border-slate-200 object-cover"
          onError={(e) => {
            e.currentTarget.style.display = 'none';
          }}
        />
      </div>
    </Card>
  );
}

function NotExtractedNotice() {
  const { lessonId, refreshIndex } = useApp();
  const [busy, setBusy] = useState(false);
  return (
    <EmptyState
      icon={FileQuestion}
      title={`Lesson ${String(lessonId).padStart(2, '0')} — Chưa trích xuất`}
      description={`Chưa có tệp lessons_json/lesson_${String(lessonId).padStart(2, '0')}.json. Hãy chạy OCR (scripts/run_ocr_pipeline.py) để sinh dữ liệu, sau đó bấm "Quét lại".`}
      action={
        <Button
          variant="primary"
          disabled={busy}
          onClick={async () => {
            setBusy(true);
            try {
              await refreshIndex(true);
            } finally {
              setBusy(false);
            }
          }}
        >
          <FileAudio className="h-4 w-4" />
          {busy ? 'Đang quét…' : 'Quét lại thư mục lessons_json/'}
        </Button>
      }
    />
  );
}

function Workspace() {
  const {
    tab,
    setTab,
    lessonId,
    lessonState,
    lesson,
    reviewThemeId,
    activeView,
    openDashboard,
    openSettings,
  } = useApp();
  const [menuOpen, setMenuOpen] = useState(false);
  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem('toeic_theme') || 'light';
    } catch {
      return 'light';
    }
  });

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
    try {
      localStorage.setItem('toeic_theme', theme);
    } catch {
      /* ignore */
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  const loading = lessonState.status === 'loading';
  const missing = !loading && lessonState.status !== LESSON_STATUS.LOADED;
  const scopeId = reviewThemeId
    ? `review-${reviewThemeId}`
    : `lesson-${lessonId}-${tab}`;

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [tab, reviewThemeId, activeView]);

  return (
    <div className="flex min-h-screen bg-slate-50 transition-colors">
      <Sidebar open={menuOpen} onClose={() => setMenuOpen(false)} />

      <main className="min-w-0 flex-1">
        {/* Top Header Bar: Logo/Menu bên trái (chỉ mobile) & Theme/Cài đặt góc phải */}
        <header className="sticky top-0 z-20 flex h-14 items-center justify-between border-b-2 border-[var(--color-duo-line)] bg-white/95 px-4 backdrop-blur-sm sm:px-6">
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setMenuOpen(true)}
              aria-label="Mở danh sách bài học"
              className="lg:hidden"
            >
              <Menu className="h-5 w-5 text-[var(--color-duo-ink)]" />
            </Button>
            {/* Chỉ hiện logo 600 WORDS trên mobile khi không có sidebar */}
            <button
              type="button"
              onClick={openDashboard}
              className="flex items-center gap-2 text-left font-black tracking-wider text-[var(--color-duo-green-dark)] hover:opacity-90 lg:hidden"
            >
              <span className="text-base">600 WORDS</span>
            </button>
          </div>

          <div className="flex items-center gap-1.5 sm:gap-2">
            {activeView !== 'dashboard' && (
              <Button
                size="sm"
                variant="ghost"
                onClick={openDashboard}
                title="Về Dashboard"
                className="font-bold text-[var(--color-duo-gray)] hover:text-[var(--color-duo-ink)]"
              >
                <Home className="h-4 w-4" />
                <span className="hidden sm:inline">Dashboard</span>
              </Button>
            )}

            {/* Nút chuyển đổi Theme Tối / Sáng */}
            <button
              type="button"
              onClick={toggleTheme}
              title={theme === 'dark' ? 'Chuyển sang Giao diện Sáng' : 'Chuyển sang Giao diện Tối'}
              className="flex h-9 w-9 items-center justify-center rounded-xl border-2 border-[var(--color-duo-line)] text-[var(--color-duo-ink)] transition-colors hover:bg-[var(--color-duo-bg-soft)] active:scale-95"
            >
              {theme === 'dark' ? (
                <Sun className="h-4 w-4 text-amber-400" />
              ) : (
                <Moon className="h-4 w-4 text-slate-600" />
              )}
            </button>

            {/* Icon Cài đặt ở góc trên bên phải */}
            <button
              type="button"
              onClick={openSettings}
              title="Cài đặt & API"
              className={`flex h-9 w-9 items-center justify-center rounded-xl border-2 transition-colors active:scale-95 ${
                activeView === 'settings'
                  ? 'border-[var(--color-duo-purple)] bg-purple-50 text-[var(--color-duo-purple-dark)]'
                  : 'border-[var(--color-duo-line)] text-[var(--color-duo-gray)] hover:bg-[var(--color-duo-bg-soft)] hover:text-[var(--color-duo-ink)]'
              }`}
            >
              <Settings className="h-4 w-4" />
            </button>
          </div>
        </header>

        <div className="mx-auto max-w-5xl px-3 py-4 sm:px-6 sm:py-6">
          {activeView === 'dashboard' ? (
            <Suspense fallback={<Spinner label="Đang tải Dashboard…" />}>
              <DashboardView />
            </Suspense>
          ) : activeView === 'srs' ? (
            <Suspense fallback={<Spinner label="Đang tải Ôn Tập Giãn Cách…" />}>
              <SrsStandaloneView />
            </Suspense>
          ) : activeView === 'settings' ? (
            <Suspense fallback={<Spinner label="Đang tải Cài Đặt…" />}>
              <SettingsView />
            </Suspense>
          ) : reviewThemeId ? (
            /* ---- Word Review theo chu de: trang rieng, khong kem tab cua 1 bai ---- */
            <Suspense fallback={<Spinner label="Đang tải Word Review…" />}>
              <div className="mb-3">
                <HighlightToggleBar scopeId={scopeId} />
              </div>
              <AnnotatableContainer scopeId={scopeId}>
                <ReviewView themeId={reviewThemeId} />
              </AnnotatableContainer>
            </Suspense>
          ) : (
            <>
              <LessonHeader />

              <div className="mb-3">
                <HighlightToggleBar scopeId={scopeId} />
              </div>

              <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
                <TabBar tabs={TABS} active={tab} onChange={setTab} />
                <AnnotatableContainer scopeId={scopeId} className="p-4">
                  {loading ? (
                    <Spinner label="Đang tải dữ liệu bài học…" />
                  ) : missing ? (
                    <Suspense fallback={<Spinner />}>
                      {tab === 'ai' ? (
                        <Tab4AiLab lesson={null} />
                      ) : tab === 'practice' ? (
                        <Tab5Practice lesson={null} />
                      ) : (
                        <NotExtractedNotice />
                      )}
                    </Suspense>
                  ) : (
                    <Suspense fallback={<Spinner />}>
                      {tab === 'vocab' && <Tab1Vocabulary lesson={lesson} />}
                      {tab === 'flashcard' && <Tab2Flashcards lesson={lesson} />}
                      {tab === 'srs' && <Tab3Srs lesson={lesson} />}
                      {tab === 'ai' && <Tab4AiLab lesson={lesson} />}
                      {tab === 'practice' && <Tab5Practice lesson={lesson} />}
                    </Suspense>
                  )}
                </AnnotatableContainer>
              </div>
            </>
          )}

          <p className="mt-5 text-center text-[10px] font-bold uppercase tracking-wider text-slate-300">
            600 WORDS · Barron's TOEIC 3rd
          </p>
        </div>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AppProvider>
      <Workspace />
    </AppProvider>
  );
}
