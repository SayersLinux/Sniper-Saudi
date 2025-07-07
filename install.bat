@echo off
REM Sniper-Saudi - سكربت التثبيت لنظام Windows

echo === بدء تثبيت Sniper-Saudi ===

REM التحقق من وجود Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python غير مثبت. الرجاء تثبيت Python 3.6 أو أحدث من https://www.python.org/downloads/
    echo [!] تأكد من تفعيل خيار "Add Python to PATH" أثناء التثبيت
    pause
    exit /b 1
)

REM تثبيت المتطلبات من pip
echo [*] تثبيت متطلبات Python...
pip install -r requirements.txt

REM إنشاء مجلد للنتائج
if not exist results mkdir results

REM تثبيت Nmap لنظام Windows (اختياري)
echo [?] هل ترغب في تثبيت Nmap لنظام Windows؟ (Y/N)
set /p choice="الاختيار: "
if /i "%choice%"=="Y" (
    echo [*] الرجاء تنزيل وتثبيت Nmap من https://nmap.org/download.html
    start https://nmap.org/download.html
)

REM إنشاء اختصار للسكربت
echo @echo off > sniper.bat
echo python "%~dp0sniper.py" %%* >> sniper.bat

echo === اكتمل تثبيت Sniper-Saudi ===
echo استخدم الأمر 'sniper.bat -h' للحصول على المساعدة

pause