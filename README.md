# 600 Essential Words for the TOEIC — Local Web App

> **Agent mới vào dự án: đọc [`ONBOARDING.md`](ONBOARDING.md) TRƯỚC.**
> File đó là bức tranh toàn cảnh (kiến trúc, shape dữ liệu thực tế, các bẫy đã
> từng sập, checklist trước khi báo xong). README này là hướng dẫn vận hành
> pipeline OCR; `app/CONTRACT.md` là hợp đồng interface.

Ứng dụng web chạy **local** để học 600 từ vựng thiết yếu TOEIC theo phương pháp
**Context-First** (ngữ cảnh trước), dựng từ cuốn *Barron's 600 Essential Words for
the TOEIC (3rd Edition)*.

---

## Chạy ứng dụng

```powershell
cd D:\LEGION\Documents\deepseek-harness\TiengAnh\app
npm install
npm run dev            # mở http://127.0.0.1:5173
```

> **Nếu `npm run dev` / `npm run build` báo `spawn EPERM`:** đây là giới hạn sandbox
> (Vite gọi `child_process.exec` để nạp config, mà sandbox chặn piped stdio). Dùng
> script tương đương không qua config loader:
> ```powershell
> npm run dev:sandbox     # node scripts/dev-server.mjs
> npm run build:sandbox   # node scripts/build.mjs
> ```

### Kiểm thử tự động

```powershell
cd app
node scripts/verify_runtime.mjs   # 20 kiểm tra: HTTP endpoint + asset
node scripts/verify_loader.mjs    # 27 kiểm tra: loader + trạng thái "Chưa trích xuất"
node scripts/verify_tabs.mjs      # 15 kiểm tra: render cả 5 tab (có/không có dữ liệu)
node scripts/lead_e2e_check.mjs   # 25 kiểm tra: end-to-end
node scripts/verify_explanations.mjs  # 15 kiểm tra: đáp án + giải thích
cd .. && node scripts/check_helpers.mjs   # highlight + cloze + dữ liệu bài 1

# Tầng dữ liệu (repo root)
py -3.11 scripts/test_parse_listening.py    # 335
py -3.11 scripts/test_answer_key.py         # 56
py -3.11 scripts/test_tapescripts.py        # 57
py -3.11 scripts/validate_explanations.py   # 7 — chất lượng giải thích
py -3.11 scripts/verify_onboarding.py       # 101 — tài liệu khớp thực tế
py -3.11 scripts/coverage_report.py         # báo cáo độ phủ đáp án
```

---

## Kiến trúc

```
TiengAnh/
├─ app/                          # React 19 + Vite 8 + Tailwind v4
│  ├─ CONTRACT.md                # hợp đồng dữ liệu & API dùng chung (đọc trước khi sửa)
│  ├─ src/
│  │  ├─ App.jsx                 # khung: sidebar + header + 5 tab
│  │  ├─ data/curriculum.js      # 10 chủ đề → 50 bài + 10 Word Review
│  │  ├─ lib/
│  │  │  ├─ types.js             # typedef + LESSON_STATUS
│  │  │  ├─ assets.js            # URL, highlight, cloze, chia dạng từ
│  │  │  ├─ lessonLoader.js      # nạp động lesson_XX.json
│  │  │  ├─ storage.js           # LocalStorage: tiến độ, SRS, cài đặt, lịch sử
│  │  │  ├─ srs.js               # thuật toán SM-2 (4 mức đánh giá)
│  │  │  └─ store.jsx            # AppProvider + useApp()
│  │  └─ tabs/Tab1..Tab5.jsx     # 5 tab chức năng
│  └─ scripts/                   # dev/build/verify không cần config loader
├─ public/                       # tài nguyên web (sinh bởi scripts/normalize_assets.py)
│  ├─ audio/track_01..50.mp3     # 50 track, đã chuẩn hoá sang MP3
│  ├─ part1_photos/lesson_01..50.jpg
│  ├─ lessons_json/              # đầu ra OCR (nguồn chính)
│  └─ sample_lessons/lesson_01.json
├─ audio/  part1_photos/  sample_lessons/  lessons_json/   # dữ liệu gốc
└─ scripts/                      # pipeline OCR + tiện ích
```

### Cơ chế nạp dữ liệu động

`lessonLoader.js` thử theo thứ tự:

1. `/lessons_json/lesson_NN.json` — đầu ra OCR (nguồn chính)
2. `/sample_lessons/lesson_NN.json` — bản mẫu đi kèm (chỉ có bài 01)
3. → trạng thái **"Chưa trích xuất"** (sidebar hiện nhãn vàng, nội dung tab hiện thông báo)

