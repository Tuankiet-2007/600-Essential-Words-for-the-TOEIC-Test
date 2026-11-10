/**
 * AskAiPopup.jsx — Khung chat Pop-up "Hỏi AI" Trợ lý Tiếng Anh & TOEIC.
 *
 * Tính năng:
 * - Khung chat nổi (Floating Pop-up) ở góc phải dưới, có thể thu nhỏ/mở rộng.
 * - Giải đáp từ vựng, ngữ pháp, mẹo làm đề thi và giải thích câu hỏi trong bài học.
 * - Tự động nhận diện ngữ cảnh bài học hiện tại (Lesson & Tab).
 * - Sử dụng chung cấu hình API (Gemini / OpenAI / Ollama) từ phần Cài đặt.
 * - Lưu lịch sử trò chuyện trong phiên làm việc (session/local).
 * - Hỗ trợ phát âm (Web Speech API) và sao chép câu trả lời.
 */
import { useEffect, useRef, useState } from 'react';
import {
  Bot,
  Check,
  ChevronDown,
  Copy,
  Maximize2,
  Minimize2,
  RotateCcw,
  Send,
  Sparkles,
  Volume2,
  X,
  ExternalLink,
  Loader2,
  MessageSquare,
} from 'lucide-react';
import { useApp } from '../lib/store.jsx';
import { callAiChat } from '../lib/aiChat.js';
import { useSpeech } from './ui.jsx';

const STORAGE_KEY = 'toeic600_ask_ai_history';

/**
 * Trình render Markdown đơn giản, an toàn cho câu trả lời của AI
 */
function FormattedMessage({ text }) {
  if (!text) return null;

  // Tách đoạn theo dòng trống
  const paragraphs = text.split(/\n\s*\n/);

  return (
    <div className="space-y-2 text-xs sm:text-[13px] leading-relaxed">
      {paragraphs.map((para, pIdx) => {
        // Danh sách gạch đầu dòng
        if (para.trim().startsWith('- ') || para.trim().startsWith('* ')) {
          const lines = para.split('\n');
          return (
            <ul key={pIdx} className="list-disc pl-4 space-y-1">
              {lines.map((l, lIdx) => {
                const item = l.replace(/^[-*]\s+/, '');
                return <li key={lIdx}>{formatInline(item)}</li>;
              })}
            </ul>
          );
        }

        // Danh sách đánh số
        if (/^\d+\.\s/.test(para.trim())) {
          const lines = para.split('\n');
          return (
            <ol key={pIdx} className="list-decimal pl-4 space-y-1">
              {lines.map((l, lIdx) => {
                const item = l.replace(/^\d+\.\s+/, '');
                return <li key={lIdx}>{formatInline(item)}</li>;
              })}
            </ol>
          );
        }

        // Dòng thông thường (hỗ trợ xuống dòng đơn lẻ)
        const lines = para.split('\n');
        return (
          <p key={pIdx}>
            {lines.map((line, lIdx) => (
              <span key={lIdx}>
                {formatInline(line)}
                {lIdx < lines.length - 1 ? <br /> : null}
              </span>
            ))}
          </p>
        );
      })}
    </div>
  );
}

/** Format in đậm (**bold**), nghiêng (*italic*), code (`code`) */
function formatInline(str) {
  if (!str) return '';
  // Tách theo token **bold**, `code`, *italic*
  const parts = str.split(/(\*\*.*?\*\*|`.*?`|\*.*?\*)/g);
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**') && part.length >= 4) {
      return (
        <strong key={i} className="font-extrabold text-[var(--color-duo-ink)]">
          {part.slice(2, -2)}
        </strong>
      );
    }
    if (part.startsWith('`') && part.endsWith('`') && part.length >= 2) {
      return (
        <code
          key={i}
          className="rounded bg-slate-200/70 dark:bg-slate-700/80 px-1 py-0.5 font-mono text-[11px] font-bold text-sky-700 dark:text-sky-300"
        >
          {part.slice(1, -1)}
        </code>
      );
    }
    if (part.startsWith('*') && part.endsWith('*') && part.length >= 2) {
      return (
        <em key={i} className="italic">
          {part.slice(1, -1)}
        </em>
      );
    }
    return part;
  });
}

