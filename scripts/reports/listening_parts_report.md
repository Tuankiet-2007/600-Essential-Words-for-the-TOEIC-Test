# Bao cao kiem tra Listening Part 3 / Part 4

Sinh boi `scripts/reports/verify_listening_parts.py` (task-4, cap nhat task-5).

- Ket qua: **DAT** (0 loi, 37 canh bao)
- Bai co cau hoi Part 3/4: **50/50**
- 50/50 (part3=3, part4=3): **50/50**
- flat `listening.questions` == part3 + part4: **50/50**
- Ghim thu tu in: **50/50 OK**

## Thay doi ky vong o task-5

Ky vong cu (13 bai co cau hoi, 37 bai 0/0, rieng L17 la file rac) da **LOI THOI**. Nguyen nhan goc: `scripts/extract_pdf_assets.py` chon anh scan bang `max(pg.images, key=lambda x: len(x.data))` — chon anh NHIEU BYTE NHAT. Anh Part 1 Photo nhung trong trang la JPEG nen nang hon ban scan toan trang (TIFF), nen 37/50 trang `listening_practice` bi luu nham thanh anh Part 1 Photo (~300x312px) thay vi ca trang (~1456x2000px). OCR mot anh chup anh -> khong chu -> rong.
- Da sua `pick_full_page_scan()` chon theo DIEN TICH PIXEL (>=800x800); ca 300 trang scan dung kich thuoc.
- Da OCR lai 37 trang (`scripts/ocr_missing_listening.py`, 37/37 OK).
- Ket qua: **ca 50 bai** deu co part3=3 & part4=3; khong con bai 0/0.
- `lesson_17` gio la du lieu THAT (markdown 1385 bytes), khong con la file rac 9 byte. Da bo ghi chu cu va bo check doi 37 bai 0/0.

Cac check THAT SU van giu nguyen, khong noi long: flat == part3+part4 (so sanh ca noi dung, khong chi so hieu), ghim thu tu in, top-level `listening.part3/part4`, va doi chieu hoi quy voi baseline.

## Ghim thu tu in (bang chung cat theo TIEU DE Part)

So luong 3/3 khong phan biet duoc "cat theo tieu de" voi "cat theo khoang so cau hoi" — chi THU TU moi phan biet duoc. Neu cat theo khoang so thi MOI bai deu ra 4,5,6 / 7,8,9.

- 21/50 bai in Part 3 khong tang dan (4,6,5): [1, 3, 4, 6, 10, 12, 13, 15, 19, 20, 29, 30, 31, 33, 34, 36, 40, 43, 44, 45, 49]
- 1/50 bai in Part 4 khong tang dan: lesson_03 -> 7,9,8

| Lesson | part3 in ra | part3 ky vong | part4 in ra | part4 ky vong | ket qua |
|---:|---|---|---|---|---|
| L01 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L02 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L03 | [4, 6, 5] | [4, 6, 5] | [7, 9, 8] | [7, 9, 8] | OK |
| L04 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L05 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L06 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L07 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L08 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L09 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L10 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L11 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L12 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L13 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L14 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L15 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L16 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L17 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L18 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L19 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L20 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L21 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L22 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L23 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L24 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L25 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L26 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L27 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L28 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L29 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L30 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L31 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L32 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L33 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L34 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L35 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L36 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L37 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L38 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L39 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L40 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L41 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L42 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L43 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L44 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L45 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L46 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L47 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L48 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |
| L49 | [4, 6, 5] | [4, 6, 5] | [7, 8, 9] | [7, 8, 9] | OK |
| L50 | [4, 5, 6] | [4, 5, 6] | [7, 8, 9] | [7, 8, 9] | OK |

`lessonLoader.js` doc `lesson.listening` o CAP CAO NHAT (`const rawListening = lesson.listening || practice.listening || {}`) va uu tien `part3`/`part4` khi co; chi khi thieu moi roi ve cach cat theo khoang so 4-6 / 7-9. Vi vay JSON publish phai co part3/part4 o CAP CAO NHAT — da assert o tren.

## Bang chi tiet

| Lesson | has text | part3 count | part4 count | part3 numbers | part4 numbers |
|---:|:---:|---:|---:|---|---|
| L01 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L02 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L03 | yes | 3 | 3 | [4, 6, 5] | [7, 9, 8] |
| L04 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L05 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L06 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L07 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L08 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L09 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L10 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L11 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L12 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L13 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L14 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L15 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L16 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L17 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L18 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L19 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L20 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L21 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L22 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L23 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L24 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L25 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L26 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L27 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L28 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L29 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L30 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L31 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L32 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L33 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L34 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L35 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L36 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L37 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L38 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L39 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L40 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L41 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L42 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L43 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L44 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L45 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L46 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L47 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L48 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |
| L49 | yes | 3 | 3 | [4, 6, 5] | [7, 8, 9] |
| L50 | yes | 3 | 3 | [4, 5, 6] | [7, 8, 9] |

