# Onboarding cho người phát triển và Agent

Đọc [README](<README.md>) để chạy dự án, sau đó đọc [kiến trúc](<docs/ARCHITECTURE.md>) và [đặc tả SRS](<docs/SRS.md>) trước khi sửa luồng học. Repository dùng Git, nhánh triển khai là `main`; thay đổi tài liệu không tự cho phép push hoặc deploy.

## Quy tắc làm việc

1. Kiểm tra working tree trước khi sửa; giữ thay đổi của người dùng. Chia phạm vi ghi khi nhiều Agent làm song song.
2. UI bằng tiếng Việt; từ, định nghĩa và nội dung đề giữ ngôn ngữ của nguồn. Không gán dữ liệu suy luận thành dữ liệu sách.
3. Mỗi từ trong phiên Active Recall có đúng hai câu: từ gốc và một câu context ngẫu nhiên; gộp thành một đánh giá SRS. Không thay bằng hai lịch độc lập.
4. Không đưa thao tác ghi storage vào React state updater. Không tự thay đổi lịch khi luyện thêm hoặc nộp bài thi TOEIC.
5. Không xóa tiến độ để giải quyết lỗi đếm. Test persistence bằng storage giả hoặc profile riêng.
6. Ưu tiên JSON đã cấu trúc. Không nạp toàn bộ PDF/OCR thô vào context. Khi cần đối chiếu nguồn, chọn đúng trang/đoạn và nêu giới hạn kiểm chứng; không suy đoán phần thiếu.
7. Đọc source và dữ liệu hiện hành trước khi tin các số liệu lịch sử. Các báo cáo sinh lại không phải đặc tả API.

## Bản đồ đọc nhanh

- [Kiến trúc và các điểm dễ sai](<docs/ARCHITECTURE.md>)
- [Yêu cầu SRS và trạng thái thực thi](<docs/SRS.md>)
- [Pipeline và nguồn dữ liệu](<docs/DATA.md>)
- [Test, build, deploy và xử lý sự cố](<docs/DEVELOPMENT.md>)
- [Backlog có thứ tự ưu tiên](<docs/BACKLOG.md>)

## Trước khi báo hoàn tất

- Chạy test phù hợp phạm vi và build nếu đổi source ứng dụng; xem [hướng dẫn kiểm chứng](<docs/DEVELOPMENT.md>).
- Nếu đổi pipeline/data, kiểm tra nguồn và bản publish cùng thay đổi; không chạy generator ghi đè hàng loạt chỉ để kiểm tra.
- Nếu đổi luật SRS, cập nhật đặc tả, migration và test hồi quy; không reschedule toàn bộ card cũ ngoài chủ đích.
- Nêu rõ kiểm chứng tĩnh, test chạy thực tế và kiểm chứng trình duyệt/deploy. Không dùng build pass để tuyên bố đã kiểm tra end-to-end.
- Cập nhật một tài liệu chuẩn phù hợp; không thêm báo cáo nháp riêng ở gốc nếu nội dung có thể đưa vào tài liệu sẵn có.
