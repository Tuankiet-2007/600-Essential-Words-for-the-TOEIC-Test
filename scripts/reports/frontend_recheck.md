# Frontend re-check — Tab1/Tab2 + word families (task-6)

**Người thực hiện:** frontend-dev
**Thời điểm:** 2026-11-07 ~14:30–14:45 (+07:00)
**Bối cảnh:** converter đã sinh lại TOÀN BỘ `public/lessons_json/` sau khi OCR lại 37 trang
listening (sửa `extract_pdf_assets.py` chọn ảnh theo pixel thay vì theo số byte).
Mục đích: xác minh Tab 1 / Tab 2 **không bị regression**.

> Phạm vi: CHỈ đọc dữ liệu và chạy lệnh. Không sửa file nguồn nào.

---

## (a) Kết quả assertion từng script

| Script | Kết quả | Ghi chú |
|---|---|---|
| `app/scripts/verify_runtime.mjs` | **20 passed, 0 failed** | app shell, 5 module tab, lesson JSON, audio, part1_photos, SPA-fallback |
| `app/scripts/verify_loader.mjs` | **27 passed, 0 failed** | chuẩn hoá layout OCR → tab |
| `app/scripts/verify_tabs.mjs` | **15 passed, 0 failed** | SSR 5 tab × (có lesson / lesson=null) |
| `py -3.11 scripts/test_parse_listening.py` | **335/335 PASS** | đúng kỳ vọng |
| `node scripts/check_helpers.mjs` | **ALL CHECKS PASSED** | 7 nhóm kiểm tra highlight/cloze/blank |

Lệnh đã chạy (từ `app/`):

```
$env:npm_config_cache="D:\LEGION\Documents\deepseek-harness\TiengAnh\.npm-cache"
node scripts/verify_runtime.mjs
node scripts/verify_loader.mjs
node scripts/verify_tabs.mjs
```

Chi tiết đáng chú ý trong `verify_loader.mjs`:

```
PASS  practice.listening.part3 có câu hỏi (150) — JSON để listening ở top-level
PASS  practice.listening.part4 có câu hỏi (150)
```

Trước khi sửa là **39** câu mỗi part; nay là **150** (50 bài × 3 câu). Đây là bằng chứng
định lượng cho thấy bản sửa Part 3/Part 4 đã có hiệu lực.

SSR HTML của Tab 1 tăng từ 79.602 B (lần kiểm tra trước) và hiện render đầy đủ bảng họ từ.

---

## (b) Số dòng word-family thật trên 50 bài

| Chỉ số | Giá trị |
|---|---|
| **Tổng số dòng family có dữ liệu thật (50 bài)** | **883** |
| Tổng số từ mục tiêu có ít nhất 1 dòng family | 298 |
| Số bài có 0 dòng family | **0** (không bài nào) |
| Số bài có đúng 18 dòng | 41 |

Phân bố theo bài:

```
L01-L10: 18, 18, 18, 18, 18, 18, 18, 18, 18, 18
L11-L20: 18, 18, 18, 18, 15, 18, 18, 18, 18, 18
L21-L30: 17, 17, 18, 16, 18, 18, 15, 18, 18, 18
L31-L40: 15, 18, 17, 18, 18, 17, 17, 18, 17, 18
L41-L50: 18, 18, 18, 18, 18, 18, 18, 18, 18, 18
```

Các bài 15/16/17 dòng là do sách chỉ in 5–6 nhóm họ từ cho bài đó — đúng dữ liệu gốc,
không phải mất mát.

### Kiểm tra riêng lesson_01 (theo yêu cầu mục 2)

**ĐÚNG 6 từ có họ từ, mỗi từ 3 dòng; 6 từ còn lại 0 dòng (dấu — là đúng, không bịa):**

