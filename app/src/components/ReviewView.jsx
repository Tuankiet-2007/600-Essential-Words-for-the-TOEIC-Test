/**
 * Word Review — trang on tap gop theo CHU DE (10 chu de x 5 bai = 60 tu).
 * Owned by the Lead.
 *
 * Nguyen tac Context-First van duoc giu: moi tu luon di kem it nhat MOT cau vi
 * du trong sach (lay tu bai goc), khong bao gio hien tu don le. Moi nhom tu ghi
 * ro xuat xu (bai nao), va nut "Mo bai" dua nguoi hoc ve dung bai do de hoc
 * sau hon voi SRS/flashcard/AI Lab.
 *
 * Du lieu doc truc tiep tu lessons_json qua loadLesson() (da memoized), nen
 * khong can them fetch moi.
 */
import { useEffect, useMemo, useState } from 'react';
import {
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  Circle,
  Layers,
  Volume2,
} from 'lucide-react';
import { Badge, Button, Card, Highlighted, ProgressBar, SectionTitle, useSpeech } from './ui.jsx';
import { THEMES, lessonTitle } from '../data/curriculum.js';
import { loadLesson } from '../lib/lessonLoader.js';
import { markWordLearned } from '../lib/storage.js';
import { useApp } from '../lib/store.jsx';

function progressKey(lessonId) {
  return `L${String(Number(lessonId)).padStart(2, '0')}`;
}

function isLearned(progress, lessonId, word) {
  return Boolean(progress?.[progressKey(lessonId)]?.words?.[word]);
}

