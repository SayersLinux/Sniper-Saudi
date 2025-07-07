#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sniper-Saudi - Multi-function Security Scanning Tool
"""

import os
import sys
import argparse
import socket
import subprocess
import threading
import time
import ipaddress
import random
import json
import re
import logging
import queue
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from colorama import Fore, Style, init
from tqdm import tqdm

# Import configuration file
try:
    from config import *
except ImportError:
    print("[!] Configuration file not found. Please make sure config.py exists")
    sys.exit(1)

try:
    import nmap
    import requests
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent
except ImportError:
    print("[!] Some required libraries are not available. Please install requirements:")
    print("    pip install -r requirements.txt")
    sys.exit(1)

# Initialize colorama
init(autoreset=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Sniper-Saudi")

# Create global thread pool
thread_pool = ThreadPoolExecutor(max_workers=MAX_THREADS)

# Banner
def print_banner():
    banner = f'''
{Fore.GREEN}  ███████╗███╗   ██╗██╗██████╗ ███████╗██████╗       ███████╗ █████╗ ██╗   ██╗██████╗ ██╗
  ██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗      ██╔════╝██╔══██╗██║   ██║██╔══██╗██║
  ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝█████╗███████╗███████║██║   ██║██║  ██║██║
  ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗╚════╝╚════██║██╔══██║██║   ██║██║  ██║██║
  ███████║██║ ╚████║██║██║     ███████╗██║  ██║      ███████║██║  ██║╚██████╔╝██████╔╝██║
  ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝      ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝{Style.RESET_ALL}
                                                                                  
{Fore.YELLOW}  Multi-function Security Scanning Tool{Style.RESET_ALL}
  
  Use -h for help
'''
    print(banner)

# Validate target
def validate_target(target):
    """Validate target (IP or domain name)"""
    try:
        # Check if it's an IP address
        ipaddress.ip_address(target)
        return True
    except ValueError:
        # Check if it's a domain name
        try:
            socket.gethostbyname(target)
            return True
        except socket.gaierror:
            return False

# Create output directory
def create_output_dir(target):
    """Create directory for results"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_dir = os.path.join(RESULTS_DIR, f"{target}_{timestamp}")
    
    if not os.path.exists(RESULTS_DIR):
        os.mkdir(RESULTS_DIR)
    
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    
    return target_dir

# Execute command and return result
def run_command(command, output_file=None):
    """Execute command and return result"""
    try:
        if output_file:
            with open(output_file, 'w') as f:
                process = subprocess.Popen(
                    command,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    shell=True
                )
        else:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                universal_newlines=True
            )
        
        stdout, stderr = process.communicate()
        
        if process.returncode != 0 and stderr:
            logger.error(f"Error executing command: {stderr}")
            return None
        
        return stdout if not output_file else True
    
    except Exception as e:
        logger.error(f"Exception while executing command: {str(e)}")
        return None

# Scan ports using nmap
def scan_ports(target, output_dir, mode="normal"):
    """Scan ports using nmap"""
    logger.info(f"Starting port scan for {target} in {mode} mode")
    
    nm = nmap.PortScanner()
    output_file = os.path.join(output_dir, "nmap_scan.xml")
    
    try:
        # Use settings from config.py
        if mode == "normal":
            # Basic scan for common ports
            nm.scan(target, DEFAULT_PORTS, NMAP_NORMAL_ARGS)
        elif mode == "stealth":
            # Stealth scan
            nm.scan(target, WEB_PORTS, NMAP_STEALTH_ARGS)
        elif mode == "fullportonly":
            # Full port scan
            nm.scan(target, FULL_PORTS, NMAP_FULL_ARGS)
        elif mode == "web":
            # Web ports scan
            nm.scan(target, WEB_PORTS, NMAP_WEB_ARGS)
        else:
            # Default scan
            nm.scan(target, COMMON_PORTS, '-sV')
        
        # Save results to XML file
        with open(output_file, 'w') as f:
            f.write(nm.get_nmap_last_output())
        
        return nm
    
    except Exception as e:
        logger.error(f"Error during port scan: {str(e)}")
        return None

# Vulnerability scanning
def vulnerability_scan(target, output_dir):
    """Scan for vulnerabilities using nmap scripts"""
    logger.info(f"Starting vulnerability scan for {target}")
    
    output_file = os.path.join(output_dir, "vuln_scan.txt")
    
    # Use nmap with vulnerability scripts from config file
    command = f"nmap {NMAP_VULN_ARGS} {target} -oN {output_file}"
    
    return run_command(command, output_file)

