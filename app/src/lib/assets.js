/**
 * FROZEN CONTRACT — asset path resolution + target-word highlighting.
 *
 * REFERENCE-COUNT: highlightWord() is imported by Tab1, Tab2, Tab3 and Tab5.
 * Every lesson entry in book_structure_map.json declares assets like
 *   audio_track: "audio/track_01.mp3"
 *   part1_photo: "part1_photos/lesson_01.jpg"
 * Author-time filenames on disk are inconsistent ("Track 1.wma", "Track 26.mp3"),
 * so scripts/normalize_assets.py copies/symlinks everything into
 *   public/audio/track_XX.mp3        (canonical, always exists)
 *   public/part1_photos/lesson_XX.jpg
 * The resolver therefore rewrites whatever the JSON says to the canonical public URL.
 */

const BASE = import.meta.env.BASE_URL || './';
const cleanBase = BASE.endsWith('/') ? BASE : BASE + '/';

/** Canonical Vite public-dir URLs. */
export function audioUrlFor(lessonId) {
  return `${cleanBase}audio/track_${pad2(lessonId)}.mp3`;
}

export function photoUrlFor(lessonId) {
  return `${cleanBase}part1_photos/lesson_${pad2(lessonId)}.jpg`;
}

function pad2(n) {
  return String(Number(n)).padStart(2, '0');
}

/**
 * Resolve an arbitrary asset reference from lesson JSON / structure map into a
 * real, browser-loadable URL.
 * @param {string} ref e.g. "audio/track_01.mp3" or "part1_photos/lesson_01.jpg"
 * @param {'audio'|'photo'} kind
 * @param {number} lessonId
 */
export function resolveAsset(ref, kind, lessonId) {
  if (kind === 'audio') return audioUrlFor(lessonId);
  if (kind === 'photo') return photoUrlFor(lessonId);
  // Fallback: strip any leading ./ or / and serve from public root.
  return `${cleanBase}` + String(ref || '').replace(/^\.?[\\/]/, '');
}

/* ------------------------------------------------------------------ */
/* Target-word highlighting                                            */
/* ------------------------------------------------------------------ */

const ESCAPE_RE = /[.*+?^${}()|[\]\\]/g;

function escapeRegex(s) {
  return s.replace(ESCAPE_RE, '\\$&');
}

const VOWELS = 'aeiou';

/**
 * Generate the surface forms an English headword can take in the book's
 * sentences. Deliberately over-generates a little (a missed highlight is a
 * product bug; a rare extra form is harmless):
 *   obligate -> obligates / obligated / obligating
 *   specify  -> specifies / specified / specifying      (-y -> -ies)
 *   submit   -> submits / submitted / submitting        (consonant doubling)
 *   party    -> parties / partied / partying
 *   abide    -> abides / abided / abiding
 *   assess   -> assesses / assessed / assessing
 *   pass     -> passes / passed / passing
 * @param {string} word single token, no spaces
 * @returns {string[]}
 */
