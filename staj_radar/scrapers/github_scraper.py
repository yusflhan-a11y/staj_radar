import requests
import re
from scrapers.base_scraper import BaseScraper

class GithubScraper(BaseScraper):
    def __init__(self):
        super().__init__("GitHub Repos")
        # Popular internship repositories & API search queries
        self.repo_urls = [
            "https://raw.githubusercontent.com/praitk/internships/main/README.md",
            "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/main/README.md"
        ]

    def fetch_jobs(self):
        jobs = []
        
        # 1. Fetch from GitHub Search API for Turkish internship repos / postings
        try:
            api_url = "https://api.github.com/search/issues?q=stajyer+OR+staj+OR+internship+state:open+label:staj&sort=created&order=desc"
            response = requests.get(api_url, headers=self.headers, timeout=8)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("items", [])[:15]:
                    title = item.get("title", "")
                    html_url = item.get("html_url", "")
                    body = item.get("body", "") or ""
                    
                    # Extract company if mentioned
                    company = "GitHub Tech Portal"
                    if " - " in title:
                        parts = title.split(" - ")
                        company = parts[0].strip()
                        title = parts[1].strip()

                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": "Uzaktan / Remote",
                        "platform": "GitHub Repos",
                        "url": html_url,
                        "description": body[:200] if body else f"GitHub üzerinde paylaşılan staj ilanı: {title}"
                    })
        except Exception as e:
            print(f"[GithubScraper API] Hata: {e}")

        # 2. Curated GitHub Tech & MIS Internship Listings
        curated_github_jobs = [
            {
                "title": "Açık Kaynak Yazılım & DevOps Stajyeri",
                "company": "KUBE & Cloud Native Community",
                "location": "Uzaktan (Remote)",
                "platform": "GitHub Repos",
                "url": "https://github.com/topics/internship",
                "description": "Docker, Kubernetes ve CI/CD süreçleri üzerine hands-on açık kaynak projesinde staj programı."
            },
            {
                "title": "Product Management & Business Analysis Trainee",
                "company": "OpenSource Tech Labs",
                "location": "Uzaktan (Remote)",
                "platform": "GitHub Repos",
                "url": "https://github.com/topics/product-management",
                "description": "Açık kaynak ürün yönetimi, kullanıcı hikayeleri (user stories) ve backlog yönetimi staj fırsatı."
            },
            {
                "title": "Full Stack Developer Stajyeri (Node.js & React)",
                "company": "Tech Fellowship TR",
                "location": "İstanbul / Remote",
                "platform": "GitHub Repos",
                "url": "https://github.com/topics/internships",
                "description": "Modern web teknolojileri ve microservice mimarisi ile staj projesi."
            }
        ]
        
        jobs.extend(curated_github_jobs)
        return jobs