export default function AskAiPopup() {
  const {
    askAiOpen,
    closeAskAi,
    openAskAi,
    askAiContext,
    settings,
    openSettings,
    lessonId,
    lesson,
    tab,
  } = useApp();
  const { speak, supported: speechSupported } = useSpeech();

  const [messages, setMessages] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [copiedIdx, setCopiedIdx] = useState(null);
  const [isExpanded, setIsExpanded] = useState(false);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Lưu tin nhắn vào localStorage
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
    } catch {
      /* ignore */
    }
  }, [messages]);

  // Tự động cuộn xuống tin nhắn mới nhất
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (askAiOpen) {
      scrollToBottom();
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [askAiOpen, messages, loading]);

  // Nếu mở bằng ngữ cảnh cụ thể (ví dụ bôi đen một câu hoặc bấm Hỏi AI từ selection)
  useEffect(() => {
    if (askAiOpen && askAiContext) {
      setInput(askAiContext);
      setTimeout(() => inputRef.current?.focus(), 150);
    }
  }, [askAiOpen, askAiContext]);

  // Provider & Model hiện tại theo Cài đặt
  const activeProvider = settings?.aiLabProvider || settings?.provider || 'gemini';
  const providerLabel =
    activeProvider === 'gemini'
      ? `Gemini (${settings?.geminiModel || '2.5 Flash'})`
      : activeProvider === 'openai'
        ? `OpenAI (${settings?.openaiModel || 'gpt-4o-mini'})`
        : `Ollama (${settings?.ollamaModel || 'llama3.1'})`;

  // Gợi ý câu hỏi nhanh
  const quickPrompts = [
    `Giải thích các từ vựng trọng tâm trong Bài ${String(lessonId).padStart(2, '0')}: ${lesson?.title || ''}`,
    'Phân biệt cách dùng cấu trúc "in order to" và "so as to"',
    'Cách phân biệt từ loại (Noun/Verb/Adj/Adv) trong đề thi TOEIC Part 5',
    'Cho 3 câu ví dụ giao tiếp thực tế với từ vựng bài này',
  ];

  const handleSend = async (textToSend) => {
    const text = (textToSend || input).trim();
    if (!text || loading) return;

    const userMsg = { role: 'user', content: text, createdAt: new Date().toISOString() };
    const nextMessages = [...messages, userMsg];
    setMessages(nextMessages);
    setInput('');
    setLoading(true);

    const currentContext = `Người học đang ở Lesson ${lessonId} (${lesson?.title || ''}), Tab: ${tab}.`;
    const res = await callAiChat(nextMessages, settings, currentContext);

    if (res.ok) {
      setMessages([
        ...nextMessages,
        {
          role: 'assistant',
          content: res.text,
          createdAt: new Date().toISOString(),
          provider: res.provider,
        },
      ]);
    } else {
      setMessages([
        ...nextMessages,
        {
          role: 'assistant',
          content: res.error || 'Có lỗi xảy ra khi gọi AI.',
          isError: true,
          missingKey: res.missingKey,
          createdAt: new Date().toISOString(),
        },
      ]);
    }
    setLoading(false);
  };

  const handleClearChat = () => {
    if (window.confirm('Bạn có chắc chắn muốn xóa toàn bộ lịch sử trò chuyện?')) {
      setMessages([]);
      localStorage.removeItem(STORAGE_KEY);
    }
  };

  const handleCopy = (text, idx) => {
    navigator.clipboard?.writeText(text);
    setCopiedIdx(idx);
    setTimeout(() => setCopiedIdx(null), 2000);
  };

  return (
    <>
      {/* 1. NÚT NỔI (FAB) Ở GÓC DƯỚI PHẢI KHI ĐANG ĐÓNG KHUNG CHAT */}
      {!askAiOpen && (
        <button
          type="button"
          onClick={() => openAskAi()}
          aria-label="Mở Trợ lý Hỏi AI"
          className="fixed bottom-5 right-5 z-40 flex items-center gap-2 rounded-full bg-gradient-to-r from-purple-600 via-indigo-600 to-sky-500 px-4 py-3 font-black text-white shadow-xl hover:scale-105 active:scale-95 transition-all duration-200 group"
          title="Hỏi AI Trợ Lý Tiếng Anh & TOEIC"
        >
          <Sparkles className="h-5 w-5 animate-pulse text-amber-300" />
          <span className="text-sm font-extrabold tracking-wide">Hỏi AI</span>
          <span className="hidden sm:inline-block rounded-full bg-white/20 px-2 py-0.5 text-[10px] uppercase font-bold text-white">
            Trợ lý
          </span>
        </button>
      )}

      {/* 2. KHUNG POP-UP CHAT KHI ĐANG BẬT */}
      {askAiOpen && (
        <div
          className={`fixed z-50 flex flex-col overflow-hidden rounded-2xl border-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg)] text-[var(--color-duo-ink)] shadow-2xl transition-all duration-200 ${
            isExpanded
              ? 'inset-3 sm:inset-10 sm:max-w-4xl sm:mx-auto'
              : 'bottom-4 right-4 sm:bottom-6 sm:right-6 w-[calc(100vw-2rem)] sm:w-[420px] h-[580px] max-h-[85vh]'
          }`}
        >
          {/* Header */}
          <div className="flex items-center justify-between border-b-2 border-[var(--color-duo-line)] bg-gradient-to-r from-purple-600 via-indigo-600 to-sky-600 px-4 py-3 text-white">
            <div className="flex items-center gap-2.5 min-w-0">
              <span className="flex h-8 w-8 items-center justify-center rounded-xl bg-white/20 text-white shadow-inner">
                <Bot className="h-5 w-5 text-amber-300" />
              </span>
              <div className="min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-black tracking-wide truncate">
                    Ask AI · Trợ Lý TOEIC
                  </h3>
                </div>
                <button
                  type="button"
                  onClick={openSettings}
                  className="flex items-center gap-1 text-[10.5px] font-bold text-white/80 hover:text-white truncate"
                  title="Thay đổi mô hình hoặc API Key trong Cài đặt"
                >
                  <span className="inline-block h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
                  <span className="truncate">{providerLabel}</span>
                  <ExternalLink className="h-3 w-3 inline opacity-70" />
                </button>
              </div>
            </div>

            <div className="flex items-center gap-1 shrink-0">
              {messages.length > 0 && (
                <button
                  type="button"
                  onClick={handleClearChat}
                  className="rounded-lg p-1.5 text-white/80 hover:bg-white/20 hover:text-white transition-colors"
                  title="Xóa lịch sử chat"
                >
                  <RotateCcw className="h-4 w-4" />
                </button>
              )}
              <button
                type="button"
                onClick={() => setIsExpanded((prev) => !prev)}
                className="hidden sm:inline-flex rounded-lg p-1.5 text-white/80 hover:bg-white/20 hover:text-white transition-colors"
                title={isExpanded ? 'Thu nhỏ cửa sổ' : 'Phóng to cửa sổ'}
              >
                {isExpanded ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
              </button>
              <button
                type="button"
                onClick={closeAskAi}
                className="rounded-lg p-1.5 text-white/80 hover:bg-white/20 hover:text-white transition-colors"
                title="Đóng (Esc)"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
          </div>

          {/* Vùng tin nhắn chat */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3.5 bg-[var(--color-duo-bg-soft)]">
            {messages.length === 0 ? (
              <div className="py-6 px-2 text-center space-y-4">
                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-tr from-purple-500 to-indigo-500 text-white shadow-md">
                  <Sparkles className="h-6 w-6 text-amber-200" />
                </div>
                <div>
                  <h4 className="text-sm font-black text-[var(--color-duo-ink)]">
                    Xin chào! Tôi có thể giúp gì cho bạn hôm nay?
                  </h4>
                  <p className="mt-1 text-xs text-[var(--color-duo-muted)]">
                    Hỏi giải thích câu hỏi trong đề, phân biệt ngữ pháp, từ vựng hoặc dịch thuật bối cảnh TOEIC.
                  </p>
                </div>

                {/* Gợi ý câu hỏi nhanh */}
                <div className="pt-2 text-left space-y-1.5">
                  <p className="text-[11px] font-black uppercase tracking-wider text-[var(--color-duo-muted)]">
                    Gợi ý câu hỏi nhanh:
                  </p>
                  {quickPrompts.map((p, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => handleSend(p)}
                      className="w-full text-left rounded-xl border border-[var(--color-duo-line)] bg-[var(--color-duo-bg)] p-2.5 text-xs font-bold text-[var(--color-duo-ink)] hover:border-purple-500 hover:bg-purple-50/50 dark:hover:bg-purple-950/20 transition-all shadow-2xs"
                    >
                      💡 {p}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              messages.map((m, idx) => {
                const isUser = m.role === 'user';
                return (
                  <div
                    key={idx}
                    className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}
                  >
                    <div
                      className={`max-w-[88%] rounded-2xl p-3 shadow-2xs transition-all ${
                        isUser
                          ? 'bg-gradient-to-br from-indigo-600 to-sky-600 text-white font-medium rounded-br-xs'
                          : m.isError
                            ? 'border-2 border-rose-300 bg-rose-50 dark:bg-rose-950/30 text-rose-900 dark:text-rose-200 rounded-bl-xs'
                            : 'border-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg)] text-[var(--color-duo-ink)] rounded-bl-xs'
                      }`}
                    >
                      <FormattedMessage text={m.content} />

                      {/* Thông báo thiếu API Key kèm nút 1-click */}
                      {m.missingKey && (
                        <div className="mt-2.5 pt-2 border-t border-rose-200 dark:border-rose-800">
                          <button
                            type="button"
                            onClick={() => {
                              closeAskAi();
                              openSettings();
                            }}
                            className="inline-flex items-center gap-1.5 rounded-lg bg-rose-600 px-3 py-1.5 text-xs font-extrabold text-white shadow hover:bg-rose-700"
                          >
                            <span>Đi tới Cài đặt để thêm API Key</span>
                            <ExternalLink className="h-3.5 w-3.5" />
                          </button>
                        </div>
                      )}

                      {/* Action buttons cho câu trả lời của AI */}
                      {!isUser && !m.isError && (
                        <div className="mt-2.5 flex items-center justify-between border-t border-[var(--color-duo-line)] pt-1.5 text-[11px] text-[var(--color-duo-muted)]">
                          <span className="text-[10px] font-bold">
                            {m.provider ? `${m.provider}` : 'AI'}
                          </span>
                          <div className="flex items-center gap-1">
                            {speechSupported && (
                              <button
                                type="button"
                                onClick={() => speak(m.content)}
                                className="rounded-md p-1 hover:bg-[var(--color-duo-line)] hover:text-[var(--color-duo-ink)] transition-colors"
                                title="Đọc to câu trả lời"
                              >
                                <Volume2 className="h-3.5 w-3.5" />
                              </button>
                            )}
                            <button
                              type="button"
                              onClick={() => handleCopy(m.content, idx)}
                              className="rounded-md p-1 hover:bg-[var(--color-duo-line)] hover:text-[var(--color-duo-ink)] transition-colors"
                              title="Sao chép nội dung"
                            >
                              {copiedIdx === idx ? (
                                <Check className="h-3.5 w-3.5 text-emerald-600" />
                              ) : (
                                <Copy className="h-3.5 w-3.5" />
                              )}
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })
            )}

            {/* Loading indicator */}
            {loading && (
              <div className="flex items-center gap-2 rounded-2xl border-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg)] p-3 text-xs font-bold text-[var(--color-duo-muted)] w-fit">
                <Loader2 className="h-4 w-4 animate-spin text-purple-600" />
                <span>AI đang phân tích và soạn câu trả lời…</span>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Ô nhập câu hỏi */}
          <div className="border-t-2 border-[var(--color-duo-line)] p-3 bg-[var(--color-duo-bg)]">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
              className="flex items-end gap-2"
            >
              <textarea
                ref={inputRef}
                rows={1}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
                placeholder="Hỏi AI bất kỳ điều gì về tiếng Anh, TOEIC..."
                className="flex-1 max-h-28 min-h-[40px] resize-none rounded-xl border-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg-soft)] p-2.5 text-xs sm:text-sm font-semibold text-[var(--color-duo-ink)] outline-none focus:border-purple-600 transition-colors"
              />
              <button
                type="submit"
                disabled={loading || !input.trim()}
                className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-purple-600 text-white shadow-md hover:bg-purple-700 disabled:opacity-40 disabled:cursor-not-allowed active:scale-95 transition-all"
                title="Gửi câu hỏi (Enter)"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
              </button>
            </form>
            <div className="mt-1 flex items-center justify-between px-1 text-[10px] font-bold text-[var(--color-duo-muted)]">
              <span>Enter để gửi · Shift+Enter để xuống dòng</span>
              <span>Cài đặt API ở mục Cài đặt ⚙️</span>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