function inflect(word) {
  const out = new Set([word]);
  const lower = word.toLowerCase();
  if (!/^[a-z][a-z'-]*$/.test(lower)) return [...out];

  const last1 = lower.slice(-1);
  const last2 = lower.slice(-2);
  const isVowel = (c) => VOWELS.includes(c);
  const endsConsonantY = /[^aeiou]y$/.test(lower);
  /** CVC ending (submit, cancel, plan) -> the final consonant doubles. */
  const doubles =
    lower.length >= 3 &&
    !isVowel(last1) &&
    last1 !== 'w' &&
    last1 !== 'x' &&
    last1 !== 'y' &&
    isVowel(lower.slice(-2, -1)) &&
    !isVowel(lower.slice(-3, -2));
  const stem = last1 === 'e' ? lower.slice(0, -1) : lower;

  /* --- plural / 3rd person singular --- */
  out.add(`${lower}s`);
  if (last2 === 'ch' || last2 === 'sh' || last2 === 'ss' || last2 === 'zz' || /[sxz]$/.test(last1)) {
    out.add(`${lower}es`);
  }
  if (endsConsonantY) out.add(`${lower.slice(0, -1)}ies`);

  /* --- past tense --- */
  if (last1 === 'e') out.add(`${lower}d`);
  else if (endsConsonantY) out.add(`${lower.slice(0, -1)}ied`);
  else if (doubles) {
    // US and UK differ for final -l: "canceled"/"cancelled". The book is
    // American English but its word-family rows and tapescripts mix both,
    // so emit the doubled form AND the single-consonant variant for -l.
    out.add(`${lower}${last1}ed`);
    if (last1 === 'l') out.add(`${lower}ed`);
  } else out.add(`${lower}ed`);

  /* --- present participle --- */
  if (last2 === 'ee' || last2 === 'oe' || last2 === 'ye') out.add(`${lower}ing`);
  else if (last1 === 'e') out.add(`${stem}ing`);
  else if (doubles) {
    out.add(`${lower}${last1}ing`);
    if (last1 === 'l') out.add(`${lower}ing`);
  } else out.add(`${lower}ing`);

  /* --- comparative / superlative --- */
  if (endsConsonantY) {
    out.add(`${lower.slice(0, -1)}ier`);
    out.add(`${lower.slice(0, -1)}iest`);
  } else if (doubles) {
    out.add(`${lower}${last1}er`);
    out.add(`${lower}${last1}est`);
  }

  /*
   * Common derivational endings. The book's Word Family tables use these
   * ("specific" -> "specification", "provide" -> "provision"), and students
   * meet them in the passage, so they must highlight too.
   */
  const derived = [
    `${stem}ation`, // specify -> specification, cancel -> cancellation (approx)
    `${stem}ion`, // provide -> provision (approx)
    `${stem}ment`, // establish -> establishment, agree -> agreement
    `${stem}ance`,
    `${stem}ence`,
    `${stem}able`,
    `${stem}ible`,
    `${stem}al`,
    `${stem}ly`,
    `${stem}ness`,
    `${stem}er`,
    `${stem}or`,
    `${stem}ist`,
    `${stem}ive`,
    `${stem}ity`,
  ];
  for (const d of derived) {
    if (d.length >= 5) out.add(d);
    // Doubled-consonant variants: cancel -> cancellation, submit -> submission-ish
    if (doubles && `${stem}${last1}`.length >= 2) out.add(`${stem}${last1}${d.slice(stem.length)}`);
  }
  // -ify / -ification family (specific -> specification is already covered above)
  if (lower.endsWith('y')) out.add(`${lower.slice(0, -1)}ication`);

  /*
   * Irregular derivations that the book's Word Family tables actually use.
   * These cannot be produced by suffix rules, and leaving them out means a
   * family word fails to highlight in its own example sentence.
   */
  const IRREGULAR = {
    provide: ['provision', 'provisions', 'provider', 'providers', 'providing'],
    engage: ['engagement', 'engagements', 'engaging'],
    agree: ['agreement', 'agreements', 'agreeable', 'disagree', 'disagreement'],
    apply: ['application', 'applicant', 'applicants'],
    specify: ['specification', 'specifications', 'specific', 'specifically'],
    maintain: ['maintenance'],
    receive: ['receipt', 'receivable', 'receivables'],
    pay: ['payment', 'payments', 'payable', 'payee'],
    employ: ['employee', 'employees', 'employer', 'employment'],
    invest: ['investment', 'investments', 'investor', 'investors'],
    compete: ['competition', 'competitor', 'competitive'],
    negotiate: ['negotiation', 'negotiations', 'negotiator'],
    subscribe: ['subscription', 'subscriber'],
    attend: ['attendance', 'attendee', 'attendant'],
    advertise: ['advertisement', 'advertising'],
    manage: ['management', 'manager', 'managers', 'managerial'],
    account: ['accountant', 'accounting', 'accounts'],
    consult: ['consultant', 'consultants', 'consultation'],
    purchase: ['purchaser', 'purchasing'],
    qualify: ['qualification', 'qualifications', 'qualified'],
    accept: ['acceptance', 'acceptable', 'unacceptable'],
    assist: ['assistance', 'assistant', 'assistants'],
    insure: ['insurance', 'insured', 'insurer'],
    reside: ['residence', 'resident', 'residents', 'residential'],
    differ: ['difference', 'differences', 'different', 'differently'],
    depend: ['dependence', 'dependent', 'independent', 'independence'],
    produce: ['product', 'products', 'production', 'productive', 'productivity'],
    decide: ['decision', 'decisions', 'decisive'],
    divide: ['division', 'divisions'],
    conclude: ['conclusion', 'conclusions'],
    permit: ['permission', 'permissible'],
    admit: ['admission'],
    omit: ['omission'],
    sell: ['sale', 'sales', 'seller'],
    buy: ['purchase', 'buyer', 'buyers'],
    grow: ['growth'],
    choose: ['choice', 'choices'],
    lose: ['loss', 'losses'],
    prove: ['proof'],
    advise: ['advice', 'adviser', 'advisor'],
    analyse: ['analysis', 'analyst'],
    analyze: ['analysis', 'analyst'],
    certify: ['certificate', 'certification', 'certified'],
    identify: ['identification', 'identity'],
    satisfy: ['satisfaction', 'satisfactory', 'satisfied', 'unsatisfactory'],
    apply_for: ['application'],
  };
  for (const v of IRREGULAR[lower] || []) out.add(v);

  return [...out].filter((v) => v.length >= 2);
}

/**
 * Build a regex that matches every target word plus its inflections.
 *
 * Multi-word entries ("abide by") inflect their HEAD (first) token, so
 * "abide by" matches "abided by" — inflecting the final token would wrongly
 * produce "abide bying".
 *
 * Matching is case-insensitive and tolerant of hyphenation, because the book
 * writes derived forms that way: "self-assurance" must count as "assurance".
 *
 * @param {string[]} words
 * @returns {RegExp|null}
 */
export function buildWordRegex(words) {
  const variants = new Set();

  for (const raw of words || []) {
    const w = String(raw || '').trim();
    if (!w) continue;

    const parts = w.split(/\s+/);
    const head = parts[0];
    const tail = parts.slice(1);

    // Inflect the head token, then re-attach the remaining tokens.
    for (const form of inflect(head)) {
      variants.add(tail.length ? [form, ...tail].join(' ') : form);
    }
    // Also allow the head to stay bare with an inflected tail
    // (e.g. "abide by" -> "abide bying" is junk, but "abide by" phrases such
    // as "abide by" + "the conditions" still match via the bare head below).
    variants.add(w);
  }

  const list = [...variants].filter(Boolean).sort((a, b) => b.length - a.length || a.localeCompare(b));
  if (!list.length) return null;

  // NOTE: the 'g' flag makes a RegExp stateful (lastIndex), so a bare
  // `re.test(x)` is unreliable across successive calls. We keep 'g' because
  // the highlight loop needs it, but every internal use resets `lastIndex`
  // first, and callers that only want a yes/no answer should use
  // `containsWord()` instead of `buildWordRegex(...).test()`.
  //
  // Boundary rules:
  //   - Not preceded by a LETTER (so "part" does not match inside "party").
  //   - A preceding hyphen IS allowed, so the word is found inside hyphenated
  //     compounds: "self-assurance" contains "assurance". The hyphen itself is
  //     absorbed later by highlightSegments so the whole compound is marked.
  //   - Not followed by a letter, EXCEPT a hyphen is allowed so that
  //     "well-established" style compounds still match at their tail.
  const body = list.map(escapeRegex).join('|');
  return new RegExp(`(?<!\\p{L})(?:${body})(?!\\p{L})`, 'giu');
}

/**
 * Stateless containment test — the safe way to ask "does this text contain a
 * target word?". Resets `lastIndex` internally, so it is immune to the
 * statefulness of a global regex.
 * @param {string} text
 * @param {string[]} words
 * @returns {boolean}
 */
export function containsWord(text, words) {
  const re = buildWordRegex(words);
  if (!re) return false;
  re.lastIndex = 0;
  return re.test(String(text ?? ''));
}

/**
 * Splitting wrapper used by `highlightWord` that ALSO reports hyphenated
 * compounds: for "Her self-assurance ..." the segment "self-assurance" is
 * returned as a single hit, because the target word sits inside it.
 */
function highlightSegments(text, words) {
  const src = String(text ?? '');
  const re = buildWordRegex(words);
  if (!re) return [{ text: src, hit: false }];

  const out = [];
  let last = 0;
  re.lastIndex = 0;
  let m;
  while ((m = re.exec(src)) !== null) {
    let start = m.index;
    let end = m.index + m[0].length;
    // Absorb an immediately-preceding hyphenated qualifier ("self-assurance").
    while (start > 0 && src[start - 1] === '-') {
      let k = start - 1;
      while (k > 0 && /[\p{L}'-]/u.test(src[k - 1])) k -= 1;
      start = k;
    }
    if (start > last) out.push({ text: src.slice(last, start), hit: false });
    out.push({ text: src.slice(start, end), hit: true });
    last = end;
    if (m[0].length === 0) re.lastIndex += 1;
  }
  if (last < src.length) out.push({ text: src.slice(last), hit: false });
  return out;
}

/**
 * Split text into [{text, hit}] segments so callers can wrap hits in <mark>.
 * Hyphenated compounds containing the target word are reported as one hit
 * ("self-assurance" for "assurance"), and multi-word entries match their
 * inflected head ("abided by" for "abide by").
 * A null/empty `words` list returns a single non-hit segment.
 * @param {string} text
 * @param {string[]} words
 * @returns {{text:string, hit:boolean}[]}
 */
export function highlightWord(text, words) {
  const src = String(text ?? '');
  if (!src) return [];
  return highlightSegments(src, words);
}

/* ------------------------------------------------------------------ */
/* Cloze (blank-out) helper — Tab 2 & Tab 3 Mode 2                     */
/* ------------------------------------------------------------------ */

/**
 * Replace every occurrence of `word` (and its inflections) inside `sentence`
 * with a blank token. Uses the same matcher as highlighting, so a sentence
 * that highlights also cloze-blanks.
 * @param {string} sentence
 * @param {string} word
 * @param {string} [token] default "______"
 * @returns {string}
 */
export function makeCloze(sentence, word, token = '______') {
  const src = String(sentence ?? '');
  if (!src) return src;
  // Rebuild the sentence from segments so hyphenated compounds are blanked
  // in full ("self-assurance" -> "______").
  const segs = highlightSegments(src, [word]);
  if (!segs.some((s) => s.hit)) return src;
  return segs.map((s) => (s.hit ? token : s.text)).join('');
}

/**
 * All example sentences for a lesson, flattened, tagged with their source word.
 * @param {import('./types.js').Lesson} lesson
 * @returns {{word:string, pos:string, en:string, vi:string, source:'example'|'family'}[]}
 */
export function collectSentences(lesson) {
  const rows = [];
  for (const w of lesson?.words_to_learn || []) {
    for (const ex of w.examples || []) {
      if (ex?.en) rows.push({ word: w.word, pos: w.pos, en: ex.en, vi: ex.vi || '', source: 'example' });
    }
    for (const fam of w.word_family || []) {
      if (fam?.example) {
        rows.push({ word: fam.word, pos: fam.pos, en: fam.example, vi: '', source: 'family' });
      }
    }
  }
  return rows;
}
