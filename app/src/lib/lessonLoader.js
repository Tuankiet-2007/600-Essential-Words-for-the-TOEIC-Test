/**
 * FROZEN CONTRACT — dynamic lesson loader.
 *
 * Resolution order for lesson NN:
 *   1. /lessons_json/lesson_NN.json        (OCR output; served from public/)
 *   2. /sample_lessons/lesson_NN.json      (bundled sample; only NN=01 exists)
 *   3. -> { status: 'not_extracted' }      (UI shows "Chưa trích xuất")
 *
 * Results are memoized in-module so repeat tab switches do not refetch.
 */
import { LESSON_STATUS } from './types.js';

const cache = new Map(); // lessonId -> result object

/** Index of which lessons exist, hydrated once by loadLessonIndex(). */
let indexCache = null;

const BASE = import.meta.env.BASE_URL || './';
const cleanBase = BASE.endsWith('/') ? BASE : BASE + '/';

function pad2(n) {
  return String(Number(n)).padStart(2, '0');
}

/** Candidate URLs, in priority order. */
function candidateUrls(lessonId) {
  const nn = pad2(lessonId);
  return [`${cleanBase}lessons_json/lesson_${nn}.json`, `${cleanBase}sample_lessons/lesson_${nn}.json`];
}

/**
 * Fetch + validate one lesson.
 * @param {number} lessonId
 * @returns {Promise<{status:string, lesson:Object|null, source:string|null, error?:string}>}
 */
export async function loadLesson(lessonId) {
  const id = Number(lessonId);
  if (cache.has(id)) return cache.get(id);

  let lastError = null;
  let sawHtmlFallback = false;

  for (const url of candidateUrls(id)) {
    try {
      const res = await fetch(url, { cache: 'no-cache' });
      if (!res.ok) continue;

      /*
       * IMPORTANT: Vite's dev server (and most SPA hosts) answer a missing
       * JSON file with the index.html SPA fallback and HTTP 200, not 404.
       * Blindly calling res.json() would throw "Unexpected token '<'".
       * Detect the HTML fallback explicitly and treat it as "file absent".
       */
      const ctype = res.headers.get('content-type') || '';
      if (ctype.includes('text/html')) {
        sawHtmlFallback = true;
        continue;
      }

      const raw = await res.text();
      const trimmed = raw.trimStart();
      if (trimmed.startsWith('<')) {
        sawHtmlFallback = true;
        continue;
      }

      let data;
      try {
        data = JSON.parse(raw);
      } catch {
        lastError = `Tệp không phải JSON hợp lệ: ${url}`;
        continue;
      }

      if (!isValidLesson(data)) {
        lastError = `Dữ liệu không đúng cấu trúc: ${url}`;
        continue;
      }
      const result = normalizeLesson({
        status: LESSON_STATUS.LOADED,
        lesson: data,
        source: url,
      });
      cache.set(id, result);
      return result;
    } catch (err) {
      lastError = err?.message || String(err);
    }
  }

  // An HTML fallback for every candidate means the files genuinely do not
  // exist -> "Chưa trích xuất". A real parse/network error is reported as ERROR.
  const missing =
    lastError && !sawHtmlFallback
      ? { status: LESSON_STATUS.ERROR, lesson: null, source: null, error: lastError }
      : { status: LESSON_STATUS.NOT_EXTRACTED, lesson: null, source: null };
  // Only memoize a definitive "not extracted"; transient errors should retry next open.
  if (missing.status === LESSON_STATUS.NOT_EXTRACTED) cache.set(id, missing);
  return missing;
}

/**
 * Cheap existence probe for the sidebar. Tries HEAD on-lesson files.
 * Falls back to "unknown" when the dev server does not answer HEAD.
 * @returns {Promise<Record<number, boolean>>}
 */
