# Hướng Dẫn Deploy Lên GitHub Pages & Mở Link Truy Cập Trực Tuyến

Tài liệu này hướng dẫn chi tiết từng bước đưa dự án **Học 600 từ vựng TOEIC** lên GitHub và kích hoạt **GitHub Pages** để bạn và mọi người có thể truy cập web thông qua đường link:
> `https://<ten-tai-khoan-github>.github.io/<ten-repository>/`

---

## 📌 Các bước chuẩn bị đã được thiết lập sẵn trong mã nguồn
Trước khi thực hiện, dự án đã được tinh chỉnh tương thích hoàn toàn với GitHub Pages:
- Đã cấu hình `base: './'` trong [vite.config.js](file:///d:/LEGION/Documents/deepseek-harness/TiengAnh/app/vite.config.js) (tránh lỗi trắng trang do sai đường dẫn file tĩnh).
- Đã đồng bộ các đường dẫn tài nguyên tĩnh (`audio`, `part1_photos`, `lessons_json`, `answers`) tương thích với mọi URL subpath của GitHub.
- Đã tạo sẵn file tự động hoá CI/CD: [deploy.yml](file:///d:/LEGION/Documents/deepseek-harness/TiengAnh/.github/workflows/deploy.yml) nằm trong thư mục `.github/workflows/`.

---

## BƯỚC 1: Tạo Repository Mới Trên GitHub

1. Truy cập vào trang web [GitHub](https://github.com/) và đăng nhập tài khoản của bạn.
2. Bấm vào nút **New** (hoặc dấu `+` ở góc trên bên phải chọn **New repository**).
3. Điền thông tin repository:
   - **Repository name**: ví dụ `toeic-600-words` (hoặc tên tuỳ ý viết liền không dấu).
   - **Public / Private**: Để **Public** (nếu dùng tài khoản GitHub miễn phí thì GitHub Pages yêu cầu repo ở chế độ Public để mở link web).
   - **KHÔNG tích** vào các ô *Add a README file*, *Add .gitignore*, *Choose a license* (vì dự án của chúng ta đã có sẵn các file này).
4. Bấm nút xanh **Create repository**.
5. Sau khi tạo xong, GitHub sẽ hiển thị đường dẫn URL repository của bạn, dạng:
   ```text
   https://github.com/<ten-tai-khoan>/<ten-repository>.git
   ```

---

## BƯỚC 2: Khởi Tạo Git & Đẩy Mã Nguồn Lên GitHub

Mở cửa sổ dòng lệnh (PowerShell hoặc Terminal) tại thư mục gốc của dự án (`d:\LEGION\Documents\deepseek-harness\TiengAnh`) và chạy tuần tự các lệnh sau:

### 1. Khởi tạo Git và thêm file
```powershell
# Khởi tạo kho git (nếu máy chưa khởi tạo)
git init

# Thêm tất cả các file mã nguồn vào git
git add .

# Tạo commit đầu tiên
git commit -m "feat: initial commit with github pages configuration"
```

### 2. Liên kết với Repository trên GitHub và đẩy mã nguồn lên
> ⚠️ *Lưu ý: Thay thế `<ten-tai-khoan>` và `<ten-repository>` bằng thông tin thật của bạn từ Bước 1.*

```powershell
# Đổi tên nhánh mặc định thành main
git branch -M main

# Gán địa chỉ remote repository GitHub của bạn
git remote add origin https://github.com/<ten-tai-khoan>/<ten-repository>.git

# Đẩy toàn bộ mã nguồn lên nhánh main
git push -u origin main
```

*(Nếu GitHub yêu cầu đăng nhập, hãy đăng nhập qua trình duyệt hoặc nhập Personal Access Token của bạn).*

---

## BƯỚC 3: Cấu Hình GitHub Pages (Tự Động Build)

Khi mã nguồn đã được đẩy lên GitHub, chỉ cần 2 thao tác click chuột trên GitHub để kích hoạt:

1. Trên trang repository của bạn trên GitHub, vào tab **Settings** (biểu tượng bánh răng ở thanh menu trên cùng).
2. Ở cột danh mục bên trái, tìm và bấm vào mục **Pages** (nằm trong nhóm *Code and automation*).
3. Tại phần **Build and deployment**:
   - Ở mục **Source**, bấm vào menu thả xuống và chọn: **GitHub Actions**.
4. GitHub sẽ tự động nhận diện workflow có sẵn trong file `.github/workflows/deploy.yml` mà dự án đã tạo.

---

## BƯỚC 4: Kiểm Tra Tiến Trình & Mở Link Truy Cập

1. Chuyển sang tab **Actions** (ở thanh menu trên cùng của repository).
2. Bạn sẽ thấy một tiến trình có tên **Deploy to GitHub Pages** đang chạy (có biểu tượng vòng tròn màu vàng xoay).
3. Đợi khoảng **1 - 2 phút** để GitHub Actions tự động:
   - Tải các thư viện npm (`npm ci`).
   - Biên dịch ứng dụng web (`npm run build`).
   - Đóng gói và phát hành lên máy chủ GitHub Pages.
4. Khi tiến trình hoàn thành và xuất hiện **dấu tích xanh (✓)**:
   - Bấm vào tên luồng chạy đó, bạn sẽ thấy link trang web được tạo ở mục **deploy** -> **github-pages**.
   - Hoặc quay lại tab **Settings** -> **Pages**, bạn sẽ thấy thông báo:
     > *"Your site is live at `https://<ten-tai-khoan>.github.io/<ten-repository>/`"*
5. Bấm vào đường link đó để mở trang web ứng dụng học từ vựng trực tiếp trên trình duyệt!

---

## 🔄 Khi Cập Nhật Code Trong Tương Lai

Mỗi khi bạn sửa code, bổ sung bài học hoặc tính năng mới, bạn chỉ cần gõ 3 lệnh quen thuộc để cập nhật trang web:

```powershell
git add .
git commit -m "Cập nhật tính năng / nội dung mới"
git push origin main
```

GitHub Actions sẽ tự động phát hiện thay đổi, tự động build lại và cập nhật link web cho bạn trong vòng 1-2 phút mà không cần thao tác thủ công nào khác!

---

## ❓ Câu Hỏi & Xử Lý Sự Cố Thường Gặp (Troubleshooting)

### 1. Web mở lên bị trang trắng (Blank screen) hoặc báo 404 cho file CSS/JS?
- **Nguyên nhân**: Thông thường do thiết lập đường dẫn tuyệt đối `/` thay vì đường dẫn tương đối `./`.
- **Cách khắc phục**: Dự án này đã được cấu hình `base: './'` trong `vite.config.js` nên sẽ tự động tương thích với mọi URL subpath của GitHub Pages.

### 2. GitHub Actions báo lỗi quyền hạn (Permission denied: 403)?
- Vào **Settings** của repository -> chọn **Actions** ở menu trái -> chọn **General**.
- Kéo xuống mục **Workflow permissions**, tích chọn **Read and write permissions**.
- Bấm **Save**.

### 3. Repository để Private có mở được GitHub Pages không?
- Với tài khoản GitHub cá nhân miễn phí (Free), GitHub Pages chỉ áp dụng cho **Public repository**.
- Nếu bạn để Private, GitHub sẽ yêu cầu nâng cấp tài khoản lên GitHub Pro. Vì vậy, hãy chắc chắn chọn **Public** khi tạo repository.
