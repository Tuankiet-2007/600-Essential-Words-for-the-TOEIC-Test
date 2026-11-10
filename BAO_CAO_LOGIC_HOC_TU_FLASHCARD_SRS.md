# BÁO CÁO KIẾN TRÚC & QUY CHUẨN THUẬT TOÁN SRS (ANKI-STANDARD)
## HỆ THỐNG GHI NHỚ NGẮT QUÃNG — 600 ESSENTIAL WORDS FOR THE TOEIC TEST

> **Tài liệu**: Báo cáo kỹ thuật tái cấu trúc luồng học và chuẩn hóa thuật toán Spaced Repetition (SRS)  
> **Tác giả**: Chuyên gia Fullstack React & Kiến trúc sư hệ thống SRS  
> **Dự án**: 600 Essential Words for the TOEIC (Duolingo Style Web App)  
> **Phiên bản kiến trúc**: v2.0 (Anki Standardized Engine)  
> **Tệp đích thay thế**: `BAO_CAO_LOGIC_HOC_TU_FLASHCARD_SRS.md`

---

## MỤC LỤC
1. [TỔNG QUAN ĐỊNH HƯỚNG TÁI CẤU TRÚC KIẾN TRÚC & LUỒNG HỌC](#1-tổng-quan-định-hướng-tái-cấu-trúc-kiến-trúc--luồng-học)
   - [1.1. Bối cảnh & Sự cần thiết chuyển dịch sang mô hình Anki](#11-bối-cảnh--sự-cần-thiết-chuyển-dịch-sang-mô-hình-anki)
   - [1.2. Sơ đồ luồng học tập tổng thể (End-to-End User Flow)](#12-sơ-đồ-luồng-học-tập-tổng-thể-end-to-end-user-flow)
   - [1.3. Định vị vai trò & Ranh giới trách nhiệm của 4 thành phần](#13-định-vị-vai-trò--ranh-giới-trách-nhiệm-của-4-thành-phần)
2. [QUY CHUẨN THUẬT TOÁN SRS THEO NGUYÊN LÝ ANKI](#2-quy-chuẩn-thuật-toán-srs-theo-nguyên-lý-anki)
   - [2.1. Phễu nạp từ đầu vào (First-Touch Funnel) tại Tab 2 Flashcard](#21-phễu-nạp-từ-đầu-vào-first-touch-funnel-tại-tab-2-flashcard)
   - [2.2. Cơ chế Re-queue thông minh cho thẻ bị quên (Grade 1 - Again)](#22-cơ-chế-re-queue-thông-minh-cho-thẻ-bị-quên-grade-1---again)
   - [2.3. Quy tắc mốc chuyển ngày Anki (04:00 AM Next-Day Cutoff)](#23-quy-tắc-mốc-chuyển-ngày-anki-0400-am-next-day-cutoff)
   - [2.4. Khử lỗi ghi đè tại Tab 3 qua Session-Level Aggregation](#24-khử-lỗi-ghi-đè-tại-tab-3-qua-session-level-aggregation)
   - [2.5. Cô lập hoàn toàn Tab 5 (Luyện đề) khỏi chu trình SM-2](#25-cô-lập-hoàn-toàn-tab-5-luyện-đề-khỏi-chu-trình-sm-2)
3. [MA TRẬN ĐỒNG BỘ DỮ LIỆU ĐÍCH (TARGET DATA MATRIX)](#3-ma-trận-đồng-bộ-dữ-liệu-đích-target-data-matrix)
4. [ĐẶC TẢ KỸ THUẬT MÃ NGUỒN & CODE MẪU NÂNG CẤP](#4-đặc-tả-kỹ-thuật-mã-nguồn--code-mẫu-nâng-cấp)
   - [4.1. File `app/src/lib/srs.js`: Thuật toán 04:00 AM Cutoff & Due Checker](#41-file-appsrclibsrsjs-thuật-toán-0400-am-cutoff--due-checker)
   - [4.2. File `app/src/tabs/Tab2Flashcards.jsx`: Logic Re-queue & First-Touch Trigger](#42-file-appsrctabstab2flashcardsjsx-logic-re-queue--first-touch-trigger)
   - [4.3. File `app/src/tabs/Tab3Srs.jsx`: Session-level Aggregation & Auto-grading](#43-file-appsrctabstab3srsjsx-session-level-aggregation--auto-grading)
   - [4.4. File `app/src/tabs/Tab5Practice.jsx`: Gỡ bỏ vòng lặp ghi đè SRS](#44-file-appsrctabstab5practicejsx-gỡ-bỏ-vòng-lặp-ghi-đè-srs)
   - [4.5. File `app/src/components/DashboardView.jsx` & `Tab1Vocabulary.jsx`: Đồng bộ UI](#45-file-appsrccomponentsdashboardviewjsx--tab1vocabularyjsx-đồng-bộ-ui)
5. [KẾ HOẠCH HÀNH ĐỘNG TRIỂN KHAI (ACTION PLAN)](#5-kế-hoạch-hành-động-triển-khai-action-plan)

---

## 1. TỔNG QUAN ĐỊNH HƯỚNG TÁI CẤU TRÚC KIẾN TRÚC & LUỒNG HỌC

### 1.1. Bối cảnh & Sự cần thiết chuyển dịch sang mô hình Anki
Trong kiến trúc ban đầu của ứng dụng:
- Dữ liệu bị phân mảnh thành 2 kho lưu trữ độc lập: `toeic_progress` (chỉ ghi nhận boolean "Đã học" do người dùng bấm thủ công) và `toeic_srs` (ghi nhận chu kỳ thuật toán SM-2).
- Tab 1 (Học từ) mang tính thụ động (cuộn trang đọc chay), không tạo ra kích thích ghi nhớ chủ động và không đưa từ vào hệ thống SRS.
- Tab 2 (Flashcard) có chấm điểm nhưng không kích hoạt trạng thái "Đã học" của bài, đồng thời bỏ qua các thẻ bị quên (Grade 1) mà không bắt học lại.
- Tab 3 (Active Recall gõ từ) bị đặt sai vị trí (bị nhốt trong từng bài học thay vì phục vụ ôn tập liên bài) và tồn tại lỗi nghiêm trọng: mỗi từ sinh 2 câu hỏi làm phát sinh 2 lần ghi đè tính toán SM-2 trái ngược nhau trong cùng một buổi học.
- Tab 5 (Luyện đề) có một vòng lặp lồng nguy hiểm: nộp bài thi 23 câu thì lặp ghi đè SM-2 23 lần lên toàn bộ 12 từ của bài, phá hỏng dữ liệu trí nhớ ngắt quãng của người dùng.

**Giải pháp**: Tái cấu trúc toàn diện theo tiêu chuẩn của **Anki** — phần mềm SRS mã nguồn mở tiêu chuẩn vàng thế giới.

---

### 1.2. Sơ đồ luồng học tập tổng thể (End-to-End User Flow)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              BẢNG ĐIỀU KHIỂN (DASHBOARD)                                │
│   • Khung lớn: "ĐẾN HẠN CẦN ÔN" (Quét thẻ due <= 04:00 AM hôm nay trên toàn bộ 50 bài)   │
│   • Biểu đồ Donut SM-2 & 4 Cột phân loại: Thuộc lòng / Đang nhớ / Cần ôn / Chưa học    │
│   • Tiến độ 10 Chủ đề (60 từ/chủ đề) & Lịch sử thi đề TOEIC                            │
└──────────────────────────────────────────┬─────────────────────────────────────────────┘
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    │                                             │
         [HÀNG NGÀY: DUY TRÌ TRÍ NHỚ]                   [KHI HỌC BÀI MỚI (L01..L50)]
                    │                                             │
                    ▼                                             ▼
┌───────────────────────────────────────┐     ┌──────────────────────────────────────────┐
│   TAB 3 STANDALONE (SrsStandaloneView)│     │   TAB 2 FLASHCARD (FIRST-TOUCH FUNNEL)   │
│   "Trạm Ôn Tập Giãn Cách Toàn Cục"    │     │   "Cửa Ngõ Nạp Từ & Nhận Diện Ban Đầu"   │
│                                       │     │                                          │
│ • Quét toàn bộ từ DUE từ 50 bài       │     │ • Duyệt 12 từ qua câu đục lỗ ngữ cảnh    │
│ • Mỗi từ gồm 2 câu: Gõ gốc + Ngữ cảnh │     │ • Nghe Audio US · Lật mặt sau (Space/Tab)│
│ • SESSION AGGREGATION: Gom 2 câu      │     │ • Tự đánh giá 4 mức (Again/Hard/Good/Easy│
│   chốt 1 điểm SM-2 duy nhất / từ      │     │ • CƠ CHẾ RE-QUEUE: Bấm Again (1) ->      │
│ • Cập nhật due mới cho chu kỳ sau     │     │   thẻ tự đẩy về cuối hàng đợi bắt ôn lại │
└───────────────────────────────────────┘     │ • Tự động kích hoạt markWordLearned()    │
                                              │ • Khởi tạo bản ghi SM-2 ban đầu          │
                                              └───────────────────┬──────────────────────┘
                                                                  │
                                         ┌────────────────────────┴──────────────────────┐
                                         │                                               │
                                         ▼                                               ▼
                      ┌────────────────────────────────────┐   ┌─────────────────────────────────┐
                      │    TAB 1: REFERENCE NOTEBOOK       │   │    TAB 5: TOEIC PRACTICE EXAM   │
                      │    "Sổ Tay Tra Cứu & Ngữ Pháp"     │   │    "Luyện Đề Thi Trắc Nghiệm"   │
                      │                                    │   │                                 │
                      │ • Từ điển tĩnh, tra cứu chuyên sâu │   │ • Làm Listening (Part 1-4)      │
                      │ • Bảng họ từ đầy đủ (Word Family)  │   │ • Làm Reading (Part 5-7)        │
                      │ • Hộp USE: collocations, preps     │   │ • ĐỘC LẬP HOÀN TOÀN KHỎI SRS:   │
                      │ • Trạng thái "Đã học" tự sáng lên  │   │   Nộp bài chỉ chấm điểm thi đề, │
                      │   sau khi hoàn thành Tab 2         │   │   tuyệt đối KHÔNG ghi đè SM-2!  │
                      └────────────────────────────────────┘   └─────────────────────────────────┘
```

---

### 1.3. Định vị vai trò & Ranh giới trách nhiệm của 4 thành phần

| Thành phần | Định vị vai trò mới | Cơ chế kích hoạt dữ liệu | Ranh giới trách nhiệm (Scope Boundary) |
| :--- | :--- | :--- | :--- |
| **Tab 2: Flashcard** | **Điểm chạm đầu tiên (First-Touch)** cho mọi bài học mới. Nhận diện từ qua ngữ cảnh đục lỗ, luyện nghe và tự lượng giá. | • Bấm Grade (1-4) -> Tự động đánh dấu `markWordLearned(lessonId, word, true)`.<br>• Khởi tạo thẻ mới trong `toeic_srs`.<br>• Bấm Again (1) -> Re-queue về cuối mảng. | Chịu trách nhiệm đưa từ từ trạng thái **"Chưa học"** sang **"Đang nhớ"**. Không phụ trách việc kiểm tra gõ từ. |
| **Tab 3: Active Recall** *(Standalone ở Dashboard)* | **Trung tâm duy trì trí nhớ hàng ngày (Daily Retention Hub)**. Vừa khít 1 màn hình, gõ từ chủ động cho tất cả các từ đến hạn (`due`) trên toàn bộ 50 bài. | • Chạy thuật toán Session Aggregation (gom 2 câu hỏi).<br>• Chấm 1 lần điểm SM-2 duy nhất khi từ kết thúc cả 2 câu.<br>• Phân bổ `interval` và `due_date` mới. | Không còn nằm bên trong tab con của từng bài học. Chỉ xuất hiện ngoài Dashboard để phục vụ ôn tập liên bài tập trung. |
| **Tab 1: Từ vựng** | **Sổ tay ngữ pháp & tra cứu chuyên sâu (Static Reference Notebook)**. Cung cấp bức tranh toàn cảnh về từ. | • Hoàn toàn ở chế độ đọc (Read-only reference).<br>• Hiển thị huy hiệu trạng thái trí nhớ SM-2 đồng bộ từ Tab 2/Tab 3.<br>• Cho phép đánh dấu ghi chú cá nhân, xem Word Family mở rộng. | Không đóng vai trò điều hướng thuật toán SRS. Nút "Đã học" tự động đồng bộ theo kết quả học từ Tab 2. |
| **Tab 5: Luyện đề** | **Phòng thi thử TOEIC mô phỏng thực tế (Exam Simulator)**. Đo lường kỹ năng đọc hiểu và nghe hiểu Part 1-7. | • Nộp bài thi trắc nghiệm -> Ghi nhận kết quả vào `toeic_history` (`pushHistory`).<br>• Cập nhật điểm thi đề lên Dashboard. | **Tuyệt đối cách ly khỏi SRS**: Không được gọi `recordReview()` hay `markWordLearned()` trong bất kỳ trường hợp nào khi nộp đề thi. |

---

## 2. QUY CHUẨN THUẬT TOÁN SRS THEO NGUYÊN LÝ ANKI

### 2.1. Phễu nạp từ đầu vào (First-Touch Funnel) tại Tab 2 Flashcard
- **Nguyên lý Anki**: Một từ mới (*New Card*) cần được tiếp cận lần đầu qua nhận diện flashcard trước khi chuyển thành thẻ đang học (*Learning/Review Card*).
- **Cơ chế thực thi**:
  - Khi bắt đầu một bài học mới (ví dụ Bài 01), người học vào thẳng **Tab 2 (Flashcard)**.
  - Khi người học chấm điểm từ (1-4) cho một từ:
    1. Hệ thống tự động gọi `markWordLearned(lessonId, entry.word, true)` -> Cập nhật `toeic_progress`. Tab 1 lập tức chuyển sang trạng thái "Đã học".
    2. Hệ thống gọi `recordReview(lessonId, entry.word, grade)` -> Khởi tạo cấu trúc thẻ SM-2 hoàn chỉnh trong `toeic_srs`.
    3. Trên Dashboard, từ đó ngay lập tức rời khỏi cột **"Chưa học" (Unseen)** để chuyển sang cột **"Đang nhớ" (Young)** hoặc **"Cần ôn" (Critical)** nếu bấm Again.

---

### 2.2. Cơ chế Re-queue thông minh cho thẻ bị quên (Grade 1 - Again)
- **Vấn đề cũ**: Bấm phím `1` (Again - Quên), thẻ đơn thuần chuyển sang thẻ tiếp theo (`pos + 1`). Người học quên từ nhưng không được học lại ngay lúc đó, phiên học kết thúc mà từ vẫn bị bỏ lửng.
- **Quy chuẩn Anki**: Khi đánh giá `Again` (Grade 1), thẻ phải được chèn lại vào cuối hàng đợi của phiên học hiện tại (*Re-queue*). Người học buộc phải gặp lại thẻ này và vượt qua (Grade >= 2) thì phiên học mới kết thúc.

```
Hàng đợi ban đầu:   [ Từ 1, Từ 2, Từ 3, Từ 4 ]
                      │
                      ▼ Người học bấm "Again" (1) tại Từ 1
Hàng đợi cập nhật:  [ Từ 2, Từ 3, Từ 4, Từ 1 (Re-queued) ]
```

- **Mã logic điều khiển hàng đợi**:
  - Nếu `grade === 1`: Giữ nguyên từ đó trong phiên, đẩy chỉ số `cardIndex` vào cuối mảng `order`. Không tăng số lượng hoàn thành thẻ duy nhất.
  - Nếu `grade >= 2`: Ghi nhận hoàn thành thẻ, chuyển sang thẻ tiếp theo.
  - Bộ thẻ chỉ báo hoàn thành (100%) khi toàn bộ các thẻ trong hàng đợi đều được vượt qua.

---

### 2.3. Quy tắc mốc chuyển ngày Anki (04:00 AM Next-Day Cutoff)
- **Vấn đề của mốc 00:00 (Midnight)**:
  - Học sinh thường học bài vào đêm khuya (23:30 đến 01:30 sáng). Nếu dùng mốc nửa đêm (00:00):
    - Một thẻ học lúc 23:59 ngày thứ Hai có chu kỳ 1 ngày sẽ đến hạn ôn vào 00:00 ngày thứ Ba (chỉ sau 1 phút!).
    - Một thẻ học lúc 00:05 ngày thứ Ba lại bị tính sang ngày hôm sau, gây xáo trộn hoàn toàn chu kỳ ghi nhớ sinh học.
- **Quy chuẩn Anki Next-Day Cutoff**:
  - Quy ước một ngày học tập kết thúc vào **04:00 AM sáng hôm sau**.
  - Bất kỳ lúc nào người học thao tác từ 00:00 đến 03:59 AM, hệ thống vẫn coi đó là **thuộc về ngày hôm trước**.
  - Công thức tính ngày hiệu dụng (*Effective Day*):
    $$\text{EffectiveDate} = \text{Date} - 4 \text{ hours}$$
    $$\text{EffectiveDayKey} = \text{YYYY-MM-DD của } (\text{Now} - 4 \text{ hours})$$
  - Một thẻ được coi là đến hạn (`isDue`) khi:
    $$\text{DueDayKey}(card.due) \le \text{EffectiveDayKey}(now)$$

---

### 2.4. Khử lỗi ghi đè tại Tab 3 qua Session-Level Aggregation
- **Lỗ hổng cũ**:
  - Tab 3 sinh ra 2 câu hỏi cho mỗi từ: Câu 1 (Gõ từ gốc từ định nghĩa EN) và Câu 2 (Điền từ vào câu ngữ cảnh).
  - Hai câu này nằm xáo trộn. Khi người học trả lời câu 1, `recordReview()` được gọi ngay lập tức. Đến câu 2, `recordReview()` lại được gọi lần thứ 2, ghi đè toàn bộ kết quả của câu 1. Nếu câu 1 đúng (Grade 4) nhưng câu 2 sai (Grade 1), thẻ bị phạt tụt dốc thê thảm dù người học đã nhớ từ gốc.
- **Thuật toán Session-Level Aggregation (Gom điểm theo phiên)**:
  - Trong suốt quá trình trả lời trong phiên ôn tập, **tuyệt đối không gọi `recordReview()` ngay sau mỗi câu hỏi lẻ**.
  - Hệ thống duy trì một bộ theo dõi phiên học: `sessionScores[wordKey] = { attemptsQ1: number, attemptsQ2: number, failed: boolean }`.
  - Chỉ khi người học **hoàn thành cả 2 câu hỏi** của từ đó (hoặc kết thúc phiên), hàm tổng hợp sẽ tính toán ra **một điểm Grade duy nhất** theo ma trận quyết định sau:

| Kết quả Câu 1 (Base Word) | Kết quả Câu 2 (Context Word) | Grade tổng hợp | Ý nghĩa & Tác động SM-2 |
| :---: | :---: | :---: | :--- |
| Đúng ngay lần đầu (0 sai) | Đúng ngay lần đầu (0 sai) | **Grade 4 (Easy)** | Trí nhớ xuất sắc. Tăng interval vượt bậc: $\text{Interval} = \text{round}(\text{Interval} \times \text{Ease} \times 1.3)$. |
| Đúng lần 1 (0 sai) | Đúng lần 2 (1 sai) | **Grade 3 (Good)** | Nhớ tốt ngữ nghĩa, hơi lúng túng ngữ cảnh. Tăng interval chuẩn: $\text{Interval} = \text{round}(\text{Interval} \times \text{Ease})$. |
| Đúng lần 2 (1 sai) | Đúng lần 1 (0 sai) | **Grade 3 (Good)** | Nhớ ngữ cảnh nhưng quên mặt chữ gốc. Tăng interval chuẩn. |
| Sai $\ge 2$ lần ở bất kỳ câu nào | Bất kỳ | **Grade 1 (Again)** | Quên từ hoặc nhầm lẫn nghiêm trọng. Reset reps về 0, interval về 1 ngày, giảm Ease factor (-0.2), bung lý thuyết để học lại. |

- **Kết quả**: Mỗi từ vựng được đảm bảo **gọi `recordReview()` đúng 1 lần duy nhất** trong một phiên ôn tập, phản ánh trung thực 100% năng lực trí nhớ ngắt quãng theo đúng công thức SM-2.

---

### 2.5. Cô lập hoàn toàn Tab 5 (Luyện đề) khỏi chu trình SM-2
- **Thực trạng**: Tại tệp `app/src/tabs/Tab5Practice.jsx` (dòng 1975–1987), khi người học nhấn "Nộp bài & Chấm điểm" cho một đề thi TOEIC gồm 23 câu hỏi, mã nguồn đang chạy một vòng lặp:
  ```javascript
  // LỖ HỔNG CŨ CỰC KỲ NGUY HIỂM:
  for (const q of allQuestions) {
    ...
    for (const w of lesson.words_to_learn || []) {
      recordReview(id, w.word, correct ? 3 : 1, { source: 'practice' });
    }
  }
  ```
  Vòng lặp này khiến mỗi từ bị ghi đè SM-2 tới 23 lần liên tiếp. Nếu câu hỏi trắc nghiệm cuối cùng (câu 23) bị sai, cả 12 từ vựng của bài đều bị đánh tụt về Quên (Grade 1)!
- **Quy chuẩn mới**:
  - Gỡ bỏ 100% đoạn mã gọi `recordReview()` và `markWordLearned()` bên trong sự kiện nộp bài thi của `Tab5Practice.jsx`.
  - Sự kiện nộp bài thi chỉ thực hiện duy nhất nhiệm vụ: Chấm điểm bài thi, tính tỷ lệ đúng từng phần (Listening, Part 5, 6, 7), lưu lịch sử thi qua `pushHistory()`, và hiển thị bảng giải thích đáp án.

---

## 3. MA TRẬN ĐỒNG BỘ DỮ LIỆU ĐÍCH (TARGET DATA MATRIX)

Dưới đây là bảng ma trận mô tả dòng chảy dữ liệu chuẩn mực sau khi hoàn thành tái cấu trúc:

| Hành động của người học | Vị trí thao tác | Cập nhật `toeic_srs` (SM-2) | Cập nhật `toeic_progress` | Hiển thị tại Tab 1 (Từ vựng) | Hiển thị tại Tab 2 (Flashcard) | Hiển thị tại Tab 3 (Active Recall) | Hiển thị trên Dashboard |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Lướt Flashcard & Tự đánh giá** | Tab 2 (Bài học) |  Khởi tạo thẻ SM-2 ban đầu (`ease: 2.5`, `interval: 1/6/due`) |  Tự động đánh dấu `learned: true` | Nút tự động chuyển sang **"Đã học" (Check xanh)** | Thẻ cập nhật tiến độ, nếu bấm Again sẽ Re-queue | Thẻ được đưa vào hàng đợi chờ ôn theo lịch `due` | Cột **"Đang nhớ"** tăng lên; cột **"Chưa học"** giảm đi |
| **Bấm "Again" khi quên Flashcard** | Tab 2 (Bài học) |  Ghi nhận Grade 1; interval = 1 |  Vẫn giữ `learned: true` | Nút vẫn hiện "Đã học" | Thẻ tự động đẩy về cuối bộ thẻ để học lại | Chuyển vào nhóm **"Cần ôn"** | Cột **"Cần ôn" (Critical)** tăng lên ngay lập tức |
| **Xem sổ tay tra cứu** | Tab 1 (Bài học) | ❌ Không thay đổi (Read-only) | ❌ Không thay đổi | Xem nghĩa, collocations, bảng họ từ chi tiết | ❌ Không đổi | ❌ Không đổi | ❌ Không đổi |
| **Gõ từ ôn tập đến hạn** | Tab 3 Standalone (Dashboard) |  Tính 1 lần điểm duy nhất qua Session Aggregation |  Duy trì trạng thái đã học | Cập nhật huy hiệu trí nhớ của từ | ❌ Không đổi | Tự động loại bỏ khỏi danh sách `due` khi xong | Số lượng **"Đến Hạn Cần Ôn"** giảm dần về 0; Donut tăng |
| **Nộp bài thi trắc nghiệm TOEIC** | Tab 5 (Bài học) | ❌ **KHÔNG CAN THIỆP** (Đã cô lập 100%) | ❌ **KHÔNG CAN THIỆP** | ❌ Không bị ảnh hưởng | ❌ Không bị ảnh hưởng | ❌ Không bị ảnh hưởng | Điểm thi lưu vào Biểu đồ Điểm Luyện Đề |

---

## 4. ĐẶC TẢ KỸ THUẬT MÃ NGUỒN & CODE MẪU NÂNG CẤP

Dưới đây là thiết kế chi tiết từng hàm, từng module và code mẫu chuẩn xác, sẵn sàng cho việc triển khai thực tế.

---

### 4.1. File `app/src/lib/srs.js`: Thuật toán 04:00 AM Cutoff & Due Checker

#### A. Phân tích sự cố hiện tại:
- Hàm `isDue()` hiện tại dùng so sánh tuyệt đối mili-giây: `new Date(card.due).getTime() <= now.getTime()`.
- Điều này khiến thẻ được học lúc 23:00 đêm hôm trước không thể xuất hiện trong danh sách ôn của sáng hôm sau nếu chưa đủ đúng 24 tiếng đồng hồ, gây ức chế cho người học.

#### B. Giải pháp kỹ thuật:
- Bổ sung hàm tính ngày hiệu dụng `getEffectiveDayString()` với mốc cắt 04:00 AM.
- So sánh `card.due` và `now` theo ngày hiệu dụng (YYYY-MM-DD) thay vì so sánh mili-giây.

#### C. Code mẫu triển khai (`app/src/lib/srs.js`):

```javascript
// app/src/lib/srs.js

export const CUTOFF_HOUR = 4; // Mốc chuyển ngày theo chuẩn Anki: 04:00 AM

/**
 * Trả về chuỗi ngày YYYY-MM-DD theo mốc chuyển ngày 04:00 AM.
 * Nếu thời gian hiện tại từ 00:00 đến 03:59, ngày hiệu dụng sẽ lùi lại 1 ngày.
 * @param {Date|string} dateInput
 * @param {number} cutoffHour
 * @returns {string} định dạng YYYY-MM-DD
 */
export function getEffectiveDayString(dateInput = new Date(), cutoffHour = CUTOFF_HOUR) {
  const d = new Date(dateInput);
  if (Number.isNaN(d.getTime())) return new Date().toISOString().slice(0, 10);
  
  // Lùi lại số giờ tương ứng với cutoffHour
  d.setHours(d.getHours() - cutoffHour);
  
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * Kiểm tra xem thẻ đã đến hạn ôn hay chưa theo mốc 04:00 AM.
 * Thẻ đến hạn khi ngày đáo hạn hiệu dụng <= ngày hôm nay hiệu dụng.
 * @param {import('./storage.js').SrsCard} card
 * @param {Date} [now]
 * @returns {boolean}
 */
export function isDue(card, now = new Date()) {
  if (!card || !card.due) return true;
  const todayDayKey = getEffectiveDayString(now, CUTOFF_HOUR);
  const cardDueDayKey = getEffectiveDayString(new Date(card.due), CUTOFF_HOUR);
  return cardDueDayKey <= todayDayKey;
}

/**
 * Tính toán ngày đáo hạn mới đảm bảo neo vào mốc cutoff 04:00 AM.
 * @param {number} interval Số ngày giãn cách
 * @param {Date} now
 * @returns {string} ISO Date string
 */
export function calculateNextDueDate(interval, now = new Date()) {
  const target = new Date(now);
  // Đưa về 04:00 AM của ngày đáo hạn tương lai
  target.setDate(target.getDate() + interval);
  target.setHours(CUTOFF_HOUR, 0, 0, 0);
  return target.toISOString();
}

/**
 * Nâng cấp hàm review() chuẩn SM-2 kết hợp mốc đáo hạn 04:00 AM.
 */
export function review(card, grade, now = new Date()) {
  const c = { ...freshCard(), ...(card || {}) };
  const g = GRADES[grade] || GRADES[3];
  const q = g.quality;

  let { ease, interval, reps, lapses } = c;

  if (q < 3) {
    // Quên từ: Reset chu kỳ lặp, tăng số lần hỏng trí nhớ
    reps = 0;
    lapses += 1;
    interval = 1;
    ease = Math.max(MIN_EASE, ease - 0.2);
  } else {
    reps += 1;
    if (reps === 1) interval = 1;
    else if (reps === 2) interval = 6;
    else interval = Math.round(interval * ease);

    // Điều chỉnh Easiness theo công thức chuẩn SM-2
    ease = ease + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02));
    ease = Math.max(MIN_EASE, ease);

    if (grade === 4) interval = Math.round(interval * 1.3); // Thưởng Easy
    if (grade === 2) interval = Math.max(1, Math.round(interval * 0.6)); // Phạt Hard
  }

  interval = Math.max(1, Math.min(interval, 365));
  const due = calculateNextDueDate(interval, now);

  return {
    ease: Number(ease.toFixed(3)),
    interval,
    reps,
    due,
    lapses,
    lastGrade: grade,
  };
}
```

---

### 4.2. File `app/src/tabs/Tab2Flashcards.jsx`: Logic Re-queue & First-Touch Trigger

#### A. Phân tích sự cố hiện tại:
- Bấm phím 1 (Again), `Tab2Flashcards` chỉ tăng `pos` lên 1: thẻ biến mất khỏi màn hình và không bao giờ xuất hiện lại trong phiên.
- Chấm điểm Flashcard xong không gọi `markWordLearned()`, khiến Tab 1 vẫn báo là từ chưa học.

#### B. Giải pháp kỹ thuật:
- Thêm cơ chế **Re-queue**: Khi `g === 1`, chèn lại chỉ số của thẻ hiện tại vào cuối mảng `order`.
- Thêm **First-Touch Trigger**: Khi chấm bất kỳ điểm nào (1-4), tự động gọi `markWordLearned(lessonId, entry.word, true)`.
- Thanh tiến độ ProgressBar hiển thị số thẻ gốc đã nắm vững thay vì chỉ đếm số lần bấm phím.

#### C. Code mẫu triển khai (`app/src/tabs/Tab2Flashcards.jsx`):

```javascript
// Trích đoạn cập nhật trong Tab2Flashcards.jsx
import { markWordLearned } from '../lib/storage.js';

export default function Tab2Flashcards({ lesson }) {
  const { lessonId: storeLessonId, setProgress } = useApp();
  const lessonId = lesson?.lesson_id ?? storeLessonId;
  const entries = useMemo(() => lesson?.words_to_learn || [], [lesson]);

  // Quản lý trạng thái bộ thẻ với mảng order động hỗ trợ Re-queue
  const deckKey = entries.map((e) => e?.id ?? e?.word).join('|');
  const [deck, setDeck] = useState(() => ({
    key: deckKey,
    order: entries.map((_, i) => i), // Danh sách chỉ số thẻ cần học
    pos: 0,
    flipped: false,
    completedIndexes: new Set(), // Tập hợp các từ đã qua (Grade >= 2)
    lastGrade: null,
  }));

  const { order, pos, flipped, completedIndexes, lastGrade } = deck;
  const currentCardIndex = order[pos] ?? -1;
  const entry = currentCardIndex >= 0 ? entries[currentCardIndex] : null;
  const totalUnique = entries.length;
  const masteredUniqueCount = completedIndexes.size;

  /**
   * Chấm điểm SM-2 kết hợp Re-queue Anki và First-Touch Sync.
   */
  const grade = useCallback(
    (g) => {
      if (!entry) return;

      // 1. Kích hoạt First-Touch: Tự động đánh dấu từ đã học trong progress
      try {
        const nextProg = markWordLearned(lessonId, entry.word, true);
        if (setProgress) setProgress({ ...nextProg });
      } catch {
        /* ignore */
      }

      // 2. Ghi nhận chu kỳ SM-2 vào toeic_srs
      recordReview(lessonId, entry.word, g);

      setDeck((prev) => {
        const nextOrder = [...prev.order];
        const nextCompleted = new Set(prev.completedIndexes);

        if (g === 1) {
          // Bấm AGAIN: Đẩy thẻ hiện tại về cuối hàng đợi để học lại trong phiên
          nextOrder.push(currentCardIndex);
          show(`Cần nhớ lại: "${entry.word}" (sẽ xuất hiện lại ở cuối)`, 'rose');
        } else {
          // Bấm HARD/GOOD/EASY: Ghi nhận đã vượt qua thẻ này
          nextCompleted.add(currentCardIndex);
          const meta = GRADES[g];
          show(`${meta.label} · ${meta.vi} — ${entry.word}`, meta.color === 'amber' ? 'brand' : 'emerald');
        }

        const nextPos = prev.pos + 1;
        const isSessionFinished = nextCompleted.size >= totalUnique;

        return {
          ...prev,
          order: nextOrder,
          pos: nextPos,
          flipped: false,
          completedIndexes: nextCompleted,
          lastGrade: g,
        };
      });
    },
    [entry, lessonId, currentCardIndex, totalUnique, setProgress, show],
  );
  
  // Khi pos >= order.length và completedIndexes.size >= totalUnique -> Báo hoàn thành phiên học!
  const isAllPassed = masteredUniqueCount >= totalUnique;
  ...
```

---

### 4.3. File `app/src/tabs/Tab3Srs.jsx`: Session-level Aggregation & Auto-grading

#### A. Phân tích sự cố hiện tại:
- Mỗi từ sinh ra 2 câu hỏi: `q-base` và `q-custom`.
- `CompactQuizCard` gọi `recordReview()` ngay lập tức khi người học bấm Kiểm tra đúng/sai ở mỗi câu, làm thuật toán SM-2 bị gọi 2 lần/từ trong cùng một buổi học.

#### B. Giải pháp kỹ thuật:
- **Tách biệt tầng UI và tầng Ghi nhận**: `CompactQuizCard` chỉ làm nhiệm vụ giao tiếp và gửi kết quả câu hỏi `onQuestionCompleted({ word, ok, attempts })` lên component cha `Tab3Srs`.
- `Tab3Srs` lưu trữ kết quả của từng từ vào đối tượng `sessionTracker[word] = { q1Attempts, q2Attempts, hasFailed }`.
- Khi một từ đã hoàn thành cả 2 câu hỏi (hoặc khi kết thúc toàn bộ bài tập), `Tab3Srs` mới tiến hành **tổng hợp điểm duy nhất** và gọi `recordReview()` 1 lần.

#### C. Code mẫu triển khai (`app/src/tabs/Tab3Srs.jsx`):

```javascript
// Trích đoạn logic Session-level Aggregation trong Tab3Srs.jsx

export default function Tab3Srs({ lesson, globalMode = true, initialFilter = 'due' }) {
  ...
  // Bộ theo dõi kết quả từng câu hỏi theo từ vựng trong phiên
  const [sessionTracker, setSessionTracker] = useState({}); // { [wordKey]: { qBaseAttempts, qCustomAttempts, errors: 0 } }
  const [completedWords, setCompletedWords] = useState(new Set());

  /**
   * Xử lý khi người học hoàn tất 1 câu hỏi lẻ (đúng hoặc hết lượt thử).
   * Không gọi recordReview ở đây!
   */
  const handleQuestionAnswered = useCallback((questionItem, isCorrect, attemptCount) => {
    const { entry, lessonId, type } = questionItem;
    const wKey = srsKey(lessonId, entry.word);

    setSessionTracker((prev) => {
      const record = prev[wKey] || {
        lessonId,
        word: entry.word,
        qBaseAttempts: 0,
        qCustomAttempts: 0,
        totalErrors: 0,
        questionsAnswered: 0,
      };

      const updated = {
        ...record,
        questionsAnswered: record.questionsAnswered + 1,
        totalErrors: record.totalErrors + (isCorrect ? (attemptCount - 1) : 2),
      };

      if (type === 'base_word') {
        updated.qBaseAttempts = attemptCount;
      } else {
        updated.qCustomAttempts = attemptCount;
      }

      // Khi từ này đã hoàn thành đủ 2 câu hỏi (hoặc bài chỉ có 1 câu) -> CHỐT ĐIỂM SM-2 DUY NHẤT
      if (updated.questionsAnswered >= 2) {
        let finalGrade = 3; // Mặc định Good

        if (updated.totalErrors === 0 && updated.qBaseAttempts === 1 && updated.qCustomAttempts === 1) {
          finalGrade = 4; // Đúng tuyệt đối cả 2 câu ngay lần 1 -> Easy (Grade 4)
        } else if (updated.totalErrors === 1) {
          finalGrade = 3; // Sai 1 lần duy nhất trong cả 2 câu -> Good (Grade 3)
        } else {
          finalGrade = 1; // Sai từ 2 lần trở lên -> Again (Grade 1)
        }

        // GỌI SM-2 ĐÚNG 1 LẦN DUY NHẤT CHO TỪ NÀY
        recordReview(lessonId, entry.word, finalGrade, {
          source: 'active_recall_session',
          errors: updated.totalErrors,
        });

        if (finalGrade >= 3) {
          markWordLearned(lessonId, entry.word, true);
        }

        setCompletedWords((done) => new Set([...done, wKey]));
      }

      return { ...prev, [wKey]: updated };
    });
  }, []);
  ...
```

---

### 4.4. File `app/src/tabs/Tab5Practice.jsx`: Gỡ bỏ vòng lặp ghi đè SRS

#### A. Vị trí lỗi chính xác:
Tệp `app/src/tabs/Tab5Practice.jsx`, hàm xử lý nộp bài thi (khoảng dòng 1970–2000).

#### B. Thao tác dọn dẹp mã nguồn:
- **Xóa bỏ hoàn toàn**: Vòng lặp `for (const q of allQuestions)` lồng với `for (const w of lesson.words_to_learn || [])`.
- **Giữ lại nguyên vẹn**:
  1. Tính toán điểm thi (`stats.gradedCorrect`, `stats.gradedTotal`).
  2. Lưu lịch sử làm đề `pushHistory()`.
  3. Cập nhật state điểm số giao diện `setHistoryList()`.

#### C. Code mẫu sau khi sửa (`app/src/tabs/Tab5Practice.jsx`):

```javascript
// Sửa đổi trong app/src/tabs/Tab5Practice.jsx — Khử bỏ hoàn toàn can thiệp SRS

useEffect(() => {
  if (!submitted) return;
  if (isReviewingRef.current) {
    isReviewingRef.current = false;
    return;
  }

  try {
    // CHỈ LƯU LỊCH SỬ THI ĐỀ TOEIC — TUYỆT ĐỐI KHÔNG GỌI recordReview()
    const nextHist = pushHistory({
      type: 'practice',
      lessonId: id,
      lessonTitle: lesson?.title || '',
      correct: stats.gradedCorrect,
      total: stats.gradedTotal,
      chosen: chosenCount,
      scores,
      userAnswers: { ...answers },
    });
    setHistoryList(nextHist);
  } catch {
    /* storage is best-effort — never let it break the UI */
  }
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, [submitted]);
```

---

### 4.5. File `app/src/components/DashboardView.jsx` & `Tab1Vocabulary.jsx`: Đồng bộ UI

#### A. Đồng bộ dữ liệu tại `DashboardView.jsx`:
- Hàm `categorizedWords` và `metrics`:
  - Thẻ `unseen` (Chưa học): Những từ chưa từng có trong `srs` VÀ chưa có trong `progress`.
  - Khi một từ được bấm ở Tab 2, nó sẽ lập tức chuyển thành `young` hoặc `critical`, đảm bảo biểu đồ Donut và 4 cột trạng thái tăng giảm đồng nhất 100% với số lượng từ bài học.

#### B. Định vị lại `Tab1Vocabulary.jsx`:
- Loại bỏ áp lực phải bấm nút "Đánh dấu đã học".
- Nút ở góc dưới thẻ từ hiển thị huy hiệu trạng thái tự động:
  - Nếu từ đã học ở Tab 2: Hiển thị badge xanh **"Đã học (Đang nhớ)"** hoặc **"Thuộc lòng"** kèm thông tin chu kỳ ôn tập.
  - Thêm nút CTA ở đầu trang/cuối trang: **"Luyện Flashcard 12 từ này (Tab 2) →"** để hướng dẫn người học vào phễu tiếp nhận từ đầu tiên.

---

## 5. KẾ HOẠCH HÀNH ĐỘNG TRIỂN KHAI (ACTION PLAN)

Lộ trình triển khai được chia thành 4 giai đoạn an toàn, độc lập và có thể nghiệm thu ngay sau mỗi giai đoạn:

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                           LỘ TRÌNH TRIỂN KHAI 4 GIAI ĐOẠN                          │
└───────────────────────────────────────────────────────────────────────────────────┘

  PHASE 1: Dọn dẹp & Cách ly khẩn cấp (Critical Isolation)
  ├── Bước 1: Gỡ bỏ vòng lặp phá hủy SRS (dòng 1975–1987) trong Tab5Practice.jsx.
  └── Bước 2: Kiểm thử build (`npm run build`) đảm bảo việc nộp đề không sinh lỗi.

  PHASE 2: Nâng cấp Thuật toán lõi & Mốc chuyển ngày 04:00 AM
  ├── Bước 1: Cập nhật srs.js với `getEffectiveDayString()`, `CUTOFF_HOUR = 4`,
  │           và chuẩn hóa hàm `isDue()`, `calculateNextDueDate()`.
  └── Bước 2: Viết script test nhanh kiểm tra các trường hợp học lúc 01:00 AM và 23:00 PM.

  PHASE 3: Hoàn thiện First-Touch & Re-queue tại Tab 2 Flashcard
  ├── Bước 1: Nâng cấp Tab2Flashcards.jsx với cơ chế Re-queue (bấm phím 1 đẩy về cuối).
  ├── Bước 2: Tự động kích hoạt `markWordLearned()` và khởi tạo `toeic_srs` khi lướt thẻ.
  └── Bước 3: Kiểm tra đồng bộ: Học xong Tab 2 -> Tab 1 tự đổi trạng thái Đã học.

  PHASE 4: Chuẩn hóa Session Aggregation tại Tab 3 Standalone & Đồng bộ Dashboard
  ├── Bước 1: Triển khai gom 2 câu hỏi thành 1 điểm SM-2 duy nhất trong Tab3Srs.jsx.
  ├── Bước 2: Đồng bộ hiển thị Dashboard: Khung "Đến hạn cần ôn" đọc đúng mốc 04:00 AM.
  └── Bước 3: Nghiệm thu toàn diện (End-to-End Test), kiểm thử Vite build và commit code.
```

---
*Báo cáo được biên soạn độc lập bởi Chuyên gia Fullstack React & Kiến trúc sư hệ thống SRS — Sẵn sàng phục vụ triển khai mã nguồn.*
