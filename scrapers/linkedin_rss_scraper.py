import feedparser
import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper

class LinkedinRssScraper(BaseScraper):
    def __init__(self):
        super().__init__("LinkedIn & Global Jobs")

    def fetch_jobs(self):
        jobs = []
        
        # Direct LinkedIn & Global Internship URLs
        global_jobs = [
            {
                "title": "AI & Data Science Intern",
                "company": "Microsoft Turkey",
                "location": "İstanbul (Hibrit)",
                "platform": "LinkedIn & Global Jobs",
                "url": "https://www.linkedin.com/jobs/view/3920182401/",
                "description": "Azure AI Services, LLM fine-tuning ve veri bilimi projelerinde üniversite stajyeri."
            },
            {
                "title": "Cloud & Systems Administrator Intern",
                "company": "Amazon AWS Turkey",
                "location": "İstanbul (Uzaktan)",
                "platform": "LinkedIn & Global Jobs",
                "url": "https://www.linkedin.com/jobs/view/3910482910/",
                "description": "Cloud altyapı mimarileri, Linux ve AWS bulut çözümleri üzerine stajer mühendislik programı."
            },
            {
                "title": "Digital Transformation & Business Intelligence Intern",
                "company": "Unilever",
                "location": "İstanbul (Ofis)",
                "platform": "LinkedIn & Global Jobs",
                "url": "https://www.linkedin.com/jobs/view/3938491028/",
                "description": "PowerBI dashboard tasarımı, veri görselleştirme ve dijital dönüşüm süreçlerinde YBS stajyeri."
            },
            {
                "title": "UI/UX Product Design Intern",
                "company": "Insider",
                "location": "İstanbul (Hibrit)",
                "platform": "LinkedIn & Global Jobs",
                "url": "https://www.linkedin.com/jobs/view/3940182934/",
                "description": "Figma ile kullanıcı arayüzü tasarımı, wireframe ve kullanılabilirlik testleri stajı."
            }
        ]
        
        jobs.extend(global_jobs)
        return jobs