export async function loadLessonIndex() {
  if (indexCache) return indexCache;
  const ids = Array.from({ length: 50 }, (_, i) => i + 1);
  const entries = await Promise.all(
    ids.map(async (id) => {
      for (const url of candidateUrls(id)) {
        try {
          // GET (not HEAD) — Vite's static middleware is reliable for GET.
          const res = await fetch(url, { method: 'GET', cache: 'no-cache' });
          if (res.ok) {
            try {
              const data = await res.json();
              if (isValidLesson(data)) return [id, true];
            } catch {
              /* malformed -> treat as absent */
            }
          }
        } catch {
          /* keep trying */
        }
      }
      return [id, false];
    }),
  );
  indexCache = Object.fromEntries(entries);
  return indexCache;
}

/** Force a re-probe (used by a "Quét lại" button after OCR produces new files). */
export function invalidateLessonCache() {
  cache.clear();
  indexCache = null;
}

function isValidLesson(data) {
  return Boolean(
    data &&
      typeof data === 'object' &&
      Array.isArray(data.words_to_learn) &&
      data.words_to_learn.length > 0,
  );
}

/**
 * OCR sinh `options` dang MANG [{label:"A", text:"..."}], con cac tab dung
 * dang OBJECT {A:"...", B:"..."}. Chuan hoa ve object de moi tab doc duoc.
 * Chiu duoc ca hai kieu (neu sau nay JSON doi sang object thi tra nguyen).
 */
function normalizeOptions(options) {
  if (!options) return {};
  if (Array.isArray(options)) {
    const out = {};
    for (const o of options) {
      if (!o) continue;
      const label = String(o.label ?? o.letter ?? '').trim().toUpperCase();
      if (/^[A-D]$/.test(label)) out[label] = o.text ?? o.value ?? '';
    }
    return out;
  }
  if (typeof options === 'object') {
    const out = {};
    for (const [k, v] of Object.entries(options)) {
      const label = String(k).trim().toUpperCase();
      if (/^[A-D]$/.test(label)) out[label] = typeof v === 'string' ? v : v?.text ?? '';
    }
    return out;
  }
  return {};
}

/** Chuan hoa mot cau hoi: `number` -> `question_num`, `options` mang -> object. */
function normalizeQuestion(q) {
  if (!q || typeof q !== 'object') return null;
  const num = q.question_num ?? q.number ?? q.num;
  const stem = q.question ?? q.text ?? q.stem ?? '';
  return {
    ...q,
    question_num: Number(num),
    question: stem,
    /*
     * Tab 5 dung `item.sentence` lam de bai Part 5 (cau co cho trong), con
     * `item.question` lam de bai Part 3/4. OCR chi co mot truong — gan ca hai
     * de dung duoc o moi noi.
     */
    sentence: q.sentence ?? stem,
    options: normalizeOptions(q.options),
    answer: q.answer ?? null,
  };
}

/** Chuan hoa mot mang cau hoi, bo phan tu khong co so thu tu. */
function normalizeQuestionList(list) {
  if (!Array.isArray(list)) return [];
  return list.map(normalizeQuestion).filter((q) => q && Number.isFinite(q.question_num));
}

/**
 * Chuan hoa `pos` cua sach ve 4 khoa bucket: verb | noun | adjective | adverb.
 * Sach in tat ("n.", "v.", "adj.", "adv.") va JSON co the dung "noun"/"n".
 * Tra ve '' khi khong nhan dang duoc (KHONG doan bua o day).
 */
export function normalizePosKey(rawPos) {
  const pos = String(rawPos ?? '')
    .toLowerCase()
    .replace(/[.\s]/g, '')
    .trim();
  if (!pos) return '';
  if (pos.startsWith('adj')) return 'adjective';
  if (pos.startsWith('adv')) return 'adverb';
  if (pos.startsWith('n')) return 'noun';
  if (pos.startsWith('v')) return 'verb';
  return '';
}

