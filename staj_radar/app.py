import os
import sys
from flask import Flask, render_template, request, jsonify, Response
import csv
import io
import threading
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import database
from config import SCAN_INTERVAL_SECONDS
from scrapers.runner import run_all_scrapers

app = Flask(__name__)

# Automated Background Scheduler (Runs scan every 6 hours and on startup)
def start_scheduler():
    def loop():
        # Startup scan after 5 seconds
        time.sleep(5)
        try:
            print("[Scheduler] Sunucu başlangıç staj taraması çalıştırılıyor...")
            run_all_scrapers()
        except Exception as e:
            print(f"[Scheduler Startup] Hata: {e}")

        # Recurring 6-hour loop
        while True:
            time.sleep(SCAN_INTERVAL_SECONDS)
            try:
                print("[Scheduler] Otomatik 6 saatlik staj taraması başlatılıyor...")
                run_all_scrapers()
            except Exception as e:
                print(f"[Scheduler Loop] Hata: {e}")

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()

# Local use keeps the convenient in-process scheduler. In production an
# external scheduler calls /api/scan, so a sleeping/restarted web process does
# not silently stop the six-hour refresh cycle.
if os.environ.get("ENABLE_IN_PROCESS_SCHEDULER", "").lower() in {"1", "true", "yes"} or os.environ.get("RENDER_SERVICE_TYPE") != "web":
    start_scheduler()

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
    limit = int(request.args.get("limit", 100))
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
    return jsonify({"status": "success", "jobs": jobs, "count": len(jobs)})

@app.route("/api/user/status", methods=["GET", "POST"])
def api_user_status():
    if request.method == "POST":
        data = request.json or {}
        email = data.get("email", "").strip().lower()
        job_id = data.get("job_id")
        status = data.get("status")

        if not email or not job_id:
            return jsonify({"status": "error", "message": "E-posta adresi ve İlan ID gereklidir."}), 400

        database.set_user_job_status(email, job_id, status)
        return jsonify({"status": "success", "message": "İlan durumu başarıyla güncellendi."})

    else:
        email = request.args.get("email", "").strip().lower()
        if not email:
            return jsonify({"status": "success", "statuses": {}})
        statuses = database.get_user_job_statuses(email)
        return jsonify({"status": "success", "statuses": statuses})

@app.route("/api/notes", methods=["GET", "POST"])
def api_notes():
    if request.method == "POST":
        data = request.json or {}
        author = data.get("author", "Anonim").strip()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"status": "error", "message": "Not mesajı boş olamaz."}), 400

        note_id = database.add_note(author, message)
        return jsonify({"status": "success", "note_id": note_id, "message": "Not panoya eklendi."})
    else:
        notes = database.get_notes(limit=50)
        return jsonify({"status": "success", "notes": notes})

@app.route("/api/notifications", methods=["GET", "POST"])
def api_notifications():
    if request.method == "POST":
        database.mark_notifications_read()
        return jsonify({"status": "success", "message": "Tüm bildirimler okundu."})
    else:
        notifications = database.get_notifications(limit=50)
        unread_count = database.get_unread_notification_count()
        return jsonify({"status": "success", "notifications": notifications, "unread_count": unread_count})

@app.route("/api/stats", methods=["GET"])
def api_stats():
    stats = database.get_stats()
    return jsonify({"status": "success", "stats": stats})

@app.route("/api/scan", methods=["POST"])
def api_scan():
    def run_scan():
        run_all_scrapers()

    thread = threading.Thread(target=run_scan)
    thread.start()
    return jsonify({"status": "success", "message": "Staj ilanı taraması arka planda başlatıldı."})

@app.route("/api/jobs/export", methods=["GET"])
def api_export_jobs():
    category = request.args.get("category")
    jobs = database.get_jobs(category=category, limit=500)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Başlık", "Şirket", "Konum", "Platform", "Kategori", "Çalışma Tipi", "Doğrudan Başvuru Linki", "Ekleme Tarihi"])

    for job in jobs:
        writer.writerow([
            job["id"],
            job["title"],
            job["company"],
            job["location"],
            job["platform"],
            job["category"],
            job["work_type"],
            job["url"],
            job["created_at"]
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=staj_ilanlari_export.csv"}
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
