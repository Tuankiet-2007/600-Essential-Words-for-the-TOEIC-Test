/**
 * FROZEN CONTRACT — global app store (React context + hooks).
 * Owned by the Lead. Tabs consume the hooks; they must not edit this file.
 */
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { LESSON_STATUS } from '../lib/types.js';
import { loadLesson, loadLessonIndex, invalidateLessonCache } from '../lib/lessonLoader.js';
import {
  loadProgress,
  loadSettings,
  loadSrs,
  saveProgress,
  saveSettings as persistSettings,
} from '../lib/storage.js';

const AppCtx = createContext(null);

export function AppProvider({ children }) {
  const [lessonId, setLessonId] = useState(1);
  const [tab, setTab] = useState('vocab');
  /*
   * Word Review theo chu de: khi khac null, Workspace hien trang on tap gop
   * 60 tu cua 5 bai trong chu de (thay cho header + 5 tab cua 1 bai).
   */
  const [reviewThemeId, setReviewThemeId] = useState(null);
  /*
   * activeView: 'dashboard' | 'srs' | 'lesson' | 'settings'
   * Mặc định khi mở trình duyệt luôn ở Dashboard.
   */
  const [activeView, setActiveView] = useState('dashboard');
  const [srsParams, setSrsParams] = useState({ filter: 'due', themeId: null, lessonId: null });

  const [lessonState, setLessonState] = useState({
    status: 'loading',
    lesson: null,
    source: null,
  });

  const [lessonIndex, setLessonIndex] = useState(null);
  const [progress, setProgress] = useState(() => loadProgress());
  const [srs, setSrs] = useState(() => loadSrs());
  const [settings, setSettings] = useState(() => loadSettings());

  /* ---- load current lesson whenever lessonId changes ---- */
  useEffect(() => {
    let cancelled = false;
    setLessonState({ status: 'loading', lesson: null, source: null });
    loadLesson(lessonId).then((res) => {
      if (cancelled) return;
      setLessonState(res);
      if (res.status === LESSON_STATUS.LOADED) {
        setProgress((prev) => {
          const key = `L${String(lessonId).padStart(2, '0')}`;
          const next = {
            ...prev,
            [key]: { ...(prev[key] || {}), lastOpened: new Date().toISOString() },
          };
          saveProgress(next);
          return next;
        });
      }
    });
    return () => {
      cancelled = true;
    };
  }, [lessonId]);

  /* ---- probe which lessons exist (sidebar badges) ---- */
  const refreshIndex = useCallback(async (force = false) => {
    if (force) invalidateLessonCache();
    const idx = await loadLessonIndex();
    setLessonIndex({ ...idx });
    return idx;
  }, []);

  useEffect(() => {
    refreshIndex(false).catch(() => {});
  }, [refreshIndex]);

  const updateSettings = useCallback((patch) => {
    setSettings((prev) => {
      const next = { ...prev, ...patch };
      persistSettings(patch);
      return next;
    });
  }, []);

  const openDashboard = useCallback(() => {
    setReviewThemeId(null);
    setActiveView('dashboard');
  }, []);

  const openSrsReview = useCallback((params = {}) => {
    setReviewThemeId(null);
    setSrsParams((prev) => ({ ...prev, ...params }));
    setActiveView('srs');
  }, []);

  const openSettings = useCallback(() => {
    setReviewThemeId(null);
    setActiveView('settings');
  }, []);

  const openLesson = useCallback((id, nextTab = 'vocab') => {
    setReviewThemeId(null);
    setActiveView('lesson');
    if (id) setLessonId(id);
    if (nextTab) setTab(nextTab);
  }, []);

  const value = useMemo(
    () => ({
      lessonId,
      setLessonId,
      tab,
      setTab,
      reviewThemeId,
      setReviewThemeId,
      activeView,
      setActiveView,
      openDashboard,
      openSrsReview,
      srsParams,
      openSettings,
      openLesson,
      lessonState,
      lesson: lessonState.lesson,
      lessonIndex,
      refreshIndex,
      progress,
      setProgress,
      srs,
      setSrs,
      settings,
      updateSettings,
    }),
    [
      lessonId,
      tab,
      reviewThemeId,
      activeView,
      openDashboard,
      openSrsReview,
      srsParams,
      openSettings,
      openLesson,
      lessonState,
      lessonIndex,
      refreshIndex,
      progress,
      srs,
      settings,
      updateSettings,
    ],
  );

  return <AppCtx.Provider value={value}>{children}</AppCtx.Provider>;
}

export function useApp() {
  const ctx = useContext(AppCtx);
  if (!ctx) throw new Error('useApp must be used inside <AppProvider>');
  return ctx;
}

export default AppCtx;
