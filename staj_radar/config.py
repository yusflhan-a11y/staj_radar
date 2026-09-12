import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "staj_radar.db")

# Category Keywords for Automatic Categorization
CATEGORY_KEYWORDS = {
    "computer_engineering": [
        "yazılım", "software", "backend", "frontend", "fullstack", "full stack",
        "python", "java", "c++", "c#", ".net", "react", "vue", "angular", "node",
        "developer", "geliştirici", "geliştirme", "mobil", "android", "ios", "flutter",
        "ai", "yapay zeka", "machine learning", "makine öğrenmesi", "data engineer",
        "veri mühendisi", "cyber security", "siber güvenlik", "devops", "cloud",
        "gömülü", "embedded", "qa", "test mühendisi", "test engineer"
    ],
    "mis": [
        "iş analisti", "business analyst", "veri analisti", "data analyst",
        "ürün yönetimi", "product manager", "product management", "proje yönetimi",
        "project manager", "it specialist", "bilgi teknolojileri", "sistem analisti",
        "system analyst", "erp", "sap", "bi", "business intelligence", "iş zekası",
        "dijital dönüşüm", "digital transformation", "ui/ux", "ux", "ui", "crm",
        "veritabanı", "database admin", "süreç analisti", "process analyst"
    ]
}

# General Internship Keywords to Filter Relevant Listings
INTERNSHIP_KEYWORDS = [
    "staj", "stajyer", "intern", "internship", "trainee", "genç yetenek",
    "fellowship", "candidate", "talent", "bootcamp", "aday"
]

# Work Type Recognition Keywords
WORK_TYPE_KEYWORDS = {
    "remote": ["remote", "uzaktan", "evden", "work from home"],
    "hybrid": ["hibrit", "hybrid", "karma"],
    "office": ["ofis", "office", "yerinde", "on-site", "onsite"]
}
