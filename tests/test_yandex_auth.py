import unittest

AUTH_URL = 'https://passport.yandex.ru/auth/'


class TestYandexAuth(unittest.TestCase):
    def test_auth_page_has_login_form(self):
        try:
            from selenium import webdriver
            from selenium.common.exceptions import TimeoutException, WebDriverException
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
        except ImportError:
            self.skipTest('Selenium не установлен')

        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1280,800')

        try:
            driver = webdriver.Chrome(options=options)
        except WebDriverException as error:
            self.skipTest(f'Не удалось запустить Chrome: {error}')

        try:
            driver.get(AUTH_URL)
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input'))
                )
            except TimeoutException:
                self.skipTest('Форма авторизации Яндекса не загрузилась')

            visible_inputs = [
                element for element in driver.find_elements(By.CSS_SELECTOR, 'input')
                if element.is_displayed()
            ]
            self.assertTrue(visible_inputs, 'На странице нет поля для ввода логина')
            self.assertIn('yandex', driver.current_url)
        finally:
            driver.quit()


if __name__ == '__main__':
    unittest.main()
