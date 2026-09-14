import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scrapers.youthall_scraper import YouthallScraper
from scrapers.coderspace_scraper import CoderspaceScraper
from scrapers.kariyer_scraper import KariyerScraper
import database
from datetime import datetime

def run_all_scrapers():
    print("[ScraperRunner] Scrapers başlatılıyor...")
    scan_id = database.record_scan_start()
    scan_started_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    scrapers = [
        YouthallScraper(),
        CoderspaceScraper(),
        KariyerScraper()
    ]
    
    total_found = 0
    total_added = 0
    successful_platforms = []
    
    for scraper in scrapers:
        try:
            print(f"[ScraperRunner] {scraper.platform_name} taranıyor...")
            jobs = scraper.fetch_jobs()
            total_found += len(jobs)

            # Empty results are valid. Only a successful HTTP response allows
            # this source's unseen listings to be archived.
            if scraper.last_fetch_succeeded:
                successful_platforms.append(scraper.platform_name)
            
            for job in jobs:
                # Ensure URL is direct and valid
                if job.get("url") and job["url"].startswith("http"):
                    job_id, is_new = database.save_job(job)
                    if is_new:
                        total_added += 1
        except Exception as e:
            print(f"[ScraperRunner] {scraper.platform_name} hatası: {e}")
            
    expired_count = database.expire_unseen_jobs(successful_platforms, scan_started_at)
    database.record_scan_end(scan_id, total_found, total_added)
    
    if total_added > 0:
        database.add_notification(
            title=f"🔔 {total_added} Yeni Staj İlanı Eklendi!",
            message=f"Taramada {total_added} yeni doğrudan başvurulabilir staj ilanı bulundu.",
            n_type="info"
        )

    if expired_count > 0:
        database.add_notification(
            title=f"📦 {expired_count} İlan Süresi Bitti",
            message="Kaynağında artık görünmeyen ilanlar ‘Süresi Bitmiş’ kutusuna taşındı.",
            n_type="info"
        )
        
    print(f"[ScraperRunner] Tarama tamamlandı. Bulunan: {total_found}, Yeni: {total_added}, Süresi biten: {expired_count}")
    return total_found, total_added, expired_count

if __name__ == "__main__":
    run_all_scrapers()
