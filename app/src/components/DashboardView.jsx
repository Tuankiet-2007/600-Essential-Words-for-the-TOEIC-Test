/**
 * DashboardView — Bảng Điều Khiển Tối Giản Phong Cách Duolingo.
 *
 * Tinh gọn, ít chữ, tập trung vào:
 *   1. Ô duy nhất: "ĐẾN HẠN CẦN ÔN" (bấm vào nhảy sang tab/view Ôn bài riêng).
 *   2. Biểu đồ 1: Trí nhớ SM-2 (Donut + Biểu đồ cột có màu theo trạng thái).
 *   3. Biểu đồ 2: Tiến độ 10 Chủ đề (Minimal Cards).
 *   4. Biểu đồ 3: Điểm luyện đề (Biểu đồ cột điểm % các lần làm đề).
 */
import { useEffect, useMemo, useState } from 'react';
import {
  Award,
  Brain,
  CheckCircle2,
  Clock,
  Flame,
  Layers,
  Play,
  Sparkles,
  Target,
  Trash2,
  TrendingUp,
} from 'lucide-react';
import { THEMES, TOTAL_WORDS, lessonTitle } from '../data/curriculum.js';
import { isDue } from '../lib/srs.js';
import { clearHistory, deleteHistoryItem, loadHistory } from '../lib/storage.js';
import { useApp } from '../lib/store.jsx';
import { Button, Card, ProgressBar, useToast } from './ui.jsx';

function countLessonLearned(progress, srs, lessonId) {
  const lKey = `L${String(lessonId).padStart(2, '0')}`;
  const wordsMap = progress?.[lKey]?.words || {};
  const learnedWords = new Set();

  for (const [k, val] of Object.entries(wordsMap)) {
    if (val) {
      const clean = String(k).includes(':') ? String(k).split(':').slice(1).join(':') : String(k);
      learnedWords.add(clean.toLowerCase());
    }
  }

  const prefix = `${lKey}:`;
  for (const [k, card] of Object.entries(srs || {})) {
    if (k.startsWith(prefix) && card && (card.reps > 0 || card.lastGrade > 0)) {
      learnedWords.add(k.slice(prefix.length).toLowerCase());
    }
  }

  return Math.min(12, learnedWords.size);
}

function formatDateShort(iso) {
  if (!iso) return '—';
  try {
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return '—';
    return d.toLocaleDateString('vi-VN', {
      day: '2-digit',
      month: '2-digit',
    });
  } catch {
    return '—';
  }
}

/* Donut SVG nhỏ gọn */
function SrsDonut({ scheduled, total }) {
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const ratio = total > 0 ? scheduled / total : 0;
  const strokeDash = ratio * circumference;

  return (
    <div className="relative flex items-center justify-center">
      <svg viewBox="0 0 140 140" className="h-32 w-32 -rotate-90 transform">
        <circle
          cx="70"
          cy="70"
          r={radius}
          fill="transparent"
          stroke="#e5e5e5"
          strokeWidth="16"
        />
        <circle
          cx="70"
          cy="70"
          r={radius}
          fill="transparent"
          stroke="#58cc02"
          strokeWidth="16"
          strokeDasharray={`${strokeDash} ${circumference}`}
          strokeLinecap="round"
        />
      </svg>
      <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center text-center">
        <span className="text-2xl font-black text-[var(--color-duo-ink)]">
          {scheduled}
        </span>
        <span className="text-[10px] font-black uppercase text-[var(--color-duo-gray)]">
          / {total}
        </span>
      </div>
    </div>
  );
}