> **Lưu ý kỹ thuật quan trọng:** Vite (và hầu hết SPA host) trả về `index.html` kèm
> HTTP **200** cho tệp JSON không tồn tại, *không phải* 404. Loader kiểm tra
> `content-type` và chặn fallback HTML trước khi gọi `.json()`, nếu không sẽ lỗi
> `Unexpected token '<'` thay vì hiện đúng "Chưa trích xuất".

---

## 5 Tab chức năng

| Tab | Nội dung |
|---|---|
| **1. Học Từ Vựng** | 12 card: từ, `pos`, IPA, phát âm giọng Mỹ (Web Speech API), nghĩa EN/VI, collocations, **2 câu ví dụ a/b** (in đậm từ mục tiêu, ẩn/hiện dịch), **bảng Word Family** Verb/Noun/Adj/Adv kèm ví dụ gốc. Lọc đã/chưa học. |
| **2. Flashcard Ngữ Cảnh** | Mặt trước: từ + câu ví dụ trong sách **đã đục lỗ** từ mục tiêu. Mặt sau: nghĩa EN/VI, câu đầy đủ + dịch, collocations, Word Family. Lật 3D, `Space` để lật, `1-2-3-4` để chấm mức nhớ. |
| **3. Ôn Tập Giãn Cách** | SM-2. *Chế độ 1*: đoạn văn 12 chỗ trống + word bank, chấm điểm. *Chế độ 2*: gõ từ đúng chính tả & đúng dạng từ loại, gợi ý bằng nghĩa tiếng Việt. |
| **4. AI Sentence Lab** | BYOK (Gemini / OpenAI / Ollama). AI sinh câu tiếng Việt văn phong công sở + gợi ý collocation → người học dịch → AI chấm thang 10, sửa ngữ pháp, gợi ý 2 cách diễn đạt Business English. |
| **5. Luyện Đề & Audio** | Sticky audio player (tua ±5s, tốc độ 0.8–1.5x, tapescript). Listening Part 1–4 (câu 1–9, Part 1 có ảnh, Part 2 ẩn text tới khi nộp). Reading Part 5–7 (câu 10–23, Part 7 split-screen). Chấm điểm + highlight từ mục tiêu. |

---

## Nguyên tắc Context-First

Mọi từ vựng hiển thị trên UI **luôn** đi kèm câu ví dụ thực tế trong sách, cụm từ
đi kèm (collocations) và bảng gia đình từ. Không có từ nào hiển thị đơn lẻ.

`lib/assets.js` xử lý việc in đậm/đục lỗ từ mục tiêu và đã được kiểm thử với:

- **Biến thể hình thái:** `obligate→obligates/obligated/obligating`,
  `specify→specifies/specified/specifying/specification`, `party→parties`,
  `submit→submitted/submitting`, `cancel→canceled/cancelled` (cả Anh-Mỹ và Anh-Anh)
- **Cụm nhiều từ:** `abide by → abided by` (chia ở từ đầu, không phải "abide bying")
- **Từ ghép gạch nối:** `self-assurance` được tính là `assurance`
- **Ranh giới từ:** `part` KHÔNG khớp trong `party`/`particular`; `form` không khớp
  trong `information`/`performance`

Dùng `containsWord(text, words)` cho câu hỏi đúng/sai. **Không** dùng
`buildWordRegex(...).test()` trực tiếp — regex có cờ `g` nên có trạng thái
(`lastIndex`), gọi liên tiếp sẽ trả về sai.

---

## Tài nguyên

- **Âm thanh:** `audio/` chứa 25 tệp `.wma` (Track 1–25) và 25 tệp `.mp3` (Track 26–50).
  WMA **không phát được trên trình duyệt**, nên `scripts/normalize_assets.py` đã
  chuyển 25 tệp WMA sang MP3 (ffmpeg, libmp3lame) và xuất tất cả 50 track ra
  `public/audio/track_XX.mp3` theo tên chuẩn.
- **Ảnh:** 50 ảnh Part 1 Photo đã copy sang `public/part1_photos/lesson_XX.jpg`.

---

## Pipeline OCR (49 bài còn lại)

