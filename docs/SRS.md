# Đặc tả học từ và SRS

Cập nhật 17/11/2026. Đây là tài liệu chuẩn cho Agent sửa tính năng; phân biệt **yêu cầu sản phẩm**, **hành vi hiện có** và **phần chưa hoàn tất**. [README](<../README.md>) · [Kiến trúc](<ARCHITECTURE.md>) · [Backlog](<BACKLOG.md>)

## Yêu cầu sản phẩm bắt buộc

Mỗi từ trong một vòng Active Recall có đúng hai câu trong cùng phiên:

1. `base_word`: gõ từ gốc từ định nghĩa tiếng Anh.
2. `context_word`: điền từ vào một câu ngẫu nhiên trong corpus/bộ đề liên quan từ đó; có thể là dạng chia thì hoặc họ từ đã liên kết rõ với từ gốc.

Hai câu được gộp thành **một đánh giá SRS cho từ**. Không tạo hai lịch độc lập, không giấu một câu sang hôm sau để mô phỏng bury siblings của Anki. Lần thử gõ lại không phải câu cơ sở mới; bước học lại không phải một review ngày độc lập.

| Đại lượng | Định nghĩa |
|---|---|
| Từ đến hạn | Từ trong danh mục có card và `isDue` |
| Từ của phiên | Snapshot cố định tại lúc khởi tạo |
| Câu của phiên | Hai câu cho mỗi từ đủ dữ liệu |
| Từ đã kiểm tra | Đã kết thúc cả hai câu và lưu commit thành công; không đồng nghĩa đã thuộc |

Ví dụ **16 từ = 32 câu**: Dashboard ghi `16 từ đến hạn · 32 câu`; phiên ghi `Đã kiểm tra 0/16 từ · Câu 1/32`. Progress theo từ chỉ tăng khi cặp câu được chốt. Vị trí câu hiện tại bắt đầu 1; số câu đã trả lời bắt đầu 0.

## Tạo phiên và nguồn câu

[Tab3Srs](<../app/src/tabs/Tab3Srs.jsx>) chờ tải đủ 50 bài trước khi tạo phiên; không dùng 5/6 từ tải sớm rồi yêu cầu người dùng bấm làm lại. Due rỗng phải hiện hoàn tất, không tự lấy từ chưa đến hạn hoặc từ mới. Theo bài/chủ đề/từ đã học là **luyện thêm**, không đổi lịch SRS.

[Helper](<../app/src/lib/recallSession.js>) sinh UID ổn định theo từ, loại câu và sessionId; shuffle giữ đúng một base và một context mỗi từ. Lựa chọn random được giữ trong draft của phiên, không đổi sau reload.

Cả hai loại câu hiển thị gợi ý nghĩa tiếng Việt. Câu từ gốc dùng `definition_vi`; câu họ từ ưu tiên `meaning_vi` riêng của dạng đang hỏi, còn câu khác dùng nghĩa từ gốc thay vì nguyên bản dịch câu. Draft cũ thiếu hint có fallback nghĩa từ gốc.

Pool hiện gồm `srs_sentence`, ví dụ bài và word families được truyền vào helper. Candidate phải có đáp án và cloze hợp lệ; lưu nguồn/ID nguồn/bài nguồn. Không gọi AI để tạo câu thay dữ liệu thiếu khi đang ôn. Chưa có pool bao phủ mọi phần đề thi hoặc cơ chế tránh lặp candidate giữa các phiên.

Nếu thiếu định nghĩa/câu context, không sinh cặp rỗng, không dời due hay giả vờ đã hoàn tất. **Hiện tại** UI chặn phiên và liệt kê mục thiếu. **Đích tiếp theo**: có thể cho người học chủ động chọn ôn phần đủ, ví dụ 14 từ/28 câu và 1 từ bị chặn, nhưng phải báo rõ vẫn còn từ thiếu dữ liệu. Không mô tả khả năng này là đã triển khai.

## Chấm và commit

Mỗi câu cho tối đa hai lần gửi đáp án không rỗng. Đúng thì kết thúc; sai lần đầu cho nhập lại, sai lần hai kết thúc thất bại. Chuẩn hóa hoa/thường, khoảng trắng, dấu câu cuối và các biến thể đã khai báo; không tự nhận từ gần giống là đúng.

| Kết quả hai câu | Grade tự động hiện dùng |
|---|---|
| Cả hai cuối cùng đúng trong giới hạn thử | Good (3) |
| Một hoặc hai câu thất bại | Again (1) |

Không tự cho Easy chỉ vì gõ đúng lần đầu. Flashcard vẫn cho tự đánh giá Again/Hard/Good/Easy sau khi lật. Easy trong Active Recall cần một thiết kế đánh giá nỗ lực riêng nếu bổ sung sau.

