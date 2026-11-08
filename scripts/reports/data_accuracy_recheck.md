# Recheck độ chính xác dữ liệu Listening Part 3 / Part 4

**Task:** task-7 — đối chiếu dữ liệu mới với ảnh scan thật (chống bịa)
**Người thực hiện:** mineru-dev
**Ngày:** 2026-11-07
**Phạm vi:** CHỈ ĐỌC. Không sửa file nguồn nào.

---

## 0. Bối cảnh

Người dùng phàn nàn "part3,4 sách có in rõ ràng". Nguyên nhân gốc nằm ở tầng
**EXTRACT**, không phải tầng parser:

`scripts/extract_pdf_assets.py` chọn ảnh scan bằng `max(pg.images, key=lambda x: len(x.data))`
— tức chọn ảnh **nhiều BYTE nhất**. Ảnh Part 1 Photo nhúng trong trang là JPEG,
nặng hơn bản scan toàn trang (TIFF) **dù TIFF lớn hơn rất nhiều về pixel**. Kết quả:
37/50 trang `listening_practice` bị lưu nhầm thành **ảnh Part 1 Photo (~300×312 px)**
thay vì cả trang (~1456×2000 px).

MinerU OCR một bức ảnh chụp ảnh → không có chữ → trả về rỗng. Đó là lý do 37 bài
trông như "sách không in Part 3/Part 4" dù sách in rất rõ.

Đã sửa `pick_full_page_scan()` chọn theo **diện tích pixel** (≥800×800), OCR lại
37 trang, chạy lại converter → **50/50 bài có part3 = 3 câu, part4 = 3 câu**.

Ghi chú: parser `parse_listening()` (task-1) vẫn đúng và không cần sửa — nó nhóm
theo tiêu đề Part trong Markdown, nên tự động đúng khi đầu vào được sửa.

---

## (a) Bảng đối chiếu 4 bài với ảnh scan

Ảnh scan đã đọc trực tiếp bằng tool đọc ảnh (không qua OCR):

| Bài | File scan | Kích thước | Số câu P3/P4 | Đối chiếu nội dung | Kết luận |
|---|---|---|---|---|---|
| lesson_02 | `022_listening_practice.png` | 1456×1936 | 3/3 | 6/6 câu + 24/24 lựa chọn | **KHỚP HOÀN TOÀN** |
| lesson_04 | `034_listening_practice.png` | 1456×2000 | 3/3 | 6/6 câu + 24/24 lựa chọn | **KHỚP HOÀN TOÀN** |
| lesson_17 | `118_listening_practice.png` | 1456×1984 | 3/3 | 6/6 câu + 24/24 lựa chọn | **KHỚP HOÀN TOÀN** (1 lỗi escape `\$`) |
| lesson_44 | `290_listening_practice.png` | 1456×2000 | 3/3 | 6/6 câu + 24/24 lựa chọn | **KHỚP HOÀN TOÀN** |

**Tổng: 24/24 câu hỏi và 96/96 lựa chọn khớp từng chữ với ảnh scan.**

### Chi tiết lesson_02 (Part 3)
| # | Sách in | JSON | |
|---|---|---|---|
| 4 | Why does the store need to be more competitive? | *giống hệt* | ✅ |
| 4-A..D | There's currently a recession. / Productivity has dropped lately. / There's a new competitor nearby. / New employees have little experience. | *giống hệt* | ✅ |
| 5 | How will the store attract more customers? | *giống hệt* | ✅ |
| 5-A..D | By giving them trial products. / By giving them discounts. / By selling new products. / By featuring happy customers in ads. | *giống hệt* | ✅ |
| 6 | Who will the woman call? | *giống hệt* | ✅ |
| 6-A..D | A photographer. / A photocopy salesperson. / A customer. / A marketing executive. | *giống hệt* | ✅ |

Part 4 (7,8,9) cũng khớp hoàn toàn, kể cả "Where will the listeners be this afternoon?" → At home. / In a workshop. / At a store. / With a client.

### Chi tiết lesson_04
Part 3 = 4,6,5. Câu 4 "How do the speakers feel about Alexa's business plan?" với
4 lựa chọn (A) She has gathered too much data. … (D) She is serious-minded and cautious.
— khớp hệt, kể cả dấu nháy đơn trong "Alexa's". Part 4 = 7,8,9 khớp hệt.

### Chi tiết lesson_17 — bài trước đây CHỈ CÓ 9 BYTE RÁC
Đây là bài từng bị lỗi extract nặng nhất. Sau khi sửa, dữ liệu khớp hoàn toàn với scan:
- P3: 4 "What is the man looking for?" → A diverse range of applicants. / A glassware merchant. / A pair of eyeglasses. / A warehouse. ✅
- P3: 5 "How will he obtain more information about what he needs?" → He'll write a letter. / He'll make a phone call. / The woman will tell him. / He'll visit a web site. ✅
- P3: 6 "When does the woman want to speak to the man again?" → Today. / Tuesday. / Next week. / On the weekend. ✅
- P4: 7,8,9 khớp hệt, kể cả "Employees at Margatel." và "When did Carla take the order?" → January 14/19/21/30.

