import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "staj_radar.db")
TIMEZONE = "Europe/Istanbul"
CRON_SECRET = os.environ.get("CRON_SECRET", "staj_radar_cron_secret_key")

# Strict exclusions from Computer Engineering category
NON_CE_EXCLUSIONS = [
    "satış", "satis", "mağaza", "magaza", "perakende", "hukuk", "saha",
    "servis", "adli", "muhasebe", "müşteri", "musteri", "danışmanı", "danismani"
]

CATEGORY_KEYWORDS = {
    "computer_engineering": [
        "yazılım", "software", "backend", "frontend", "fullstack", "mobile", "mobil",
        "android", "ios", "react", "node", "python", "java", "c++", "c#", ".net",
        "developer", "geliştirici", "yazılım mühendis", "devops", "cloud",
        "cyber", "siber", "yapay zeka", "ai", "machine learning", "veri bilim", "data science",
        "it infrastructure", "qa", "kalite güvence", "test mühendis", "sistem yöneticis"
    ],
    "mis": [
        "yönetim bilişim", "ybs", "mis", "iş analist", "business analyst",
        "veri analist", "data analyst", "iş zekası", "bi ", "powerbi", "tableau",
        "ürün yönet", "product manager", "project manager", "proje yönet", "proje",
        "erp", "sap", "crm", "sistem analist", "dijital dönüşüm", "pazarlama",
        "marketing", "işletme", "business", "management", "trainee", "yönetici",
        "operasyon", "ik", "insan kaynakları", "finans", "strateji", "satış", "satis",
        "burs", "lojistik", "tedarik zinciri", "kombine", "genç yetenek"
    ]
}

WORK_TYPE_KEYWORDS = {
    "remote": ["uzaktan", "remote", "home office", "evden"],
    "hybrid": ["hibrit", "hybrid", "karma"],
    "office": ["ofis", "office", "yerinde", "ofisten"]
}

INTERNSHIP_KEYWORDS = ["staj", "intern", "trainee", "genç yetenek", "talent"]

SCAN_INTERVAL_SECONDS = 6 * 60 * 60
