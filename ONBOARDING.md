# ONBOARDING — 600 Essential Words for the TOEIC (Local Web App)

> **Đọc file này trước khi làm bất cứ điều gì.** Đây là điểm vào duy nhất cho một
> agent mới. `README.md` là hướng dẫn vận hành pipeline OCR; `app/CONTRACT.md` là
> hợp đồng interface. File này là **bức tranh toàn cảnh**: dự án là gì, dữ liệu
> chảy thế nào, cái gì đã xong, cái gì còn thiếu, và **những cái bẫy đã từng làm
> sai** để bạn không lặp lại.

Cập nhật lần cuối: sau khi hoàn thành Answer Key + Explanations + Duolingo UI.

---

## 1. Dự án là gì

Ứng dụng web **chạy local** để học 600 từ vựng thiết yếu TOEIC, dựng từ cuốn
*Barron's 600 Essential Words for the TOEIC (3rd Edition)*.

Phương pháp cốt lõi: **Context-First** — một từ mục tiêu **không bao giờ** được
hiển thị đơn lẻ. Nó luôn đi kèm câu ví dụ trong sách, collocations, và bảng
word family.

**Đây KHÔNG phải git repo.** Không có `git log`, không có branch, không rollback.
Mọi thay đổi là trực tiếp trên đĩa.

- **Working dir:** `D:\LEGION\Documents\deepseek-harness\TiengAnh`
- **50 bài**, 10 chủ đề (General Business → Travel), + 10 "Word Review"
- **968 câu hỏi** trong app

---

## 2. QUY TẮC BẤT KHẢ XÂM PHẠM (đọc trước tiên)

### 2.1 Context Window Guard — TUYỆT ĐỐI

**KHÔNG BAO GIỜ** mở `600 est_.pdf` (11.7 MB) hoặc bất cứ thứ gì trong
`extracted_data/` vào context của AI.

Hai đường dẫn này nằm trong cả `.gitignore` và `.cursorignore`. Lý do: PDF scan
là ảnh, đọc vào sẽ ngốn hết context và không mang lại thông tin dùng được.

**Chỉ làm việc qua JSON.** Nếu bạn cần biết sách in gì, đọc `lessons_json/`,
`public/answers/*.json`, hoặc `scripts/data/*.json`.

### 2.2 Môi trường — các lệnh ĐÚNG

Đây là môi trường Windows bị sandbox siết. **Các lệnh "chuẩn" sẽ thất bại.**
Dùng đúng như dưới đây:

