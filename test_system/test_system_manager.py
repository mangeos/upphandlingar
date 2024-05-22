
import unittest
from unittest.mock import patch
from xmlrunner import XMLTestRunner
from system_manager import SystemManager

class TestSystemManager(unittest.TestCase):
    def setUp(self):
        self.system_manager = SystemManager()
        self.system_manager.temp = {}

    @patch('testScraping.scraping', return_value=5)
    def test_run_scraping_job_first_run(self, mock_scraping):
        job_name = 'job1'
        self.system_manager.run_scraping_job(job_name)
        self.assertEqual(
            self.system_manager.temp[job_name][0], 5,
            msg=f"Expected first run value 5 for job '{job_name}', but got {self.system_manager.temp[job_name][0]}"
        )

    @patch('testScraping.scraping', return_value=3)
    def test_run_scraping_job_existing_entry_new_value_smaller(self, mock_scraping):
        job_name = 'job1'
        self.system_manager.temp[job_name] = [5]
        self.system_manager.run_scraping_job(job_name)
        self.assertEqual(
            self.system_manager.temp[job_name], [3, 3],
            msg=f"Expected [3, 3] for job '{job_name}' with existing entry 5, but got {self.system_manager.temp[job_name]}"
        )

    @patch('testScraping.scraping', return_value=7)
    def test_run_scraping_job_existing_entry_new_value_larger(self, mock_scraping):
        job_name = 'job1'
        self.system_manager.temp[job_name] = [5]
        self.system_manager.run_scraping_job(job_name)
        self.assertEqual(
            self.system_manager.temp[job_name], [7, 7],
            msg=f"Expected [7, 7] for job '{job_name}' with existing entry 5, but got {self.system_manager.temp[job_name]}"
        )

    @patch('testScraping.scraping', return_value=-1)
    def test_run_scraping_job_new_value_minus_one(self, mock_scraping):
        job_name = 'job1'
        self.system_manager.temp[job_name] = [5]
        self.system_manager.run_scraping_job(job_name)
        self.assertEqual(
            self.system_manager.temp[job_name], [5],
            msg=f"Expected [5] for job '{job_name}' with new value -1, but got {self.system_manager.temp[job_name]}"
        )

    def tearDown(self):
        self.system_manager.stop_schedule()

if __name__ == '__main__':
    unittest.main(testRunner=XMLTestRunner(output='test-reports'))