> **Trạng thái hiện tại:** Bước 1 (trích xuất PDF) **đã chạy xong** — 50 bài × 6 trang
> ảnh sắc nét nằm trong `extracted_data/lesson_page_scans/`, đã kiểm tra bằng mắt và
> khớp chính xác với `lesson_01.json`. Bước OCR (sinh `lessons_json/lesson_NN.json`)
> bạn tự chạy.

### Bước 1 — Trích xuất ảnh/scan từ PDF (đã xong)

```powershell
python scripts\extract_pdf_assets.py
```

Cần `pypdf` và `pillow`.

### Bước 2 — OCR, chọn 1 trong 2 hướng

**Hướng 1 — Gemini API** (nhẹ, không cần GPU):

```powershell
$env:GEMINI_API_KEY="..."
python scripts/run_ocr_pipeline.py --stage ocr --provider gemini --from 2
```

**Hướng 2 — MinerU local** (miễn phí, offline, dùng RTX 4060):

> **Trạng thái: đã chạy xong cả 50 bài.** Web đã có đủ dữ liệu; phần dưới chỉ cần
> khi muốn OCR lại hoặc thêm bài mới.

MinerU đã được cài sẵn tại `D:\CODE\vibecode\TOOL\mineru` (xem README riêng của
bản cài đó). Repo này có sẵn script nối thẳng vào bản cài đó:

```bat
scripts\RUN_MINERU_OCR.bat --only 2      :: chạy thử 1 bài
scripts\RUN_MINERU_OCR.bat --from 40     :: chạy từ bài 40 (dùng khi bị dừng giữa)
scripts\RUN_MINERU_OCR.bat --convert-only :: chỉ đổi .md có sẵn -> JSON
```

**Nhấp đôi vào file `.bat`** (hoặc mở `cmd` rồi gọi). Không cần Admin.

Nó tự nạp môi trường MinerU, OCR 6 trang mỗi bài ra Markdown
(`extracted_data/mineru_md/lesson_NN/`), đổi sang JSON đúng schema app đọc
(`lessons_json/lesson_NN.json`), rồi copy sang `public/lessons_json/`.

Nếu bị dừng giữa chừng (máy ngủ, đóng cửa sổ), bài đang OCR dở sẽ chỉ có vài
trang — chạy lại đúng bài đó bằng `--only NN` hoặc `--from NN`. Bài đã xong được
bỏ qua, không OCR lại từ đầu.

> **Vì sao phải tự nhấp đôi, không để agent chạy:** MinerU render PDF qua
> `multiprocessing.Pipe` (named pipe). Sandbox của DSH chặn named pipe, nên mọi
> lần parse đều chết với `PermissionError: [WinError 5] Access is denied` —
> hoặc ở `home\models\.locks\...` (sandbox không cho ghi ra ngoài workspace),
> hoặc ngay tại `multiprocessing/connection.py::Pipe`.
>
> Đây là **giới hạn của sandbox**, không phải lỗi bản cài. Đã kiểm chứng: ngay cả
> `python -c "import multiprocessing as m; m.Pipe()"` cũng bị chặn. Chạy từ shell
> bình thường của bạn thì không gặp gì.

Sau khi OCR xong, quay lại web app bấm **"Quét lại"** ở sidebar.

### Kết quả OCR đã kiểm chứng

**Cả 50 bài đã OCR xong và vào web.** Đối chiếu bài 1 với `sample_lessons/lesson_01.json`
(bản chuẩn):

| Hạng mục | Bản chuẩn | OCR ra |
|---|---|---|
| Số từ | 12 | **12** |
| Câu ví dụ | 24 | **24** |
| Dòng word-family | 18 | **18** |
| Word bank | 12 | **12** |
| Chỗ trống (1)..(12) | 12 | **12** |

Danh sách từ khớp **chính xác từng từ**. `word_families` giữ được cả 6 nhóm
(`agree/agreement/agreeable`, …) kèm câu ví dụ.

Toàn sách: **599/600 từ**, 1195 câu ví dụ, 883 dòng word-family.

| Mức | Số bài |
|---|---|
| Đạt chuẩn đầy đủ (12 từ · 24 ví dụ · 18 fam · 12 bank · 12 chỗ trống) | **37/50** |
| Thiếu một phần do MinerU đọc sót (xem bên dưới) | 13 |

**Sách này có nhiều kiểu trình bày khác nhau, và MinerU trả về mỗi trang một kiểu.**
Script đã xử lý hết (đây là những chỗ từng làm mất dữ liệu):

