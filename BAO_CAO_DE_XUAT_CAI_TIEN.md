 # Báo cáo rà soát và đề xuất cải thiện dự án TOEIC 600

**Ngày rà soát:** 09/11/2026  
**Phạm vi:** Tài liệu dự án, mã nguồn ứng dụng React/Vite, quản lý dữ liệu, pipeline OCR, tài nguyên `public/` và workflow GitHub Actions. Không mở PDF gốc hoặc thư mục `extracted_data/` theo quy tắc của dự án. Đây là đánh giá tĩnh; không chạy build hay test trong lượt rà soát này.

## 1. Tóm tắt

Dự án đã có nền tảng sản phẩm tốt: 50 bài học, 10 chủ đề, 5 khu vực học, SRS, luyện đề, lưu tiến độ, ghi chú, sao lưu/khôi phục, cùng pipeline OCR và nhiều script kiểm tra. Điểm mạnh đáng giữ là hướng **Context-First**, xử lý dữ liệu thiếu có ghi nhận thay vì tự bịa, và các hợp đồng dữ liệu/tài liệu onboarding khá chi tiết.

Các cải tiến nên ưu tiên tiếp theo là bảo vệ khóa API, giảm dung lượng tải khi triển khai, đưa kiểm tra hiện có vào CI, hoàn tất/hiển thị minh bạch phần dữ liệu đề còn thiếu, và củng cố độ tin cậy của lưu trữ tiến độ. Đây là các đề xuất; lượt rà soát này chưa chỉnh sửa chức năng ứng dụng.

## 2. Phát hiện và đề xuất theo ưu tiên

### Ưu tiên cao — Khóa API bị đưa vào bản sao lưu

`app/src/lib/storage.js` lưu Gemini/OpenAI API key trong LocalStorage. Hàm `exportAllData()` xuất nguyên `settings`, nên file sao lưu có thể chứa khóa API ở dạng đọc được. Màn hình Cài đặt cho phép tải file này về và chia sẻ/di chuyển; người dùng có thể vô tình gửi khóa cùng tiến độ học.

**Đề xuất:** loại `geminiKey` và `openaiKey` khỏi bản export mặc định; khi import, bỏ qua các trường khóa từ file. Thêm tùy chọn xuất khóa riêng có cảnh báo rõ nếu thực sự cần chuyển. Cân nhắc lưu khóa tách biệt khỏi dữ liệu học và cung cấp nút xóa khóa. Vì ứng dụng chạy trực tiếp trên trình duyệt, không thể bảo vệ khóa khỏi mã độc chạy cùng origin; cần nêu rõ điều đó trong hướng dẫn.

**Tiêu chí hoàn thành:** file backup mặc định không có API key; import backup không ghi đè khóa đã cấu hình; có kiểm tra hồi quy cho hai trường hợp này.

### Ưu tiên cao — Bản deploy có lượng tài nguyên tĩnh lớn

Thư mục `public/audio/` có 50 tệp, tổng khoảng **136.4 MB** theo kiểm kê tại thời điểm rà soát. Toàn bộ thư mục public có khoảng 144 MB. Cách triển khai GitHub Pages hiện tải lên toàn bộ bản build, vì vậy audio là phần lớn dung lượng phát hành và có thể làm chậm lần tải đầu hoặc gây khó khăn khi cập nhật.

**Đề xuất:** bật nén/bitrate phù hợp cho lời thoại, kiểm tra chất lượng âm thanh trước/sau; chỉ tải audio của bài đang học hoặc tải theo yêu cầu; đặt preload audio mặc định thành `none`/`metadata`; xem xét tách audio thành gói/tài nguyên tải riêng nếu hosting cho phép. Ghi lại kích thước build và mục tiêu dung lượng để tránh tăng âm thầm.

**Tiêu chí hoàn thành:** trang đầu không tải hàng loạt audio; phát bài hiện tại vẫn ổn định; có số liệu dung lượng trước/sau và không suy giảm chất lượng nghe đáng kể.

### Ưu tiên cao — CI chưa chạy các kiểm tra đã có

`.github/workflows/deploy.yml` cài Node, chạy `npm ci`, `npm run build`, rồi deploy. Trong khi đó README/ONBOARDING liệt kê nhiều kiểm tra runtime, loader, tabs, giải thích, helper và dữ liệu. Như vậy lỗi dữ liệu hoặc hồi quy giao diện có thể lọt tới nhánh deploy nếu chỉ dựa vào build.

**Đề xuất:** tách workflow thành bước kiểm tra và bước deploy phụ thuộc kiểm tra thành công. Thêm các kiểm tra Node/Python phù hợp vào CI; pin phiên bản Python cần thiết và chỉ cài dependency tối thiểu. Với các script chủ ý trả exit code khác 0 khi còn dữ liệu nguồn thiếu, quy định rõ ngưỡng/allowlist để CI phân biệt thiếu đã biết với lỗi mới.

**Tiêu chí hoàn thành:** pull request chạy được các kiểm tra cốt lõi; deploy chỉ chạy khi kiểm tra đạt; log nêu rõ lỗi theo tầng.

### Ưu tiên cao — Độ phủ đề và audio transcript chưa trọn vẹn

Tài liệu onboarding ghi nhận 966/968 câu có đáp án/giải thích; còn thiếu đáp án bài 8 câu 5–6. Tapescript hiện có 34/50 bài. Hai khoảng trống này ảnh hưởng trực tiếp đến tự chấm và phần giải thích nghe.

