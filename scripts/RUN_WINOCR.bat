@echo off
rem ============================================================
rem  OCR bo sung bang Windows OCR (khong can GPU, ~2 giay/trang)
rem
rem  OCR 3 nhom trang con thieu:
rem    1. 37 trang Listening Practice ma MinerU tra ve rong
rem       (phan Part 3/4 cau hoi trac nghiem cua bai nghe)
rem    2. 4 trang Answer Key   -> dap an toan sach
rem    3. 33 trang Tapescripts -> loi thoai that cua bai nghe
rem
rem  Chay xong hay quay lai bao agent chyt lenh convert de cap nhat web,
rem  hoac tu chay:  py -3.11 scripts\convert_available_lessons.py
rem ============================================================
chcp 65001 >nul
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\winocr_pages.ps1 %*
echo.
pause