| Kiểu trình bày | Xử lý |
|---|---|
| Word-family bảng HTML 2 cột | nhận cột 1 = từ |
| Word-family bảng HTML 3 cột (có cột từ loại) | nhận cột 2 = từ (cột 1 là `√b`, `a)`, `r)` — rác OCR) |
| Word-family bảng Markdown, có/không cột từ loại | như trên |
| **Một trang trộn cả bảng Markdown lẫn `<table>` HTML** | đọc cả hai rồi ghép theo đúng thứ tự xuất hiện (bài 6, 8) |
| **18 dòng fam không có dòng trống giữa các nhóm** | tách nhóm theo **gốc từ** (bài 46: 108 dòng → 18/6 nhóm) |
| Word bank trong bảng Markdown | đọc theo ô |
| **Word bank tách/gộp sai ranh giới cụm** | căn theo **12 từ mục tiêu** bằng quy hoạch động (bài 7, 11, 12, 15, 33) |
| Mục từ thiếu dấu chấm: `7 failure n., …` | nhận cả `7.` và `7 ` |
| MinerU gộp `a.` và `b.` cùng dòng | tách theo vị trí ` b. ` |
| Cùng một mục từ bị OCR lặp, khác hoa/thường | gộp lại (bài 33: `individual` + `Individual`) |
| Từ gốc 3 ký tự (`opt`) không khớp nhóm | hạ ngưỡng so khớp gốc từ xuống ≥3, mỗi nhóm chỉ gán cho 1 từ |
| Câu hỏi Part 3/4 nằm rải nhiều dòng | gom theo số thứ tự rồi hút các dòng `(A)…(D)` |
| Ảnh nhúng base64 (30–55 KB/trang) | bỏ tự động trong `convert()`, giữ nguyên chữ |

### Lỗi tích hợp đã sửa (dữ liệu có mà UI không thấy)

Bốn lỗi "lệch hợp đồng" giữa JSON OCR và các tab — dữ liệu nằm đúng trong file
nhưng tab đọc nhầm vị trí/dạng, nên gần như toàn bộ phần luyện đề không hiện:

| Lỗi | Hậu quả trước đây | Sửa ở |
|---|---|---|
| JSON đặt `listening` ở cấp cao nhất, tab đọc `practice.listening` | 78 câu Part 3/4 biến mất | `normalizeLesson()` đọc cả hai vị trí |
| JSON đặt `practice.part5/6/7`, tab đọc `practice.reading.*` | Part 5/7 biến mất | như trên |
| JSON trả `options` dạng mảng `[{label,text}]`, tab cần `{A:...}` | mọi lựa chọn trống | `normalizeOptions()` |
| Tab đọc `item.sentence` làm đề Part 5, JSON chỉ có `question` | đề bài Part 5 trống chữ | loader gán cả hai tên |
| Tab đọc `passage.header`/`passage.body`, JSON chỉ có `text` | tài liệu Part 7 "(Trống)" | loader đổ vào `body` |
| `parse_part6()` không tồn tại — sách in Part 6 ngay trên trang Part 5 | **149 câu Part 6 + đoạn văn biến mất** | parser mới đọc cả 3 kiểu layout (2 cột, 1 dòng, cột trộn) |
| `parse_part7()` bỏ hết câu hỏi | 0 câu Part 7 dù md có đầy đủ | parser đọc câu hỏi + tách khỏi đoạn văn |
| `tapescript` bị gán nhầm phần hướng dẫn | người học tưởng đã có lời thoại | để trống trung thực (tapescript thật ở trang 341–373) |

Sau khi sửa, Tab 5 hiển thị đầy đủ: 39 Part 3 + 39 Part 4 + 299 Part 5 +
**149 Part 6** + 220 Part 7 (Part 1 luôn hiện ảnh + 4 nút A/B/C/D tự chấm;
Part 2 dự phòng từ audio). Các kiểm thử trong `app/scripts/verify_loader.mjs`
(27 check) khoá cứng những lỗi này.

### Word Families — đúng như sách in

Sách chỉ in bảng họ từ cho **một phần** các từ mục tiêu (bài 1: 6/12 từ có họ
từ, tổng 18 dòng) — dữ liệu OCR khớp **100%** với bản chuẩn `lesson_01.json`,
không phải lỗi thiếu. Để người học xem được nguyên bảng như trong sách, Tab 1
có thêm mục **"Bảng Word Families — nguyên trang sách"**: render đủ 6 nhóm kèm
câu ví dụ, không bịa thêm dòng nào.

### OCR bổ sung bằng Windows OCR (không cần GPU)