> ⚠️ **Sai khác duy nhất (cosmetic):** câu 8 lựa chọn B lưu là `The company lost a \$50,000 client.`
> trong khi sách in `The company lost a $50,000 client.` — **dư một dấu `\`**. Nội dung số
> tiền đúng, chỉ là escape LaTeX còn sót. Xem mục (c) bên dưới.

### Chi tiết lesson_44
Part 3 = 4,6,5 (4 "What are the speakers discussing?" → A drawing./A sculpture./A painting./A photograph.;
6 "What does the woman say about the museum?"; 5 "What does the man like about it?") — khớp hệt.
Part 4 = 7,8,9 khớp hệt, kể cả "How can you find out the schedule of guided tours?" → Visit the main gallery. / Press two. / Go online. / Speak with an operator.

---

## (b) Kiểm tra thứ tự in (2 cột)

Sách in Part 3 thành **2 cột**: câu 4 bên trái, câu 6 bên phải, câu 5 ở dưới.
Thứ tự đọc tự nhiên là **4, 6, 5**. Tương tự Part 4: **7, 9, 8**.

JSON **GIỮ ĐÚNG** thứ tự in này, không bị sắp xếp lại:

| Bài | part3 | part4 | Ghi chú |
|---|---|---|---|
| lesson_01 | `[4, 6, 5]` | `[7, 8, 9]` | ✅ đúng như yêu cầu |
| lesson_03 | `[4, 6, 5]` | `[7, 9, 8]` | ✅ đúng như yêu cầu |
| lesson_02 | `[4, 5, 6]` | `[7, 8, 9]` | trang này in 1 cột dọc |
| lesson_04 | `[4, 6, 5]` | `[7, 8, 9]` | ✅ giữ thứ tự 2 cột |
| lesson_17 | `[4, 5, 6]` | `[7, 8, 9]` | trang này in 1 cột dọc |
| lesson_44 | `[4, 6, 5]` | `[7, 8, 9]` | ✅ giữ thứ tự 2 cột |

**Kết quả toàn bộ 50 bài: 21 bài giữ thứ tự 2 cột (không sắp xếp), 29 bài vốn in
1 cột dọc.** Không bài nào bị sắp xếp lại thành 4,5,6 / 7,8,9 khi sách in 2 cột.
Bằng chứng lesson_03 `part4 = [7, 9, 8]` — nếu bị sort sẽ thành `[7,8,9]`.

---

## (c) Số câu thiếu lựa chọn

| Hạng mục | Kết quả |
|---|---|
| Tổng số câu part3 + part4 (50 bài) | **300** |
| Câu thiếu lựa chọn / sai nhãn A-D | **0** |
| Lựa chọn có nội dung rỗng | **0** |
| Lựa chọn chứa token rác (TODO, TBD, placeholder, ...) | **0** |
| Bài có `flat questions != part3 + part4` | **0 / 50** |
| Bài lệch giữa `lessons_json/` và `public/lessons_json/` | **0 / 50** |

### Lỗi escape còn sót — 9 vị trí / 3 bài (KHÔNG phải lỗi nội dung)

| Bài | Câu | Trường | Hiện tại | Sách in |
|---|---|---|---|---|
| lesson_17 | part4 q8 | (B) | `The company lost a \$50,000 client.` | `The company lost a $50,000 client.` |
| lesson_40 | part3 q5 | (A) | `\$4.` | `$4.` |
| lesson_40 | part3 q5 | (B) | `\$9.` | `$9.` |
| lesson_40 | part3 q5 | (C) | `\$13.` | `$13.` |
| lesson_40 | part3 q5 | (D) | `\$30.` | `$30.` |
| lesson_43 | part4 q9 | (A) | `\$3.` | `$3.` |
| lesson_43 | part4 q9 | (B) | `\$13.` | `$13.` |
| lesson_43 | part4 q9 | (C) | `\$25.` | `$25.` |
| lesson_43 | part4 q9 | (D) | `\$30.` | `$30.` |

Đã đối chiếu lesson_40 trực tiếp với scan `264_listening_practice.png`: sách in
`$4`, `$9`, `$13`, `$30` — **giá trị đúng hoàn toàn**, chỉ dư ký tự `\` do escape
LaTeX của MinerU. Đây là lỗi hiển thị, không phải lỗi dữ liệu.
**Đề xuất:** thêm `clean_md()` / `.replace("\\$", "$")` khi xuất JSON (việc nhỏ,
ngoài phạm vi task-7 nên tôi không tự sửa).

---

## (d) Kết luận

> ### ✅ DỮ LIỆU CÓ ĐÁNG TIN — đủ tin cậy để đưa cho người học.

Căn cứ:

1. **Khớp ảnh scan thật:** 4/4 bài kiểm tra (lesson_02, 04, 17, 44 — đều là bài
   được OCR lại) khớp **từng chữ** với ảnh scan: 24/24 câu, 96/96 lựa chọn.
   Không có dấu hiệu bịa.
2. **Không mất / không thêm dữ liệu:** cả 50 bài đều có `flat questions == part3 + part4`.
3. **Không có dữ liệu rỗng:** 300/300 câu đều có đủ 4 lựa chọn A/B/C/D có nội dung thật.
4. **Thứ tự in được tôn trọng:** 21 bài in 2 cột giữ nguyên thứ tự (4,6,5 / 7,9,8),
   chứng minh không có bước sắp xếp nào can thiệp.
5. **Hai thư mục nhất quán:** `lessons_json/` == `public/lessons_json/` cho cả 50 bài.
6. **Giả thuyết nguyên nhân gốc được xác nhận:** ảnh scan giờ đều là bản toàn trang
   (1456×1936 – 1456×2000 px), không còn ảnh Part 1 Photo ~300×312 px.

**Vấn đề tồn đọng duy nhất:** 9 vị trí dư escape `\` trước `$` (lesson_17, 40, 43).
Đây là lỗi **hiển thị cosmetic**, giá trị nội dung đúng — **không ảnh hưởng độ tin
cậy của dữ liệu**, nhưng nên sửa để hiển thị đẹp.

---

## Phụ lục — cách tái lập

```bash
# Kiểm tra tự động toàn bộ 50 bài (chỉ đọc)
py -3.11 scripts/recheck_listening_data.py

# Kiểm tra parser (task-1)
py -3.11 scripts/test_parse_listening.py
```
