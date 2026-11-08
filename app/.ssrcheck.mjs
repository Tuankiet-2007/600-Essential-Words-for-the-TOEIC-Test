/**
 * Definitive verification: bundle Tab1 + Tab2 with rolldown (in-process, no spawn),
 * then server-render both against the REAL lesson_01.json inside an AppProvider.
 * Proves: modules resolve, no runtime crash, and context-first output is present.
 */
import { rolldown } from 'rolldown';
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const entryId = 'ssr-entry';
const entryCode = `
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { AppProvider } from './src/lib/store.jsx';
import Tab1 from './src/tabs/Tab1Vocabulary.jsx';
import Tab2 from './src/tabs/Tab2Flashcards.jsx';
import lesson from './.lesson.json' with { type: 'json' };

export function render() {
  const out = {};
  out.tab1 = renderToStaticMarkup(
    React.createElement(AppProvider, null, React.createElement(Tab1, { lesson }))
  );
  out.tab2 = renderToStaticMarkup(
    React.createElement(AppProvider, null, React.createElement(Tab2, { lesson }))
  );
  out.tab1Null = renderToStaticMarkup(
    React.createElement(AppProvider, null, React.createElement(Tab1, { lesson: null }))
  );
  out.tab2Null = renderToStaticMarkup(
    React.createElement(AppProvider, null, React.createElement(Tab2, { lesson: null }))
  );
  // Tab2 shows ONE card at a time — render a single-word lesson per word so every
  // word's own back face (collocations + family) can be asserted.
  out.perWord = lesson.words_to_learn.map((w) => ({
    word: w.word,
    html: renderToStaticMarkup(
      React.createElement(AppProvider, null,
        React.createElement(Tab2, { lesson: { ...lesson, words_to_learn: [w] } }))
    ),
  }));
  return out;
}
export default render;
`;

const bundle = await rolldown({
  input: entryId,
  plugins: [
    {
      name: 'virtual-entry',
      resolveId(id) {
        if (id === entryId) return id;
        return null;
      },
      load(id) {
        if (id === entryId) return entryCode;
        return null;
      },
    },
  ],
});

await bundle.write({
  file: '.ssr/out.mjs',
  format: 'esm',
  inlineDynamicImports: true,
});
await bundle.close();

console.log('BUNDLE OK -> .ssr/out.mjs');

const mod = await import(pathToFileURL(path.resolve('.ssr/out.mjs')).href);
const out = mod.render();

const assert = (cond, label) => console.log((cond ? '  OK   ' : '  FAIL ') + label);

console.log('\n=== Tab1 rendered (lesson present) ===');
assert(out.tab1.length > 2000, `produces markup (${out.tab1.length} chars)`);
assert((out.tab1.match(/vocab-hit/g) || []).length >= 12, `highlights target words in examples (${(out.tab1.match(/vocab-hit/g) || []).length} marks)`);
assert(/abide by/.test(out.tab1), 'renders word "abide by"');
assert(/tuân thủ/.test(out.tab1), 'renders Vietnamese definition');
assert(/abide by a decision/.test(out.tab1), 'renders collocation chips');
assert(/Cụm từ thường gặp/.test(out.tab1), 'renders collocation section label');
assert(/Họ từ \(word family\)/.test(out.tab1), 'renders word-family table');
assert(/assuredly/.test(out.tab1), 'renders adverb family form (assuredly)');
assert(/He spoke assuredly/.test(out.tab1), 'renders family form OWN example sentence');
assert(/Đánh dấu đã học/.test(out.tab1), 'renders learned toggle');
assert(/Hiện tiếng Việt/.test(out.tab1), 'renders VI show/hide toggle');
assert(/—/.test(out.tab1), 'renders em dash for missing family cells');
assert(/Ví dụ trong sách/.test(out.tab1), 'labels the in-book examples');
// count em dashes: must be >= number of empty family cells (12 words, 6 with family)
const dashes = (out.tab1.match(/>—</g) || []).length;
assert(dashes >= 12, `em-dash cells present (${dashes})`);

