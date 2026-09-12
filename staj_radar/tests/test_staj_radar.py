import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        test_job = {
            "title": "Test Yazılım Stajyeri",
            "company": "Unit Test Corp",
            "location": "Ankara",
            "platform": "TestPlatform",
            "url": "https://testcorp.com/job/12345",
            "description": "Test açıklaması"
        }
        job_id, is_new = save_job(test_job)
        self.assertIsNotNone(job_id)
        
        # Verify deduplication
        job_id2, is_new2 = save_job(test_job)
        self.assertFalse(is_new2)
        self.assertEqual(job_id, job_id2)

if __name__ == "__main__":
    unittest.main()
