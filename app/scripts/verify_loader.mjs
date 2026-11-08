/**
 * verify_loader.mjs — prove the "Chưa trích xuất" state against a REAL server.
 *
 * Boots the dev server in-process, then exercises the actual lessonLoader
 * against it with a fetch shim pointed at the live URL. This is the check that
 * matters: Vite answers a missing .json with the index.html SPA fallback and
 * HTTP 200, so the loader must reject HTML rather than throw.
 *
 * Usage:  node scripts/verify_loader.mjs
 */
import { createServer } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const appRoot = resolve(here, '..');
const repoRoot = resolve(appRoot, '..');

const server = await createServer({
  root: appRoot,
  configFile: false,
  plugins: [react()],
  publicDir: resolve(repoRoot, 'public'),
  server: { port: 5214, strictPort: false, host: '127.0.0.1', fs: { allow: [repoRoot] } },
  logLevel: 'silent',
});
await server.listen();
const port = server.httpServer.address().port;
const base = `http://127.0.0.1:${port}`;

// Point the loader's relative fetches at the live server.
const realFetch = globalThis.fetch;
globalThis.fetch = (input, init) => {
  const url = typeof input === 'string' && input.startsWith('/') ? base + input : input;
  return realFetch(url, init);
};

const { loadLesson } = await import('../src/lib/lessonLoader.js');
const { LESSON_STATUS } = await import('../src/lib/types.js');

