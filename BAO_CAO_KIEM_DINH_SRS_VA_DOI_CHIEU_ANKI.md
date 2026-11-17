# Kiểm định logic học từ, Flashcard và SRS — đối chiếu Anki

Ngày kiểm tra/cập nhật: 16/11/2026. Phiên bản tài liệu bàn giao: 1.1 (bổ sung yêu cầu hai lượt/từ và quy tắc đồng bộ bộ đếm). Phạm vi: repository hiện tại. Không thay đổi mã nguồn ứng dụng.

**Vai trò tài liệu:** đây là tài liệu bàn giao chuẩn để Agent sửa tính năng. Phần 4 ghi nhận hiện trạng/lỗi tại thời điểm kiểm tra; phần 5 là yêu cầu đích bắt buộc của người dùng; phần 6 là tham khảo Anki; phần 8 là kế hoạch và điều kiện nghiệm thu. Khi nội dung thiết kế cũ mâu thuẫn với yêu cầu hai lượt ở phần 5, dùng phần 5 làm chuẩn. Agent không được coi việc thiếu dữ liệu hoặc build thành công là lý do giảm yêu cầu hai lượt.

## 1. Kết luận

**Chưa thể kết luận logic đã đúng. Hệ thống hiện có lỗi làm sai lịch ôn và đồng bộ tiến độ; chưa tương đương bộ lập lịch của Anki.**

Tài liệu [báo cáo thiết kế](<BAO_CAO_LOGIC_HOC_TU_FLASHCARD_SRS.md>) là đề xuất có nhiều hướng hợp lý, nhưng các khẳng định “Anki Standard”, “đồng bộ 100%”, “gọi đúng 1 lần” và “phản ánh trung thực 100% năng lực trí nhớ” chưa được mã nguồn hoặc kiểm thử chứng minh. Một số quy tắc trong chính tài liệu cũng cần sửa.

Ứng dụng dùng **biến thể SM-2 tự viết**. Anki hỗ trợ cả bộ lập lịch SM-2 cũ và FSRS. Không có FSRS tự nó không phải lỗi; vấn đề là trạng thái học, thời điểm ôn, cách chấm và cách lưu kết quả đang thiếu hoặc không nhất quán.

Ưu tiên: sửa đồng bộ state, khởi tạo phiên toàn cục, ghi review an toàn, phân biệt luyện thêm với ôn theo lịch, rồi hoàn thiện trạng thái Learning/Relearning và cutoff.

## 2. Phạm vi và độ chắc chắn

- Đã kiểm kê toàn bộ cây thư mục, quét tham chiếu SRS/progress/queue/due trên repository; đọc toàn bộ báo cáo thiết kế và đọc trực tiếp các module thực thi liên quan.
- Các luồng đã kiểm tra: scheduler, LocalStorage, React store, Flashcard, Active Recall, sổ tay từ vựng, Word Review, Dashboard, Sidebar, standalone review, bài thi, khôi phục dữ liệu và tài liệu kiểm chứng cũ.
- Tài nguyên audio/ảnh/PDF, npm cache, thư viện phụ thuộc và output sinh sẵn được phân loại theo vai trò; không tuyên bố đọc từng byte của mọi tài nguyên hay kiểm toán toàn bộ dependency. Những tài nguyên này không quyết định thuật toán lập lịch trong source.
- Kiểm chứng chạy trực tiếp module JavaScript với Node và LocalStorage giả lập; thử ngày giờ ở múi giờ Việt Nam.
- Chạy lint source thành công, có warning và không có error. Lint toàn app bị nhiễu nhiều warning từ output `.ssr` sinh sẵn. Lint hiện tại không chứng minh logic đúng và đã không bắt được biến `total` chưa khai báo.
- Không chạy phiên trình duyệt đầu-cuối hoặc build mới trong đợt này. Các nhận định về luồng React là bằng chứng tĩnh; riêng rủi ro ghi lặp StrictMode chưa được tái hiện bằng UI.
- Không thấy bộ test SRS tự động hoặc script `test` trong [package.json](<app/package.json>). [Ghi chú kiểm chứng cũ](<app/verify_notes.md>) chỉ ghi các probe thủ công, chưa bao phủ các lỗi dưới đây.

## 3. Phần đã làm đúng hoặc đúng hướng

