import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from essential_data import sign_up_data, new_article_data


def sign_in(browser):
    sign_in_header_button = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/login"]')))

    sign_in_header_button.click()

    sign_in_email_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))

    sign_in_email_input.send_keys(sign_up_data[1])

    sign_in_password_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))

    sign_in_password_input.send_keys(sign_up_data[2])

    sign_in_btn = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))

    sign_in_btn.click()

    time.sleep(2)


def make_new_article(browser):
    new_article_btn = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/editor"]')))

    new_article_btn.click()

    article_title_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))

    article_title_input.send_keys(new_article_data['article_title'])

    about_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))

    about_input.send_keys(new_article_data['about'])

    article_body_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))

    article_body_input.send_keys(new_article_data['article'])

    tag_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter tags"]')))

    tag_input.send_keys(new_article_data['tags'])

    publish_article_btn = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg pull-xs-right btn-primary"]')))

    publish_article_btn.click()
