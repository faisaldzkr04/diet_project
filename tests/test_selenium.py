# tests/test_selenium.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest

class FoodAppSeleniumTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()  # Pastikan chromedriver sesuai path
        self.browser.implicitly_wait(5)  # Sebagai fallback
        self.wait = WebDriverWait(self.browser, 10)

    def test_user_page_form_input(self):
        self.browser.get("http://localhost:8000/user/")

        self.wait.until(EC.presence_of_element_located((By.NAME, "age"))).send_keys("22")
        self.browser.find_element(By.NAME, "weight").send_keys("60")
        self.browser.find_element(By.NAME, "height").send_keys("170")

        gender_select = Select(self.browser.find_element(By.NAME, "gender"))
        gender_select.select_by_visible_text("Laki-laki")

        activity_select = Select(self.browser.find_element(By.NAME, "activity"))
        activity_select.select_by_value("1.55")  # pilih 'Sedang (3-5x per minggu)'

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "form button[type='submit']")
        submit_button.click()

        # Tunggu sampai ada teks "Hasil BMI" muncul di halaman, sebagai indikasi hasil sudah tampil
        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Hasil BMI"))

        # Cek apakah hasil memang muncul
        self.assertIn("Hasil BMI", self.browser.page_source)

    def tearDown(self):
        self.browser.quit()