# Web application scanning
def web_scan(target, output_dir, port=None, https=False):
    """Scan web applications"""
    protocol = "https" if https else "http"
    target_port = f":{port}" if port else ""
    url = f"{protocol}://{target}{target_port}"
    
    logger.info(f"Starting web application scan: {url}")
    
    output_file = os.path.join(output_dir, f"web_scan_{protocol}_{port if port else 'default'}.txt")
    
    try:
        # Create random User-Agent
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        
        # فحص الصفحة الرئيسية باستخدام الإعدادات من ملف config.py
        response = requests.get(url, headers=headers, verify=VERIFY_SSL, timeout=HTTP_TIMEOUT)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n")
            f.write(f"Status Code: {response.status_code}\n")
            f.write(f"Server: {response.headers.get('Server', 'Unknown')}\n")
            f.write(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}\n\n")
            
            # استخراج العناوين والروابط
            if 'text/html' in response.headers.get('Content-Type', ''):
                soup = BeautifulSoup(response.text, 'html.parser')
                
                f.write("=== العناوين ===\n")
                for heading in soup.find_all(['h1', 'h2', 'h3']):
                    f.write(f"{heading.name}: {heading.text.strip()}\n")
                
                f.write("\n=== الروابط ===\n")
                for link in soup.find_all('a', href=True):
                    f.write(f"{link['href']}\n")
        
        # تشغيل nikto لفحص الثغرات الأمنية في تطبيق الويب
        nikto_output = os.path.join(output_dir, f"nikto_{protocol}_{port if port else 'default'}.txt")
        nikto_command = f"nikto -h {url} -o {nikto_output}"
        run_command(nikto_command)
        
        # تشغيل gobuster لاكتشاف المسارات
        gobuster_output = os.path.join(output_dir, f"gobuster_{protocol}_{port if port else 'default'}.txt")
        gobuster_command = f"gobuster dir -u {url} -w /usr/share/wordlists/dirb/common.txt -o {gobuster_output}"
        run_command(gobuster_command)
        
        return True
    
    except requests.exceptions.RequestException as e:
        logger.error(f"خطأ أثناء فحص تطبيق الويب: {str(e)}")
        with open(output_file, 'w') as f:
            f.write(f"Error: {str(e)}\n")
        return False

# فحص شبكة فرعية
def discover_hosts(cidr, output_dir):
    """اكتشاف المضيفين في شبكة فرعية"""
    logger.info(f"بدء اكتشاف المضيفين في {cidr}")
    
    output_file = os.path.join(output_dir, "discovered_hosts.txt")
    
    try:
        # استخدام nmap لاكتشاف المضيفين
        command = f"nmap -sn {cidr} -oG - | grep 'Up' | cut -d ' ' -f 2"
        result = run_command(command)
        
        if result:
            hosts = result.strip().split('\n')
            
            with open(output_file, 'w') as f:
                for host in hosts:
                    if host.strip():
                        f.write(f"{host.strip()}\n")
            
            logger.info(f"تم اكتشاف {len(hosts)} مضيف في {cidr}")
            return hosts
        
        return []
    
    except Exception as e:
        logger.error(f"خطأ أثناء اكتشاف المضيفين: {str(e)}")
        return []

# وضع FLYOVER - فحص سريع متعدد الخيوط
def flyover_scan(target, output_dir):
    """فحص سريع متعدد الخيوط"""
    logger.info(f"بدء فحص FLYOVER للهدف: {target}")
    
    try:
        # إنشاء مجلد للنتائج
        flyover_dir = os.path.join(output_dir, "flyover_results")
        if not os.path.exists(flyover_dir):
            os.mkdir(flyover_dir)
        
        target_dir = os.path.join(flyover_dir, target.replace('.', '_'))
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
        
        # إنشاء قائمة بالمهام
        tasks = [
            ("port_scan", lambda: scan_ports(target, target_dir, "normal")),
            ("vuln_scan", lambda: vulnerability_scan(target, target_dir))
        ]
        
        # تنفيذ المهام بالتوازي
        futures = {}
        for task_name, task_func in tasks:
            futures[task_name] = thread_pool.submit(task_func)
        
        # فحص تطبيقات الويب إذا كانت منافذ الويب مفتوحة
        def scan_web_ports():
            web_results = []
            nm = nmap.PortScanner()
            nm.scan(target, WEB_PORTS, '-sS --max-retries 1')
            
            if target in nm.all_hosts():
                for proto in nm[target].all_protocols():
                    ports = sorted(nm[target][proto].keys())
                    for port in ports:
                        if nm[target][proto][port]['state'] == 'open':
                            if port in [80, 8080]:
                                web_results.append((port, False))
                            elif port in [443, 8443]:
                                web_results.append((port, True))
            return web_results
        
        # إضافة مهمة فحص منافذ الويب
        futures["web_ports"] = thread_pool.submit(scan_web_ports)
        
        # إنشاء تقرير مفصل
        def create_detailed_report():
            # تنفيذ فحص سريع للمنافذ الشائعة
            nm = nmap.PortScanner()
            nm.scan(target, '21-25,80,443,8080,8443,3389,5900', '-T4 --max-retries 1 --host-timeout 30s')
            
            output_file = os.path.join(target_dir, "flyover_summary.txt")
            
            with open(output_file, 'w') as f:
                f.write(f"=== FLYOVER Scan for {target} ===\n\n")
                
                if target in nm.all_hosts():
                    f.write(f"Host: {target} ({nm[target].hostname() if 'hostname' in nm[target] else 'Unknown'})\n")
                    f.write(f"State: {nm[target].state()}\n\n")
                    
                    for proto in nm[target].all_protocols():
                        f.write(f"Protocol: {proto}\n")
                        
                        ports = sorted(nm[target][proto].keys())
                        for port in ports:
                            service = nm[target][proto][port]
                            f.write(f"Port: {port}\tState: {service['state']}\t")
                            f.write(f"Service: {service['name']}\tVersion: {service.get('product', 'Unknown')} {service.get('version', '')}\n")
                        
                        f.write("\n")
            return output_file
        
        # إضافة مهمة إنشاء التقرير
        futures["report"] = thread_pool.submit(create_detailed_report)
        
        # انتظار اكتمال المهام الأساسية
        for task_name, future in futures.items():
            try:
                if task_name != "web_ports":
                    result = future.result(timeout=THREAD_TIMEOUT)
                    logger.debug(f"اكتملت مهمة {task_name} بنتيجة: {result is not None}")
            except Exception as e:
                logger.error(f"خطأ في مهمة {task_name}: {str(e)}")
        
        # معالجة نتائج فحص منافذ الويب وبدء فحص الويب
        try:
            web_ports = futures["web_ports"].result(timeout=THREAD_TIMEOUT)
            web_futures = []
            
            # إذا وجدت منافذ ويب مفتوحة، قم بفحصها بالتوازي
            if web_ports:
                for port, is_https in web_ports:
                    web_future = thread_pool.submit(web_scan, target, target_dir, port, https=is_https)
                    web_futures.append(web_future)
                
                # انتظار اكتمال فحوصات الويب
                for future in web_futures:
                    try:
                        future.result(timeout=THREAD_TIMEOUT)
                    except Exception as e:
                        logger.error(f"خطأ أثناء فحص الويب: {str(e)}")
        except Exception as e:
            logger.error(f"خطأ أثناء فحص منافذ الويب: {str(e)}")
        
        # انتظار اكتمال التقرير
        try:
            report_file = futures["report"].result(timeout=THREAD_TIMEOUT)
            logger.info(f"تم إنشاء تقرير الفحص في: {report_file}")
        except Exception as e:
            logger.error(f"خطأ أثناء إنشاء التقرير: {str(e)}")
        
        logger.info("اكتمل فحص FLYOVER")
        return True
    
    except Exception as e:
        logger.error(f"خطأ أثناء فحص FLYOVER: {str(e)}")
        return False