| Việc | ❌ Sẽ lỗi | ✅ Dùng cái này |
|---|---|---|
| Chạy dev server | `npm run dev` → `spawn EPERM` | `node scripts/dev-server.mjs` (trong `app/`) |
| Build | `npm run build` → `spawn EPERM` | `node scripts/build.mjs` (trong `app/`) |
| Bất kỳ lệnh npm | lỗi ghi log | set `$env:npm_config_cache="D:\LEGION\Documents\deepseek-harness\TiengAnh\.npm-cache"` |
| Python | `python` | `py -3.11` |
| PowerShell 7 | `pwsh` không có trên PATH | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File <script>` |
| Chạy script .py dài | `py -3.11 -c "..."` → lỗi quote | **viết file `.py` tạm rồi chạy** |

**Tại sao `spawn EPERM`:** Vite gọi `child_process.exec` để nạp config, mà sandbox
chặn piped stdio. `scripts/dev-server.mjs` và `scripts/build.mjs` gọi Vite API
trực tiếp, không qua config loader.

**Tại sao không dùng heredoc:** PowerShell không hỗ trợ heredoc, và
`py -3.11 -c "..."` vỡ ngay khi có dấu ngoặc lồng nhau. Luôn viết file `.py`.

### 2.3 Ghi file — dùng tool, không dùng shell

Ưu tiên `read`/`edit`/`write`. Khi gặp `FS_STALE_VERSION`: đọc lại file, ghép
thay đổi lên nội dung mới, thử lại. Nhiều agent cùng sửa một file là nguyên nhân
số 1 của lỗi `Identifier 'x' has already been declared`.

---

## 3. Kiến trúc

```
TiengAnh/
├─ 600 est_.pdf                  # ⛔ PDF gốc — KHÔNG ĐỌC
├─ book_structure_map.json       # bản đồ 374 trang PDF → 50 bài
├─ extracted_data/               # ⛔ dump OCR thô — KHÔNG ĐỌC
│  └─ mineru_md/lesson_NN/*.md   #   6 file/bài (xem §4.1)
├─ scripts/                      # pipeline OCR + sinh dữ liệu
│  └─ data/                      # NGUỒN của answer_key / explanations / tapescripts
├─ lessons_json/                 # bản sao nguồn
├─ public/                       # tài nguyên web được serve
│  ├─ lessons_json/lesson_NN.json    # ← đường nạp chính của app
│  ├─ answers/                       # ← answer_key + explanations + tapescripts
│  ├─ audio/track_01..50.mp3
│  └─ part1_photos/lesson_01..50.jpg
└─ app/                          # React 19 + Vite 8 + Tailwind v4
   ├─ CONTRACT.md                # hợp đồng interface
   ├─ vite.config.js             # publicDir -> ../public  (QUAN TRỌNG)
   └─ src/
      ├─ App.jsx                 # shell: sidebar + header + 5 tab
      ├─ index.css               # Tailwind + design tokens Duolingo
      ├─ data/curriculum.js      # 10 chủ đề → 50 bài
      ├─ lib/
      │  ├─ lessonLoader.js      # nạp động + normalizeLesson() + derivePos()
      │  ├─ answerKey.js         # nạp answer_key + explanations
      │  ├─ assets.js            # URL, highlight, cloze
      │  ├─ storage.js           # LocalStorage: tiến độ, SRS, cài đặt
      │  ├─ srs.js               # SM-2
      │  └─ store.jsx            # AppProvider + useApp()
      ├─ components/ui.jsx       # Button/Card/Badge/Highlighted/useSpeech
      └─ tabs/Tab1..Tab5.jsx
```

### 3.1 Chi tiết dễ sai nhất: `publicDir`

`app/vite.config.js` đặt `publicDir: '../public'`. Nghĩa là:

- **App đọc asset từ `TiengAnh/public/`, KHÔNG phải `app/public/`.**
- `app/public/` **không tồn tại** và không nên tạo.
- Muốn thêm file cho app dùng → đặt vào `TiengAnh/public/`.

### 3.2 Cơ chế nạp bài

`lessonLoader.js` thử theo thứ tự:

1. `/lessons_json/lesson_NN.json` ← nguồn chính
2. `/sample_lessons/lesson_NN.json` ← chỉ có bài 01
3. → trạng thái **"Chưa trích xuất"** (sidebar hiện nhãn vàng)

`normalizeLesson()` lấp mọi nhánh optional, nên sau khi load **luôn** có thể giả
định các nhánh tồn tại (có thể rỗng/null).

---

## 4. Pipeline dữ liệu

### 4.1 Cấu trúc sách

`book_structure_map.json`: 374 trang PDF, `page_offset_book_to_pdf: 12`.
Mỗi bài chiếm **6 trang**, theo thứ tự:

| # | Section | Nội dung |
|---|---|---|
| 1 | `words_to_learn` | 12 từ mục tiêu + định nghĩa + ví dụ |
| 2 | `words_in_context` | đoạn văn có chỗ trống + word bank |
| 3 | `word_families` | bảng họ từ (verb/noun/adj/adv) |
| 4 | `listening_practice` | **Part 1–4** |
| 5 | `reading_part5_6` | Part 5 + Part 6 |
| 6 | `reading_part7` | Part 7 |

Các trang đặc biệt: **Answer Key ở PDF trang 333–336**, **Tapescripts 341–373**.

### 4.2 Luồng

```
PDF scan
  → extract_pdf_assets.py      (cắt ảnh từng section)
  → MinerU OCR                 (ảnh → Markdown)
  → extracted_data/mineru_md/
  → run_mineru_local.py        (Markdown → JSON có cấu trúc)
  → lessons_json/ + public/lessons_json/
  → lessonLoader.js nạp vào app
```

Các script sinh dữ liệu phụ (đọc trực tiếp từ `extracted_data/`, ghi vào
`scripts/data/` rồi copy sang `public/answers/`):

| Script | Sinh ra | Ghi chú |
|---|---|---|
| `parse_answer_key.py` | `scripts/data/answer_key.json` | đọc 4 file Answer Key |
| `parse_tapescripts.py` | `scripts/data/tapescripts.json` | đọc 33 file Tapescript |
| `build_explanations.py` | `scripts/data/explanations.json` | cần 2 file trên |
| `convert_available_lessons.py` | `lessons_json/` | pipeline chính |

**Quan trọng:** `scripts/data/` là **nguồn**, `public/answers/` là **bản publish**.
Sửa nguồn xong **phải copy sang `public/`**:

```powershell
Copy-Item scripts\data\answer_key.json    public\answers\answer_key.json -Force
Copy-Item scripts\data\explanations.json  public\answers\explanations.json -Force
Copy-Item scripts\data\tapescripts.json   public\answers\tapescripts.json -Force
```

Quên bước này là nguyên nhân của lỗi "dữ liệu đúng mà UI không thấy".

### 4.3 Đánh số câu — THEO SÁCH, không theo thứ tự đọc

Đây là điểm gây nhầm lẫn nhiều nhất:

| Part | Số câu | Ghi chú |
|---|---|---|
| Part 1 | (không có số) | chỉ có ảnh |
| Part 2 | (không có số) | chỉ có audio, nhãn A/B/C |
| Part 3 | **4–6** | |
| Part 4 | **7–9** | |
| Part 5 | 10–15 | |
| Part 6 | 16–18 | |
| Part 7 | 19–23 | |

**Part 1 và Part 2 KHÔNG có câu hỏi dạng text** → đánh số bắt đầu từ 4. Đây là lý
do có "khoảng trống" 1–3, **không phải lỗi**.

**Bẫy hai cột:** Part 3/4 in **hai cột**, nên thứ tự tự nhiên là `4, 6, 5` và
`7, 9, 8` — **KHÔNG sắp xếp lại**. UI phải hiển thị đúng thứ tự sách in.

---

## 5. Shape dữ liệu THỰC TẾ

> ⚠️ `app/CONTRACT.md` mô tả shape *dự định*. Shape **thực tế** khác ở vài chỗ
> (đã liệt kê dưới). **Tin file JSON, không tin doc.**

### 5.1 `public/lessons_json/lesson_NN.json`

```jsonc
{
  "lesson_id": 1,
  "title": "Contracts",
  "theme_name": "General Business",
  "audio_track": "track_01.mp3",          // KHÁC contract: không có tiền tố "audio/"
  "part1_photo": "part1_photos/lesson_01.jpg",
  "words_to_learn": [{
    "id": 2, "word": "agreement", "pos": "n.",
    "ipa": "",                             // RỖNG toàn bộ (xem §8)
    "definition_en": "a mutual arrangement, a contract",
    "definition_vi": "",                   // RỖNG toàn bộ
    "examples": [{ "en": "...", "vi": "" }],
    "needs_translation": true
  }],
  "words_in_context": { "passage": "...", "word_bank": [...], "blanks": [...],
                        "questions": [...], "bank_certain": ... },
  "word_families": [ [ {"pos":"", "word":"agree", "example":"..."}, ... ] ],
  "practice": { "part5": [...], "part6": {...}, "part7": [...] },   // CHỈ 5/6/7
  "listening": {                          // TOP-LEVEL, không nằm trong practice
    "questions": [...], "instructions": "...",
    "tapescript": "",                     // luôn RỖNG
    "parts": [...],
    "part3": [...], "part4": [...]        // PART 3/4 nằm Ở ĐÂY
  },
  "tapescript": "",
  "_raw": { "words_to_learn": ..., "listening_practice": ..., ... },
  "needs_review": true
}
```

**Khác biệt so với CONTRACT.md — ghi nhớ:**

1. `listening` là **top-level**, không phải `practice.listening`
2. `practice` chỉ có `part5`, `part6`, `part7` — **không có `listening`/`reading`**
3. `part7` là **array of blocks** (`[{passages, questions}]`), không phải object
4. `audio_track` = `"track_01.mp3"`, không phải `"audio/track_01.mp3"`
5. `words_to_learn[].word_family` thường **vắng**; dữ liệu họ từ nằm ở
   `lesson.word_families`
6. Option là **array `[{label, text}]`**, không phải object `{A: "...", ...}`
7. Câu hỏi dùng key `number`, không phải `question_num`

### 5.2 `public/answers/answer_key.json`

```jsonc
{
  "1": {
    "lesson_id": 1,
    "title": "Contracts",
    "words_in_context": { "1": "agreement", "2": "parties", ... },   // 12 mục
    "word_practice":    { "1": "B", "2": "A", ... },                // 23 mục = câu 1..23
    "warnings": [...]                                               // tùy chọn
  }, ...
}
```

`word_practice` gộp **tất cả** các part có text theo số câu của sách: 4–9
(listening), 10–15 (Part 5), 16–18 (Part 6), 19–23 (Part 7).

### 5.3 `public/answers/explanations.json`

```jsonc
{
  "1": {
    "10": {
      "answer": "A",
      "why": "Đáp án đúng là (A) <b>agreement</b>. Chỗ trống cần một <b>danh từ</b>...",
      "pos_needed": "noun",                  // "" nếu không suy ra được
      "option_notes": { "B": "(B) agreeable — là <b>tính từ</b>, nhưng..." },
      "source": "grammar",                   // xem bảng dưới
      "section": "part5"                     // part5|part6|part7|listening3|listening4
    }, ...
  }, ...
}
```

`source` có 5 giá trị:

| source | Ý nghĩa |
|---|---|
| `grammar` | Part 5/6 — suy luận ngữ pháp từ vị trí chỗ trống |
| `passage` | Part 7 — **có trích dẫn** câu trong bài đọc (`evidence`) |
| `passage-no-evidence` | Part 7 — không tìm được câu khớp |
| `tapescript` | Listening — **có trích dẫn** lời thoại (`evidence`) |
| `listening-no-script` | Listening — bài không có tapescript |

`why` và `option_notes` chứa HTML **giới hạn** (`<b>`, `<i>`) — UI render qua
helper `renderExplain()`, **KHÔNG dùng `dangerouslySetInnerHTML`**.

### 5.4 `public/answers/tapescripts.json`

```jsonc
{ "2": { "lesson_id": 2, "part3": "[W] With a new store opening...", "part4": "..." } }
```

Chỉ **34/50 bài** có. 16 bài thiếu là **thiếu dữ liệu gốc** (xem §8).

---

## 6. Frontend

### 6.1 5 tab

| Tab | File | Chức năng |
|---|---|---|
| 1 | `Tab1Vocabulary.jsx` | Học từ theo ngữ cảnh |
| 2 | `Tab2Flashcards.jsx` | Flashcard lật |
| 3 | `Tab3Srs.jsx` | Ôn tập giãn cách (SM-2) |
| 4 | `Tab4AiLab.jsx` | AI Sentence Lab |
| 5 | `Tab5Practice.jsx` | **Luyện đề & Audio — chấm bài + giải thích** |

`Tab5Practice.jsx` là file lớn nhất (~68 KB) và phức tạp nhất.

### 6.2 Design system — Duolingo

Tokens trong `index.css`:

```
--color-duo-green:  #58CC02    (đậm hơn: #58A700)
--color-duo-blue:   #1CB0F6
--color-duo-red:    #FF4B4B
--color-duo-yellow: #FFC800
--color-duo-purple: #CE82FF
correct: #D7FFB8    wrong: #FFDFE0
```

Nút 3D đặc trưng của Duolingo:

```css
box-shadow: 0 4px 0 <màu đậm hơn>;
/* :active */ transform: translateY(4px); box-shadow: none;
```

Class chính: `.duo-choice` (option), `.duo-btn`, `.duo-progress`,
`.duo-nav-item`, `.duo-explain*` (khối giải thích).
**Giữ nguyên `.vocab-hit`, `.cloze-blank`, `.flip-*`** — đó là contract cũ.

### 6.3 Luồng chấm bài (Tab 5)

```
useEffect → loadAnswers() + loadExplanations()   (1 lần, module-cached)
         ↓