**Đề xuất:** duy trì trạng thái thiếu rõ trong giao diện, phân biệt “không có đáp án nguồn” với “người học chưa trả lời”; thêm trang tổng quan độ phủ dữ liệu theo bài/part. Với tapescript, chỉ bổ sung từ nguồn đáng tin cậy và ghi nguồn/trạng thái xác minh; không sinh nội dung thay thế bằng suy đoán. Nếu chưa thể khôi phục đáp án L08, giữ câu ở chế độ tự đối chiếu hoặc không tính vào điểm tối đa.

**Tiêu chí hoàn thành:** số liệu coverage được sinh tự động; UI không làm người học tưởng câu thiếu đáp án là câu sai; thay đổi dữ liệu có truy xuất nguồn.

### Ưu tiên trung bình — Lưu trữ LocalStorage có thể mất trạng thái âm thầm

`write()` trong `storage.js` bắt lỗi nhưng chỉ trả `false`; nhiều hàm gọi bỏ qua kết quả. Khi trình duyệt hết quota hoặc chặn lưu trữ, UI vẫn có thể hoạt động như thể tiến độ đã được lưu. Import backup cũng ghi từng nhóm dữ liệu riêng lẻ, có thể để trạng thái khôi phục dở dang.

**Đề xuất:** đưa trạng thái lưu thành thông tin quan sát được trong UI (đã lưu/lỗi lưu); kiểm tra kết quả ghi và thông báo khi thất bại; validate phiên bản/schema backup trước khi áp dụng; khôi phục theo kiểu all-or-nothing hoặc sao lưu trạng thái hiện tại để rollback nếu một bước lỗi. Thêm nút kiểm tra/khôi phục bản backup gần nhất nếu thiết kế phù hợp.

### Ưu tiên trung bình — Kiểm tra tính hợp lệ dữ liệu JSON còn nông ở runtime

`lessonLoader.isValidLesson()` hiện chỉ xác nhận có mảng `words_to_learn` không rỗng. Các lỗi sâu hơn như số từ bất thường, câu thiếu, đáp án không nằm trong lựa chọn hoặc trường sai kiểu có thể chỉ lộ khi người học vào đúng phần.

**Đề xuất:** tạo schema kiểm tra dữ liệu dùng chung trong pipeline trước publish và một bộ kiểm tra nhẹ cho runtime. Không bắt buộc mọi bài đủ dữ liệu hoàn hảo; nên phân loại cảnh báo theo mức độ, ví dụ cấu trúc lỗi, dữ liệu thiếu được biết trước, và nội dung cần người duyệt. Gắn `data_version` hoặc `schema_version` cho JSON để việc nâng cấp dễ kiểm soát.

### Ưu tiên trung bình — Khả năng dùng và tiếp cận trên thiết bị nhỏ

Ứng dụng có nhiều chức năng và Tab 5 được mô tả là phần phức tạp/lớn nhất. Đây là khu vực dễ phát sinh thao tác khó trên màn hình hẹp, bàn phím ảo, hoặc trình đọc màn hình.

**Đề xuất:** rà soát luồng học trên mobile: kích thước vùng chạm, cuộn audio/tapescript, bảng và split-screen Part 7, focus khi mở/đóng modal, trạng thái đúng/sai không chỉ dựa vào màu. Bổ sung kiểm tra thủ công theo checklist mobile và bàn phím; ưu tiên các luồng học từ vựng, flashcard và làm đề.

### Ưu tiên thấp — Đồng bộ tiến độ giữa thiết bị

Tiến độ và SRS hiện lưu theo trình duyệt trong LocalStorage; đã có backup/import thủ công nhưng chưa có đồng bộ tài khoản. Đây là giới hạn vận hành nếu người học dùng nhiều máy, không nhất thiết là lỗi với mục tiêu local-first.

**Đề xuất:** trước mắt cải thiện quy trình backup (nhắc xuất định kỳ, ngày backup gần nhất, kiểm tra file trước import). Chỉ triển khai đồng bộ cloud khi có yêu cầu sản phẩm rõ ràng vì sẽ cần tài khoản, backend, chính sách riêng tư và giải quyết xung đột dữ liệu.

## 3. Lộ trình đề nghị

1. **Đợt 1 — An toàn dữ liệu:** loại khóa API khỏi backup mặc định; validate import; báo lỗi khi LocalStorage không ghi được.
2. **Đợt 2 — Độ tin cậy phát hành:** đưa kiểm tra cốt lõi vào CI; deploy phụ thuộc CI; sinh báo cáo coverage theo dữ liệu thực tế.
3. **Đợt 3 — Tốc độ tải:** đo build, tối ưu audio, chỉ tải tài nguyên khi cần.
4. **Đợt 4 — Hoàn thiện học tập:** hiển thị trạng thái thiếu dữ liệu nhất quán; rà soát mobile/accessibility; cân nhắc đồng bộ chỉ khi có nhu cầu.

## 4. Giới hạn của đánh giá

Các nhận định về độ phủ dữ liệu tham chiếu README/ONBOARDING và báo cáo sẵn có trong repo; dung lượng tài nguyên được đo trực tiếp từ thư mục `public/`. Chưa chạy build, test, kiểm thử trình duyệt hay xác minh thủ công toàn bộ 50 bài trong lượt này. Vì vậy, báo cáo là đánh giá tĩnh và lộ trình đề xuất, không phải xác nhận rằng các cải tiến đã được triển khai.
