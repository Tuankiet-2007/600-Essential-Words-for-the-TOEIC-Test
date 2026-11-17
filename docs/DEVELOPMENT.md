# Phát triển, kiểm chứng và triển khai

[README](<../README.md>) · [Onboarding](<../ONBOARDING.md>)

## Chạy và build

Trong `app/`:

```powershell
npm ci
npm run dev
npm test
npm run lint
npm run build
```

Khuyến nghị Node 24.15+ hoặc 26+; script test dùng `--test-isolation=none` để không cần spawn worker. Không giả định mọi phiên bản Node đều hỗ trợ cùng cờ. Kiểm tra [package.json](<../app/package.json>) và lockfile trước khi đổi môi trường.

Nếu sandbox chặn config loader Vite, dùng `npm run dev:sandbox` / `npm run build:sandbox`. Hai script gọi Vite API trực tiếp; khi phát hành subpath phải kiểm base và asset URL của bản build thực tế. Khi npm không ghi được cache, chọn cache trong workspace theo môi trường hiện tại, không hard-code đường dẫn máy người khác.

## Chọn kiểm tra theo thay đổi

| Phạm vi | Kiểm tra |
|---|---|
| Scheduler/recall/persistence | `npm test` trong app |
| React/UI | Lint source, build, kiểm tra browser luồng bị đổi |
| Loader | `node scripts/verify_loader.mjs` trong app |
| Render tabs | `node scripts/verify_tabs.mjs` trong app; SSR không thay thế effects/browser |
| HTTP/assets | `node scripts/verify_runtime.mjs` trong app; đọc script để biết server cần chạy |
| Giải thích frontend | `node scripts/verify_explanations.mjs` trong app |
| Luồng tổng hợp | `node scripts/lead_e2e_check.mjs` trong app; kiểm phạm vi thực tế trước khi gọi là browser E2E |
| Highlight/cloze | `node scripts/check_helpers.mjs` từ root |
| Nội dung OCR/đáp án | Các script trong [Dữ liệu](<DATA.md>) |

[verify_onboarding.py](<../scripts/verify_onboarding.py>) hiện là bộ kiểm tra baseline đường dẫn/số liệu lịch sử; không parse nội dung Markdown và không phải trình kiểm chứng mọi câu trong onboarding mới. Không dùng kết quả đó để khẳng định tài liệu luôn khớp toàn bộ source.

Lần kiểm SRS ngày 17/11/2026: 15/15 ca test đạt, build production đạt, lint phần sửa 0 errors nhưng còn warnings. Chạy lại khi thay đổi source; không chép số PASS lịch sử làm bằng chứng mới. `npm run lint` có thể quét output sinh sẵn; dùng `oxlint src` khi cần tách warning source và bundle.

## GitHub Pages

- [Trang công khai](https://tuankiet-2007.github.io/600-Essential-Words-for-the-TOEIC-Test/)
- [Repository](https://github.com/Tuankiet-2007/600-Essential-Words-for-the-TOEIC-Test)
- [Workflow](<../.github/workflows/deploy.yml>): push `main`/`master` hoặc workflow_dispatch → npm ci → build → upload artifact → deploy Pages.

Quy trình cập nhật:

1. Xem `git status`, test/build phạm vi thay đổi, rà diff.
2. Stage đúng file; tránh `git add .` khi có probe/backup hoặc dữ liệu ngoài nhiệm vụ.
3. Commit, push nhánh được cho phép.
4. Trong GitHub Actions, kiểm run đúng commit đã thành công; push thành công chưa phải deploy thành công.
5. Kiểm trang công khai, asset JSON/audio và cold load SRS; hard refresh nếu đang giữ bundle cũ. Không xóa tiến độ để làm mới bundle.

Workflow hiện khai báo Node 20 và chưa chạy `npm test`. Với Vite 8 và cờ test hiện tại, cần nâng Node CI rồi thêm test gate; đây là [backlog](<BACKLOG.md>), không coi đã sửa chỉ bằng thay tài liệu. Không hứa thời gian deploy cố định.

## Chẩn đoán

- Trang trắng/404 assets: kiểm đường dẫn subpath, `base`, nội dung HTML và URL JS/CSS thực tế.
- Data đúng nhưng UI cũ: kiểm bản publish, cache loader/bundle và React store; LocalStorage không tự cập nhật context.
- Quota/import lỗi: xuất backup nếu đọc được, giữ lỗi hiển thị, không reset tự động. Backup có thể chứa API key.
- Git báo không đọc được credentials trong sandbox: kiểm quyền thực tế; dùng cơ chế approval của môi trường nếu cần. Không ghi token vào tài liệu hay command history.
- Nhiều server local: xác định đúng URL/process của dự án trước khi kiểm UI; không mặc định URL của công cụ phát triển là URL ứng dụng học từ.
