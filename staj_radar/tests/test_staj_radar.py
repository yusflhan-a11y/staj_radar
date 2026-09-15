import sys
import os
import unittest
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import database
from database import categorize_job, detect_work_type, save_job, get_jobs, update_job_status

class TestStajRadar(unittest.TestCase):
    def setUp(self):
        database.init_db()

    def test_categorize_job_computer_engineering(self):
        cat = categorize_job("Backend Python Software Developer Intern", "Django ve FastAPI ile yazılım geliştirme stajı.")
        self.assertIn(cat, ["computer_engineering", "both"])

    def test_categorize_job_mis(self):
        cat = categorize_job("İş Analisti Stajyeri", "Jira, Agile ve iş gereksinim analizi.")
        self.assertIn(cat, ["mis", "both"])

    def test_detect_work_type(self):
        wt_remote = detect_work_type("Software Intern", "Uzaktan çalışma imkanı", "İstanbul")
        self.assertEqual(wt_remote, "remote")
        
        wt_hybrid = detect_work_type("Data Intern", "Hibrit düzen haftada 2 gün ofis", "İstanbul")
        self.assertEqual(wt_hybrid, "hybrid")

    def test_save_and_retrieve_job(self):
        unique_url = f"https://sampletech.com/job/{int(time.time() * 1000)}"
        test_job = {
            "title": "Unit Test Yazılım Stajyeri",
            "company": "Sample Unit Company",
            "location": "Ankara",
            "platform": "TestPlatform",
            "url": unique_url,
            "description": "Test açıklaması"
        }
        res = save_job(test_job)
        job_id = res[0]
        is_new = res[1]
        self.assertIsNotNone(job_id)
        self.assertTrue(is_new)
        
        res2 = save_job(test_job)
        job_id2 = res2[0]
        is_new2 = res2[1]
        is_updated2 = res2[2]
        self.assertFalse(is_new2)
        self.assertTrue(is_updated2)
        self.assertEqual(job_id, job_id2)

if __name__ == "__main__":
    unittest.main()
