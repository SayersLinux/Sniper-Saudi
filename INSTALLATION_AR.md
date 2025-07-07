# دليل التثبيت والإعداد لـ Sniper-Saudi

هذا الدليل يشرح خطوات تثبيت وإعداد أداة Sniper-Saudi على أنظمة Linux و Windows.

## متطلبات النظام

### الحد الأدنى من المتطلبات

- **نظام التشغيل**: Linux (Ubuntu, Debian, Kali, CentOS) أو Windows 10/11
- **المعالج**: معالج ثنائي النواة بسرعة 2 جيجاهرتز أو أعلى
- **الذاكرة**: 2 جيجابايت من ذاكرة الوصول العشوائي (RAM)
- **مساحة القرص**: 500 ميجابايت من المساحة الحرة
- **الاتصال بالإنترنت**: مطلوب لتنزيل التبعيات وتحديثها

### المتطلبات الموصى بها

- **نظام التشغيل**: Linux (Kali Linux مفضل)
- **المعالج**: معالج رباعي النواة بسرعة 3 جيجاهرتز أو أعلى
- **الذاكرة**: 8 جيجابايت من ذاكرة الوصول العشوائي (RAM)
- **مساحة القرص**: 2 جيجابايت من المساحة الحرة
- **الاتصال بالإنترنت**: اتصال سريع ومستقر

## المتطلبات المسبقة

### البرامج المطلوبة

- **Python**: الإصدار 3.6 أو أحدث
- **pip**: مدير حزم Python
- **git**: لتنزيل المستودع (اختياري)

### الأدوات الخارجية

- **Nmap**: لفحص المنافذ واكتشاف الخدمات
- **Masscan**: لفحص المنافذ السريع على نطاق واسع
- **Nikto**: لفحص تطبيقات الويب
- **Gobuster**: لاكتشاف المسارات والملفات في تطبيقات الويب
- **OpenVAS** (اختياري): لفحص الثغرات الأمنية

## التثبيت على Linux

### الطريقة 1: باستخدام سكربت التثبيت التلقائي

1. قم بتنزيل المستودع:

```bash
git clone https://github.com/Sniper-Saudi/Sniper-Saudi.git
cd Sniper-Saudi
```

2. قم بتشغيل سكربت التثبيت:

```bash
chmod +x install.sh
./install.sh
```

سيقوم السكربت تلقائيًا بتثبيت جميع التبعيات المطلوبة وإعداد الأداة.

### الطريقة 2: التثبيت اليدوي

1. قم بتثبيت المتطلبات المسبقة:

```bash
# على توزيعات Debian/Ubuntu/Kali
sudo apt update
sudo apt install -y python3 python3-pip git nmap masscan nikto

# تثبيت Gobuster
sudo apt install -y gobuster

# أو تثبيته من المصدر
go install github.com/OJ/gobuster/v3@latest
```

2. قم بتنزيل المستودع:

```bash
git clone https://github.com/Sniper-Saudi/Sniper-Saudi.git
cd Sniper-Saudi
```

3. قم بتثبيت تبعيات Python:

```bash
pip3 install -r requirements.txt
```

4. قم بإنشاء المجلدات اللازمة:

```bash
mkdir -p results logs temp wordlists
```

5. قم بجعل الملف الرئيسي قابلاً للتنفيذ:

```bash
chmod +x sniper.py
```

6. (اختياري) قم بإنشاء رابط رمزي للأداة:

```bash
sudo ln -s $(pwd)/sniper.py /usr/local/bin/sniper
```

## التثبيت على Windows

### الطريقة 1: باستخدام سكربت التثبيت التلقائي

1. قم بتنزيل المستودع:
   - يمكنك تنزيل المستودع كملف ZIP من GitHub وفك ضغطه
   - أو استخدام git إذا كان مثبتًا:

```cmd
git clone https://github.com/Sniper-Saudi/Sniper-Saudi.git
cd Sniper-Saudi
```

2. قم بتشغيل سكربت التثبيت:

```cmd
install.bat
```

سيقوم السكربت تلقائيًا بتثبيت تبعيات Python وإعداد الأداة.

### الطريقة 2: التثبيت اليدوي

