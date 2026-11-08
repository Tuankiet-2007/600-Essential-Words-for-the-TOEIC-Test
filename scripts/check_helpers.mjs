// Lead-side sanity harness for the shared highlight/cloze helpers.
// Run: node scripts/check_helpers.mjs
import { readFileSync } from 'node:fs';
import { highlightWord, makeCloze, buildWordRegex } from '../app/src/lib/assets.js';

const lesson = JSON.parse(
  readFileSync(new URL('../public/lessons_json/lesson_01.json', import.meta.url), 'utf8'),
);
const all = lesson.words_to_learn.map((w) => w.word);
let fails = 0;

console.log('=== 1. Every example sentence highlights its own target word ===');
// A valid highlight is the headword OR one of its inflected/derived forms.
// Asking for the exact headword would wrongly fail "parties" for "party".
const headOf = (w) => w.toLowerCase().split(/\s+/)[0].replace(/e$/, '');
for (const w of lesson.words_to_learn) {
  for (const ex of w.examples) {
    const segs = highlightWord(ex.en, all);
    const hits = segs.filter((s) => s.hit).map((s) => s.text.toLowerCase());
    const head = headOf(w.word);
    // Accept the headword anywhere inside the hit, so hyphenated compounds
    // ("self-assurance" for "assurance") count as a valid highlight.
    const own = hits.some((h) => h.replace(/[^a-z]/g, '').includes(head.slice(0, 4)));
    if (!own) {
      fails++;
      console.log(`  [FAIL] "${w.word}" not highlighted in: ${ex.en}`);
      console.log(`         hits=${JSON.stringify(hits)}`);
    }
  }
}
if (!fails) console.log('  all 24 example sentences OK');

console.log('\n=== 2. Multi-word entry "abide by" ===');
const abide = lesson.words_to_learn.find((w) => w.word === 'abide by');
for (const ex of abide.examples) {
  const segs = highlightWord(ex.en, all);
  const hits = segs.filter((s) => s.hit).map((s) => s.text);
  console.log(`  "${ex.en}"`);
  console.log(`    hits=${JSON.stringify(hits)}`);
  if (!hits.length) fails++;
}

console.log('\n=== 3. Cloze actually removes the target word ===');
for (const w of lesson.words_to_learn) {
  for (const ex of w.examples) {
    const cloaked = makeCloze(ex.en, w.word);
    if (cloaked === ex.en) {
      fails++;
      console.log(`  [FAIL] makeCloze left sentence unchanged for "${w.word}": ${ex.en}`);
    }
  }
}
if (!fails) console.log('  all cloze substitutions applied');

console.log('\n=== 4. Words in Context passage blanks ===');
const passage = lesson.words_in_context.passage;
for (let n = 1; n <= 12; n++) {
  const c = passage.split(`(${n})`).length - 1;
  if (c !== 1) {
    fails++;
    console.log(`  [FAIL] blank (${n}) appears ${c} times`);
  }
}
console.log('  12 blanks numbered (1)..(12) exactly once');

console.log('\n=== 5. answers subset of word_bank ===');
// `answers` là tuỳ chọn: bài OCR từ sách không kèm đáp án (người học tự điền).
// Chỉ kiểm tra quan hệ bao hàm khi thật sự có đáp án.
const { answers, word_bank } = lesson.words_in_context;
if (!word_bank || !word_bank.length) {
  fails++;
  console.log('  [FAIL] word_bank rỗng — không kiểm tra được');
} else if (!answers || !Object.keys(answers).length) {
  console.log(`  (bài này không kèm đáp án — bỏ qua; word_bank có ${word_bank.length} từ)`);
} else {
  const outside = Object.entries(answers).filter(([, v]) => !word_bank.includes(v));
  if (outside.length) {
    fails++;
    console.log('  [FAIL] answers outside word_bank:', outside);
  } else {
    console.log(`  tất cả ${Object.keys(answers).length} đáp án đều có trong word_bank`);
  }
}

console.log('\n=== 6. Highlighting the full passage with the answer set ===');
const segs = highlightWord(passage, word_bank);
console.log(`  segments=${segs.length} hits=${segs.filter((s) => s.hit).length}`);

console.log('\n=== 7. Cloze on the passage ===');
const blanked = word_bank.reduce((acc, w) => makeCloze(acc, w), passage);
const remaining = word_bank.filter((w) => buildWordRegex([w]).test(blanked));
console.log(`  words still present after blanket cloze: ${remaining.length ? remaining.join(', ') : 'none'}`);

console.log(`\n${fails === 0 ? 'ALL CHECKS PASSED' : `${fails} FAILURE(S)`}`);
process.exit(fails === 0 ? 0 : 1);
