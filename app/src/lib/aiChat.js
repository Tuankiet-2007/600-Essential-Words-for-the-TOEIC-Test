/**
 * aiChat.js — Xử lý gọi API trò chuyện với Trợ lý AI (Ask AI).
 *
 * Tận dụng chung cấu hình trong Cài đặt (Settings):
 * - Gemini API (Google AI Studio hoặc reverse proxy riêng)
 * - OpenAI API & tương thích (OpenAI, DeepSeek, Groq, OpenRouter, Proxy riêng)
 * - Ollama (Local AI)
 */

export function resolveGeminiUrl(customUrl, model, key) {
  const raw = String(customUrl || '').trim().replace(/\/+$/, '');
  const base = raw || 'https://generativelanguage.googleapis.com';
  if (base.includes(':generateContent')) {
    return base.includes('key=') ? base : `${base}?key=${encodeURIComponent(key)}`;
  }
  if (base.includes('/v1beta/models') || base.includes('/v1/models')) {
    return `${base}/${encodeURIComponent(model)}:generateContent?key=${encodeURIComponent(key)}`;
  }
  return `${base}/v1beta/models/${encodeURIComponent(model)}:generateContent?key=${encodeURIComponent(key)}`;
}

export function resolveOpenAiUrl(customUrl) {
  const raw = String(customUrl || '').trim().replace(/\/+$/, '');
  if (!raw) return 'https://api.openai.com/v1/chat/completions';
  if (raw.endsWith('/chat/completions')) return raw;
  if (raw.endsWith('/v1')) return `${raw}/chat/completions`;
  return `${raw}/chat/completions`;
}

