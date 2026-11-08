/**
 * Tab 4 — AI Sentence Lab (Luyện đặt câu theo ngữ cảnh TOEIC).
 *
 * QUAN TRỌNG:
 *  - Phần cấu hình chi tiết API key & chọn mô hình đã được gộp tập trung vào mục
 *    Cài đặt hệ thống (SettingsView.jsx). Đầu tab hiển thị thanh trạng thái gọn nhẹ
 *    cho biết đang dùng mô hình nào và nút mở nhanh trang Cài đặt.
 *  - Tab này PHẢI dùng được cả khi lesson === null (verify_tabs.mjs SSR check).
 *  - Mọi fetch đều nằm trong try/catch, không để unhandled rejection.
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  CheckCircle2,
  Cpu,
  FileQuestion,
  Info,
  KeyRound,
  Languages,
  Lightbulb,
  Loader2,
  PenLine,
  RefreshCw,
  Send,
  Settings2,
  Sparkles,
  Wand2,
} from 'lucide-react';
import {
  Badge,
  Button,
  Card,
  EmptyState,
  Highlighted,
  SectionTitle,
  useSpeech,
} from '../components/ui.jsx';
import { callAiForFeature, maskKey } from '../components/SettingsView.jsx';
import { useApp } from '../lib/store.jsx';

/* ------------------------------------------------------------------ */
/* Hằng số & tiện ích                                                  */
/* ------------------------------------------------------------------ */

const PROVIDERS = [
  { id: 'gemini', label: 'Google Gemini' },
  { id: 'openai', label: 'OpenAI (GPT)' },
  { id: 'ollama', label: 'Ollama (Local AI)' },
];

/** Strips ```json ... ``` fences và lấy object JSON đầu tiên. */
function stripFences(raw) {
  let t = String(raw ?? '').trim();
  t = t.replace(/^```(?:json|JSON)?\s*/, '').replace(/```\s*$/, '').trim();
  if (!t) return t;
  const start = t.search(/[[{]/);
  if (start > 0) t = t.slice(start);
  const lastBrace = Math.max(t.lastIndexOf('}'), t.lastIndexOf(']'));
  if (lastBrace >= 0) t = t.slice(0, lastBrace + 1);
  return t.trim();
}

/** Parse JSON phòng thủ. Trả {ok:true,data} hoặc {ok:false,raw}. Không bao giờ throw. */
function parseAiJson(raw) {
  if (raw == null) return { ok: false, raw: '' };
  try {
    return { ok: true, data: JSON.parse(raw) };
  } catch {
    /* thử tiếp */
  }
  const cleaned = stripFences(raw);
  try {
    return { ok: true, data: JSON.parse(cleaned) };
  } catch {
    return { ok: false, raw: String(raw) };
  }
}

/**
 * Gọi provider AI cho tính năng Luyện đặt câu (Tab 4).
 * Sử dụng settings.aiLabProvider || settings.provider || 'gemini'.
 */
async function callAi(prompt, settings) {
  return callAiForFeature(prompt, settings, 'aiLab');
}

/* ------------------------------------------------------------------ */
/* Thanh trạng thái AI gọn nhẹ (thay cho form cài đặt dài trước đây)   */
/* ------------------------------------------------------------------ */

function AiProviderStatusBanner() {
  const { settings, openSettings } = useApp();
  const provider = settings?.aiLabProvider || settings?.provider || 'gemini';
  const providerLabel = PROVIDERS.find((p) => p.id === provider)?.label || provider;

  const activeModel =
    provider === 'gemini'
      ? settings?.geminiModel || settings?.model || 'gemini-2.5-flash'
      : provider === 'openai'
        ? settings?.openaiModel || settings?.model || 'gpt-4o-mini'
        : settings?.ollamaModel || 'llama3.1';

  const currentKey =
    provider === 'gemini'
      ? settings?.geminiKey
      : provider === 'openai'
        ? settings?.openaiKey
        : '';
  const hasKey = provider === 'ollama' ? true : Boolean(String(currentKey || '').trim());

  return (
    <Card className="mb-4 px-4 py-3">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-2.5">
          <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[var(--color-duo-blue-light)] text-[var(--color-duo-blue)]">
            <Settings2 className="h-5 w-5" />
          </span>
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-sm font-extrabold text-slate-900">
                AI Luyện đặt câu: {providerLabel}
              </span>
              <Badge tone="slate">{activeModel}</Badge>
              {provider === 'ollama' ? (
                <Badge tone="violet">Local · Không cần API key</Badge>
              ) : hasKey ? (
                <Badge tone="emerald">
                  <CheckCircle2 className="h-3 w-3" />
                  Đã có API key ({maskKey(currentKey)})
                </Badge>
              ) : (
                <Badge tone="amber">
                  <KeyRound className="h-3 w-3" />
                  Chưa nhập API key
                </Badge>
              )}
            </div>
            <p className="mt-0.5 text-xs text-slate-500">
              Toàn bộ tùy chọn nhà cung cấp AI (cho cả Luyện đặt câu &amp; Tra từ bôi đen) được quản lý tập trung tại mục Cài đặt.
            </p>
          </div>
        </div>

        <Button size="sm" variant="secondary" onClick={openSettings}>
          <Settings2 className="h-4 w-4" />
          Cài đặt API &amp; Chọn mô hình
        </Button>
      </div>
    </Card>
  );
}

/* ------------------------------------------------------------------ */
/* Hiển thị kết quả chấm — có fallback raw text                         */
/* ------------------------------------------------------------------ */

function RawFallback({ text }) {
  return (
    <div className="rounded-lg border border-amber-200 bg-amber-50 px-3 py-2.5">
      <p className="mb-1 flex items-center gap-1.5 text-xs font-semibold text-amber-800">
        <AlertTriangle className="h-3.5 w-3.5" />
        AI không trả về JSON hợp lệ — hiển thị nguyên văn phản hồi:
      </p>
      <pre className="max-h-80 overflow-auto whitespace-pre-wrap break-words text-xs text-slate-700">{text}</pre>
    </div>
  );
}

function ErrorBox({ message, onOpenSettings }) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-rose-200 bg-rose-50 px-3 py-2.5 text-sm text-rose-800">
      <div className="flex items-start gap-2">
        <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
        <span>{message}</span>
      </div>
      {onOpenSettings ? (
        <Button size="sm" variant="secondary" onClick={onOpenSettings}>
          <Settings2 className="h-3.5 w-3.5" />
          Mở Cài đặt API
        </Button>
      ) : null}
    </div>
  );
}

