import csv
import time
from sign_up_data import sign_up_data
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select


class TestConduit(object):
    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(service=service, options=options)

        URL = "http://localhost:1667/#/"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        pass
        self.browser.quit()

    # Adatkezelési nyilatkozat használata - cookie-k elfogadása
    def test_apply_privacy_statement_as_cookies(self):
        cookie_accept_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button[class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')))
        cookie_accept_btn.click()
        cookie_panel = self.browser.find_elements(By.ID, 'cookie-policy-panel')
        assert len(cookie_panel) == 0

    # Regisztráció érvényes adatokkal
    def test_sign_up(self):
        sign_up_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/register"]')))
        sign_up_button.click()
        username_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Username"]')))
        username_input.send_keys(sign_up_data[0])
        email_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
        email_input.send_keys(sign_up_data[1])
        password_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
        password_input.send_keys(sign_up_data[2])
        submit_sign_up = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))
        submit_sign_up.click()
        time.sleep(2)
        success_report = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="swal-text"]')))
        assert success_report.text == "Your registration was successful!"
        successful_ok_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="swal-button swal-button--confirm"]')))
        successful_ok_btn.click()

    # Bejelentkezés érvényes adatokkal
    def test_sign_in(self):
        sign_in_header_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/login"]')))
        sign_in_header_button.click()
        sign_in_email_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
        sign_in_email_input.send_keys(sign_up_data[1])
        sign_in_password_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
        sign_in_password_input.send_keys(sign_up_data[2])
        sign_in_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))
        sign_in_btn.click()
        time.sleep(2)
        header_menus = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="nav-link"]')))
        name_text = header_menus[2]
        assert name_text.text == sign_up_data[0]

    # def test_listed_datas(self):
    #     pass
    #
    # def test_navigation_links(self):
    #     pass
    #
    # def test_write_new_data(self):
    #     pass
    #
    # def test_new_data_from_file(self):
    #     pass
    #
    # def test_modify_data(self):
    #     pass
    #
    # def test_delete_data(self):
    #     pass
    #
    # def test_save_data_from_interface(self):
    #     pass
    #
    # def test_sign_out(self):
    #     pass
