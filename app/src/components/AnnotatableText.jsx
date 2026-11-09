/**
 * AnnotatableText.jsx — Thanh công cụ bôi đen (Highlight / Gạch chân đỏ / Ghi chú / Tra từ trực tiếp).
 *
 * Bám sát thiết kế Image 4:
 *  - HighlightToggleBar({ scopeId }): công tắc bật/tắt "Highlight nội dung" + tooltip (i) + quản lý nhanh.
 *  - AnnotatableContainer({ scopeId, children, className }):
 *      + Bắt sự kiện bôi đen văn bản (hoặc click vào đoạn đã đánh dấu)
 *      + Hiện thanh công cụ nổi màu tối: [Note] | [Tra từ] | [Bảng 5 màu + abc gạch đỏ] | [Delete]
 *      + Hiển thị trực tiếp ghi chú [📝 ... ×] và nghĩa tra từ [🔍 ... ×] ngay kế bên từ/câu trong văn bản.
 *      + Hoàn toàn SSR-safe (không truy cập window/document ngoài useEffect & event handlers).
 */
import { useCallback, useEffect, useRef, useState } from 'react';
import {
  BookOpen,
  Check,
  Highlighter,
  Info,
  Loader2,
  PenLine,
  Search,
  Settings2,
  Trash2,
  Volume2,
  X,
} from 'lucide-react';
import { ALL_WORDS } from '../data/allWords.js';
import { useApp } from '../lib/store.jsx';
import {
  deleteAnnotation,
  loadAnnotations,
  saveAnnotation,
} from '../lib/storage.js';
import { callAiForFeature } from './SettingsView.jsx';
import { useSpeech } from './ui.jsx';

/* ------------------------------------------------------------------ */
/* Bảng màu Highlight & Sự kiện đồng bộ                                */
/* ------------------------------------------------------------------ */

export const HIGHLIGHT_COLORS = [
  { id: 'blue', label: 'Xanh dương nhạt', bg: '#bae6fd', border: '#38bdf8' },
  { id: 'pink', label: 'Hồng phấn', bg: '#fecdd3', border: '#fb7185' },
  { id: 'green', label: 'Xanh lá nhạt', bg: '#bbf7d0', border: '#4ade80' },
  { id: 'yellow', label: 'Vàng tươi', bg: '#fef08a', border: '#facc15' },
  { id: 'orange', label: 'Cam nhạt', bg: '#fed7aa', border: '#fb923c' },
];

const COLOR_MAP = Object.fromEntries(HIGHLIGHT_COLORS.map((c) => [c.id, c.bg]));

const ANN_SYNC_EVENT = 'toeic600:annotations-changed';

function emitAnnotationSync(scopeId) {
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new CustomEvent(ANN_SYNC_EVENT, { detail: { scopeId } }));
  }
}

/* ------------------------------------------------------------------ */
/* Dịch & Tra từ trực tiếp (Bộ nhớ đệm + 600 từ TOEIC + Google/AI)     */
/* ------------------------------------------------------------------ */

// Bộ nhớ đệm tra từ tức thì (0ms) cho các từ đã tra
const TRANSLATION_CACHE = new Map();

/** Tra cứu tức thời 0ms trong 600 từ TOEIC */
export function lookupCuratedWord(text) {
  const clean = String(text ?? '').replace(/\s+/g, ' ').trim().toLowerCase();
  if (!clean) return null;
  const match = ALL_WORDS.find((w) => w.word.toLowerCase() === clean);
  if (match) {
    const pos = match.pos ? `[${match.pos}] ` : '';
    return `${pos}${match.defVi}`;
  }
  return null;
}

async function fetchFreeGoogleTranslate(text) {
  const q = encodeURIComponent(text);
  const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&dt=bd&q=${q}`;

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000);
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    const mainTrans = Array.isArray(data?.[0])
      ? data[0]
          .map((seg) => seg?.[0] || '')
          .join('')
          .trim()
      : '';

    // Nếu là từ đơn/cụm ngắn và có từ điển từ loại (data[1]), lấy thêm từ loại + nghĩa sát nhất
    let dictParts = [];
    if (Array.isArray(data?.[1]) && text.split(/\s+/).length <= 3) {
      dictParts = data[1].slice(0, 2).map((entry) => {
        const pos = entry?.[0] || '';
        const terms = Array.isArray(entry?.[1]) ? entry[1].slice(0, 3).join(', ') : '';
        return pos && terms ? `${pos}: ${terms}` : terms;
      });
    }

    if (mainTrans && dictParts.length > 0) {
      return `${mainTrans} (${dictParts.join(' · ')})`;
    }
    if (mainTrans) return mainTrans;
  } catch {
    /* Thử fallback MyMemory bên dưới */
  }

  try {
    const fallbackUrl = `https://api.mymemory.translated.net/get?q=${q}&langpair=en|vi`;
    const controller2 = new AbortController();
    const timeoutId2 = setTimeout(() => controller2.abort(), 3500);
    const res2 = await fetch(fallbackUrl, { signal: controller2.signal });
    clearTimeout(timeoutId2);
    if (res2.ok) {
      const json2 = await res2.json();
      const t2 = String(json2?.responseData?.translatedText || '').trim();
      if (t2) return t2;
    }
  } catch {
    /* ignore */
  }

  return 'Không thể kết nối máy chủ dịch tự động. Vui lòng kiểm tra mạng.';
}