37/50 trang Listening Practice bị MinerU trả về **rỗng** (trang nhiều ảnh, VLM
không OCR được chữ) — nên chỉ 13 bài có câu hỏi Part 3/4. PDF gốc là sách scan
thuần (không có lớp chữ), nên bắt buộc phải OCR. MinerU không chạy được trong
sandbox, nhưng **Windows OCR (WinRT) có sẵn trên máy** và chạy được từ shell
thường của bạn:

```
scripts\RUN_WINOCR.bat        <- nhấp đôi; ~2 giay/trang
```

Script tự OCR 3 nhóm trang còn thiếu:

| Nhóm | Số trang | Kết quả |
|---|---|---|
| Listening Practice (37 bài MinerU bỏ trống) | 37 | câu hỏi Part 3/4 cho mọi bài |
| Answer Key (trang 333–336) | 4 | đáp án tự chấm cho toàn sách |
| Listening Tapescripts (trang 341–373) | 33 | lời thoại thật của bài nghe |

Chạy xong, quay lại báo agent chạy `py -3.11 scripts\convert_available_lessons.py`
để nạp dữ liệu mới vào web.

### Word Review theo chủ đề

Nút "Word Review 1..10" trên sidebar trước đây là nút chết (chỉ đổi tab của bài
đang mở). Giờ nó mở **trang ôn tập gộp** của cả chủ đề:

- Gộp 60 từ của 5 bài (giữ nguyên câu ví dụ trong sách — Context-First).
- Thanh tiến độ thuộc bài của cả chủ đề (đếm từ đã đánh dấu ở từng bài).
- Từng từ: đánh dấu đã thuộc, phát âm US-English, và nút "Mở bài →" quay về
  đúng bài gốc để học sâu với SRS/Flashcard/AI Lab.
- Bài nào OCR đọc sót từ thì hiện ghi chú trung thực, không bịa.

### 13 bài MinerU đọc sót (và cách xử lý)

Đây là **mất mát thật của OCR**, không phải lỗi parser — đã đối chiếu từng bài với
Markdown gốc. Script **không bịa** phần thiếu.

| Bài | Thiếu gì | Ghi chú |
|---|---|---|
| 15 | mục từ #3 (`dedicate`) — mất cả tiêu đề lẫn 2 ví dụ | không thể khôi phục |
| 31 | mục từ #10 (`secure`) — mất tiêu đề, **còn 2 ví dụ** | **đã khôi phục**, định nghĩa để trống |
| 20 | 1 ví dụ của `scan` (mục `b.`) | — |
| 21, 22, 24, 27, 33, 36, 37, 39 | word-family 15–17 dòng thay vì 18 | nhóm 2 dòng hoặc mất 1 dòng |
| 41 | đoạn văn chứa chỗ trống (2)(3) | passage nhảy (1) → (4) |
| 45 | đoạn văn chứa chỗ trống (4) | passage nhảy (3) → (5) |

Riêng bài 31 khôi phục được vì 2 câu ví dụ của `secure` vẫn còn nguyên trong
`words_to_learn.md`, chỉ mất dòng tiêu đề:

```json
{ "word": "secure", "definition_en": "", "needs_review": true,
  "recovered_from": "extracted_data/mineru_md/lesson_31/words_to_learn.md" }
```

Các bài còn lại được đánh dấu trong bảng kiểm tra chất lượng để người đọc biết
chính xác bài nào cần đối chiếu ảnh scan.

### Khi nào cần xem lại bằng mắt

Script **không đoán bừa**. Nếu phải gộp cụm từ mà không khớp khuôn nào, hoặc số
mục word bank khác số chỗ trống, trường `words_in_context.bank_certain` được đặt
`false`. Cách kiểm tra nhanh:

```powershell
python -c "import json,glob; [print(p, json.load(open(p,encoding='utf-8'))['words_in_context'].get('bank_certain')) for p in sorted(glob.glob('lessons_json/*.json'))]"
```

Mọi bài in ra `True` nghĩa là word bank khớp đúng số chỗ trống.

**Nhưng `bank_certain` không bắt được mọi thứ.** MinerU có lần **bỏ nguyên một
nhóm word-family 3 dòng** mà không hề báo lỗi — JSON vẫn hợp lệ, chỉ thiếu dòng.
Cách duy nhất phát hiện là so với số mong đợi. `convert_available_lessons.py`
làm việc đó và in bảng kiểm tra sau khi sinh JSON:

