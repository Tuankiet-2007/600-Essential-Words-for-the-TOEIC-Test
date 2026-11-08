# verify_notes.md — verifier scratch (task-4)

## PHASE A — data fidelity + pure functions (DONE, evidence below)

Commands (repo root `D:\LEGION\Documents\deepseek-harness\TiengAnh`):

```
mkdir .verify
cp app/src/lib/assets.js .verify/assets.mjs
node -e "import('./.verify/assets.mjs').then(A => { ... })"
```

### A1 PASS — lesson_01.json shape
- `public/lessons_json/lesson_01.json` = 12 `words_to_learn`; every entry has
  word/pos/ipa/definition_en/definition_vi/collocations/examples. 2 examples + >=2 collocations each.
- word_family ABSENT for: abide by, determine, engage, establish, party, resolve (id 1,5,6,7,9,11).
- `words_in_context` = {word_bank(12), passage(917 chars), answers(12)}.
- answers keys 1..12, all 12 values appear in word_bank (case-insensitive). PASS.
- passage blank markers: exactly `(1)`..`(12)`, each once, no dups, no missing, and every
  marker is followed by `___`. PASS.

### A2 BLOCKER — buildWordRegex drops sibilant-final -es/-ed, apostrophe and y->ies
`app/src/lib/assets.js:71-87`. Line 71 gates inflection generation on
`/^[a-z][a-z'-]*$/i.test(last)`; lines 72-81 then build forms by naive suffix concatenation
with `base = last.replace(/e$/i,'')` — which is wrong for the R-less doubling case.

Measured (`specifies`, `specifying`, `specified`, `establishment`, `parties`, `abided by`,
`cancelled`, `provisioning`, `engaging` are all realistic forms the app must highlight/cloze):

| input | highlighted? |
|---|---|
| obligates / obligated / obligating | YES |
| specifies / specifying / specified | **NO** |
| establishment | **NO** |
| parties | **NO** |
| provisioning | **NO** |
| abided (in "abided by") | **NO** |
| cancelled | **NO** |

Root cause: `specific` -> base `specif` -> `specifes/specifed/specifing`; `party` -> base `party`
-> `partys/partyes/partyed`; `establish` has no `-ment` form; `abide by` head/last split produces
`abide bys/abide byed/abide bying` and no `abided by`; `cancel` -> base `cancel` -> `canceles/canceled`.

Regex source confirms the fabricated variants: `specificing|specifices|specificed|partying|partyes|resolvees|resolveed|engagees|engageed|provisiones|...`

### A3 MAJOR (user-visible) — cloze fails on 3 of 24 example sentences
`makeCloze` inherits A2. Verified per-word (isolated, `highlightWord(ex.en,[w.word])`):

| word | example sentence | cloze result |
|---|---|---|
| abide by | "For years he has **abided by** a commitment to annual employee raises." | NOT blanked (returns sentence unchanged) |
| assurance | "Her **self-assurance** made it easy to see why she was in charge..." | NOT blanked |
| party | "The **parties** agreed to a settlement in their contract dispute." | NOT blanked |

3 FAIL / 24 example sentences; the other 21 blank correctly.
Note: `party`/`parties` is **answer #2 of the words_in_context passage**, so Tab3 Mode 1/2
and Tab2 flashcards show a raw answer with the target word still visible.
Caveat for the author: `self-assurance` is arguably a *different* head word (assurance in a
compound); blanking it is optional, but leaving it unblanked means Tab2 shows the answer in clear.

### A4 PASS — no false-positive highlighting
Boundaries `(?<![\w'-])...(?![\w'-])` are correct. Adversarial probes all clean:
`part`, `particular`, `provisional`, `determination`, `resolution`, `engagement`,
`specification`, `specifically`, `we must part ways` -> NO hits. Good.

## PHASE B — static contract compliance (DONE)

Files: Tab1Vocabulary, Tab2Flashcards, Tab3Srs, Tab4AiLab, Tab5Practice.