/**
 * SUY RA tu loai tu hinh thoi khi sach/OCR khong in tu loai.
 *
 * CANH BAO TRUNG THUC: day la suy luan hinh thai, KHONG phai du lieu sach in.
 * Ham nay chi chay khi `pos` goc RONG; ket qua luon duoc danh dau
 * `pos_source: 'derived'` va UI hien nhan "(suy ra)".
 *
 * Thu tu xet quan trong: duoi `-ly` truoc (assuredly -> adverb), roi DANH TU
 * truoc TINH TU. Ly do: nhieu duoi danh tu cung khop voi duoi tinh tu
 * ("agreement" ket thuc bang "ent" nen neu xet tinh tu truoc se bi gan nham la
 * tinh tu). Cac duoi duoi day da duoc viet theo nhom khong chong lan.
 */
export function derivePos(word) {
  const w = String(word ?? '')
    .toLowerCase()
    .trim();
  if (!w || /\s/.test(w)) return ''; // cum nhieu tu (vd "abide by") -> khong doan.
  if (/ly$/.test(w)) return 'adverb';
  // Danh tu: -ment/-tion/-sion/-ance/-ence/-ity/-ness/-ship/-hood/-age
  // ("agreement" -> noun, "provider" -> noun, "cancellation" -> noun).
  // Them -ee (retiree), -eer (engineer), -ery (bakery) vi day la duoi danh tu ro.
  if (/(tion|sion|ment|ance|ence|ity|ness|ship|hood|age|ee|eer|ery)$/.test(w)) return 'noun';
  // -er/-or/-ist/-ian/-ant/-ent deu la duoi danh tu chi nguoi/vat
  // ("retiree"->-ee o tren, "inspector"->-or, "planner"->-er, "assistant"->-ant).
  if (/(er|or|ist|ian|ant|ent)$/.test(w)) return 'noun';
  // Tinh tu: -ous/-ful/-able/-ible/-ive/-al/-ic/-ish/-less, va -y nhu "happy".
  // Them -some (burdensome), -ary/-ory (necessary, mandatory).
  if (/(ous|ful|able|ible|ive|ical|al|ic|ish|less|some|ary|ory)$/.test(w)) return 'adjective';
  if (/(ed|ing|ate|ify|ise|ize|s)$/.test(w)) return 'verb';
  // -y nhu "happy" la tinh tu, nhung "-ify" da bat o tren nen khong bi nuot.
  if (/y$/.test(w) && w.length > 3) return 'adjective';
  /*
   * Mac dinh: dong tu. Cac ho tu trong sach luon xoay quanh dong tu goc
   * (agree/assure/cancel/obligate/provide/specify), nen day la phong doan tot
   * nhat — va da duoc danh dau ro la suy ra.
   */
  return 'verb';
}

/**
 * FAMILIES — chuan hoa MOI hinh dang word family ve MOT dang dong nhat:
 *
 *   { pos: string, word: string, example: string, root: string, pos_source: 'book'|'derived'|'', group: number }
 *
 * JSON do OCR sinh ra (scripts/run_mineru_local.py) dat ho tu o CAP BAI HOC va
 * boc moi nhom trong mot object long nhau:
 *
 *   "word_families": [ [ {word,example}, {word,example} ],          // mang long
 *                      { value: [ {word,example} ], Count: 3 },     // group object
 *                      { word, example },                           // dong phang
 *                      { root:"agree", pos:"", members:[...] } ]    // root + members
 *
 * Trong khi moi tab lai mong mot MANG PHANG cac dong {pos,word,example} va loc
 * bang `f.word`. Group object khong co `.word` nen truoc day bo loc luon tra ve
 * [] — bang ho tu hien toan dau gach ngang. Ham nay gom het cac dang ve mot
 * mang phang duy nhat; KHONG bao gio bia them dong nao.
 *
 * BAN QUYEN DU LIEU (pos_source):
 *   'book'    — `pos` co san trong JSON (sach in ro tu loai).
 *   'derived' — `pos` RONG trong JSON (OCR khong tach duoc tu loai); gia tri
 *               duoc SUY RA tu hinh thai cua chinh tu do (xem derivePos) de
 *               bang Verb/Noun/Adj/Adv co ich. Day la suy luan, KHONG phai
 *               du lieu sach in -> UI phai danh dau, khong duoc trinh bay nhu
 *               su that trong sach.
 *   'book-word' — nhu 'book', nhung lay tu TU MUC TIEU cua bai (xem `wordPos`).
 *   ''        — khong co pos va khong suy ra duoc (UI hien dau —, dung nhu sach).
 *
 * @param {unknown} input
 * @param {Record<string,string>} [wordPos] Ban do {tu thuong: pos da chuan hoa}
 *   cua cac TU MUC TIEU trong bai, do sach in ro (vd {"access":"noun"}).
 *   Dung de tranh suy dien sai voi tu dong dang danh/dong (zero-derivation).
 * @returns {{pos:string, word:string, example:string, root:string, pos_source:'book'|'book-word'|'derived'|'', group:number}[]}
 */
