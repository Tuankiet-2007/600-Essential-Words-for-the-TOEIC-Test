/**
 * FROZEN CONTRACT — global app store (React context + hooks).
 * Owned by the Lead. Tabs consume the hooks; they must not edit this file.
 */
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { LESSON_STATUS } from '../lib/types.js';
import { ALL_WORDS } from '../data/allWords.js';
import { CUTOFF_HOUR, isDue } from './srs.js';
import { loadLesson, loadLessonIndex, invalidateLessonCache } from '../lib/lessonLoader.js';
import {
  loadProgress,
  loadSettings,
  loadSrs,
  saveProgress,
  saveSettings as persistSettings,
  srsKey,
} from '../lib/storage.js';

const AppCtx = createContext(null);
const CATALOG_WORDS = [...new Map(ALL_WORDS.map((item) => [srsKey(item.lessonId, item.word), item])).values()];
const CATALOG_KEYS = new Set(CATALOG_WORDS.map((item) => srsKey(item.lessonId, item.word)));

/** Count vocabulary items once, accepting canonical and legacy progress keys. */
export function lessonLearnedCount(progress, lessonId) {
  const words = progress?.[`L${String(lessonId).padStart(2, '0')}`]?.words || {};
  return CATALOG_WORDS.filter((item) => {
    if (Number(item.lessonId) !== Number(lessonId)) return false;
    const key = srsKey(lessonId, item.word);
    if (typeof words[key] === 'boolean') return words[key];
    return Object.entries(words).some(([storedKey, learned]) =>
      Boolean(learned) && storedKey.toLowerCase() === item.word.toLowerCase());
  }).length;
}

