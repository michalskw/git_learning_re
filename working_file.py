# Import webdivera z biblioteki selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import unittest
import time

# DANE TESTOWE
valid_name = "Zygfryd"
valid_lastname = "Kowalski"
valid_gender = "male"
valid_country_code = "+355"
invalid_phone_number = "123123123"
valid_email = "ofertydlams@gmail.com"
valid_password = "Babajaga321"
valid_country = "Albania"

invalid_phone_number = "abc"
#...

class WizzairRegistration(unittest.TestCase):
    def setUp(self):
        """ Warunki wstępne """
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://wizzair.com/pl-pl#/")

    def tearDown(self):
        """ Porządki po teście """
        self.driver.quit()


    def testInvalidTelephone(self):
        # KROKI
        # KROK: 1. KLIKNIJ "ZALOGUJ SIĘ"
        # LOKALIZOWANIE ELEMENTU
        # SKOPIOWANY CSS SELECTOR
        # #app > div > header > div.header__inner > div > nav > ul > li:nth-child(6) > button
        # SKOPIOWANY FULL XPATH
        # /html/body/div[2]/div/header/div[1]/div/nav/ul/li[6]/button
        # SKOPIOWANY XPATH
        # //*[@id="app"]/div/header/div[1]/div/nav/ul/li[6]/button
        # NAPISANY CSS SELECTOR
        # button[data-test="navigation-menu-signin"]
        driver = self.driver
        # Ustawienie : bezwarunkowy (maksymalny) czas oczekiwania na elementy
        driver.implicitly_wait(60)
        # Wywołanie metody find_elemet_by na obiekcie klasy WebDriver
        # Metoda zwraca WebElement (zaloguj_btn będzie klasy WebElement)
        zaloguj_btn = driver.find_element_by_css_selector('button[data-test="navigation-menu-signin"]')
        # Kliknij w element
        zaloguj_btn.click()
        # KROK:  2. Kliknij Rejestracja
        driver.find_element_by_xpath('//button[@data-test="registration"]').click()
        # KROK: 3. Wpisz imię
        name_input = driver.find_element_by_name("firstName")
        name_input.send_keys(valid_name)
        # KROK: 4. Wpisz nazwisko
        lastname_input = driver.find_element_by_name("lastName")
        lastname_input.send_keys(valid_lastname)
        actions = ActionChains(driver)
        # KROK: 5. Wybierz płeć
        if valid_gender == "female":
            female = driver.find_element_by_xpath('//label[@data-test="register-genderfemale"]')
            actions.move_to_element_with_offset(female, -200, 200)
            actions.click()
            actions.perform()
        else:
            male = driver.find_element_by_xpath('//label[@data-test="register-gendermale"]')
            actions.move_to_element_with_offset(male, 200, 200)
            actions.click()
            actions.perform()
        # KROK: 6. Wpisz kod kraju
        driver.find_element_by_xpath('//div[@data-test="booking-register-country-code"]').click()
        cc_input = driver.find_element_by_name('phone-number-country-code')
        cc_input.send_keys(valid_country_code, Keys.RETURN)
        # KROK: 7. Wpisz niepoprawny numer telefonu
        driver.find_element_by_name('phoneNumberValidDigits').send_keys(invalid_phone_number)
        # KROK: 8. Wpisz poprawny e-mail
        driver.find_element_by_name('email').send_keys(valid_email)
        # KROK: 9. Wpisz hasło
        driver.find_element_by_name('password').send_keys(valid_password)
        # KROK: 10. Wybierz narodowość
        nationality_input = driver.find_element_by_name('country-select')
        nationality_input.click()
        # countries - lista WebElementów
        countries = driver.find_elements_by_xpath('//div[@class="register-form__country-container__locations"]/label')
        for label in countries:
            # Szukaj wewnątrz elementu label
            country = label.find_element_by_tag_name("strong")
            if country.get_attribute("textContent") == valid_country:
                # Przewiń do wybranego kraju
                country.location_once_scrolled_into_view
                # Kliknij w niego
                country.click()
                # Nie szukaj dalej
                break
        time.sleep(10)

        #### UWAGA! (DOPIERO) TERAZ BĘDZIE TEST !!!! ####
        error_messages = driver.find_elements_by_xpath('//span[@class="input-error__message"]/span')
        # Pusta lista na widoczne błędy
        visible_error_messages = []
        # Sprawdżmy, które błędy są widoczne
        for error in error_messages:
            # Sprawdzamy, czy błąd jest widoczny
            if error.is_displayed():
                # jeśli tak, to dodajemy go do listy widocznych błędów
                visible_error_messages.append(error)
        # SPRAWDZAMY, CZY JEST WIDOCZNY TYLKO JEDEN BŁĄD
        print(len(visible_error_messages))
        for v in visible_error_messages:
            print(v.text)
        assert len(visible_error_messages) == 1 # "Czysty" Python
        # self.asserEqual(len(visible_error_messages), 1) # unittest
        # SPRAWDZAMY TREŚĆ TEGO BŁĘDU
        # assert visible_error_messages[0].text == "Nieprawidłowy numer telefonu"
        self.assertEqual(visible_error_messages[0].text, "Please add a valid mobile phone number")

if __name__ == "__main__":
    # Uruchomienie testów
    unittest.main(verbosity=2)
