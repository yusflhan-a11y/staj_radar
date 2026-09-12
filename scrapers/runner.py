import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import save_job, add_notification, record_scan_start, record_scan_end
from scrapers.youthall_scraper import YouthallScraper
from scrapers.github_scraper import GithubScraper
from scrapers.kariyer_scraper import KariyerScraper
from scrapers.linkedin_rss_scraper import LinkedinRssScraper

def run_all_scrapers():
    scan_id = record_scan_start()
    scrapers = [
        YouthallScraper(),
        GithubScraper(),
        KariyerScraper(),
        LinkedinRssScraper()
    ]
    
    total_found = 0
    new_jobs_added = 0
    
    for scraper in scrapers:
        print(f"[{scraper.name}] Tarama başlatılıyor...")
        try:
            jobs = scraper.fetch_jobs()
            total_found += len(jobs)
            for job in jobs:
                job_id, is_new = save_job(job)
                if is_new:
                    new_jobs_added += 1
        except Exception as e:
            print(f"[{scraper.name}] Tarama hatası: {e}")
            
    record_scan_end(scan_id, total_found, new_jobs_added)
    
    # Trigger in-app notification if new jobs found or summary scan completed
    if new_jobs_added > 0:
        add_notification(
            title="🎯 Yeni Staj İlanları Bulundu!",
            message=f"Günlük taramada {new_jobs_added} adet yeni staj ilanı listelerinize eklendi.",
            n_type="new_jobs"
        )
    else:
        add_notification(
            title="🔍 Tarama Tamamlandı",
            message=f"Tüm platformlar tarandı ({total_found} ilan tarandı). Yeni ilan eklenmedi.",
            n_type="info"
        )
        
    print(f"Tarama Tamamlandı! Toplam Taranan: {total_found}, Yeni Eklenen: {new_jobs_added}")
    return {
        "total_found": total_found,
        "new_jobs_added": new_jobs_added
    }

if __name__ == "__main__":
    run_all_scrapers()
