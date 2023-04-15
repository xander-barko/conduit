import csv
import time
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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
        self.browser.quit()


    # Adatkezelési nyilatkozat használata - Cookie-k elfogadása
    def test_apply_privacy_statement_as_cookies(self):

        # Megkeresem azt az elemet (gombot), amellyel elfogadom a cookie-kat, majd rákattintok.
        cookie_accept_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button[class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')))

        cookie_accept_btn.click()

        time.sleep(2)

        # Ellenőrzöm, hogy az elfogadást, illetve elutasítást tartalmazó panel eltűnik, elemeinek száma 0.
        assert len(self.browser.find_elements(By.ID, 'cookie-policy-panel')) == 0


    # Regisztráció - Érvényes adatokkal
    def test_sign_up(self):

        # Megkeresem, majd rákattintok a regisztráció gombjára.
        sign_up_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/register"]')))

        sign_up_button.click()

        # Megkeresem a kitöltendő beviteli mezőket és az adatokat importálva kitöltöm azokat.
        username_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Username"]')))

        username_input.send_keys(sign_up_data[0])

        email_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))

        email_input.send_keys(sign_up_data[1])

        password_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))

        password_input.send_keys(sign_up_data[2])

        # Megkeresem és rákattintok a regisztráció beküldése gombra.
        submit_sign_up = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))

        submit_sign_up.click()

        time.sleep(2)

        # Kikeresve a sikeres regisztráció paneljét, igazolom, hogy az annak megfelelő szöveget kapom visszajelzésként.
        success_report = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="swal-text"]')))

        assert success_report.text == "Your registration was successful!"

        time.sleep(2)

        # Az "OK" gombbal visszatérek a főoldalra, bejelentkezve.
        successful_ok_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="swal-button swal-button--confirm"]')))

        successful_ok_btn.click()


    # Bejelentkezés - Érvényes adatokkal
    def test_sign_in(self):

        # Megkeresem, majd rákattintok a bejelentkezés gombjára.
        sign_in_header_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/login"]')))

        sign_in_header_button.click()

        # Megkeresem a kitöltendő beviteli mezőket és az adatokat importálva kitöltöm azokat.
        sign_in_email_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))

        sign_in_email_input.send_keys(sign_up_data[1])

        sign_in_password_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))

        sign_in_password_input.send_keys(sign_up_data[2])

        # Megkeresem és rákattintok a bejelentkezés gombra.
        sign_in_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))

        sign_in_btn.click()

        time.sleep(2)

        # Megkeresem és egy külön változóba elmentve hasonlítom össze
        # a külső forrásból hivatkozott nevet a fejléc menüjében megjelent névvel.
        header_menus = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="nav-link"]')))

        name_text = header_menus[2]

        assert name_text.text == sign_up_data[0]


    # Adatok listázása - Global Feed cikkek címeinek listázása bejelentkezés után
    def test_listed_datas(self):

        # Bejelentkezés segédfüggvénnyel
        sign_in(self.browser)

        # Megkeresem a "Global Feed" cikkeit tartalmazó elemet, és azon belül is a cikkek címeire hivatkozom.
        global_feed_data = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//h1')))[1::]

        # Elmentem egy listába ezeket a címeket (.text) és ellenőrzöm, hogy a listám nem üres,
        # tehát a benne található elemek száma nem nulla.
        global_feed_list = []
        for feed in global_feed_data:
            global_feed_list.append(feed.text)
        print(global_feed_list)

        assert len(global_feed_list) != 0


    # Több oldalas lista bejárása - A Global feed oldalainak bejárása
    def test_navigation_links(self):

        # Bejelentkezés segédfüggvénnyel
        sign_in(self.browser)

        # Megkeresem és kiválasztom a kattintható navigációs linkek listáját.
        pagination_btns = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="page-link"]')))

        # Végigiterálok az oldalakon, miközben ciklusonként ellenőrzöm,
        # hogy a különböző attribútumok megkapják-e az aktív állapotot
        # és megegyezik-e az adott oldal száma az éppen aktuális ciklus sorszámával.
        page_counter = 0
        for page_button in pagination_btns:
            page_button.click()
            active_item = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//li[@class="page-item active"]')))
            assert 'active' in active_item.get_attribute('class')
            page_counter += 1
            assert int(active_item.text) == page_counter
            assert int(page_button.text) == page_counter

        # Végül egy változó segítségével ellenőrzöm az összes oldal számát,
        # ezt összehasonlítom az iterációk számával, mely két számnak egyeznie kell.
        all_pages_number = len(pagination_btns)

        assert all_pages_number == page_counter


    # Új adat bevitele - Egy új komment és egy új cikk létrehozása
    def test_write_new_data(self):

        # Bejelentkezés segédfüggvénnyel
        sign_in(self.browser)

        # Megkeresem azt a cikket, amihez kommentet szeretnék fűzni, majd rákattintok.
        commented_article = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//h1')))[1]

        commented_article.click()

        # Megkeresem a beviteli mezőt, majd importálom az adatot, amit kommentként szeretnék használni.
        comment_area = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Write a comment..."]')))

        comment_area.send_keys(comment_data)

        # Megkeresem a komment beküldésére alkalmas gombot és rá is kattintok.
        post_comment_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-sm btn-primary"]')))

        post_comment_btn.click()

        # Megkeresem az új komment elemet, és annak szövegét összehasonlítom a külső import fájlban lévő releváns szöveggel.
        new_comment_text = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//p[@class="card-text"]')))

        assert new_comment_text.text == comment_data

        # Megkeresem a fejlécben a menüpontot új cikk létrehozásához és rákkatintok.
        new_article_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/editor"]')))

        new_article_btn.click()

        # Megkeresem a kitöltendő beviteli mezőket és az adatokat importálva kitöltöm azokat.
        article_title_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))

        article_title_input.send_keys(new_article_data['article_title'])

        about_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))

        about_input.send_keys(new_article_data['about'])

        article_body_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))

        article_body_input.send_keys(new_article_data['article'])

        tag_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter tags"]')))

        tag_input.send_keys(new_article_data['tags'])

        # Megkeresem az új cikk beküldésére alkalmas gombot és rá is kattintok.
        publish_article_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg pull-xs-right btn-primary"]')))

        publish_article_btn.click()

        # Ellenőrzöm, hogy az új cikk címe megjelenik-e és egyezik-e a külső fájlból importált címmel.
        new_published_article = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1')))

        assert new_published_article.is_displayed()
        assert new_published_article.text == new_article_data['article_title']


    # Ismételt és sorozatos adatbevitel adatforrásból - Három új cikk létrehozása csv fájlból
    def test_new_data_from_file_constantly(self):

        # Bejelentkezés segédfüggvénnyel
        sign_in(self.browser)

        # Előzetesen létrehozok egy .csv fájlt, a kívánt adatokkal, majd előkészítem ezeket beolvasásra, kihagyva a fájl első sorát.
        with open('test/input_transfer.csv', 'r', encoding='UTF-8') as articles:
            article_reader = csv.reader(articles, delimiter=',')
            next(article_reader)

            # Megkeresem a kitöltendő beviteli mezőket és az adatokat importálva kitöltöm azokat minden iteráció alkalmával.
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

                # Ellenőrzöm minden iteráció során, hogy az új cikk címe megjelenik-e és egyezik-e a külső fájlból importált címmel.
                assert new_published_article.is_displayed()
                assert new_published_article.text == article[0]

                time.sleep(1)

    # Meglévő adat módosítása
    def test_modify_data(self):

        # Bejelentkezés segédfüggvénnyel
        sign_in(self.browser)

        # Megkeresem és rákattintok a beállítások gombra a profilom módosításához.
        profile_settings_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/settings"]')))
        profile_settings_btn.click()

        # Megkeresek minden módosítani kívánt beviteli mezőt, kitörlöm azok addig tartalmát, és importálom az új adatokat külső fájból.
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

        # Kikeresve a sikeres módosítás paneljét, igazolom, hogy az annak megfelelő szöveget kapom visszajelzésként.
        update_success_report = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="swal-title"]')))

        assert update_success_report.text == "Update successful!"

        # Az "OK" gombot megnyomva visszatérünk az oldalra.
        successful_ok_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="swal-button swal-button--confirm"]')))
        successful_ok_btn.click()

    # Adat vagy adatok törlése - saját cikk törlése
    def test_delete_data(self):

        # Bejelentkezés segédfüggvénnyel
        sign_in(self.browser)

        # Új cikk létrehozása segédfüggvénnyel
        make_new_article(self.browser)

        # Megkeresem a törlésre vonatkozó funkció gombját.
        delete_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-outline-danger btn-sm"]')))

        # Ellenőrzöm, hogy a gomb elérhető-e.
        assert delete_btn.is_displayed

        # Rákattintok a törlés gombra.
        delete_btn.click()

        time.sleep(2)

        # Ellenőrzöm, hogy az aktuális url cím az az elvárt is egyben.
        assert self.browser.current_url == 'http://localhost:1667/#/'

        # Megkeresem a cikkek listáját és ellenőrzöm, hogy a korábban felvitt cikk címe már nem található a cikkek listájában.
        global_feed_list = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="home-global"]')))

        assert not new_article_data['article_title'] in global_feed_list


    # Adatok lementése felületről
    def test_save_data(self):

        # Bejelentkezés segédfüggvénnyel
        sign_in(self.browser)

        # Megkeresem a szerzők neveit tartalmazó elemek listáját.
        authors = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="author"]')))

        # Létrehozok egy .csv kiterjesztésű fájlt, majd végigiterálva a szerzőkön beleírom azokat ebbe a fájlba, mindegyiket új sorba.
        with open('saved_data.csv', 'w', encoding='UTF-8', newline='') as author_saved:
            author_writer = csv.writer(author_saved, delimiter=';')
            for author in authors:
                author_writer.writerow([author.text])

        # Kiolvasom a létrehozott .csv fájból az adatokat, majd ezeken végigiterálva egy listába mentem azokat.
        # Ennek a listának a hosszát hasonlítom össze a DOM-ban kiválasztott lista elemeinek a számával.
        name_of_authors = []
        with open('saved_data.csv', 'r', encoding='UTF-8') as read_authors:
            author_reader = csv.reader(read_authors, delimiter=';')
            for author in author_reader:
                name_of_authors.append(author)

        assert len(name_of_authors) == len(authors)

    # Kijelentkezés
    def test_sign_out(self):

        # Bejelentkezés segédfüggvénnyel
        sign_in(self.browser)

        # Megkeresem a kijelentkezés gomb elérési útját, létrehozok egy változót a kijelentkezés előtti menüpontok számával
        # és rákattintok a kijelentkezés gombra.
        log_out_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[@class="nav-item"]')))[4]

        number_of_logged_in_menu_items = len(self.browser.find_elements(By.XPATH, '//li[@class="nav-item"]'))

        log_out_btn.click()

        time.sleep(2)

        # Ellenőrzöm, hogy a menüpontok száma kijelentkezés után kevesebb, mint bejelentkezve,
        # és azt is, hogy ez a szám, ebben az esetben, mennyi pontosan(4)
        assert len(self.browser.find_elements(By.XPATH, '//li[@class="nav-item"]')) < number_of_logged_in_menu_items
        assert len(self.browser.find_elements(By.XPATH, '//li[@class="nav-item"]')) == 4

        # Létrehozok egy "kivételt", ami a kijelentkezés utáni kijelentkezés gombra való kattintás elérhetetlenségét hivatott kezelni
        with pytest.raises(Exception) as e_info:
            log_out_btn.click()
