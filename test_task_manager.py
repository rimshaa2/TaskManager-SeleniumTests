import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class TaskManagerTest(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.base_url = "http://16.16.28.38:8081"  # Change this to your actual deployed URL or port

    def tearDown(self):
        self.driver.quit()

    def test_1_page_loads(self):
        self.driver.get(self.base_url)
        self.assertIn("Task Manager", self.driver.title)

    def test_2_add_task(self):
        self.driver.get(self.base_url)
        task_input = self.driver.find_element(By.NAME, "task")
        task_input.send_keys("Test Task 1")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        tasks = self.driver.find_elements(By.CLASS_NAME, "list-group-item")
        self.assertTrue(any("Test Task 1" in task.text for task in tasks))

    def test_3_add_second_task(self):
        self.driver.get(self.base_url)
        task_input = self.driver.find_element(By.NAME, "task")
        task_input.send_keys("Test Task 2")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        tasks = self.driver.find_elements(By.CLASS_NAME, "list-group-item")
        self.assertTrue(any("Test Task 2" in task.text for task in tasks))

    def test_4_add_multiple_tasks(self):
        self.driver.get(self.base_url)
        for i in range(3, 6):
            task_input = self.driver.find_element(By.NAME, "task")
            task_input.send_keys(f"Task {i}")
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            time.sleep(0.5)
        tasks = self.driver.find_elements(By.CLASS_NAME, "list-group-item")
        self.assertGreaterEqual(len(tasks), 3)

    def test_5_delete_task(self):
        self.driver.get(self.base_url)
        initial_tasks = self.driver.find_elements(By.CLASS_NAME, "list-group-item")
        if initial_tasks:
            self.driver.find_element(By.LINK_TEXT, "Delete").click()
            alert = self.driver.switch_to.alert
            alert.accept()
            time.sleep(1)
            new_tasks = self.driver.find_elements(By.CLASS_NAME, "list-group-item")
            self.assertLess(len(new_tasks), len(initial_tasks))

    def test_6_required_field(self):
        self.driver.get(self.base_url)
        submit = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit.click()
        time.sleep(0.5)
        alert = self.driver.find_element(By.NAME, "task").get_attribute("validationMessage")
        self.assertTrue("fill out" in alert.lower())

    def test_7_page_responsive(self):
        self.driver.set_window_size(375, 667)  # iPhone 6/7/8
        self.driver.get(self.base_url)
        header = self.driver.find_element(By.CLASS_NAME, "card-header")
        self.assertTrue(header.is_displayed())

    def test_8_empty_state_message(self):
        self.driver.get(self.base_url)
        while True:
            delete_buttons = self.driver.find_elements(By.LINK_TEXT, "Delete")
            if not delete_buttons:
                break
            delete_buttons[0].click()
            alert = self.driver.switch_to.alert
            alert.accept()
            time.sleep(0.5)
        self.driver.get(self.base_url)
        message = self.driver.find_element(By.CLASS_NAME, "alert-info").text
        self.assertIn("No tasks yet", message)

    def test_9_xss_injection_protection(self):
        self.driver.get(self.base_url)
        script = '<script>alert("XSS")</script>'
        self.driver.find_element(By.NAME, "task").send_keys(script)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        page_source = self.driver.page_source
        self.assertNotIn(script, page_source)

    def test_10_ui_elements_present(self):
        self.driver.get(self.base_url)
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "card"))
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "btn-success"))

if __name__ == "__main__":
    unittest.main()
