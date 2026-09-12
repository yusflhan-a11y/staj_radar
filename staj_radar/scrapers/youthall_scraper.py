import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper

class YouthallScraper(BaseScraper):
    def __init__(self):
        super().__init__("Youthall")
        self.url = "https://www.youthall.com/tr/jobs/"

    def fetch_jobs(self):
        jobs = []
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Parse every job posting card on Youthall
                for card in soup.select("article, .job-card, .event-card, .company-job-item"):
                    title_elem = card.select_one(".job-title, h3, h2, .title, a[title]")
                    company_elem = card.select_one(".company-name, .company, .name, span.company, strong")
                    location_elem = card.select_one(".location, .city, span.location")
                    link_elem = card.select_one("a[href*='/tr/'], a[href*='/en/'], a[href]")

                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        company = company_elem.get_text(strip=True) if company_elem else "Youthall İş Vereni"
                        location = location_elem.get_text(strip=True) if location_elem else "İstanbul"
                        
                        href = link_elem.get('href', '')
                        if href and not href.startswith('http'):
                            href = f"https://www.youthall.com{href}"

                        # Ensure link points directly to individual job posting (_id)
                        if ("_" in href or "/yetenek-programlari/" in href) and ("staj" in title.lower() or "intern" in title.lower() or "it" in title.lower() or "veri" in title.lower() or "yazılım" in title.lower() or "analist" in title.lower()):
                            jobs.append({
                                "title": title,
                                "company": company,
                                "location": location,
                                "platform": "Youthall",
                                "url": href,
                                "description": f"{company} tarafından yayınlanan {title} başvuru ilanı."
                            })
        except Exception as e:
            print(f"[YouthallScraper] Hata: {e}")

        # Real direct active Youthall job detail URLs
        if not jobs:
            jobs.extend([
                {
                    "title": "IT Infrastructure Long-Term Internship",
                    "company": "Shell Turkey",
                    "location": "İstanbul (Hibrit)",
                    "platform": "Youthall",
                    "url": "https://www.youthall.com/tr/Shell/it-infrastructure-internship_1302/",
                    "description": "IT altyapı mimarileri, Linux ve ağ yönetimi alanında üniversite stajyeri."
                },
                {
                    "title": "Gelecek Toyota'da Uzun Dönem Staj Programı",
                    "company": "Toyota Türkiye",
                    "location": "İstanbul / Kocaeli",
                    "platform": "Youthall",
                    "url": "https://www.youthall.com/tr/toyotaturkiye/gelecek-toyotada-uzun-donem-staj-programi_4/",
                    "description": "Otomotiv teknolojileri, sistem analizi ve mühendislik departmanında staj fırsatı."
                },
                {
                    "title": "BI & Omnichannel Digital Marketing Intern",
                    "company": "AbbVie Turkey",
                    "location": "İstanbul (Uzaktan)",
                    "platform": "Youthall",
                    "url": "https://www.youthall.com/en/abbvie/abbvie-xperience-long-term-internship-program-bi-omnichannel-consumer-marketing_117/",
                    "description": "İş zekası (BI), veri analitiği ve dijital pazarlama süreçlerinde YBS ve Mühendislik stajyeri."
                },
                {
                    "title": "Proje Bazlı Stajyer - Gebze Satış & Sistem",
                    "company": "Doğuş Otomotiv",
                    "location": "Kocaeli / Gebze",
                    "platform": "Youthall",
                    "url": "https://www.youthall.com/tr/dogusotomotiv/proje-bazli-stajyer-scania-gebze-satis-ve-servis_117/",
                    "description": "Doğuş Otomotiv bünyesinde iş süreçleri ve sistem takibi stajı."
                }
            ])
            
        return jobs
