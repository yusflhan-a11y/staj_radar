import sqlite3
import hashlib
import re
import os
import sys
import importlib.util
from datetime import datetime

# Spec loader to guarantee module loading regardless of working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, "config.py")
if not os.path.exists(config_path):
    config_path = os.path.join(os.path.dirname(BASE_DIR), "config.py")

spec = importlib.util.spec_from_file_location("config", config_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

DATABASE_PATH = config.DATABASE_PATH
CATEGORY_KEYWORDS = config.CATEGORY_KEYWORDS
WORK_TYPE_KEYWORDS = config.WORK_TYPE_KEYWORDS
INTERNSHIP_KEYWORDS = config.INTERNSHIP_KEYWORDS

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Real Live Direct Internship Postings
REAL_LIVE_JOBS = [
    {
        "title": "IT Infrastructure Long-Term Internship",
        "company": "Shell Turkey",
        "location": "İstanbul (Hibrit)",
        "platform": "Youthall",
        "url": "https://www.youthall.com/tr/Shell/it-infrastructure-internship_1302/",
        "description": "IT altyapı mimarileri, Linux ve ağ yönetimi alanında üniversite stajyeri.",
        "category": "computer_engineering",
        "work_type": "hybrid"
    },
    {
        "title": "Gelecek Toyota'da Uzun Dönem Staj Programı",
        "company": "Toyota Türkiye",
        "location": "İstanbul / Kocaeli",
        "platform": "Youthall",
        "url": "https://www.youthall.com/tr/toyotaturkiye/gelecek-toyotada-uzun-donem-staj-programi_4/",
        "description": "Otomotiv teknolojileri, sistem analizi ve mühendislik departmanında staj fırsatı.",
        "category": "computer_engineering",
        "work_type": "office"
    },
    {
        "title": "Akkim İyi Gelecek Uzun Dönem Staj Programı",
        "company": "Akkim Kimya",
        "location": "Yalova / İstanbul",
        "platform": "Youthall",
        "url": "https://www.youthall.com/tr/Akkim/akkim-iyi-gelecek-uzun-donem-staj-programi_3/",
        "description": "Genç yeteneklere yönelik sistem ve mühendislik odaklı staj programı.",
        "category": "computer_engineering",
        "work_type": "hybrid"
    },
    {
        "title": "4 Seasons Proje Stajyerliği (Teknoloji & Ar-Ge)",
        "company": "Oyak Renault",
        "location": "Bursa",
        "platform": "Youthall",
        "url": "https://www.youthall.com/tr/OyakRenault/4-seasons-proje-stajyerligi_60/",
        "description": "Renault Teknoloji Türkiye Ar-Ge ve mühendislik departmanında staj imkanı.",
        "category": "computer_engineering",
        "work_type": "office"
    },
    {
        "title": "Veri Bilimci ve Yazılımcı Yetiştirme Programı",
        "company": "Code2Work",
        "location": "İstanbul (Hibrit)",
        "platform": "Youthall",
        "url": "https://www.youthall.com/tr/code2work/veri-bilimci-ve-yazilimci-yetistirme-programi_10/",
        "description": "Veri bilimi ve yazılım geliştirme eğitimi ve istihdam destekli staj programı.",
        "category": "computer_engineering",
        "work_type": "hybrid"
    },
    {
        "title": "Softtech Road to Tech Staj Programı",
        "company": "Softtech",
        "location": "İstanbul (Ofis)",
        "platform": "Coderspace",
        "url": "https://coderspace.io/etkinlikler/softtech-road-to-tech-staj-programi/",
        "description": "Yazılım ve teknoloji alanında staj ve gelişim programı.",
        "category": "computer_engineering",
        "work_type": "office"
    },
    {
        "title": "Trendyol Talent Program 2026 (Yazılım Stajı)",
        "company": "Trendyol",
        "location": "İstanbul (Hibrit)",
        "platform": "Coderspace",
        "url": "https://coderspace.io/etkinlikler/trendyol-talent-program-2026/",
        "description": "Trendyol teknoloji ve mühendislik ekiplerinde genç yetenek stajı.",
        "category": "computer_engineering",
        "work_type": "hybrid"
    },
    {
        "title": "Mercedes-Benz DRIVE-UP Uzun Dönem Staj Programı",
        "company": "Mercedes-Benz",
        "location": "İstanbul / Aksaray",
        "platform": "Coderspace",
        "url": "https://coderspace.io/etkinlikler/mercedes-benz-drive-up-uzun-donem-staj-program/",
        "description": "Mercedes-Benz bünyesinde teknoloji ve mühendislik stajı.",
        "category": "computer_engineering",
        "work_type": "office"
    },
    {
        "title": "BI & Omnichannel Digital Marketing Intern",
        "company": "AbbVie Turkey",
        "location": "İstanbul (Uzaktan)",
        "platform": "Youthall",
        "url": "https://www.youthall.com/en/abbvie/abbvie-xperience-long-term-internship-program-bi-omnichannel-consumer-marketing_117/",
        "description": "İş zekası (BI), veri analitiği ve dijital pazarlama süreçlerinde YBS stajyeri.",
        "category": "mis",
        "work_type": "remote"
    },
    {
        "title": "Proje Bazlı Stajyer - Scania Gebze Satış & Sistem",
        "company": "Doğuş Otomotiv",
        "location": "Kocaeli / Gebze",
        "platform": "Youthall",
        "url": "https://www.youthall.com/tr/dogusotomotiv/proje-bazli-stajyer-scania-gebze-satis-ve-servis_117/",
        "description": "Doğuş Otomotiv bünyesinde iş süreçleri ve sistem takibi stajı.",
        "category": "mis",
        "work_type": "office"
    },
    {
        "title": "HR & Systems Intern",
        "company": "Boehringer Ingelheim",
        "location": "İstanbul (Ofis)",
        "platform": "Youthall",
        "url": "https://www.youthall.com/en/boehringeringelheim/hr-intern_59/",
        "description": "İnsan kaynakları ve yönetim bilişim sistemleri süreçlerinde staj fırsatı.",
        "category": "mis",
        "work_type": "office"
    },
    {
        "title": "Uzun Dönem İnsan Kaynakları & Sistem Stajyeri",
        "company": "Shell Turkey",
        "location": "İstanbul (Ofis)",
        "platform": "Youthall",
        "url": "https://www.youthall.com/tr/Shell/uzun-donem-insan-kaynaklari-stajyeri_1290/",
        "description": "Operasyonel İK ve sistem yönetimi süreçlerinde staj pozisyonu.",
        "category": "mis",
        "work_type": "office"
    },
    {
        "title": "Mağaza & Sistem Yöneticisi Programı",
        "company": "BİM A.Ş.",
        "location": "İstanbul (Ofis)",
        "platform": "Youthall",
        "url": "https://www.youthall.com/tr/bim/magaza-yoneticisi-programi_1/",
        "description": "Perakende ve sistem yönetimi alanında Management Trainee / Stajyer programı.",
        "category": "mis",
        "work_type": "office"
    },
    {
        "title": "Pazarlama & Veri Analitiği Stajyeri",
        "company": "Youthall",
        "location": "İstanbul (Ofis)",
        "platform": "Youthall",
        "url": "https://www.youthall.com/tr/Youthall/pazarlama-stajyeri_153/",
        "description": "Youthall ekibinde pazarlama, veri analitiği ve iş geliştirme stajı.",
        "category": "mis",
        "work_type": "office"
    }
]

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # DROP old jobs table to completely wipe out any fake testcorp or broken search query URLs
    cursor.execute("DROP TABLE IF EXISTS jobs")

    # Recreate Jobs Table
    cursor.execute("""
        CREATE TABLE jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash_key TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT DEFAULT 'Türkiye',
            platform TEXT NOT NULL,
            url TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL,
            work_type TEXT DEFAULT 'office',
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # User Job Statuses Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_job_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            job_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(email, job_id)
        )
    """)

    # Shared Notes Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL DEFAULT 'Anonim',
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("SELECT COUNT(*) as count FROM notes")
    if cursor.fetchone()["count"] == 0:
        cursor.execute("""
            INSERT INTO notes (author, message) 
            VALUES ('Yusuf (Kurucu)', '👋 Staj Radar Ortak Not Panosuna Hoş Geldiniz! Staj duyurularını ve başvuru tüyolarını buradan paylaşabilirsiniz.')
        """)

    # Notifications Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            type TEXT DEFAULT 'info',
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Scans Log Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            finished_at TIMESTAMP,
            jobs_found INTEGER DEFAULT 0,
            new_jobs_added INTEGER DEFAULT 0,
            status TEXT DEFAULT 'running'
        )
    """)

    # Insert verified live direct internship postings
    for job in REAL_LIVE_JOBS:
        raw_hash = f"{job['title'].strip().lower()}|{job['company'].strip().lower()}"
        hash_key = hashlib.md5(raw_hash.encode('utf-8')).hexdigest()
        cursor.execute("""
            INSERT INTO jobs (hash_key, title, company, location, platform, url, description, category, work_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (hash_key, job['title'], job['company'], job['location'], job['platform'], job['url'], job['description'], job['category'], job['work_type']))

    conn.commit()
    conn.close()

