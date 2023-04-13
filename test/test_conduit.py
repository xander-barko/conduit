import csv
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

from essential_data import *
from functions_to_import import *


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

        assert len(self.browser.find_elements(By.ID, 'cookie-policy-panel')) == 0

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

    # Adatok listázása - Global Feed cikkek címeinek listázása bejelentkezés után
    def test_listed_datas(self):
        sign_in(self.browser)

        global_feed_data = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//h1')))[1::]

        global_feed_list = []
        for feed in global_feed_data:
            global_feed_list.append(feed.text)
        print(global_feed_list)

        assert len(global_feed_list) != 0

    # Több oldalas lista bejárása - A Global feed oldalainak bejárása
    def test_navigation_links(self):
        sign_in(self.browser)

        pagination_btns = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="page-link"]')))

        page_counter = 0
        for page_button in pagination_btns:
            page_button.click()
            page_counter += 1

        all_pages_number = len(pagination_btns)

        assert all_pages_number == page_counter

    # Új adat bevitele
    def test_write_new_data(self):
        sign_in(self.browser)

        new_article_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/editor"]')))
        new_article_btn.click()

        article_title_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))
        article_title_input.send_keys(new_article_data['article_title'])

        about_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))
        about_input.send_keys(new_article_data['about'])

        article_body_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))
        article_body_input.send_keys(new_article_data['article'])

        tag_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter tags"]')))
        tag_input.send_keys(new_article_data['tags'])

        publish_article_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg pull-xs-right btn-primary"]')))
        publish_article_btn.click()

        new_published_article = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1')))

        assert new_published_article.text == new_article_data['article_title']

    # Ismételt és sorozatos adatbevitel adatforrásból
    def test_new_data_from_file_constantly(self):
        sign_in(self.browser)

        with open('test/input_transfer.csv', 'r', encoding='UTF-8') as articles:
            article_reader = csv.reader(articles, delimiter=',')
            next(article_reader)

            for article in article_reader:
                new_article_btn = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/editor"]')))
                new_article_btn.click()

                article_title_input = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))

                about_input = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))

                article_body_input = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))

                tag_input = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter tags"]')))

                publish_article_btn = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//button[@class="btn btn-lg pull-xs-right btn-primary"]')))

                article_title_input.send_keys(article[0])
                about_input.send_keys(article[1])
                article_body_input.send_keys(article[2])
                tag_input.send_keys(article[3])

                publish_article_btn.click()
                new_published_article = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'h1')))
                assert new_published_article.text == article[0]
                time.sleep(1)

    # Meglévő adat módosítása
    def test_modify_data(self):
        sign_in(self.browser)

        profile_settings_btn = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/settings"]')))
        profile_settings_btn.click()

        image_url_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="URL of profile picture"]')))
        bio_text_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[placeholder="Short bio about you"]')))
        password_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
        update_settings_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))

        image_url_input.clear()
        bio_text_input.clear()
        password_input.clear()

        image_url_input.send_keys(modify_profile[0])
        bio_text_input.send_keys(modify_profile[1])
        password_input.send_keys(modify_profile[2])
        update_settings_btn.click()

        update_success_report = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="swal-title"]')))

        assert update_success_report.text == "Update successful!"

        successful_ok_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="swal-button swal-button--confirm"]')))
        successful_ok_btn.click()


    # Adat vagy adatok törlése
    # def test_delete_data(self):
    #     pass
    #
    # Adatok lementése felületről
    # def test_save_data(self):
    #     pass
    #
    # Kijelentkezés
    def test_sign_out(self):
        sign_in(self.browser)

        log_out_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[@class="nav-item"]')))[4]
        # assert len(self.browser.find_elements(By.XPATH, '//li[@class="nav-item"]')) == 7
        log_out_btn.click()
        time.sleep(2)
        assert len(self.browser.find_elements(By.XPATH, '//li[@class="nav-item"]')) == 4
        # assert not log_out_btn.is_enabled()