## Doi chieu baseline (`baseline_before_part_fix.json`)

| Chi so | before | after | chenh lech |
|---|---:|---:|---|
| words | 599 | 599 | khong doi |
| examples | 1197 | 1197 | khong doi |
| family | 883 | 883 | khong doi |
| bank | 602 | 602 | khong doi |
| blanks | 597 | 597 | khong doi |
| listening_questions | 78 | 300 | +222 |

| Lesson | Chi so | before | after | huong |
|---:|---|---:|---:|---|
| L02 | listening_questions | 0 | 6 | TANG |
| L04 | listening_questions | 0 | 6 | TANG |
| L05 | listening_questions | 0 | 6 | TANG |
| L06 | listening_questions | 0 | 6 | TANG |
| L07 | listening_questions | 0 | 6 | TANG |
| L08 | listening_questions | 0 | 6 | TANG |
| L09 | listening_questions | 0 | 6 | TANG |
| L12 | listening_questions | 0 | 6 | TANG |
| L13 | listening_questions | 0 | 6 | TANG |
| L14 | listening_questions | 0 | 6 | TANG |
| L15 | listening_questions | 0 | 6 | TANG |
| L16 | listening_questions | 0 | 6 | TANG |
| L17 | listening_questions | 0 | 6 | TANG |
| L18 | listening_questions | 0 | 6 | TANG |
| L20 | listening_questions | 0 | 6 | TANG |
| L21 | listening_questions | 0 | 6 | TANG |
| L24 | listening_questions | 0 | 6 | TANG |
| L25 | listening_questions | 0 | 6 | TANG |
| L28 | listening_questions | 0 | 6 | TANG |
| L29 | listening_questions | 0 | 6 | TANG |
| L30 | listening_questions | 0 | 6 | TANG |
| L31 | listening_questions | 0 | 6 | TANG |
| L32 | listening_questions | 0 | 6 | TANG |
| L34 | listening_questions | 0 | 6 | TANG |
| L35 | listening_questions | 0 | 6 | TANG |
| L36 | listening_questions | 0 | 6 | TANG |
| L38 | listening_questions | 0 | 6 | TANG |
| L39 | listening_questions | 0 | 6 | TANG |
| L40 | listening_questions | 0 | 6 | TANG |
| L41 | listening_questions | 0 | 6 | TANG |
| L42 | listening_questions | 0 | 6 | TANG |
| L43 | listening_questions | 0 | 6 | TANG |
| L44 | listening_questions | 0 | 6 | TANG |
| L45 | listening_questions | 0 | 6 | TANG |
| L46 | listening_questions | 0 | 6 | TANG |
| L47 | listening_questions | 0 | 6 | TANG |
| L50 | listening_questions | 0 | 6 | TANG |

## Canh bao

- L02.listening_questions: 0 -> 6 (tang)
- L04.listening_questions: 0 -> 6 (tang)
- L05.listening_questions: 0 -> 6 (tang)
- L06.listening_questions: 0 -> 6 (tang)
- L07.listening_questions: 0 -> 6 (tang)
- L08.listening_questions: 0 -> 6 (tang)
- L09.listening_questions: 0 -> 6 (tang)
- L12.listening_questions: 0 -> 6 (tang)
- L13.listening_questions: 0 -> 6 (tang)
- L14.listening_questions: 0 -> 6 (tang)
- L15.listening_questions: 0 -> 6 (tang)
- L16.listening_questions: 0 -> 6 (tang)
- L17.listening_questions: 0 -> 6 (tang)
- L18.listening_questions: 0 -> 6 (tang)
- L20.listening_questions: 0 -> 6 (tang)
- L21.listening_questions: 0 -> 6 (tang)
- L24.listening_questions: 0 -> 6 (tang)
- L25.listening_questions: 0 -> 6 (tang)
- L28.listening_questions: 0 -> 6 (tang)
- L29.listening_questions: 0 -> 6 (tang)
- L30.listening_questions: 0 -> 6 (tang)
- L31.listening_questions: 0 -> 6 (tang)
- L32.listening_questions: 0 -> 6 (tang)
- L34.listening_questions: 0 -> 6 (tang)
- L35.listening_questions: 0 -> 6 (tang)
- L36.listening_questions: 0 -> 6 (tang)
- L38.listening_questions: 0 -> 6 (tang)
- L39.listening_questions: 0 -> 6 (tang)
- L40.listening_questions: 0 -> 6 (tang)
- L41.listening_questions: 0 -> 6 (tang)
- L42.listening_questions: 0 -> 6 (tang)
- L43.listening_questions: 0 -> 6 (tang)
- L44.listening_questions: 0 -> 6 (tang)
- L45.listening_questions: 0 -> 6 (tang)
- L46.listening_questions: 0 -> 6 (tang)
- L47.listening_questions: 0 -> 6 (tang)
- L50.listening_questions: 0 -> 6 (tang)
