import time
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
        options.add_argument('window-position=-1000,0')
        self.browser = webdriver.Chrome(service=service, options=options)

        URL = "http://localhost:1667/#/"
        self.browser.get(URL)
        self.browser.maximize_window()
    def teardown_method(self):
        self.browser.quit()

    def test_sign_up(self):
        sign_up_button = self.browser.find_elements(By.CLASS_NAME, 'nav-link')[0]
        sign_up_button.click()

    # def test_sign_in(self):
    #     pass
    #
    # def test_apply_privacy_statement(self):
    #     pass
    #
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

