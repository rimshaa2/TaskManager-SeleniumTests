from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import unittest

# Replace with your deployed application URL
URL = "http://16.16.28.38:8081/"

class TaskManagerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get(URL)

    def test_1_page_load(self):
        self.assertIn("Task Manager", self.driver.title)

    def test_2_add_task(self):
        self.driver.find_element(By.NAME, "task").send_keys("Test Task 1")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.assertIn("Test Task 1", self.driver.page_source)

    def test_3_add_empty_task(self):
        self.driver.find_element(By.NAME, "task").send_keys("")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.assertNotIn("<li class=\"list-group-item\"", self.driver.page_source)

    def test_4_add_multiple_tasks(self):
        for i in range(3):
            self.driver.find_element(By.NAME, "task").send_keys(f"Task {i}")
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        page = self.driver.page_source
        self.assertIn("Task 0", page)
        self.assertIn("Task 1", page)
        self.assertIn("Task 2", page)

    def test_5_delete_task(self):
        self.driver.find_element(By.NAME, "task").send_keys("Delete Me")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.driver.find_element(By.LINK_TEXT, "Delete").click()
        time.sleep(1)
        self.assertNotIn("Delete Me", self.driver.page_source)

    def test_6_persistence(self):
        self.driver.find_element(By.NAME, "task").send_keys("Persistent Task")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.driver.refresh()
        self.assertIn("Persistent Task", self.driver.page_source)

    def test_7_xss_protection(self):
        xss = "<script>alert('xss')</script>"
        self.driver.find_element(By.NAME, "task").send_keys(xss)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.assertNotIn(xss, self.driver.page_source)

    def test_8_empty_state_message(self):
        if "Delete" in self.driver.page_source:
            delete_buttons = self.driver.find_elements(By.LINK_TEXT, "Delete")
            for button in delete_buttons:
                button.click()
                time.sleep(0.5)
        self.assertIn("No tasks yet", self.driver.page_source)

    def test_9_add_button_present(self):
        btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.assertEqual(btn.text.strip(), "Add Task")

    def test_10_delete_buttons_present(self):
        self.driver.find_element(By.NAME, "task").send_keys("Delete Button Check")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        delete_buttons = self.driver.find_elements(By.LINK_TEXT, "Delete")
        self.assertGreater(len(delete_buttons), 0)

if __name__ == '__main__':
    unittest.main()