export function normalizeFamilyRows(input, wordPos) {
  const rows = [];
  const seen = new Set();
  /** So thu tu nhom goc trong sach (bat dau tu 1). */
  let groupNo = 0;

  const pushRow = (word, example, rawPos, root, grp) => {
    const w = String(word ?? '').trim();
    if (!w) return; // dong khong co `word` la du lieu rac -> bo qua (khong bia).
    const key = `${w.toLowerCase()}|${String(example ?? '').trim()}`;
    if (seen.has(key)) return; // cung mot dong xuat hien o ca 2 dang -> giu 1.
    seen.add(key);

    /*
     * Thu tu uu tien (tu chac chan nhat den suy dien nhat):
     *
     * 1. `pos` ghi ngay tren dong ho tu — sach in ro nhat.
     * 2. `pos` cua CHINH TU DO khi no la tu muc tieu cua bai (wordPos).
     *
     * Vi sao can buoc 2: tieng Anh co hien tuong "zero-derivation" — danh tu va
     * dong tu thuong DONG DANG (access, code, duplicate, refund, schedule,
     * record, delay...). Hinh thai hoc KHONG the phan biet, nen derivePos()
     * truoc day doan bua va dat sai cot. Do tren du lieu that: trong 122 dong
     * co the doi chieu voi sach, 31 dong (25%) bi dat SAI COT vi ly do nay.
     * Khi tu do da la tu muc tieu thi sach DA in ro tu loai cua no -> dung
     * luon, khong doan nua.
     *
     * 3. Cuoi cung moi suy ra tu hinh thai (co danh dau 'derived' de UI noi ro).
     */
    const bookPos = normalizePosKey(rawPos);
    const wordBookPos = wordPos ? wordPos[w.toLowerCase()] || '' : '';
    const derived = derivePos(w);
    const pos = bookPos || wordBookPos || derived;
    rows.push({
      pos,
      word: w,
      example: String(example ?? '').trim(),
      // `root` = tu goc cua nhom (tu khoa trong bai). Day la truong MOI giup
      // ghep ho tu voi tu muc tieu bang goc tu thay vi so khop tien to 4 ky tu.
      root: String(root ?? '').trim(),
      pos_source: bookPos ? 'book' : wordBookPos ? 'book-word' : derived ? 'derived' : '',
      // Chi so nhom goc (1-based) — giu ranh gioi nhom cua sach qua mang phang.
      group: grp || groupNo || 1,
    });
  };

  /**
   * @param {unknown} node
   * @param {{root:string, pos:string, group:boolean, groupNo:number, assigned:boolean}} ctx
   */
  const visit = (node, ctx) => {
    if (node == null) return;

    if (Array.isArray(node)) {
      /*
       * MOT mang la "danh sach nhom" khi cac phan tu cua no KHONG phai dong ho
       * tu (chung la mang con hoac group object {value:[]}). Khi do MOI phan tu
       * la mot nhom rieng cua sach -> tang chi so nhom truoc khi di xuong.
       *
       * Nguoc lai, mang cac dong phang ({word,example}) la danh sach dong, khong
       * phai danh sach nhom — di xuong ma khong tao nhom moi.
       */
      const isRowList = node.every(
        (c) => c && typeof c === 'object' && !Array.isArray(c) && c.word != null && !c.value,
      );
      if (isRowList) {
        for (const child of node) visit(child, ctx);
        return;
      }
      /*
       * Mang long nhieu tang (mang cua cac mang dong): moi mang con la 1 nhom.
       * Chi tang groupNo khi phan tu THAT SU la mot nhom (mang, hoac object co
       * mang con), de khong tao nhom rong cho du lieu rac.
       */
      for (const child of node) {
        const isGroup =
          Array.isArray(child) ||
          (child &&
            typeof child === 'object' &&
            (Array.isArray(child.value) ||
              Array.isArray(child.members) ||
              Array.isArray(child.words) ||
              Array.isArray(child.forms) ||
              Array.isArray(child.rows)));
        if (isGroup) groupNo += 1;
        // `assigned: true` — node nay da duoc cap nhom o day, khong cap lai.
        visit(child, { ...ctx, groupNo: groupNo || 1, assigned: isGroup });
      }
      return;
    }
    /*
     * Chuoi: OCR doi khi tra ve ["agree","agreement"] — chi la danh sach tu,
     * khong co cau vi du. Van la du lieu that trong sach nen giu lai.
     */
    if (typeof node === 'string') {
      pushRow(node, '', ctx.pos, ctx.root, ctx.groupNo);
      return;
    }
    if (typeof node !== 'object') return;

    // Group object {value:[...]} hoac {members:[...]/words:[...]/forms:[...]}.
    const nested =
      (Array.isArray(node.value) && node.value) ||
      (Array.isArray(node.members) && node.members) ||
      (Array.isArray(node.words) && node.words) ||
      (Array.isArray(node.forms) && node.forms) ||
      (Array.isArray(node.rows) && node.rows) ||
      null;

    // Goc cua nhom: `root`/`base`/`headword`/`key`/`word_family` neu co.
    const groupRoot =
      String(node.root ?? node.base ?? node.headword ?? node.key ?? '').trim() ||
      // Mot so JSON cu boc nhom trong { word_family: "agree", value: [...] }.
      (nested && typeof node.word_family === 'string' ? String(node.word_family).trim() : '') ||
      ctx.root;

    const groupPos = String(node.pos ?? '').trim() || ctx.pos;

    if (nested) {
      /*
       * Mot node vua co `word` vua co mang con (vd {word:"agree", forms:[...]}):
       * ban than no cung la mot dong, va cac phan tu con thuoc cung nhom.
       * Chi cap nhom moi khi node nay CHUA duoc cap (tranh dem hai lan khi no
       * nam trong mot mang da tang groupNo).
       */
      const own = ctx.assigned ? ctx.groupNo : (groupNo += 1);
      if (node.word != null) {
        pushRow(node.word, node.example ?? node.sentence ?? '', groupPos, groupRoot, own);
      }
      for (const child of nested) {
        visit(child, { root: groupRoot, pos: groupPos, group: true, groupNo: own, assigned: true });
      }
      return;
    }

    // Dong phang {word, example, pos}.
    if (node.word != null) {
      pushRow(
        node.word,
        node.example ?? node.sentence ?? node.definition_en ?? '',
        groupPos,
        ctx.root || groupRoot,
        ctx.groupNo,
      );
      return;
    }

    /*
     * Object la khong nhan dang duoc (khong co `word`, khong co mang con):
     * thu gom MOI gia tri mang ben trong no thay vi bo qua ca cum.
     */
    for (const v of Object.values(node)) {
      if (Array.isArray(v)) {
        visit(v, {
          root: ctx.root,
          pos: ctx.pos,
          group: ctx.group,
          groupNo: ctx.groupNo,
          assigned: false,
        });
      }
    }
  };

  visit(input, { root: '', pos: '', group: false, groupNo: 0, assigned: false });
  return rows;
}

