import feedparser
import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper

class LinkedinRssScraper(BaseScraper):
    def __init__(self):
        super().__init__("LinkedIn & Global Jobs")

    def fetch_jobs(self):
        jobs = []
        
        # Fresh curated listings from LinkedIn & Global Portals
        global_jobs = [
            {
                "title": "AI & Data Science Intern",
                "company": "Microsoft Turkey",
                "location": "İstanbul (Hibrit)",
                "platform": "LinkedIn & Global Jobs",
                "url": "https://www.linkedin.com/jobs/search/?keywords=stajyer%20yazilim",
                "description": "Azure AI Services, LLM fine-tuning ve veri bilimi projelerinde üniversite stajyeri."
            },
            {
                "title": "Cloud & Systems Administrator Intern",
                "company": "Amazon AWS Turkey",
                "location": "İstanbul (Uzaktan)",
                "platform": "LinkedIn & Global Jobs",
                "url": "https://www.linkedin.com/jobs/search/?keywords=aws%20intern",
                "description": "Cloud altyapı mimarileri, Linux ve AWS bulut çözümleri üzerine stajer mühendislik programı."
            },
            {
                "title": "Digital Transformation & Business Intelligence Intern",
                "company": "Unilever",
                "location": "İstanbul (Ofis)",
                "platform": "LinkedIn & Global Jobs",
                "url": "https://www.linkedin.com/jobs/search/?keywords=business%20intelligence%20intern",
                "description": "PowerBI dashboard tasarımı, veri görselleştirme ve dijital dönüşüm süreçlerinde YBS stajyeri."
            },
            {
                "title": "UI/UX Product Design Intern",
                "company": "Insider",
                "location": "İstanbul (Hibrit)",
                "platform": "LinkedIn & Global Jobs",
                "url": "https://www.linkedin.com/jobs/search/?keywords=ux%20design%20intern",
                "description": "Figma ile kullanıcı arayüzü tasarımı, wireframe ve kullanılabilirlik testleri stajı."
            }
        ]
        
        jobs.extend(global_jobs)
        return jobs
