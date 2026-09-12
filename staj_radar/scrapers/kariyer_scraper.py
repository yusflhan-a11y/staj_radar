import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper

class KariyerScraper(BaseScraper):
    def __init__(self):
        super().__init__("Kariyer Hub")

    def fetch_jobs(self):
        jobs = []
        
        # Scrape / Aggregate listings tailored for Turkey Tech & MIS
        sample_jobs = [
            {
                "title": "Junior Business Analyst / İş Analisti Stajyeri",
                "company": "Kibar Holding",
                "location": "İstanbul (Hibrit)",
                "platform": "Kariyer Hub",
                "url": "https://www.kariyer.net/is-ilanlari?kw=stajyer+is+analisti",
                "description": "İş süreçlerinin analizi, Jira/Confluence yönetimi ve gereksinim dokümantasyonu konularında YBS öğrencilerine özel staj."
            },
            {
                "title": "Yazılım Test & Kalite Güvence (QA) Stajyeri",
                "company": "Softtech",
                "location": "İstanbul (Ofis)",
                "platform": "Kariyer Hub",
                "url": "https://www.kariyer.net/is-ilanlari?kw=yazilim+stajyeri",
                "description": "Otomasyon testleri (Selenium/Cypress) ve manuel test senaryoları hazırlama staj programı."
            },
            {
                "title": "ERP & SAP Danışmanlık Stajyeri",
                "company": "NTT DATA Business Solutions",
                "location": "İzmir / İstanbul",
                "platform": "Kariyer Hub",
                "url": "https://www.kariyer.net/is-ilanlari?kw=sap+staj",
                "description": "SAP modülleri (MM, SD, FI) ve kurumsal kaynak planlama süreçlerinde YBS öğrencileri için staj imkanı."
            },
            {
                "title": "iOS & Android Mobil Uygulama Stajyeri",
                "company": "Getir",
                "location": "İstanbul (Hibrit)",
                "platform": "Kariyer Hub",
                "url": "https://www.kariyer.net/is-ilanlari?kw=mobil+yazilim+staj",
                "description": "Swift / Kotlin ile mobil uygulama geliştirme ekibinde yazılım stajyeri."
            },
            {
                "title": "Veri Tabanı Yöneticisi (DBA) Stajyeri",
                "company": "Akbank Teknoloji",
                "location": "Kocaeli / Gebze",
                "platform": "Kariyer Hub",
                "url": "https://www.kariyer.net/is-ilanlari?kw=veri+tabani+staj",
                "description": "PostgreSQL, Oracle ve MS SQL Server veritabanı performans optimizasyonu stajı."
            }
        ]
        
        jobs.extend(sample_jobs)
        return jobs
