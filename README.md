# كيفية تشغيل أداة Sniper-Saudi
بعد تحليل أداة Sniper-Saudi، يمكنني تقديم الإرشادات التالية لتشغيلها:

## المتطلبات الأساسية
قبل تشغيل الأداة، يجب تثبيت المتطلبات التالية:

1. Python 3.6+ - الأداة تعمل على Python الإصدار 3.6 أو أحدث
2. مكتبات Python - يمكن تثبيتها باستخدام الأمر:
   ```
   pip install -r requirements.txt
   ```
3. nmap - أداة أساسية للفحص الأمني، يجب تثبيتها من الموقع الرسمي: https://nmap.org/download.html
4. أدوات إضافية (اختيارية) - مثل masscan وnikto وgobuster وOpenVAS وBurpsuite وArachni
## طريقة التثبيت
1. قم بتشغيل ملف install.bat الموجود في المجلد الرئيسي للأداة (لنظام Windows)
2. أو قم بتشغيل ملف install.sh (لنظام Linux)
## طريقة التشغيل
يمكن تشغيل الأداة بعدة أوضاع مختلفة حسب نوع الفحص المطلوب:

### الوضع العادي (Normal Mode)
```
python sniper.py [target]
```
أو باستخدام ملف الدفعة:

```
sniper.bat [target]
```
### وضع التخفي (Stealth Mode)
```
python sniper.py [target] stealth
```
### وضع FLYOVER
```
python sniper.py [target] flyover
```
### وضع AIRSTRIKE (لفحص أهداف متعددة)
```
python sniper.py /path/to/targets.txt strike
```
### وضع NUKE (لفحص شامل لأهداف متعددة)
```
python sniper.py /path/to/targets.txt nuke
```
### وضع اكتشف (Discover Mode)
```
python sniper.py [CIDR] discover
```
### وضع المنفذ (Port Mode)
```
python sniper.py [target] port [port]
```
### وضع FULLPORTONLY
```
python sniper.py [target] fullportonly
```
### وضع MASSPORTSCAN
```
python sniper.py -f /path/to/targets.txt massportscan
```
### وضع ويب (Web Mode)
```
python sniper.py [target] web
```
### وضع MASSWEB
```
python sniper.py -f /path/to/targets.txt massweb
```
### وضع WEBPORTHTTP
```
python sniper.py [target] [port] webporthttp
```
### وضع WEBPORTHTTPS
```
python sniper.py [target] [port] webporthttps
```
### وضع WEBSCAN
```
python sniper.py [target] webscan
```
### وضع MASSWEBSCAN
```
python sniper.py -f /path/to/targets.txt masswebscan
```
### وضع VULNSCAN
```
python sniper.py [target] vulnscan
```
### وضع MASSVULNSCAN
```
python sniper.py -f /path/to/targets.txt massvulnscan
```
## ملاحظات هامة
- تأكد من تثبيت nmap بشكل صحيح وإضافته إلى متغير PATH في النظام
- النتائج يتم حفظها في مجلد results داخل المجلد الرئيسي للأداة
- يتم إنشاء مجلد جديد لكل عملية فحص باسم الهدف والتاريخ والوقت
- سجلات التشغيل يتم حفظها في ملف sniper.log
## إخلاء المسؤولية
هذه الأداة مخصصة للاستخدام في اختبار الاختراق القانوني والأخلاقي فقط. استخدام هذه الأداة ضد أنظمة غير مصرح بها قد يكون غير قانوني. المستخدم مسؤول بالكامل عن أي سوء استخدام أو ضرر ناتج عن استخدام هذه الأداة


# Sniper-Saudi

أداة فحص أمني متعددة الوظائف مصممة لاختبار الاختراق واكتشاف الثغرات الأمنية.

## الميزات

