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
        tasks_to_add = ["Task A", "Task B", "Task C"]
        for task in tasks_to_add:
            self.driver.get(self.base_url)
            self.driver.find_element(By.NAME, "task").send_keys(task)
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            time.sleep(0.5)
    
        task_elements = self.driver.find_elements(By.CLASS_NAME, "list-group-item")
        task_texts = [task.text for task in task_elements]
        for task in tasks_to_add:
            assert any(task in text for text in task_texts)


    def test_5_delete_task(self):
        self.driver.get(self.base_url)
        self.add_task("Delete Me")
    
        delete_button = self.driver.find_element(By.LINK_TEXT, "Delete")
        delete_button.click()
    
        # Accept the confirmation dialog
        alert = self.driver.switch_to.alert
        alert.accept()
    
        time.sleep(1)
        tasks = self.driver.find_elements(By.CLASS_NAME, "list-group-item")
        assert all("Delete Me" not in task.text for task in tasks)


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
        self.driver.get(self.base_url)
        delete_links = self.driver.find_elements(By.LINK_TEXT, "Delete")
        for link in delete_links:
            link.click()
            alert = self.driver.switch_to.alert
            alert.accept()
            time.sleep(0.5)
    
        self.driver.get(self.base_url)
        message = self.driver.find_element(By.CLASS_NAME, "alert-info").text
        assert "No tasks yet" in message


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