# وضع AIRSTRIKE - فحص سريع لعدة مضيفين
def airstrike_scan(targets_file, output_dir):
    """فحص سريع لعدة مضيفين"""
    logger.info(f"بدء فحص AIRSTRIKE باستخدام قائمة الأهداف: {targets_file}")
    
    try:
        # قراءة قائمة الأهداف
        with open(targets_file, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
        
        if not targets:
            logger.error("ملف الأهداف فارغ")
            return False
        
        logger.info(f"تم العثور على {len(targets)} هدف في الملف")
        
        # إنشاء مجلد للنتائج
        airstrike_dir = os.path.join(output_dir, "airstrike_results")
        if not os.path.exists(airstrike_dir):
            os.mkdir(airstrike_dir)
        
        # وظيفة لفحص هدف واحد
        def scan_single_target(target):
            if validate_target(target):
                target_dir = os.path.join(airstrike_dir, target.replace('.', '_'))
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)
                return scan_ports(target, target_dir)
            return None
        
        # استخدام مجمع الخيوط لفحص الأهداف بالتوازي
        futures = []
        valid_targets = [t for t in targets if validate_target(t)]
        
        # إنشاء شريط تقدم
        with tqdm(total=len(valid_targets), desc="AIRSTRIKE Scan Progress") as pbar:
            # تقديم المهام إلى مجمع الخيوط
            for target in valid_targets:
                future = thread_pool.submit(scan_single_target, target)
                future.add_done_callback(lambda p: pbar.update(1))
                futures.append(future)
            
            # انتظار اكتمال جميع المهام
            for future in futures:
                future.result(timeout=THREAD_TIMEOUT)
        
        logger.info("اكتمل فحص AIRSTRIKE")
        return True
    
    except Exception as e:
        logger.error(f"خطأ أثناء فحص AIRSTRIKE: {str(e)}")
        return False