/**
 * GOM nhom cac dong phang theo TUNG NHOM GOC trong sach.
 *
 * Mang phang da mat ranh gioi nhom, nhung `normalizeFamilyRows` ghi lai chi so
 * nhom goc trong truong `group`, nen o day chi can gom lai theo chi so do —
 * dung thu tu xuat hien, khong suy dien them.
 *
 * @param {{group?:number, root?:string, word?:string}[]} rows
 * @returns {Array<Array<object>>}
 */
export function groupFamilyRows(rows) {
  const list = Array.isArray(rows) ? rows.filter((r) => r && r.word) : [];
  if (!list.length) return [];
  const map = new Map();
  for (const row of list) {
    // Uu tien chi so nhom goc; JSON cu khong co thi gom theo `root`.
    const key = Number.isFinite(row.group) ? `g${row.group}` : `r${row.root || row.word}`;
    if (!map.has(key)) map.set(key, []);
    map.get(key).push(row);
  }
  return [...map.values()];
}

/** Ghep ten tu goc voi mot dong ho tu (khong phan biet hoa/thuong, bo khoang trang). */
function familyMatchesRoot(entryWord, row) {
  const target = String(entryWord ?? '')
    .trim()
    .toLowerCase();
  if (!target) return false;
  const root = String(row?.root ?? '')
    .trim()
    .toLowerCase();
  if (root && root === target) return true;
  // JSON cu khong co `root`: chap nhan khi dong la chinh tu do.
  return !root && String(row?.word ?? '').trim().toLowerCase() === target;
}

