from flask import Flask, render_template, jsonify, request, Response
import database
from scrapers.runner import run_all_scrapers
import threading
import time
import csv
import io
import json

app = Flask(__name__)

# Initialize database
database.init_db()

# Seed initial jobs if database is empty (e.g. on fresh Render deployment)
def seed_jobs_if_empty():
    stats = database.get_stats()
    if stats.get("total_jobs", 0) == 0:
        print("🌱 Veritabanı boş, ilk ilan taraması otomatik başlatılıyor...")
        run_all_scrapers()

seed_jobs_if_empty()

# Background Scheduler for Automatic Periodic Scans
def start_background_scheduler(interval_hours=6):
    def scheduler_loop():
        while True:
            time.sleep(interval_hours * 3600)
            print("⏰ Otomatik periyodik tarama başlatılıyor...")
            try:
                run_all_scrapers()
            except Exception as e:
                print(f"Otomatik tarama hatası: {e}")

    thread = threading.Thread(target=scheduler_loop, daemon=True)
    thread.start()

start_background_scheduler(interval_hours=6)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/jobs", methods=["GET"])
def api_get_jobs():
    category = request.args.get("category")
    search = request.args.get("search")
    work_type = request.args.get("work_type")
    status = request.args.get("status")
    platform = request.args.get("platform")
    limit = int(request.args.get("limit", 200))
    offset = int(request.args.get("offset", 0))

    jobs = database.get_jobs(
        category=category,
        search=search,
        work_type=work_type,
        status=status,
        platform=platform,
        limit=limit,
        offset=offset
    )
    return jsonify({"success": True, "count": len(jobs), "jobs": jobs})

# Email-based User Status APIs
@app.route("/api/user/status", methods=["GET", "POST"])
def api_user_status():
    if request.method == "POST":
        data = request.json or {}
        email = data.get("email", "").strip().lower()
        job_id = data.get("job_id")
        status = data.get("status")
        
        if not email or not job_id:
            return jsonify({"success": False, "error": "E-posta ve ilan ID gereklidir."}), 400
            
        database.set_user_job_status(email, job_id, status)
        statuses = database.get_user_job_statuses(email)
        return jsonify({"success": True, "statuses": statuses})
    else:
        email = request.args.get("email", "").strip().lower()
        statuses = database.get_user_job_statuses(email)
        return jsonify({"success": True, "statuses": statuses})

@app.route("/api/notes", methods=["GET", "POST"])
def api_notes():
    if request.method == "POST":
        data = request.json or {}
        author = data.get("author", "Anonim Öğrenci")
        message = data.get("message", "")
        if not message.strip():
            return jsonify({"success": False, "error": "Not içeriği boş olamaz."}), 400
        
        note_id = database.add_note(author, message)
        return jsonify({"success": True, "note_id": note_id})
    else:
        notes = database.get_notes(limit=50)
        return jsonify({"success": True, "notes": notes})

@app.route("/api/jobs/export", methods=["GET"])
def api_export_jobs():
    category = request.args.get("category")
    search = request.args.get("search")
    work_type = request.args.get("work_type")
    fmt = request.args.get("format", "csv").lower()

    jobs = database.get_jobs(category=category, search=search, work_type=work_type, limit=1000)

    if fmt == "json":
        return Response(
            json.dumps(jobs, ensure_ascii=False, indent=2),
            mimetype="application/json",
            headers={"Content-Disposition": "attachment;filename=staj_ilanlari.json"}
        )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "İlan Başlığı", "Şirket", "Şehir/Konum", "Platform", "Çalışma Türü", "Kategori", "Başvuru Linki", "Tarih"])

    for job in jobs:
        writer.writerow([
            job["id"],
            job["title"],
            job["company"],
            job["location"],
            job["platform"],
            job["work_type"],
            job["category"],
            job["url"],
            job["created_at"]
        ])

    return Response(
        output.getvalue().encode('utf-8-sig'),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=staj_ilanlari.csv"}
    )

@app.route("/api/stats", methods=["GET"])
def api_get_stats():
    stats = database.get_stats()
    return jsonify({"success": True, "stats": stats})

@app.route("/api/scan", methods=["POST"])
def api_trigger_scan():
    try:
        res = run_all_scrapers()
        return jsonify({
            "success": True,
            "total_found": res.get("total_found", 0),
            "new_jobs_added": res.get("new_jobs_added", 0),
            "message": f"Tarama tamamlandı! {res.get('new_jobs_added', 0)} yeni ilan bulundu."
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=False)