# وضع NUKE - فحص شامل لعدة مضيفين
def nuke_scan(targets_file, output_dir):
    """فحص شامل لعدة مضيفين"""
    logger.info(f"بدء فحص NUKE باستخدام قائمة الأهداف: {targets_file}")
    
    try:
        # قراءة قائمة الأهداف
        with open(targets_file, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
        
        if not targets:
            logger.error("ملف الأهداف فارغ")
            return False
        
        logger.info(f"تم العثور على {len(targets)} هدف في الملف")
        
        # إنشاء مجلد للنتائج
        nuke_dir = os.path.join(output_dir, "nuke_results")
        if not os.path.exists(nuke_dir):
            os.mkdir(nuke_dir)
        
        # وظيفة لفحص هدف واحد بشكل شامل
        def nuke_scan_target(target):
            if validate_target(target):
                target_dir = os.path.join(nuke_dir, target.replace('.', '_'))
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)
                
                scan_results = {
                    "ports": False,
                    "vulns": False,
                    "web": False,
                    "web_ports": []
                }
                
                # فحص المنافذ
                port_scan_result = scan_ports(target, target_dir, "fullportonly")
                scan_results["ports"] = (port_scan_result is not None)
                
                # فحص الثغرات الأمنية
                vuln_scan_result = vulnerability_scan(target, target_dir)
                scan_results["vulns"] = (vuln_scan_result is not None)
                
                # فحص تطبيقات الويب إذا كانت منافذ الويب مفتوحة
                nm = nmap.PortScanner()
                nm.scan(target, WEB_PORTS, '-sS --max-retries 1')
                
                if target in nm.all_hosts():
                    for proto in nm[target].all_protocols():
                        ports = sorted(nm[target][proto].keys())
                        for port in ports:
                            if nm[target][proto][port]['state'] == 'open':
                                if port in [80, 8080]:
                                    web_scan(target, target_dir, port, https=False)
                                    scan_results["web"] = True
                                    scan_results["web_ports"].append(f"http:{port}")
                                elif port in [443, 8443]:
                                    web_scan(target, target_dir, port, https=True)
                                    scan_results["web"] = True
                                    scan_results["web_ports"].append(f"https:{port}")
                
                return target, scan_results
            return target, None
        
        # استخدام مجمع الخيوط لفحص الأهداف بالتوازي
        futures = []
        results = {}
        valid_targets = [t for t in targets if validate_target(t)]
        
        # إنشاء شريط تقدم
        with tqdm(total=len(valid_targets), desc="NUKE Scan Progress") as pbar:
            # تقديم المهام إلى مجمع الخيوط
            for target in valid_targets:
                future = thread_pool.submit(nuke_scan_target, target)
                future.add_done_callback(lambda p: pbar.update(1))
                futures.append(future)
            
            # جمع النتائج
            for future in futures:
                try:
                    target, scan_results = future.result(timeout=THREAD_TIMEOUT * 3)  # زيادة المهلة للفحص الشامل
                    if scan_results:
                        results[target] = scan_results
                except Exception as e:
                    logger.error(f"خطأ أثناء فحص NUKE للهدف: {str(e)}")
        
        # طباعة ملخص النتائج
        successful_scans = len(results)
        web_targets = sum(1 for r in results.values() if r["web"])
        logger.info(f"تم فحص {successful_scans} هدف بنجاح، منها {web_targets} يحتوي على خدمات ويب")
        
        logger.info("اكتمل فحص NUKE")
        return True
    
    except Exception as e:
        logger.error(f"خطأ أثناء فحص NUKE: {str(e)}")
        return False

# وضع MASSPORTSCAN - فحص المنافذ لعدة مضيفين
def mass_port_scan(targets_file, output_dir):
    """فحص المنافذ لعدة مضيفين"""
    logger.info(f"بدء فحص MASSPORTSCAN باستخدام قائمة الأهداف: {targets_file}")
    
    try:
        # قراءة قائمة الأهداف
        with open(targets_file, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
        
        if not targets:
            logger.error("ملف الأهداف فارغ")
            return False
        
        logger.info(f"تم العثور على {len(targets)} هدف في الملف")
        
        # إنشاء مجلد للنتائج
        massportscan_dir = os.path.join(output_dir, "massportscan_results")
        if not os.path.exists(massportscan_dir):
            os.mkdir(massportscan_dir)
        
        # إنشاء ملف مؤقت للأهداف
        temp_targets = os.path.join(massportscan_dir, "targets.txt")
        with open(temp_targets, 'w') as f:
            for target in targets:
                if validate_target(target):
                    f.write(f"{target}\n")
        
        # استخدام masscan لفحص المنافذ بسرعة
        output_file = os.path.join(massportscan_dir, "masscan_results.txt")
        command = f"masscan -iL {temp_targets} -p1-65535 --rate={MASSCAN_RATE} -oL {output_file}"
        
        run_command(command)
        
        # تحليل نتائج masscan وإجراء فحص nmap للمنافذ المفتوحة
        try:
            with open(output_file, 'r') as f:
                masscan_results = f.readlines()
            
            # استخراج المنافذ المفتوحة لكل هدف
            open_ports = {}
            for line in masscan_results:
                if line.startswith('#'):
                    continue
                
                parts = line.strip().split()
                if len(parts) >= 4 and parts[0] == "open":
                    ip = parts[3]
                    port = parts[2]
                    
                    if ip not in open_ports:
                        open_ports[ip] = []
                    
                    open_ports[ip].append(port)
            
            # وظيفة لفحص هدف واحد باستخدام nmap
            def scan_target_ports(ip, ports):
                target_dir = os.path.join(massportscan_dir, ip.replace('.', '_'))
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)
                
                ports_str = ','.join(ports)
                nm = nmap.PortScanner()
                nm.scan(ip, ports_str, '-sV')
                
                # حفظ نتائج nmap
                nmap_output = os.path.join(target_dir, "nmap_scan.xml")
                with open(nmap_output, 'w') as f:
                    f.write(nm.get_nmap_last_output())
                
                return ip, len(ports)
            
            # استخدام مجمع الخيوط لفحص الأهداف بالتوازي
            futures = []
            results = {}
            
            # إنشاء شريط تقدم
            with tqdm(total=len(open_ports), desc="MASSPORTSCAN Nmap Progress") as pbar:
                # تقديم المهام إلى مجمع الخيوط
                for ip, ports in open_ports.items():
                    future = thread_pool.submit(scan_target_ports, ip, ports)
                    future.add_done_callback(lambda p: pbar.update(1))
                    futures.append(future)
                
                # جمع النتائج
                for future in futures:
                    try:
                        ip, port_count = future.result(timeout=THREAD_TIMEOUT)
                        results[ip] = port_count
                    except Exception as e:
                        logger.error(f"خطأ أثناء فحص المنافذ: {str(e)}")
            
            # طباعة ملخص النتائج
            logger.info(f"تم فحص {len(results)} هدف بنجاح")
        
        except Exception as e:
            logger.error(f"خطأ أثناء تحليل نتائج masscan: {str(e)}")
        
        logger.info("اكتمل فحص MASSPORTSCAN")
        return True
    
    except Exception as e:
        logger.error(f"خطأ أثناء فحص MASSPORTSCAN: {str(e)}")
        return False