Import whitelist audit (`.verify/static_check.mjs`, 16 files):
- `import/export problems: 0` — every relative import resolves to a real file, and every
  named import actually exists as an export in the target module.
- No bare imports other than react / react-dom / lucide-react.
- Tab5 imports: react, lucide-react, ../components/ui.jsx, ../lib/assets.js, ../lib/srs.js,
  ../lib/storage.js, ../lib/store.jsx. All allowed.

Syntax/parse audit with the project's OWN parser (rolldown ~1.2.16, same engine Vite 8.3.6 uses),
`.verify/entry_check.mjs`:
- `app/src/App.jsx` -> 19 chunks OK  (this pulls in lib/, data/, components/ and all 5 lazy tabs)
- `app/src/tabs/Tab5Practice.jsx` -> 1 chunk OK
- `main.jsx` "fails" only under my bare-rolldown harness because bare rolldown cannot bundle
  the CSS entry (`@import 'tailwindcss'`) — NOT an app defect; Vite supplies the CSS plugin.
- => all 16 src files parse clean. No JSX/syntax errors.

Null-safety (every default export takes `{lesson}` and guards):
- Tab1Vocabulary.jsx:315 `export default function Tab1Vocabulary({ lesson })`, guard L353 `if (!lesson || !entries.length)`
- Tab2Flashcards.jsx:150 `({ lesson })`, guard L230 `if (!lesson || !entries.length)`
- Tab3Srs.jsx:849 `({ lesson })`, guard L860 `if (!lesson)`
- Tab4AiLab.jsx:875 `({ lesson })`, guard L880 `{!lesson ? (`
- Tab5Practice.jsx:1209 `({ lesson })`, L1216 `Number(lesson?.lesson_id ?? lessonId ?? 1)`, L1239-1257 all `lesson?.practice?...`

### FINDING B3 — MAJOR — Hard Rule 1 violation + unescaped RegExp
`app/src/tabs/Tab2Flashcards.jsx:338`
```jsx
{c.replace(new RegExp(entry.word, 'gi'), '______')}
```
- CONTRACT.md:105-110: "never hand-rolled regex". This is hand-rolled.
- `entry.word` is an UNESCAPED regex source. Adversarial probe (`.verify/tab2_regex_probe.mjs`):
  `c++` -> SyntaxError "Nothing to repeat"; `[unclosed` -> "Unterminated character class";
  `(` -> "Unterminated group"; `a|b` on "cat" -> `c______t`; `a.b` matches `axb`.
  A throw happens during render and App.jsx has no error boundary -> whole tab dies.
  Latent for lesson_01 (metachar-free) but live for any future OCR word.
- Even on clean lesson_01 data it mis-blanks (no word boundaries, no inflection awareness):
  "legal and moral obligation" -> UNCHANGED (target obligate) — answer visible
  "both parties"               -> UNCHANGED (target party)    — answer visible
  "at your establishment (n.)" -> "at your ______ment (n.)"
  "be obligated by..."         -> "be ______d by..."
  "make provisions for"        -> "make ______s for"
  "according to our specifications" -> "according to our ______ations"
Routed to vocab-dev.

## PHASE D — RE-VERIFICATION AFTER THE FIX (assets.js rewritten by Lead)

