#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sniper-Saudi - وظائف مساعدة
"""

import os
import sys
import socket
import ipaddress
import re
import json
import logging
import random
import string
from datetime import datetime
from colorama import Fore, Style, init

# تهيئة colorama
init(autoreset=True)

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("utils.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Sniper-Saudi-Utils")

# التحقق من صحة عنوان IP
def is_valid_ip(ip):
    """التحقق من صحة عنوان IP"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# التحقق من صحة اسم النطاق
def is_valid_domain(domain):
    """التحقق من صحة اسم النطاق"""
    domain_pattern = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    )
    return bool(domain_pattern.match(domain))

# التحقق من صحة عنوان CIDR
def is_valid_cidr(cidr):
    """التحقق من صحة عنوان CIDR"""
    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False

# التحقق من صحة المنفذ
def is_valid_port(port):
    """التحقق من صحة المنفذ"""
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except ValueError:
        return False

# التحقق من وجود ملف
def file_exists(file_path):
    """التحقق من وجود ملف"""
    return os.path.isfile(file_path)

# التحقق من وجود مجلد
def dir_exists(dir_path):
    """التحقق من وجود مجلد"""
    return os.path.isdir(dir_path)

# إنشاء مجلد إذا لم يكن موجودًا
def create_dir_if_not_exists(dir_path):
    """إنشاء مجلد إذا لم يكن موجودًا"""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        return True
    return False

# الحصول على الوقت الحالي بتنسيق معين
def get_timestamp(format_str="%Y%m%d_%H%M%S"):
    """الحصول على الوقت الحالي بتنسيق معين"""
    return datetime.now().strftime(format_str)

# توليد سلسلة عشوائية
def generate_random_string(length=10):
    """توليد سلسلة عشوائية"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# تحويل عنوان IP إلى اسم مضيف
def ip_to_hostname(ip):
    """تحويل عنوان IP إلى اسم مضيف"""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except (socket.herror, socket.gaierror):
        return None

# تحويل اسم المضيف إلى عنوان IP
def hostname_to_ip(hostname):
    """تحويل اسم المضيف إلى عنوان IP"""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

# تحويل قناع الشبكة إلى CIDR
def netmask_to_cidr(netmask):
    """تحويل قناع الشبكة إلى CIDR"""
    return sum(bin(int(x)).count('1') for x in netmask.split('.'))

# تحويل CIDR إلى قناع الشبكة
def cidr_to_netmask(cidr):
    """تحويل CIDR إلى قناع الشبكة"""
    cidr = int(cidr)
    mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
    return ".