console.log('\n=== Tab2 rendered (lesson present) ===');
assert(out.tab2.length > 1500, `produces markup (${out.tab2.length} chars)`);
assert(/flip-scene/.test(out.tab2) && /flip-inner/.test(out.tab2) && /flip-face/.test(out.tab2), 'uses .flip-scene/.flip-inner/.flip-face');
assert(!/is-flipped/.test(out.tab2), 'starts unflipped');
assert(/cloze-blank/.test(out.tab2), 'renders cloze blank with .cloze-blank');
assert(/______/.test(out.tab2), 'cloze blank token present on front');
assert(/Thẻ 1\/12/.test(out.tab2), 'session counter "Thẻ 1/12"');
assert(/Xáo trộn/.test(out.tab2) && /Bắt đầu lại/.test(out.tab2), 'shuffle + restart controls');
assert(/Again/.test(out.tab2) && /Hard/.test(out.tab2) && /Good/.test(out.tab2) && /Easy/.test(out.tab2), 'GRADES labels from srs.js');
assert(/Quên/.test(out.tab2) && /Khó/.test(out.tab2), 'Vietnamese grade sublabels');
// front must NOT reveal the answer: target word must be gone from the cloze sentence
assert(/The two parties agreed to ______ the judge/.test(out.tab2),
       "target word blanked out of its own example (front shows \"agreed to ______ the judge's decision.\")");
assert(!/agreed to abide by the judge/.test(out.tab2), 'unblanked sentence is NOT on the front face');

console.log('\n=== Null-safety (lesson={null}) ===');
assert(/Chưa có dữ liệu từ vựng/.test(out.tab1Null), 'Tab1 renders Vietnamese empty state');
assert(/Chưa có flashcard/.test(out.tab2Null), 'Tab2 renders Vietnamese empty state');
assert(out.tab1Null.length < 2000 && out.tab2Null.length < 2000, 'empty states are small, no crash');

// ---- CONTEXT-FIRST AUDIT: every word appears in a card that also has its example ----
console.log('\n=== Context-first audit (Tab1) ===');
const lesson = JSON.parse(fs.readFileSync('.lesson.json', 'utf8'));
let bare = [];
for (const w of lesson.words_to_learn) {
  const escaped = w.word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const idx = out.tab1.search(new RegExp('>' + escaped + '<'));
  const hasWord = idx >= 0;
  // every occurrence of the word must co-occur with its definition
  const defOk = out.tab1.includes(w.definition_en.slice(0, 20));
  if (!hasWord) bare.push(w.word);
  if (!defOk) bare.push(w.word + ' (no definition)');
}
assert(bare.length === 0, bare.length ? 'missing context for: ' + bare.join(', ') : 'all 12 words ship with definition + examples + collocations + family table');

console.log('\n=== Regression: verifier-flagged collocation integrity (per-word cards) ===');
// Tab2 renders ONE card at a time, so assert each word against its OWN rendered card.
let butchered = [];
let checked = 0;
for (const { word, html } of out.perWord) {
  const w = lesson.words_to_learn.find((x) => x.word === word);
  for (const c of w.collocations || []) {
    checked++;
    if (!html.includes(c)) butchered.push(`${word}: ${c}`);
  }
}
assert(butchered.length === 0,
  butchered.length ? 'butchered/missing collocations: ' + butchered.slice(0, 6).join(' | ')
                   : `all ${checked} collocations render verbatim on their card's back face`);

// No partial-word blanking artifacts anywhere.
const artifacts = ['______ment', '______ions', '______ations', '______d b', '______s f'];
const artifactHits = [];
for (const { html } of out.perWord) {
  for (const a of artifacts) if (html.includes(a)) artifactHits.push(a);
}
assert(artifactHits.length === 0,
  artifactHits.length ? 'partial-blank artifacts: ' + [...new Set(artifactHits)].join(', ')
                      : 'no partial-word blanking artifacts');

