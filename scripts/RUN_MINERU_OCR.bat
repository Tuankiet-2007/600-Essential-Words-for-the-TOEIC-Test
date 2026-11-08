@echo off
rem ==========================================================================
rem  OCR 49 bai con lai bang MinerU (ban cai tai D:\CODE\vibecode\TOOL\mineru)
rem
rem  CACH DUNG: nhap doi vao file nay.
rem  Chay thu 1 bai truoc:  keo tha -> khong, hay mo cmd roi go:
rem      RUN_MINERU_OCR.bat --only 2
rem
rem  File nay tu nap moi truong MinerU cua ban, nen KHONG can Admin.
rem  Phai chay o day (ngoai sandbox) vi MinerU dung named pipe ma sandbox chan.
rem ==========================================================================
setlocal enabledelayedexpansion
cd /d "%~dp0.."

set "TOOLROOT=D:\CODE\vibecode\TOOL\mineru"

echo ============================================================
echo   OCR sach TOEIC 600 bang MinerU
echo ============================================================
echo.

if not exist "%TOOLROOT%\.venv\Scripts\mineru-kit.exe" (
    echo [LOI] Khong thay MinerU tai: %TOOLROOT%
    echo       Sua bien TOOLROOT trong file nay neu ban cai cho khac.
    echo.
    pause
    exit /b 1
)

if not exist "extracted_data\lesson_page_scans" (
    echo [LOI] Chua co anh scan. Chay truoc:
    echo       python scripts\extract_pdf_assets.py
    echo.
    pause
    exit /b 1
)

rem --- Nap moi truong MinerU (giong cac file .cmd cua ban cai) --------------
set "MINERU_HOME=%TOOLROOT%\home"
set "MINERU_MODEL_VLM_ENGINE=llama-cpp"
set "UV_CACHE_DIR=%TOOLROOT%\.cache\uv"
set "UV_PYTHON_INSTALL_DIR=%TOOLROOT%\.python"
set "HF_HOME=%TOOLROOT%\.cache\huggingface"
set "MODELSCOPE_CACHE=%TOOLROOT%\.cache\modelscope"
set "TMP=%TOOLROOT%\.tmp"
set "TEMP=%TOOLROOT%\.tmp"
set "VIRTUAL_ENV=%TOOLROOT%\.venv"
set "PATH=%TOOLROOT%\.venv\Scripts;%PATH%"

echo Tool      : %TOOLROOT%
echo MINERU_HOME: %MINERU_HOME%
echo.
echo Bat dau. Lan dau se cham hon (nap model vao GPU).
echo.

"%TOOLROOT%\.venv\Scripts\python.exe" scripts\run_mineru_local.py %*

echo.
if errorlevel 1 (
    echo [CO BAI LOI] Xem chi tiet phia tren.
) else (
    echo [XONG] Mo web app va bam "Quet lai" o sidebar.
)
echo.
pause
