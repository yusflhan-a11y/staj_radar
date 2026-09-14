import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
import re

class YouthallScraper(BaseScraper):
    def __init__(self):
        super().__init__("Youthall")
        self.urls = [
            "https://www.youthall.com/tr/jobs/",
            "https://www.youthall.com/tr/is-ilanlari/stajyer/"
        ]

    def fetch_jobs(self):
        jobs = []
        seen_urls = set()

        for target_url in self.urls:
            try:
                response = requests.get(target_url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    self.last_fetch_succeeded = True
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Parse all job links on Youthall
                    for a in soup.find_all("a", href=True):
                        href = a['href']
                        if ("_" in href or "/yetenek-programlari/" in href) and ("/tr/" in href or "/en/" in href):
                            if not href.startswith("http"):
                                href = f"https://www.youthall.com{href}"

                            if href in seen_urls:
                                continue

                            seen_urls.add(href)
                            text = a.get_text(separator=" ", strip=True)

                            # Clean up title and company
                            lines = [line.strip() for line in text.split("\n") if line.strip()]
                            full_text = " ".join(lines)
                            
                            # Filter for relevant keywords
                            lower_text = full_text.lower()
                            if any(kw in lower_text for kw in ["staj", "intern", "trainee", "yazılım", "ybs", "it ", "veri", "analist", "programı"]):
                                # Extract company name from URL if possible (e.g. /tr/Shell/title_123/)
                                company = "Youthall İş Vereni"
                                match = re.search(r'/tr/([^/]+)/|/en/([^/]+)/', href)
                                if match:
                                    raw_comp = match.group(1) or match.group(2)
                                    if raw_comp and raw_comp.lower() not in ["jobs", "is-ilanlari", "yetenek-programlari"]:
                                        company = raw_comp.replace("-", " ").title()

                                # Title cleanup
                                title = lines[0] if lines else "Staj Pozisyonu"
                                if len(title) > 80:
                                    title = title[:77] + "..."

                                jobs.append({
                                    "title": title,
                                    "company": company,
                                    "location": "İstanbul / Türkiye",
                                    "platform": "Youthall",
                                    "url": href,
                                    "description": f"{company} tarafından açılan {title} ilanı. Doğrudan Youthall başvuru sayfası."
                                })
            except Exception as e:
                print(f"[YouthallScraper] Hata ({target_url}): {e}")

        return jobs