```
OK  abide by       rows=0 (want 0)
OK  agreement      rows=3 (want 3)  agree · agreement · agreeable
OK  assurance      rows=3 (want 3)  assure · assurance · assuredly
OK  cancellation   rows=3 (want 3)  cancel · cancellation · canceled
OK  determine      rows=0 (want 0)
OK  engage         rows=0 (want 0)
OK  establish      rows=0 (want 0)
OK  obligate       rows=3 (want 3)  obligate · obligation · obligatory
OK  party          rows=0 (want 0)
OK  provision      rows=3 (want 3)  provide · provider · provision
OK  resolve        rows=0 (want 0)
OK  specific       rows=3 (want 3)  specify · specification · specific
```

Xác minh trực tiếp trên DOM (SSR qua loader thật, dữ liệu converter hiện tại):

```
status=loaded source=/lessons_json/lesson_01.json
flat families=18 groups=3,3,3,3,3,3
group words: agree/agreement/agreeable | assure/assurance/assuredly |
             cancel/cancellation/canceled | obligate/obligation/obligatory |
             provide/provider/provision | specify/specification/specific
per-word families: ALL 12 CORRECT
Tab1: first-card family rows = [agree, agreement, agreeable] (3/3) | examples = true
Tab2: first-card family rows = [agree, agreement, agreeable] (3/3) | examples = true
```

→ **Tab 1 và Tab 2 đều render đúng 3 dòng họ từ kèm câu ví dụ.**

---

## (c) So sánh với baseline — KHÔNG có regression

Đối chiếu `scripts/reports/baseline_before_part_fix.json` (trường `family` từng bài)
với số dòng family hiện tại:

| Chỉ số | Baseline | Hiện tại | Chênh lệch |
|---|---|---|---|
| Tổng số dòng family (50 bài) | 883 | **883** | **+0** |
| Bài giảm số dòng (mất dữ liệu) | — | **0** | — |
| Bài tăng số dòng | — | 0 | — |
| Bài không đổi | — | **50/50** | — |

**KẾT LUẬN: KHÔNG CÓ REGRESSION.** Cả 50 bài giữ nguyên chính xác số dòng họ từ so với
baseline; không bài nào mất dữ liệu do lần chạy converter mới.

*Lưu ý về cách đối chiếu:* khoá trong baseline là dạng **zero-padded** (`"01"`, `"02"`, …),
không phải `"1"`. Nếu tra bằng khoá không pad sẽ thấy 9 bài "thiếu" (L01–L09) — đó là
lỗi tra cứu, không phải mất dữ liệu. Sau khi pad đúng, đủ 50/50 bài khớp.

---

## (d) Bất thường khác

### 1. `pos` từ sách đã có tác dụng — nhưng chỉ 289/883 dòng

Converter mới lưu `pos` thật khi sách in: **289/883 dòng (33%)** có `pos` từ sách,
**594 dòng còn lại `pos` rỗng**.

Kiểm chứng nhãn nguồn gốc trên `lesson_04`:

```
avoid           pos=verb       pos_source=derived
avoidance       pos=noun       pos_source=book
avoided         pos=adjective  pos_source=book
develop         pos=verb       pos_source=book
development     pos=noun       pos_source=derived
...
pos_source tally: book=9 derived=9 none=0
```

Nhãn hoạt động đúng: `pos` của sách được giữ nguyên và đánh dấu `book`; chỉ những dòng
thật sự rỗng mới bị suy ra và đánh dấu `derived` (UI hiện chữ "suy ra").

### 2. ⚠️ ĐỘ CHÍNH XÁC CỦA `pos` SUY RA CHỈ 37% — cần lead quyết định

Đây là phát hiện quan trọng nhất. Với những từ mà sách **in `pos` ở một chỗ khác trong
sách**, ta có bằng chứng độc lập để kiểm tra phỏng đoán hình thái:

| Chỉ số | Giá trị |
|---|---|
| Dòng `pos` rỗng | 594 |
| Trong đó có bằng chứng sách để đối chiếu | 27 |
| Suy ra **đúng** | 10 |
| Suy ra **SAI** (mâu thuẫn với sách) | **17** |
| **Độ chính xác khi kiểm chứng được** | **37,0%** |

Danh sách 17 trường hợp sai:

```
lesson_05 register:   derived="noun"      book="verb"
lesson_06 duplicate:  derived="verb"      book="noun"
lesson_06 warning:    derived="verb"      book="noun"
lesson_08 code:       derived="verb"      book="noun"
lesson_08 practice:   derived="verb"      book="noun"
lesson_10 petition:   derived="noun"      book="verb"
lesson_10 register:   derived="noun"      book="verb"
lesson_16 mandate:    derived="verb"      book="noun"
lesson_17 function:   derived="noun"      book="verb"
lesson_21 sign:       derived="verb"      book="noun"
lesson_24 refund:     derived="verb"      book="noun"
lesson_25 detail:     derived="verb"      book="noun"
lesson_28 uniform:    derived="verb"      book="noun"
lesson_30 condition:  derived="noun"      book="verb"
lesson_36 delay:      derived="adjective" book="noun"
lesson_44 schedule:   derived="verb"      book="noun"
lesson_46 record:     derived="verb"      book="noun"
```

**Ảnh hưởng thực tế lên UI** (form hiện sai cột trong bảng Verb/Noun/Adj/Adv):

```
word        derived-bucket   book-prints      UI column
duplicate   verb             noun             target "duplicate" -> VERB column
code        verb             noun             target "code"      -> VERB column
sign        verb             noun             target "signature" -> VERB column
refund      verb             noun             target "refund"    -> VERB column
schedule    verb             noun             target "schedule"  -> VERB column
record      verb             noun             target "record"    -> VERB column
delay       adjective        noun             target "delay"     -> ADJECTIVE column
```

Nguyên nhân: các danh từ một âm tiết không có hậu tố đặc trưng
(`code`, `sign`, `refund`, `record`, `schedule`, `delay`, `detail`, `uniform`, …) rơi vào
nhánh mặc định `return 'verb'`. Trong tiếng Anh, danh từ và động từ thường **đồng dạng**
(zero-derivation), nên hình thái học đơn thuần không thể phân biệt — đây là giới hạn cố
hữu của phương pháp, không phải lỗi cài đặt.

**Điểm tích cực:** mọi dòng suy ra đều được gắn nhãn "suy ra" trong UI, nên người học
không bị đánh lừa là dữ liệu sách in. Tuy nhiên **vị trí cột vẫn sai**.

**Đề xuất (chờ lead quyết định — không tự sửa vì ngoài hành vi được giao):**
- Ưu tiên 1: dùng `pos` của chính từ mục tiêu trong sách để gán cho các form đồng dạng
  (ví dụ `code` là từ mục tiêu → `pos` sách = noun → dùng noun cho form `code`s).
- Ưu tiên 2: nếu một từ có `pos` thật ở bất kỳ bài nào, dùng nó thay vì suy ra.
- Ưu tiên 3: khi không chắc, để `pos = ""` và render thành danh sách không chia cột
  (đã nêu trong task-2 như phương án thay thế) — trung thực hơn là đoán sai 63%.

### 3. Không có bất thường khác

- Không bài nào mất họ từ.
- `word_families` cấp bài vẫn là mảng 6 nhóm (mảng lồng), loader chuẩn hoá tốt.
- `check_helpers.mjs` pass toàn bộ (highlight, cloze, blank, đáp án).
- 50/50 bài đều tải được; không có bài `not_extracted` ngoài dự kiến.

---

## Tóm tắt cho lead

| Mục | Kết quả |
|---|---|
| (a) Assertion | runtime 20/20 · loader 27/27 · tabs 15/15 · parser 335/335 · helpers ALL PASS |
| (b) Dòng family thật | **883 dòng / 50 bài**, không bài nào rỗng |
| (c) Baseline | 883 → 883, **50/50 bài không đổi, KHÔNG REGRESSION** |
| (d) Bất thường | `pos` suy ra chỉ đúng **37%** (10/27) — 17 form hiện sai cột; đã có nhãn "suy ra" nên không lừa người học, nhưng vị trí cột sai. Cần lead quyết định có sửa không. |

**Không có regression về word family. Tab 1 và Tab 2 render đúng.** Vấn đề duy nhất cần
quyết định là độ chính xác của `pos` suy ra.
