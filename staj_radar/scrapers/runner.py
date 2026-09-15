import sys
import os
import time
import threading
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scrapers.youthall_scraper import YouthallScraper
from scrapers.coderspace_scraper import CoderspaceScraper
from scrapers.kariyer_scraper import KariyerScraper
import database

SCAN_LOCK = threading.Lock()

def run_all_scrapers():
    # Job Lock / Distributed Mutex Lock
    acquired = SCAN_LOCK.acquire(blocking=False)
    if not acquired:
        print("[ScraperRunner] Tarama zaten devam ediyor. İkinci eşzamanlı tarama engellendi.")
        return {
            "status": "locked",
            "message": "Tarama zaten arka planda çalışıyor.",
            "jobs_found": 0, "new_jobs": 0, "updated_jobs": 0, "expired_jobs": 0, "closed_jobs": 0
        }

    start_time = time.time()
    scan_id = database.record_scan_start()
    scan_started_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    scrapers = [
        YouthallScraper(),
        CoderspaceScraper(),
        KariyerScraper()
    ]
    
    total_found = 0
    new_jobs = 0
    updated_jobs = 0
    errors = []
    successful_platforms = []

    try:
        # Step 1: Check application deadlines
        deadline_expired = database.check_deadlines_and_status()

        # Step 2: Run each platform scraper with try/catch isolation
        for scraper in scrapers:
            p_name = scraper.platform_name
            try:
                print(f"[ScraperRunner] {p_name} taranıyor...")
                jobs = scraper.fetch_jobs()
                total_found += len(jobs)

                if getattr(scraper, "last_fetch_succeeded", True):
                    successful_platforms.append(p_name)
                
                for job in jobs:
                    if job.get("url") and job["url"].startswith("http"):
                        job_id, is_new, is_updated = database.save_job(job)
                        if is_new:
                            new_jobs += 1
                        elif is_updated:
                            updated_jobs += 1

            except Exception as e:
                err_msg = f"{p_name} hatası: {str(e)}"
                print(f"[ScraperRunner] {err_msg}")
                errors.append(err_msg)

        # Step 3: Expire listings absent from successful scans
        unseen_expired = database.expire_unseen_jobs(successful_platforms, scan_started_at)
        total_expired = deadline_expired + unseen_expired

        duration = round(time.time() - start_time, 2)
        errors_str = " | ".join(errors) if errors else ""
        scan_status = "completed" if not errors else ("partial_error" if successful_platforms else "failed")

        database.record_scan_end(
            scan_id=scan_id,
            jobs_found=total_found,
            new_jobs_added=new_jobs,
            updated_jobs=updated_jobs,
            expired_jobs=total_expired,
            closed_jobs=0,
            duration_seconds=duration,
            status=scan_status,
            errors_log=errors_str
        )

        if new_jobs > 0:
            database.add_notification(
                title=f"🔔 {new_jobs} Yeni Staj İlanı Eklendi!",
                message=f"Taramada {new_jobs} yeni doğrudan başvurulabilir staj ilanı bulundu.",
                n_type="info"
            )

        print(f"[ScraperRunner] Tarama tamamlandı ({duration} sn). Bulunan: {total_found}, Yeni: {new_jobs}, Güncellenen: {updated_jobs}, Süresi Dolar: {total_expired}")

        return {
            "status": scan_status,
            "duration_seconds": duration,
            "jobs_found": total_found,
            "new_jobs": new_jobs,
            "updated_jobs": updated_jobs,
            "expired_jobs": total_expired,
            "closed_jobs": 0,
            "errors": errors
        }

    finally:
        SCAN_LOCK.release()

if __name__ == "__main__":
    run_all_scrapers()