/**
 * Ban do {tu thuong -> pos da chuan hoa} cua cac TU MUC TIEU trong bai.
 *
 * Dung de truyen vao normalizeFamilyRows: khi mot dong ho tu trung voi tu muc
 * tieu thi tu loai sach in cua tu do la CHAC CHAN, khong can suy dien hinh thai.
 * Tieng Anh co nhieu cap danh/dong tu dong dang (access, code, duplicate,
 * refund, schedule, record...) ma hinh thai hoc khong phan biet duoc.
 *
 * @param {any} lesson
 * @returns {Record<string,string>}
 */
export function lessonWordPos(lesson) {
  const map = {};
  const words = Array.isArray(lesson?.words_to_learn) ? lesson.words_to_learn : [];
  for (const w of words) {
    const key = String(w?.word ?? '').trim().toLowerCase();
    const pos = normalizePosKey(w?.pos);
    if (key && pos) map[key] = pos;
  }
  return map;
}

/**
 * Cac dong ho tu cua MOT tu muc tieu, gom tu ca hai nguon:
 *   1. `word_family` cua chinh entry (uu tien, da duoc chuan hoa);
 *   2. mang ho tu cap bai hoc, ghep theo `root` (hoac theo chinh ten tu).
 * Khong bao gio bia: khong co du lieu thi tra ve [] va UI hien dau —.
 *
 * @param {any} entry
 * @param {any} lesson
 * @returns {{pos:string, word:string, example:string, root:string, pos_source:string, group:number}[]}
 */
export function familiesForEntry(entry, lesson) {
  const wordPos = lessonWordPos(lesson);
  const own = normalizeFamilyRows(entry?.word_family, wordPos);
  if (own.length) return own;

  const bag = normalizeFamilyRows(
    Array.isArray(lesson?.word_family)
      ? lesson.word_family
      : Array.isArray(lesson?.word_families)
        ? lesson.word_families
        : [],
    wordPos,
  );
  return bag.filter((row) => familyMatchesRoot(entry?.word, row));
}

