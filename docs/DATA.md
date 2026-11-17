# Dữ liệu và pipeline

[README](<../README.md>) · [Kiến trúc](<ARCHITECTURE.md>) · [Backlog](<BACKLOG.md>)

## Nguồn và bản publish

| Đường dẫn | Vai trò |
|---|---|
| [Bản đồ sách](<../book_structure_map.json>) | Ánh xạ trang/section |
| `lessons_json/` | JSON bài nguồn |
| `public/lessons_json/` | Bản web thực sự tải |
| `scripts/data/` | Nguồn answer key, explanations, tapescripts, enrichment |
| `public/answers/` | Bản publish đáp án/giải thích/lời thoại |
| `public/audio/`, `public/part1_photos/` | MP3 và ảnh phục vụ trên web |
| `sample_lessons/`, `public/sample_lessons/` | Bài mẫu/fallback |

Dữ liệu sách, dữ liệu bổ sung và dữ liệu suy ra phải giữ provenance. Answer Key là nguồn ưu tiên cho đáp án; không sửa đáp án theo một lời giải suy đoán. Khi nguồn chưa đủ, ghi thiếu và không tính câu đó như đáp án sai của người học.

## Hiện trạng và khoảng trống

Đợt kiểm tra SRS 17/11/2026 đọc 50 JSON bài, đếm 599 từ. `secure` ở bài 31 có ví dụ nhưng thiếu `definition_en`; bài 15 thiếu một mục từ do OCR. Không tự bịa định nghĩa hoặc thêm từ để ép tổng thành 600.

Các báo cáo trước ghi thiếu đáp án L08 câu 5–6 và một phần tapescript. Đây là thông tin cần tái kiểm bằng công cụ khi sửa dữ liệu, không coi các tổng 966/968 hoặc 34/50 trong báo cáo lịch sử là số luôn đúng. Bản dịch/IPA/collocations đã có enrichment ở nhiều mục; không tiếp tục mô tả tất cả đều rỗng.

Word families không bắt buộc mỗi từ có đủ bốn dạng. Từ loại có thể do sách hoặc suy luận; giữ nhãn nguồn. Số dòng khác 18 chỉ là tín hiệu kiểm tra, không đủ để kết luận sách thiếu hoặc OCR sai.

## Nghĩa ngắn Word Family

Các bảng họ từ dùng `meaning_vi` (nghĩa ngắn), tách khỏi `vi` có thể là bản dịch câu ví dụ. Nghĩa là dữ liệu bổ sung tiếng Việt, không gán là nội dung sách. Nguồn được duy trì trong bốn tệp `scripts/data/family_gloss_*.json` theo khoảng bài; có 2.092 ánh xạ theo bài/từ loại/từ. Chạy `python scripts/apply_family_glosses.py` để validate toàn bộ trước khi áp dụng sang nguồn, bản publish và bài mẫu. `build_vocab_enrichment.py` gọi lại bước này sau khi thay extra_families. Nếu OCR lại bằng đường khác, chạy enrichment/gloss publish sau đó.

UI hiển thị nghĩa dưới từ ở sổ tay, Flashcard và phần lý thuyết SRS. Gợi ý SRS dùng nghĩa của từ gốc, hoặc nghĩa riêng của dạng họ từ nếu câu context yêu cầu dạng đó.

## Shape nguồn và chuẩn hóa

- Listening có thể nằm cấp bài; practice có `part5`, `part6`, `part7`.
- Options nguồn có thể là `[{label,text}]`; key câu nguồn thường là `number`.
- Part 7 có nhiều block; không giả định chỉ một passage.
- Sách có bố cục hai cột, có thể in thứ tự 4,6,5 hoặc 7,9,8. Giữ thứ tự nguồn, không sort cho đẹp.
- Dùng [loader](<../app/src/lib/lessonLoader.js>) để chuẩn hóa trước khi UI đọc.

## Tái tạo dữ liệu

Dữ liệu đã có; các lệnh dưới đây chỉ dùng khi chủ đích OCR/publish lại. Đọc script trước khi chạy vì nhiều công cụ ghi đè JSON hoặc báo cáo.

```powershell
# Từ repo root; cần Python/dependencies tương ứng đã cài
python scripts/extract_pdf_assets.py
python scripts/convert_available_lessons.py
python scripts/patch_missing.py --dry-run
python scripts/run_ocr_pipeline.py --validate
```

MinerU/Windows OCR dùng các launcher trong `scripts/`; đường dẫn cài công cụ phụ thuộc máy, không có môi trường MinerU mặc định cho mọi người. Chỉ kiểm đúng trang/section cần thiết thay vì mở toàn bộ dump OCR.

Sau khi sửa nguồn, publish bằng bước có sẵn trong generator hoặc copy có chủ đích sang `public/`. Không chỉ sửa bản web vì lần sinh sau có thể làm mất bản vá. Các bản vá thủ công phải ghi nguồn ảnh/trang và cách kiểm chứng.

Các script kiểm tra: [parser listening](<../scripts/test_parse_listening.py>), [answer key](<../scripts/test_answer_key.py>), [tapescript](<../scripts/test_tapescripts.py>), [giải thích](<../scripts/validate_explanations.py>), [coverage](<../scripts/coverage_report.py>), [listening parts](<../scripts/reports/verify_listening_parts.py>). Một số script có thể sinh file trước khi trả mã lỗi vì dữ liệu thiếu; đọc hành vi trước khi chạy trong working tree đang có thay đổi.

## Báo cáo sinh tự động

Giữ [báo cáo listening](<../scripts/reports/listening_parts_report.md>) ở đường dẫn generator đang ghi; nội dung là snapshot lần chạy, không phải đặc tả sản phẩm. Giữ [baseline JSON](<../scripts/reports/baseline_before_part_fix.json>) để phục vụ kiểm tra hồi quy. Không xóa báo cáo rồi tạo lại với số xanh nếu chưa thực sự chạy kiểm chứng.

Kinh nghiệm cần giữ từ các báo cáo cũ: chọn ảnh scan theo diện tích pixel thay vì byte; parser phải giữ state qua ranh giới trang; chỉ loại token OCR nhiễu thay vì xóa cả khối lời thoại; escape ký tự như `\$` cần được xử lý ở pipeline và kiểm tra hiển thị.