export default function ReviewView({ themeId }) {
  const theme = THEMES.find((t) => t.review_id === Number(themeId)) || null;
  const { progress, setProgress, setLessonId, setTab, setReviewThemeId } = useApp();
  const { speak, supported: speechSupported } = useSpeech();
  const [lessons, setLessons] = useState(null); // null = dang tai

  useEffect(() => {
    let cancelled = false;
    setLessons(null);
    (async () => {
      const results = await Promise.all(
        (theme?.lessons || []).map(async (id) => {
          const r = await loadLesson(id);
          return r.status === 'loaded' ? r.lesson : null;
        }),
      );
      if (!cancelled) setLessons(results);
    })();
    return () => {
      cancelled = true;
    };
  }, [theme]);

  const stats = useMemo(() => {
    const loaded = (lessons || []).filter(Boolean);
    const words = loaded.flatMap((l) =>
      (l.words_to_learn || []).map((w) => ({ ...w, lessonId: l.lesson_id })),
    );
    const learned = words.filter((w) => isLearned(progress, w.lessonId, w.word)).length;
    return { total: words.length, learned, loadedCount: loaded.length };
  }, [lessons, progress]);

  const toggle = (lessonId, word, next) => {
    const map = markWordLearned(lessonId, word, next);
    setProgress({ ...map });
  };

  const openLesson = (id) => {
    setReviewThemeId(null);
    setLessonId(id);
    setTab('vocab');
  };

  if (!theme) {
    return (
      <Card className="p-6 text-center text-sm text-slate-500">
        Không tìm thấy Word Review #{themeId}.
        <Button variant="secondary" className="ml-3" onClick={() => setReviewThemeId(null)}>
          <ArrowLeft className="h-4 w-4" /> Về bài học
        </Button>
      </Card>
    );
  }

  return (
    <div>
      {/* ---- header ---- */}
      <Card className="mb-4 flex flex-wrap items-center justify-between gap-3 px-4 py-3">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <Badge tone="violet">Word Review {theme.review_id}</Badge>
            <Badge tone="slate">{theme.theme_name}</Badge>
            <Badge tone="emerald">{stats.loadedCount}/5 bài đã trích xuất</Badge>
          </div>
          <h2 className="mt-1.5 text-xl font-bold text-slate-900">
            Ôn tập {stats.total} từ của chủ đề “{theme.theme_name}”
          </h2>
          <p className="text-xs text-slate-500">
            Gộp từ của bài {theme.lessons.join(', ')} · mỗi từ giữ nguyên câu ví dụ trong sách
          </p>
        </div>
        <Button variant="secondary" onClick={() => setReviewThemeId(null)}>
          <ArrowLeft className="h-4 w-4" /> Về bài học
        </Button>
      </Card>

      {/* ---- progress ---- */}
      <Card className="mb-4 px-4 py-3">
        <div className="mb-2 flex items-center justify-between text-xs text-slate-600">
          <span className="inline-flex items-center gap-1.5 font-medium">
            <Layers className="h-3.5 w-3.5 text-violet-500" />
            Tiến độ thuộc bài của chủ đề này
          </span>
          <span className="font-mono">
            {stats.learned}/{stats.total || 60} từ
          </span>
        </div>
        <ProgressBar
          value={stats.learned}
          max={stats.total || 60}
          tone={stats.total && stats.learned >= stats.total ? 'emerald' : 'brand'}
        />
      </Card>

      {/* ---- words grouped by lesson ---- */}
      {lessons === null ? (
        <Card className="p-6 text-center text-sm text-slate-500">Đang tải dữ liệu 5 bài…</Card>
      ) : (
        (lessons || [])
          .map((lesson, idx) => ({ lesson, plannedId: theme.lessons[idx] }))
          .map(({ lesson, plannedId }) =>
            lesson ? (
              <section key={lesson.lesson_id} className="mb-6">
                <SectionTitle
                  icon={BookOpen}
                  title={`Lesson ${String(lesson.lesson_id).padStart(2, '0')} — ${lessonTitle(lesson.lesson_id)}`}
                  subtitle={`${lesson.words_to_learn.length} từ mục tiêu`}
                  right={
                    <Button size="sm" variant="secondary" onClick={() => openLesson(lesson.lesson_id)}>
                      Mở bài →
                    </Button>
                  }
                />
                <div className="grid gap-2">
                  {(lesson.words_to_learn || []).map((entry, i) => {
                    const learned = isLearned(progress, lesson.lesson_id, entry.word);
                    const example = (entry.examples || [])[0]?.en || '';
                    return (
                      <Card key={`${lesson.lesson_id}-${entry.word}`} className="px-4 py-3">
                        <div className="flex items-start gap-3">
                          <button
                            type="button"
                            onClick={() => toggle(lesson.lesson_id, entry.word, !learned)}
                            title={learned ? 'Bỏ đánh dấu đã thuộc' : 'Đánh dấu đã thuộc'}
                            aria-pressed={learned}
                            className="mt-0.5 shrink-0"
                          >
                            {learned ? (
                              <CheckCircle2 className="h-5 w-5 text-emerald-500" />
                            ) : (
                              <Circle className="h-5 w-5 text-slate-300 hover:text-slate-400" />
                            )}
                          </button>

                          <div className="min-w-0 flex-1">
                            <div className="flex flex-wrap items-baseline gap-2">
                              <span className="text-[11px] font-bold text-slate-400">
                                {i + 1}.
                              </span>
                              <h4 className="text-[15px] font-extrabold text-slate-900">
                                {entry.word}
                              </h4>
                              {entry.pos ? <Badge tone="violet">{entry.pos}</Badge> : null}
                              {entry.definition_en ? (
                                <span className="text-[12.5px] text-slate-600">
                                  {entry.definition_en}
                                </span>
                              ) : null}
                            </div>
                            {example ? (
                              <p className="mt-1 text-[13px] leading-relaxed text-slate-700">
                                “<Highlighted text={example} words={[entry.word]} />”
                              </p>
                            ) : (
                              <p className="mt-1 text-[12px] italic text-slate-400">
                                Bài này OCR đọc sót câu ví dụ của từ — mở bài để xem phần còn lại.
                              </p>
                            )}
                          </div>

                          <Button
                            size="icon"
                            variant={speechSupported ? 'ghost' : 'ghost'}
                            disabled={!speechSupported}
                            onClick={() => speak(entry.word)}
                            aria-label={`Phát âm ${entry.word}`}
                            title={
                              speechSupported
                                ? `Nghe phát âm: ${entry.word}`
                                : 'Trình duyệt không hỗ trợ đọc tiếng Anh'
                            }
                            className="shrink-0"
                          >
                            <Volume2 className="h-4 w-4 text-brand-600" />
                          </Button>
                        </div>
                      </Card>
                    );
                  })}
                </div>
              </section>
            ) : (
              <section key={`missing-${plannedId}`} className="mb-6">
                <SectionTitle
                  icon={BookOpen}
                  title={`Lesson ${String(plannedId).padStart(2, '0')} — ${lessonTitle(plannedId)}`}
                  subtitle="Chưa trích xuất"
                />
                <Card className="px-4 py-3 text-sm text-slate-500">
                  Bài này chưa có dữ liệu OCR nên không có mặt trong phần ôn tập.
                </Card>
              </section>
            ),
          )
      )}
    </div>
  );
}