export default function DashboardView() {
  const { progress, srs, openLesson, openSrsReview, setReviewThemeId, setActiveView } = useApp();
  const { show, node } = useToast();
  const [history, setHistory] = useState(() => loadHistory());

  useEffect(() => {
    setHistory(loadHistory());
  }, [progress, srs]);

  const metrics = useMemo(() => {
    const now = new Date();
    const srsEntries = Object.entries(srs || {});
    const scheduledCount = srsEntries.length;

    let dueCount = 0;
    let criticalCount = 0;
    let youngCount = 0;
    let masteredCount = 0;

    for (const [, card] of srsEntries) {
      if (!card) continue;
      const due = isDue(card, now);
      if (due) dueCount += 1;

      const interval = Number(card.interval || 0);
      const lastGrade = Number(card.lastGrade || 0);

      if (lastGrade === 1 || interval <= 1) {
        criticalCount += 1;
      } else if (interval >= 7) {
        masteredCount += 1;
      } else {
        youngCount += 1;
      }
    }

    const unseenCount = Math.max(0, TOTAL_WORDS - scheduledCount);

    const themeBreakdown = THEMES.map((theme) => {
      const learned = theme.lessons.reduce(
        (sum, lid) => sum + countLessonLearned(progress, srs, lid),
        0,
      );
      return {
        ...theme,
        learned,
        maxWords: theme.lessons.length * 12,
      };
    });

    return {
      scheduledCount,
      dueCount,
      criticalCount,
      youngCount,
      masteredCount,
      unseenCount,
      themeBreakdown,
    };
  }, [progress, srs]);

  const handleDeleteHistory = (idOrAt) => {
    const next = deleteHistoryItem(idOrAt);
    setHistory(next);
    show('Đã xoá lượt làm đề.', 'brand');
  };

  const handleClearAll = () => {
    const next = clearHistory();
    setHistory(next);
    show('Đã xoá lịch sử.', 'rose');
  };

  // Tìm giá trị max để scale biểu đồ cột trạng thái
  const maxBarVal = Math.max(
    1,
    metrics.masteredCount,
    metrics.youngCount,
    metrics.criticalCount,
    metrics.unseenCount,
  );

  return (
    <div className="space-y-5">
      {node}

      {/* 1. KHUNG DUY NHẤT: ĐẾN HẠN CẦN ÔN (Call To Action Lớn) */}
      <button
        type="button"
        onClick={() => openSrsReview({ filter: metrics.dueCount > 0 ? 'due' : 'all' })}
        className="group relative flex w-full items-center justify-between overflow-hidden rounded-2xl border-2 border-[var(--color-duo-line)] bg-white p-5 text-left transition-all hover:border-[var(--color-duo-blue)] active:scale-[0.99] duo-card"
      >
        <div className="flex items-center gap-4">
          <div
            className={`flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl text-white shadow-[0_4px_0_0_rgba(0,0,0,0.15)] ${
              metrics.dueCount > 0
                ? 'bg-[var(--color-duo-yellow)] text-slate-900'
                : 'bg-[var(--color-duo-green)] text-white'
            }`}
          >
            {metrics.dueCount > 0 ? (
              <Clock className="h-7 w-7" />
            ) : (
              <CheckCircle2 className="h-7 w-7" />
            )}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-black uppercase tracking-wider text-[var(--color-duo-gray)]">
                Đến Hạn Cần Ôn
              </span>
              {metrics.dueCount > 0 ? (
                <span className="rounded-full bg-amber-100 px-2 py-0.5 text-[10px] font-black text-amber-800">
                  Cần làm
                </span>
              ) : (
                <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-black text-emerald-800">
                  Hoàn thành
                </span>
              )}
            </div>
            <div className="mt-1 flex items-baseline gap-2">
              <span className="text-3xl font-black text-[var(--color-duo-ink)]">
                {metrics.dueCount}
              </span>
              <span className="text-sm font-bold text-[var(--color-duo-gray)]">
                {metrics.dueCount > 0
                  ? 'từ vựng cần ôn hôm nay'
                  : 'từ đến hạn · Đã hoàn thành mục tiêu!'}
              </span>
            </div>
          </div>
        </div>

        <div className="hidden sm:block">
          <span
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2.5 text-xs font-black uppercase tracking-wider text-white shadow-[0_3px_0_0_rgba(0,0,0,0.2)] transition-transform group-hover:scale-105 ${
              metrics.dueCount > 0
                ? 'bg-[var(--color-duo-green)] shadow-[0_3px_0_0_var(--color-duo-green-dark)]'
                : 'bg-[var(--color-duo-blue)] shadow-[0_3px_0_0_var(--color-duo-blue-dark)]'
            }`}
          >
            <Brain className="h-4 w-4" />
            {metrics.dueCount > 0 ? 'Ôn Tập Ngay →' : 'Luyện Thêm →'}
          </span>
        </div>
      </button>

      {/* 2. BIỂU ĐỒ 1: TRÍ NHỚ SM-2 (DONUT + BIỂU ĐỒ CỘT CÓ MÀU) */}
      <Card className="p-4 sm:p-5">
        <div className="mb-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Target className="h-4 w-4 text-[var(--color-duo-green-dark)]" />
            <h3 className="text-sm font-black uppercase tracking-wider text-[var(--color-duo-ink)]">
              Trí nhớ SM-2
            </h3>
          </div>
          <span className="text-xs font-bold text-[var(--color-duo-muted)]">
            {metrics.scheduledCount}/{TOTAL_WORDS} từ
          </span>
        </div>

        <div className="grid items-center gap-6 md:grid-cols-12">
          {/* Donut bên trái */}
          <div className="flex justify-center md:col-span-4">
            <SrsDonut scheduled={metrics.scheduledCount} total={TOTAL_WORDS} />
          </div>

          {/* Biểu đồ cột có màu theo trạng thái bên phải */}
          <div className="md:col-span-8">
            <div className="grid grid-cols-4 gap-2 pt-2">
              {/* Cột 1: Thuộc lòng */}
              <div className="flex flex-col items-center gap-1.5">
                <span className="text-xs font-black text-emerald-600">
                  {metrics.masteredCount}
                </span>
                <div className="flex h-24 w-full items-end justify-center rounded-xl bg-[var(--color-duo-bg-soft)] p-1">
                  <div
                    className="w-full rounded-lg bg-[var(--color-duo-green)] transition-all"
                    style={{
                      height: `${Math.max(12, (metrics.masteredCount / maxBarVal) * 100)}%`,
                    }}
                  />
                </div>
                <span className="text-center text-[11px] font-extrabold text-[var(--color-duo-ink)]">
                  Thuộc lòng
                </span>
              </div>

              {/* Cột 2: Đang nhớ */}
              <div className="flex flex-col items-center gap-1.5">
                <span className="text-xs font-black text-sky-600">{metrics.youngCount}</span>
                <div className="flex h-24 w-full items-end justify-center rounded-xl bg-[var(--color-duo-bg-soft)] p-1">
                  <div
                    className="w-full rounded-lg bg-[var(--color-duo-blue)] transition-all"
                    style={{
                      height: `${Math.max(12, (metrics.youngCount / maxBarVal) * 100)}%`,
                    }}
                  />
                </div>
                <span className="text-center text-[11px] font-extrabold text-[var(--color-duo-ink)]">
                  Đang nhớ
                </span>
              </div>

              {/* Cột 3: Cần ôn */}
              <div className="flex flex-col items-center gap-1.5">
                <span className="text-xs font-black text-amber-600">
                  {metrics.criticalCount}
                </span>
                <div className="flex h-24 w-full items-end justify-center rounded-xl bg-[var(--color-duo-bg-soft)] p-1">
                  <div
                    className="w-full rounded-lg bg-[var(--color-duo-yellow)] transition-all"
                    style={{
                      height: `${Math.max(12, (metrics.criticalCount / maxBarVal) * 100)}%`,
                    }}
                  />
                </div>
                <span className="text-center text-[11px] font-extrabold text-[var(--color-duo-ink)]">
                  Cần ôn
                </span>
              </div>

              {/* Cột 4: Chưa học */}
              <div className="flex flex-col items-center gap-1.5">
                <span className="text-xs font-black text-slate-400">
                  {metrics.unseenCount}
                </span>
                <div className="flex h-24 w-full items-end justify-center rounded-xl bg-[var(--color-duo-bg-soft)] p-1">
                  <div
                    className="w-full rounded-lg bg-slate-300 transition-all"
                    style={{
                      height: `${Math.max(12, (metrics.unseenCount / maxBarVal) * 100)}%`,
                    }}
                  />
                </div>
                <span className="text-center text-[11px] font-extrabold text-[var(--color-duo-muted)]">
                  Chưa học
                </span>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* 3. BIỂU ĐỒ 2: TIẾN ĐỘ 10 CHỦ ĐỀ (MINIMAL CARDS) */}
      <Card className="p-4 sm:p-5">
        <div className="mb-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Layers className="h-4 w-4 text-[var(--color-duo-purple)]" />
            <h3 className="text-sm font-black uppercase tracking-wider text-[var(--color-duo-ink)]">
              Tiến độ 10 Chủ đề
            </h3>
          </div>
        </div>

        <div className="grid gap-2.5 sm:grid-cols-2">
          {metrics.themeBreakdown.map((t) => {
            const pct = Math.round((t.learned / t.maxWords) * 100);
            return (
              <div
                key={t.theme_id}
                className="flex items-center justify-between gap-3 rounded-xl border-2 border-[var(--color-duo-line)] bg-white p-3 transition-colors hover:border-slate-300"
              >
                <div className="min-w-0 flex-1">
                  <div className="flex items-center justify-between gap-2">
                    <span className="truncate text-xs font-black text-slate-800">
                      {String(t.theme_id).padStart(2, '0')} · {t.theme_name}
                    </span>
                    <span className="text-[11px] font-bold tabular-nums text-[var(--color-duo-gray)]">
                      {t.learned}/{t.maxWords}
                    </span>
                  </div>
                  <div className="mt-1.5">
                    <ProgressBar
                      value={t.learned}
                      max={t.maxWords}
                      tone={pct >= 80 ? 'emerald' : 'brand'}
                    />
                  </div>
                </div>

                <div className="flex shrink-0 items-center gap-1">
                  <button
                    type="button"
                    onClick={() => openLesson?.(t.lessons[0], 'vocab')}
                    className="rounded-lg bg-[var(--color-duo-bg-soft)] px-2 py-1 text-[11px] font-extrabold text-[var(--color-duo-ink)] hover:bg-slate-200"
                  >
                    Học
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setActiveView?.('lesson');
                      setReviewThemeId?.(t.review_id);
                    }}
                    className="rounded-lg bg-purple-50 px-2 py-1 text-[11px] font-extrabold text-[var(--color-duo-purple-dark)] hover:bg-purple-100"
                    title={`Word Review ${t.review_id}`}
                  >
                    Ôn
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </Card>

      {/* 4. BIỂU ĐỒ 3: ĐIỂM LUYỆN ĐỀ (BIỂU ĐỒ CỘT) */}
      <Card className="p-4 sm:p-5">
        <div className="mb-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-[var(--color-duo-blue)]" />
            <h3 className="text-sm font-black uppercase tracking-wider text-[var(--color-duo-ink)]">
              Điểm luyện đề
            </h3>
          </div>
          {history.length > 0 ? (
            <button
              type="button"
              onClick={handleClearAll}
              className="text-[11px] font-bold text-rose-500 hover:underline"
            >
              Xoá lịch sử
            </button>
          ) : null}
        </div>

        {history.length === 0 ? (
          <div className="rounded-xl border-2 border-dashed border-[var(--color-duo-line)] p-4 text-center">
            <p className="text-xs font-bold text-[var(--color-duo-muted)]">
              Chưa có lượt nộp bài
            </p>
            <Button
              size="sm"
              variant="secondary"
              className="mt-2 text-xs"
              onClick={() => openLesson?.(1, 'practice')}
            >
              <Play className="h-3 w-3" />
              Làm đề ngay
            </Button>
          </div>
        ) : (
          <div className="space-y-3">
            {/* Biểu đồ cột */}
            <div className="flex h-32 items-end gap-2 overflow-x-auto rounded-xl bg-[var(--color-duo-bg-soft)] p-3">
              {history
                .slice(0, 10)
                .slice()
                .reverse()
                .map((item, idx) => {
                  const total = Math.max(1, Number(item.total || 1));
                  const correct = Number(item.correct || 0);
                  const pct = Math.round((correct / total) * 100);
                  const color =
                    pct >= 80
                      ? 'bg-[var(--color-duo-green)]'
                      : pct >= 50
                        ? 'bg-[var(--color-duo-yellow)]'
                        : 'bg-[var(--color-duo-red)]';

                  return (
                    <div
                      key={item.id || item.at || idx}
                      className="flex min-w-[2.5rem] flex-1 flex-col items-center gap-1"
                    >
                      <span className="text-[10px] font-black text-slate-700">{pct}%</span>
                      <div className="flex h-20 w-full items-end justify-center rounded-md bg-white/70 p-0.5">
                        <div
                          className={`w-full rounded-sm transition-all ${color}`}
                          style={{ height: `${Math.max(12, pct)}%` }}
                        />
                      </div>
                      <span className="text-[9px] font-black text-[var(--color-duo-gray)]">
                        L{String(item.lessonId || 1).padStart(2, '0')}
                      </span>
                    </div>
                  );
                })}
            </div>

            {/* Danh sách rút gọn */}
            <div className="grid gap-1.5 sm:grid-cols-2">
              {history.slice(0, 4).map((item, idx) => {
                const total = Math.max(1, Number(item.total || 1));
                const correct = Number(item.correct || 0);
                const pct = Math.round((correct / total) * 100);
                const lid = Number(item.lessonId || 1);

                return (
                  <div
                    key={item.id || item.at || idx}
                    className="flex items-center justify-between rounded-lg border border-[var(--color-duo-line)] bg-white px-2.5 py-1.5"
                  >
                    <div className="flex items-center gap-2">
                      <span
                        className={`rounded px-1.5 py-0.5 text-[10px] font-black ${
                          pct >= 80
                            ? 'bg-emerald-100 text-emerald-800'
                            : pct >= 50
                              ? 'bg-amber-100 text-amber-800'
                              : 'bg-rose-100 text-rose-800'
                        }`}
                      >
                        {pct}%
                      </span>
                      <span className="text-xs font-bold text-slate-800">
                        Bài {String(lid).padStart(2, '0')}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] text-slate-400">
                        {formatDateShort(item.at)}
                      </span>
                      <button
                        type="button"
                        onClick={() => handleDeleteHistory(item.id || item.at)}
                        className="text-slate-300 hover:text-rose-500"
                        title="Xoá"
                      >
                        <Trash2 className="h-3 w-3" />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
