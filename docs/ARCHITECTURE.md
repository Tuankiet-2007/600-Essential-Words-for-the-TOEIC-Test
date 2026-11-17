# Kiến trúc và API

Cập nhật theo source ngày 17/11/2026. [Mục lục dự án](<../README.md>) · [SRS](<SRS.md>) · [Dữ liệu](<DATA.md>)

## Frontend

React 19, Vite 8, Tailwind CSS v4; ứng dụng tĩnh, không có backend SRS hoặc đồng bộ tài khoản. Các view chính là Dashboard, SRS standalone, bài học, Word Review theo chủ đề và Settings.

| Thành phần | Trách nhiệm |
|---|---|
| [App](<../app/src/App.jsx>) | Shell, chuyển view/tab, lazy load |
| [Store](<../app/src/lib/store.jsx>) | AppProvider/useApp, state dùng chung, đồng bộ persistence, đồng hồ due |
| [Loader](<../app/src/lib/lessonLoader.js>) | Nạp JSON, chuẩn hóa các dạng dữ liệu OCR |
| [Storage](<../app/src/lib/storage.js>) | Settings, progress, SRS, lịch sử thi, annotations, backup/import |
| [Scheduler](<../app/src/lib/srs.js>) | Review thuần, due, lưu review có ID/version |
| [Recall session](<../app/src/lib/recallSession.js>) | Tạo cặp câu và tổng hợp kết quả thuần |
| [UI dùng chung](<../app/src/components/ui.jsx>) | Button, Card, ProgressBar, phát âm, toast |
| [Assets](<../app/src/lib/assets.js>) | URL, highlight và cloze |

Không giữ quyền sở hữu file theo tên Agent cố định. Khi làm song song, khai báo phạm vi từng nhiệm vụ; module dùng chung mới được phép nếu có trách nhiệm rõ và kiểm thử.

## Luồng dữ liệu

```text
public/ JSON → lessonLoader → React views
LocalStorage ↔ storage/scheduler → state-changed → AppProvider → Dashboard/phiên SRS
```

Loader thử JSON bài trong `lessons_json/`, sau đó `sample_lessons/`; thiếu cả hai thì trả trạng thái chưa trích xuất. Vite có thể trả HTML với HTTP 200 cho URL JSON không tồn tại, nên phải kiểm content type/parse, không chỉ status.

Nguồn OCR có thể dùng `listening` cấp bài, `practice.part5/6/7`, options dạng mảng và key `number`. UI đọc dạng đã chuẩn hóa qua loader; không ép nguồn thô giống một ví dụ mẫu duy nhất. Họ từ có thể nằm ở cấp bài và theo nhóm; dùng `familiesForEntry` thay vì tự giả định mỗi từ có đủ bốn từ loại.

`publicDir: '../public'` trong [Vite config](<../app/vite.config.js>), `base: './'` để build dưới subpath Pages. Khi đổi cấu hình build, đối chiếu cả [build thay thế](<../app/scripts/build.mjs>) và [dev server thay thế](<../app/scripts/dev-server.mjs>).

## Persistence

Các khóa chính: `toeic600.settings`, `toeic600.srs`, `toeic600.progress`, `toeic600.history`, `toeic600.annotations`. Draft SRS dùng prefix `toeic600.recallDraft:`.

- `srsKey(lessonId, word)` tạo khóa `L01:abide by` (viết thường). Không tự thay normalization hoặc đổi ID mà thiếu migration.
- Progress nằm dưới `progress.L01.words[srsKey(...)]`; không đọc bare `words[word]` làm nguồn duy nhất.
- `saveSrs` validate card, ghi rồi phát `toeic600:state-changed`. Lỗi ghi phải được xử lý ở caller.
- `loadSrs` ném lỗi nếu JSON/card sai; không thay bằng `{}` rồi ghi đè dữ liệu hỏng. Provider giữ trạng thái đọc thành công gần nhất và báo lỗi.
- Store nghe sự kiện cùng cửa sổ, `storage` cửa sổ khác, focus/visibility và cập nhật đồng hồ due.
- `history` là lịch sử thi; `reviewLog` trong card là lịch sử SRS, không dùng thay nhau.

Import validate các section trước khi ghi, nhưng chưa có rollback đầy đủ cho nhiều khóa khi lỗi quota giữa chừng. Backup xuất cả settings, có thể gồm API key; xem [backlog](<BACKLOG.md>).

## API quan trọng

Chữ ký rút gọn; source là nơi tra các trường mở rộng.

```js
// srs.js
review(card, grade, now?) // thuần; không ghi storage
isDue(card, now?)
calculateNextDueDate(interval, now?)
recordReview(lessonId, word, grade, { reviewId, expectedVersion, ...metadata })
cardsForLesson(lessonId)
buildQueue(lessonId, words, now?)

// recallSession.js
buildQuizSession(records, { sessionId, random? })
// => { sessionId, questions, words, missing, complete }
aggregateQuestionResults(results)

// storage.js
loadSrs(); saveSrs(map);
loadProgress(); markWordLearned(lessonId, word, learned?);
exportAllData(); importAllData(payload); clearAll();
```

`useApp()` còn cung cấp điều hướng, `srsNow`, `dueWordKeys`, `orphanedCardKeys`, `stateError`. Không lấy một snapshot LocalStorage rồi mặc định React tự cập nhật.

## Quy tắc UI

Sổ tay/Flashcard giới thiệu từ bằng ngữ cảnh; khi kiểm tra recall không lộ đáp án. Tab thiếu dữ liệu phải có empty/error state. Tái sử dụng token trong [CSS](<../app/src/index.css>) và component chung; giữ các class highlight/cloze/flip còn đang được sử dụng.

Dùng helper highlight/cloze đã escape và xử lý dạng từ khi phù hợp. Regex có cờ `g` có `lastIndex`; không gọi `.test()` liên tiếp rồi coi kết quả là hàm thuần. Các câu context trong SRS có helper riêng và đáp án có khai báo; xem giới hạn pool trong đặc tả SRS.
