/**
 * Centralized Settings View (Cài đặt hệ thống & Phân quyền AI theo tính năng).
 *
 * Quản lý tập trung:
 *  1. Chọn API cho từng tính năng:
 *     - Tra từ trực tiếp khi bôi đen (Free Google Dịch & Từ điển / Gemini / OpenAI / Ollama)
 *     - Luyện đặt câu AI Sentence Lab — Tab 4 (Gemini / OpenAI / Ollama)
 *  2. Quản lý API Keys & Models (BYOK — chỉ lưu localStorage trên trình duyệt, không lộ key ra DOM)
 *  3. Tùy chọn công cụ Highlight / Ghi chú / Tra từ, tốc độ giọng đọc TTS và quản lý dữ liệu.
 */
import { useCallback, useEffect, useRef, useState } from 'react';
import {
  ArrowLeft,
  BookOpenCheck,
  CheckCircle2,
  Cpu,
  Globe,
  Highlighter,
  Info,
  KeyRound,
  RotateCcw,
  Save,
  Settings2,
  Sparkles,
  Trash2,
  Volume2,
  Wand2,
} from 'lucide-react';
import { Badge, Button, Card, SectionTitle } from './ui.jsx';
import { useApp } from '../lib/store.jsx';
import {
  DEFAULT_SETTINGS,
  clearAll,
  clearHistory,
  loadProgress,
  loadSrs,
} from '../lib/storage.js';

/* ------------------------------------------------------------------ */
/* Danh sách lựa chọn API theo tính năng                               */
/* ------------------------------------------------------------------ */

export const LOOKUP_PROVIDERS = [
  {
    id: 'free',
    label: 'Miễn phí — Google Dịch & Từ điển',
    badge: 'Khuyên dùng · Free',
    badgeTone: 'emerald',
    desc: 'Tra từ và dịch câu trực tiếp siêu tốc, kèm từ loại & nghĩa từ điển, không cần API key.',
  },
  {
    id: 'gemini',
    label: 'Google Gemini API',
    badge: 'Cần API Key',
    badgeTone: 'brand',
    desc: 'Dịch ngắn gọn chuẩn ngữ cảnh bài thi TOEIC Business bằng mô hình Gemini.',
  },
  {
    id: 'openai',
    label: 'OpenAI API (GPT)',
    badge: 'Cần API Key',
    badgeTone: 'sky',
    desc: 'Dịch và giải nghĩa từ vựng theo ngữ cảnh bằng mô hình GPT (gpt-4o-mini / gpt-4o).',
  },
  {
    id: 'ollama',
    label: 'Ollama Local AI',
    badge: 'Offline · Free',
    badgeTone: 'violet',
    desc: 'Chạy mô hình AI cục bộ ngay trên máy tính của bạn, không tốn phí API.',
  },
];

export const AI_LAB_PROVIDERS = [
  {
    id: 'gemini',
    label: 'Google Gemini API',
    badge: 'Khuyên dùng',
    badgeTone: 'brand',
    desc: 'Tốc độ nhanh, chấm câu và gợi ý viết lại Business English sát chuẩn TOEIC.',
  },
  {
    id: 'openai',
    label: 'OpenAI API (GPT)',
    badge: 'GPT-4o / mini',
    badgeTone: 'sky',
    desc: 'Phân tích lỗi ngữ pháp chi tiết, nhận xét tự nhiên với mô hình OpenAI GPT.',
  },
  {
    id: 'ollama',
    label: 'Ollama Local AI',
    badge: 'Chạy trên máy',
    badgeTone: 'violet',
    desc: 'Hoạt động độc lập không cần khóa API. Yêu cầu ứng dụng Ollama đang mở.',
  },
];

const TTS_RATES = [
  { value: 0.8, label: '0.8x (Chậm rõ)' },
  { value: 0.95, label: '0.95x (Chuẩn TOEIC)' },
  { value: 1.0, label: '1.0x (Tự nhiên)' },
  { value: 1.15, label: '1.15x (Nhanh)' },
];

