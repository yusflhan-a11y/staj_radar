import requests
import re
from urllib.parse import urlparse, urljoin

class BaseScraper:
    def __init__(self, name):
        self.name = name
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }

    def sanitize_url(self, url, base_domain=""):
        if not url:
            return ""
        url = url.strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            if base_domain:
                url = urljoin(base_domain, url)
            else:
                url = f"https://{url}"
        
        # Remove tracking parameters
        url = re.sub(r'[\?&](utm_[^&]+|ref_[^&]+|session[^&]+)', '', url)
        return url

    def is_valid_url(self, url):
        if not url:
            return False
        try:
            result = urlparse(url)
            return all([result.scheme in ['http', 'https'], result.netloc])
        except Exception:
            return False

    def build_company_career_url(self, company_name, platform_name=""):
        """
        Smart fallback URL builder for any company to prevent 404 or broken links
        """
        clean_company = re.sub(r'[^\w\s]', '', company_name).strip()
        search_query = f"{clean_company} kariyer staj başvurusu"
        return f"https://www.google.com/search?q={requests.utils.quote(search_query)}"

    def fetch_jobs(self):
        raise NotImplementedError("Subclasses must implement fetch_jobs()")