# وضع MASSWEB - فحص تطبيقات الويب لعدة مضيفين
def mass_web_scan(targets_file, output_dir):
    """فحص تطبيقات الويب لعدة مضيفين"""
    logger.info(f"بدء فحص MASSWEB باستخدام قائمة الأهداف: {targets_file}")
    
    try:
        # قراءة قائمة الأهداف
        with open(targets_file, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
        
        if not targets:
            logger.error("ملف الأهداف فارغ")
            return False
        
        logger.info(f"تم العثور على {len(targets)} هدف في الملف")
        
        # إنشاء مجلد للنتائج
        massweb_dir = os.path.join(output_dir, "massweb_results")
        if not os.path.exists(massweb_dir):
            os.mkdir(massweb_dir)
        
        # وظيفة لفحص منافذ الويب لهدف واحد
        def scan_web_target_ports(target):
            if not validate_target(target):
                return target, [], None
            
            target_dir = os.path.join(massweb_dir, target.replace('.', '_'))
            if not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)
            
            # فحص منافذ الويب
            web_ports = []
            try:
                nm = nmap.PortScanner()
                nm.scan(target, WEB_PORTS, '-sS --max-retries 1')
                
                if target in nm.all_hosts():
                    for proto in nm[target].all_protocols():
                        ports = sorted(nm[target][proto].keys())
                        for port in ports:
                            if nm[target][proto][port]['state'] == 'open':
                                if port in [80, 8080]:
                                    web_ports.append((port, False))
                                elif port in [443, 8443]:
                                    web_ports.append((port, True))
            except Exception as e:
                logger.error(f"خطأ أثناء فحص منافذ الويب للهدف {target}: {str(e)}")
            
            return target, web_ports, target_dir
        
        # وظيفة لفحص منفذ ويب واحد
        def scan_single_web_port(target, port, https, target_dir):
            try:
                result = web_scan(target, target_dir, port, https=https)
                return target, port, https, result
            except Exception as e:
                logger.error(f"خطأ أثناء فحص الويب للهدف {target} على المنفذ {port}: {str(e)}")
                return target, port, https, False
        
        # استخدام مجمع الخيوط لفحص منافذ الويب لجميع الأهداف
        port_scan_futures = []
        valid_targets = [t for t in targets if validate_target(t)]
        
        with tqdm(total=len(valid_targets), desc="MASSWEB Port Scan Progress") as pbar:
            # تقديم مهام فحص المنافذ
            for target in valid_targets:
                future = thread_pool.submit(scan_web_target_ports, target)
                future.add_done_callback(lambda p: pbar.update(1))
                port_scan_futures.append(future)
        
        # جمع نتائج فحص المنافذ
        web_scan_tasks = []
        target_results = {}
        
        for future in port_scan_futures:
            try:
                target, web_ports, target_dir = future.result(timeout=THREAD_TIMEOUT)
                if web_ports:
                    target_results[target] = []
                    for port, https in web_ports:
                        web_scan_tasks.append((target, port, https, target_dir))
            except Exception as e:
                logger.error(f"خطأ أثناء معالجة نتائج فحص المنافذ: {str(e)}")
        
        # فحص تطبيقات الويب على المنافذ المفتوحة
        if web_scan_tasks:
            web_scan_futures = []
            with tqdm(total=len(web_scan_tasks), desc="MASSWEB Application Scan Progress") as pbar:
                # تقديم مهام فحص تطبيقات الويب
                for target, port, https, target_dir in web_scan_tasks:
                    future = thread_pool.submit(scan_single_web_port, target, port, https, target_dir)
                    future.add_done_callback(lambda p: pbar.update(1))
                    web_scan_futures.append(future)
                
                # جمع نتائج فحص تطبيقات الويب
                for future in web_scan_futures:
                    try:
                        target, port, https, result = future.result(timeout=THREAD_TIMEOUT * 2)  # زيادة المهلة لفحص الويب
                        protocol = "https" if https else "http"
                        if target in target_results:
                            target_results[target].append(f"{protocol}:{port}")
                    except Exception as e:
                        logger.error(f"خطأ أثناء انتظار اكتمال فحص الويب: {str(e)}")
        else:
            logger.info("لم يتم العثور على منافذ ويب مفتوحة في أي من الأهداف")
        
        # طباعة ملخص النتائج
        web_targets_count = sum(1 for ports in target_results.values() if ports)
        logger.info(f"تم العثور على {web_targets_count} هدف يحتوي على خدمات ويب")
        
        logger.info("اكتمل فحص MASSWEB")
        return True
    
    except Exception as e:
        logger.error(f"خطأ أثناء فحص MASSWEB: {str(e)}")
        return False

