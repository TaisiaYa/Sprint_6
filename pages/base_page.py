import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Открыть главную страницу")
    def open(self):
        self.driver.get(self.BASE_URL)

    @allure.step("Найти элемент")
    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step("Найти кликабельный элемент")
    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Кликнуть по элементу")
    def click(self, locator):
        self.find_clickable(locator).click()

    @allure.step("Ввести текст")
    def type_text(self, locator, text):
        field = self.find_clickable(locator)
        field.clear()
        field.send_keys(text)

    @allure.step("Прокрутить до элемента")
    def scroll_into_view(self, locator):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

    @allure.step("Кликнуть через JS")
    def js_click(self, locator):
        element = self.find_clickable(locator)
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Прокрутить и кликнуть через JS")
    def scroll_and_js_click(self, locator):
        element = self.scroll_into_view(locator)
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Проверить видимость элемента")
    def is_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Получить текст элемента")
    def get_text(self, locator):
        return self.find(locator).text

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Переключиться на новую вкладку")
    def switch_to_new_tab(self):
        original = self.driver.current_window_handle
        self.wait.until(lambda d: len(d.window_handles) > 1)
        new_window = [w for w in self.driver.window_handles if w != original][0]
        self.driver.switch_to.window(new_window)
        self.wait.until(lambda d: d.current_url != "about:blank")
        return self.driver.current_url