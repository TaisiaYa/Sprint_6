"""
Базовый класс для всех страниц (Page Object).
Содержит общие методы работы с элементами.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Родительский класс — все остальные страницы наследуются от него."""

    BASE_URL = "https://qa-scooter.praktikum-services.ru/"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        """Открыть главную страницу сайта."""
        self.driver.get(self.BASE_URL)

    def find(self, locator):
        """Дождаться появления элемента и вернуть его."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator):
        """Дождаться кликабельности элемента и вернуть его."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        """Кликнуть по элементу."""
        self.find_clickable(locator).click()

    def type_text(self, locator, text):
        """Ввести текст в поле."""
        field = self.find_clickable(locator)
        field.clear()
        field.send_keys(text)

    def scroll_into_view(self, locator):
        """Прокрутить страницу до элемента."""
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

    def is_visible(self, locator):
        """Проверить, виден ли элемент."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def get_text(self, locator):
        """Получить текст элемента."""
        return self.find(locator).text
