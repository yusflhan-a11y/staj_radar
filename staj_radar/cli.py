import argparse
import json
import csv
import database
from scrapers.runner import run_all_scrapers

def main():
    parser = argparse.ArgumentParser(description="Staj Radar - CLI Takip ve Tarama")
    parser.add_argument("--scan", action="store_true", help="Tüm platformları tara ve ilanları güncelle")
    parser.add_argument("--ce", action="store_true", help="Bilgisayar Mühendisliği ilanlarını listele")
    parser.add_argument("--mis", action="store_true", help="Yönetim Bilişim Sistemleri (YBS) ilanlarını listele")
    parser.add_argument("--stats", action="store_true", help="Uygulama istatistiklerini göster")
    parser.add_argument("--export-csv", type=str, help="İlanları CSV dosyası olarak kaydet (ör: ilanlar.csv)")

    args = parser.parse_args()

    database.init_db()

    if args.scan:
        print("🔍 Tarama başlatılıyor...")
        res = run_all_scrapers()
        print(f"✅ Tarama bitti. Taranan: {res['total_found']}, Yeni Eklenen: {res['new_jobs_added']}")

    if args.ce:
        jobs = database.get_jobs(category="computer_engineering")
        print(f"\n💻 BILGISAYAR MÜHENDISLIĞI STAJ ILANLARI ({len(jobs)} Adet):")
        print("="*60)
        for j in jobs:
            print(f"• [{j['platform']}] {j['title']} - {j['company']} ({j['location']})")
            print(f"  Başvuru URL: {j['url']}\n")

    if args.mis:
        jobs = database.get_jobs(category="mis")
        print(f"\n📊 YÖNETIM BILIŞIM SISTEMLERI (YBS) STAJ ILANLARI ({len(jobs)} Adet):")
        print("="*60)
        for j in jobs:
            print(f"• [{j['platform']}] {j['title']} - {j['company']} ({j['location']})")
            print(f"  Başvuru URL: {j['url']}\n")

    if args.stats:
        stats = database.get_stats()
        print("\n📈 STAJ RADAR İSTATİSTİKLERİ:")
        print(f"  - Toplam İlan: {stats['total_jobs']}")
        print(f"  - Bilgisayar Mühendisliği: {stats['ce_jobs']}")
        print(f"  - Yönetim Bilişim Sistemleri: {stats['mis_jobs']}")
        print(f"  - Bugün Eklendi: {stats['today_jobs']}")
        print(f"  - Okunmamış Bildirimler: {stats['unread_notifications']}\n")

    if args.export_csv:
        filename = args.export_csv
        jobs = database.get_jobs(limit=1000)
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Başlık", "Şirket", "Konum", "Platform", "Çalışma Türü", "Kategori", "URL", "Tarih"])
            for j in jobs:
                writer.writerow([j["id"], j["title"], j["company"], j["location"], j["platform"], j["work_type"], j["category"], j["url"], j["created_at"]])
        print(f"✅ İlanlar '{filename}' dosyasına başarıyla dışa aktarıldı!")

    if not any([args.scan, args.ce, args.mis, args.stats, args.export_csv]):
        parser.print_help()

if __name__ == "__main__":
    main()
