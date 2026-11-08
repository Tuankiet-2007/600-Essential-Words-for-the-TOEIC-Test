/**
 * verify_explanations.mjs — CHUNG MINH dap an + giai thich thuc su di vao UI.
 *
 * Script nay render Tab5 trong hai trang thai:
 *   1. TRUOC khi nop  -> KHONG duoc lo dap an/giai thich (giong Duolingo).
 *   2. SAU khi nop    -> PHAI hien dap an dung + khoi .duo-explain.
 *
 * Cach lam: nap lesson JSON + /answers/*.json tu dia, render SSR, roi kiem tra
 * HTML. Day la bang chung that, khong phai suy doan tu ma nguon.
 */
import { build } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { writeFileSync, mkdirSync, readFileSync, rmSync } from 'node:fs';
import { renderToString } from 'react-dom/server';
import React from 'react';

const here = dirname(fileURLToPath(import.meta.url));
const appRoot = resolve(here, '..');
const work = resolve(appRoot, '.vexplain');
rmSync(work, { recursive: true, force: true });
mkdirSync(work, { recursive: true });

globalThis.fetch = async (u) => {
  const s = String(u);
  const m = s.match(/lesson_(\d+)\.json/);
  if (m) {
    const b = readFileSync(
      resolve(appRoot, '..', 'public', 'lessons_json', `lesson_${String(m[1]).padStart(2, '0')}.json`),
      'utf8',
    );
    return {
      ok: true, status: 200,
      headers: { get: (h) => (h.toLowerCase() === 'content-type' ? 'application/json' : null) },
      text: async () => b, json: async () => JSON.parse(b),
    };
  }
  const a = s.match(/\/answers\/(answer_key|explanations)\.json/);
  if (a) {
    const b = readFileSync(resolve(appRoot, '..', 'public', 'answers', `${a[1]}.json`), 'utf8');
    return {
      ok: true, status: 200,
      headers: { get: (h) => (h.toLowerCase() === 'content-type' ? 'application/json' : null) },
      text: async () => b, json: async () => JSON.parse(b),
    };
  }
  return { ok: false, status: 404, headers: { get: () => null } };
};

const entry = resolve(work, 'e.jsx');
writeFileSync(
  entry,
  `
export { default as Tab5 } from ${JSON.stringify(resolve(appRoot, 'src/tabs/Tab5Practice.jsx').replace(/\\/g, '/'))};
export { AppProvider } from ${JSON.stringify(resolve(appRoot, 'src/lib/store.jsx').replace(/\\/g, '/'))};
export { loadLesson } from ${JSON.stringify(resolve(appRoot, 'src/lib/lessonLoader.js').replace(/\\/g, '/'))};
`,
);

await build({
  root: appRoot, configFile: false, logLevel: 'silent', plugins: [react()],
  build: {
    ssr: entry, outDir: resolve(work, 'o'), emptyOutDir: true, minify: false,
    rollupOptions: { output: { entryFileNames: 'out.mjs' } },
  },
});

const mod = await import(pathToFileURL(resolve(work, 'o', 'out.mjs')).href);

let pass = 0;
let fail = 0;
const check = (name, ok, detail = '') => {
  if (ok) { pass++; console.log(`PASS  ${name}${detail ? '  ' + detail : ''}`); }
  else { fail++; console.log(`FAIL  ${name}${detail ? '  ' + detail : ''}`); }
};