/** Che API key: chỉ hiện tối đa 4 ký tự cuối, không bao giờ lộ toàn bộ key. */
export function maskKey(key) {
  const s = String(key ?? '').trim();
  if (!s) return '';
  if (s.length <= 4) return '•'.repeat(s.length);
  return `${'•'.repeat(Math.min(12, s.length - 4))}${s.slice(-4)}`;
}

/* ------------------------------------------------------------------ */
/* Hàm gọi AI dùng chung cho các tính năng (AI Lab & Tra từ AI)        */
/* ------------------------------------------------------------------ */

/**
 * Gọi provider AI theo cấu hình tính năng ('aiLab' | 'lookup' hoặc chỉ định trực tiếp).
 * Không bao giờ throw — luôn trả về { ok: true, text, provider } hoặc { ok: false, error, missingKey }.
 */
export async function callAiForFeature(prompt, settings, featureOrProvider = 'aiLab') {
  const s = settings || {};
  let provider = featureOrProvider;
  if (featureOrProvider === 'aiLab') {
    provider = s.aiLabProvider || s.provider || 'gemini';
  } else if (featureOrProvider === 'lookup') {
    provider = s.lookupProvider || 'free';
  }

  let url = '';
  let headers = { 'Content-Type': 'application/json' };
  let body = null;

  if (provider === 'gemini') {
    const key = String(s.geminiKey || '').trim();
    if (!key) {
      return {
        ok: false,
        missingKey: true,
        provider,
        error: 'Chưa có Gemini API key. Hãy vào mục Cài đặt để nhập khóa API.',
      };
    }
    const model =
      String(s.geminiModel || (s.provider === 'gemini' ? s.model : '') || 'gemini-2.5-flash').trim() ||
      'gemini-2.5-flash';
    url = `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(
      model,
    )}:generateContent?key=${encodeURIComponent(key)}`;
    body = { contents: [{ parts: [{ text: prompt }] }] };
  } else if (provider === 'openai') {
    const key = String(s.openaiKey || '').trim();
    if (!key) {
      return {
        ok: false,
        missingKey: true,
        provider,
        error: 'Chưa có OpenAI API key. Hãy vào mục Cài đặt để nhập khóa API.',
      };
    }
    const model =
      String(
        s.openaiModel ||
          (s.provider === 'openai' && !String(s.model || '').startsWith('gemini') ? s.model : '') ||
          'gpt-4o-mini',
      ).trim() || 'gpt-4o-mini';
    url = 'https://api.openai.com/v1/chat/completions';
    headers = { ...headers, Authorization: `Bearer ${key}` };
    body = {
      model,
      messages: [{ role: 'user', content: prompt }],
    };
  } else if (provider === 'ollama') {
    const raw = String(s.ollamaUrl ?? '').trim().replace(/\/+$/, '');
    const base = raw || 'http://localhost:11434';
    const model = String(s.ollamaModel || 'llama3.1').trim() || 'llama3.1';
    url = `${base}/api/chat`;
    body = {
      model,
      messages: [{ role: 'user', content: prompt }],
      stream: false,
    };
  } else {
    return { ok: false, provider, error: `Provider không được hỗ trợ: ${provider}` };
  }

  try {
    const res = await fetch(url, { method: 'POST', headers, body: JSON.stringify(body) });

    if (!res.ok) {
      let detail = '';
      try {
        detail = (await res.text()).slice(0, 320);
      } catch {
        detail = '';
      }
      const base = `Lỗi từ ${provider} (HTTP ${res.status} ${res.statusText}).`;
      if (res.status === 401 || res.status === 403) {
        return { ok: false, provider, error: `${base} API key có thể sai hoặc đã hết hạn.` };
      }
      if (res.status === 429) {
        return { ok: false, provider, error: `${base} Vượt giới hạn gọi API (rate limit), vui lòng thử lại sau.` };
      }
      return { ok: false, provider, error: detail ? `${base} Chi tiết: ${detail}` : base };
    }

    let json = null;
    try {
      json = await res.json();
    } catch {
      return { ok: false, provider, error: 'Không đọc được JSON từ phản hồi của nhà cung cấp AI.' };
    }

    const text =
      json?.candidates?.[0]?.content?.parts?.map((p) => p?.text || '').join('') ??
      json?.choices?.[0]?.message?.content ??
      json?.message?.content ??
      '';

    if (!String(text).trim()) {
      return { ok: false, provider, error: 'Nhà cung cấp trả về nội dung rỗng. Thử lại hoặc đổi model.' };
    }
    return { ok: true, provider, text: String(text).trim() };
  } catch (err) {
    const msg = err?.message || String(err);
    return {
      ok: false,
      provider,
      error: `Không kết nối được tới ${provider}. Kiểm tra mạng / URL / CORS. Chi tiết: ${msg}`,
    };
  }
}