| Nội dung | Đánh giá và bằng chứng |
|---|---|
| Cách ly thi TOEIC khỏi SRS | Đúng trong source hiện tại. Submit chỉ lưu `pushHistory`, không còn gọi review cho toàn bộ từ. [Tab5Practice](<app/src/tabs/Tab5Practice.jsx#L1965>). |
| Flashcard đưa từ vào tiến độ và SRS | Có thực hiện `markWordLearned` và `recordReview`. Tuy nhiên chưa đồng bộ SRS về React store. [Tab2Flashcards](<app/src/tabs/Tab2Flashcards.jsx#L311>). |
| Again đưa thẻ về cuối hàng đợi | Đúng với đường chấm tuần tự thông thường. Chưa có thời gian chờ hoặc trạng thái học lại được lưu bền. [Tab2Flashcards](<app/src/tabs/Tab2Flashcards.jsx#L331>). |
| Gom kết quả câu hỏi theo từ | Có triển khai, tránh việc cố ý chấm hai câu thành hai lần ôn dài hạn. Còn lỗi kiến trúc ghi trong updater và thiếu chống trùng theo UID. [Tab3Srs](<app/src/tabs/Tab3Srs.jsx#L751>). |
| Ôn tập toàn cục | Có màn hình và tải 50 bài, nhưng khởi tạo phiên có lỗi phụ thuộc dữ liệu bất đồng bộ. [SrsStandaloneView](<app/src/components/SrsStandaloneView.jsx#L31>). |
| Khóa thẻ theo bài + từ | `Lxx:word` viết thường giúp cô lập bài và tránh khác biệt hoa/thường. Chưa chuẩn hóa khoảng trắng hoặc kiểm tra khóa nhập vào. [storage](<app/src/lib/storage.js#L75>). |
| Ngày học bắt đầu 04:00 | Đúng về ý tưởng; đây là mặc định có thể cấu hình của Anki, không phải quy tắc bất biến. Hàm tạo due hiện còn sai trước 04:00. |

## 4. Lỗi cần ưu tiên sửa

### F01 — Cao: SRS lưu xuống LocalStorage nhưng React store vẫn giữ dữ liệu cũ

Nguồn: [store](<app/src/lib/store.jsx#L45>), [recordReview](<app/src/lib/srs.js#L125>), [Flashcard](<app/src/tabs/Tab2Flashcards.jsx#L324>), [Active Recall](<app/src/tabs/Tab3Srs.jsx#L800>).

`recordReview` đọc/ghi LocalStorage rồi trả card. Các đường chấm điểm không gọi `setSrs` hoặc phát sự kiện để cập nhật context. `srs` được nạp một lần khi AppProvider khởi tạo. Settings có gọi `setSrs` khi restore/reset, nhưng học và ôn không làm vậy. Active Recall còn ghi progress mà không cập nhật `setProgress`.

Hậu quả: Dashboard giữ số due cũ, không nhận card mới, phiên sau có thể lấy lại từ vừa ôn hoặc bỏ sót từ vừa học. Tải lại trang có thể khiến số liệu đúng trở lại. Probe thực tế xác nhận snapshot đã nạp vẫn `{}` sau khi recordReview, trong khi LocalStorage có card.

Cách sửa: gom việc chấm, lưu và cập nhật context vào một API dùng chung; không để từng tab tự ghi persistence độc lập. Một hành động phải cập nhật cùng phiên bản SRS/progress cho toàn bộ UI.

### F02 — Cao: Luyện thêm trong cùng ngày làm tăng interval quá nhanh

Nguồn: [Flashcard tạo deck](<app/src/tabs/Tab2Flashcards.jsx#L252>), [restart](<app/src/tabs/Tab2Flashcards.jsx#L297>), [bộ lọc Active Recall](<app/src/tabs/Tab3Srs.jsx#L673>), [scheduler](<app/src/lib/srs.js#L77>).

Flashcard luôn lấy mọi từ của bài. Active Recall theo bài/chủ đề cũng lấy mọi từ. Khi không có due, chế độ “Cần ôn hôm nay” tự rơi về toàn bộ từ đã học hoặc 12 từ mới. Mọi lần trả lời đều gọi cùng phép cập nhật SM-2, dù thẻ chưa đến hạn và chưa có ngày nào trôi qua.

Probe cùng một thời điểm, bốn lần Good liên tiếp: **interval 1 → 6 → 15 → 38 ngày**. Đây là ghi nhận năng lực dài hạn quá mức từ các lần lặp ngắn. CTA ngay sau hoàn tất Flashcard còn đưa người học vào Active Recall của cùng bài, nên có thể làm khoảng ôn nhảy tiếp ngay lập tức.

Cách sửa: chế độ due rỗng phải hiện đã hoàn thành; có nút riêng để luyện thêm. Luyện thêm mặc định không thay đổi lịch dài hạn. Nếu cho phép reschedule khi ôn sớm, phải dùng bộ lập lịch có hiểu trạng thái và thời gian đã trôi qua. Không dùng một luật “cấm mọi review cùng ngày”, vì Learning/Relearning hợp lệ cần nhiều lần trả lời trong ngày.

### F03 — Cao: Phiên SRS toàn cục không khởi tạo lại khi dữ liệu tải xong

Nguồn: [nạp bài](<app/src/tabs/Tab3Srs.jsx#L607>), [initQuiz](<app/src/tabs/Tab3Srs.jsx#L699>).

Effect gọi `initQuiz` chỉ phụ thuộc bộ lọc/bài/chủ đề. Nếu lần đầu chạy chưa có từ, hàm trả về; sau khi tải 50 bài, effect không chạy lại. Nếu lúc đầu có một bài, phiên có thể chỉ chứa bài đó và bỏ qua từ due ở các bài tải đến sau.

Cách sửa: có trạng thái loading/ready/error; chỉ tạo snapshot phiên khi dữ liệu cho phạm vi đã sẵn sàng. Sau khi bắt đầu, giữ phiên ổn định, không tái tạo sau mỗi câu trả lời hoặc mỗi cập nhật SRS.

### F04 — Cao: Ghi SRS trong React state updater không bảo đảm một lần

Nguồn: [handleReviewed](<app/src/tabs/Tab3Srs.jsx#L757>), [chốt cuối phiên](<app/src/tabs/Tab3Srs.jsx#L724>), [StrictMode](<app/src/main.jsx#L7>).

`recordReview` và `markWordLearned` nằm trong hàm truyền vào `setSessionTracker`. React yêu cầu updater thuần; StrictMode ở chế độ phát triển có thể gọi updater hai lần để phát hiện side effect. Cờ `updated.recorded` chỉ nằm trong kết quả tính lại, chưa phải khóa giao dịch đã lưu. Cùng callback cũng không loại UID câu hỏi đã nhận trước đó.

Kết luận: cấu trúc hiện tại không đủ chứng minh “chấm đúng một lần”; rủi ro ghi lặp dev dựa trên code và cơ chế React, chưa tuyên bố đã tái hiện production.

Cách sửa: tách reducer/tổng hợp thuần khỏi commit; review có ID ổn định và cơ chế idempotent. Loại callback trùng UID. Tránh mutate `rec.recorded` trực tiếp trong state cũ.

### F05 — Cao: Chưa có trạng thái Learning/Relearning và hàng đợi theo thời gian

Nguồn: [schema](<app/src/lib/storage.js#L63>), [review](<app/src/lib/srs.js#L84>), [Again Flashcard](<app/src/tabs/Tab2Flashcards.jsx#L331>), [sai Active Recall](<app/src/tabs/Tab3Srs.jsx#L287>).

Mọi thẻ chỉ có ease/interval/reps/due/lapses/lastGrade. Again luôn về interval 1 ngày, tăng lapses và giảm ease, kể cả thẻ mới. Flashcard chỉ đẩy cuối mảng; chỉ có một thẻ thì gặp lại ngay. Thoát component làm mất hàng đợi. Active Recall sai thì xem đáp án và chuyển tiếp, không có hàng đợi học lại cùng phiên.

Cần phân biệt New, Learning, Review, Relearning; lưu bước học và due của bước. Thẻ trong ngày phải so timestamp, thẻ review theo ngày học. Anki cho cấu hình bước học/lại; không bắt buộc mọi thiết lập Anki đều có cùng mốc phút cố định.

### F06 — Cao: Phím Enter và mũi tên Flashcard dùng biến không tồn tại

Nguồn: [Enter](<app/src/tabs/Tab2Flashcards.jsx#L371>), [mũi tên](<app/src/tabs/Tab2Flashcards.jsx#L396>).

Handler dùng `total`, trong khi chỉ có `totalInQueue` và `totalUnique`. Nhấn các phím này sẽ gây ReferenceError khi updater thực thi. Nút điều hướng chuột dùng `totalInQueue`, nên hành vi khác bàn phím.

Cần sửa tham chiếu và thống nhất luật chuyển thẻ/chấm; đồng thời không để việc đi qua vị trí cuối hàng đợi được coi là đã học đủ nếu còn thẻ chưa pass.

### F07 — Vừa: Due lệch một ngày học khi ôn lúc 00:00–03:59

Nguồn: [effective day](<app/src/lib/srs.js#L32>), [calculateNextDueDate](<app/src/lib/srs.js#L51>).

Ví dụ đã chạy ở UTC+7:

| Giá trị | Thực tế |
|---|---|
| Giờ ôn | 16/11/2026 01:00 |
| Ngày học hiệu dụng | 15/11/2026 |
| Interval | 1 ngày |
| Due code hiện tạo | **17/11/2026 04:00** |
| Due theo ngày học hiệu dụng + 1 | **16/11/2026 04:00** |

Hàm trừ 4 giờ khi kiểm due nhưng cộng interval từ ngày dân sự khi tạo due. Cần dùng cùng một hệ tọa độ ngày học. Ví dụ này có khoảng thực chỉ ba giờ là hợp lệ theo lịch review tính bằng ngày; không phải yêu cầu mọi thẻ phải chờ đủ 24 giờ.

Ngoài ra Dashboard/Sidebar/active pool memo hóa theo dữ liệu, không có tín hiệu chuyển ngày hoặc khi quay lại cửa sổ. Nếu mở app qua 04:00, số due có thể chưa đổi.

### F08 — Vừa: Các đường “Đã học” không nhất quán

- [Tab1](<app/src/tabs/Tab1Vocabulary.jsx#L454>) vẫn cho đánh dấu thủ công và tạo SRS, trái mô tả sổ tay read-only. Card tạo có interval=1/reps=1 nhưng giữ due=NOW từ freshCard, nên đến hạn ngay. Bỏ đánh dấu chỉ đổi progress, còn card SRS.
- [Word Review](<app/src/components/ReviewView.jsx#L32>) đọc `words[word]` nhưng [hàm ghi](<app/src/lib/storage.js#L92>) ghi `words['Lxx:word']`. Badge/toggle có thể không nhận trạng thái vừa ghi. Luồng này chỉ lưu progress, không tạo SRS.
- [Dashboard](<app/src/components/DashboardView.jsx#L150>) coi không có card là unseen; có thể khác tiến độ đã học. Sidebar đếm progress, Dashboard có nơi hợp nhất progress và SRS.

Cần định nghĩa rõ “đã tiếp cận”, “đang học”, “đến hạn”, “đã ổn định”; dùng một selector dùng chung. Bỏ đánh dấu không nên ngầm reset trí nhớ; reset/suspend là hành động riêng.

### F09 — Vừa: Thước đo nhớ và nhãn Dashboard đang gây hiểu nhầm

Nguồn: [mặt trước Flashcard](<app/src/tabs/Tab2Flashcards.jsx#L542>), [chấm trước lật](<app/src/tabs/Tab2Flashcards.jsx#L418>), [auto-grade](<app/src/tabs/Tab3Srs.jsx#L784>), [phân nhóm Dashboard](<app/src/components/DashboardView.jsx#L156>).

Mặt trước câu đục lỗ vẫn hiện ngay từ cần nhớ. Có thể chấm bằng phím trước khi xem đáp án. Đây có thể phục vụ giới thiệu từ mới, nhưng không đủ làm phép đo recall để kéo interval dài.

Active Recall tự gán Easy cho mọi câu gõ đúng lần đầu, dù người học phải suy nghĩ rất lâu. Anki định nghĩa Easy là nhớ đúng gần như không cần nỗ lực; Good mới là lựa chọn phổ biến. Gõ sai rồi sửa thành đúng không tự chứng minh recall thành công theo nghĩa Anki; cần phân biệt lỗi gõ với thực sự quên.

Dashboard coi interval<=1 là “Cần ôn”, >=7 là “Thuộc lòng”, không xét due trong phân nhóm. Vì vậy thẻ Good hẹn mai vẫn nằm “Cần ôn”, thẻ 30 ngày quá hạn lâu vẫn “Thuộc lòng”. Anki dùng mature từ 21 ngày trong thống kê và mature cũng không bảo đảm thuộc tuyệt đối. Nên hiển thị riêng độ ổn định và trạng thái đến hạn.

### F10 — Vừa: Persistence và dữ liệu nhập thiếu xác thực

Nguồn: [read/write](<app/src/lib/storage.js#L13>), [import](<app/src/lib/storage.js#L205>), [review](<app/src/lib/srs.js#L77>).

Lỗi ghi LocalStorage bị nuốt; UI vẫn báo thành công. Import nhận object mà không validate card/schema. Probe card có `reps:'2'` cho kết quả `reps:'21'` vì cộng chuỗi; các dữ liệu sai khác có thể tạo NaN hoặc lỗi ngày. Invalid due được đổi thành ngày UTC hiện tại, khác valid path dùng local date; đây là che giấu lỗi dữ liệu.

Cần validate/normalize dữ liệu, version schema/migration, kiểm lỗi ghi và thông báo rõ khi chưa lưu. Nhiều cửa sổ cùng đọc-sửa-ghi nguyên map có nguy cơ mất cập nhật; chưa có khóa hoặc cơ chế đồng bộ cửa sổ.

## 5. Đặc tả bắt buộc: mỗi từ có đúng hai lượt ôn

Đây là yêu cầu sản phẩm cần giữ nguyên khi Agent sửa mã nguồn:

> **Mỗi từ trong một phiên Active Recall phải được kiểm tra đúng hai lượt:**
> 1. `base_word`: gõ từ gốc dựa trên định nghĩa tiếng Anh.
> 2. `context_word`: điền từ vào một câu ngữ cảnh được chọn ngẫu nhiên từ bộ đề/corpus của chính từ đó.

Hai lượt này là **hai câu hỏi trong cùng một phiên**, được gộp thành **một lần đánh giá SRS cho một từ** trong thiết kế bàn giao này. Không được gọi `recordReview()` sau từng câu. Chỉ sau khi cả hai lượt của từ đã kết thúc, hệ thống mới tổng hợp kết quả và commit một review duy nhất cho khóa từ đó.

### 5.1. Quy tắc tạo câu hỏi

Với mỗi `WordRecord` đủ điều kiện ôn:

```text
questions[wordKey] = [
  { uid: `base:${wordKey}:${sessionId}`, type: 'base_word' },
  { uid: `context:${wordKey}:${sessionId}`, type: 'context_word' },
]
```

- `base_word` luôn bắt buộc. Nếu thiếu `definition_en`, đó là lỗi dữ liệu/coverage và phải được ghi rõ; không được âm thầm giảm số lượt mà vẫn báo phiên hoàn chỉnh. Đáp án phải là từ gốc của `wordKey`, các biến thể chấp nhận chỉ được khai báo rõ trong dữ liệu.
- `context_word` luôn bắt buộc theo yêu cầu sản phẩm. Nguồn chuẩn là **câu có sẵn trong bộ đề/corpus của ứng dụng** liên quan đúng từ đang ôn. Agent phải kiểm kê và xây pool từ câu trong bộ đề, `srs_sentence`, ví dụ trong bài và câu word family đã có; không mặc định chỉ lấy câu ví dụ đầu tiên. Mỗi candidate phải lưu `sourceKind`, bài/đề nguồn, ID câu hoặc vị trí nguồn, câu gốc, đáp án và liên kết tới `wordKey`. Không được lấy câu không có quan hệ với từ rồi gán lịch cho từ đó.
- Không gọi AI tạo câu hoặc đưa câu ngoài bộ đề vào pool trong lúc ôn để bù thiếu dữ liệu. Nếu corpus không có câu hợp lệ, bộ nạp phải báo thiếu câu và danh sách cần bổ sung; không được coi từ chỉ có một câu là phiên “đủ hai lượt”. Câu bổ sung sau này phải được kiểm tra dữ liệu trước khi trở thành nguồn chính thức.
- Candidate hợp lệ phải có ít nhất một chỗ trống đánh giá được, đáp án phù hợp ngữ pháp của câu, và các đáp án chấp nhận đã được khai báo. Dạng chia thì/họ từ được phép nếu dữ liệu liên kết rõ với từ gốc. Không lộ đáp án qua tiêu đề, tooltip, collocation hoặc bản dịch khi đang kiểm tra.
- Chọn ngẫu nhiên một candidate cho mỗi từ khi tạo phiên; lưu lựa chọn đó trong snapshot để reload không đổi câu/đáp án. Nếu có từ hai candidate trở lên, ưu tiên không lặp candidate của lần ôn trước; nếu chỉ có một candidate thì được dùng lại. Không yêu cầu các câu khác nhau luôn có xác suất bằng nhau nếu đã áp dụng quy tắc tránh lặp.
- Hai UID phải ổn định trong một `sessionId`, không dùng random UID mới cho cùng một câu khi component re-render. Callback cùng UID chỉ được tính một lần.
- Thứ tự hai câu có thể shuffle giữa các từ, nhưng mỗi từ phải có đủ một `base_word` và một `context_word`. Không được shuffle làm mất hoặc nhân đôi câu.
- Một phiên gồm `N` từ phải có chính xác `2N` câu hỏi. Ví dụ Dashboard báo **15 từ đến hạn** thì màn hình SRS phải tạo **15 từ × 2 = 30 câu**, hiển thị rõ `Đã kiểm tra 0/15 từ · Câu 1/30`; tuyệt đối không để người dùng hiểu `1/10` là còn 10 từ.

### 5.2. Mô hình trạng thái phiên và bộ đếm UI

Tách các khái niệm sau, không dùng một biến `quizQuestions.length` cho mọi nhãn:

```text
DueWord = một từ có card SRS và isDue(card, now) === true
SessionWord = một từ được chụp vào phiên hiện tại
Question = một trong hai lượt của SessionWord
```

State tối thiểu:

```text
session = {
  sessionId,
  status: 'loading' | 'incomplete' | 'ready' | 'active' | 'finished' | 'empty' | 'error',
  words: SessionWord[],
  questions: Question[],       // luôn có 2 phần tử cho mỗi wordKey
  currentQuestionIndex,
  completedQuestionUids,
  completedWordKeys,
}
```

UI bắt buộc hiển thị tách biệt:

- Dashboard: `15 từ đến hạn` — đếm `DueWord`, không đếm câu.
- SRS hiển thị chính: `Đã kiểm tra 0/15 từ · Câu 1/30`. Số từ đã kiểm tra chỉ tăng khi đủ hai câu và commit đã lưu thành công. Nếu shuffle giữa nhiều từ, không dùng `Từ 1/15` như vị trí của từ hiện tại vì không có thứ tự từ tuyến tính.
- `Câu 1/30` là vị trí câu đang hiển thị, không phải số câu đã hoàn thành; bộ đếm hoàn thành câu riêng bắt đầu từ 0/30. Khi kết thúc, hiển thị `Đã kiểm tra 15/15 từ · Đã trả lời 30/30 câu`.
- Progress bar chính của mục tiêu ôn dùng `completedWordKeys.size / words.length`, không dùng `currentQuestionIndex / questions.length` để gọi là tiến độ từ.
- Khi một câu hoàn thành, chỉ tăng tiến độ câu. Khi đủ hai câu của một từ, mới tăng tiến độ từ và chốt SRS.
- Nếu có 15 due words nhưng chỉ dựng được 10 questions, session phải vào `error`/`incomplete` và báo số liệu coverage; không được hiển thị như phiên bình thường.

### 5.3. Quy tắc tổng hợp kết quả hai lượt

Mỗi câu lưu độc lập kết quả nhập liệu:

```text
QuestionResult = {
  uid,
  wordKey,
  type: 'base_word' | 'context_word',
  attempts,
  isCorrect,
  wrongCount,
  completedAt,
}
```

Khi đủ đúng hai UID của một `wordKey`:

1. Xác nhận có đủ cả `base_word` và `context_word`.
2. Khóa wordKey để callback lặp không thể commit lần hai.
3. Tổng hợp grade theo policy sản phẩm đã công bố.
4. Gọi scheduler/recordReview đúng một lần cho wordKey.
5. Cập nhật `setSrs` và `setProgress` từ cùng một transaction UI.
6. Đánh dấu `completedWordKeys`.

Policy mặc định cho lần triển khai này (quyết định kỹ thuật đề xuất để Agent có thể thực thi; không phải quy tắc do Anki bắt buộc): mỗi câu tối đa hai lần gửi đáp án không rỗng. Ô trống không tính lượt; đáp án đúng kết thúc câu; sai lần đầu cho nhập lại, sai lần hai kết thúc câu thất bại. Một câu đã kết thúc không được sửa kết quả để tính lại lịch. Chuẩn hóa hoa/thường, khoảng trắng và biến thể được dữ liệu khai báo; không tự coi từ gần giống là đúng.

Ma trận tổng hợp bắt buộc theo policy mặc định:

| Base word | Context word | Grade gợi ý |
|---|---|---:|
| Đúng ngay lần đầu | Đúng ngay lần đầu | 3 Good mặc định; chỉ 4 Easy nếu người học tự xác nhận rất dễ |
| Một hoặc cả hai câu đúng sau nỗ lực/sai một lần | Câu còn lại đúng | 3 Good |
| Một câu hoặc cả hai câu không nhớ sau giới hạn thử | Bất kỳ | 1 Again |

Hai câu không được tự động biến thành Easy chỉ vì không có lỗi gõ. Đây là bài kiểm tra recall và cần giữ ý nghĩa nút theo Anki: Again = quên, Hard/Good = nhớ nhưng có nỗ lực, Easy = nhớ gần như không cần nỗ lực. Nếu sản phẩm muốn dùng một công thức khác, phải ghi rõ đó là policy riêng, không gọi là chuẩn Anki.

### 5.4. Hành vi khi thiếu dữ liệu hoặc phiên bị gián đoạn

- Không có câu context hợp lệ: không giảm âm thầm từ hai câu xuống một câu; báo `incomplete_context` và đưa từ vào danh sách dữ liệu cần sửa. Giữ từ đó đến hạn, không tự dời due, không coi là đã hoàn thành và không sinh câu AI để lấp chỗ trống.
- Tải bài toàn cục chưa xong: hiển thị `Đang tải X/50 bài`, chưa tạo phiên chính thức. Khi tải xong, tạo một snapshot duy nhất.
- Không có due words: hiển thị `0 từ đến hạn`, kết thúc phiên. Nút `Luyện thêm` là luồng riêng và không được gọi scheduler review dài hạn mặc định. Nếu người dùng chủ động chọn luyện thêm, UI phải ghi rõ đây là luyện ngoài lịch và không được hiển thị kết quả như số due đã hoàn thành.
- Người dùng reload/unmount giữa hai câu: giữ session draft hoặc đánh dấu từ chưa hoàn tất; không commit nửa phiên như một review hoàn chỉnh.
- Người dùng bấm lại cùng câu hoặc callback bị phát lại: UID idempotency giữ kết quả đầu tiên, không tăng `reps` lần hai.

### 5.5. Tiêu chí nghiệm thu riêng cho yêu cầu hai lượt

| Tình huống | Kết quả bắt buộc |
|---|---|
| 1 due word có đủ dữ liệu | Tạo đúng 2 câu: 1 base + 1 context; chốt đúng 1 review. |
| 15 due words có đủ dữ liệu | Tạo đúng 30 câu; UI hiển thị 15 từ và 30 câu tách biệt. |
| 15 due words nhưng 1 từ thiếu context | Báo 15 từ đến hạn, 14 từ sẵn sàng (28 câu), 1 từ thiếu dữ liệu; giữ due của từ thiếu. Chỉ bắt đầu 14 từ sau hành động rõ ràng của người học; kết thúc ghi “Hoàn tất 14 từ của phiên, còn 1 từ thiếu câu”, không ghi “hết từ đến hạn”. |
| Hai câu của một từ hoàn thành theo thứ tự bất kỳ | Chỉ chốt sau khi đủ đúng hai loại câu. |
| Cùng UID callback hai lần | Chỉ tính một kết quả, không tăng reps/interval hai lần. |
| Câu base đúng, context sai | Một grade tổng hợp theo policy; không ghi hai review riêng. |
| Đổi bộ lọc khi đang làm | Hủy/lưu draft có chủ đích; không mất âm thầm và không commit nửa chừng. |
| Dashboard báo N nhưng SRS tạo M câu | UI phải báo coverage/incomplete; không được hiển thị `1/M` như số từ còn lại. |

### 5.6. Tính nhất quán Dashboard → phiên → lịch ôn

Dùng chung selector trên cùng phiên bản dữ liệu để tạo `dueWordKeys` và số trên Dashboard. Không đếm mọi khóa lưu trong LocalStorage mà không đối chiếu danh mục từ hiện hành. Khóa mồ côi/không tải được bài phải được liệt kê để phục hồi dữ liệu, không bỏ âm thầm khỏi một màn hình nhưng vẫn tính ở màn hình khác.

Tại thời điểm bắt đầu phiên, lưu `snapshotAt`, `studyDayKey`, `dataVersion`, `dueWordKeys`, `eligibleWordKeys`, `blockedWords` và câu context đã chọn. Với cùng snapshot:

```text
dueCount = eligibleWordKeys.length + blockedWords.length
session.words.length = eligibleWordKeys.length
session.questions.length = 2 * session.words.length
```

Nếu có hạn mức ngày hoặc chia phiên nhỏ, phải hiển thị số đang ôn và số còn chờ riêng, ví dụ `Phiên này 10/15 từ đến hạn · còn 5 từ chờ`, không đổi nghĩa con số 15. Lần sửa lỗi hiện tại không tự thêm giới hạn 5/10/12 từ vào phiên.

Dashboard là số due đang sống; tổng số câu/từ của phiên đã bắt đầu là snapshot cố định. Từ mới đến hạn trong lúc làm không được chèn âm thầm; UI có thể báo còn lượt tiếp theo. Sau mỗi commit, cập nhật Dashboard từ card mới: Good hẹn tương lai làm giảm due; Again chuyển Relearning có thể vẫn còn cần học, nên không được ép số due về 0 bằng cách trừ theo số từ đã kiểm tra.

### 5.7. Hai lượt bắt buộc và học lại khi quên

“Đúng hai lượt” nghĩa là **hai câu cơ sở của mỗi từ trong một vòng đánh giá**, không phải hai lần tăng reps, không phải tối đa hai lần thử gõ, cũng không phải giới hạn tổng số lần ôn cả đời của từ.

- Hai câu cơ sở luôn là từ gốc và context. Một câu có thể có hai lần thử theo phần 5.3; thử lại không tạo câu cơ sở mới.
- Nếu một câu thất bại, kết quả tổng hợp là Again và chuyển từ sang Relearning. Không cho lần trả lời lại ngay sau khi xem đáp án ghi đè thành Good/Easy của vòng vừa thất bại.
- Các bước Relearning hợp lệ thuộc hàng đợi riêng có thời gian và ID bước. UI ghi rõ `Học lại`, hiển thị thêm số bước; không làm mẫu số 30 câu cơ sở âm thầm tăng thành 31/32. Việc hoàn tất hai câu không đồng nghĩa đã hết các bước học lại.
- “Một commit/từ” áp dụng cho một cặp câu của một vòng đánh giá. Review log có thể lưu các sự kiện bước học lại riêng theo scheduler, nhưng không được coi chúng là các lần review ngày độc lập để nhảy chuỗi 1→6→15 trong vài phút.

### 5.8. Commit, resume và dữ liệu bền

ID commit của cặp câu là `pair:${sessionId}:${wordKey}`. Repository có thể dùng cấu trúc lưu khác, nhưng phải bảo đảm:

1. Chỉ commit khi có hai kết quả hoàn chỉnh của đúng hai loại câu, kiểm tra lại version card trước cập nhật.
2. Card mới, log review và dấu đã xử lý ID phải được lưu nhất quán. `setState` và React reducer chỉ tính dữ liệu, không ghi storage. Nếu persistence hiện tại không hỗ trợ tính nhất quán này, Agent phải bổ sung cơ chế giao dịch/khóa phù hợp và test phục hồi lỗi.
3. Chỉ sau khi lưu thành công mới tăng số từ đã kiểm tra và publish state cho UI. Khi lưu lỗi, giữ draft để thử lại cùng commit ID, không tăng reps lần nữa.
4. Lưu draft phiên bằng array/object JSON; serialize Set/Map rõ ràng. Reload tiếp tục đúng câu, nguồn ngẫu nhiên, kết quả và các commit đã xử lý.
5. Hai cửa sổ cùng ôn một card phải phát hiện version conflict và tải trạng thái mới; không last-write-wins âm thầm. Reset/import từ cửa sổ khác phải vô hiệu draft không còn hợp lệ.
6. `completedWordKeys` nghĩa là hoàn tất cặp câu và lưu thành công, không có nghĩa “đã thuộc”. Màn hình kết thúc cần nêu số từ đã kiểm tra, số Again và số còn cần học lại.

## 6. Đối chiếu Anki và hướng hoàn thiện

| Thành phần | Hiện tại | Hướng đề xuất |
|---|---|---|
| Thuật toán | SM-2 tùy biến | Công bố rõ biến thể hoặc dùng thư viện FSRS đã kiểm thử; không cần viết lại toàn bộ Anki. |
| Learning/Relearning | Không có trạng thái/bước lưu bền | State machine và hàng đợi timestamp; thí dụ bước 1 phút, 10 phút là cấu hình tham khảo, không phải bắt buộc. |
| Hard | `oldInterval * ease * 0.6` sau giai đoạn đầu | Nếu tương thích legacy Anki, dùng cơ chế Hard riêng; mặc định Anki khoảng 1.2 lần interval cũ. Probe ease=1.3, interval10 cho Hard8 ngày, tức giảm khoảng dù trả lời đúng. |
| Good/Easy | Lần đầu đều 1 ngày; lần 2 Good6/Easy8; Easy tự động vì gõ đúng | Dùng luật theo trạng thái. Gõ đúng mặc định Good; Easy cần đánh giá nỗ lực phù hợp. Hiện next interval trên nút trước commit. |
| Ease | Khởi đầu2.5, min1.3; Hard-.14, Easy+.1, Again-.2 | Có hằng số gần SM-2 nhưng không giống đầy đủ legacy Anki; không giảm review ease vì sai trong Learning. FSRS dùng mô hình khác. |
| Quá hạn | Không có thời gian từ lần ôn trước | Lưu lastReviewedAt; dùng thuật toán xử lý elapsed/overdue, xếp ưu tiên backlog theo chính sách rõ ràng. |
| Fuzz | Không có; shuffle câu hỏi không phải fuzz lịch | Phân tán due nhẹ theo thuật toán để 12/60/600 từ không dồn cùng ngày. |
| Giới hạn ngày | Không có | Tùy chọn số từ mới/ngày, lượng ôn/ngày và hiển thị backlog bị giới hạn; ưu tiên ôn trước học mới. |
| Leech | Chỉ đếm lapses | Ngưỡng từ hay quên, gắn cờ/suspend tùy cấu hình và đề nghị sửa nội dung; lapses phải mang nghĩa rõ ràng. |
| Hai kỹ năng/từ | Gộp từ gốc + câu ngẫu nhiên, cùng một lịch | **Giữ bắt buộc hai câu trong cùng phiên và một lịch SRS cho mỗi từ theo phần 5.** Anki có thể tách card theo kỹ năng, nhưng Agent không được tự tách hai lịch hoặc bury một trong hai câu sang hôm sau. Có thể giãn hai câu bằng câu của từ khác để giảm gợi nhớ. |
| Lịch sử SRS | Ghi đè snapshot; history hiện là thi TOEIC | Review log có ID, thời điểm, rating, source, state trước/sau, version scheduler. Hỗ trợ undo, kiểm toán, thống kê retention và FSRS sau này. |
| Nhắc ngoài app | Không tìm thấy Notification/service worker/push trong source | Hiện là danh sách due trong app. Nếu cần thông báo khi đóng app phải thiết kế riêng quyền thông báo và cơ chế chạy nền/server; không suy ra đã có từ chữ “nhắc”. |

Không nên sửa tất cả khác biệt thành “giống Anki” một cách máy móc. Lựa chọn tách hay gộp kỹ năng, giới hạn 365 ngày, hoặc tự chấm điểm có thể là chủ đích sản phẩm; phải mô tả đúng và kiểm chứng tác động.

## 7. Những điểm phải sửa trong báo cáo thiết kế ban đầu

1. “Again bắt buộc đẩy cuối mảng” là một cách đơn giản hóa, không phải chuẩn đầy đủ của Anki. Anki lập lịch theo state, bước và thời gian; có thể learn-ahead theo cấu hình.
2. 04:00 là mặc định có thể thay đổi, cần đồng nhất ngày hiệu dụng khi tạo và kiểm due. Code mẫu hiện có lỗi trước 04:00.
3. “Hai câu đúng = Easy” và “sai một lần rồi đúng = Good” là chính sách tự đặt, không phải ma trận chuẩn Anki.
4. Với sản phẩm này, đã chốt **hai câu cho mỗi từ trong cùng phiên, một lần chấm SRS tổng hợp**. Không tự chuyển sang hai card có lịch độc lập khi tham khảo Anki. Bảo vệ commit bằng ID giao dịch lưu bền, không chỉ cờ trong updater.
5. Ma trận tài liệu không bao phủ trường hợp mỗi câu sai một lần: bảng nói Again khi bất kỳ câu nào sai >=2, còn code tổng hai lỗi cũng Again. Cần thống nhất đặc tả.
6. “Đã học” ở lần chạm đầu tiên chỉ nên hiểu là đã tiếp cận; bấm Again không có nghĩa đã nhớ hay thuộc.
7. Các tên storage trong tài liệu (`toeic_srs`, `toeic_progress`) khác namespace thực tế `toeic600.srs`, `toeic600.progress`; phải cập nhật để tránh thao tác sai dữ liệu.
8. Không dùng các câu khẳng định “100% chuẩn”, “chuẩn xác sẵn sàng triển khai” khi chưa có test trạng thái, cutoff, persistence và end-to-end.

## 8. Thứ tự sửa và tiêu chí nghiệm thu

### Đợt 1 — Tính đúng của dữ liệu và phiên

- API review chung cập nhật persistence + React context, có báo lỗi lưu.
- Phiên due đúng phạm vi, chỉ bắt đầu khi đã tải dữ liệu, due rỗng không tự lấy thẻ khác.
- Reducer thuần; commit có ID chống lặp, UID câu hỏi không được cộng hai lần.
- Sửa phím `total`, đồng bộ key progress và các đường đánh dấu học.
- Luyện thêm không kéo dài lịch ôn một cách âm thầm.

### Đợt 2 — Hoàn thiện scheduler

- Chọn rõ legacy SM-2 tương thích hay FSRS; lưu version thuật toán.
- State New/Learning/Review/Relearning, phút/ngày và bước học lưu bền.
- Sửa cutoff, clock refresh, migration due cũ và dữ liệu nhập.
- Rating đúng ý nghĩa; mặt trước không lộ đáp án khi đang đánh giá recall.

### Đợt 3 — Quản lý khối lượng và chất lượng

- Giới hạn từ mới/ngày, thứ tự backlog, fuzz, leech, undo/review log.
- Đổi nhãn thống kê để không đánh đồng interval với “thuộc lòng”.
- Theo dõi tỷ lệ nhớ đúng trên lần ôn đến hạn trước khi tối ưu retention.

### Checklist bàn giao triển khai cho Agent

| Thứ tự | Phạm vi sửa | Sản phẩm đầu ra/điều kiện hoàn tất |
|---|---|---|
| 1 | [storage](<app/src/lib/storage.js>), [store](<app/src/lib/store.jsx>), [scheduler](<app/src/lib/srs.js>) | API commit dùng chung, lỗi lưu được truyền về, ID chống ghi lặp, schema/version và migration có backup. |
| 2 | [lessonLoader](<app/src/lib/lessonLoader.js>), dữ liệu bài/đề và module pool câu mới nếu cần | Mỗi từ có candidate context có nguồn và đáp án; báo cáo coverage theo danh mục thực tế, không hard-code đủ 600 từ khi dữ liệu khác. |
| 3 | [Tab3Srs](<app/src/tabs/Tab3Srs.jsx>), [SrsStandaloneView](<app/src/components/SrsStandaloneView.jsx>) | Chờ dữ liệu sẵn sàng, snapshot ổn định, đúng 2 câu/từ, UID ổn định, draft resume, ma trận chấm và một commit/cặp. |
| 4 | [Dashboard](<app/src/components/DashboardView.jsx>), [Sidebar](<app/src/components/Sidebar.jsx>) | Cùng selector due, bộ đếm ghi đơn vị, trạng thái thiếu dữ liệu và backlog rõ ràng, cập nhật sau commit/focus/chuyển ngày. |
| 5 | [Flashcard](<app/src/tabs/Tab2Flashcards.jsx>), [Tab1](<app/src/tabs/Tab1Vocabulary.jsx>), [Word Review](<app/src/components/ReviewView.jsx>) | Đồng bộ key/state, sửa phím lỗi, không tự tăng lịch khi luyện thêm và không lộ đáp án khi đo recall. |
| 6 | Scheduler và persistence | Cutoff đồng nhất, phân biệt timestamp/ngày học, Learning/Relearning bền; không đổi thuật toán hoặc reschedule hàng loạt dữ liệu cũ mà thiếu migration/test. |
| 7 | Test và kiểm chứng UI | Test tự động các hợp đồng phần 5; chạy build/lint; kiểm tra UI với fixture 15 từ/30 câu và dữ liệu đủ/thiếu, không dùng tiến độ thật để test phá hủy. |

Agent phải bàn giao danh sách file đã sửa, quyết định scheduler thực tế, kết quả test có thể chạy lại, coverage pool câu và những phần chưa hoàn tất. Build/lint pass không thay thế test hành vi. Không tự xóa dữ liệu tiến độ để che lỗi migration hoặc làm số đếm khớp.

Các chi tiết mặc định về chấm điểm, retry và tránh lặp câu trong phần 5 là đề xuất triển khai của tài liệu. Yêu cầu người dùng bắt buộc là **mỗi từ có hai lượt từ gốc + câu random từ corpus**, giữ cùng phiên; tham khảo Anki không được làm mất một trong hai lượt.

### Bộ kiểm thử tối thiểu trước khi gọi tính năng hoàn thiện

| Trường hợp | Kết quả mong đợi |
|---|---|
| 23:59, 00:01, 03:59, 04:00, 04:01 | Cùng quy ước ngày học; interval1 cộng đúng một ngày học. |
| Cuối tháng/năm, năm nhuận, múi giờ đổi | Không lệch ngày hay tạo due không hợp lệ; chính sách timezone rõ ràng. |
| Again rồi thoát/reload | Học lại vẫn còn trong trạng thái lưu bền. |
| Good nhiều lần trong luyện thêm | Không tăng interval dài hạn theo số lần bấm đơn thuần. |
| StrictMode và callback UID lặp | Một review ID chỉ commit một lần. |
| Mở SRS trước khi tải xong 50 bài | Tải xong phải tạo đúng tập từ; không treo, không thiếu bài. |
| Ôn xong quay Dashboard | Due giảm ngay; từ mới xuất hiện ngay trong state. |
| Qua 04:00 khi app đang mở | Due tự tính lại hoặc tính lại khi focus. |
| Không có due | Hiện hoàn tất; luyện thêm là lựa chọn riêng. |
| Nộp thi TOEIC | SRS trước/sau giống nhau; chỉ history thi thay đổi. |
| Import card sai, LocalStorage không ghi được | Từ chối/sửa dữ liệu có kiểm soát, không báo lưu thành công giả. |
| Hai cửa sổ cùng ôn | Không mất cập nhật, không tăng hai lần do cùng một event. |
| Progress Word Review/Tab1/Flashcard | Mọi màn hình đọc cùng khóa và đúng nghĩa trạng thái. |

## 9. Nguồn tham khảo chính thức

Đã đọc nội dung tài liệu chính thức; bản Markdown GitHub được dùng để tránh trang HTML bị cắt bởi công cụ.

- [Anki — Studying: Answer Buttons, Fuzz, Siblings, Falling Behind](https://docs.ankiweb.net/manual/studying)
- [Anki — Deck Options: Learning, Lapses, Daily Limits, FSRS, Advanced](https://docs.ankiweb.net/manual/deck-options)
- [Anki — Preferences: Next day starts at, Learn ahead](https://docs.ankiweb.net/manual/preferences)
- [Nguồn Markdown Studying](https://raw.githubusercontent.com/ankitects/anki-manual/main/src/studying.md)
- [Nguồn Markdown Deck Options](https://raw.githubusercontent.com/ankitects/anki-manual/main/src/deck-options.md)
- [Nguồn Markdown Preferences](https://raw.githubusercontent.com/ankitects/anki-manual/main/src/preferences.md)

Kết luận tại thời điểm kiểm định ban đầu: **chưa đạt tính đúng đầu-cuối**. Trạng thái triển khai mới được ghi bên dưới; không coi các phát hiện ban đầu là kết quả kiểm thử của bản mới.

## 10. Cập nhật triển khai — 17/11/2026

Đã sửa source và build production:

- Store đồng bộ SRS/progress sau lưu, khi focus, thay đổi storage và chuyển ngày; Dashboard/Sidebar dùng cùng danh sách due theo danh mục.
- Active Recall chờ tải đủ 50 bài mới tạo phiên, không lấy 12 câu từ phần dữ liệu tải sớm; đủ N từ tạo 2N câu có UID cố định. Due rỗng không tự lấy từ khác.
- UI tách số từ và số câu: `16 từ đến hạn · 32 câu`; phiên ghi `Đã kiểm tra 0/16 từ · Câu 1/32`. Thêm thời điểm lượt ôn kế tiếp ở Dashboard và due của từ vừa chốt cặp câu.
- Kết quả cặp câu commit ngoài React updater; có ID chống lặp/version check, giữ lịch khi luyện thêm; lỗi lưu hiện rõ và cho thử lại. Có draft phiên giữ câu đã chọn/kết quả để tiếp tục sau reload; draft thay đổi version/reset không được tiếp tục âm thầm.
- Scheduler sửa cutoff trước 04:00, thêm Learning/Relearning theo timestamp, không tăng lịch cho ôn sớm, Hard không làm giảm interval. Không reschedule hàng loạt card cũ.
- Flashcard sửa phím total chưa khai báo, chống phím giữ/chấm lặp, chấm sau lật; tiến độ Word Review đọc đúng key.
- Validation backup/card và lỗi quota được xử lý thay vì báo lưu thành công giả.

Kiểm chứng: 15/15 test Node đạt; build production đạt; lint phần SRS có warning nhưng 0 errors; diff formatting đạt. Chưa xác minh trực tiếp bản đang được phục vụ trên trình duyệt của người dùng, do chưa có URL/target ứng dụng học từ được xác định. Ảnh cũ còn nhãn `1/12` là giao diện trước bộ đếm mới; phải refresh bản đã build/deploy đúng ứng dụng để thấy thay đổi.

Giới hạn/dữ liệu cần xử lý:

- Corpus thực tế có 599 từ. `secure` ở bài 31 thiếu `definition_en`; phiên chứa từ này báo thiếu dữ liệu, không sinh câu gốc giả và không dời due. Test coverage xác nhận đúng lỗi này; chưa tự thay đổi nội dung gốc.
- Chưa hoàn thiện pool trích từ mọi phần đề thi ngoài các câu corpus đã liên kết; nguồn hiện có srs_sentence, examples và word families. Chưa có thuật toán tránh lặp candidate giữa các phiên.
- Có version check và Web Locks cho đường commit Active Recall khi trình duyệt hỗ trợ, nhưng chưa bảo đảm giao dịch đa cửa sổ cho mọi đường ghi. Import nhiều khóa chưa có rollback đầy đủ khi quota lỗi giữa chừng.
- FSRS, giới hạn ngày, fuzz, leech và undo đầy đủ chưa triển khai. Các phần này vẫn là backlog, không được tuyên bố đã tương đương Anki.

Gợi ý UI để người dùng duyệt thêm (chưa đổi toàn bộ giao diện): rút tiêu đề câu gốc thành `Từ gốc`, câu ngữ cảnh thành `Điền từ`; thu gọn tiến độ về một dòng, chuyển bắt đầu lại vào menu phụ, đổi `Thuộc lòng` thành nhãn độ ổn định phù hợp và giảm chữ in hoa. Giữ thông báo lỗi/thiếu dữ liệu vì chúng giải thích số lượng phiên.