- Chỉ commit sau đủ hai UID khác loại; callback cùng UID không tính hai lần.
- Commit nằm ngoài React updater. ID cặp của implementation là `${sessionId}:${wordKey}`; `recordReview` lưu processed IDs, version và log cùng card trong một SRS write.
- `expectedVersion` phát hiện snapshot cũ; Web Locks được dùng ở đường Active Recall khi có hỗ trợ. Chưa có khóa giao dịch cho mọi đường ghi/nhiều cửa sổ.
- Lưu thành công mới tăng bộ đếm từ. Lưu lỗi giữ câu, báo lỗi, thử lại cùng ID để không tăng reps lần nữa.
- Draft lưu câu, kết quả, cursor, version và các từ đã commit. Khôi phục kiểm tra version/ID; reset hoặc thay đổi từ cửa sổ khác có xử lý vô hiệu phiên. Việc khôi phục mọi trường hợp crash/concurrency vẫn cần kiểm thử trình duyệt.
- Chỉ nộp thi TOEIC thì ghi lịch sử thi; tuyệt đối không chấm SRS toàn bộ từ của bài.

## Scheduler hiện có

[Scheduler](<../app/src/lib/srs.js>) là **SM-2 tùy biến có bước học**, không phải bản sao Anki hoặc FSRS. `schedulerVersion` hiện là `sm2-stages-v2`; card cũ không bị reschedule hàng loạt.

| Trạng thái | Hành vi hiện có |
|---|---|
| New | Again → Learning 1 phút; Hard/Good → Learning 10 phút; Easy → Review 4 ngày |
| Learning | Again về bước 0 sau 1 phút; Hard ở bước học 10 phút; Good ở bước 0 sang bước 1 sau 10 phút; Good khi bước 1 đến hạn → Review 1 ngày |
| Review | Again → Relearning 1 phút, tăng lapse, giảm ease 0.2; Hard kéo dài tối thiểu 1 ngày và khoảng 1.2× interval; Good/Easy dùng nhánh SM-2 hiện có |
| Relearning | Again 1 phút; Good/Hard theo bước 10 phút; tốt nghiệp giữ tối thiểu 1 ngày, khoảng nửa interval cũ |

Review không đến hạn là practice: giữ due/ease/interval/reps. Nếu gọi API trực tiếp, practice vẫn có thể được ghi log/version; UI luyện thêm tránh gọi scheduler mặc định. Ease khởi đầu 2.5, sàn 1.3; review Hard giảm 0.15, Easy tăng 0.1; interval review giới hạn 365 ngày.

Learning/Relearning so timestamp. Review so ngày học địa phương bắt đầu **04:00**. Khi tạo due phải cộng interval từ ngày hiệu dụng, không từ ngày dân sự:

```text
Ôn 01:00 ngày 16/11 → ngày học 15/11
interval 1 ngày → due 04:00 ngày 16/11
```

04:00 hiện hard-code. Múi giờ theo thiết bị; đổi timezone/DST chưa có bộ test đầy đủ. Store cập nhật đồng hồ theo due/cutoff, tối đa mỗi phút và khi focus.

## Nhãn trên Dashboard

Code ưu tiên kiểm due: đến hạn → `Cần ôn`; chưa đến hạn và interval >=7 → `Thuộc lòng`; còn lại → `Đang nhớ`; không có card → `Chưa học`.

“Thuộc lòng” hiện là nhãn interval, không chứng minh nhớ vĩnh viễn và không đồng nghĩa mature trong Anki. Đề xuất đổi thành `Ôn ổn định`; chưa tự đổi mốc 7 ngày hay dùng mốc 21 ngày. Bỏ dấu đã học không xóa lịch trí nhớ đã có.

## Test và điều kiện nghiệm thu

Chạy trong `app/`: `npm test`. [Bộ test](<../app/scripts/srs.test.mjs>) hiện có 15 ca, gồm cặp 15 từ/30 câu, dữ liệu thiếu, callback trùng, cutoff, dedupe, version conflict, học theo phút, ôn sớm, dữ liệu hỏng/import và quota. Lần chạy ngày 17/11/2026: 15/15 đạt; build đạt. Đây chưa phải chứng nhận browser end-to-end hoặc deploy hiện tại.

Các tình huống phải kiểm chứng khi sửa tiếp:

- Cold load đủ bài; due rỗng; cùng snapshot Dashboard và phiên có số từ khớp nhau.
- Chốt một câu chưa thay đổi lịch; đủ hai câu chỉ commit một lần, kể cả StrictMode/callback lặp.
- Reload giữa cặp, sau commit và trong lúc lỗi lưu; không đổi câu/không nhảy interval.
- 03:59/04:00, cuối tháng/năm, đổi timezone và DST.
- Nộp thi không đổi SRS; luyện thêm không đổi lịch.
- Nhiều cửa sổ/reset/import không mất hoặc hồi sinh tiến độ cũ.
- UI bàn phím/mobile, bộ đếm từ/câu, due tiếp theo và trạng thái thiếu dữ liệu.

## Giới hạn và tham khảo

Từ `secure` bài 31 thiếu định nghĩa EN nên bị báo thiếu dữ liệu; corpus là 599 mục từ. Chưa có FSRS, fuzz lịch, giới hạn ngày, leech/suspend hay undo đầy đủ. Import nhiều khóa có thể dở dang khi ghi thất bại; xem [backlog](<BACKLOG.md>).

Tham khảo chính thức: [Anki Studying](https://docs.ankiweb.net/manual/studying), [Deck Options](https://docs.ankiweb.net/manual/deck-options), [Preferences](https://docs.ankiweb.net/manual/preferences). Anki cho cấu hình learning/relearning và hỗ trợ cả legacy SM-2 lẫn FSRS. Quy tắc hai câu/một từ là yêu cầu riêng của sản phẩm này.