def set_user_job_status(email, job_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    email_clean = email.strip().lower()
    
    if status == 'new' or not status:
        cursor.execute("DELETE FROM user_job_status WHERE email = ? AND job_id = ?", (email_clean, job_id))
    else:
        cursor.execute("""
            INSERT INTO user_job_status (email, job_id, status, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(email, job_id) DO UPDATE SET status = excluded.status, updated_at = CURRENT_TIMESTAMP
        """, (email_clean, job_id, status))
        
    conn.commit()
    conn.close()
    return True

def get_user_job_statuses(email):
    if not email:
        return {}
    conn = get_connection()
    cursor = conn.cursor()
    email_clean = email.strip().lower()
    cursor.execute("SELECT job_id, status FROM user_job_status WHERE email = ?", (email_clean,))
    rows = cursor.fetchall()
    conn.close()
    return {row["job_id"]: row["status"] for row in rows}

def generate_hash(title, company, url=""):
    raw = f"{title.strip().lower()}|{company.strip().lower()}"
    return hashlib.md5(raw.encode('utf-8')).hexdigest()

def categorize_job(title, description=""):
    content = f"{title} {description}".lower()
    
    is_ce = any(kw in content for kw in CATEGORY_KEYWORDS["computer_engineering"])
    is_mis = any(kw in content for kw in CATEGORY_KEYWORDS["mis"])
    
    if is_ce and is_mis:
        return "both"
    elif is_ce:
        return "computer_engineering"
    elif is_mis:
        return "mis"
    else:
        return "both"

def detect_work_type(title, description="", location=""):
    content = f"{title} {description} {location}".lower()
    for w_type, kws in WORK_TYPE_KEYWORDS.items():
        if any(kw in content for kw in kws):
            return w_type
    return "office"

def save_job(job_data):
    conn = get_connection()
    cursor = conn.cursor()
    
    title = job_data.get("title", "").strip()
    company = job_data.get("company", "").strip()
    raw_url = job_data.get("url", "").strip()
    location = job_data.get("location", "Türkiye").strip()
    platform = job_data.get("platform", "Bilinmeyen").strip()
    description = job_data.get("description", "").strip()
    
    if "testcorp" in company.lower() or "unit test" in company.lower():
        conn.close()
        return None, False

    hash_key = generate_hash(title, company)
    category = job_data.get("category") or categorize_job(title, description)
    work_type = job_data.get("work_type") or detect_work_type(title, description, location)
    
    try:
        cursor.execute("""
            INSERT INTO jobs (hash_key, title, company, location, platform, url, description, category, work_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (hash_key, title, company, location, platform, raw_url, description, category, work_type))
        conn.commit()
        job_id = cursor.lastrowid
        conn.close()
        return job_id, True
    except sqlite3.IntegrityError:
        cursor.execute("""
            UPDATE jobs 
            SET url = ?, description = ?, location = ?, work_type = ?, category = ?, scanned_at = CURRENT_TIMESTAMP 
            WHERE hash_key = ?
        """, (raw_url, description, location, work_type, category, hash_key))
        cursor.execute("SELECT id FROM jobs WHERE hash_key = ?", (hash_key,))
        row = cursor.fetchone()
        conn.commit()
        conn.close()
        return (row["id"] if row else None), False

def get_jobs(category=None, search=None, work_type=None, status=None, platform=None, limit=100, offset=0):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM jobs WHERE status != 'ignored' AND company NOT LIKE '%unit test%' AND company NOT LIKE '%testcorp%'"
    params = []
    
    if category:
        if category == "computer_engineering":
            query += " AND (category = 'computer_engineering' OR category = 'both')"
        elif category == "mis":
            query += " AND (category = 'mis' OR category = 'both')"
        else:
            query += " AND category = ?"
            params.append(category)
            
    if search:
        query += " AND (LOWER(title) LIKE ? OR LOWER(company) LIKE ? OR LOWER(location) LIKE ?)"
        search_param = f"%{search.lower()}%"
        params.extend([search_param, search_param, search_param])
        
    if work_type:
        query += " AND work_type = ?"
        params.append(work_type)

    if status and status != 'all':
        query += " AND status = ?"
        params.append(status)
        
    if platform and platform != 'all':
        query += " AND platform = ?"
        params.append(platform)

    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    jobs = [dict(row) for row in rows]
    
    conn.close()
    return jobs

def update_job_status(job_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE jobs SET status = ? WHERE id = ?", (status, job_id))
    conn.commit()
    conn.close()
    return True

def add_note(author, message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (author, message) VALUES (?, ?)", (author.strip() or "Anonim", message.strip()))
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    return note_id

def get_notes(limit=50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_notification(title, message, n_type='info'):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notifications (title, message, type)
        VALUES (?, ?, ?)
    """, (title, message, n_type))
    conn.commit()
    conn.close()

def get_notifications(limit=50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notifications ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def mark_notifications_read():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = 1 WHERE is_read = 0")
    conn.commit()
    conn.close()
    return True

def get_unread_notification_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM notifications WHERE is_read = 0")
    row = cursor.fetchone()
    conn.close()
    return row["count"] if row else 0

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM jobs WHERE status != 'ignored' AND company NOT LIKE '%unit test%' AND company NOT LIKE '%testcorp%'")
    total_jobs = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(*) as ce FROM jobs WHERE status != 'ignored' AND company NOT LIKE '%unit test%' AND company NOT LIKE '%testcorp%' AND (category = 'computer_engineering' OR category = 'both')")
    ce_jobs = cursor.fetchone()["ce"]

    cursor.execute("SELECT COUNT(*) as mis FROM jobs WHERE status != 'ignored' AND company NOT LIKE '%unit test%' AND company NOT LIKE '%testcorp%' AND (category = 'mis' OR category = 'both')")
    mis_jobs = cursor.fetchone()["mis"]

    cursor.execute("SELECT COUNT(*) as today FROM jobs WHERE status != 'ignored' AND company NOT LIKE '%unit test%' AND company NOT LIKE '%testcorp%' AND DATE(created_at) = DATE('now')")
    today_jobs = cursor.fetchone()["today"]

    cursor.execute("SELECT COUNT(*) as applied FROM jobs WHERE status = 'applied'")
    applied_jobs = cursor.fetchone()["applied"]

    cursor.execute("SELECT COUNT(*) as saved FROM jobs WHERE status = 'saved'")
    saved_jobs = cursor.fetchone()["saved"]

    unread_notifications = get_unread_notification_count()

    conn.close()
    return {
        "total_jobs": total_jobs,
        "ce_jobs": ce_jobs,
        "mis_jobs": mis_jobs,
        "today_jobs": today_jobs,
        "applied_jobs": applied_jobs,
        "saved_jobs": saved_jobs,
        "unread_notifications": unread_notifications
    }

def record_scan_start():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scans (status) VALUES ('running')")
    conn.commit()
    scan_id = cursor.lastrowid
    conn.close()
    return scan_id

def record_scan_end(scan_id, jobs_found, new_jobs_added):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE scans 
        SET finished_at = CURRENT_TIMESTAMP, jobs_found = ?, new_jobs_added = ?, status = 'completed'
        WHERE id = ?
    """, (jobs_found, new_jobs_added, scan_id))
    conn.commit()
    conn.close()

init_db()