# وضع MASSWEBSCAN - فحص شامل لتطبيقات الويب لعدة مضيفين
def mass_webscan(targets_file, output_dir):
    """فحص شامل لتطبيقات الويب لعدة مضيفين"""
    logger.info(f"بدء فحص MASSWEBSCAN باستخدام قائمة الأهداف: {targets_file}")
    
    try:
        # قراءة قائمة الأهداف
        with open(targets_file, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
        
        if not targets:
            logger.error("ملف الأهداف فارغ")
            return False
        
        logger.info(f"تم العثور على {len(targets)} هدف في الملف")
        
        # إنشاء مجلد للنتائج
        masswebscan_dir = os.path.join(output_dir, "masswebscan_results")
        if not os.path.exists(masswebscan_dir):
            os.mkdir(masswebscan_dir)
        
        # وظيفة لفحص منافذ الويب لهدف واحد
        def scan_target_web_ports(target):
            if not validate_target(target):
                return target, []
            
            target_dir = os.path.join(masswebscan_dir, target.replace('.', '_'))
            if not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)
            
            # فحص منافذ الويب
            web_ports = []
            try:
                nm = nmap.PortScanner()
                nm.scan(target, WEB_PORTS, '-sS --max-retries 1')
                
                if target in nm.all_hosts():
                    for proto in nm[target].all_protocols():
                        ports = sorted(nm[target][proto].keys())
                        for port in ports:
                            if nm[target][proto][port]['state'] == 'open':
                                if port in [80, 8080]:
                                    web_ports.append((port, False))
                                elif port in [443, 8443]:
                                    web_ports.append((port, True))
            except Exception as e:
                logger.error(f"خطأ أثناء فحص منافذ الويب للهدف {target}: {str(e)}")
            
            return target, web_ports, target_dir
        
        # وظيفة لفحص منفذ ويب واحد بشكل شامل
        def scan_web_port_advanced(target, port, https, target_dir):
            try:
                # فحص الويب الأساسي
                web_scan(target, target_dir, port, https=https)
                
                # تشغيل أوامر إضافية لفحص تطبيق الويب
                protocol = "https" if https else "http"
                url = f"{protocol}://{target}:{port}"
                results = {}
                
                # فحص Nikto متقدم
                nikto_output = os.path.join(target_dir, f"nikto_advanced_{port}.txt")
                nikto_command = f"nikto -h {url} -Tuning x6 -o {nikto_output}"
                nikto_result = run_command(nikto_command)
                results["nikto"] = (nikto_result is not None)
                
                # فحص Gobuster متقدم
                gobuster_output = os.path.join(target_dir, f"gobuster_advanced_{port}.txt")
                gobuster_command = f"gobuster dir -u {url} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o {gobuster_output}"
                gobuster_result = run_command(gobuster_command)
                results["gobuster"] = (gobuster_result is not None)
                
                # فحص شهادة SSL إذا كان HTTPS
                if https:
                    ssl_output = os.path.join(target_dir, f"ssl_check_{port}.txt")
                    ssl_command = f"openssl s_client -connect {target}:{port} -showcerts > {ssl_output}"
                    ssl_result = run_command(ssl_command)
                    results["ssl"] = (ssl_result is not None)
                
                return target, port, https, results
            except Exception as e:
                logger.error(f"خطأ أثناء الفحص الشامل للويب للهدف {target} على المنفذ {port}: {str(e)}")
                return target, port, https, {}
        
        # استخدام مجمع الخيوط لفحص منافذ الويب لجميع الأهداف
        port_scan_futures = []
        valid_targets = [t for t in targets if validate_target(t)]
        
        with tqdm(total=len(valid_targets), desc="MASSWEBSCAN Port Scan Progress") as pbar:
            # تقديم مهام فحص المنافذ
            for target in valid_targets:
                future = thread_pool.submit(scan_target_web_ports, target)
                future.add_done_callback(lambda p: pbar.update(1))
                port_scan_futures.append(future)
        
        # جمع نتائج فحص المنافذ
        web_scan_tasks = []
        target_results = {}
        
        for future in port_scan_futures:
            try:
                target, web_ports, target_dir = future.result(timeout=THREAD_TIMEOUT)
                if web_ports:
                    target_results[target] = []
                    for port, https in web_ports:
                        web_scan_tasks.append((target, port, https, target_dir))
            except Exception as e:
                logger.error(f"خطأ أثناء معالجة نتائج فحص المنافذ: {str(e)}")
        
        # فحص تطبيقات الويب على المنافذ المفتوحة
        if web_scan_tasks:
            web_scan_futures = []
            with tqdm(total=len(web_scan_tasks), desc="MASSWEBSCAN Advanced Scan Progress") as pbar:
                # تقديم مهام فحص تطبيقات الويب
                for target, port, https, target_dir in web_scan_tasks:
                    future = thread_pool.submit(scan_web_port_advanced, target, port, https, target_dir)
                    future.add_done_callback(lambda p: pbar.update(1))
                    web_scan_futures.append(future)
                
                # جمع نتائج فحص تطبيقات الويب
                for future in web_scan_futures:
                    try:
                        target, port, https, results = future.result(timeout=THREAD_TIMEOUT * 3)  # زيادة المهلة للفحص الشامل
                        protocol = "https" if https else "http"
                        if target in target_results:
                            target_results[target].append(f"{protocol}:{port}")
                    except Exception as e:
                        logger.error(f"خطأ أثناء انتظار اكتمال فحص الويب الشامل: {str(e)}")
        else:
            logger.info("لم يتم العثور على منافذ ويب مفتوحة في أي من الأهداف")
        
        # طباعة ملخص النتائج
        web_targets_count = sum(1 for ports in target_results.values() if ports)
        logger.info(f"تم العثور على {web_targets_count} هدف يحتوي على خدمات ويب")
        
        logger.info("اكتمل فحص MASSWEBSCAN")
        return True
    
    except Exception as e:
        logger.error(f"خطأ أثناء فحص MASSWEBSCAN: {str(e)}")
        return False

