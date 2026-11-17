# 600 Essential Words for the TOEIC

Ứng dụng học từ vựng theo ngữ cảnh từ *Barron's 600 Essential Words for the TOEIC*: sổ tay từ, Flashcard, ôn tập SRS, AI Sentence Lab và luyện đề nghe/đọc.

- [Mở ứng dụng](https://tuankiet-2007.github.io/600-Essential-Words-for-the-TOEIC-Test/)
- [Repository](https://github.com/Tuankiet-2007/600-Essential-Words-for-the-TOEIC-Test)

## Bắt đầu

Cần Node.js tương thích với Vite 8 (khuyến nghị Node 24.15+ hoặc 26+) và npm. Dữ liệu đã có sẵn; không cần chạy OCR để dùng ứng dụng.

```powershell
cd app
npm ci
npm run dev
```

Mở URL Vite in ra terminal. Cổng mặc định là 5173 nhưng có thể đổi khi đang được dùng.

```powershell
# Chạy trong app/
npm test
npm run lint
npm run build
```

Nếu môi trường Windows/sandbox chặn trình nạp config Vite bằng `spawn EPERM`, có thể dùng `npm run dev:sandbox` hoặc `npm run build:sandbox`. Đây là đường chạy thay thế; không phải yêu cầu của mọi máy.

## Tài liệu

| Nhu cầu | Tài liệu |
|---|---|
| Agent/người phát triển mới | [Onboarding](<ONBOARDING.md>) |
| Kiến trúc, API và lưu trữ | [Kiến trúc](<docs/ARCHITECTURE.md>) |
| Luật học hai lượt/từ, scheduler và nghiệm thu | [Đặc tả SRS](<docs/SRS.md>) |
| Nguồn dữ liệu, OCR và dữ liệu thiếu | [Dữ liệu](<docs/DATA.md>) |
| Chạy test và phát hành GitHub Pages | [Vận hành](<docs/DEVELOPMENT.md>) |
| Các việc chưa hoàn tất | [Backlog](<docs/BACKLOG.md>) |

## Cấu trúc chính

```text
app/src/           React: UI, loader, SRS và LocalStorage
app/scripts/       Dev/build và test JavaScript
public/            Tài nguyên được phục vụ: JSON, audio, ảnh, đáp án
lessons_json/      Dữ liệu bài nguồn trước publish
scripts/           Pipeline OCR, enrichment và kiểm tra dữ liệu
scripts/data/      Nguồn đáp án, giải thích, tapescript, enrichment
docs/              Tài liệu được duy trì
scripts/reports/   Báo cáo sinh bởi công cụ và baseline dữ liệu
```

`publicDir` trỏ tới thư mục `public/` ở gốc repository, không phải `app/public/`. Dữ liệu hiện có 50 bài và 599 mục từ; tên sản phẩm “600” không phải cam kết corpus đã đủ 600 từ.

Tiến độ được lưu trên trình duyệt/origin hiện tại. Localhost và GitHub Pages không tự chia sẻ tiến độ. Dùng sao lưu/khôi phục khi chuyển máy hoặc origin; bản sao lưu hiện có thể chứa khóa API đã cấu hình, cần giữ riêng tư.

Tài liệu mô tả trạng thái mã nguồn được rà soát ngày 17/11/2026. Test/build đạt không đồng nghĩa đã xác minh giao diện đang triển khai hoặc toàn bộ nội dung sách.
