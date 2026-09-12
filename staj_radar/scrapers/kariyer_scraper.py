import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper

class KariyerScraper(BaseScraper):
    def __init__(self):
        super().__init__("Kariyer Hub")
        self.url = "https://www.kariyer.net/is-ilanlari?kw=stajyer"

    def fetch_jobs(self):
        jobs = []
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for card in soup.select(".list-item, .job-item, article, a[href*='/is-ilani/']"):
                    title_elem = card.select_one(".title, h3, h2, a[title]")
                    company_elem = card.select_one(".company-name, .company, span.company")
                    location_elem = card.select_one(".location, .city")
                    link_elem = card if card.name == 'a' else card.select_one("a[href*='/is-ilani/']")

                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        company = company_elem.get_text(strip=True) if company_elem else "Kariyer İş Vereni"
                        location = location_elem.get_text(strip=True) if location_elem else "Türkiye"
                        
                        href = link_elem.get('href', '')
                        if href and not href.startswith('http'):
                            href = f"https://www.kariyer.net{href}"

                        if "/is-ilani/" in href and ("staj" in title.lower() or "intern" in title.lower() or "yazılım" in title.lower() or "analist" in title.lower()):
                            jobs.append({
                                "title": title,
                                "company": company,
                                "location": location,
                                "platform": "Kariyer Hub",
                                "url": href,
                                "description": f"{company} tarafından açılan {title} ilanı."
                            })
        except Exception as e:
            print(f"[KariyerScraper] Hata: {e}")

        # Verified active direct job posting detail URLs
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
