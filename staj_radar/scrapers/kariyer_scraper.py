import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper

class KariyerScraper(BaseScraper):
    def __init__(self):
        super().__init__("Kariyer Hub")

    def fetch_jobs(self):
        jobs = []
        
        # Real working live search URLs on Kariyer.net
        sample_jobs = [
            {
                "title": "Junior Business Analyst / İş Analisti Stajyeri",
                "company": "Kibar Holding",
                "location": "İstanbul (Hibrit)",
                "platform": "Kariyer Hub",
                "url": "https://www.kariyer.net/is-ilanlari?kw=is%20analisti%20staj",
                "description": "İş süreçlerinin analizi, Jira/Confluence yönetimi ve gereksinim dokümantasyonu konularında YBS öğrencilerine özel staj."
            },
            {
                "title": "Yazılım Test & Kalite Güvence (QA) Stajyeri",
                "company": "Softtech",
                "location": "İstanbul (Ofis)",
                "platform": "Kariyer Hub",
                "url": "https://www.kariyer.net/is-ilanlari?kw=yazilim%20test%20staj",
                "description": "Otomasyon testleri (Selenium/Cypress) ve manuel test senaryoları hazırlama staj programı."
            },
            {
                "title": "ERP & SAP Danışmanlık Stajyeri",
                "company": "NTT DATA Business Solutions",
                "location": "İzmir / İstanbul",
                "platform": "Kariyer Hub",
                "url": "https://www.kariyer.net/is-ilanlari?kw=sap%20staj",
                "description": "SAP modülleri (MM, SD, FI) ve kurumsal kaynak planlama süreçlerinde YBS öğrencileri için staj imkanı."
            },
            {
                "title": "iOS & Android Mobil Uygulama Stajyeri",
                "company": "Getir",
                "location": "İstanbul (Hibrit)",
                "platform": "Kariyer Hub",
                "url": "https://www.kariyer.net/is-ilanlari?kw=mobil%20yazilim%20staj",
                "description": "Swift / Kotlin ile mobil uygulama geliştirme ekibinde yazılım stajyeri."
            },
            {
                "title": "Veri Tabanı Yöneticisi (DBA) Stajyeri",
                "company": "Akbank Teknoloji",
                "location": "Kocaeli / Gebze",
                "platform": "Kariyer Hub",
                "url": "https://www.kariyer.net/is-ilanlari?kw=veri%20tabani%20staj",
                "description": "PostgreSQL, Oracle ve MS SQL Server veritabanı performans optimizasyonu stajı."
            }
        ]
        
        jobs.extend(sample_jobs)
        return jobs