- **عادي**: فحص أساسي للأهداف والمنافذ المفتوحة باستخدام فحوصات نشطة وسلبية للحصول على الأداء الأمثل.
- **التخفي**: إحصاء الأهداف الفردية بسرعة باستخدام عمليات مسح غير تدخلية لتجنب حظر WAF/IPS.
- **FLYOVER**: عمليات مسح سريعة متعددة الخيوط وعالية المستوى لأهداف متعددة.
- **AIRSTRIKE**: يُحصي المنافذ/الخدمات المفتوحة بسرعة على عدة مضيفين، ويُجري بصمة أساسية.
- **NUKE**: تدقيق كامل لمضيفين متعددين محددين في ملف نصي.
- **اكتشف**: يُحلل جميع المضيفين على شبكة فرعية/CIDR ويبدأ فحصًا شاملًا لكل مضيف.
- **المنفذ**: يفحص منفذًا محددًا بحثًا عن الثغرات الأمنية.
- **FULLPORTONLY**: فحص تفصيلي كامل للمنافذ مع حفظ النتائج في XML.
- **MASSPORTSCAN**: يقوم بتشغيل فحص "fullportonly" على أهداف متعددة.
- **ويب**: عمليات مسح تلقائية كاملة لتطبيقات الويب (المنفذ 80/tcp و443/tcp).
- **MASSWEB**: يقوم بتشغيل عمليات مسح وضع "الويب" على أهداف متعددة.
- **WEBPORTHTTP**: فحص تطبيق الويب HTTP الكامل ضد مضيف ومنفذ محددين.
- **WEBPORTHTTPS**: فحص تطبيق الويب HTTPS الكامل ضد مضيف ومنفذ محددين.
- **WEBSCAN**: فحص كامل لتطبيقات الويب HTTP و HTTPS عبر Burpsuite و Arachni.
- **MASSWEBSCAN**: يقوم بتشغيل عمليات مسح وضع "webscan" لأهداف متعددة.
- **VULNSCAN**: فحص الثغرات الأمنية في OpenVAS.
- **MASSVULNSCAN**: يقوم بتشغيل عمليات مسح وضع "vulnscan" على أهداف متعددة.

## طريقة الاستخدام

```
# الوضع العادي
./sniper.py [target]

# وضع التخفي
./sniper.py [target] stealth

# وضع FLYOVER
./sniper.py [target] flyover

# وضع AIRSTRIKE
./sniper.py /path/to/targets.txt strike

# وضع NUKE
./sniper.py /path/to/targets.txt nuke

# وضع اكتشف
./sniper.py [CIDR] discover

# وضع المنفذ
./sniper.py [target] port [port]

# وضع FULLPORTONLY
./sniper.py [target] fullportonly

# وضع MASSPORTSCAN
./sniper.py -f /path/to/targets.txt massportscan

# وضع ويب
./sniper.py [target] web

# وضع MASSWEB
./sniper.py -f /path/to/targets.txt massweb

# وضع WEBPORTHTTP
./sniper.py [target] [port] webporthttp

# وضع WEBPORTHTTPS
./sniper.py [target] [port] webporthttps

# وضع WEBSCAN
./sniper.py [target] webscan

# وضع MASSWEBSCAN
./sniper.py -f /path/to/targets.txt masswebscan

# وضع VULNSCAN
./sniper.py [target] vulnscan

# وضع MASSVULNSCAN
./sniper.py -f /path/to/targets.txt massvulnscan
```

## المتطلبات

- Python 3.6+
- nmap
- masscan
- nikto
- gobuster
- OpenVAS (اختياري للفحص الشامل للثغرات)
- Burpsuite (اختياري لفحص تطبيقات الويب)
- Arachni (اختياري لفحص تطبيقات الويب)

## التثبيت

```
# تثبيت المتطلبات
pip install -r requirements.txt

# تثبيت الأدوات الإضافية (على نظام Ubuntu/Debian)
sudo apt update
sudo apt install nmap masscan nikto
```

## إخلاء المسؤولية

هذه الأداة مخصصة للاستخدام في اختبار الاختراق القانوني والأخلاقي فقط. استخدام هذه الأداة ضد أنظمة غير مصرح بها قد يكون غير قانوني. المستخدم مسؤول بالكامل عن أي سوء استخدام أو ضرر ناتج عن استخدام هذه الأداة.

## المطور

- **المبرمج**: Sayer Linux
- **البريد الإلكتروني**: Sayerlinux@gmail.com
