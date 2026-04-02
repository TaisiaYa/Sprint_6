import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class MainPage(BasePage):

    ORDER_BUTTON_TOP = (By.XPATH, "//button[contains(@class,'Button_Button') and not(contains(@class,'UltraBig')) and contains(text(),'Заказать')]")
    ORDER_BUTTON_BOTTOM = (By.XPATH, "//button[contains(@class,'Button_UltraBig')]")

    LOGO_SAMOKAT = (By.XPATH, "//a[contains(@class,'Header_LogoScooter')]")
    LOGO_YANDEX = (By.XPATH, "//a[contains(@class,'Header_LogoYandex')]")
    COOKIE_BUTTON = (By.XPATH, "//button[contains(., 'да все привыкли')]")

    @staticmethod
    def faq_heading(index):
        return By.XPATH, f"//div[@id='accordion__heading-{index}']"

    @staticmethod
    def faq_panel(index):
        return By.XPATH, f"//div[@id='accordion__panel-{index}']"

    @allure.step("Открыть главную страницу")
    def open(self):
        self.driver.get(self.BASE_URL)
        self._dismiss_cookies()

    def _dismiss_cookies(self):
        try:
            self.wait.until(lambda d: d.find_elements(*self.COOKIE_BUTTON))
            self.click(self.COOKIE_BUTTON)
        except TimeoutException:
            pass

    @allure.step("Нажать кнопку Заказать (верхняя)")
    def click_order_top(self):
        self.click(self.ORDER_BUTTON_TOP)

    @allure.step("Нажать кнопку Заказать (нижняя)")
    def click_order_bottom(self):
        self.scroll_and_js_click(self.ORDER_BUTTON_BOTTOM)

    @allure.step("Открыть вопрос FAQ")
    def click_faq_question(self, index):
        self.scroll_and_js_click(self.faq_heading(index))

    @allure.step("Получить текст ответа FAQ")
    def get_faq_answer_text(self, index):
        panel = self.is_visible(self.faq_panel(index))
        return panel.text

    @allure.step("Кликнуть логотип Самоката")
    def click_logo_samokat(self):
        self.js_click(self.LOGO_SAMOKAT)

    @allure.step("Кликнуть логотип Яндекса")
    def click_logo_yandex(self):
        self.js_click(self.LOGO_YANDEX)