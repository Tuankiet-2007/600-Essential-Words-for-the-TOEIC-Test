/**
 * Shared UI primitives. Owned by the Lead (lead) — do not edit in tab tasks.
 * Other files import from here rather than restyling buttons inline.
 */
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { highlightWord } from '../lib/assets.js';

/* ---------------- Button ---------------- */

/*
 * Nút kiểu Duolingo: khối 3D có bóng cứng bên dưới, bấm thì dịch xuống.
 * Hiệu ứng nằm trong .duo-btn (index.css) để SSR render ra class ổn định.
 */
const BTN_BASE = 'duo-btn focus:outline-none disabled:cursor-not-allowed';

const BTN_VARIANTS = {
  primary: 'duo-btn-green',
  secondary: 'duo-btn-ghost',
  ghost: 'duo-btn-ghost',
  success: 'duo-btn-green',
  danger: 'duo-btn-red',
  amber: 'duo-btn-yellow',
  blue: 'duo-btn-blue',
  purple: 'duo-btn-purple',
};

const BTN_SIZES = {
  sm: 'duo-btn-sm',
  md: '',
  lg: 'duo-btn-lg',
  // Nút icon tròn: giữ bóng cứng nhưng không ép chữ IN HOA / padding ngang.
  icon: '!px-0 !py-0 h-10 w-10 !rounded-full',
};

export function Button({
  variant = 'secondary',
  size = 'md',
  className = '',
  as: Tag = 'button',
  ...rest
}) {
  return (
    <Tag
      className={`${BTN_BASE} ${BTN_VARIANTS[variant] || BTN_VARIANTS.secondary} ${BTN_SIZES[size] || BTN_SIZES.md} ${className}`}
      {...rest}
    />
  );
}

/* ---------------- Card ---------------- */

export function Card({ className = '', flat = false, children, ...rest }) {
  return (
    <div className={`duo-card ${flat ? 'duo-card-flat' : ''} ${className}`} {...rest}>
      {children}
    </div>
  );
}

/* ---------------- Badge ---------------- */

const BADGE_TONES = {
  slate: 'duo-badge',
  brand: 'duo-badge-blue',
  emerald: 'duo-badge-green',
  amber: 'duo-badge-yellow',
  rose: 'duo-badge-red',
  sky: 'duo-badge-blue',
  violet: 'duo-badge-purple',
};

export function Badge({ tone = 'slate', className = '', children }) {
  return (
    <span className={`duo-badge ${BADGE_TONES[tone] || BADGE_TONES.slate} ${className}`}>
      {children}
    </span>
  );
}

/* ---------------- Highlighted text ---------------- */

/**
 * Render `text`, wrapping every occurrence of any word in `words` in <mark>.
 * Context-First rule: this is the ONLY way target vocabulary is displayed
 * inside sentences/passages.
 */
export function Highlighted({ text, words, className = '' }) {
  const segments = useMemo(() => highlightWord(text, words), [text, words]);
  return (
    <span className={className}>
      {segments.map((seg, i) =>
        seg.hit ? (
          <mark
            key={i}
            className="vocab-hit dark:!text-yellow-300 dark:!bg-yellow-400/20 dark:border-b-2 dark:border-yellow-400 font-bold px-1 rounded-xs"
          >
            {seg.text}
          </mark>
        ) : (
          <span key={i}>{seg.text}</span>
        ),
      )}
    </span>
  );
}

/* ---------------- Section heading ---------------- */

export function SectionTitle({ icon: Icon, title, subtitle, right }) {
  return (
    <div className="mb-3 flex items-end justify-between gap-3">
      <div className="flex items-center gap-2.5">
        {Icon ? (
          <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[var(--color-duo-green-light)] text-[var(--color-duo-green-dark)]">
            <Icon className="h-5 w-5" />
          </span>
        ) : null}
        <div>
          <h3 className="text-base font-extrabold tracking-tight text-[var(--color-duo-ink)]">
            {title}
          </h3>
          {subtitle ? <p className="text-xs font-medium text-[var(--color-duo-gray)]">{subtitle}</p> : null}
        </div>
      </div>
      {right}
    </div>
  );
}

/* ---------------- Spinner / states ---------------- */

export function Spinner({ label = 'Đang tải…' }) {
  return (
    <div className="flex items-center justify-center gap-3 py-16 text-slate-500">
      <span className="h-5 w-5 animate-spin rounded-full border-2 border-slate-300 border-t-brand-600" />
      <span className="text-sm">{label}</span>
    </div>
  );
}