export async function callAiChat(messages, settings, currentContext = '') {
  const s = settings || {};
  const provider = s.aiLabProvider || s.provider || 'gemini';

  let systemPrompt = `Bạn là Trợ lý AI Gia sư tiếng Anh thông minh và tận tâm trong ứng dụng học "600 Essential Words for the TOEIC Test".
Nhiệm vụ của bạn:
1. Giải đáp mọi thắc mắc về tiếng Anh: từ vựng, ngữ pháp, thành ngữ, collocations, phát âm, mẹo làm bài thi TOEIC.
2. Phân tích chi tiết câu hỏi và đáp án trong đề thi TOEIC (Part 1 - Part 7), giải thích tại sao đáp án đúng và vì sao các đáp án khác sai.
3. Luôn trả lời bằng tiếng Việt thân thiện, rõ ràng, sư phạm, có cấu trúc tốt, định dạng Markdown đẹp mắt (in đậm, gạch đầu dòng, ví dụ song ngữ Anh-Việt).
4. Khi đưa ra từ mới hoặc ví dụ tiếng Anh, hãy kèm theo nghĩa tiếng Việt và cách dùng trong bối cảnh thương mại / công sở (TOEIC context).`;

  if (currentContext) {
    systemPrompt += `\n\n[Thông tin ngữ cảnh học tập hiện tại của người dùng: ${currentContext}]`;
  }

  // 1. Google Gemini
  if (provider === 'gemini') {
    const key = String(s.geminiKey || '').trim();
    if (!key) {
      return {
        ok: false,
        missingKey: true,
        provider: 'Gemini',
        error: 'Chưa cấu hình Gemini API Key. Vui lòng vào Cài đặt để thêm khóa API (hoàn toàn miễn phí từ Google AI Studio).',
      };
    }
    const model =
      String(s.geminiModel || (s.provider === 'gemini' ? s.model : '') || 'gemini-2.5-flash').trim() ||
      'gemini-2.5-flash';
    const url = resolveGeminiUrl(s.geminiUrl, model, key);

    const contents = messages.map((m) => ({
      role: m.role === 'assistant' ? 'model' : 'user',
      parts: [{ text: m.content }],
    }));

    const body = {
      system_instruction: {
        parts: [{ text: systemPrompt }],
      },
      contents,
    };

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        let detail = '';
        try {
          detail = (await res.text()).slice(0, 300);
        } catch {
          detail = '';
        }
        if (res.status === 401 || res.status === 403) {
          return {
            ok: false,
            missingKey: true,
            provider: 'Gemini',
            error: 'Gemini API key không hợp lệ hoặc đã hết hạn.',
          };
        }
        if (res.status === 429) {
          return {
            ok: false,
            provider: 'Gemini',
            error: 'Đã vượt hạn mức gọi API Gemini (Rate limit), vui lòng đợi một chút rồi thử lại.',
          };
        }
        return {
          ok: false,
          provider: 'Gemini',
          error: `Lỗi kết nối Gemini (HTTP ${res.status}): ${detail}`,
        };
      }

      const json = await res.json();
      const text =
        json?.candidates?.[0]?.content?.parts?.map((p) => p.text || '').join('') || '';
      if (!text.trim()) {
        return {
          ok: false,
          provider: 'Gemini',
          error: 'AI không trả về nội dung. Vui lòng thử lại câu hỏi khác.',
        };
      }
      return { ok: true, provider: 'Gemini', text: text.trim() };
    } catch (err) {
      return { ok: false, provider: 'Gemini', error: `Lỗi mạng khi gọi Gemini: ${err.message}` };
    }
  }

  // 2. OpenAI
  if (provider === 'openai') {
    const key = String(s.openaiKey || '').trim();
    if (!key) {
      return {
        ok: false,
        missingKey: true,
        provider: 'OpenAI',
        error: 'Chưa cấu hình OpenAI API Key. Vui lòng vào Cài đặt để thêm khóa API.',
      };
    }
    const model =
      String(
        s.openaiModel ||
          (s.provider === 'openai' && !String(s.model || '').startsWith('gemini') ? s.model : '') ||
          'gpt-4o-mini',
      ).trim() || 'gpt-4o-mini';
    const url = resolveOpenAiUrl(s.openaiUrl);

    const reqMessages = [
      { role: 'system', content: systemPrompt },
      ...messages.map((m) => ({ role: m.role, content: m.content })),
    ];

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${key}`,
        },
        body: JSON.stringify({
          model,
          messages: reqMessages,
        }),
      });

      if (!res.ok) {
        let detail = '';
        try {
          detail = (await res.text()).slice(0, 300);
        } catch {
          detail = '';
        }
        if (res.status === 401 || res.status === 403) {
          return {
            ok: false,
            missingKey: true,
            provider: 'OpenAI',
            error: 'OpenAI API key không hợp lệ hoặc hết hạn ngạch credit.',
          };
        }
        if (res.status === 429) {
          return {
            ok: false,
            provider: 'OpenAI',
            error: 'Vượt hạn mức OpenAI (Rate limit) hoặc tài khoản hết số dư.',
          };
        }
        return { ok: false, provider: 'OpenAI', error: `Lỗi kết nối OpenAI: ${detail}` };
      }

      const json = await res.json();
      const text = json?.choices?.[0]?.message?.content || '';
      if (!text.trim()) {
        return { ok: false, provider: 'OpenAI', error: 'AI không trả về nội dung.' };
      }
      return { ok: true, provider: 'OpenAI', text: text.trim() };
    } catch (err) {
      return { ok: false, provider: 'OpenAI', error: `Lỗi mạng khi gọi OpenAI: ${err.message}` };
    }
  }

  // 3. Ollama (Local)
  if (provider === 'ollama') {
    const raw = String(s.ollamaUrl ?? '').trim().replace(/\/+$/, '');
    const base = raw || 'http://localhost:11434';
    const model = String(s.ollamaModel || 'llama3.1').trim() || 'llama3.1';
    const url = `${base}/api/chat`;

    const reqMessages = [
      { role: 'system', content: systemPrompt },
      ...messages.map((m) => ({ role: m.role, content: m.content })),
    ];

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model,
          messages: reqMessages,
          stream: false,
        }),
      });

      if (!res.ok) {
        return { ok: false, provider: 'Ollama', error: `Lỗi từ Ollama (HTTP ${res.status})` };
      }

      const json = await res.json();
      const text = json?.message?.content || '';
      return { ok: true, provider: 'Ollama', text: text.trim() };
    } catch (err) {
      return {
        ok: false,
        provider: 'Ollama',
        error: `Không thể kết nối tới Ollama tại ${base}. Hãy đảm bảo Ollama đã khởi động và cho phép CORS.`,
      };
    }
  }

  return { ok: false, provider, error: `Provider không được hỗ trợ: ${provider}` };
}