withKey(q)  →  gắn q.answer + q.explanation      (Answer Key ưu tiên hơn JSON)
         ↓
expectedFor(num) → normalizeKeyLetter()
         ↓
Khi bấm "Nộp bài" → graded = true
         ↓
QuestionCard hiện: đáp án đúng + badge + khối giải thích
```

**Giải thích CHỈ hiện sau khi nộp bài** — không lộ đáp án khi đang làm.

---

## 7. Kiểm thử

Chạy TẤT CẢ trước khi báo xong:

```powershell
cd D:\LEGION\Documents\deepseek-harness\TiengAnh
$env:npm_config_cache="D:\LEGION\Documents\deepseek-harness\TiengAnh\.npm-cache"

# --- Tầng dữ liệu ---
py -3.11 scripts\test_parse_listening.py        # 335 assertion
py -3.11 scripts\test_answer_key.py             # 56 assertion
py -3.11 scripts\test_tapescripts.py            # 57 assertion
py -3.11 scripts\reports\verify_listening_parts.py
py -3.11 scripts\validate_explanations.py       # 7 assertion chất lượng
py -3.11 scripts\coverage_report.py             # báo cáo độ phủ

# --- Tầng app ---
cd app
node scripts\verify_runtime.mjs                 # 20
node scripts\verify_loader.mjs                  # 27
node scripts\verify_tabs.mjs                    # 15
node scripts\lead_e2e_check.mjs                 # 25
node scripts\verify_explanations.mjs            # 15
cd ..
node scripts\check_helpers.mjs                  # ALL CHECKS PASSED
cd app && node scripts\build.mjs                # BUILD OK
```

> `coverage_report.py` và `parse_*.py` **exit 1 khi còn thiếu dữ liệu** — đó là
> chủ ý để CI bắt được. File JSON vẫn được ghi xong **trước** khi exit.

### 7.1 Test âm — chứng minh test thật sự "cắn"

Test xanh chưa chứng minh được gì nếu nó không thể fail. Đã kiểm chứng:

- Xóa giải thích L1 q10 → 7 FAIL
- Đổi đáp án L1 q10 từ A sang B → 3 FAIL
- Chèn câu vô nghĩa bị cấm → FAIL
- Xóa `option_notes` → FAIL

**Khi thêm test mới, hãy làm nó fail trước.**

---

## 8. Trạng thái dữ liệu — ĐÃ XONG gì, CÒN THIẾU gì

### 8.1 Con số chính xác

| Hạng mục | Số | Chuẩn |
|---|---|---|
| Bài có JSON | 50/50 | 50 |
| Tổng câu hỏi trong app | 968 | — |
| **Chấm được (có đáp án)** | **966 (99.8%)** | — |
| **Có giải thích** | **966 (99.8%)** | — |
| Listening Part 3/4 chấm được | 298/300 (99.3%) | — |
| Answer Key — Words In Context | 600/600 | 600 |
| Answer Key — Word Practice | 1148/1150 | 1150 |
| Tapescripts | 34/50 bài | 50 |

Phân bố câu hỏi: Part 3 = 150, Part 4 = 150, Part 5 = 299, Part 6 = 149, Part 7 = 220.

### 8.2 Những thứ CÒN THIẾU — và lý do (KHÔNG ĐƯỢC BỊA)

Đây là **thiếu dữ liệu gốc**, đã điều tra và xác nhận. **Không được lấp bằng
suy đoán.**

| Thiếu | Số lượng | Nguyên nhân đã xác minh |
|---|---|---|
| Đáp án L08 câu 5, 6 | 2 | Nguồn in `4. B 7. A` — 21 giá trị cho 23 ô; OCR **xóa hẳn** cả số lẫn giá trị |
| Tapescript | 16 bài | Giữa `LESSON N` và `LESSON N+1` chỉ có Part 1 + Part 2, **không hề có khối Part 3/4**. Bài 1 nằm ở trang 329, **trước** file tapescript đầu tiên (341) |
| `ipa` | 0/12 từ/bài | MinerU không đọc được ký hiệu phiên âm |
| `definition_vi` | 0/12 từ/bài | Sách không in bản dịch |
| `collocations` | 0/12 từ/bài | Không có trong bản OCR |
| Word family rows | 13 bài thiếu | Bài `[15,20,21,22,24,27,31,33,36,37,39,41,45]` — MinerU đọc sót |

16 bài thiếu tapescript (**đã kiểm chứng bằng script**):
`[1, 5, 8, 11, 14, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50]` — `34/50` bài có.

**Cách UI xử lý (đúng):** khi thiếu tapescript, khối giải thích **nói thẳng** là
bài này chưa có bản ghi và đáp án lấy từ Answer Key — **không bịa lời thoại**.

### 8.3 Cảnh báo trong answer_key (đã xử lý, giữ lại để truy vết)

`answer_key.json` có `warnings` ở 6 bài — **không phải lỗi**, là ghi chú OCR:

- L05, L06: `WIC: 21 -> 11` — OCR nhầm số trang; từ **có** trong 12 từ mục tiêu
- L08: `WP: thiếu mục [5, 6]` — không thể khôi phục
- L27, L40, L44: OCR đọc `B` thành `8`, hoặc ẩn số thứ tự — **đã khôi phục đúng**

---

## 9. BẪY ĐÃ TỪNG SẬP — đọc để không lặp lại

Đây là phần giá trị nhất của file. Mỗi mục là một bug **có thật** đã sửa.

### 9.1 Trích ảnh sai → mất toàn bộ Part 3/4 của 37 bài

**Triệu chứng:** 37/50 bài không có nội dung listening.

**Nguyên nhân:** `extract_pdf_assets.py` chọn ảnh bằng
`max(pg.images, key=lambda x: len(x.data))` — chọn theo **số byte**. Ảnh JPEG
nhỏ của Part 1 (21,055 B, 296×312) **nặng byte hơn** ảnh scan toàn trang
(20,714 B, 1456×1936). Kết quả: nộp cho OCR một tấm ảnh chụp lại ảnh → không có
text.

**Đã sửa:** `pick_full_page_scan(page)` chọn theo **diện tích pixel**
(`w >= 800 and h >= 800`), áp dụng ở cả 3 chỗ.

**Bài học:** đừng bao giờ chọn ảnh theo kích thước file. Dùng kích thước pixel.

### 9.2 Đáp án cắt qua ranh giới trang → mất 23 đáp án

**Triệu chứng:** L37 mất sạch 23 đáp án Word Practice.

**Nguyên nhân:** Trang 335 kết thúc giữa bài; trang 336 bắt đầu bằng
`Word Practice: 1. D 2. C ...` của L37. Parser **reset "bài đang đọc" theo từng
file**.

**Đã sửa:** viết lại thành **máy trạng thái quét một lượt** qua 4 file, mang
"bài đang đọc" + "mục đang đọc" **xuyên qua ranh giới file**.

**Bài học:** dữ liệu trải trên nhiều file thì state phải mang qua ranh giới.

### 9.3 Regex coi `l`/`I`/`O` là chữ số GIỮA TỪ → mất 18 mục

**Triệu chứng:** 18 mục Word In Context bị "rong".

**Nguyên nhân:** regex cho phép `l`/`I`/`O` làm chữ số ở **bất kỳ đâu**. Nên
`9. layout` khớp `l` trong `layout` → mục 9 biến thành `ayout`. Tương tự
`6. loyalty`, `5. logical`.

**Đã sửa:** bắt buộc có **dấu phân cách** (`[.,]`) sau số, hoặc số + chữ HOA dính
liền.

### 9.4 Cắt thô theo nhãn `(A)(B)(C)(D)` → 10 bài bị rỗng

**Bối cảnh:** khi parse tapescript, ta muốn bỏ các dòng nhãn phương án tranh ảnh.

**Cách SAI (đã thử):** cắt bỏ **cả cụm từ nhãn trở đi**. File 342 bài 4 có
`Part 3:` theo sau là `(A)(B)(C)(D)` + 4 câu mô tả tranh (vật liệu Part 1), rồi
**lại là lời thoại Part 3 thật ở dưới**. Cắt thô làm **10 bài bị rỗng**.

**Đã sửa:** chỉ bỏ **từng dòng nhãn**, giữ phần còn lại. Test có assertion ghi
lại đúng cái bẫy này.

**Bài học:** khi dọn nhiễu, chỉ xóa đúng thứ gây nhiễu, đừng xóa cả vùng.

### 9.5 Nhiều agent sửa cùng file → trùng khai báo

**Triệu chứng:** `[PARSE_ERROR] Identifier 'withKey' has already been declared`.

**Nguyên nhân:** hai lần sửa chồng lên nhau cùng thêm một hàm.

**Bài học:** chia write scope rõ ràng, một file một người. Đọc lại file trước
khi sửa.

### 9.6 Dữ liệu mới nhưng UI vẫn báo cũ

**Triệu chứng:** một câu **đã có đáp án** nhưng ngay dưới vẫn hiện
*"Câu này chưa có đáp án"*.

**Nguyên nhân:** dòng cảnh báo render **vô điều kiện**; sau khi nối Answer Key
vào, điều kiện không còn đúng nữa.

**Đã sửa:** gate bằng `part2.some((q) => !normalizeLetter(q.answer))`.

**Bài học:** khi thêm năng lực mới, **rà lại mọi thông báo cũ** nói về việc thiếu
năng lực đó.

### 9.7 Giải thích rỗng nghĩa, lặp lại y nguyên

**Triệu chứng:** mọi câu nghe đều có `why` = *"Phần này cần NGHE audio để tự
đánh giá..."* — đúng nhưng **vô dụng**.

**Đã sửa:** sinh lời khuyên theo **dạng câu hỏi** (WHO/WHAT/WHERE/WHEN/WHY/HOW)
kèm chiến lược nghe cụ thể; và khi có tapescript thì trích dẫn thật.

**Bài học:** một câu đúng mà không mang thông tin thì vẫn là lỗi chất lượng.

### 9.8 `derivePos` lệch giữa Python và JS

**Vấn đề:** `build_explanations.py` (Python) và `lessonLoader.js` (JS) **cùng
đoán từ loại**. Nếu lệch nhau, cột word family trên UI và khối giải thích sẽ
**mâu thuẫn**.

**Đã sửa:** thêm `ee/eer/ery` (noun) và `some/ary/ory/ian/ant/ent` vào **cả hai**.

**Quy tắc:** hai chỗ cài đặt cùng logic thì **phải sửa cùng lúc**. Đã có
`validate_explanations.py` kiểm tra `pos_needed` không mâu thuẫn đáp án.

### 9.9 Chrome headless bị sandbox chặn

Screenshot thất bại vì Chrome cần IPC/crash-handler process. Cách chạy được:

```
chrome.exe --headless=new --disable-gpu --no-sandbox --disable-crash-reporter
  --disable-breakpad --user-data-dir=<thư mục ghi được> --screenshot=<out.png>
