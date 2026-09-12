import requests

class BaseScraper:
    def __init__(self, name):
        self.name = name
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }

    def fetch_jobs(self):
        """
        Subclasses must implement this method.
        Should return a list of dicts:
        [
            {
                "title": "Software Engineering Intern",
                "company": "Trendyol",
                "location": "İstanbul (Hibrit)",
                "platform": "Youthall",
                "url": "https://...",
                "description": "...",
                "work_type": "hybrid"
            },
            ...
        ]
        """
        raise NotImplementedError("Subclasses must implement fetch_jobs()")