# MASSVULNSCAN Mode - Vulnerability scanning for multiple hosts
def mass_vuln_scan(targets_file, output_dir):
    """Vulnerability scanning for multiple hosts"""
    logger.info(f"Starting MASSVULNSCAN using targets list: {targets_file}")
    
    try:
        # Read targets list
        with open(targets_file, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
        
        if not targets:
            logger.error("Targets file is empty")
            return False
        
        logger.info(f"Found {len(targets)} targets in the file")
        
        # Create results directory
        massvulnscan_dir = os.path.join(output_dir, "massvulnscan_results")
        if not os.path.exists(massvulnscan_dir):
            os.mkdir(massvulnscan_dir)
        
        # Function to scan a single target
        def scan_target_vulns(target):
            if validate_target(target):
                target_dir = os.path.join(massvulnscan_dir, target.replace('.', '_'))
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)
                
                # Vulnerability scanning
                result = vulnerability_scan(target, target_dir)
                return target, (result is not None)
            return target, False
        
        # Use thread pool to scan targets in parallel
        futures = []
        results = {}
        valid_targets = [t for t in targets if validate_target(t)]
        
        # Create progress bar
        with tqdm(total=len(valid_targets), desc="MASSVULNSCAN Progress") as pbar:
            # Submit tasks to thread pool
            for target in valid_targets:
                future = thread_pool.submit(scan_target_vulns, target)
                future.add_done_callback(lambda p: pbar.update(1))
                futures.append(future)
            
            # Collect results
            for future in futures:
                try:
                    target, success = future.result(timeout=THREAD_TIMEOUT)
                    results[target] = success
                except Exception as e:
                    logger.error(f"Error during vulnerability scan: {str(e)}")
        
        # Print results summary
        successful_scans = sum(1 for success in results.values() if success)
        logger.info(f"Successfully scanned {successful_scans} targets out of {len(valid_targets)}")
        
        logger.info("MASSVULNSCAN completed")
        return True
    
    except Exception as e:
        logger.error(f"Error during MASSVULNSCAN: {str(e)}")
        return False