let pass = 0;
let fail = 0;
const check = (ok, msg) => {
  ok ? pass++ : fail++;
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${msg}`);
};

// 1. Lesson 1 loads from the OCR path.
const l1 = await loadLesson(1);
check(l1.status === LESSON_STATUS.LOADED, `lesson 1 status = ${l1.status} (want loaded)`);
check(l1.lesson?.words_to_learn?.length === 12, `lesson 1 word count = ${l1.lesson?.words_to_learn?.length} (want 12)`);
check(l1.source?.includes('lesson_01.json'), `lesson 1 source = ${l1.source}`);
check(l1.lesson?.title === 'Contracts', `lesson 1 title = ${l1.lesson?.title}`);

// 2. A missing lesson must resolve to NOT_EXTRACTED, never ERROR/throw.
//    Không hardcode số bài: bài nào đã OCR xong thì không còn "missing" nữa.
//    Tìm một bài thật sự chưa có, dựa trên những bài tải được.
const loaded = [];
for (let i = 1; i <= 50; i++) {
  const r = await loadLesson(i);
  loaded.push([i, r.status]);
}
const missingIds = loaded
  .filter(([, st]) => st === LESSON_STATUS.NOT_EXTRACTED)
  .map(([i]) => i);
const presentIds = loaded
  .filter(([, st]) => st === LESSON_STATUS.LOADED)
  .map(([i]) => i);

console.log(
  `  (đã trích xuất: ${presentIds.length} bài${presentIds.length ? ` — ${presentIds.slice(0, 8).join(',')}${presentIds.length > 8 ? '…' : ''}` : ''}; ` +
    `chưa: ${missingIds.length} bài)`,
);

// Không bắt buộc phải còn bài thiếu: khi đã OCR đủ 50 bài thì điều kiện đó vô
// nghĩa. Miễn là mọi bài được báo NOT_EXTRACTED đều thật sự không có payload.
for (const id of missingIds.slice(0, 3)) {
  const r = await loadLesson(id);
  check(
    r.status === LESSON_STATUS.NOT_EXTRACTED,
    `lesson ${id} status = ${r.status} (want ${LESSON_STATUS.NOT_EXTRACTED})`,
  );
  check(r.lesson === null, `lesson ${id} has no lesson payload`);
}

// Đủ cả 50 bài thì không còn bài "missing" thật để thử. Vẫn phải chứng minh
// cơ chế fallback hoạt động: một id NGOÀI khoảng 1..50 chắc chắn không có file,
// loader phải trả NOT_EXTRACTED chứ không throw.
{
  const r = await loadLesson(999);
  check(
    r.status === LESSON_STATUS.NOT_EXTRACTED,
    `lesson 999 (ngoài sách) status = ${r.status} (want ${LESSON_STATUS.NOT_EXTRACTED})`,
  );
  check(r.lesson === null, 'lesson 999 has no lesson payload');
}

// 3. Normalisation must be present so tabs never see undefined branches.
const L = l1.lesson;
check(Array.isArray(L.practice?.listening?.part2), 'practice.listening.part2 normalized to array');
check(Array.isArray(L.practice?.reading?.part5), 'practice.reading.part5 normalized to array');
check(typeof L.words_in_context?.passage === 'string' && L.words_in_context.passage.length > 0, 'words_in_context.passage present');
// `answers` là tuỳ chọn: bài OCR từ sách không kèm đáp án, và loader phải trả {}
// thay vì undefined để Tab 1 không vỡ. Bài có đáp án thì phải đủ 12 khoá.
const answers = L.words_in_context?.answers;
check(answers !== undefined && typeof answers === 'object', 'words_in_context.answers is an object (never undefined)');
const nAns = Object.keys(answers || {}).length;
check(
  nAns === 0 || nAns === 12,
  `words_in_context.answers has ${nAns} keys (want 0 khi chưa có đáp án, hoặc 12)`,
);
// Bài OCR phải có word_bank để người học tự đối chiếu khi thiếu đáp án.
check(Array.isArray(L.words_in_context?.word_bank), 'words_in_context.word_bank normalized to array');

// 4. Các lỗi tích hợp từng làm MẤT dữ liệu phải không tái diễn.
//
// JSON của OCR đặt `listening` ở cấp cao nhất và `practice.part5/6/7`, còn các
// tab đọc `practice.listening.*` và `practice.reading.*`. Trước đây loader chỉ
// đọc vị trí của tab, nên TOÀN BỘ phần Listening và Part 5/7 biến mất khỏi UI
// dù JSON có đủ. Test dưới đây khoá lại đúng lỗi đó.
console.log('\n--- normalization: OCR layout -> tab layout ---');

// Đếm thật trên toàn sách: các tab chỉ đọc dữ liệu đã chuẩn hoá.
let totP3 = 0;
let totP4 = 0;
let totP5 = 0;
let totP7q = 0;
for (let i = 1; i <= 50; i++) {
  const r = await loadLesson(i);
  if (r.status !== LESSON_STATUS.LOADED) continue;
  const p = r.lesson.practice;
  totP3 += p.listening.part3.length;
  totP4 += p.listening.part4.length;
  totP5 += p.reading.part5.length;
  totP7q += p.reading.part7.questions.length;
}
check(totP3 > 0, `practice.listening.part3 có câu hỏi (${totP3}) — JSON để listening ở top-level`);
check(totP4 > 0, `practice.listening.part4 có câu hỏi (${totP4})`);
check(totP5 > 0, `practice.reading.part5 có câu hỏi (${totP5}) — JSON để ở practice.part5`);
check(totP7q > 0, `practice.reading.part7.questions có câu hỏi (${totP7q})`);

// Mỗi câu hỏi phải có số thứ tự và options dạng object {A:...}, không phải mảng.
const sample = L.practice.reading.part5[0];
check(Boolean(sample), 'part5[0] tồn tại sau chuẩn hoá');
if (sample) {
  check(
    Number.isFinite(sample.question_num),
    `part5[0].question_num là số (${sample.question_num})`,
  );
  check(
    sample.options && !Array.isArray(sample.options) && typeof sample.options === 'object',
    'part5[0].options là object {A:...} (JSON gốc là mảng [{label,text}])',
  );
  check(
    typeof sample.options.A === 'string' && sample.options.A.length > 0,
    `part5[0].options.A có nội dung ("${String(sample.options.A).slice(0, 30)}…")`,
  );
  // Tab 5 đọc `item.sentence` làm đề bài Part 5 — thiếu nó thì câu hỏi trống chữ.
  check(
    typeof sample.sentence === 'string' && sample.sentence.length > 10,
    'part5[0].sentence có nội dung (Tab 5 đọc trường này làm đề bài)',
  );
}

// Part 6: passage có marker [16][17][18] + câu hỏi đi kèm (sách in Part 6 trên
// cùng trang Part 5; trước đây parser bỏ qua hoàn toàn).
const p6 = L.practice.reading.part6;
check(Boolean(p6?.passage), 'part6.passage có đoạn văn');
check(
  /\[1[6-8]\]/.test(p6?.passage || ''),
  'part6.passage giữ marker [16]/[17]/[18] để gắn câu hỏi',
);
check(
  (p6?.questions?.length || 0) >= 2,
  `part6.questions có câu hỏi (${p6?.questions?.length})`,
);

// Part 7: tài liệu phải có nội dung trong `body` (PassageDocument đọc header/body).
const p7doc = L.practice.reading.part7.passages?.[0];
check(
  typeof p7doc?.body === 'string' && p7doc.body.length > 50,
  'part7.passages[0].body có nội dung tài liệu',
);

// Tapescript phải trung thực: chưa scan phần cuối sách thì KHÔNG được bịa.
// (Trường này rỗng là đúng; điều sai là nhét phần hướng dẫn vào đây.)
let bogusTapescript = 0;
for (let i = 1; i <= 50; i++) {
  const r = await loadLesson(i);
  if (r.status !== LESSON_STATUS.LOADED) continue;
  const t = r.lesson.practice.tapescript;
  if (typeof t === 'string' && /Look at the picture and listen/i.test(t)) bogusTapescript++;
}
check(
  bogusTapescript === 0,
  `không bài nào nhét phần hướng dẫn vào tapescript (${bogusTapescript} bài sai)`,
);

// 5. Memoisation: second call must be the same object (no refetch).
const again = await loadLesson(1);
check(again === l1, 'lesson 1 result is memoized (same object identity)');

console.log(`\n${pass} passed, ${fail} failed`);
await server.close();
process.exit(fail === 0 ? 0 : 1);