/* ------------------------------------------------------------------ */
/* Component chính: SettingsView                                       */
/* ------------------------------------------------------------------ */

export default function SettingsView() {
  const { settings, updateSettings, lessonId, tab, openLesson, setProgress, setSrs } = useApp();

  const [savedBanner, setSavedBanner] = useState('');
  const [geminiDraft, setGeminiDraft] = useState('');
  const [openaiDraft, setOpenaiDraft] = useState('');
  const [revealGemini, setRevealGemini] = useState(false);
  const [revealOpenai, setRevealOpenai] = useState(false);
  const [confirmClearHist, setConfirmClearHist] = useState(false);
  const [confirmResetAll, setConfirmResetAll] = useState(false);

  const timerRef = useRef(null);

  useEffect(() => () => timerRef.current && clearTimeout(timerRef.current), []);

  const notifySaved = useCallback((msg = 'Đã lưu cài đặt') => {
    setSavedBanner(msg);
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => setSavedBanner(''), 2200);
  }, []);

  const applyPatch = useCallback(
    (patch, msg) => {
      updateSettings(patch);
      notifySaved(msg);
    },
    [updateSettings, notifySaved],
  );

  const lookupProvider = settings?.lookupProvider || 'free';
  const aiLabProvider = settings?.aiLabProvider || settings?.provider || 'gemini';
  const highlightEnabled = settings?.highlightEnabled !== false;
  const ttsRate = Number(settings?.ttsRate || 0.95);

  const hasGeminiKey = Boolean(String(settings?.geminiKey || '').trim());
  const hasOpenaiKey = Boolean(String(settings?.openaiKey || '').trim());

  const geminiModelVal = settings?.geminiModel || settings?.model || 'gemini-2.5-flash';
  const openaiModelVal = settings?.openaiModel || 'gpt-4o-mini';

  return (
    <div className="space-y-6 pb-10">
      {/* Header */}
      <Card className="flex flex-wrap items-center justify-between gap-4 px-5 py-4">
        <div className="flex items-center gap-3">
          <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-[var(--color-duo-blue-light)] text-[var(--color-duo-blue)]">
            <Settings2 className="h-6 w-6" />
          </span>
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <h2 className="text-xl font-extrabold text-slate-900">
                Cài Đặt Hệ Thống &amp; Phân Quyền AI
              </h2>
              {savedBanner ? (
                <Badge tone="emerald">
                  <CheckCircle2 className="h-3.5 w-3.5" />
                  {savedBanner}
                </Badge>
              ) : null}
            </div>
            <p className="mt-0.5 text-xs text-slate-500">
              Tùy chỉnh nguồn API cho từng tính năng (Tra từ nhanh &amp; Luyện đặt câu AI). Khóa API chỉ
              lưu cục bộ trên trình duyệt của bạn.
            </p>
          </div>
        </div>

        <Button variant="secondary" size="sm" onClick={() => openLesson(lessonId, tab)}>
          <ArrowLeft className="h-4 w-4" />
          Quay lại bài học
        </Button>
      </Card>

      {/* SECTION 1: PHÂN QUYỀN API THEO TÍNH NĂNG */}
      <Card className="p-5">
        <SectionTitle
          icon={Sparkles}
          title="1. Chọn nguồn API cho từng tính năng"
          subtitle="Bạn có thể dùng từ điển miễn phí khi tra từ bôi đen và dùng AI riêng cho phần luyện đặt câu."
        />

        <div className="grid gap-6 lg:grid-cols-2">
          {/* 1A. Tính năng Tra từ khi bôi đen */}
          <div className="rounded-2xl border-2 border-slate-200 bg-slate-50/60 p-4">
            <div className="mb-3 flex items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <Globe className="h-5 w-5 text-sky-600" />
                <h4 className="text-sm font-extrabold text-slate-900">
                  Tính năng Tra từ trực tiếp (khi bôi đen)
                </h4>
              </div>
              <Badge tone="sky">Thanh công cụ Highlight</Badge>
            </div>
            <p className="mb-3 text-xs text-slate-500">
              Chọn dịch vụ sẽ chạy khi bạn bôi đen một từ hoặc câu trong bài học rồi bấm nút{' '}
              <strong className="text-slate-700">Tra từ</strong>:
            </p>

            <div className="space-y-2.5">
              {LOOKUP_PROVIDERS.map((item) => {
                const active = lookupProvider === item.id;
                return (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() =>
                      applyPatch(
                        { lookupProvider: item.id },
                        `Đã chọn nguồn Tra từ: ${item.label}`,
                      )
                    }
                    aria-pressed={active}
                    className={`w-full rounded-xl border-2 p-3 text-left transition-all ${
                      active
                        ? 'border-[#1cb0f6] bg-[#ddf4ff]/60 shadow-sm'
                        : 'border-slate-200 bg-white hover:border-slate-300'
                    }`}
                  >
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="text-sm font-bold text-slate-900">{item.label}</span>
                      <Badge tone={item.badgeTone}>{item.badge}</Badge>
                    </div>
                    <p className="mt-1 text-xs leading-relaxed text-slate-600">{item.desc}</p>
                  </button>
                );
              })}
            </div>
          </div>

          {/* 1B. Tính năng Luyện đặt câu AI Sentence Lab */}
          <div className="rounded-2xl border-2 border-slate-200 bg-slate-50/60 p-4">
            <div className="mb-3 flex items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <Wand2 className="h-5 w-5 text-brand-600" />
                <h4 className="text-sm font-extrabold text-slate-900">
                  Tính năng Luyện đặt câu (AI Sentence Lab)
                </h4>
              </div>
              <Badge tone="brand">Tab 4 · Chấm câu AI</Badge>
            </div>
            <p className="mb-3 text-xs text-slate-500">
              Chọn mô hình AI dùng để ra đề câu tiếng Việt và chấm điểm, sửa lỗi ngữ pháp ở Tab{' '}
              <strong className="text-slate-700">AI Sentence Lab</strong>:
            </p>

            <div className="space-y-2.5">
              {AI_LAB_PROVIDERS.map((item) => {
                const active = aiLabProvider === item.id;
                const nextModel =
                  item.id === 'gemini'
                    ? geminiModelVal
                    : item.id === 'openai'
                      ? openaiModelVal
                      : settings?.ollamaModel || 'llama3.1';
                return (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() =>
                      applyPatch(
                        {
                          provider: item.id,
                          aiLabProvider: item.id,
                          model: nextModel,
                        },
                        `Đã chọn AI cho Luyện đặt câu: ${item.label}`,
                      )
                    }
                    aria-pressed={active}
                    className={`w-full rounded-xl border-2 p-3 text-left transition-all ${
                      active
                        ? 'border-[#1cb0f6] bg-[#ddf4ff]/60 shadow-sm'
                        : 'border-slate-200 bg-white hover:border-slate-300'
                    }`}
                  >
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="text-sm font-bold text-slate-900">{item.label}</span>
                      <Badge tone={item.badgeTone}>{item.badge}</Badge>
                    </div>
                    <p className="mt-1 text-xs leading-relaxed text-slate-600">{item.desc}</p>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </Card>

      {/* SECTION 2: QUẢN LÝ API KEYS & MODELS (BYOK) */}
      <Card className="p-5">
        <SectionTitle
          icon={KeyRound}
          title="2. Quản lý Khóa API & Mô hình (BYOK)"
          subtitle="Nhập API key một lần tại đây để dùng chung cho các tính năng bạn đã phân quyền ở trên."
        />

        <div className="grid gap-5 lg:grid-cols-3">
          {/* Google Gemini */}
          <div className="flex flex-col justify-between rounded-2xl border-2 border-slate-200 bg-white p-4">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-extrabold text-slate-900">Google Gemini</span>
                <Badge tone={hasGeminiKey ? 'emerald' : 'amber'}>
                  {hasGeminiKey ? `Đã lưu (${maskKey(settings?.geminiKey)})` : 'Chưa có key'}
                </Badge>
              </div>

              <div>
                <label className="mb-1 block text-xs font-bold text-slate-600">
                  Gemini API Key
                </label>
                <div className="flex items-center gap-1.5">
                  <input
                    type={revealGemini ? 'text' : 'password'}
                    value={geminiDraft}
                    onChange={(e) => {
                      const v = e.target.value;
                      setGeminiDraft(v);
                      if (v.trim()) {
                        updateSettings({ geminiKey: v.trim() });
                      }
                    }}
                    placeholder={hasGeminiKey ? 'Nhập key mới để thay thế…' : 'AIzaSy…'}
                    autoComplete="off"
                    spellCheck={false}
                    className="w-full rounded-xl border-2 border-slate-300 bg-white px-3 py-2 font-mono text-xs text-slate-800 outline-none focus:border-brand-500"
                  />
                  <Button
                    size="sm"
                    variant="ghost"
                    type="button"
                    onClick={() => setRevealGemini((r) => !r)}
                  >
                    {revealGemini ? 'Ẩn' : 'Hiện'}
                  </Button>
                </div>
                <div className="mt-2 flex flex-wrap items-center gap-2">
                  <Button
                    size="sm"
                    variant="primary"
                    type="button"
                    disabled={!geminiDraft.trim()}
                    onClick={() => {
                      applyPatch({ geminiKey: geminiDraft.trim() }, 'Đã lưu Gemini API Key');
                      setGeminiDraft('');
                    }}
                  >
                    <Save className="h-3.5 w-3.5" />
                    Lưu key
                  </Button>
                  {hasGeminiKey ? (
                    <Button
                      size="sm"
                      variant="ghost"
                      type="button"
                      onClick={() => {
                        applyPatch({ geminiKey: '' }, 'Đã xóa Gemini API Key');
                        setGeminiDraft('');
                      }}
                    >
                      Xóa key
                    </Button>
                  ) : null}
                </div>
              </div>

              <div>
                <label className="mb-1 block text-xs font-bold text-slate-600">
                  Tên mô hình Gemini
                </label>
                <input
                  type="text"
                  value={geminiModelVal}
                  onChange={(e) => {
                    const v = e.target.value;
                    applyPatch(
                      aiLabProvider === 'gemini'
                        ? { geminiModel: v, model: v }
                        : { geminiModel: v },
                    );
                  }}
                  placeholder="gemini-2.5-flash"
                  autoComplete="off"
                  spellCheck={false}
                  className="w-full rounded-xl border-2 border-slate-300 bg-white px-3 py-2 font-mono text-xs text-slate-800 outline-none focus:border-brand-500"
                />
                <div className="mt-1.5 flex flex-wrap gap-1">
                  {['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-pro'].map((m) => (
                    <button
                      key={m}
                      type="button"
                      onClick={() =>
                        applyPatch(
                          aiLabProvider === 'gemini'
                            ? { geminiModel: m, model: m }
                            : { geminiModel: m },
                          `Đã chọn model ${m}`,
                        )
                      }
                      className="rounded-md bg-slate-100 px-2 py-0.5 font-mono text-[11px] text-slate-600 hover:bg-slate-200"
                    >
                      {m}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* OpenAI */}
          <div className="flex flex-col justify-between rounded-2xl border-2 border-slate-200 bg-white p-4">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-extrabold text-slate-900">OpenAI (GPT)</span>
                <Badge tone={hasOpenaiKey ? 'emerald' : 'amber'}>
                  {hasOpenaiKey ? `Đã lưu (${maskKey(settings?.openaiKey)})` : 'Chưa có key'}
                </Badge>
              </div>

              <div>
                <label className="mb-1 block text-xs font-bold text-slate-600">
                  OpenAI API Key
                </label>
                <div className="flex items-center gap-1.5">
                  <input
                    type={revealOpenai ? 'text' : 'password'}
                    value={openaiDraft}
                    onChange={(e) => {
                      const v = e.target.value;
                      setOpenaiDraft(v);
                      if (v.trim()) {
                        updateSettings({ openaiKey: v.trim() });
                      }
                    }}
                    placeholder={hasOpenaiKey ? 'Nhập key mới để thay thế…' : 'sk-proj-…'}
                    autoComplete="off"
                    spellCheck={false}
                    className="w-full rounded-xl border-2 border-slate-300 bg-white px-3 py-2 font-mono text-xs text-slate-800 outline-none focus:border-brand-500"
                  />
                  <Button
                    size="sm"
                    variant="ghost"
                    type="button"
                    onClick={() => setRevealOpenai((r) => !r)}
                  >
                    {revealOpenai ? 'Ẩn' : 'Hiện'}
                  </Button>
                </div>
                <div className="mt-2 flex flex-wrap items-center gap-2">
                  <Button
                    size="sm"
                    variant="primary"
                    type="button"
                    disabled={!openaiDraft.trim()}
                    onClick={() => {
                      applyPatch({ openaiKey: openaiDraft.trim() }, 'Đã lưu OpenAI API Key');
                      setOpenaiDraft('');
                    }}
                  >
                    <Save className="h-3.5 w-3.5" />
                    Lưu key
                  </Button>
                  {hasOpenaiKey ? (
                    <Button
                      size="sm"
                      variant="ghost"
                      type="button"
                      onClick={() => {
                        applyPatch({ openaiKey: '' }, 'Đã xóa OpenAI API Key');
                        setOpenaiDraft('');
                      }}
                    >
                      Xóa key
                    </Button>
                  ) : null}
                </div>
              </div>

              <div>
                <label className="mb-1 block text-xs font-bold text-slate-600">
                  Tên mô hình OpenAI
                </label>
                <input
                  type="text"
                  value={openaiModelVal}
                  onChange={(e) => {
                    const v = e.target.value;
                    applyPatch(
                      aiLabProvider === 'openai'
                        ? { openaiModel: v, model: v }
                        : { openaiModel: v },
                    );
                  }}
                  placeholder="gpt-4o-mini"
                  autoComplete="off"
                  spellCheck={false}
                  className="w-full rounded-xl border-2 border-slate-300 bg-white px-3 py-2 font-mono text-xs text-slate-800 outline-none focus:border-brand-500"
                />
                <div className="mt-1.5 flex flex-wrap gap-1">
                  {['gpt-4o-mini', 'gpt-4o', 'gpt-4.1-mini'].map((m) => (
                    <button
                      key={m}
                      type="button"
                      onClick={() =>
                        applyPatch(
                          aiLabProvider === 'openai'
                            ? { openaiModel: m, model: m }
                            : { openaiModel: m },
                          `Đã chọn model ${m}`,
                        )
                      }
                      className="rounded-md bg-slate-100 px-2 py-0.5 font-mono text-[11px] text-slate-600 hover:bg-slate-200"
                    >
                      {m}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Ollama Local */}
          <div className="flex flex-col justify-between rounded-2xl border-2 border-slate-200 bg-white p-4">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-extrabold text-slate-900">Ollama (Local AI)</span>
                <Badge tone="violet">Không cần Key</Badge>
              </div>

              <div>
                <label className="mb-1 block text-xs font-bold text-slate-600">
                  Ollama Base URL
                </label>
                <input
                  type="text"
                  value={settings?.ollamaUrl ?? 'http://localhost:11434'}
                  onChange={(e) => applyPatch({ ollamaUrl: e.target.value })}
                  placeholder="http://localhost:11434"
                  autoComplete="off"
                  spellCheck={false}
                  className="w-full rounded-xl border-2 border-slate-300 bg-white px-3 py-2 font-mono text-xs text-slate-800 outline-none focus:border-brand-500"
                />
              </div>

              <div>
                <label className="mb-1 block text-xs font-bold text-slate-600">
                  Ollama Model
                </label>
                <input
                  type="text"
                  value={settings?.ollamaModel ?? 'llama3.1'}
                  onChange={(e) => applyPatch({ ollamaModel: e.target.value })}
                  placeholder="llama3.1"
                  autoComplete="off"
                  spellCheck={false}
                  className="w-full rounded-xl border-2 border-slate-300 bg-white px-3 py-2 font-mono text-xs text-slate-800 outline-none focus:border-brand-500"
                />
                <div className="mt-1.5 flex flex-wrap gap-1">
                  {['llama3.1', 'qwen2.5:7b', 'gemma2:9b'].map((m) => (
                    <button
                      key={m}
                      type="button"
                      onClick={() => applyPatch({ ollamaModel: m }, `Đã chọn model ${m}`)}
                      className="rounded-md bg-slate-100 px-2 py-0.5 font-mono text-[11px] text-slate-600 hover:bg-slate-200"
                    >
                      {m}
                    </button>
                  ))}
                </div>
              </div>

              <p className="rounded-lg bg-slate-50 p-2 text-[11px] text-slate-500">
                <Cpu className="mr-1 inline h-3.5 w-3.5 text-slate-400" />
                Mẹo bật CORS khi chạy Ollama:
                <code className="ml-1 font-mono font-semibold text-slate-700">
                  OLLAMA_ORIGINS=* ollama serve
                </code>
              </p>
            </div>
          </div>
        </div>
      </Card>

      {/* SECTION 3: CÔNG CỤ HỌC TẬP & QUẢN LÝ DỮ LIỆU */}
      <Card className="p-5">
        <SectionTitle
          icon={BookOpenCheck}
          title="3. Tùy chọn Công cụ Học tập & Dữ liệu"
          subtitle="Bật/tắt thanh công cụ bôi đen (Highlight / Ghi chú / Tra từ), điều chỉnh giọng đọc và quản lý bộ nhớ."
        />

        <div className="grid gap-5 md:grid-cols-2">
          {/* Highlight & TTS */}
          <div className="space-y-4 rounded-2xl border-2 border-slate-200 bg-slate-50/50 p-4">
            <div className="flex items-center justify-between gap-3">
              <div className="flex items-start gap-2.5">
                <Highlighter className="mt-0.5 h-5 w-5 shrink-0 text-sky-600" />
                <div>
                  <p className="text-sm font-extrabold text-slate-900">
                    Highlight nội dung, Ghi chú &amp; Tra từ khi bôi đen
                  </p>
                  <p className="text-xs text-slate-500">
                    Khi bật, bôi đen bất kỳ từ hoặc câu nào sẽ hiện thanh công cụ chọn màu, gạch chân đỏ,
                    thêm ghi chú và tra nghĩa trực tiếp.
                  </p>
                </div>
              </div>
              <button
                type="button"
                role="switch"
                aria-checked={highlightEnabled}
                onClick={() =>
                  applyPatch(
                    { highlightEnabled: !highlightEnabled },
                    !highlightEnabled ? 'Đã bật Highlight nội dung' : 'Đã tắt Highlight nội dung',
                  )
                }
                className={`relative inline-flex h-7 w-12 shrink-0 cursor-pointer items-center rounded-full transition-colors ${
                  highlightEnabled ? 'bg-[#1cb0f6]' : 'bg-slate-300'
                }`}
              >
                <span
                  className={`inline-block h-5 w-5 transform rounded-full bg-white shadow transition-transform ${
                    highlightEnabled ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>

            <div className="border-t border-slate-200 pt-3">
              <label className="mb-2 flex items-center gap-1.5 text-xs font-extrabold uppercase tracking-wide text-slate-600">
                <Volume2 className="h-4 w-4 text-sky-600" />
                Tốc độ phát âm tiếng Anh (Web Speech TTS)
              </label>
              <div className="flex flex-wrap gap-2">
                {TTS_RATES.map((r) => {
                  const active = Math.abs(ttsRate - r.value) < 0.03;
                  return (
                    <button
                      key={r.value}
                      type="button"
                      onClick={() =>
                        applyPatch({ ttsRate: r.value }, `Đã đặt tốc độ đọc ${r.label}`)
                      }
                      className={`rounded-xl border-2 px-3 py-1.5 text-xs font-bold transition-colors ${
                        active
                          ? 'border-[#1cb0f6] bg-[#ddf4ff] text-[#0b6ea8]'
                          : 'border-slate-200 bg-white text-slate-600 hover:bg-slate-100'
                      }`}
                    >
                      {r.label}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Quản lý dữ liệu */}
          <div className="flex flex-col justify-between space-y-4 rounded-2xl border-2 border-slate-200 bg-slate-50/50 p-4">
            <div>
              <h4 className="text-sm font-extrabold text-slate-900">Quản lý bộ nhớ học tập</h4>
              <p className="mt-1 text-xs text-slate-500">
                Toàn bộ lịch sử luyện đề, thẻ SRS, ghi chú highlight và tiến độ bài học được lưu cục bộ
                trong trình duyệt của bạn.
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-2.5">
              {!confirmClearHist ? (
                <Button
                  size="sm"
                  variant="secondary"
                  type="button"
                  onClick={() => setConfirmClearHist(true)}
                >
                  <Trash2 className="h-3.5 w-3.5" />
                  Xóa toàn bộ lịch sử làm bài
                </Button>
              ) : (
                <div className="flex items-center gap-2 rounded-xl border border-rose-200 bg-rose-50 px-3 py-1.5">
                  <span className="text-xs font-bold text-rose-800">Xác nhận xóa lịch sử?</span>
                  <Button
                    size="sm"
                    variant="danger"
                    type="button"
                    onClick={() => {
                      clearHistory(null);
                      setConfirmClearHist(false);
                      notifySaved('Đã xóa toàn bộ lịch sử làm bài');
                    }}
                  >
                    Xóa ngay
                  </Button>
                  <Button
                    size="sm"
                    variant="ghost"
                    type="button"
                    onClick={() => setConfirmClearHist(false)}
                  >
                    Hủy
                  </Button>
                </div>
              )}

              {!confirmResetAll ? (
                <Button
                  size="sm"
                  variant="ghost"
                  type="button"
                  onClick={() => setConfirmResetAll(true)}
                >
                  <RotateCcw className="h-3.5 w-3.5" />
                  Khôi phục gốc (Xóa hết dữ liệu)
                </Button>
              ) : (
                <div className="flex items-center gap-2 rounded-xl border border-rose-300 bg-rose-50 px-3 py-1.5">
                  <span className="text-xs font-bold text-rose-800">
                    Xóa mọi tiến độ, SRS &amp; cài đặt?
                  </span>
                  <Button
                    size="sm"
                    variant="danger"
                    type="button"
                    onClick={() => {
                      clearAll();
                      updateSettings({ ...DEFAULT_SETTINGS });
                      if (setProgress) setProgress(loadProgress());
                      if (setSrs) setSrs(loadSrs());
                      setConfirmResetAll(false);
                      notifySaved('Đã khôi phục toàn bộ dữ liệu về mặc định');
                    }}
                  >
                    Đồng ý xóa hết
                  </Button>
                  <Button
                    size="sm"
                    variant="ghost"
                    type="button"
                    onClick={() => setConfirmResetAll(false)}
                  >
                    Hủy
                  </Button>
                </div>
              )}
            </div>

            <p className="flex items-center gap-1.5 text-[11px] text-slate-400">
              <Info className="h-3.5 w-3.5 shrink-0" />
              Mọi thay đổi được lưu tự động vào LocalStorage (namespace: toeic600.*).
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}