```

Ngoài ra `renderToString()` **không chạy `useEffect`** — muốn chụp trạng thái
"đã nộp bài" phải **seed sẵn state từ file thật**, không dựa vào effect.

---

## 10. Nguồn dữ liệu — đâu là sự thật

Khi có mâu thuẫn, thứ tự ưu tiên:

1. **`answer_key.json`** — đáp án in trong sách, chép lại. **Cao nhất.**
2. **Dữ liệu book in trong JSON** (`pos`, `definition_en`, `examples`)
3. **Suy luận** (`derivePos`) — luôn bị đánh dấu "suy ra" trên UI

UI ghi rõ nguồn: dữ liệu sách hiện `Verb`, dữ liệu suy ra hiện `Verb (suy ra)`.
Trên 885 dòng word family: 289 `book`, 215 `book-word`, 377 `derived`, 4 không có.

**Provenance là ràng buộc, không phải trang trí.** Đã đo: 504 dòng nhận là từ
sách có **0 sai lệch**; 377 dòng ghi rõ `derived`. Không có tuyên bố sai.

---

## 11. Việc còn lại (nếu muốn làm tiếp)

1. **OCR thêm trang Tapescript** cho 16 bài thiếu → sẽ thêm được trích dẫn lời
   thoại thật (hiện 74 câu có evidence).
2. **OCR lại các trang Answer Key** chất lượng cao hơn → có thể khôi phục L08
   câu 5, 6 (hiện 21/23 giá trị).
3. **Bổ sung `ipa` / `definition_vi`** — cần nguồn ngoài hoặc OCR lại.
4. **13 bài thiếu word family rows** — OCR lại trang `word_families`.

⚠️ **Trước khi làm bất kỳ điều nào ở trên: KHÔNG được bịa.** Một đáp án sai còn
tệ hơn một đáp án trống, vì người học sẽ tin nó.

---

## 12. Checklist trước khi báo "xong"

- [ ] Chạy **tất cả** test ở §7 — không có FAIL
- [ ] Nếu sửa `scripts/data/*` → **đã copy sang `public/answers/`**
- [ ] Nếu sửa logic dữ liệu → chạy lại `coverage_report.py`
- [ ] Nếu sửa `derivePos` → sửa **cả** Python **và** JS
- [ ] Nếu thêm test → đã thử làm nó **fail** trước
- [ ] Không rác: xóa file probe/tạm (`.shots/`, `__*.jsx`, script chẩn đoán)
- [ ] Không mở `600 est_.pdf` hay `extracted_data/`
- [ ] Nếu không chắc một dữ liệu → **để trống + ghi warning**, đừng đoán

---

## 13. Bảng tra nhanh

| Tôi muốn... | Làm cái này |
|---|---|
| Chạy app | `cd app && node scripts/dev-server.mjs` |
| Build | `cd app && node scripts/build.mjs` |
| Thêm asset cho app | Đặt vào `TiengAnh/public/` (KHÔNG phải `app/public/`) |
| Xem 1 bài | `public/lessons_json/lesson_NN.json` |
| Xem đáp án | `public/answers/answer_key.json` |
| Xem giải thích | `public/answers/explanations.json` |
| Sinh lại giải thích | `py -3.11 scripts/build_explanations.py` rồi copy sang `public/answers/` |
| Kiểm tra độ phủ | `py -3.11 scripts/coverage_report.py` |
| Kiểm tra chất lượng giải thích | `py -3.11 scripts/validate_explanations.py` |
| Biết sách in gì | `book_structure_map.json` |
| Hợp đồng interface | `app/CONTRACT.md` |
| Pipeline OCR | `README.md` |
