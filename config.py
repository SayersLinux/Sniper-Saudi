#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sniper-Saudi - Configuration File
"""

import os

# General Settings
RESULTS_DIR = "results"  # Main results directory
LOG_FILE = "sniper.log"  # Log file
DEBUG_MODE = False  # Debug mode

# Thread Settings
MAX_THREADS = 10  # Maximum number of concurrent threads
THREAD_TIMEOUT = 300  # Thread timeout in seconds (5 minutes)
THREAD_RETRY_COUNT = 2  # Number of retry attempts when a task fails
THREAD_RETRY_DELAY = 5  # Delay between retry attempts in seconds

# Scan Settings
DEFAULT_SCAN_MODE = "normal"  # Default scan mode
DEFAULT_PORTS = "21-25,80,443,8080,8443"  # Default ports for scanning
WEB_PORTS = "80,443,8080,8443"  # Default web ports
FULL_PORTS = "1-65535"  # All ports
COMMON_PORTS = "1-1000"  # Common ports
MAIL_PORTS = "25,110,143,465,587,993,995"  # Email ports
DATABASE_PORTS = "1433,1521,3306,5432,6379,27017,27018,27019"  # Database ports

# Nmap Settings
NMAP_NORMAL_ARGS = "-sV -sS --script=default"  # Normal Nmap arguments
NMAP_STEALTH_ARGS = "-sS -T2 --max-retries 1 --host-timeout 15m"  # Stealth Nmap arguments
NMAP_FULL_ARGS = "-sS -T4 --max-retries 1"  # Full scan Nmap arguments
NMAP_WEB_ARGS = "-sV -sS --script=http-*"  # Web scan Nmap arguments
NMAP_VULN_ARGS = "-sV --script=vuln"  # Vulnerability scan Nmap arguments
NMAP_TIMEOUT = 300  # Nmap timeout in seconds
NMAP_MAX_RETRIES = 2  # Number of retry attempts for Nmap

# Masscan Settings
MASSCAN_RATE = "10000"  # Scan rate for Masscan
MASSCAN_WAIT = 10  # Wait time after Masscan completion in seconds

# Gobuster Settings
GOBUSTER_WORDLIST = os.path.join("wordlists", "rockyou-50.txt")  # Wordlist for Gobuster
GOBUSTER_THREADS = 50  # Number of threads for Gobuster
GOBUSTER_EXTENSIONS = "php,html,js,txt"  # File extensions to search for
GOBUSTER_TIMEOUT = 10  # Gobuster timeout in seconds

# Nikto Settings
NIKTO_TUNING = "x6"  # Nikto tuning settings
NIKTO_TIMEOUT = 300  # Nikto timeout in seconds

# HTTP Settings
HTTP_TIMEOUT = 10  # HTTP request timeout in seconds
VERIFY_SSL = False  # Verify SSL certificates
HTTP_MAX_RETRIES = 3  # Number of retry attempts for HTTP requests
HTTP_RETRY_DELAY = 2  # Delay between retry attempts in seconds
USER_AGENTS = [  # List of user agents to rotate
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

# Report Settings
REPORT_FORMATS = ["txt", "xml", "html", "json"]  # Supported report formats
REPORT_INCLUDE_SCREENSHOTS = False  # Include screenshots in reports
REPORT_INCLUDE_RAW_DATA = True  # Include raw data in reports

# Notification Settings
ENABLE_NOTIFICATIONS = False  # Enable notifications
NOTIFICATION_EMAIL = ""  # Email for notifications
SMTP_SERVER = "smtp.gmail.com"  # SMTP server
SMTP_PORT = 587  # SMTP port
SMTP_USERNAME = ""  # SMTP username
SMTP_PASSWORD = ""  # SMTP password

# Security Settings
SAFE_MODE = True  # Safe mode (restricts some dangerous scans)
MAX_PACKET_RATE = 5000  # Maximum packet rate per second
BLACKLIST_TARGETS = []  # List of blacklisted targets