# Backlog và giới hạn đã biết

Rà soát tài liệu ngày 17/11/2026. Đây là việc chưa hoàn tất, không phải tính năng đã triển khai. [README](<../README.md>) · [SRS](<SRS.md>)

## Ưu tiên cao

| Việc | Điều kiện hoàn tất |
|---|---|
| Khóa API trong backup | Export mặc định bỏ khóa, import không ghi đè khóa ngoài chủ đích; test hai chiều. Hiện settings vẫn có thể chứa khóa trong JSON backup. |
| CI và deploy | Nâng Node workflow phù hợp Vite 8/test runner, chạy test trước deploy, xác minh run đúng commit và URL Pages. |
| Dữ liệu gốc thiếu | Đối chiếu `secure` L31 thiếu EN, từ thiếu L15, đáp án/tapescript còn thiếu bằng nguồn xác thực; báo coverage, không bịa. |
| Giao dịch persistence | Import nhiều khóa có rollback/journal; mọi đường review phối hợp khóa/version; test quota và hai cửa sổ, không mất tiến độ. |
| Kiểm thử browser SRS | Cold load đủ N từ/2N câu, reload draft, retry sau lỗi, StrictMode, focus, cutoff, reset/import và mobile. Test Node hiện chưa chứng minh hết các trường hợp này. |

## Hoàn thiện học tập

- Cho chủ động ôn phần đủ dữ liệu khi có từ bị chặn; giữ số tổng/số bị chặn rõ ràng.
- Pool context từ nhiều phần bộ đề hơn, liên kết đáp án với wordKey, tránh lặp câu giữa các phiên và giữ provenance.
- Cải thiện draft khi crash đúng giữa commit và lưu draft; hợp nhất schema session và kiểm tra draft chặt hơn.
- Thiết kế Learning/Relearning riêng trong UI nếu cần; không để số bước làm tăng mẫu số hai câu cơ sở.
- Cân nhắc thư viện FSRS đã kiểm thử, cấu hình retention, daily limits, fuzz, leech/suspend và undo. Không thay thuật toán/reschedule hàng loạt mà thiếu kế hoạch migration.
- Rà lại nhãn `Thuộc lòng` (hiện interval>=7, chưa due). Đề xuất `Ôn ổn định`; đổi mốc là quyết định sản phẩm riêng.

## UI được đề xuất để duyệt

- Rút tiêu đề `Nghĩa tiếng Anh (Gõ từ gốc)` thành `Từ gốc`, `Điền từ vào câu` thành `Điền từ`.
- Một dòng tiến độ chính, giảm chữ in hoa và độ đậm ở thông tin phụ.
- Đưa bắt đầu lại vào menu phụ để giảm bấm nhầm; giữ nhãn truy cập được cho nút icon.
- Kiểm focus bàn phím, thông báo đúng/sai không chỉ dùng màu, input khi bàn phím ảo mở, bảng họ từ và Part 7 trên màn hình hẹp.

## Hiệu năng và vận hành

Đo tải thực tế trước khi tối ưu audio. Upload toàn bộ MP3 trong artifact không có nghĩa browser tải toàn bộ lúc mở trang. Kiểm `preload` và network waterfall, sau đó mới thay bitrate/lazy loading. Không dùng dung lượng đo từ báo cáo cũ làm số liệu hiện tại.

Tiến độ hiện local theo origin; cloud sync và thông báo khi app đóng chưa có. Chỉ triển khai khi có yêu cầu rõ, gồm xử lý xung đột, quyền thông báo và bảo vệ dữ liệu.