export function EmptyState({ icon: Icon, title, description, action }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 rounded-2xl border-2 border-dashed border-[var(--color-duo-line-strong)] bg-white px-6 py-16 text-center">
      {Icon ? <Icon className="h-10 w-10 text-[var(--color-duo-muted)]" /> : null}
      <h3 className="text-base font-extrabold text-[var(--color-duo-ink)]">{title}</h3>
      {description ? (
        <p className="max-w-md text-sm font-medium text-[var(--color-duo-gray)]">{description}</p>
      ) : null}
      {action}
    </div>
  );
}

/* ---------------- Progress bar ---------------- */

export function ProgressBar({ value = 0, max = 100, tone = 'brand', className = '', showTrack = true }) {
  const pct = max > 0 ? Math.min(100, Math.max(0, Math.round((value / max) * 100))) : 0;
  const tones = {
    brand: '',
    emerald: '',
    amber: 'duo-progress-fill-yellow',
    blue: 'duo-progress-fill-blue',
    red: 'duo-progress-fill-red',
  };
  return (
    <div className={`duo-progress ${showTrack ? '' : '!bg-transparent !h-2'} ${className}`}>
      <div
        className={`duo-progress-fill ${tones[tone] || ''}`}
        style={{ width: `${pct}%` }}
      />
    </div>
  );
}

/* ---------------- Tabs ---------------- */

export function TabBar({ tabs, active, onChange }) {
  return (
    <div className="flex gap-2 overflow-x-auto border-b-2 border-[var(--color-duo-line)] bg-[var(--color-duo-bg)] px-3 py-2">
      {tabs.map((t) => {
        const isActive = t.id === active;
        return (
          <button
            key={t.id}
            type="button"
            onClick={() => onChange(t.id)}
            aria-selected={isActive}
            role="tab"
            className={`inline-flex shrink-0 items-center gap-2 rounded-xl border-2 px-3.5 py-2 text-[13px] font-extrabold uppercase tracking-wide transition-colors ${
              isActive
                ? 'border-[var(--color-duo-blue)] bg-[var(--color-duo-blue-light)] text-[#0b6ea8]'
                : 'border-transparent text-[var(--color-duo-gray)] hover:bg-[var(--color-duo-bg-soft)] hover:text-[var(--color-duo-ink)]'
            }`}
          >
            {t.icon ? <t.icon className="h-4 w-4" /> : null}
            {t.label}
          </button>
        );
      })}
    </div>
  );
}

/* ---------------- Speech (US English) ---------------- */

/**
 * Web Speech API pronunciation with a preference for en-US voices.
 * @returns {{speak:(text:string,opts?:{rate?:number})=>void, supported:boolean, speaking:boolean}}
 */
export function useSpeech() {
  const supported = typeof window !== 'undefined' && 'speechSynthesis' in window;
  const [speaking, setSpeaking] = useState(false);

  const speak = useCallback(
    (text, opts = {}) => {
      if (!supported || !text) return;
      const synth = window.speechSynthesis;
      try {
        synth.cancel();
        const u = new SpeechSynthesisUtterance(String(text));
        const voices = synth.getVoices();
        const us =
          voices.find((v) => v.lang === 'en-US' && /google|samantha|aria|jenny/i.test(v.name)) ||
          voices.find((v) => v.lang === 'en-US') ||
          voices.find((v) => v.lang?.startsWith('en'));
        if (us) u.voice = us;
        u.lang = us?.lang || 'en-US';
        u.rate = opts.rate ?? 0.95;
        u.onend = () => setSpeaking(false);
        u.onerror = () => setSpeaking(false);
        setSpeaking(true);
        synth.speak(u);
      } catch {
        setSpeaking(false);
      }
    },
    [supported],
  );

  useEffect(() => {
    return () => {
      if (supported) window.speechSynthesis.cancel();
    };
  }, [supported]);

  return { speak, supported, speaking };
}

/* ---------------- Toast ---------------- */

export function useToast() {
  const [toast, setToast] = useState(null);
  const timer = useRef(null);
  const show = useCallback((message, tone = 'brand') => {
    setToast({ message, tone });
    if (timer.current) clearTimeout(timer.current);
    timer.current = setTimeout(() => setToast(null), 2600);
  }, []);
  useEffect(() => () => timer.current && clearTimeout(timer.current), []);
  const node = toast ? (
    <div className="pointer-events-none fixed bottom-6 left-1/2 z-50 -translate-x-1/2">
      <div
        className={`rounded-lg px-4 py-2.5 text-sm font-medium text-white shadow-lg ${
          toast.tone === 'rose' ? 'bg-rose-600' : toast.tone === 'emerald' ? 'bg-emerald-600' : 'bg-slate-900'
        }`}
      >
        {toast.message}
      </div>
    </div>
  ) : null;
  return { show, node };
}

export default {};
