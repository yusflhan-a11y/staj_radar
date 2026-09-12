class BaseScraper:
    def __init__(self, platform_name):
        self.platform_name = platform_name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'
        }

    def fetch_jobs(self):
        raise NotImplementedError("Subclasses must implement fetch_jobs()")
