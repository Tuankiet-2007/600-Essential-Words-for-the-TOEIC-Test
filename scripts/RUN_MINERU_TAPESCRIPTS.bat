@echo off
rem ==========================================================================
rem  OCR 34 trang Listening Tapescripts (340..373) bang MinerU
rem  (ban cai tai D:\CODE\vibecode\TOOL\mineru)
rem
rem  CACH DUNG: nhap doi vao file nay hoac chay tu cmd:
rem      scripts\RUN_MINERU_TAPESCRIPTS.bat
rem ==========================================================================
setlocal enabledelayedexpansion
cd /d "%~dp0.."

set "TOOLROOT=D:\CODE\vibecode\TOOL\mineru"

echo ============================================================
echo   OCR 34 trang Listening Tapescripts (340..373) bang MinerU
echo ============================================================
echo.

if not exist "%TOOLROOT%\.venv\Scripts\mineru-kit.exe" (
    echo [LOI] Khong thay MinerU tai: %TOOLROOT%
    echo       Chuyen sang che do Column-Aware Split + Windows OCR...
    py -3.11 scripts\extract_tapescripts_mineru.py --fallback-ocr
    exit /b !errorlevel!
)

rem --- Nap moi truong MinerU ---
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

echo Tool       : %TOOLROOT%
echo MINERU_HOME: %MINERU_HOME%
echo.

"%TOOLROOT%\.venv\Scripts\python.exe" scripts\extract_tapescripts_mineru.py --mineru-all

echo.
if errorlevel 1 (
    echo [CO LOI] Xem chi tiet phia tren.
) else (
    echo [XONG] Da xuat Markdown tapescripts. Chay tiep:
    echo        py -3.11 scripts\parse_tapescripts_full.py
)
echo.
pause
