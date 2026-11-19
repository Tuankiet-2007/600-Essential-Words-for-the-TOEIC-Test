// Persist the selected prompts and one vocabulary snapshot per word.
// Lesson bodies and result.item are available in memory and must not be duplicated.
export function packRecallDraft({ questions, results, ...state }) {
  const entries = {};
  const packedQuestions = questions.map(({ lessonObj, entry, ...question }) => {
    entries[question.wordKey] = entry;
    return question;
  });
  return {
    ...state, schema: 2, entries, questions: packedQuestions,
    results: results.map(({ item, ...result }) => result),
  };
}

export function unpackRecallDraft(draft, lessons) {
  if (![1, 2].includes(draft?.schema) || !Array.isArray(draft.questions) ||
      !Array.isArray(draft.results) || !Array.isArray(draft.committed) ||
      !draft.session?.versions || !Number.isInteger(draft.cursor) || draft.cursor < 0) {
    throw new Error('Phiên ôn đã lưu không hợp lệ.');
  }
  const questions = draft.questions.map((question) => {
    const entry = draft.schema === 2 ? draft.entries?.[question.wordKey] : question.entry;
    if (!entry?.word || !question.uid || !lessons[question.lessonId]) {
      throw new Error('Thiếu dữ liệu khôi phục phiên ôn.');
    }
    return { ...question, entry, lessonObj: lessons[question.lessonId] };
  });
  const byUid = new Map(questions.map((question) => [question.uid, question]));
  const results = draft.results.map(({ item, ...result }) => {
    const question = byUid.get(result.uid);
    if (!question || result.wordKey !== question.wordKey || typeof result.isCorrect !== 'boolean') {
      throw new Error('Kết quả phiên ôn không hợp lệ.');
    }
    return { ...result, item: question };
  });
  return { ...draft, questions, results };
}

function isQuotaError(error) {
  return ['QuotaExceededError', 'NS_ERROR_DOM_QUOTA_REACHED'].includes(error?.name);
}

export function saveRecallDraft(storage, key, draft) {
  const raw = JSON.stringify(draft);
  try {
    storage.setItem(key, raw);
    return;
  } catch (error) {
    if (!isQuotaError(error)) throw error;
  }

  // Older sessions under other filters can fill the same storage quota.
  for (let i = 0; i < storage.length; i += 1) {
    const otherKey = storage.key(i);
    if (!otherKey?.startsWith('toeic600.recallDraft:') || otherKey === key) continue;
    const previous = storage.getItem(otherKey);
    try {
      const legacy = JSON.parse(previous);
      if (legacy?.schema !== 1 || legacy.session?.scope !== otherKey ||
          !Array.isArray(legacy.questions) || !legacy.questions.every((q) => q?.entry?.word && q.wordKey)) continue;
      const compact = JSON.stringify(packRecallDraft(legacy));
      if (compact.length < previous.length) storage.setItem(otherKey, compact);
    } catch {
      // Keep unreadable or unwritable drafts intact and try any remaining keys.
    }
  }
  storage.setItem(key, raw);
}

export function recallDraftError(error) {
  if (isQuotaError(error)) {
    return 'Bộ nhớ lưu trữ của trang đã đầy, chưa lưu được phiên đang học. Hãy sao lưu dữ liệu trong Cài đặt trước khi dọn bộ nhớ.';
  }
  if (error?.name === 'SecurityError') {
    return 'Trình duyệt đang chặn lưu dữ liệu của trang. Hãy cho phép lưu trữ rồi thử lưu lại.';
  }
  return `Chưa lưu được phiên đang học: ${error?.message || 'Lỗi lưu trữ chưa xác định'}`;
}