function StepHeader({ n, title, active, done }) {
  return (
    <div className="mb-3 flex items-center gap-2">
      <span
        className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-xs font-bold ${
          done ? 'bg-emerald-100 text-emerald-700' : active ? 'bg-brand-600 text-white' : 'bg-slate-200 text-slate-500'
        }`}
      >
        {done ? <CheckCircle2 className="h-4 w-4" /> : n}
      </span>
      <h4 className="text-sm font-bold text-slate-900">{title}</h4>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Lab — chỉ render khi có lesson                                       */
/* ------------------------------------------------------------------ */

const JSON_RULES =
  'CHỈ trả về JSON hợp lệ, không kèm markdown, không kèm giải thích ngoài JSON.';

function Lab({ lesson }) {
  const { settings, openSettings } = useApp();
  const { speak } = useSpeech();

  const words = useMemo(() => lesson?.words_to_learn || [], [lesson]);
  const allWords = useMemo(() => words.map((w) => w.word).filter(Boolean), [words]);

  const [selected, setSelected] = useState(null);
  const [step, setStep] = useState(1);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const [promptData, setPromptData] = useState(null); // {vi_sentence, collocation_hint}
  const [promptRaw, setPromptRaw] = useState('');
  const [translation, setTranslation] = useState('');
  const [feedback, setFeedback] = useState(null); // parsed object
  const [feedbackRaw, setFeedbackRaw] = useState('');

  // Chọn từ đầu tiên khi đổi bài
  useEffect(() => {
    setSelected(words[0]?.word ?? null);
    setStep(1);
    setPromptData(null);
    setPromptRaw('');
    setTranslation('');
    setFeedback(null);
    setFeedbackRaw('');
    setError('');
  }, [lesson?.lesson_id]); // eslint-disable-line react-hooks/exhaustive-deps

  const entry = useMemo(() => words.find((w) => w.word === selected) || null, [words, selected]);

  /* ---------- Bước 1: sinh câu tiếng Việt ---------- */
  const generatePrompt = useCallback(async () => {
    if (!entry) {
      setError('Hãy chọn một từ mục tiêu trước.');
      return;
    }
    setBusy(true);
    setError('');
    setFeedback(null);
    setFeedbackRaw('');

    const prompt = `Bạn là giáo viên tiếng Anh thương mại luyện thi TOEIC.
Từ mục tiêu: "${entry.word}" (${entry.pos}) — nghĩa: ${entry.definition_vi}
Collocations trong sách: ${(entry.collocations || []).join('; ') || 'không có'}

Hãy viết ĐÚNG MỘT câu tiếng Việt ở văn phong công sở/kinh doanh (chuẩn TOEIC) mà khi dịch sang tiếng Anh BẮT BUỘC phải dùng từ mục tiêu ở đúng dạng ngữ pháp.
${JSON_RULES}
Schema: {"vi_sentence": string, "collocation_hint": string}
Trong đó "collocation_hint" là một cụm từ tiếng Anh gợi ý (ví dụ: "abide by a decision").`;

    const res = await callAi(prompt, settings);
    setBusy(false);

    if (!res.ok) {
      setError(res.error);
      return;
    }
    const parsed = parseAiJson(res.text);
    if (parsed.ok && parsed.data && typeof parsed.data === 'object') {
      setPromptData({
        vi_sentence: String(parsed.data.vi_sentence ?? parsed.data.viSentence ?? '').trim(),
        collocation_hint: String(parsed.data.collocation_hint ?? parsed.data.collocationHint ?? '').trim(),
      });
      setPromptRaw('');
    } else {
      setPromptData(null);
      setPromptRaw(res.text);
    }
    setTranslation('');
    setStep(2);
  }, [entry, settings]);

  /* ---------- Bước 3: chấm điểm ---------- */
  const grade = useCallback(async () => {
    if (!norm(translation)) {
      setError('Hãy nhập bản dịch tiếng Anh của bạn trước khi chấm điểm.');
      return;
    }
    setBusy(true);
    setError('');
    setFeedback(null);
    setFeedbackRaw('');

    const viSentence = promptData?.vi_sentence || promptRaw || '';
    const prompt = `Bạn là giám khảo TOEIC chuyên chấm phần viết.
Từ mục tiêu bắt buộc: "${entry?.word}" (${entry?.pos}) — nghĩa: ${entry?.definition_vi}
Câu tiếng Việt gốc: "${viSentence}"
Bản dịch tiếng Anh của học viên: "${translation}"

Hãy chấm điểm và phân tích. ${JSON_RULES}
Schema:
{
  "score": number,                       // thang điểm 0-10
  "usage_analysis": string,              // nhận xét cách dùng từ mục tiêu bằng tiếng Việt
  "grammar_errors": [                    // danh sách lỗi ngữ pháp
    {"error": string, "correction": string, "explanation": string}
  ],
  "rewrites": [                          // ĐÚNG 2 câu viết lại hay hơn, văn phong Business English
    {"text": string, "note": string}
  ],
  "common_phrases": [string]             // các cụm từ thường dùng liên quan
}`;

    const res = await callAi(prompt, settings);
    setBusy(false);

    if (!res.ok) {
      setError(res.error);
      return;
    }
    const parsed = parseAiJson(res.text);
    if (parsed.ok && parsed.data && typeof parsed.data === 'object') {
      setFeedback(parsed.data);
      setFeedbackRaw('');
    } else {
      setFeedback(null);
      setFeedbackRaw(res.text);
    }
    setStep(3);
  }, [entry, promptData, promptRaw, translation, settings]);

  const resetAll = () => {
    setStep(1);
    setPromptData(null);
    setPromptRaw('');
    setTranslation('');
    setFeedback(null);
    setFeedbackRaw('');
    setError('');
  };

  if (!words.length) {
    return (
      <EmptyState
        icon={FileQuestion}
        title="Bài này chưa có từ vựng"
        description="Cần words_to_learn để luyện viết câu với AI. Hãy chạy OCR để bổ sung dữ liệu cho bài này."
      />
    );
  }

  const activeProvider = settings?.aiLabProvider || settings?.provider || 'gemini';

  return (
    <div>
      {/* Bộ chọn từ mục tiêu */}
      <Card className="mb-4 px-4 py-3">
        <SectionTitle
          icon={Wand2}
          title="Chọn từ mục tiêu"
          subtitle="AI sẽ ra một câu tiếng Việt buộc bạn phải dùng đúng từ này trong bản dịch."
        />
        <div className="flex flex-wrap gap-2">
          {words.map((w) => (
            <button
              key={w.id ?? w.word}
              type="button"
              onClick={() => {
                setSelected(w.word);
                resetAll();
              }}
              className={`rounded-lg border px-2.5 py-1 text-sm font-medium transition-colors ${
                selected === w.word
                  ? 'border-brand-500 bg-brand-50 text-brand-700'
                  : 'border-slate-300 bg-white text-slate-600 hover:bg-slate-50'
              }`}
            >
              {w.word}
              <span className="ml-1 text-[11px] text-slate-400">{w.pos}</span>
            </button>
          ))}
        </div>
        {entry ? (
          <p className="mt-2 text-xs text-slate-500">
            Đang chọn: <span className="font-semibold text-slate-700">{entry.word}</span> —{' '}
            {entry.definition_vi}
          </p>
        ) : null}
      </Card>

      {error ? (
        <div className="mb-3">
          <ErrorBox message={error} onOpenSettings={openSettings} />
        </div>
      ) : null}

      {/* BƯỚC 1 */}
      <Card className="mb-4 px-4 py-4">
        <StepHeader n={1} title="Sinh đề bài tiếng Việt" active={step === 1} done={step > 1} />
        <p className="mb-3 text-sm text-slate-600">
          AI tạo một câu tiếng Việt trong ngữ cảnh công sở. Bạn sẽ dịch câu đó sang tiếng Anh, buộc phải
          dùng từ <span className="font-semibold">{selected}</span>.
        </p>
        <div className="flex flex-wrap items-center gap-2">
          <Button variant="primary" onClick={generatePrompt} disabled={busy || !entry}>
            {busy && step === 1 ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
            {busy && step === 1 ? 'Đang tạo đề…' : promptData ? 'Tạo đề khác' : 'Tạo đề bài'}
          </Button>
          {promptData || promptRaw ? (
            <Button variant="ghost" onClick={resetAll}>
              <RefreshCw className="h-4 w-4" />
              Làm lại từ đầu
            </Button>
          ) : null}
          <span className="text-xs text-slate-400">
            Provider: {PROVIDERS.find((p) => p.id === activeProvider)?.label}
          </span>
        </div>

        {promptData ? (
          <div className="mt-3 rounded-lg border border-brand-100 bg-brand-50/60 px-3 py-3">
            <p className="text-xs font-semibold uppercase tracking-wide text-brand-700">Câu tiếng Việt</p>
            <p className="mt-1 text-[15px] font-medium leading-7 text-slate-800">{promptData.vi_sentence}</p>
            {promptData.collocation_hint ? (
              <p className="mt-2 text-sm text-slate-600">
                <Lightbulb className="mr-1 inline h-3.5 w-3.5 text-amber-500" />
                Gợi ý collocation:{' '}
                <span className="font-semibold">
                  <Highlighted text={promptData.collocation_hint} words={allWords} />
                </span>
              </p>
            ) : null}
          </div>
        ) : promptRaw ? (
          <div className="mt-3">
            <RawFallback text={promptRaw} />
          </div>
        ) : null}
      </Card>

      {/* BƯỚC 2 */}
      <Card className="mb-4 px-4 py-4">
        <StepHeader n={2} title="Dịch sang tiếng Anh" active={step === 2} done={step > 2} />
        <textarea
          value={translation}
          onChange={(e) => setTranslation(e.target.value)}
          rows={3}
          placeholder="Nhập bản dịch tiếng Anh của bạn…"
          spellCheck={false}
          className="w-full rounded-lg border-2 border-slate-300 bg-white px-3 py-2 text-sm text-slate-800 outline-none focus:border-brand-500"
        />
        <div className="mt-3 flex flex-wrap items-center gap-2">
          <Button
            variant="primary"
            onClick={grade}
            disabled={busy || !entry || (!promptData && !promptRaw) || !norm(translation)}
          >
            {busy && step === 2 ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
            {busy && step === 2 ? 'Đang chấm…' : 'Nhờ AI chấm điểm'}
          </Button>
          {!promptData && !promptRaw ? (
            <span className="text-xs text-slate-500">Hãy tạo đề bài ở bước 1 trước.</span>
          ) : null}
          {translation ? (
            <Button variant="ghost" size="sm" onClick={() => speak(translation)}>
              Nghe thử
            </Button>
          ) : null}
        </div>
      </Card>

      {/* BƯỚC 3 */}
      <Card className="px-4 py-4">
        <StepHeader n={3} title="Phân tích & chấm điểm" active={step === 3} done={false} />

        {busy && step === 3 ? (
          <p className="flex items-center gap-2 text-sm text-slate-500">
            <Loader2 className="h-4 w-4 animate-spin" />
            AI đang phân tích bài viết của bạn…
          </p>
        ) : null}

        {feedbackRaw ? <RawFallback text={feedbackRaw} /> : null}

        {feedback ? <FeedbackView feedback={feedback} allWords={allWords} /> : null}

        {!feedback && !feedbackRaw && !busy ? (
          <p className="text-sm text-slate-500">
            Chưa có kết quả. Hoàn thành bước 2 rồi bấm “Nhờ AI chấm điểm”.
          </p>
        ) : null}
      </Card>
    </div>
  );
}

function norm(s) {
  return String(s ?? '').replace(/\s+/g, ' ').trim();
}

/* ------------------------------------------------------------------ */
/* Khung hiển thị kết quả chấm                                          */
/* ------------------------------------------------------------------ */

function FeedbackView({ feedback, allWords }) {
  const rawScore = feedback.score ?? feedback.total ?? feedback.points;
  const score = Number.isFinite(Number(rawScore)) ? Number(rawScore) : null;

  const usage =
    feedback.usage_analysis ?? feedback.usageAnalysis ?? feedback.usage ?? feedback.cach_dung_tu ?? '';
  const errors = Array.isArray(feedback.grammar_errors)
    ? feedback.grammar_errors
    : Array.isArray(feedback.grammarErrors)
      ? feedback.grammarErrors
      : [];
  const rewrites = Array.isArray(feedback.rewrites) ? feedback.rewrites.slice(0, 2) : [];
  const phrases = Array.isArray(feedback.common_phrases)
    ? feedback.common_phrases
    : Array.isArray(feedback.commonPhrases)
      ? feedback.commonPhrases
      : [];

  const tone = score == null ? 'slate' : score >= 8 ? 'emerald' : score >= 5 ? 'amber' : 'rose';

  return (
    <div className="space-y-4">
      {/* Điểm */}
      <div className="flex flex-wrap items-center gap-4 rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
        <div className="text-center">
          <p className="text-4xl font-black text-brand-600">{score == null ? '—' : score}</p>
          <p className="text-[11px] font-semibold uppercase tracking-wide text-slate-500">trên 10</p>
        </div>
        <Badge tone={tone}>
          {score == null
            ? 'AI không trả về điểm'
            : score >= 8
              ? 'Rất tốt'
              : score >= 5
                ? 'Tạm được'
                : 'Cần cải thiện'}
        </Badge>
        {score != null ? (
          <div className="ml-auto w-full max-w-[12rem]">
            <div className="h-2 w-full overflow-hidden rounded-full bg-slate-200">
              <div
                className={`h-full rounded-full ${
                  score >= 8 ? 'bg-emerald-500' : score >= 5 ? 'bg-amber-500' : 'bg-rose-500'
                }`}
                style={{ width: `${Math.min(100, (score / 10) * 100)}%` }}
              />
            </div>
          </div>
        ) : null}
      </div>

      {/* Cách dùng từ */}
      <div>
        <p className="mb-1 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-slate-500">
          <Languages className="h-3.5 w-3.5" />
          Cách dùng từ
        </p>
        <p className="text-sm leading-6 text-slate-700">
          {usage ? usage : <span className="italic text-slate-400">Không có nhận xét.</span>}
        </p>
      </div>

      {/* Lỗi ngữ pháp */}
      <div>
        <p className="mb-1.5 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-slate-500">
          <AlertTriangle className="h-3.5 w-3.5" />
          Lỗi ngữ pháp &amp; cách sửa
        </p>
        {errors.length === 0 ? (
          <p className="flex items-center gap-1.5 text-sm text-emerald-700">
            <CheckCircle2 className="h-4 w-4" />
            Không phát hiện lỗi ngữ pháp.
          </p>
        ) : (
          <ul className="space-y-2">
            {errors.map((e, i) => {
              const errText = typeof e === 'string' ? e : e?.error ?? e?.mistake ?? '';
              const corr = typeof e === 'string' ? '' : e?.correction ?? e?.fix ?? '';
              const expl = typeof e === 'string' ? '' : e?.explanation ?? e?.note ?? '';
              return (
                <li key={i} className="rounded-lg border border-slate-200 bg-white px-3 py-2">
                  <p className="text-sm text-rose-700">{errText || '(lỗi không mô tả)'}</p>
                  {corr ? (
                    <p className="mt-1 text-sm text-emerald-700">
                      <span className="font-semibold">Sửa lại: </span>
                      {corr}
                    </p>
                  ) : null}
                  {expl ? <p className="mt-1 text-xs text-slate-500">{expl}</p> : null}
                </li>
              );
            })}
          </ul>
        )}
      </div>

      {/* 2 câu viết lại */}
      <div>
        <p className="mb-1.5 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-slate-500">
          <PenLine className="h-3.5 w-3.5" />
          Hai câu viết lại theo Business English
        </p>
        {rewrites.length === 0 ? (
          <p className="text-sm italic text-slate-400">AI không trả về câu viết lại.</p>
        ) : (
          <ol className="space-y-2">
            {rewrites.map((r, i) => {
              const text = typeof r === 'string' ? r : r?.text ?? r?.sentence ?? '';
              const note = typeof r === 'string' ? '' : r?.note ?? r?.explanation ?? '';
              return (
                <li
                  key={i}
                  className="rounded-lg border border-emerald-100 bg-emerald-50/50 px-3 py-2"
                >
                  <p className="text-sm font-medium text-slate-800">
                    <span className="mr-1.5 font-bold text-emerald-700">{i + 1}.</span>
                    <Highlighted text={text} words={allWords} />
                  </p>
                  {note ? <p className="mt-1 text-xs text-slate-600">{note}</p> : null}
                </li>
              );
            })}
          </ol>
        )}
        {rewrites.length > 0 && rewrites.length < 2 ? (
          <p className="mt-1.5 text-xs text-amber-700">
            AI chỉ trả về {rewrites.length}/2 câu viết lại. Bấm chấm lại để thử lấy đủ 2 câu.
          </p>
        ) : null}
      </div>

      {/* Cụm từ thường dùng */}
      <div>
        <p className="mb-1.5 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-slate-500">
          <Cpu className="h-3.5 w-3.5" />
          Cụm từ thường dùng
        </p>
        {phrases.length === 0 ? (
          <p className="text-sm italic text-slate-400">Không có cụm từ gợi ý.</p>
        ) : (
          <ul className="flex flex-wrap gap-2">
            {phrases.map((p, i) => (
              <li key={i}>
                <span className="inline-block rounded-md bg-slate-100 px-2.5 py-1 text-sm text-slate-700">
                  <Highlighted text={typeof p === 'string' ? p : JSON.stringify(p)} words={allWords} />
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Tab 4 — LUÔN render AiProviderStatusBanner, kể cả khi lesson === null */
/* ------------------------------------------------------------------ */

export default function Tab4AiLab({ lesson }) {
  return (
    <div>
      <AiProviderStatusBanner />

      {!lesson ? (
        <EmptyState
          icon={FileQuestion}
          title="Cần dữ liệu bài học để luyện với AI"
          description="Bài này chưa được trích xuất (thiếu lessons_json/lesson_XX.json) nên chưa có danh sách từ mục tiêu. Bạn có thể bấm 'Cài đặt API & Chọn mô hình' ở trên để thiết lập trước. Hãy chạy OCR rồi quét lại, hoặc chọn bài khác."
        />
      ) : (
        <>
          <div className="mb-3 flex items-start gap-2 rounded-lg border border-sky-100 bg-sky-50 px-3 py-2.5 text-sm text-sky-900">
            <Info className="mt-0.5 h-4 w-4 shrink-0" />
            <span>
              Quy trình 3 bước: AI ra câu tiếng Việt → bạn dịch sang tiếng Anh → AI chấm điểm, chỉ lỗi ngữ
              pháp và gợi ý 2 câu viết lại chuẩn Business English.
            </span>
          </div>
          <Lab lesson={lesson} />
        </>
      )}
    </div>
  );
}
