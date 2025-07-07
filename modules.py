#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sniper-Saudi - وحدات إضافية
"""

import os
import sys
import socket
import subprocess
import threading
import time
import random
import json
import re
import logging
from datetime import datetime
from colorama import Fore, Style, init

try:
    import nmap
    import requests
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent
    import scapy.all as scapy
except ImportError:
    print("[!] بعض المكتبات المطلوبة غير متوفرة. الرجاء تثبيت المتطلبات:")
    print("    pip install -r requirements.txt")
    sys.exit(1)

# تهيئة colorama
init(autoreset=True)

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("modules.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Sniper-Saudi-Modules")

# وحدة فحص DNS
class DNSModule:
    """وحدة فحص DNS"""
    
    def __init__(self, target, output_dir):
        self.target = target
        self.output_dir = output_dir
    
    def dns_lookup(self):
        """استعلام DNS الأساسي"""
        try:
            ip = socket.gethostbyname(self.target)
            return ip
        except socket.gaierror:
            return None
    
    def reverse_dns_lookup(self, ip):
        """استعلام DNS العكسي"""
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except (socket.herror, socket.gaierror):
            return None
    
    def dns_zone_transfer(self):
        """محاولة نقل منطقة DNS"""
        output_file = os.path.join(self.output_dir, "dns_zone_transfer.txt")
        
        command = f"dig @{self.target} {self.target} AXFR"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=10
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            if "Transfer failed" in result.stdout or "connection timed out" in result.stdout:
                return False
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر نقل منطقة DNS")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء محاولة نقل منطقة DNS: {str(e)}")
            return False
    
    def run_all_checks(self):
        """تشغيل جميع فحوصات DNS"""
        results = {}
        
        logger.info(f"بدء فحوصات DNS لـ {self.target}")
        
        # استعلام DNS الأساسي
        ip = self.dns_lookup()
        if ip:
            results["dns_lookup"] = ip
            logger.info(f"استعلام DNS: {self.target} -> {ip}")
            
            # استعلام DNS العكسي
            hostname = self.reverse_dns_lookup(ip)
            if hostname:
                results["reverse_dns_lookup"] = hostname
                logger.info(f"استعلام DNS العكسي: {ip} -> {hostname}")
        
        # محاولة نقل منطقة DNS
        zone_transfer = self.dns_zone_transfer()
        results["zone_transfer_successful"] = zone_transfer
        if zone_transfer:
            logger.info(f"نجح نقل منطقة DNS لـ {self.target}")
        else:
            logger.info(f"فشل نقل منطقة DNS لـ {self.target}")
        
        # حفظ النتائج في ملف JSON
        output_file = os.path.join(self.output_dir, "dns_results.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        return results

# وحدة فحص SSL/TLS
class SSLModule:
    """وحدة فحص SSL/TLS"""
    
    def __init__(self, target, port, output_dir):
        self.target = target
        self.port = port
        self.output_dir = output_dir
    
    def check_ssl_certificate(self):
        """فحص شهادة SSL"""
        output_file = os.path.join(self.output_dir, f"ssl_certificate_{self.port}.txt")
        
        command = f"openssl s_client -connect {self.target}:{self.port} -showcerts"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=10
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر فحص شهادة SSL")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء فحص شهادة SSL: {str(e)}")
            return False
    
    def check_ssl_vulnerabilities(self):
        """فحص ثغرات SSL/TLS"""
        output_file = os.path.join(self.output_dir, f"ssl_vulnerabilities_{self.port}.txt")
        
        # فحص ثغرات SSL/TLS باستخدام nmap
        command = f"nmap --script ssl-enum-ciphers,ssl-heartbleed,ssl-poodle,ssl-ccs-injection -p {self.port} {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر فحص ثغرات SSL")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء فحص ثغرات SSL: {str(e)}")
            return False
    
    def run_all_checks(self):
        """تشغيل جميع فحوصات SSL/TLS"""
        results = {}
        
        logger.info(f"بدء فحوصات SSL/TLS لـ {self.target}:{self.port}")
        
        # فحص شهادة SSL
        cert_check = self.check_ssl_certificate()
        results["certificate_check"] = cert_check
        
        # فحص ثغرات SSL/TLS
        vuln_check = self.check_ssl_vulnerabilities()
        results["vulnerability_check"] = vuln_check
        
        # حفظ النتائج في ملف JSON
        output_file = os.path.join(self.output_dir, f"ssl_results_{self.port}.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        return results

# وحدة فحص SMB
class SMBModule:
    """وحدة فحص SMB"""
    
    def __init__(self, target, output_dir):
        self.target = target
        self.output_dir = output_dir
    
    def check_smb_vulnerabilities(self):
        """فحص ثغرات SMB"""
        output_file = os.path.join(self.output_dir, "smb_vulnerabilities.txt")
        
        # فحص ثغرات SMB باستخدام nmap
        command = f"nmap --script smb-vuln* -p 139,445 {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر فحص ثغرات SMB")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء فحص ثغرات SMB: {str(e)}")
            return False
    
    def enumerate_smb_shares(self):
        """استعراض مشاركات SMB"""
        output_file = os.path.join(self.output_dir, "smb_shares.txt")
        
        # استعراض مشاركات SMB باستخدام nmap
        command = f"nmap --script smb-enum-shares -p 139,445 {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=30
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر استعراض مشاركات SMB")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء استعراض مشاركات SMB: {str(e)}")
            return False
    
    def run_all_checks(self):
        """تشغيل جميع فحوصات SMB"""
        results = {}
        
        logger.info(f"بدء فحوصات SMB لـ {self.target}")
        
        # فحص ثغرات SMB
        vuln_check = self.check_smb_vulnerabilities()
        results["vulnerability_check"] = vuln_check
        
        # استعراض مشاركات SMB
        shares_check = self.enumerate_smb_shares()
        results["shares_enumeration"] = shares_check
        
        # حفظ النتائج في ملف JSON
        output_file = os.path.join(self.output_dir, "smb_results.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        return results

# وحدة فحص FTP
class FTPModule:
    """وحدة فحص FTP"""
    
    def __init__(self, target, output_dir):
        self.target = target
        self.output_dir = output_dir
    
    def check_anonymous_ftp(self):
        """فحص إمكانية الوصول إلى FTP كمجهول"""
        output_file = os.path.join(self.output_dir, "ftp_anonymous.txt")
        
        # فحص إمكانية الوصول إلى FTP كمجهول باستخدام nmap
        command = f"nmap --script ftp-anon -p 21 {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=30
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return "Anonymous FTP login allowed" in result.stdout
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر فحص FTP كمجهول")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء فحص FTP كمجهول: {str(e)}")
            return False
    
    def check_ftp_vulnerabilities(self):
        """فحص ثغرات FTP"""
        output_file = os.path.join(self.output_dir, "ftp_vulnerabilities.txt")
        
        # فحص ثغرات FTP باستخدام nmap
        command = f"nmap --script ftp-vuln* -p 21 {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر فحص ثغرات FTP")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء فحص ثغرات FTP: {str(e)}")
            return False
    
    def run_all_checks(self):
        """تشغيل جميع فحوصات FTP"""
        results = {}
        
        logger.info(f"بدء فحوصات FTP لـ {self.target}")
        
        # فحص إمكانية الوصول إلى FTP كمجهول
        anon_check = self.check_anonymous_ftp()
        results["anonymous_access"] = anon_check
        if anon_check:
            logger.info(f"تم اكتشاف إمكانية الوصول إلى FTP كمجهول على {self.target}")
        
        # فحص ثغرات FTP
        vuln_check = self.check_ftp_vulnerabilities()
        results["vulnerability_check"] = vuln_check
        
        # حفظ النتائج في ملف JSON
        output_file = os.path.join(self.output_dir, "ftp_results.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        return results

# وحدة فحص SSH
class SSHModule:
    """وحدة فحص SSH"""
    
    def __init__(self, target, output_dir):
        self.target = target
        self.output_dir = output_dir
    
    def check_ssh_version(self):
        """فحص إصدار SSH"""
        output_file = os.path.join(self.output_dir, "ssh_version.txt")
        
        # فحص إصدار SSH باستخدام nmap
        command = f"nmap -sV -p 22 {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=30
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر فحص إصدار SSH")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء فحص إصدار SSH: {str(e)}")
            return False
    
    def check_ssh_vulnerabilities(self):
        """فحص ثغرات SSH"""
        output_file = os.path.join(self.output_dir, "ssh_vulnerabilities.txt")
        
        # فحص ثغرات SSH باستخدام nmap
        command = f"nmap --script ssh-auth-methods,ssh-hostkey,ssh-brute,ssh2-enum-algos -p 22 {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر فحص ثغرات SSH")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء فحص ثغرات SSH: {str(e)}")
            return False
    
    def run_all_checks(self):
        """تشغيل جميع فحوصات SSH"""
        results = {}
        
        logger.info(f"بدء فحوصات SSH لـ {self.target}")
        
        # فحص إصدار SSH
        version_check = self.check_ssh_version()
        results["version_check"] = version_check
        
        # فحص ثغرات SSH
        vuln_check = self.check_ssh_vulnerabilities()
        results["vulnerability_check"] = vuln_check
        
        # حفظ النتائج في ملف JSON
        output_file = os.path.join(self.output_dir, "ssh_results.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        return results

# وحدة فحص SNMP
class SNMPModule:
    """وحدة فحص SNMP"""
    
    def __init__(self, target, output_dir):
        self.target = target
        self.output_dir = output_dir
    
    def check_snmp_community_strings(self):
        """فحص سلاسل مجتمع SNMP"""
        output_file = os.path.join(self.output_dir, "snmp_community_strings.txt")
        
        # فحص سلاسل مجتمع SNMP باستخدام nmap
        command = f"nmap --script snmp-brute -p 161 {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر فحص سلاسل مجتمع SNMP")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء فحص سلاسل مجتمع SNMP: {str(e)}")
            return False
    
    def enumerate_snmp_info(self):
        """استعراض معلومات SNMP"""
        output_file = os.path.join(self.output_dir, "snmp_info.txt")
        
        # استعراض معلومات SNMP باستخدام nmap
        command = f"nmap --script snmp-info,snmp-interfaces,snmp-netstat,snmp-processes,snmp-sysdescr -p 161 {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر استعراض معلومات SNMP")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء استعراض معلومات SNMP: {str(e)}")
            return False
    
    def run_all_checks(self):
        """تشغيل جميع فحوصات SNMP"""
        results = {}
        
        logger.info(f"بدء فحوصات SNMP لـ {self.target}")
        
        # فحص سلاسل مجتمع SNMP
        community_check = self.check_snmp_community_strings()
        results["community_check"] = community_check
        
        # استعراض معلومات SNMP
        info_check = self.enumerate_snmp_info()
        results["info_enumeration"] = info_check
        
        # حفظ النتائج في ملف JSON
        output_file = os.path.join(self.output_dir, "snmp_results.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        return results

# وحدة فحص SMTP
class SMTPModule:
    """وحدة فحص SMTP"""
    
    def __init__(self, target, output_dir):
        self.target = target
        self.output_dir = output_dir
    
    def check_smtp_commands(self):
        """فحص أوامر SMTP"""
        output_file = os.path.join(self.output_dir, "smtp_commands.txt")
        
        # فحص أوامر SMTP باستخدام nmap
        command = f"nmap --script smtp-commands -p 25,465,587 {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=30
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر فحص أوامر SMTP")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء فحص أوامر SMTP: {str(e)}")
            return False
    
    def check_smtp_vulnerabilities(self):
        """فحص ثغرات SMTP"""
        output_file = os.path.join(self.output_dir, "smtp_vulnerabilities.txt")
        
        # فحص ثغرات SMTP باستخدام nmap
        command = f"nmap --script smtp-vuln* -p 25,465,587 {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر فحص ثغرات SMTP")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء فحص ثغرات SMTP: {str(e)}")
            return False
    
    def run_all_checks(self):
        """تشغيل جميع فحوصات SMTP"""
        results = {}
        
        logger.info(f"بدء فحوصات SMTP لـ {self.target}")
        
        # فحص أوامر SMTP
        commands_check = self.check_smtp_commands()
        results["commands_check"] = commands_check
        
        # فحص ثغرات SMTP
        vuln_check = self.check_smtp_vulnerabilities()
        results["vulnerability_check"] = vuln_check
        
        # حفظ النتائج في ملف JSON
        output_file = os.path.join(self.output_dir, "smtp_results.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        return results

# وحدة فحص الشبكة
class NetworkModule:
    """وحدة فحص الشبكة"""
    
    def __init__(self, target, output_dir):
        self.target = target
        self.output_dir = output_dir
    
    def traceroute(self):
        """تتبع المسار إلى الهدف"""
        output_file = os.path.join(self.output_dir, "traceroute.txt")
        
        # تتبع المسار باستخدام nmap
        command = f"nmap --traceroute {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر تتبع المسار")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء تتبع المسار: {str(e)}")
            return False
    
    def os_detection(self):
        """اكتشاف نظام التشغيل"""
        output_file = os.path.join(self.output_dir, "os_detection.txt")
        
        # اكتشاف نظام التشغيل باستخدام nmap
        command = f"nmap -O {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر اكتشاف نظام التشغيل")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء اكتشاف نظام التشغيل: {str(e)}")
            return False
    
    def run_all_checks(self):
        """تشغيل جميع فحوصات الشبكة"""
        results = {}
        
        logger.info(f"بدء فحوصات الشبكة لـ {self.target}")
        
        # تتبع المسار
        traceroute_check = self.traceroute()
        results["traceroute"] = traceroute_check
        
        # اكتشاف نظام التشغيل
        os_check = self.os_detection()
        results["os_detection"] = os_check
        
        # حفظ النتائج في ملف JSON
        output_file = os.path.join(self.output_dir, "network_results.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        return results

# وحدة فحص تطبيقات الويب
class WebAppModule:
    """وحدة فحص تطبيقات الويب"""
    
    def __init__(self, target, port, https, output_dir):
        self.target = target
        self.port = port
        self.https = https
        self.protocol = "https" if https else "http"
        self.url = f"{self.protocol}://{self.target}:{self.port}"
        self.output_dir = output_dir
    
    def directory_brute_force(self, wordlist="/usr/share/wordlists/dirb/common.txt"):
        """اكتشاف المسارات باستخدام القوة الغاشمة"""
        output_file = os.path.join(self.output_dir, f"dirb_{self.protocol}_{self.port}.txt")
        
        # اكتشاف المسارات باستخدام gobuster
        command = f"gobuster dir -u {self.url} -w {wordlist} -o {output_file}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=300
            )
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر اكتشاف المسارات")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء اكتشاف المسارات: {str(e)}")
            return False
    
    def check_web_vulnerabilities(self):
        """فحص ثغرات تطبيق الويب"""
        output_file = os.path.join(self.output_dir, f"nikto_{self.protocol}_{self.port}.txt")
        
        # فحص ثغرات تطبيق الويب باستخدام nikto
        command = f"nikto -h {self.url} -o {output_file}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=300
            )
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر فحص ثغرات تطبيق الويب")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء فحص ثغرات تطبيق الويب: {str(e)}")
            return False
    
    def check_waf(self):
        """فحص وجود جدار حماية تطبيقات الويب (WAF)"""
        output_file = os.path.join(self.output_dir, f"wafw00f_{self.protocol}_{self.port}.txt")
        
        # فحص وجود WAF باستخدام wafw00f
        command = f"wafw00f {self.url} -o {output_file}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر فحص WAF")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء فحص WAF: {str(e)}")
            return False
    
    def run_all_checks(self):
        """تشغيل جميع فحوصات تطبيق الويب"""
        results = {}
        
        logger.info(f"بدء فحوصات تطبيق الويب لـ {self.url}")
        
        # اكتشاف المسارات
        dirb_check = self.directory_brute_force()
        results["directory_brute_force"] = dirb_check
        
        # فحص ثغرات تطبيق الويب
        nikto_check = self.check_web_vulnerabilities()
        results["vulnerability_check"] = nikto_check
        
        # فحص وجود WAF
        waf_check = self.check_waf()
        results["waf_check"] = waf_check
        
        # حفظ النتائج في ملف JSON
        output_file = os.path.join(self.output_dir, f"webapp_results_{self.protocol}_{self.port}.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        return results

# وحدة فحص قواعد البيانات
class DatabaseModule:
    """وحدة فحص قواعد البيانات"""
    
    def __init__(self, target, output_dir):
        self.target = target
        self.output_dir = output_dir
    
    def check_mysql(self):
        """فحص خدمة MySQL"""
        output_file = os.path.join(self.output_dir, "mysql_check.txt")
        
        # فحص خدمة MySQL باستخدام nmap
        command = f"nmap --script mysql-info,mysql-empty-password,mysql-brute,mysql-users,mysql-audit,mysql-enum,mysql-dump-hashes -p 3306 {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر فحص MySQL")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء فحص MySQL: {str(e)}")
            return False
    
    def check_mssql(self):
        """فحص خدمة MSSQL"""
        output_file = os.path.join(self.output_dir, "mssql_check.txt")
        
        # فحص خدمة MSSQL باستخدام nmap
        command = f"nmap --script ms-sql-info,ms-sql-empty-password,ms-sql-brute,ms-sql-config,ms-sql-dump-hashes -p 1433 {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر فحص MSSQL")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء فحص MSSQL: {str(e)}")
            return False
    
    def check_postgresql(self):
        """فحص خدمة PostgreSQL"""
        output_file = os.path.join(self.output_dir, "postgresql_check.txt")
        
        # فحص خدمة PostgreSQL باستخدام nmap
        command = f"nmap --script pgsql-brute,pgsql-databases,pgsql-empty-password -p 5432 {self.target}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"انتهت مهلة أمر فحص PostgreSQL")
            return False
        except Exception as e:
            logger.error(f"خطأ أثناء فحص PostgreSQL: {str(e)}")
            return False
    
    def run_all_checks(self):
        """تشغيل جميع فحوصات قواعد البيانات"""
        results = {}
        
        logger.info(f"بدء فحوصات قواعد البيانات لـ {self.target}")
        
        # فحص MySQL
        mysql_check = self.check_mysql()
        results["mysql_check"] = mysql_check
        
        # فحص MSSQL
        mssql_check = self.check_mssql()
        results["mssql_check"] = mssql_check
        
        # فحص PostgreSQL
        postgresql_check = self.check_postgresql()
        results["postgresql_check"] = postgresql_check
        
        # حفظ النتائج في ملف JSON
        output_file = os.path.join(self.output_dir, "database_results.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        return results

# تصدير الوحدات
__all__ = [
    'DNSModule',
    'SSLModule',
    'SMBModule',
    'FTPModule',
    'SSHModule',
    'SNMPModule',
    'SMTPModule',
    'NetworkModule',
    'WebAppModule',
    'DatabaseModule'
]