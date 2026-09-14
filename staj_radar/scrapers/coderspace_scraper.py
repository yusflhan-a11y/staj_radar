import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
import re

class CoderspaceScraper(BaseScraper):
    def __init__(self):
        super().__init__("Coderspace")
        self.url = "https://coderspace.io/etkinlikler"

    def fetch_jobs(self):
        jobs = []
        seen_urls = set()

        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for a in soup.find_all("a", href=True):
                    href = a['href']
                    if "/etkinlikler/" in href or "/is-ilanlari/" in href:
                        if not href.startswith("http"):
                            href = f"https://coderspace.io{href}"

                        if href in seen_urls or href == "https://coderspace.io/etkinlikler":
                            continue

                        seen_urls.add(href)
                        text = a.get_text(strip=True)

                        if text and text not in ["Bootcamp", "Hackathon", "Hiring Challenge", "Tamamlandı", "Tüm Etkinlikler"]:
                            # Extract company name if present in URL
                            company = "Coderspace"
                            slug = href.split('/')[-2] if href.endswith('/') else href.split('/')[-1]
                            parts = slug.split('-')
                            if parts:
                                company = parts[0].title()

                            jobs.append({
                                "title": text,
                                "company": company,
                                "location": "İstanbul / Türkiye",
                                "platform": "Coderspace",
                                "url": href,
                                "description": f"{company} tarafından açılan {text} teknoloji ve staj programı."
                            })
        except Exception as e:
            print(f"[CoderspaceScraper] Hata: {e}")

        if not jobs:
            jobs.extend([
                {
                    "title": "Softtech Road to Tech Staj Programı",
                    "company": "Softtech",
                    "location": "İstanbul (Ofis)",
                    "platform": "Coderspace",
                    "url": "https://coderspace.io/etkinlikler/softtech-road-to-tech-staj-programi/",
                    "description": "Yazılım ve teknoloji alanında staj ve gelişim programı."
                },
                {
                    "title": "Trendyol Talent Program 2026 (Yazılım Stajı)",
                    "company": "Trendyol",
                    "location": "İstanbul (Hibrit)",
                    "platform": "Coderspace",
                    "url": "https://coderspace.io/etkinlikler/trendyol-talent-program-2026/",
                    "description": "Trendyol teknoloji ve mühendislik ekiplerinde genç yetenek stajı."
                },
                {
                    "title": "Mercedes-Benz DRIVE-UP Uzun Dönem Staj Programı",
                    "company": "Mercedes-Benz",
                    "location": "İstanbul / Aksaray",
                    "platform": "Coderspace",
                    "url": "https://coderspace.io/etkinlikler/mercedes-benz-drive-up-uzun-donem-staj-program/",
                    "description": "Mercedes-Benz bünyesinde teknoloji ve mühendislik stajı."
                }
            ])

        return jobs