/** Live due vocabulary keys; orphaned storage entries are reported separately. */
export function selectDueWordKeys(srs, now = new Date()) {
  return CATALOG_WORDS.flatMap((item) => {
    const key = srsKey(item.lessonId, item.word);
    return srs?.[key] && isDue(srs[key], now) ? [key] : [];
  });
}

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
  const [pendingScrollWord, setPendingScrollWord] = useState(null);
  const [dictionaryOpen, setDictionaryOpen] = useState(false);
  const [dictionaryWord, setDictionaryWord] = useState('');
  const [askAiOpen, setAskAiOpen] = useState(false);
  const [askAiContext, setAskAiContext] = useState('');
  const [initialState] = useState(() => {
    try {
      return { progress: loadProgress(), srs: loadSrs(), error: null };
    } catch (error) {
      return { progress: loadProgress(), srs: {}, error: error.message };
    }
  });
  const [progress, setProgress] = useState(initialState.progress);
  const [srs, setSrs] = useState(initialState.srs);
  const [stateError, setStateError] = useState(initialState.error);
  const [srsNow, setSrsNow] = useState(() => new Date());
  const [settings, setSettings] = useState(() => loadSettings());
  const dueWordKeys = useMemo(() => selectDueWordKeys(srs, srsNow), [srs, srsNow]);
  const orphanedCardKeys = useMemo(() => Object.keys(srs || {}).filter((key) => !CATALOG_KEYS.has(key)), [srs]);

  const reloadLearningState = useCallback(() => {
    try {
      const nextSrs = loadSrs();
      const nextProgress = loadProgress();
      setSrs(nextSrs);
      setProgress(nextProgress);
      setStateError(null);
    } catch (error) {
      setStateError(error.message);
    }
    setSrsNow(new Date());
  }, []);

  useEffect(() => {
    let timer;
    const scheduleClock = () => {
      window.clearTimeout(timer);
      const now = new Date();
      const cutoff = new Date(now);
      cutoff.setHours(CUTOFF_HOUR, 0, 0, 0);
      if (cutoff <= now) cutoff.setDate(cutoff.getDate() + 1);
      const nextDue = Object.values(srs || {}).reduce((earliest, card) => {
        const time = new Date(card?.due).getTime();
        return time > now.getTime() ? Math.min(earliest, time) : earliest;
      }, Infinity);
      const delay = Math.max(1, Math.min(60_000, cutoff - now, nextDue - now.getTime()));
      timer = window.setTimeout(() => {
        setSrsNow(new Date());
        scheduleClock();
      }, delay);
    };
    const onStateChanged = (event) => {
      if (event.detail?.kind === 'settings' || event.detail?.kind === 'reset') setSettings(loadSettings());
      if (event.detail?.kind !== 'settings') reloadLearningState();
    };
    const onStorage = (event) => {
      if (event.key === null || event.key?.startsWith('toeic600.')) {
        setSettings(loadSettings());
        reloadLearningState();
      }
    };
    const onFocus = () => { reloadLearningState(); scheduleClock(); };
    const onVisibility = () => { if (document.visibilityState === 'visible') onFocus(); };
    window.addEventListener('toeic600:state-changed', onStateChanged);
    window.addEventListener('storage', onStorage);
    window.addEventListener('focus', onFocus);
    document.addEventListener('visibilitychange', onVisibility);
    scheduleClock();
    return () => {
      window.clearTimeout(timer);
      window.removeEventListener('toeic600:state-changed', onStateChanged);
      window.removeEventListener('storage', onStorage);
      window.removeEventListener('focus', onFocus);
      document.removeEventListener('visibilitychange', onVisibility);
    };
  }, [srs, reloadLearningState]);

  /* ---- load current lesson whenever lessonId changes ---- */
  useEffect(() => {
    let cancelled = false;
    setLessonState({ status: 'loading', lesson: null, source: null });
    loadLesson(lessonId).then((res) => {
      if (cancelled) return;
      setLessonState(res);
      if (res.status === LESSON_STATUS.LOADED) {
        const current = loadProgress();
        const key = `L${String(lessonId).padStart(2, '0')}`;
        const next = {
          ...current,
          [key]: { ...(current[key] || {}), lastOpened: new Date().toISOString() },
        };
        try {
          saveProgress(next);
          setProgress(next);
        } catch (error) {
          setStateError(error.message);
        }
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
    const next = persistSettings(patch);
    setSettings(next);
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

  const openLesson = useCallback((id, nextTab = 'vocab', targetWord = null) => {
    setReviewThemeId(null);
    setActiveView('lesson');
    if (id) setLessonId(id);
    if (nextTab) setTab(nextTab);
    if (targetWord) setPendingScrollWord(targetWord);
  }, []);

  const openDictionary = useCallback((initialWord = '') => {
    setDictionaryWord(initialWord);
    setDictionaryOpen(true);
  }, []);

  const closeDictionary = useCallback(() => {
    setDictionaryOpen(false);
  }, []);

  const openAskAi = useCallback((contextOrPrompt = '') => {
    setAskAiContext(contextOrPrompt);
    setAskAiOpen(true);
  }, []);

  const closeAskAi = useCallback(() => {
    setAskAiOpen(false);
  }, []);

  const toggleAskAi = useCallback((contextOrPrompt = '') => {
    setAskAiOpen((prev) => {
      if (!prev && contextOrPrompt) {
        setAskAiContext(contextOrPrompt);
      }
      return !prev;
    });
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
      pendingScrollWord,
      setPendingScrollWord,
      dictionaryOpen,
      dictionaryWord,
      openDictionary,
      closeDictionary,
      askAiOpen,
      askAiContext,
      openAskAi,
      closeAskAi,
      toggleAskAi,
      lessonState,
      lesson: lessonState.lesson,
      lessonIndex,
      refreshIndex,
      progress,
      setProgress,
      srs,
      setSrs,
      srsNow,
      dueWordKeys,
      orphanedCardKeys,
      stateError,
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
      pendingScrollWord,
      dictionaryOpen,
      dictionaryWord,
      openDictionary,
      closeDictionary,
      askAiOpen,
      askAiContext,
      openAskAi,
      closeAskAi,
      toggleAskAi,
      lessonState,
      lessonIndex,
      refreshIndex,
      progress,
      srs,
      setSrs,
      srsNow,
      dueWordKeys,
      orphanedCardKeys,
      stateError,
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
