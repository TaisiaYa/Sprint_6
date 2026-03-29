"""
Page Object для главной страницы сервиса «Самокат».
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pages.base_page import BasePage


class MainPage(BasePage):
    """Главная страница qa-scooter.praktikum-services.ru"""

    # Кнопки «Заказать» — используем contains() на случай если текст в дочернем теге
    ORDER_BUTTON_TOP = (By.XPATH, "(//button[contains(., 'Заказать')])[1]")
    ORDER_BUTTON_BOTTOM = (By.XPATH, "(//button[contains(., 'Заказать')])[2]")

    # Логотипы
    LOGO_SAMOKAT = (By.XPATH, "//a[contains(@class,'Header_LogoScooter')]")
    LOGO_YANDEX = (By.XPATH, "//a[contains(@class,'Header_LogoYandex')]")

    # Кнопка закрытия баннера с куками
    COOKIE_BUTTON = (By.XPATH, "//button[contains(., 'да все привыкли')]")

    # FAQ: заголовок и панель N-го вопроса (N от 0 до 7)
    def faq_heading(self, index):
        return (By.XPATH, f"//div[@id='accordion__heading-{index}']")

    def faq_panel(self, index):
        return (By.XPATH, f"//div[@id='accordion__panel-{index}']")


    # --- Методы ---

    def open(self):
        """Открыть главную страницу и закрыть баннер куков если появится."""
        self.driver.get(self.BASE_URL)
        self._dismiss_cookies()

    def _dismiss_cookies(self):
        """Закрыть баннер куков если он появился."""
        try:
            btn = WebDriverWait(self.driver, 4).until(
                EC.element_to_be_clickable(self.COOKIE_BUTTON)
            )
            btn.click()
        except Exception:
            pass  # Баннер не появился — всё нормально

    def click_order_top(self):
        """Нажать кнопку «Заказать» вверху страницы."""
        self.click(self.ORDER_BUTTON_TOP)

    def click_order_bottom(self):
        """Прокрутить до нижней кнопки «Заказать» и кликнуть через JS
        (хедер sticky перекрывает кнопку при обычном клике)."""
        element = self.scroll_into_view(self.ORDER_BUTTON_BOTTOM)
        self.driver.execute_script("arguments[0].click();", element)

    def click_faq_question(self, index):
        """Прокрутить до вопроса FAQ и кликнуть через JS (обходит перекрытие картинкой)."""
        heading_locator = self.faq_heading(index)
        element = self.scroll_into_view(heading_locator)
        self.driver.execute_script("arguments[0].click();", element)

    def get_faq_answer_text(self, index):
        """Получить текст ответа на вопрос FAQ (ждём пока панель раскроется)."""
        panel_locator = self.faq_panel(index)
        panel = self.is_visible(panel_locator)
        return panel.text

    def click_logo_samokat(self):
        element = self.find_clickable(self.LOGO_SAMOKAT)
        self.driver.execute_script("arguments[0].click();", element)

    def click_logo_yandex(self):
        element = self.find_clickable(self.LOGO_YANDEX)
        self.driver.execute_script("arguments[0].click();", element)
