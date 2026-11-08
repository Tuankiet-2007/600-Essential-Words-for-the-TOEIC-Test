/**
 * verify_runtime.mjs — end-to-end runtime verification of the local web app.
 *
 * Starts the real Vite dev server IN THIS PROCESS (so it inherits full
 * workspace access), then requests every asset the app depends on and asserts
 * the expected status codes. Exits non-zero if any check fails.
 *
 * Usage:  node scripts/verify_runtime.mjs
 */
import { createServer } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url)); // <repo>/app/scripts
const appRoot = resolve(here, '..'); // <repo>/app
const repoRoot = resolve(appRoot, '..'); // <repo>

const server = await createServer({
  root: appRoot,
  configFile: false,
  plugins: [react()],
  publicDir: resolve(repoRoot, 'public'),
  server: { port: 5211, strictPort: false, host: '127.0.0.1', fs: { allow: [repoRoot] } },
  logLevel: 'silent',
});
await server.listen();
const port = server.httpServer.address().port;
const base = `http://127.0.0.1:${port}`;
console.log(`Dev server (in-process) listening on ${base}\n`);

/** path -> expected status */
const CHECKS = [
  ['/', 200, 'app shell'],
  ['/index.html', 200, 'app shell'],
  ['/src/main.jsx', 200, 'entry module'],
  ['/src/App.jsx', 200, 'app root module'],
  ['/src/tabs/Tab1Vocabulary.jsx', 200, 'Tab1 module'],
  ['/src/tabs/Tab2Flashcards.jsx', 200, 'Tab2 module'],
  ['/src/tabs/Tab3Srs.jsx', 200, 'Tab3 module'],
  ['/src/tabs/Tab4AiLab.jsx', 200, 'Tab4 module'],
  ['/src/tabs/Tab5Practice.jsx', 200, 'Tab5 module'],
  ['/lessons_json/lesson_01.json', 200, 'lesson 1 data (primary path)'],
  ['/sample_lessons/lesson_01.json', 200, 'lesson 1 sample fallback'],
  ['/audio/track_01.mp3', 200, 'track 1 (converted from WMA)'],
  ['/audio/track_25.mp3', 200, 'track 25 (converted from WMA)'],
  ['/audio/track_26.mp3', 200, 'track 26 (original MP3)'],
  ['/audio/track_50.mp3', 200, 'track 50 (original MP3)'],
  ['/part1_photos/lesson_01.jpg', 200, 'Part 1 photo lesson 1'],
  ['/part1_photos/lesson_50.jpg', 200, 'Part 1 photo lesson 50'],
];

let pass = 0;
let fail = 0;
for (const [path, expected, label] of CHECKS) {
  let status = 0;
  let size = 0;
  try {
    const res = await fetch(base + path);
    status = res.status;
    const buf = await res.arrayBuffer();
    size = buf.byteLength;
  } catch (e) {
    status = `ERR ${e.message}`;
  }
  const ok = status === expected;
  if (ok) pass++;
  else fail++;
  console.log(
    `${ok ? 'PASS' : 'FAIL'}  ${String(status).padEnd(5)} (want ${expected})  ${String(size).padStart(9)} B  ${path}  — ${label}`,
  );
}

/*
 * Absent lessons. NOTE: Vite answers a missing .json with the index.html SPA
 * fallback and HTTP 200, so a status-code assertion alone cannot detect
 * absence. The loader must detect the HTML content-type — assert that here,
 * because it is the real behaviour the "Chưa trích xuất" state depends on.
 */
console.log('\n--- missing lesson detection (SPA fallback must be HTML) ---');
// Không hardcode số bài: sau khi OCR chạy, các bài "2", "50" có thể đã tồn tại.
// Dò thật: bài nào trả JSON hợp lệ thì coi như có; còn lại là "chưa trích xuất".
// Nếu đã đủ 50 bài thì dùng đường dẫn chắc chắn không tồn tại để vẫn kiểm chứng
// được cơ chế fallback (đây là thứ trạng thái "Chưa trích xuất" dựa vào).
let missingPaths = [];
for (let i = 1; i <= 50 && missingPaths.length < 2; i++) {
  const p = `/lessons_json/lesson_${String(i).padStart(2, '0')}.json`;
  const res = await fetch(base + p);
  const ctype = res.headers.get('content-type') || '';
  if (!(res.status === 200 && ctype.includes('json'))) missingPaths.push(p);
}
if (missingPaths.length === 0) {
  console.log('  (đã đủ 50 bài — kiểm tra fallback bằng đường dẫn không tồn tại)');
  missingPaths = ['/lessons_json/lesson_97.json', '/lessons_json/lesson_98.json'];
}
for (const path of missingPaths) {
  const res = await fetch(base + path);
  const ctype = res.headers.get('content-type') || '';
  const body = await res.text();
  // Either a genuine 404, or a 200 serving the HTML shell (which the loader
  // rejects as "not extracted"). Anything else, e.g. real JSON, is a failure.
  const ok = res.status === 404 || ctype.includes('text/html') || body.trimStart().startsWith('<');
  ok ? pass++ : fail++;
  console.log(
    `${ok ? 'PASS' : 'FAIL'}  status=${res.status} ctype=${ctype || '(none)'}  ${path}  — detected as absent`,
  );
}

// Content sanity: lesson JSON must still parse and carry 12 words.
try {
  const res = await fetch(`${base}/lessons_json/lesson_01.json`);
  const data = await res.json();
  const words = data.words_to_learn?.length ?? 0;
  const ok = words === 12;
  ok ? pass++ : fail++;
  console.log(`\n${ok ? 'PASS' : 'FAIL'}  lesson_01.json parses, words_to_learn=${words}`);
} catch (e) {
  fail++;
  console.log(`\nFAIL  lesson_01.json did not parse: ${e.message}`);
}

console.log(`\n${pass} passed, ${fail} failed`);
await server.close();
process.exit(fail === 0 ? 0 : 1);