export async function translateSelection(text, settings) {
  const clean = String(text ?? '').replace(/\s+/g, ' ').trim();
  if (!clean) return '';
  const lower = clean.toLowerCase();

  // 1. Phản hồi tức thì 0ms nếu có trong 600 từ vựng TOEIC
  const curated = lookupCuratedWord(clean);
  if (curated) return curated;

  // 2. Phản hồi tức thì 0ms nếu đã có trong bộ nhớ đệm
  if (TRANSLATION_CACHE.has(lower)) {
    return TRANSLATION_CACHE.get(lower);
  }

  const mode = settings?.lookupProvider || 'free';
  let resText = '';

  if (mode === 'free') {
    resText = await fetchFreeGoogleTranslate(clean);
  } else {
    const prompt = `Dịch ngắn gọn sang tiếng Việt (kèm từ loại nếu là từ đơn, tối đa 25 từ) trong ngữ cảnh TOEIC cho: "${clean}". Chỉ trả về nội dung dịch ngắn gọn, không giải thích dài dòng.`;
    const aiRes = await callAiForFeature(prompt, settings, mode);
    if (aiRes.ok && aiRes.text) {
      resText = aiRes.text.replace(/^["'“”]+|["'“”]+$/g, '').trim();
    } else {
      const freeText = await fetchFreeGoogleTranslate(clean);
      resText = aiRes.missingKey
        ? `${freeText} (Dùng Google Dịch do chưa nhập API key ${mode.toUpperCase()})`
        : freeText;
    }
  }

  if (resText && !resText.startsWith('Không thể kết nối')) {
    TRANSLATION_CACHE.set(lower, resText);
  }
  return resText;
}

/* ------------------------------------------------------------------ */
/* 1. HighlightToggleBar — Thanh bật/tắt Highlight giống Image 4       */
/* ------------------------------------------------------------------ */

export function HighlightToggleBar({ scopeId = 'default' }) {
  const { settings, updateSettings, openSettings, openDictionary } = useApp();
  const [annotations, setAnnotations] = useState([]);
  const [showList, setShowList] = useState(false);
  const [showTip, setShowTip] = useState(false);

  const highlightEnabled = settings?.highlightEnabled !== false;
  const lookupMode = settings?.lookupProvider || 'free';

  const refreshList = useCallback(() => {
    setAnnotations(loadAnnotations(scopeId));
  }, [scopeId]);

  useEffect(() => {
    refreshList();
    const onSync = (e) => {
      if (!e?.detail?.scopeId || e.detail.scopeId === scopeId) {
        refreshList();
      }
    };
    window.addEventListener(ANN_SYNC_EVENT, onSync);
    return () => window.removeEventListener(ANN_SYNC_EVENT, onSync);
  }, [scopeId, refreshList]);

  const handleDeleteOne = (id) => {
    const next = deleteAnnotation(scopeId, id);
    setAnnotations(next);
    emitAnnotationSync(scopeId);
  };

  const handleClearScope = () => {
    const current = loadAnnotations(scopeId);
    current.forEach((item) => deleteAnnotation(scopeId, item.id));
    setAnnotations([]);
    setShowList(false);
    emitAnnotationSync(scopeId);
  };

  return (
    <div className="mb-3 rounded-xl border border-[var(--color-duo-line)] bg-[var(--color-duo-bg)] px-3.5 py-2.5 shadow-xs">
      <div className="flex flex-wrap items-center justify-between gap-3">
        {/* Cụm công tắc Highlight nội dung chuẩn Image 4 */}
        <div className="flex flex-wrap items-center gap-2.5">
          <button
            type="button"
            role="switch"
            aria-checked={highlightEnabled}
            onClick={() => updateSettings({ highlightEnabled: !highlightEnabled })}
            className={`relative inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full transition-colors ${
              highlightEnabled ? 'bg-[#1cb0f6]' : 'bg-slate-300'
            }`}
            title="Bật/tắt thanh công cụ Highlight, Ghi chú và Tra từ khi bôi đen"
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform ${
                highlightEnabled ? 'translate-x-6' : 'translate-x-1'
              }`}
            />
          </button>

          <span className="text-sm font-extrabold italic text-slate-800 select-none">
            Highlight nội dung
          </span>

          <div className="relative">
            <button
              type="button"
              onClick={() => setShowTip((v) => !v)}
              onMouseEnter={() => setShowTip(true)}
              onMouseLeave={() => setShowTip(false)}
              className="inline-flex h-5 w-5 items-center justify-center rounded-full text-slate-400 hover:bg-slate-100 hover:text-slate-600"
              aria-label="Hướng dẫn Highlight nội dung"
            >
              <Info className="h-4 w-4" />
            </button>
            {showTip ? (
              <div className="absolute left-0 top-7 z-40 w-72 rounded-xl border border-slate-200 bg-slate-900 p-3 text-xs leading-relaxed text-white shadow-xl">
                Bôi đen bất kỳ từ hoặc câu nào trong bài để mở thanh công cụ: tô màu highlight, gạch
                chân đỏ <span className="underline decoration-rose-400 font-bold">abc</span>, viết{' '}
                <strong>Ghi chú</strong> hoặc <strong>Tra từ</strong> hiển thị trực tiếp kế bên!
              </div>
            ) : null}
          </div>

          <span className="hidden text-xs text-slate-400 sm:inline">
            · Bôi đen từ hoặc câu để ghi chú, tra từ &amp; tô màu
          </span>
        </div>

        {/* Cụm thông tin nguồn Tra từ & danh sách đánh dấu */}
        <div className="flex flex-wrap items-center gap-2 text-xs">
          {/* Nút mở Từ điển tra cứu nhanh */}
          <button
            type="button"
            onClick={() => openDictionary()}
            className="inline-flex items-center gap-1.5 rounded-lg border-2 border-[var(--color-duo-green)] bg-[var(--color-duo-green-light)]/40 px-2.5 py-1 font-extrabold text-[var(--color-duo-green-dark)] hover:bg-[var(--color-duo-green-light)] active:scale-95 transition-all shadow-2xs"
            title="Mở Từ điển tra từ nhanh (Phím tắt: D)"
          >
            <BookOpen className="h-3.5 w-3.5" />
            <span>Từ điển</span>
          </button>

          <button
            type="button"
            onClick={openSettings}
            className="inline-flex items-center gap-1 rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-1 font-semibold text-slate-600 hover:border-sky-300 hover:bg-sky-50 hover:text-sky-700"
            title="Thay đổi nguồn API Tra từ trong Cài đặt"
          >
            <Settings2 className="h-3.5 w-3.5 text-sky-600" />
            <span>
              Tra từ:{' '}
              <strong className="text-slate-800">
                {lookupMode === 'free'
                  ? 'Google Dịch (Free)'
                  : lookupMode === 'gemini'
                    ? 'Gemini AI'
                    : lookupMode === 'openai'
                      ? 'OpenAI'
                      : 'Ollama'}
              </strong>
            </span>
          </button>

          {annotations.length > 0 ? (
            <>
              <button
                type="button"
                onClick={() => setShowList((s) => !s)}
                className="inline-flex items-center gap-1 rounded-lg bg-amber-50 px-2.5 py-1 font-bold text-amber-800 border border-amber-200 hover:bg-amber-100"
              >
                <Highlighter className="h-3.5 w-3.5" />
                {annotations.length} đánh dấu
              </button>
              <button
                type="button"
                onClick={handleClearScope}
                className="inline-flex items-center gap-1 rounded-lg px-2 py-1 font-semibold text-rose-600 hover:bg-rose-50"
                title="Xóa toàn bộ đánh dấu trên trang này"
              >
                <Trash2 className="h-3.5 w-3.5" />
                Xóa hết
              </button>
            </>
          ) : null}
        </div>
      </div>

      {/* Danh sách đánh dấu/ghi chú thu gọn trên trang hiện tại */}
      {showList && annotations.length > 0 ? (
        <div className="mt-2.5 border-t border-slate-100 pt-2.5">
          <div className="flex flex-wrap gap-2">
            {annotations.map((ann) => (
              <div
                key={ann.id}
                className="inline-flex max-w-full items-center gap-1.5 rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-1 text-xs"
              >
                <span
                  className={`font-semibold text-slate-800 truncate max-w-[14rem] px-1 rounded ${
                    ann.underlineRed ? 'underline decoration-rose-500 decoration-2' : ''
                  }`}
                  style={{
                    backgroundColor:
                      ann.color && COLOR_MAP[ann.color] ? COLOR_MAP[ann.color] : 'transparent',
                  }}
                >
                  {ann.text}
                </span>
                {ann.note ? (
                  <span className="text-rose-600 font-medium truncate max-w-[12rem]">
                    📝 {ann.note}
                  </span>
                ) : null}
                {ann.translation ? (
                  <span className="text-sky-700 font-medium truncate max-w-[12rem]">
                    🔍 {ann.translation}
                  </span>
                ) : null}
                <button
                  type="button"
                  onClick={() => handleDeleteOne(ann.id)}
                  className="ml-1 rounded text-slate-400 hover:text-rose-600"
                  title="Xóa đánh dấu này"
                >
                  <X className="h-3.5 w-3.5" />
                </button>
              </div>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Helper DOM: Unwrap & Áp dụng Highlight + Ghi chú + Dịch trực tiếp   */
/* ------------------------------------------------------------------ */

function clearDomAnnotations(container) {
  if (!container) return;
  container.querySelectorAll('.user-ann-note, .user-ann-trans').forEach((badge) => {
    badge.remove();
  });
  const parentsToNormalize = new Set();
  container.querySelectorAll('.user-ann-wrap').forEach((wrap) => {
    const parent = wrap.parentNode;
    if (!parent) return;
    while (wrap.firstChild) {
      parent.insertBefore(wrap.firstChild, wrap);
    }
    wrap.remove();
    parentsToNormalize.add(parent);
  });
  parentsToNormalize.forEach((p) => {
    try {
      p.normalize();
    } catch {
      /* ignore */
    }
  });
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function collectEligibleTextNodes(container) {
  const nodes = [];
  const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      if (!node.nodeValue) return NodeFilter.FILTER_REJECT;
      const parent = node.parentElement;
      if (!parent) return NodeFilter.FILTER_REJECT;
      if (
        parent.closest(
          'button:not(.duo-choice), input, textarea, select, script, style, .user-ann-toolbar, .user-ann-note, .user-ann-trans, .user-ann-wrap, [data-no-annotate="true"]',
        )
      ) {
        return NodeFilter.FILTER_REJECT;
      }
      return NodeFilter.FILTER_ACCEPT;
    },
  });

  let current = walker.nextNode();
  while (current) {
    nodes.push(current);
    current = walker.nextNode();
  }
  return nodes;
}

function applyDomAnnotations(container, annotations) {
  if (!container) return;
  clearDomAnnotations(container);
  if (!Array.isArray(annotations) || annotations.length === 0) return;

  // Sắp xếp theo độ dài giảm dần để câu dài được ưu tiên bọc trước
  const sorted = [...annotations]
    .filter((a) => a && typeof a.text === 'string' && a.text.trim().length > 0)
    .sort((a, b) => b.text.length - a.text.length);

  for (const ann of sorted) {
    const needle = ann.text.replace(/\s+/g, ' ').trim();
    if (!needle) continue;

    // Thu thập lại text nodes sau mỗi lần bọc
    const textNodes = collectEligibleTextNodes(container);
    if (!textNodes.length) break;

    // Ghép chuỗi toàn cục cùng bảng ánh xạ vị trí từng textNode
    let fullText = '';
    const segments = [];
    for (const node of textNodes) {
      const val = node.nodeValue || '';
      const start = fullText.length;
      fullText += val;
      segments.push({ node, start, end: fullText.length });
    }

    // Tìm khớp (cho phép khoảng trắng linh hoạt giữa các từ)
    const pattern = needle
      .split(/\s+/)
      .map(escapeRegex)
      .join('\\s+');
    const regex = new RegExp(pattern, 'i');
    const match = regex.exec(fullText);
    if (!match) continue;

    const matchStart = match.index;
    const matchEnd = matchStart + match[0].length;

    const overlapping = segments.filter(
      (seg) => seg.end > matchStart && seg.start < matchEnd,
    );
    if (!overlapping.length) continue;

    let lastWrapSpan = null;

    // Duyệt ngược để splitText không làm lệch offset của các node trước
    for (let i = overlapping.length - 1; i >= 0; i--) {
      const seg = overlapping[i];
      const localStart = Math.max(0, matchStart - seg.start);
      const localEnd = Math.min(seg.node.nodeValue.length, matchEnd - seg.start);
      if (localEnd <= localStart) continue;

      let targetNode = seg.node;
      if (localEnd < targetNode.nodeValue.length) {
        targetNode.splitText(localEnd);
      }
      if (localStart > 0) {
        targetNode = targetNode.splitText(localStart);
      }

      const wrap = document.createElement('span');
      wrap.className = 'user-ann-wrap cursor-pointer rounded-xs transition-colors';
      wrap.setAttribute('data-ann-id', ann.id);
      if (ann.color && COLOR_MAP[ann.color]) {
        wrap.style.backgroundColor = COLOR_MAP[ann.color];
        wrap.style.padding = '1px 2px';
        wrap.style.borderRadius = '3px';
      }
      if (ann.underlineRed) {
        wrap.style.textDecoration = 'underline';
        wrap.style.textDecorationColor = '#ef4444';
        wrap.style.textDecorationThickness = '2px';
        wrap.style.textUnderlineOffset = '3px';
      }

      targetNode.parentNode.insertBefore(wrap, targetNode);
      wrap.appendChild(targetNode);

      if (i === overlapping.length - 1) {
        lastWrapSpan = wrap;
      }
    }

    // Chèn badge Ghi chú [📝 ... ×] và Nghĩa tra từ [🔍 ... ×] ngay kế bên giống hệt Image 4
    if (lastWrapSpan && lastWrapSpan.parentNode) {
      let anchor = lastWrapSpan;

      if (ann.note && String(ann.note).trim()) {
        const noteBadge = document.createElement('span');
        noteBadge.className =
          'user-ann-note mx-1 inline-flex items-center gap-1 rounded-md border border-rose-300 bg-rose-50 px-1.5 py-0.5 text-xs font-semibold text-rose-600 shadow-2xs align-baseline';
        noteBadge.setAttribute('data-ann-id', ann.id);

        const textSpan = document.createElement('span');
        textSpan.textContent = ann.note;
        noteBadge.appendChild(textSpan);

        const delBtn = document.createElement('button');
        delBtn.type = 'button';
        delBtn.className =
          'ml-0.5 inline-flex h-4 w-4 items-center justify-center rounded-full text-rose-400 hover:bg-rose-200 hover:text-rose-700 font-bold leading-none';
        delBtn.setAttribute('data-del-note', ann.id);
        delBtn.title = 'Xóa ghi chú này';
        delBtn.textContent = '×';
        noteBadge.appendChild(delBtn);

        anchor.insertAdjacentElement('afterend', noteBadge);
        anchor = noteBadge;
      }

      if (ann.translation && String(ann.translation).trim()) {
        const transBadge = document.createElement('span');
        transBadge.className =
          'user-ann-trans mx-1 inline-flex items-center gap-1 rounded-md border border-sky-300 bg-sky-50 px-1.5 py-0.5 text-xs font-semibold text-sky-800 shadow-2xs align-baseline';
        transBadge.setAttribute('data-ann-id', ann.id);

        const labelSpan = document.createElement('span');
        labelSpan.textContent = `🔍 ${ann.translation}`;
        transBadge.appendChild(labelSpan);

        const delBtn = document.createElement('button');
        delBtn.type = 'button';
        delBtn.className =
          'ml-0.5 inline-flex h-4 w-4 items-center justify-center rounded-full text-sky-400 hover:bg-sky-200 hover:text-sky-800 font-bold leading-none';
        delBtn.setAttribute('data-del-trans', ann.id);
        delBtn.title = 'Ẩn / xóa nghĩa đã tra';
        delBtn.textContent = '×';
        transBadge.appendChild(delBtn);

        anchor.insertAdjacentElement('afterend', transBadge);
      }
    }
  }
}

/* ------------------------------------------------------------------ */
/* 2. AnnotatableContainer — Khung bọc văn bản hỗ trợ bôi đen          */
/* ------------------------------------------------------------------ */

export function AnnotatableContainer({ scopeId = 'default', children, className = '' }) {
  const { settings, openSettings, openDictionary } = useApp();
  const { speak } = useSpeech();

  const containerRef = useRef(null);
  const toolbarRef = useRef(null);
  const isApplyingRef = useRef(false);

  const [annotations, setAnnotations] = useState([]);
  const [popover, setPopover] = useState(null);
  // popover: { x, y, placement: 'top'|'bottom', text, annId, mode: 'menu'|'note'|'translate', noteDraft, translating, transPreview }

  const highlightEnabled = settings?.highlightEnabled !== false;

  // Tải danh sách annotations của scopeId
  const reloadScopeAnnotations = useCallback(() => {
    setAnnotations(loadAnnotations(scopeId));
  }, [scopeId]);

  useEffect(() => {
    reloadScopeAnnotations();
    setPopover(null);
  }, [scopeId, reloadScopeAnnotations]);

  // Lắng nghe sự kiện đồng bộ từ HighlightToggleBar hoặc container khác
  useEffect(() => {
    const onSync = (e) => {
      if (!e?.detail?.scopeId || e.detail.scopeId === scopeId) {
        reloadScopeAnnotations();
      }
    };
    window.addEventListener(ANN_SYNC_EVENT, onSync);
    return () => window.removeEventListener(ANN_SYNC_EVENT, onSync);
  }, [scopeId, reloadScopeAnnotations]);

  // Áp dụng highlight/note/translation vào DOM mỗi khi annotations hoặc nội dung thay đổi
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const runApply = () => {
      if (isApplyingRef.current) return;
      isApplyingRef.current = true;
      try {
        if (!highlightEnabled) {
          clearDomAnnotations(el);
        } else {
          applyDomAnnotations(el, annotations);
        }
      } finally {
        setTimeout(() => {
          isApplyingRef.current = false;
        }, 0);
      }
    };

    runApply();

    // Quan sát khi React render thêm phần tử con (ví dụ mở đáp án, đổi câu hỏi)
    let debounceTimer = null;
    const observer = new MutationObserver((mutations) => {
      if (isApplyingRef.current) return;
      const relevant = mutations.some((m) => {
        if (m.target?.closest?.('.user-ann-toolbar, .user-ann-note, .user-ann-trans, .user-ann-wrap')) return false;
        for (let i = 0; i < m.addedNodes.length; i++) {
          const n = m.addedNodes[i];
          if (n.nodeType === 1 && n.matches?.('.user-ann-toolbar, .user-ann-note, .user-ann-trans, .user-ann-wrap')) {
            return false;
          }
        }
        return true;
      });
      if (!relevant) return;
      if (debounceTimer) clearTimeout(debounceTimer);
      debounceTimer = setTimeout(runApply, 80);
    });

    observer.observe(el, { childList: true, subtree: true });

    return () => {
      if (debounceTimer) clearTimeout(debounceTimer);
      observer.disconnect();
    };
  }, [annotations, highlightEnabled, children]);

  // Đóng toolbar khi bấm ra ngoài hoặc nhấn Escape
  useEffect(() => {
    if (!popover) return;
    const onMouseDown = (e) => {
      if (toolbarRef.current && toolbarRef.current.contains(e.target)) return;
      if (e.target?.closest?.('.user-ann-wrap, .user-ann-note, .user-ann-trans')) return;
      setPopover(null);
    };
    const onKeyDown = (e) => {
      if (e.key === 'Escape') setPopover(null);
    };
    document.addEventListener('mousedown', onMouseDown);
    document.addEventListener('keydown', onKeyDown);
    return () => {
      document.removeEventListener('mousedown', onMouseDown);
      document.removeEventListener('keydown', onKeyDown);
    };
  }, [popover]);

  // Tính toán tọa độ hiển thị thanh công cụ nổi
  const computeToolbarCoords = (rect) => {
    const vw = window.innerWidth || 1024;
    const centerX = rect.left + rect.width / 2;
    const clampedX = Math.max(170, Math.min(vw - 170, centerX));
    const showBelow = rect.top < 110;
    const y = showBelow ? rect.bottom + 10 : rect.top - 10;
    return { x: clampedX, y, placement: showBelow ? 'bottom' : 'top' };
  };

  // Xử lý click vào nút xóa nhanh [×] trên badge ghi chú / nghĩa tra từ hoặc click vào highlight cũ
  const handleContainerClick = (e) => {
    if (!highlightEnabled) return;
    if (toolbarRef.current && toolbarRef.current.contains(e.target)) return;

    const delNoteId = e.target?.getAttribute?.('data-del-note');
    if (delNoteId) {
      e.preventDefault();
      e.stopPropagation();
      const existing = annotations.find((a) => a.id === delNoteId);
      if (existing) {
        if (!existing.translation && (!existing.color || existing.color === 'none') && !existing.underlineRed) {
          const next = deleteAnnotation(scopeId, delNoteId);
          setAnnotations(next);
        } else {
          const next = saveAnnotation(scopeId, { ...existing, note: '' });
          setAnnotations(next);
        }
        emitAnnotationSync(scopeId);
      }
      return;
    }

    const delTransId = e.target?.getAttribute?.('data-del-trans');
    if (delTransId) {
      e.preventDefault();
      e.stopPropagation();
      const existing = annotations.find((a) => a.id === delTransId);
      if (existing) {
        if (!existing.note && (!existing.color || existing.color === 'none') && !existing.underlineRed) {
          const next = deleteAnnotation(scopeId, delTransId);
          setAnnotations(next);
        } else {
          const next = saveAnnotation(scopeId, { ...existing, translation: '' });
          setAnnotations(next);
        }
        emitAnnotationSync(scopeId);
      }
      return;
    }

    // Nếu người dùng không bôi đen mới mà click vào một từ/câu đã được highlight trước đó
    const sel = window.getSelection?.();
    if (sel && !sel.isCollapsed && sel.toString().trim().length > 0) return;

    const wrapEl = e.target?.closest?.('.user-ann-wrap, .user-ann-note, .user-ann-trans');
    if (wrapEl) {
      const annId = wrapEl.getAttribute('data-ann-id');
      const existing = annotations.find((a) => a.id === annId);
      if (existing) {
        const rect = wrapEl.getBoundingClientRect();
        const coords = computeToolbarCoords(rect);
        setPopover({
          ...coords,
          text: existing.text,
          annId: existing.id,
          mode: 'menu',
          noteDraft: existing.note || '',
          translating: false,
          transPreview: existing.translation || '',
        });
      }
    }
  };

  // Bắt sự kiện nhả chuột sau khi bôi đen văn bản
  const handleMouseUp = (e) => {
    if (!highlightEnabled) return;
    if (toolbarRef.current && toolbarRef.current.contains(e.target)) return;
    if (e.target?.closest?.('button:not(.duo-choice), input, textarea, select')) return;

    setTimeout(() => {
      const sel = window.getSelection?.();
      if (!sel || sel.isCollapsed || sel.rangeCount === 0) return;

      const range = sel.getRangeAt(0);
      const container = containerRef.current;
      if (!container || !container.contains(range.commonAncestorContainer)) return;

      const rawText = sel.toString();
      const cleanText = rawText.replace(/\s+/g, ' ').trim();
      if (cleanText.length < 1 || cleanText.length > 600) return;

      const rect = range.getBoundingClientRect();
      if (rect.width === 0 && rect.height === 0) return;

      const existing = annotations.find(
        (a) => String(a.text || '').toLowerCase() === cleanText.toLowerCase(),
      );
      const coords = computeToolbarCoords(rect);

      setPopover({
        ...coords,
        text: existing ? existing.text : cleanText,
        annId: existing?.id || null,
        mode: 'menu',
        noteDraft: existing?.note || '',
        translating: false,
        transPreview: existing?.translation || '',
      });
    }, 10);
  };

  const activeAnn = popover?.annId
    ? annotations.find((a) => a.id === popover.annId)
    : annotations.find(
        (a) =>
          popover?.text &&
          String(a.text || '').toLowerCase() === String(popover.text).toLowerCase(),
      );

  // Thao tác chọn màu Highlight
  const handleSelectColor = (colorId) => {
    if (!popover?.text) return;
    const record = {
      id: activeAnn?.id,
      text: popover.text,
      color: colorId,
      underlineRed: Boolean(activeAnn?.underlineRed),
      note: activeAnn?.note || '',
      translation: activeAnn?.translation || '',
    };
    const next = saveAnnotation(scopeId, record);
    setAnnotations(next);
    emitAnnotationSync(scopeId);
    window.getSelection?.()?.removeAllRanges?.();
    const saved = next.find(
      (a) => a.text.toLowerCase() === popover.text.toLowerCase(),
    );
    if (saved) {
      setPopover((prev) => (prev ? { ...prev, annId: saved.id } : null));
    }
  };

  // Thao tác bật/tắt gạch chân đỏ (abc)
  const handleToggleUnderlineRed = () => {
    if (!popover?.text) return;
    const nextUnderline = !activeAnn?.underlineRed;
    const record = {
      id: activeAnn?.id,
      text: popover.text,
      color: activeAnn?.color || 'none',
      underlineRed: nextUnderline,
      note: activeAnn?.note || '',
      translation: activeAnn?.translation || '',
    };
    const next = saveAnnotation(scopeId, record);
    setAnnotations(next);
    emitAnnotationSync(scopeId);
    window.getSelection?.()?.removeAllRanges?.();
    const saved = next.find(
      (a) => a.text.toLowerCase() === popover.text.toLowerCase(),
    );
    if (saved) {
      setPopover((prev) => (prev ? { ...prev, annId: saved.id } : null));
    }
  };

  // Thao tác lưu Ghi chú (Note)
  const handleSaveNote = (e) => {
    if (e) e.preventDefault();
    if (!popover?.text) return;
    const trimmedNote = String(popover.noteDraft || '').trim();
    const record = {
      id: activeAnn?.id,
      text: popover.text,
      color: activeAnn?.color || 'pink',
      underlineRed: activeAnn?.underlineRed !== undefined ? activeAnn.underlineRed : true,
      note: trimmedNote,
      translation: activeAnn?.translation || popover.transPreview || '',
    };
    const next = saveAnnotation(scopeId, record);
    setAnnotations(next);
    emitAnnotationSync(scopeId);
    window.getSelection?.()?.removeAllRanges?.();
    setPopover(null);
  };

  // Thao tác bấm "Tra từ" — dịch và hiện trực tiếp kế bên từ/câu (phản hồi siêu nhanh 0ms nếu có cache)
  const handleLookup = async () => {
    if (!popover?.text || popover.translating) return;
    const clean = popover.text.replace(/\s+/g, ' ').trim();
    const lower = clean.toLowerCase();

    // 1. Phản hồi tức thì 0ms nếu có trong 600 từ TOEIC hoặc cache
    const instant = lookupCuratedWord(clean) || TRANSLATION_CACHE.get(lower);
    if (instant) {
      const record = {
        id: activeAnn?.id,
        text: popover.text,
        color: activeAnn?.color || 'blue',
        underlineRed: Boolean(activeAnn?.underlineRed),
        note: activeAnn?.note || '',
        translation: instant,
      };
      const next = saveAnnotation(scopeId, record);
      setAnnotations(next);
      emitAnnotationSync(scopeId);
      window.getSelection?.()?.removeAllRanges?.();
      const saved = next.find((a) => a.text.toLowerCase() === popover.text.toLowerCase());
      setPopover((prev) =>
        prev
          ? {
              ...prev,
              annId: saved?.id || prev.annId,
              mode: 'translate',
              translating: false,
              transPreview: instant,
            }
          : null,
      );
      return;
    }

    setPopover((prev) =>
      prev ? { ...prev, mode: 'translate', translating: true } : null,
    );

    const resultText = await translateSelection(popover.text, settings);

    const record = {
      id: activeAnn?.id,
      text: popover.text,
      color: activeAnn?.color || 'blue',
      underlineRed: Boolean(activeAnn?.underlineRed),
      note: activeAnn?.note || '',
      translation: resultText,
    };
    const next = saveAnnotation(scopeId, record);
    setAnnotations(next);
    emitAnnotationSync(scopeId);
    window.getSelection?.()?.removeAllRanges?.();

    const saved = next.find(
      (a) => a.text.toLowerCase() === popover.text.toLowerCase(),
    );
    setPopover((prev) =>
      prev
        ? {
            ...prev,
            annId: saved?.id || prev.annId,
            translating: false,
            transPreview: resultText,
          }
        : null,
    );
  };

  // Thao tác xóa đánh dấu (Delete)
  const handleDeleteAnnotation = () => {
    const targetId = activeAnn?.id || popover?.annId;
    if (targetId) {
      const next = deleteAnnotation(scopeId, targetId);
      setAnnotations(next);
      emitAnnotationSync(scopeId);
    }
    window.getSelection?.()?.removeAllRanges?.();
    setPopover(null);
  };

  return (
    <div
      ref={containerRef}
      onMouseUp={handleMouseUp}
      onClick={handleContainerClick}
      className={`relative ${className}`}
    >
      {children}

      {/* Thanh công cụ nổi khi bôi đen chuẩn Image 4 */}
      {popover && highlightEnabled ? (
        <div
          ref={toolbarRef}
          data-no-annotate="true"
          style={{
            position: 'fixed',
            left: `${popover.x}px`,
            top: `${popover.y}px`,
            transform:
              popover.placement === 'bottom'
                ? 'translate(-50%, 0)'
                : 'translate(-50%, -100%)',
          }}
          className="user-ann-toolbar z-50 flex flex-col items-center"
        >
          {/* Khung chính màu tối chuẩn Image 4 */}
          <div className="flex items-center gap-3 rounded-2xl bg-[#3c4043] px-3.5 py-2 text-white shadow-2xl border border-slate-600/80">
            {/* 1. Nút Note */}
            <button
              type="button"
              onClick={() =>
                setPopover((prev) =>
                  prev
                    ? {
                        ...prev,
                        mode: prev.mode === 'note' ? 'menu' : 'note',
                        noteDraft: activeAnn?.note || prev.noteDraft || '',
                      }
                    : null,
                )
              }
              className={`flex flex-col items-center justify-center gap-0.5 rounded-lg px-2 py-1 text-xs font-medium transition-colors hover:bg-white/15 ${
                popover.mode === 'note' ? 'bg-white/20 text-amber-300' : 'text-white'
              }`}
              title="Thêm ghi chú kế bên đoạn văn bản này"
            >
              <PenLine className="h-4 w-4" />
              <span className="text-[11px] font-semibold">Note</span>
            </button>

            <div className="h-8 w-px bg-slate-500/70" />

            {/* 2. Nút Tra từ */}
            <button
              type="button"
              onClick={handleLookup}
              className={`flex flex-col items-center justify-center gap-0.5 rounded-lg px-2 py-1 text-xs font-medium transition-colors hover:bg-white/15 ${
                popover.mode === 'translate' ? 'bg-white/20 text-sky-300' : 'text-white'
              }`}
              title="Tra từ / Dịch sang tiếng Việt và hiện trực tiếp kế bên"
            >
              {popover.translating ? (
                <Loader2 className="h-4 w-4 animate-spin text-sky-300" />
              ) : (
                <Search className="h-4 w-4" />
              )}
              <span className="text-[11px] font-semibold">Tra từ</span>
            </button>

            <div className="h-8 w-px bg-slate-500/70" />

            {/* 3. Lưới 2x3: 5 ô màu + nút abc gạch chân đỏ chuẩn Image 4 */}
            <div className="grid grid-cols-3 gap-1.5 items-center">
              {HIGHLIGHT_COLORS.map((c) => {
                const isSelected = activeAnn?.color === c.id;
                return (
                  <button
                    key={c.id}
                    type="button"
                    onClick={() => handleSelectColor(c.id)}
                    style={{ backgroundColor: c.bg }}
                    className={`h-5 w-6 rounded-xs border transition-transform hover:scale-110 ${
                      isSelected ? 'ring-2 ring-white border-slate-900 scale-105' : 'border-white/40'
                    }`}
                    title={`Tô màu: ${c.label}`}
                  />
                );
              })}

              {/* Ô thứ 6: abc gạch chân đỏ */}
              <button
                type="button"
                onClick={handleToggleUnderlineRed}
                className={`flex h-5 w-6 items-center justify-center rounded-xs text-[11px] font-extrabold underline decoration-rose-500 decoration-2 underline-offset-2 transition-transform hover:scale-110 ${
                  activeAnn?.underlineRed
                    ? 'bg-white/25 text-white ring-1 ring-rose-400'
                    : 'text-white hover:bg-white/10'
                }`}
                title="Gạch chân đỏ (abc)"
              >
                abc
              </button>
            </div>

            <div className="h-8 w-px bg-slate-500/70" />

            {/* 4. Nút Delete */}
            <button
              type="button"
              onClick={handleDeleteAnnotation}
              className="flex flex-col items-center justify-center gap-0.5 rounded-lg px-2 py-1 text-xs font-medium text-white transition-colors hover:bg-rose-500/30 hover:text-rose-200"
              title="Xóa đánh dấu, ghi chú & nghĩa tra từ của đoạn này"
            >
              <Trash2 className="h-4 w-4" />
              <span className="text-[11px] font-semibold">Delete</span>
            </button>
          </div>

          {/* Khung con bên dưới khi bấm Note */}
          {popover.mode === 'note' ? (
            <form
              onSubmit={handleSaveNote}
              className="mt-1.5 w-72 rounded-xl border border-slate-200 bg-white p-2.5 text-slate-800 shadow-xl"
            >
              <p className="mb-1.5 truncate text-[11px] font-bold text-slate-500">
                Ghi chú cho: <span className="italic text-slate-800">“{popover.text}”</span>
              </p>
              <input
                type="text"
                autoFocus
                value={popover.noteDraft}
                onChange={(e) =>
                  setPopover((prev) =>
                    prev ? { ...prev, noteDraft: e.target.value } : null,
                  )
                }
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    handleSaveNote(e);
                  }
                }}
                placeholder="Nhập ghi chú (Nhấn Enter để lưu)…"
                className="w-full rounded-lg border border-slate-300 px-2.5 py-1.5 text-xs text-slate-900 outline-none focus:border-sky-500"
              />
              <div className="mt-2 flex items-center justify-end gap-1.5">
                <button
                  type="button"
                  onClick={() =>
                    setPopover((prev) => (prev ? { ...prev, mode: 'menu' } : null))
                  }
                  className="rounded-lg px-2.5 py-1 text-xs font-semibold text-slate-500 hover:bg-slate-100"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="inline-flex items-center gap-1 rounded-lg bg-[#1cb0f6] px-3 py-1 text-xs font-bold text-white hover:bg-[#1899d6]"
                >
                  <Check className="h-3.5 w-3.5" />
                  Lưu ghi chú
                </button>
              </div>
            </form>
          ) : null}

          {/* Khung con bên dưới khi bấm Tra từ */}
          {popover.mode === 'translate' ? (
            <div className="mt-1.5 w-80 rounded-xl border border-slate-200 bg-white p-3 text-slate-800 shadow-xl">
              <div className="mb-1.5 flex items-center justify-between gap-2">
                <div className="flex items-center gap-1.5 min-w-0">
                  <BookOpen className="h-3.5 w-3.5 shrink-0 text-sky-600" />
                  <span className="truncate text-xs font-extrabold text-slate-900">
                    {popover.text}
                  </span>
                </div>
                <div className="flex items-center gap-1">
                  <button
                    type="button"
                    onClick={() => speak(popover.text, { rate: settings?.ttsRate || 0.95 })}
                    className="rounded-md p-1 text-slate-500 hover:bg-slate-100 hover:text-sky-600"
                    title="Nghe phát âm"
                  >
                    <Volume2 className="h-3.5 w-3.5" />
                  </button>
                  <button
                    type="button"
                    onClick={() => setPopover(null)}
                    className="rounded-md p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
                    title="Đóng"
                  >
                    <X className="h-3.5 w-3.5" />
                  </button>
                </div>
              </div>

              {popover.translating ? (
                <div className="flex items-center gap-2 py-2 text-xs text-slate-500">
                  <Loader2 className="h-4 w-4 animate-spin text-sky-600" />
                  <span>Đang tra nghĩa &amp; gắn trực tiếp vào văn bản…</span>
                </div>
              ) : (
                <div className="rounded-lg border border-sky-100 bg-sky-50/70 px-2.5 py-2 text-xs font-medium leading-relaxed text-sky-950">
                  {popover.transPreview}
                </div>
              )}

              <div className="mt-2.5 flex items-center justify-between text-[11px] text-slate-400">
                <button
                  type="button"
                  onClick={() => {
                    const textToLook = popover.text;
                    setPopover(null);
                    openDictionary(textToLook);
                  }}
                  className="inline-flex items-center gap-1 font-bold text-[var(--color-duo-green-dark)] hover:underline"
                  title="Mở toàn bộ nghĩa & bài học trong Từ điển"
                >
                  <BookOpen className="h-3 w-3" />
                  <span>Mở Từ điển (D) →</span>
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setPopover(null);
                    openSettings();
                  }}
                  className="font-semibold text-sky-600 hover:underline"
                >
                  Đổi API tra từ →
                </button>
              </div>
            </div>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}

export const AnnotatableText = AnnotatableContainer;
export default AnnotatableContainer;