`node scripts/check_helpers.mjs` (Lead's own script) -> **ALL CHECKS PASSED**, exit 0.

My independent re-run, `.verify/consolidated.mjs` + `.verify/reverify.mjs`:

CONFIRMED FIXED:
- 24/24 example sentences self-highlight AND 24/24 cloze-blank. The 3 old B2 failures are gone:
  "For years he has ______ a commitment..." / "Her ______ made it easy..." / "The ______ agreed to a settlement..."
- "abided by" now matches for target "abide by" (head-token inflection). PASS.
- establishment / parties / provisioning / engagement / agreement / specification / obligates: PASS.
- containsWord() is stateless: 5 consecutive identical calls all true.
  The old footgun is real and still present for raw callers: `buildWordRegex(...).test()` x4
  -> true,false,true,false. Documented in assets.js:241-245; all internal uses reset lastIndex.
- Boundary regression all PASS: part!~party/particular/parties, form!~information/performance,
  sign!~design, art!~part. And the correct TRUE cases: determine~determined/determination,
  provide~provision, art~artist, sign~signal.
- Hyphen absorption works: "self-assurance" -> one hit segment "self-assurance";
  "well-established" -> "well-established"; "state-of-the-art design" -> no hit (correct: "art" alone).
- makeCloze('')/makeCloze(null) return ''; double-cloze is idempotent (1 blank, not 2).

### FINDING B4 — MINOR — American "-l-" spelling not generated (1 family row misses)
`app/src/lib/assets.js:98,104` — the CVC `doubles` path emits `${lower}${last1}ed` / `${lower}${last1}ing`,
i.e. only the BRITISH doubled form. For `cancel` it produces `cancelled`/`cancelling` but NOT
`canceled`/`canceling`. The book uses American spelling.
Repro:
  node .verify/cancel_probe.mjs
  contains("canceled",  ["cancel"]) = false
  contains("canceling", ["cancel"]) = false
  contains("cancelled", ["cancel"]) = true
  contains("cancelling",["cancel"]) = true
  highlight(["cancel"], "The man canceled his magazine subscription...") -> NO HIT
Impact: lesson_01 word_family row `cancellation -> cancel` ("The man canceled his magazine
subscription and got his money back.") renders with NO highlight. This is the ONLY one of 18
family rows that misses. Same class: travel~traveled, label~labeled.
Not reachable in the 24 examples / 12 passage answers. Suggested minimal fix: in `inflect()`,
for `doubles` also emit the single-consonant variant when `last1 === 'l'`.

### NON-BUGS (explicitly checked, do NOT report as defects)
- `answer (3) specifies`, `(8) provide`, `(12) cancel` are NOT highlightable via the lesson word
  list. That is CORRECT: none of those strings is a lesson target ("specific"/"provision"/
  "cancellation" are). They are distractors in word_bank. Isolated heads DO work:
  contains("specifies",["specify"])=true, contains("cancelled",["cancel"])=true, contains("abided",["abide"])=true.
- `makeCloze(passage, lessonWords)` -> 0 blanks and output === input. CORRECT: the passage already
  has all 12 answers replaced by `___`, so the targets are absent by construction.
  Lead's check #7 "no words survive a blanket cloze" passes for this reason.
- 9/18 family rows where no lesson target appears in the family example (e.g. "assure" for target
  "assurance") — expected; the family word is not a lesson target.
- Tab2's old `new RegExp(entry.word,'gi')` at L338 is GONE. Current Tab2 uses makeCloze (L18/L189).
  FINDING B3 is RESOLVED.

### FINDING B5 — MINOR (hygiene) — debug staging file left in the source tree
`app/src/tabs/.Tab5Practice.patched.jsx` (52734 bytes) — NOT referenced by any import.
Diff vs Tab5Practice.jsx is exactly 2 lines:
  + const [answers, setAnswers] = useState(() => globalThis.__T5_ANSWERS__ || {});
  + const [submitted, setSubmitted] = useState(() => Boolean(globalThis.__T5_SUBMIT__));
VERIFIED INERT on the current revision:
- `__T5_` appears ONLY in the dotfile; Tab5Practice.jsx has zero `globalThis`/`window.__` refs.
- Dotfile is not imported anywhere (App.jsx imports './tabs/Tab5Practice.jsx' explicitly).
Recommend deleting it before final delivery so the graded source tree has no test hooks.

## PHASE B (re-check, current revisions) — ALL PASS
All five tab files exist. Imports strictly within contract:
| file | relative imports | bare |
|---|---|---|
| Tab1Vocabulary.jsx | ../components/ui.jsx, ../lib/{store,storage,types}.js | react, lucide-react |
| Tab2Flashcards.jsx | ../components/ui.jsx, ../lib/{assets,srs,store,types}.js | react, lucide-react |
| Tab3Srs.jsx | ../components/ui.jsx, ../lib/{assets,srs,types,store}.js | react, lucide-react |
| Tab4AiLab.jsx | ../components/ui.jsx, ../lib/store.jsx | react, lucide-react |
| Tab5Practice.jsx | ../components/ui.jsx, ../lib/{assets,srs,storage,store}.js | react, lucide-react |

All five: `export default function TabX({ lesson })` and an explicit null guard
(Tab1:349, Tab2:238, Tab3:860, Tab4:925, Tab5:1371).
`node .verify/static_check.mjs` -> `import/export problems: 0` (16 files; every named import exists).
`node .verify/entry_check.mjs` -> App.jsx bundles to 19 chunks OK, Tab5Practice to 1 chunk OK.
(main.jsx only "fails" under bare rolldown because it cannot bundle the Tailwind CSS entry —
harness artifact, not an app defect.)

## PHASE C — FINAL STATUS: UNVERIFIED-by-verifier (host-only)
`npm run build` and `npm run dev` both abort in Vite's config bundling with `spawn EPERM`
(piped-stdio sandbox boundary). Lead confirmed the host can run both, so Phase C stays Lead-owned.
Not retried, per instruction. Independent byte-level substitutes (all PASS) are recorded above.

```
cd D:\LEGION\Documents\deepseek-harness\TiengAnh\app
$env:npm_config_cache="D:\LEGION\Documents\deepseek-harness\TiengAnh\.npm-cache"
npm run build   -> exit 1
npm run dev     -> exit 1  (background job pwsh-805f1349572c4e38)
```
Both die identically in `failed to load config from ...\app\vite.config.js`:
`[plugin externalize-deps] Error: spawn EPERM` from
`optimizeSafeRealPathSync`/`windowsSafeRealPathSync` -> `exec` (piped stdio).
Vite 8.3.6 bundles vite.config.js at startup via a child process with piped stdio, which the
workspace-write sandbox denies. Proof the boundary is environmental, not app code:
```
node -e "const {execFile}=require('child_process');
  try{execFile('cmd.exe',['/c','echo hi'],(e,so)=>console.log(e?('ERR '+e.code):'OK'))}catch(e){console.log('throw',e.code)}"
-> throw EPERM
```
Node v24.14.0 runs plain scripts fine. Not retried another way (rules); approval disabled.
=> `npm run build` exit 0, Vite printed URL, and all 6 HTTP status checks are UNVERIFIED.
No second server started; no config edited.

### Independent partial substitute for Phase C (all PASS)
Asset resolution + byte-level content, checked on disk (`.verify` script):
- audioUrlFor/photoUrlFor for lessons 1..50 -> all 100 canonical files exist on disk.
- `public/lessons_json/lesson_02.json` ABSENT (-> loader falls through to sample, then
  `not_extracted` -> "Chưa trích xuất"). `lesson_01.json` is byte-identical to
  `sample_lessons/lesson_01.json` (25711 bytes).
- `track_01/25/26/50.mp3` all start with `ID3` => valid MPEG audio; track_26 (converted from
  WMA) is a real 2,887,680-byte MP3 at the byte level.
- `part1_photos/lesson_01.jpg` starts `ff d8 ff` => valid JPEG.
This does NOT prove HTTP 200 (needs the dev server) — it proves the bytes are servable.

### Pure-lib behaviour (`.verify/libs_probe.mjs`, localStorage shimmed)
- GRADES = 1 Again/1, 2 Hard/3, 3 Good/4, 4 Easy/5 as documented.
- srsKey(1,"Abide By") -> "L01:abide by"; markWordLearned stores {"L01:abide by":true}.
- cardsForLesson(1)=1, cardsForLesson(2)=0 (namespace isolation correct).
- isDue: fresh true, null true, +1day false.
- SM-2 intervals Good x4: 1 -> 6 -> 15 -> 38. Again then Good x2: 1/0 -> 1/1 -> 6/2.
- buildQueue(1, 12 words) = 12. pushHistory/saveSettings persistence OK.
- lessonLoader exports {default, invalidateLessonCache, loadLesson, loadLessonIndex}.
