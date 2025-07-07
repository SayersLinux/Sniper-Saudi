# دليل المطور لـ Sniper-Saudi

هذا الدليل مخصص للمطورين الذين يرغبون في فهم البنية الداخلية لـ Sniper-Saudi أو المساهمة في تطويرها.

## نظرة عامة على البنية

يتكون Sniper-Saudi من عدة مكونات رئيسية:

1. **الملف الرئيسي (sniper.py)**: نقطة الدخول الرئيسية للتطبيق، يتعامل مع تحليل الأوامر وتوجيه العمليات.
2. **وحدة التكوين (config.py)**: تحتوي على جميع إعدادات التكوين والثوابت.
3. **وحدة الوظائف المساعدة (utils.py)**: توفر وظائف مساعدة عامة مثل التحقق من المدخلات وتنسيق المخرجات.
4. **وحدة الوحدات (modules.py)**: تحتوي على وحدات الفحص المختلفة مثل فحص DNS وفحص الويب وغيرها.

## تدفق التنفيذ

1. يبدأ التنفيذ من `sniper.py` حيث يتم تحليل الأوامر باستخدام `argparse`.
2. بناءً على الوضع المحدد، يتم استدعاء الوظيفة المناسبة.
3. تقوم الوظيفة بإجراء الفحص المطلوب، غالبًا باستخدام أدوات خارجية مثل Nmap.
4. يتم معالجة النتائج وتخزينها في مجلد المخرجات.

## هيكل الكود

### sniper.py

```python
# استيراد المكتبات اللازمة
import argparse
import os
import sys
import time

# استيراد الوحدات الداخلية
from config import *
from utils import *
from modules import *

# تعريف الوظائف الرئيسية لأوضاع الفحص المختلفة
def normal_scan(target, options):
    # تنفيذ فحص عادي
    pass

def stealth_scan(target, options):
    # تنفيذ فحص متخفي
    pass

# ... وظائف أخرى لأوضاع الفحص المختلفة

# وظيفة معالجة الأوامر
def parse_args():
    parser = argparse.ArgumentParser(description=HELP_DESCRIPTION)
    # إضافة الخيارات والأوامر
    return parser.parse_args()

# الوظيفة الرئيسية
def main():
    # تحليل الأوامر
    args = parse_args()
    
    # تنفيذ الوضع المناسب
    if args.mode == 'normal':
        normal_scan(args.target, args)
    elif args.mode == 'stealth':
        stealth_scan(args.target, args)
    # ... أوضاع أخرى

if __name__ == "__main__":
    main()
```

### config.py

```python
# معلومات الإصدار
VERSION = "1.0.0"
AUTHOR = "Sniper-Saudi Team"

# المجلدات الأساسية
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

# أوامر Nmap لأوضاع الفحص المختلفة
NMAP_NORMAL = "-sV -sC -O -T4 --top-ports 1000"
NMAP_STEALTH = "-sS -T2 --top-ports 1000"
# ... أوامر أخرى

# المنافذ الشائعة
COMMON_TCP_PORTS = "21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080"
COMMON_UDP_PORTS = "53,67,68,69,123,161,162,500,514,520,1900,4500,5353"

# رسائل المساعدة
HELP_DESCRIPTION = "Sniper-Saudi - أداة استطلاع وفحص أمني متعددة الوظائف"
# ... رسائل أخرى
```

### utils.py

```python
# وظائف التحقق من المدخلات
def is_valid_ip(ip):
    # التحقق من صحة عنوان IP
    pass

def is_valid_domain(domain):
    # التحقق من صحة اسم النطاق
    pass

# وظائف إدارة الملفات والمجلدات
def ensure_dir(directory):
    # التأكد من وجود المجلد
    pass

def get_output_dir(target):
    # الحصول على مجلد المخرجات للهدف
    pass

# وظائف تنسيق المخرجات
def print_banner():
    # طباعة شعار البرنامج
    pass

def print_status(message):
    # طباعة رسالة حالة
    pass

# وظائف تشغيل الأوامر الخارجية
def run_command(command):
    # تشغيل أمر خارجي
    pass

def run_nmap(target, options, output_file):
    # تشغيل Nmap
    pass
```

