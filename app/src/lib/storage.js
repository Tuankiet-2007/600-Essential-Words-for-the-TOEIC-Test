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
    dispatchStateChanged(key.slice(NS.length + 1));
    return true;
  } catch (error) {
    const failure = new Error(`Không thể lưu dữ liệu (${key}).`);
    failure.cause = error;
    throw failure;
  }
}

function isFiniteNumber(value) {
  return typeof value === 'number' && Number.isFinite(value);
}

/** Validate and normalize one persisted SRS card. */
export function normalizeSrsCard(card, key = 'unknown') {
  if (!card || typeof card !== 'object' || Array.isArray(card)) {
    throw new Error(`Thẻ SRS không hợp lệ: ${key}`);
  }
  const numeric = ['ease', 'interval', 'reps', 'lapses', 'lastGrade'];
  const result = { ...card };
  for (const field of numeric) {
    const value = result[field];
    const number = typeof value === 'string' && value.trim() !== '' ? Number(value) : value;
    if (!isFiniteNumber(number)) throw new Error(`Trường SRS ${field} không hợp lệ: ${key}`);
    result[field] = number;
  }
  if (result.ease < 1 || result.interval < 0 || result.reps < 0 || result.lapses < 0 || result.lastGrade < 0 || result.lastGrade > 4) {
    throw new Error(`Giá trị SRS ngoài phạm vi: ${key}`);
  }
  if (typeof result.due !== 'string' || Number.isNaN(new Date(result.due).getTime())) {
    throw new Error(`Ngày đáo hạn SRS không hợp lệ: ${key}`);
  }
  for (const field of ['interval', 'reps', 'lapses', 'lastGrade']) {
    if (!Number.isSafeInteger(result[field])) throw new Error(`Trường SRS ${field} phải là số nguyên: ${key}`);
  }
  for (const field of ['version', 'learningStep']) {
    if (result[field] !== undefined && (!Number.isSafeInteger(result[field]) || result[field] < 0)) {
      throw new Error(`Trường SRS ${field} không hợp lệ: ${key}`);
    }
  }
  if (result.state !== undefined && !['new', 'learning', 'review', 'relearning'].includes(result.state)) {
    throw new Error(`Trạng thái SRS không hợp lệ: ${key}`);
  }
  if (result.lastReviewedAt !== undefined && (typeof result.lastReviewedAt !== 'string' || Number.isNaN(new Date(result.lastReviewedAt).getTime()))) {
    throw new Error(`Ngày ôn gần nhất không hợp lệ: ${key}`);
  }
  if (result.processedReviewIds !== undefined && (!Array.isArray(result.processedReviewIds) || result.processedReviewIds.some((id) => typeof id !== 'string' || !id.trim()))) {
    throw new Error(`Danh sách review ID không hợp lệ: ${key}`);
  }
  if (result.reviewLog !== undefined && !Array.isArray(result.reviewLog)) throw new Error(`Lịch sử SRS không hợp lệ: ${key}`);
  return result;
}

export function validateSrsMap(map) {
  if (!map || typeof map !== 'object' || Array.isArray(map)) throw new Error('Dữ liệu SRS không hợp lệ.');
  const normalized = {};
  for (const [key, card] of Object.entries(map)) {
    if (!/^L\d+:[^\s].*$/u.test(key) || !key.slice(key.indexOf(':') + 1).trim()) throw new Error(`Khóa SRS không hợp lệ: ${key}`);
    normalized[key] = normalizeSrsCard(card, key);
  }
  return normalized;
}

function dispatchStateChanged(kind) {
  try {
    if (typeof window !== 'undefined' && typeof window.dispatchEvent === 'function') {
      window.dispatchEvent(new CustomEvent('toeic600:state-changed', { detail: { kind } }));
    } else if (typeof globalThis !== 'undefined' && typeof globalThis.dispatchEvent === 'function') {
      globalThis.dispatchEvent(new CustomEvent('toeic600:state-changed', { detail: { kind } }));
    }
  } catch {
    // Event delivery must never turn a successful persistence operation into a failure.
  }
}

/* ---------------- Settings (BYOK & Feature Routing) ---------------- */

export const DEFAULT_SETTINGS = {
  provider: 'gemini', // 'gemini' | 'openai' | 'ollama' (for AI Sentence Lab)
  aiLabProvider: 'gemini', // 'gemini' | 'openai' | 'ollama'
  lookupProvider: 'free', // 'free' | 'gemini' | 'openai' | 'ollama' (for Tra từ)
  geminiKey: '',
  geminiUrl: '', // Tùy chọn: URL proxy riêng (mặc định https://generativelanguage.googleapis.com)
  openaiKey: '',
  openaiUrl: '', // Tùy chọn: Base URL riêng (mặc định https://api.openai.com/v1)
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
  const raw = localStorage.getItem(KEY_SRS);
  return validateSrsMap(raw ? JSON.parse(raw) : {});
}

export function saveSrs(map) {
  const normalized = validateSrsMap(map);
  write(KEY_SRS, normalized);
  return normalized;
}

/** Stable SRS key for one vocabulary item. */
export function srsKey(lessonId, word) {
  const lesson = Number(lessonId);
  const normalizedWord = typeof word === 'string' ? word.trim().replace(/\s+/g, ' ').toLowerCase() : '';
  if (!Number.isSafeInteger(lesson) || lesson < 1 || !normalizedWord) throw new Error('Bài hoặc từ SRS không hợp lệ.');
  return `L${String(lesson).padStart(2, '0')}:${normalizedWord}`;
}

/* ---------------- Progress ---------------- */

/** @typedef {{learned:boolean, flashcardGrades:number[], practiceScore?:{correct:number,total:number}, lastOpened?:string}} LessonProgress */

export function loadProgress() {
  return read(KEY_PROGRESS, {});
}

export function saveProgress(map) {
  if (!map || typeof map !== 'object' || Array.isArray(map)) throw new Error('Dữ liệu tiến độ không hợp lệ.');
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
    } catch (error) {
      const failure = new Error(`Không thể xóa dữ liệu (${k}).`);
      failure.cause = error;
      throw failure;
    }
  });
  dispatchStateChanged('reset');
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
  if (!d || typeof d !== 'object' || Array.isArray(d)) throw new Error('Định dạng file sao lưu không hợp lệ.');
  // Validate every supplied section before the first mutation.
  if (d.srs !== undefined) validateSrsMap(d.srs);
  for (const section of ['settings', 'progress', 'annotations']) {
    if (d[section] !== undefined && (!d[section] || typeof d[section] !== 'object' || Array.isArray(d[section]))) {
      throw new Error(`Dữ liệu ${section} không hợp lệ.`);
    }
  }
  if (d.history !== undefined && !Array.isArray(d.history)) throw new Error('Lịch sử không hợp lệ.');

  if (d.settings && typeof d.settings === 'object' && !Array.isArray(d.settings)) {
    saveSettings(d.settings);
  }
  if (d.srs !== undefined) {
    saveSrs(validateSrsMap(d.srs));
  }
  if (d.progress && typeof d.progress === 'object' && !Array.isArray(d.progress)) {
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