1. قم بتثبيت Python 3.6 أو أحدث من [الموقع الرسمي](https://www.python.org/downloads/windows/).
   - تأكد من تحديد خيار "Add Python to PATH" أثناء التثبيت.

2. قم بتنزيل المستودع:
   - يمكنك تنزيل المستودع كملف ZIP من GitHub وفك ضغطه
   - أو استخدام git إذا كان مثبتًا:

```cmd
git clone https://github.com/Sniper-Saudi/Sniper-Saudi.git
cd Sniper-Saudi
```

3. قم بتثبيت تبعيات Python:

```cmd
pip install -r requirements.txt
```

4. قم بإنشاء المجلدات اللازمة:

```cmd
mkdir results logs temp wordlists
```

5. قم بتثبيت Nmap من [الموقع الرسمي](https://nmap.org/download.html).
   - تأكد من تحديد خيار "Add Nmap to PATH" أثناء التثبيت.

6. (اختياري) قم بإنشاء ملف دفعي للأداة:

```cmd
echo @echo off > sniper.bat
echo python %~dp0\sniper.py %* >> sniper.bat
```

## تثبيت الأدوات الخارجية

### تثبيت Nmap

#### على Linux

```bash
sudo apt update
sudo apt install -y nmap
```

#### على Windows

قم بتنزيل وتثبيت Nmap من [الموقع الرسمي](https://nmap.org/download.html).

### تثبيت Masscan

#### على Linux

```bash
sudo apt update
sudo apt install -y masscan
```

أو من المصدر:

```bash
git clone https://github.com/robertdavidgraham/masscan.git
cd masscan
make
sudo make install
```

#### على Windows

قم بتنزيل الإصدار المناسب من [صفحة الإصدارات](https://github.com/robertdavidgraham/masscan/releases).

### تثبيت Nikto

#### على Linux

```bash
sudo apt update
sudo apt install -y nikto
```

#### على Windows

قم بتنزيل وتثبيت Nikto من [المستودع الرسمي](https://github.com/sullo/nikto).

### تثبيت Gobuster

#### على Linux

```bash
sudo apt update
sudo apt install -y gobuster
```

أو باستخدام Go:

```bash
go install github.com/OJ/gobuster/v3@latest
```

#### على Windows

قم بتثبيت Go من [الموقع الرسمي](https://golang.org/dl/)، ثم قم بتثبيت Gobuster:

```cmd
go install github.com/OJ/gobuster/v3@latest
```

### تثبيت OpenVAS (اختياري)

#### على Linux

```bash
sudo apt update
sudo apt install -y openvas
sudo gvm-setup
```

بعد التثبيت، قم بتشغيل OpenVAS:

```bash
sudo gvm-start
```

#### على Windows

OpenVAS غير متوفر بشكل رسمي لنظام Windows. يمكنك استخدام نسخة مستضافة أو تشغيله في آلة افتراضية تعمل بنظام Linux.

## التحقق من التثبيت

بعد اكتمال التثبيت، يمكنك التحقق من أن الأداة تعمل بشكل صحيح عن طريق تشغيل الأمر التالي:

### على Linux

```bash
./sniper.py -h
```

أو إذا قمت بإنشاء رابط رمزي:

```bash
sniper -h
```

### على Windows

```cmd
python sniper.py -h
```

أو إذا قمت بإنشاء ملف دفعي:

```cmd
sniper.bat -h
```

يجب أن ترى رسالة المساعدة التي تعرض الخيارات المتاحة.

## إعداد البيئة

### تكوين المجلدات

تستخدم الأداة المجلدات التالية:

- **results**: لتخزين نتائج الفحص
- **logs**: لتخزين سجلات الأداة
- **temp**: للملفات المؤقتة
- **wordlists**: لقواميس الكلمات المستخدمة في الفحص

يتم إنشاء هذه المجلدات تلقائيًا أثناء التثبيت، ولكن يمكنك تخصيصها عن طريق تعديل ملف `config.py`.

### تكوين قواميس الكلمات

تستخدم الأداة قواميس الكلمات التالية:

- **common.txt**: لاكتشاف المسارات الشائعة في تطبيقات الويب
- **subdomains-top1000.txt**: لاكتشاف النطاقات الفرعية
- **rockyou-50.txt**: لاختبار كلمات المرور الشائعة

يتم توفير هذه القواميس مع الأداة، ولكن يمكنك استبدالها بقواميس مخصصة عن طريق وضع الملفات في مجلد `wordlists`.

### تخصيص الإعدادات

يمكنك تخصيص سلوك الأداة عن طريق تعديل ملف `config.py`، الذي يحتوي على إعدادات مثل:

- أوامر Nmap الافتراضية لكل وضع
- المنافذ الشائعة للفحص
- المهل الزمنية
- مسارات قواميس الكلمات

## استكشاف الأخطاء وإصلاحها

### مشاكل شائعة

#### الأداة لا تعمل

- تأكد من تثبيت Python 3.6 أو أحدث
- تأكد من تثبيت جميع التبعيات المطلوبة
- تحقق من وجود جميع الملفات المطلوبة
- تحقق من صلاحيات الملفات (على Linux)

#### فشل فحص Nmap

- تأكد من تثبيت Nmap بشكل صحيح
- تحقق من امتلاك الصلاحيات المناسبة (قد تحتاج إلى صلاحيات الجذر على Linux)
- تحقق من إمكانية الوصول إلى الهدف

#### فشل فحص الويب

- تأكد من تثبيت Nikto و Gobuster بشكل صحيح
- تحقق من إمكانية الوصول إلى خدمة الويب على الهدف

### سجلات الأداة

إذا واجهت مشاكل، يمكنك التحقق من سجلات الأداة في مجلد `logs`.

### الحصول على المساعدة

إذا كنت بحاجة إلى مساعدة إضافية، يمكنك:

- فتح مشكلة في مستودع GitHub
- التواصل مع فريق التطوير عبر البريد الإلكتروني

## تحديث الأداة

### على Linux

```bash
cd Sniper-Saudi
git pull
pip3 install -r requirements.txt
```

### على Windows

```cmd
cd Sniper-Saudi
git pull
pip install -r requirements.txt
```

## إلغاء التثبيت

### على Linux

```bash
# إذا قمت بإنشاء رابط رمزي
sudo rm /usr/local/bin/sniper

# حذف المجلد
rm -rf Sniper-Saudi
```

### على Windows

```cmd
# حذف المجلد
rd /s /q Sniper-Saudi
```

---

**ملاحظة**: تأكد دائمًا من استخدام هذه الأداة فقط على أنظمة مصرح لك باختبارها. استخدام هذه الأداة ضد أنظمة غير مصرح بها قد يكون غير قانوني ويمكن أن يؤدي إلى عواقب قانونية خطيرة.