### modules.py

```python
# وحدة فحص DNS
class DNSScanner:
    def __init__(self, target):
        self.target = target
    
    def scan(self):
        # إجراء فحص DNS
        pass

# وحدة فحص الويب
class WebScanner:
    def __init__(self, target, port=80):
        self.target = target
        self.port = port
    
    def scan_directories(self, wordlist):
        # فحص المسارات
        pass
    
    def scan_vulnerabilities(self):
        # فحص الثغرات الأمنية
        pass

# وحدة فحص الثغرات الأمنية
class VulnerabilityScanner:
    def __init__(self, target):
        self.target = target
    
    def scan(self):
        # إجراء فحص الثغرات الأمنية
        pass
```

## إضافة وضع فحص جديد

لإضافة وضع فحص جديد، اتبع الخطوات التالية:

1. أضف ثوابت التكوين الجديدة في `config.py`:

```python
# أمر Nmap للوضع الجديد
NMAP_NEW_MODE = "-sV -sC -p 1-1000 -T3"

# رسالة المساعدة للوضع الجديد
HELP_NEW_MODE = "وصف الوضع الجديد"
```

2. أضف وظيفة الفحص الجديدة في `sniper.py`:

```python
def new_mode_scan(target, options):
    print_status(f"بدء الفحص في الوضع الجديد لـ {target}")
    
    # الحصول على مجلد المخرجات
    output_dir = get_output_dir(target)
    
    # تنفيذ الفحص
    output_file = os.path.join(output_dir, "new_mode_scan")
    run_nmap(target, NMAP_NEW_MODE, output_file)
    
    # معالجة النتائج
    # ...
    
    print_status(f"اكتمل الفحص في الوضع الجديد لـ {target}")
```

3. أضف الوضع الجديد إلى وظيفة معالجة الأوامر في `sniper.py`:

```python
def parse_args():
    parser = argparse.ArgumentParser(description=HELP_DESCRIPTION)
    # الخيارات الحالية
    # ...
    
    # إضافة الوضع الجديد
    parser.add_argument('new_mode', help=HELP_NEW_MODE)
    
    return parser.parse_args()
```

4. أضف الوضع الجديد إلى الوظيفة الرئيسية في `sniper.py`:

```python
def main():
    args = parse_args()
    
    # الأوضاع الحالية
    # ...
    
    # إضافة الوضع الجديد
    elif args.mode == 'new_mode':
        new_mode_scan(args.target, args)
```

## إضافة وحدة فحص جديدة

لإضافة وحدة فحص جديدة، اتبع الخطوات التالية:

1. أضف الوحدة الجديدة في `modules.py`:

```python
class NewScanner:
    def __init__(self, target):
        self.target = target
    
    def scan(self, options=None):
        # تنفيذ الفحص
        results = {}
        
        # ... منطق الفحص
        
        return results
```

2. استخدم الوحدة الجديدة في وظيفة الفحص المناسبة في `sniper.py`:

```python
def some_scan_mode(target, options):
    # ... الكود الحالي
    
    # استخدام الوحدة الجديدة
    scanner = NewScanner(target)
    results = scanner.scan(options)
    
    # معالجة النتائج
    # ...
```

## تخصيص المخرجات

يمكنك تخصيص تنسيق المخرجات من خلال تعديل وظائف المخرجات في `utils.py`:

```python
def save_results_as_json(results, output_file):
    # حفظ النتائج بتنسيق JSON
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

def save_results_as_xml(results, output_file):
    # حفظ النتائج بتنسيق XML
    # ...

def save_results_as_html(results, output_file):
    # حفظ النتائج بتنسيق HTML
    # ...
```

