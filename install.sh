#!/bin/bash

# Sniper-Saudi - سكربت التثبيت

echo "=== بدء تثبيت Sniper-Saudi ==="

# التحقق من وجود Python
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 غير مثبت. جاري التثبيت..."
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

# تثبيت المتطلبات من pip
echo "[*] تثبيت متطلبات Python..."
python3 -m pip install -r requirements.txt

# تثبيت الأدوات المطلوبة
echo "[*] تثبيت الأدوات المطلوبة..."
sudo apt update
sudo apt install -y nmap masscan nikto gobuster

# التحقق من تثبيت OpenVAS (اختياري)
if ! command -v openvas &> /dev/null; then
    echo "[?] OpenVAS غير مثبت. هل ترغب في تثبيته؟ (y/n)"
    read choice
    if [ "$choice" = "y" ]; then
        echo "[*] جاري تثبيت OpenVAS..."
        sudo apt install -y openvas
        sudo gvm-setup
    else
        echo "[*] تخطي تثبيت OpenVAS."
    fi
fi

# جعل السكربت الرئيسي قابل للتنفيذ
chmod +x sniper.py

# إنشاء رابط رمزي للسكربت
echo "[*] إنشاء رابط رمزي للسكربت..."
sudo ln -sf "$(pwd)/sniper.py" /usr/local/bin/sniper

echo "=== اكتمل تثبيت Sniper-Saudi ==="
echo "استخدم الأمر 'sniper -h' للحصول على المساعدة"