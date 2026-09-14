import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "staj_radar.db")

CATEGORY_KEYWORDS = {
    "computer_engineering": [
        "yazılım", "software", "backend", "frontend", "fullstack", "mobile", "mobil",
        "android", "ios", "react", "node", "python", "java", "c++", "c#", ".net",
        "developer", "geliştirici", "muhendis", "mühendis", "devops", "cloud",
        "cyber", "siber", "yapay zeka", "ai", "machine learning", "veri bilim", "data science"
    ],
    "mis": [
        "yönetim bilişim", "ybs", "mis", "iş analist", "business analyst",
        "veri analist", "data analyst", "iş zekası", "bi ", "powerbi", "tableau",
        "ürün yönet", "product manager", "project manager", "proje yönet",
        "erp", "sap", "crm", "sistem analist", "dijital dönüşüm", "proje staj"
    ]
}

WORK_TYPE_KEYWORDS = {
    "remote": ["uzaktan", "remote", "home office", "evden"],
    "hybrid": ["hibrit", "hybrid", "karma"],
    "office": ["ofis", "office", "yerinde", "ofisten"]
}

INTERNSHIP_KEYWORDS = ["staj", "intern", "trainee", "genç yetenek", "talent"]

# A scan only marks listings as expired when their source was successfully read.
# Keeping this value in one place also makes the six-hour interval testable.
SCAN_INTERVAL_SECONDS = 6 * 60 * 60