## تحسين الأداء

لتحسين أداء الأداة، يمكنك تنفيذ العمليات بشكل متوازٍ باستخدام وحدة `threading` أو `multiprocessing`:

```python
import threading

def scan_target(target, mode, options):
    # تنفيذ الفحص لهدف واحد
    # ...

def scan_multiple_targets(targets, mode, options):
    threads = []
    for target in targets:
        thread = threading.Thread(target=scan_target, args=(target, mode, options))
        threads.append(thread)
        thread.start()
    
    # انتظار اكتمال جميع الخيوط
    for thread in threads:
        thread.join()
```

## التعامل مع الأخطاء

لتحسين التعامل مع الأخطاء، يمكنك إضافة وظائف للتعامل مع الاستثناءات وتسجيل الأخطاء:

```python
import logging

# إعداد التسجيل
logging.basicConfig(
    filename=os.path.join(LOGS_DIR, 'sniper.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def safe_run_command(command):
    try:
        return run_command(command)
    except Exception as e:
        logging.error(f"خطأ في تنفيذ الأمر: {command}\n{str(e)}")
        return None
```

## الاختبار

لاختبار الأداة، يمكنك إضافة اختبارات وحدة باستخدام وحدة `unittest`:

```python
import unittest

class TestSniperSaudi(unittest.TestCase):
    def test_is_valid_ip(self):
        self.assertTrue(is_valid_ip("192.168.1.1"))
        self.assertFalse(is_valid_ip("256.256.256.256"))
    
    def test_is_valid_domain(self):
        self.assertTrue(is_valid_domain("example.com"))
        self.assertFalse(is_valid_domain("invalid domain"))
    
    # ... اختبارات أخرى

if __name__ == "__main__":
    unittest.main()
```

## التوثيق

لتوثيق الكود، استخدم تعليقات docstring بتنسيق Google أو NumPy:

```python
def run_nmap(target, options, output_file):
    """
    تشغيل Nmap مع الخيارات المحددة وحفظ المخرجات.
    
    Args:
        target (str): الهدف المراد فحصه (عنوان IP أو اسم نطاق).
        options (str): خيارات Nmap.
        output_file (str): مسار ملف المخرجات.
    
    Returns:
        bool: True إذا تم التنفيذ بنجاح، False خلاف ذلك.
    
    Raises:
        ValueError: إذا كان الهدف غير صالح.
        FileNotFoundError: إذا لم يتم العثور على Nmap.
    """
    # التحقق من صحة الهدف
    if not is_valid_ip(target) and not is_valid_domain(target):
        raise ValueError(f"هدف غير صالح: {target}")
    
    # تنفيذ الأمر
    command = f"nmap {options} {target} -oX {output_file}.xml -oN {output_file}.txt"
    return run_command(command)
```

## نصائح للمساهمين

1. **اتبع معايير الكود**: التزم بمعايير PEP 8 لكود Python.
2. **أضف تعليقات**: وثق الكود باستخدام تعليقات docstring.
3. **اختبر التغييرات**: تأكد من اختبار التغييرات قبل تقديمها.
4. **حافظ على التوافق**: تأكد من أن التغييرات متوافقة مع الأنظمة المختلفة.
5. **تجنب التبعيات غير الضرورية**: حاول تقليل التبعيات الخارجية.

## الخاتمة

هذا الدليل يوفر نظرة عامة على البنية الداخلية لـ Sniper-Saudi وكيفية المساهمة في تطويرها. إذا كانت لديك أسئلة أو اقتراحات، يرجى فتح مشكلة في مستودع GitHub أو التواصل مع فريق التطوير.

---

**ملاحظة**: هذا الدليل قابل للتغيير مع تطور الأداة. يرجى الرجوع إلى أحدث إصدار من الدليل للحصول على المعلومات الأكثر دقة.