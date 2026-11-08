/**
 * FROZEN CONTRACT — LocalStorage persistence for progress, SRS state, settings.
 * All keys are namespaced "toeic600.*". IndexedDB is unnecessary at this data size.
 */

const NS = 'toeic600';
const KEY_SETTINGS = `${NS}.settings`;
const KEY_SRS = `${NS}.srs`;
const KEY_PROGRESS = `${NS}.progress`;
const KEY_HISTORY = `${NS}.history`;
const KEY_ANNOTATIONS = `${NS}.annotations`;

function read(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function write(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch {
    return false;
  }
}

/* ---------------- Settings (BYOK & Feature Routing) ---------------- */

export const DEFAULT_SETTINGS = {
  provider: 'gemini', // 'gemini' | 'openai' | 'ollama' (for AI Sentence Lab)
  aiLabProvider: 'gemini', // 'gemini' | 'openai' | 'ollama'
  lookupProvider: 'free', // 'free' | 'gemini' | 'openai' | 'ollama' (for Tra từ)
  geminiKey: '',
  openaiKey: '',
  ollamaUrl: 'http://localhost:11434',
  ollamaModel: 'llama3.1',
  model: 'gemini-2.5-flash',
  geminiModel: 'gemini-2.5-flash',
  openaiModel: 'gpt-4o-mini',
  ttsVoice: 'en-US',
  ttsRate: 0.95,
  highlightEnabled: true,
};

export function loadSettings() {
  return { ...DEFAULT_SETTINGS, ...read(KEY_SETTINGS, {}) };
}

export function saveSettings(patch) {
  const next = { ...loadSettings(), ...patch };
  write(KEY_SETTINGS, next);
  return next;
}

/* ---------------- SRS ---------------- */

/** @typedef {{ease:number, interval:number, reps:number, due:string, lapses:number, lastGrade:number}} SrsCard */

export function loadSrs() {
  return read(KEY_SRS, {});
}

export function saveSrs(map) {
  write(KEY_SRS, map);
  return map;
}

/** Stable SRS key for one vocabulary item. */
export function srsKey(lessonId, word) {
  return `L${String(lessonId).padStart(2, '0')}:${String(word).toLowerCase()}`;
}

/* ---------------- Progress ---------------- */

/** @typedef {{learned:boolean, flashcardGrades:number[], practiceScore?:{correct:number,total:number}, lastOpened?:string}} LessonProgress */

export function loadProgress() {
  return read(KEY_PROGRESS, {});
}

export function saveProgress(map) {
  write(KEY_PROGRESS, map);
  return map;
}

export function markWordLearned(lessonId, word, learned = true) {
  const all = loadProgress();
  const key = `L${String(lessonId).padStart(2, '0')}`;
  const entry = all[key] || { words: {}, practiceScore: null, lastOpened: null };
  entry.words = entry.words || {};
  entry.words[srsKey(lessonId, word)] = learned;
  all[key] = entry;
  saveProgress(all);
  return all;
}

/* ---------------- Practice history ---------------- */

export function loadHistory() {
  return read(KEY_HISTORY, []);
}

export function pushHistory(record) {
  const all = loadHistory();
  const id = record?.id || `hist_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
  const at = record?.at || new Date().toISOString();
  all.unshift({ ...record, id, at });
  const trimmed = all.slice(0, 200);
  write(KEY_HISTORY, trimmed);
  return trimmed;
}

export function deleteHistoryItem(idOrAt) {
  const all = loadHistory();
  const next = all.filter((item) => item.id !== idOrAt && item.at !== idOrAt);
  write(KEY_HISTORY, next);
  return next;
}

export function clearHistory(lessonId = null) {
  if (lessonId === null || lessonId === undefined) {
    write(KEY_HISTORY, []);
    return [];
  }
  const all = loadHistory();
  const next = all.filter((item) => Number(item.lessonId) !== Number(lessonId));
  write(KEY_HISTORY, next);
  return next;
}

/* ---------------- Annotations (Highlight / Note / Lookup) ---------------- */

export function loadAllAnnotations() {
  return read(KEY_ANNOTATIONS, {});
}

export function loadAnnotations(scopeId) {
  const all = loadAllAnnotations();
  if (!scopeId) return all;
  return Array.isArray(all[scopeId]) ? all[scopeId] : [];
}

export function saveAnnotation(scopeId, item) {
  if (!scopeId || !item) return [];
  const all = loadAllAnnotations();
  const list = Array.isArray(all[scopeId]) ? [...all[scopeId]] : [];
  const id = item.id || `ann_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
  const idx = list.findIndex((x) => x.id === id);
  const record = { ...item, id, updatedAt: new Date().toISOString() };
  if (idx >= 0) list[idx] = { ...list[idx], ...record };
  else list.push(record);
  all[scopeId] = list;
  write(KEY_ANNOTATIONS, all);
  return list;
}

export function deleteAnnotation(scopeId, id) {
  if (!scopeId) return [];
  const all = loadAllAnnotations();
  const list = Array.isArray(all[scopeId]) ? all[scopeId] : [];
  const next = list.filter((x) => x.id !== id);
  all[scopeId] = next;
  write(KEY_ANNOTATIONS, all);
  return next;
}

/** Reset everything (Settings screen "Xóa toàn bộ tiến độ"). */
export function clearAll() {
  [KEY_SETTINGS, KEY_SRS, KEY_PROGRESS, KEY_HISTORY, KEY_ANNOTATIONS].forEach((k) => {
    try {
      localStorage.removeItem(k);
    } catch {
      /* ignore */
    }
  });
}

/**
 * Export all user state to a downloadable JSON object.
 */
export function exportAllData() {
  return {
    version: 1,
    appName: 'Barron 600 Essential Words for the TOEIC',
    exportedAt: new Date().toISOString(),
    data: {
      settings: loadSettings(),
      srs: loadSrs(),
      progress: loadProgress(),
      history: loadHistory(),
      annotations: loadAllAnnotations(),
    },
  };
}

/**
 * Import and restore state from a backup JSON payload.
 */
export function importAllData(payload) {
  if (!payload || typeof payload !== 'object') {
    throw new Error('Định dạng file sao lưu không hợp lệ.');
  }

  const d = payload.data || payload;

  if (d.settings && typeof d.settings === 'object') {
    saveSettings(d.settings);
  }
  if (d.srs && typeof d.srs === 'object') {
    saveSrs(d.srs);
  }
  if (d.progress && typeof d.progress === 'object') {
    saveProgress(d.progress);
  }
  if (Array.isArray(d.history)) {
    write(KEY_HISTORY, d.history);
  }
  if (d.annotations && typeof d.annotations === 'object') {
    write(KEY_ANNOTATIONS, d.annotations);
  }

  return true;
}

export default {
  loadSettings,
  saveSettings,
  loadSrs,
  saveSrs,
  loadProgress,
  markWordLearned,
  loadHistory,
  pushHistory,
  deleteHistoryItem,
  clearHistory,
  loadAllAnnotations,
  loadAnnotations,
  saveAnnotation,
  deleteAnnotation,
  clearAll,
  exportAllData,
  importAllData,
};