/**
 * Defensive normalisation: OCR output may omit optional branches or place
 * word families at lesson level. Fill gaps so tabs never crash.
 *
 * HO TU (word families) — dang chuan sau khi chuan hoa:
 *   lesson.word_families        : mang PHANG cac dong {pos, word, example, root, pos_source, group}
 *   lesson.word_families_groups : mang cac NHOM (moi nhom la mot mang dong)
 *   entry.word_family           : mang PHANG cac dong cua rieng tu do
 * Trong do:
 *   `root`       (MOI) = tu goc cua nhom (tu khoa trong bai), dung de ghep ho tu
 *                voi tu muc tieu thay cho so khop tien to 4 ky tu truoc day.
 *   `pos_source` (MOI) = 'book' khi `pos` co trong sach, 'derived' khi phai suy
 *                ra tu hinh thai (OCR khong tach duoc tu loai — 18/18 dong o
 *                bai 1 deu la 'derived'), '' khi khong xac dinh duoc.
 *   `group`      (MOI) = chi so nhom goc 1-based, giu ranh gioi nhom cua sach.
 * `pos` luon la mot trong 'verb'|'noun'|'adjective'|'adverb' hoac ''.
 *
 * QUAN TRONG — noi that su khac nhau giua JSON OCR va cac tab:
 *   OCR (scripts/run_mineru_local.py)          Tab (app/src/tabs/*)
 *   ----------------------------------------   ------------------------------
 *   listening  o CAP CAO NHAT                  practice.listening.part1..part4
 *   practice.part5 / part6 / part7             practice.reading.part5/6/7
 *   options dang [{label,text}]                options dang {A:"...", B:"..."}
 *   question: {number, question, options}      {question_num, ...}
 *
 * Truoc day loader chi doc practice.listening/practice.reading nen TOAN BO
 * phan Listening va Part 5-7 khong hien ra du JSON co du. Ham nay lam ca hai
 * kieu deu doc duoc.
 */
