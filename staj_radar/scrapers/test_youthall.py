import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def test_youthall():
    url = "https://www.youthall.com/tr/jobs/"
    res = requests.get(url, headers=headers, timeout=10)
    print("Youthall Status:", res.status_code)
    soup = BeautifulSoup(res.text, "html.parser")
    
    for a in soup.select("a[href]"):
        href = a.get("href", "")
        title = a.get_text(strip=True)
        if "/job/" in href or "/staj/" in href or "staj" in title.lower():
            print(f"TITLE: {title} | LINK: https://www.youthall.com{href}")

if __name__ == "__main__":
    test_youthall()