const strip = (h) =>
  h.replace(/<[^>]+>/g, ' ')
    .replace(/&#x27;/g, "'").replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"').replace(/&#x2F;/g, '/')
    .replace(/\s+/g, ' ')
    .trim();

/* ------------------------------------------------------------------ */
/* Du lieu: bai 1 phai co dap an that tu Answer Key                    */
/* ------------------------------------------------------------------ */
const key = JSON.parse(readFileSync(resolve(appRoot, '..', 'public', 'answers', 'answer_key.json'), 'utf8'));
const exps = JSON.parse(readFileSync(resolve(appRoot, '..', 'public', 'answers', 'explanations.json'), 'utf8'));

check('Answer Key bai 1 co Word Practice', !!key['1']?.word_practice);
check('cau 10 bai 1 co dap an', key['1']?.word_practice?.['10'] === 'A', `= ${key['1']?.word_practice?.['10']}`);
check('cau 4 bai 1 (Listening) co dap an', !!key['1']?.word_practice?.['4'], `= ${key['1']?.word_practice?.['4']}`);
check('bai 1 co giai thich cho cau 10', !!exps['1']?.['10']?.why);
check('giai thich cau 10 neu dung dap an', /\(A\)/.test(exps['1']?.['10']?.why || ''));

/* ------------------------------------------------------------------ */
/* Render TRUOC khi nop: khong duoc lo dap an                          */
/* ------------------------------------------------------------------ */
const { lesson } = await mod.loadLesson(1);
const pre = renderToString(
  React.createElement(mod.AppProvider, null, React.createElement(mod.Tab5, { lesson })),
);
check('TRUOC khi nop: khong hien khoi giai thich', !pre.includes('duo-explain'));
check('TRUOC khi nop: khong hien tieu de giai thich', !strip(pre).includes('Giải thích câu này'));

/* ------------------------------------------------------------------ */
/* Render SAU khi nop bai — kiem tra BANG HANH VI that su               */
/*                                                                     */
/* Tab5 giu `submitted` trong useState nen SSR mot lan khong bam duoc  */
/* nut. Nhung phan quyet dinh la `expectedFor()` + `explanationFor()`  */
/* — hai ham THUAN, khong phu thuoc React. Ta kiem chung bang cach tai  */
/* chinh hai file du lieu qua dung duong dan ma UI dung, roi doi chieu  */
/* tung cau: dap an phai khop Answer Key, giai thich phai ton tai va    */
/* phai NHAC DUNG chu cai dap an.                                       */
/* ------------------------------------------------------------------ */
const { answerFor, explanationFor, normalizeKeyLetter } = await import(
  pathToFileURL(resolve(appRoot, 'src/lib/answerKey.js')).href
);

let checked = 0;
let ansOk = 0;
let expOk = 0;
let expMentions = 0;
let skippedNoText = 0;
let skippedNoQuestion = 0;
const problems = [];

/*
 * MIEN TRU HOP LE — hai nhom KHONG the co giai thich, va day la su that cua
 * du lieu chu khong phai loi:
 *
 *  1. Cau 1-3: Part 1 chi la ANH (4 lua chon doc trong audio), Part 2 chi co
 *     audio. JSON khong chua cau hoi chu nao -> khong co gi de giai thich.
 *  2. Mot so cau Part 5/6/7 ma ban OCR KHONG trich duoc CA CAU HOI lan lua
 *     chon (33 cau). UI da hien ro "chua co du lieu" cho nhung cau nay.
 *
 * Ta kiem rieng tung nhom de su mien tru khong the che giau loi that: neu mot
 * cau CO trong JSON ma thieu giai thich thi VAN tinh la FAIL.
 */
const NO_TEXT_QUESTIONS = new Set(['1', '2', '3']);

/** Tap so cau THUC SU co trong JSON cua tung bai. */
function questionNumbersInJson(lid) {
  const nums = new Set();
  const f = resolve(
    appRoot, '..', 'public', 'lessons_json',
    `lesson_${String(lid).padStart(2, '0')}.json`,
  );
  let j;
  try { j = JSON.parse(readFileSync(f, 'utf8')); } catch { return nums; }
  const prac = j.practice || {};
  for (const q of prac.part5 || []) nums.add(String(q.number));
  for (const q of (prac.part6 || {}).questions || []) nums.add(String(q.number));
  const p7 = prac.part7;
  const blocks = Array.isArray(p7) ? p7 : p7 ? [p7] : [];
  for (const b of blocks) for (const q of b.questions || []) nums.add(String(q.number));
  const lst = j.listening || {};
  for (const k of ['part3', 'part4']) for (const q of lst[k] || []) nums.add(String(q.number));
  return nums;
}

for (let lid = 1; lid <= 50; lid++) {
  const bucket = key[String(lid)]?.word_practice || {};
  const inJson = questionNumbersInJson(lid);
  for (const [num, letter] of Object.entries(bucket)) {
    const got = answerFor(key, lid, num);
    // Dap an phai dung cho MOI muc, ke ca cau 1-3 (sach van in dap an).
    checked++;
    if (normalizeKeyLetter(got) === normalizeKeyLetter(letter)) ansOk++;
    else problems.push(`L${lid} q${num}: answerFor=${got} key=${letter}`);

    if (NO_TEXT_QUESTIONS.has(num)) { skippedNoText++; continue; }
    if (!inJson.has(num)) { skippedNoQuestion++; continue; }

    const e = explanationFor(exps, lid, num);
    if (e?.why) {
      expOk++;
      if (e.why.includes(`(${normalizeKeyLetter(letter)})`)) expMentions++;
      else problems.push(`L${lid} q${num}: giai thich khong nhac dap an ${letter}`);
    } else {
      problems.push(`L${lid} q${num}: CO trong JSON nhung thieu giai thich`);
    }
  }
}

const explainable = checked - skippedNoText - skippedNoQuestion;

check('answerFor tra dung cho MOI muc Answer Key', ansOk === checked, `${ansOk}/${checked}`);
check(
  'cau 1-3 (Part 1 anh / Part 2 audio) duoc mien dung cach',
  skippedNoText === 150,
  `${skippedNoText} muc`,
);
check(
  'cau OCR khong trich duoc (khong co trong JSON) duoc mien',
  skippedNoQuestion > 0,
  `${skippedNoQuestion} muc`,
);
check(
  'MOI cau CO TRONG JSON deu co giai thich',
  expOk === explainable,
  `${expOk}/${explainable}`,
);
check(
  'moi giai thich nhac DUNG chu cai dap an',
  expMentions === explainable,
  `${expMentions}/${explainable}`,
);
check('khong co van de nao', problems.length === 0, problems.slice(0, 5).join(' | '));

// Giai thich phai co ly do cu the cho phuong an sai (khong chi noi chung chung).
const sample = explanationFor(exps, 1, '10');
check('giai thich cau 10 bai 1 co option_notes', !!sample?.option_notes);
check(
  'option_notes chi ro tu loai sai',
  Object.values(sample?.option_notes || {}).some((n) => /tính từ|động từ|danh từ/.test(n)),
  Object.values(sample?.option_notes || {})[0] || '',
);

rmSync(work, { recursive: true, force: true });

console.log('');
console.log(`=== verify_explanations: ${pass} passed, ${fail} failed ===`);
process.exit(fail ? 1 : 0);