# Main function
def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Sniper-Saudi - Multi-functional Security Scanning Tool")
    parser.add_argument("target", help="Target (IP, domain name, or targets file)")
    parser.add_argument("mode", nargs="?", default="normal", help="Scan mode (normal, stealth, flyover, strike, nuke, discover, port, fullportonly, web, webscan, vulnscan)")
    parser.add_argument("-p", "--port", help="Specific port to scan (used with port mode)")
    parser.add_argument("-f", "--file", help="File containing list of targets")
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Verify mode and target
    target = args.target
    mode = args.mode.lower()
    
    # Create results directory
    output_dir = create_output_dir(target.split('/')[-1] if '/' in target else target)
    
    # Execute selected mode
    if mode == "normal":
        if validate_target(target):
            scan_ports(target, output_dir, "normal")
            print(f"{Fore.GREEN}[+] Normal scan completed. Results saved in: {output_dir}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Invalid target: {target}{Style.RESET_ALL}")
    
    elif mode == "stealth":
        if validate_target(target):
            scan_ports(target, output_dir, "stealth")
            print(f"{Fore.GREEN}[+] Stealth scan completed. Results saved in: {output_dir}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Invalid target: {target}{Style.RESET_ALL}")
    
    elif mode == "flyover":
        if validate_target(target):
            flyover_scan(target, output_dir)
            print(f"{Fore.GREEN}[+] FLYOVER scan completed. Results saved in: {output_dir}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Invalid target: {target}{Style.RESET_ALL}")
    
    elif mode == "strike":
        if os.path.isfile(target):
            airstrike_scan(target, output_dir)
            print(f"{Fore.GREEN}[+] AIRSTRIKE scan completed. Results saved in: {output_dir}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Targets file not found: {target}{Style.RESET_ALL}")
    
    elif mode == "nuke":
        if os.path.isfile(target):
            nuke_scan(target, output_dir)
            print(f"{Fore.GREEN}[+] NUKE scan completed. Results saved in: {output_dir}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Targets file not found: {target}{Style.RESET_ALL}")
    
    elif mode == "discover":
        try:
            ipaddress.ip_network(target)
            hosts = discover_hosts(target, output_dir)
            
            if hosts:
                print(f"{Fore.GREEN}[+] Discovered {len(hosts)} hosts in {target}. Results saved in: {output_dir}{Style.RESET_ALL}")
                
                # Ask user if they want to scan discovered hosts
                choice = input(f"{Fore.YELLOW}[?] Do you want to scan the discovered hosts? (y/n): {Style.RESET_ALL}").lower()
                
                if choice == 'y':
                    # Create temporary file for discovered hosts
                    temp_hosts_file = os.path.join(output_dir, "discovered_hosts_for_scan.txt")
                    with open(temp_hosts_file, 'w') as f:
                        for host in hosts:
                            f.write(f"{host}\n")
                    
                    # Scan discovered hosts
                    nuke_scan(temp_hosts_file, output_dir)
                    print(f"{Fore.GREEN}[+] Discovered hosts scan completed. Results saved in: {output_dir}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] No hosts discovered in {target}{Style.RESET_ALL}")
        
        except ValueError:
            print(f"{Fore.RED}[!] Invalid CIDR format: {target}{Style.RESET_ALL}")
    
    elif mode == "port":
        if validate_target(target):
            if args.port:
                port = args.port
                print(f"{Fore.YELLOW}[*] Scanning port {port} on {target}...{Style.RESET_ALL}")
                
                # Scan specific port
                nm = nmap.PortScanner()
                nm.scan(target, port, '-sV --script=vuln')
                
                output_file = os.path.join(output_dir, f"port_{port}_scan.txt")
                
                with open(output_file, 'w') as f:
                    f.write(f"=== Port Scan for {target}:{port} ===\n\n")
                    
                    if target in nm.all_hosts():
                        for proto in nm[target].all_protocols():
                            ports = sorted(nm[target][proto].keys())
                            for p in ports:
                                if int(p) == int(port):
                                    service = nm[target][proto][p]
                                    f.write(f"Port: {p}\tState: {service['state']}\t")
                                    f.write(f"Service: {service['name']}\tVersion: {service.get('product', 'Unknown')} {service.get('version', '')}\n")
                                    
                                    # Print vulnerability information if found
                                    if 'script' in service:
                                        f.write("\nVulnerability Information:\n")
                                        for script_name, script_output in service['script'].items():
                                            f.write(f"{script_name}:\n{script_output}\n\n")
                
                print(f"{Fore.GREEN}[+] Port scan completed. Results saved in: {output_file}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] Port must be specified using -p{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Invalid target: {target}{Style.RESET_ALL}")
    
    elif mode == "fullportonly":
        if validate_target(target):
            scan_ports(target, output_dir, "fullportonly")
            print(f"{Fore.GREEN}[+] Full port scan completed. Results saved in: {output_dir}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Invalid target: {target}{Style.RESET_ALL}")
    
    elif mode == "massportscan":
        if args.file and os.path.isfile(args.file):
            mass_port_scan(args.file, output_dir)
            print(f"{Fore.GREEN}[+] اكتمل فحص MASSPORTSCAN. النتائج محفوظة في: {output_dir}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] يجب تحديد ملف الأهداف باستخدام -f{Style.RESET_ALL}")
    
    elif mode == "web":
        if validate_target(target):
            scan_ports(target, output_dir, "web")
            web_scan(target, output_dir, port=80, https=False)
            web_scan(target, output_dir, port=443, https=True)
            print(f"{Fore.GREEN}[+] اكتمل فحص الويب. النتائج محفوظة في: {output_dir}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] هدف غير صالح: {target}{Style.RESET_ALL}")
    
    elif mode == "massweb":
        if args.file and os.path.isfile(args.file):
            mass_web_scan(args.file, output_dir)
            print(f"{Fore.GREEN}[+] اكتمل فحص MASSWEB. النتائج محفوظة في: {output_dir}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] يجب تحديد ملف الأهداف باستخدام -f{Style.RESET_ALL}")
    
    elif mode == "webporthttp":
        if validate_target(target) and args.port:
            web_scan(target, output_dir, port=args.port, https=False)
            print(f"{Fore.GREEN}[+] اكتمل فحص WEBPORTHTTP. النتائج محفوظة في: {output_dir}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] هدف غير صالح أو لم يتم تحديد المنفذ{Style.RESET_ALL}")
    
    elif mode == "webporthttps":
        if validate_target(target) and args.port:
            web_scan(target, output_dir, port=args.port, https=True)
            print(f"{Fore.GREEN}[+] اكتمل فحص WEBPORTHTTPS. النتائج محفوظة في: {output_dir}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] هدف غير صالح أو لم يتم تحديد المنفذ{Style.RESET_ALL}")
    
    elif mode == "webscan":
        if validate_target(target):
            web_scan(target, output_dir, port=80, https=False)
            web_scan(target, output_dir, port=443, https=True)
            print(f"{Fore.GREEN}[+] اكتمل فحص WEBSCAN. النتائج محفوظة في: {output_dir}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] هدف غير صالح: {target}{Style.RESET_ALL}")
    
    elif mode == "masswebscan":
        if args.file and os.path.isfile(args.file):
            mass_webscan(args.file, output_dir)
            print(f"{Fore.GREEN}[+] اكتمل فحص MASSWEBSCAN. النتائج محفوظة في: {output_dir}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] يجب تحديد ملف الأهداف باستخدام -f{Style.RESET_ALL}")
    
    elif mode == "vulnscan":
        if validate_target(target):
            vulnerability_scan(target, output_dir)
            print(f"{Fore.GREEN}[+] اكتمل فحص الثغرات الأمنية. النتائج محفوظة في: {output_dir}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] هدف غير صالح: {target}{Style.RESET_ALL}")
    
    elif mode == "massvulnscan":
        if args.file and os.path.isfile(args.file):
            mass_vuln_scan(args.file, output_dir)
            print(f"{Fore.GREEN}[+] اكتمل فحص MASSVULNSCAN. النتائج محفوظة في: {output_dir}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] يجب تحديد ملف الأهداف باستخدام -f{Style.RESET_ALL}")
    
    else:
        print(f"{Fore.RED}[!] وضع غير صالح: {mode}{Style.RESET_ALL}")
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] تم إلغاء الفحص بواسطة المستخدم{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[!] حدث خطأ: {str(e)}{Style.RESET_ALL}")