```
Bai     Tu   ViDu   Fam  Bank  Trong  P5  Tinh trang
L01     12     24    18    12     12   6  OK
L08     12     24    18    12     12   6  OK
L15     11     22    15    12     12   6  11 tu (mong doi 12); ...
```

Chuẩn đối chiếu: **12 từ · 24 ví dụ · 18 dòng word-family · 12 word bank ·
12 chỗ trống**. Bài nào lệch sẽ hiện cảnh báo kèm số cụ thể.

### Vá dữ liệu MinerU bỏ sót

Bài 8 bị MinerU bỏ nhóm `expose / exposure / exposed`. Dữ liệu này được đọc lại
từ chính ảnh scan (`extracted_data/lesson_page_scans/lesson_08/059_word_families.png`)
và ghi vào `scripts/patch_missing.py`.

```powershell
python scripts\patch_missing.py --dry-run   # xem sẽ vá gì
python scripts\patch_missing.py            # vá + publish
```

`convert_available_lessons.py` **tự gọi** phần vá này sau mỗi lần sinh JSON, vì
`convert()` luôn ghi lại từ Markdown nên nếu không vá ở đó thì bản vá sẽ mất.
Muốn thêm bản vá mới: mở ảnh scan, đọc, rồi thêm vào dict `PATCHES` — **ghi rõ
đang đọc từ ảnh nào** để người sau kiểm tra lại được.

### Chạy lại giữa chừng

OCR 50 bài mất khoảng một giờ. Muốn xem kết quả đã có mà không chạy lại:

```powershell
python scripts\convert_available_lessons.py
```

Script này quét `extracted_data/mineru_md/`, đổi những bài đã OCR xong sang JSON,
vá các dòng bị bỏ sót, copy vào `public/`, rồi in bảng kiểm tra chất lượng. Bài
chưa đủ dữ liệu bị **bỏ qua chứ không ghi đè** bằng bản rỗng.

**Hai thứ OCR không lấy được, và không nên bịa:**

- **Phiên âm IPA** — sách in IPA nhưng trang scan không tách được ký hiệu phiên âm.
  Trường `ipa` để rỗng.
- **Nghĩa tiếng Việt** — sách tiếng Anh, không có. `definition_vi` để rỗng và
  `needs_translation: true`; Tab 4 (AI Sentence Lab) dùng để dịch khi cần.

**31/50 trang `listening_practice` là ảnh Part 1 (không có chữ)** — MinerU trả về
đúng: trang chỉ có ảnh. Script ghi nhận `listening.questions = []` thay vì bịa câu
hỏi. Ảnh Part 1 đã có sẵn ở `public/part1_photos/`.

### Kiểm tra và publish

```powershell
python scripts\run_ocr_pipeline.py --validate    # kiểm tra schema từng bài
python scripts\run_ocr_pipeline.py --publish     # copy sang public/ cho web app đọc
```

`run_ocr_pipeline.py` bổ sung những gì `batch_ocr_to_json.py` còn thiếu:

- `--stage extract`: gọi `extract_pdf_assets.py` (Script 1) — trước đây chưa từng
  chạy nên `extracted_data/lesson_page_scans/` không tồn tại và OCR không có đầu vào.
- `--validate`: kiểm tra schema từng bài (12 từ, đủ trường, đáp án ⊆ word_bank,
  12 chỗ trống đánh số đúng) **trước khi** nạp vào app.
- `--only`, `--from`, `--to`, `--force`: chạy lại từng phần, không bỏ qua im lặng.
- `--publish`: chuẩn hoá `audio_track` / `part1_photo` và copy sang `public/`.
- Ghi JSON đã `json.loads` (không ghi text thô) nên không thể lọt JSON hỏng vào app.

### Ghi chú: giao diện web sẵn có của MinerU

Bản cài MinerU có sẵn UI để kéo-thả ảnh và xem kết quả trực quan — tiện để kiểm
tra chất lượng OCR trước khi chạy cả 49 bài:

```bat
D:\CODE\vibecode\TOOL\mineru\2-webui.cmd
```

Mở http://127.0.0.1:7860 rồi kéo-thả
`extracted_data\lesson_page_scans\lesson_01\013_words_to_learn.png`.

---

## Quy tắc Context Window

**Không bao giờ** mở `600 est_.pdf` hay thư mục `extracted_data/` vào context của AI.
Cả hai đã được liệt kê trong `.gitignore` và `.cursorignore`. Chỉ làm việc qua
`book_structure_map.json`, `sample_lessons/lesson_01.json` và `lessons_json/*.json`.