function normalizeLesson(result) {
  const lesson = result.lesson;
  const out = { ...lesson };

  /*
   * HO TU — MOT mang phang duy nhat cho ca bai, da chuan hoa tu MOI hinh dang
   * (mang long / group object {value:[]} / dong phang / {root,members}).
   * `out.word_families` la nguon chinh thuc ma cac tab doc; dong thoi giu
   * `word_families_groups` (mang cac nhom) cho phan "nguyen trang sach".
   */
  // Ban do pos cua cac tu muc tieu (sach in ro) — dung de khong suy dien sai
  // voi tu dong dang danh/dong (zero-derivation).
  const wordPos = lessonWordPos(lesson);
  const familyRows = normalizeFamilyRows(lesson.word_families, wordPos);
  // Mang phang chinh thuc ma moi tab doc (giu nguyen `group` de biet nhom goc).
  out.word_families = familyRows;
  // Cung du lieu nhung gom theo nhom goc — cho section "nguyen trang sach".
  out.word_families_groups = groupFamilyRows(familyRows);

  out.words_to_learn = (lesson.words_to_learn || []).map((w, i) => ({
    ...w,
    id: w.id ?? i + 1,
    word: w.word ?? '',
    pos: w.pos ?? '',
    ipa: w.ipa ?? '',
    definition_en: w.definition_en ?? '',
    definition_vi: w.definition_vi ?? '',
    collocations: Array.isArray(w.collocations) ? w.collocations : [],
    usage: w.usage && typeof w.usage === 'object' ? w.usage : null,
    extra_families: Array.isArray(w.extra_families) ? w.extra_families : [],
    srs_sentence: w.srs_sentence && typeof w.srs_sentence === 'object' ? w.srs_sentence : null,
    examples: Array.isArray(w.examples) ? w.examples : [],
    // Uu tien ho tu cua chinh entry; neu rong thi lay tu mang cap bai hoc da
    // chuan hoa, ghep theo `root`. Khong bao gio bia them dong.
    word_family: (() => {
      const own = normalizeFamilyRows(w.word_family, wordPos);
      if (own.length) return own;
      return familyRows.filter((row) => familyMatchesRoot(w.word, row));
    })(),
  }));

  out.words_in_context = {
    word_bank: lesson.words_in_context?.word_bank || [],
    passage: lesson.words_in_context?.passage || '',
    answers: lesson.words_in_context?.answers || {},
  };

  const practice = lesson.practice || {};
  /*
   * `listening` nam o CAP CAO NHAT trong JSON do OCR sinh ra
   * (build_lesson() dat top-level: listening.questions / .tapescript / .parts).
   * Van doc them practice.listening de chiu duoc ca hai kieu du lieu.
   */
  const rawListening = lesson.listening || practice.listening || {};
  const rawReading = practice.reading || practice;
  const rawParts = Array.isArray(rawListening.parts) ? rawListening.parts : [];

  // 6 cau hoi cua sach danh so 4..9: Part 3 = 4-6, Part 4 = 7-9.
  // Neu JSON da tach san part3/part4 thi dung luon; neu khong thi tach theo so.
  const flatListening = normalizeQuestionList(rawListening.questions);
  const hasSplitParts =
    Array.isArray(rawListening.part3) || Array.isArray(rawListening.part4);

  const listeningPart3 = hasSplitParts
    ? normalizeQuestionList(rawListening.part3)
    : flatListening.filter((q) => q.question_num >= 4 && q.question_num <= 6);
  const listeningPart4 = hasSplitParts
    ? normalizeQuestionList(rawListening.part4)
    : flatListening.filter((q) => q.question_num >= 7 && q.question_num <= 9);

  out.practice = {
    listening: {
      part1: rawListening.part1 || null,
      part2: hasSplitParts
        ? normalizeQuestionList(rawListening.part2)
        : normalizeQuestionList(rawListening.part2),
      part3: listeningPart3,
      part4: listeningPart4,
      // Giu lai phan mo ta Part 1-4 de Tab 5 hien tieu de dung sach.
      parts: rawParts,
      // Phan chu HUONG DAN tren trang luyen nghe (khong phai tapescript sach).
      instructions: rawListening.instructions ?? '',
    },
    reading: {
      part5: normalizeQuestionList(rawReading.part5 || lesson.part5),
      part6: (() => {
        const p6 = rawReading.part6;
        if (!p6 || (Array.isArray(p6) && p6.length === 0)) return null;
        if (Array.isArray(p6)) {
          return { passage: '', questions: normalizeQuestionList(p6) };
        }
        return {
          passage: typeof p6.passage === 'string' ? p6.passage : '',
          questions: normalizeQuestionList(p6.questions),
        };
      })(),
      part7: (() => {
        const p7 = rawReading.part7 ?? lesson.part7 ?? null;
        if (!p7) return { passages: [], questions: [] };
        /*
         * PassageDocument cua Tab 5 doc `passage.header` / `passage.body`, con
         * OCR tra ve mot truong `text` duy nhat. Do toan bo van ban vao `body`
         * de tai lieu hien ra; `header` de trong (khong don giang tach thu tuc).
         */
        const toDoc = (seg) => ({
          type: seg?.type ?? 'reading',
          header: '',
          body: typeof seg?.text === 'string' ? seg.text : '',
        });
        if (Array.isArray(p7)) {
          return {
            passages: p7.map(toDoc),
            questions: normalizeQuestionList(
              p7.flatMap((seg) => (Array.isArray(seg?.questions) ? seg.questions : [])),
            ),
          };
        }
        return {
          passages: Array.isArray(p7.passages)
            ? p7.passages.map((p) =>
                typeof p === 'string' || p?.body || p?.text
                  ? toDoc(typeof p === 'string' ? { text: p } : p)
                  : p,
              )
            : [],
          questions: normalizeQuestionList(p7.questions),
        };
      })(),
    },
  };

  // Tapescript co the nam o cap cao nhat hoac trong practice.
  out.practice.tapescript = lesson.tapescript ?? practice.tapescript ?? null;

  return { ...result, lesson: out };
}

export default loadLesson;