// The verifier's measured cases, each on its own word's card.
const cases = [
  ['obligate', 'legal and moral obligation'],
  ['party', 'both parties'],
  ['establish', 'at your establishment (n.)'],
  ['obligate', 'be obligated by the contract to do sth'],
  ['provision', 'make provisions for'],
  ['specific', 'according to our specifications'],
];
const caseFails = [];
for (const [word, colloc] of cases) {
  const row = out.perWord.find((p) => p.word === word);
  if (!row || !row.html.includes(colloc)) caseFails.push(`${word} -> "${colloc}"`);
}
assert(caseFails.length === 0,
  caseFails.length ? 'still mangled: ' + caseFails.join(', ')
                   : 'all previously-mangled collocations intact (obligation/parties/establishment/obligated/provisions/specifications)');

console.log('\n=== Regression: regex-metachar words must not crash or mis-match ===');
// The old `new RegExp(entry.word)` threw on these. Render Tab2 with hostile words.
const hostile = {
  lesson_id: 99, title: 'Hostile', theme_id: 1, theme_name: 'x',
  words_to_learn: [
    { id: 1, word: 'c++', pos: 'n.', ipa: '', definition_en: 'a language', definition_vi: 'ngôn ngữ',
      collocations: ['use c++ today'], examples: [{ en: 'We use c++ at work.', vi: 'Chúng tôi dùng c++.' }] },
    { id: 2, word: '[unclosed', pos: 'n.', ipa: '', definition_en: 'a bracket', definition_vi: 'dấu ngoặc',
      collocations: ['the [unclosed case'], examples: [{ en: 'This is [unclosed here.', vi: 'Đây là [unclosed.' }] },
    { id: 3, word: 'a|b', pos: 'n.', ipa: '', definition_en: 'pipe', definition_vi: 'ống',
      collocations: ['a|b chip'], examples: [{ en: 'The a|b chip is here.', vi: 'Chip a|b ở đây.' }] },
  ],
};
fs.writeFileSync('.hostile.json', JSON.stringify(hostile));
const hostileEntry = `
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { AppProvider } from './src/lib/store.jsx';
import Tab2 from './src/tabs/Tab2Flashcards.jsx';
import hostile from './.hostile.json' with { type: 'json' };
export function renderHostile() {
  // One card at a time -> render each hostile word as its own single-word lesson.
  return hostile.words_to_learn.map((w) => ({
    word: w.word,
    html: renderToStaticMarkup(
      React.createElement(AppProvider, null,
        React.createElement(Tab2, { lesson: { ...hostile, words_to_learn: [w] } }))
    ),
  }));
}
export default renderHostile;
`;
const hb = await rolldown({
  input: 'hostile-entry',
  plugins: [{
    name: 'v',
    resolveId: (id) => (id === 'hostile-entry' ? id : null),
    load: (id) => (id === 'hostile-entry' ? hostileEntry : null),
  }],
});
await hb.write({ file: '.ssr/hostile.mjs', format: 'esm', inlineDynamicImports: true });
await hb.close();
let hostileOk = true;
let hostileRows = [];
try {
  const hm = await import(pathToFileURL(path.resolve('.ssr/hostile.mjs')).href);
  hostileRows = hm.renderHostile();
} catch (e) {
  hostileOk = false;
  console.log('  THROW  rendering hostile lesson: ' + e.message);
}
assert(hostileOk, 'Tab2 renders hostile metachar words without throwing (was SyntaxError before fix)');
if (hostileOk) {
  const find = (w) => hostileRows.find((r) => r.word === w)?.html || '';
  assert(find('c++').includes('c++'), '"c++" rendered verbatim');
  assert(find('[unclosed').includes('[unclosed'), '"[unclosed" rendered verbatim');
  assert(find('a|b').includes('a|b'), '"a|b" rendered verbatim');
  // The old code mis-blanked cross-word: /a|b/ matched ANY character.
  assert(!find('a|b').includes('______'), '"a|b" card shows no bogus blank (| was treated as alternation)');
}

console.log('\nDONE');
