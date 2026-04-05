"""
Page Object для страницы оформления заказа.
Шаг 1: «Для кого самокат» — личные данные.
Шаг 2: «Про аренду» — дата, срок, цвет, комментарий.
"""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class OrderPage(BasePage):
    """Страница заказа — Шаг 1 (личные данные)."""

    FIELD_NAME = (By.XPATH, "//input[@placeholder='* Имя']")
    FIELD_LAST_NAME = (By.XPATH, "//input[@placeholder='* Фамилия']")
    FIELD_ADDRESS = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    FIELD_METRO = (By.XPATH, "//input[@placeholder='* Станция метро']")
    FIELD_PHONE = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    BUTTON_NEXT = (By.XPATH, "//button[contains(., 'Далее')]")
    METRO_DROPDOWN_OPTION = (By.XPATH, "//li[contains(@class,'select-search__row')]//button")

    @allure.step("Заполнить шаг 1: имя={name}, фамилия={last_name}, адрес={address}, метро={metro}, телефон={phone}")
    def fill_step1(self, name, last_name, address, metro, phone):
        self.type_text(self.FIELD_NAME, name)
        self.type_text(self.FIELD_LAST_NAME, last_name)
        self.type_text(self.FIELD_ADDRESS, address)
        self._select_metro(metro)
        self.type_text(self.FIELD_PHONE, phone)
        self.click(self.BUTTON_NEXT)

    def _select_metro(self, station_name):
        self.type_text(self.FIELD_METRO, station_name)
        self.click(self.METRO_DROPDOWN_OPTION)


class OrderPageStep2(BasePage):
    """Страница заказа — Шаг 2 (детали аренды «Про аренду»)."""

    FIELD_DATE = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    DROPDOWN_RENT = (By.XPATH, "//div[contains(@class,'Dropdown-root')]")
    LABEL_BLACK = (By.XPATH, "//label[contains(., 'чёрный жемчуг')]")
    LABEL_GREY = (By.XPATH, "//label[contains(., 'серая безысходность')]")
    FIELD_COMMENT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")

    # ВАЖНО: на странице 2 есть кнопка «Заказать» в хедере (первая по DOM).
    # Нам нужна кнопка ФОРМЫ — она последняя на странице, используем [last()]
    BUTTON_ORDER = (By.XPATH, "(//button[contains(., 'Заказать')])[last()]")

    MODAL_CONFIRM_YES = (By.XPATH, "//button[contains(., 'Да')]")
    MODAL_SUCCESS = (By.XPATH, "//*[contains(text(), 'Заказ оформлен')]")

    # Навигация в календаре
    CAL_NEXT = (By.XPATH, "//*[contains(@class,'react-datepicker__navigation--next')]")
    CAL_MONTH = (By.XPATH, "//*[contains(@class,'react-datepicker__current-month')]")

    # Названия месяцев на русском (именительный и родительный падеж)
    MONTHS_RU = {
        'январь': 1, 'февраль': 2, 'март': 3, 'апрель': 4,
        'май': 5, 'июнь': 6, 'июль': 7, 'август': 8,
        'сентябрь': 9, 'октябрь': 10, 'ноябрь': 11, 'декабрь': 12,
        'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
        'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
        'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12,
    }


    @allure.step("Заполнить шаг 2: дата={date}, период={rent_period}, цвет={color}, комментарий={comment}")
    def fill_step2(self, date, rent_period, color, comment):
        self._enter_date(date)
        self._select_rent_period(rent_period)
        self._select_color(color)
        if comment:
            self.type_text(self.FIELD_COMMENT, comment)

    def _enter_date(self, date_str):
        """Вводим дату через навигацию в календаре (DD.MM.YYYY)."""
        day, month, year = date_str.split('.')
        target_day = int(day)
        target_month = int(month)
        target_year = int(year)

        # Открываем календарь
        field = self.find_clickable(self.FIELD_DATE)
        field.click()

        # Листаем месяцы вперёд пока не попадём в нужный
        for _ in range(24):
            label = self.find(self.CAL_MONTH).text.lower().strip()
            parts = label.split()
            if len(parts) >= 2:
                cur_m = self.MONTHS_RU.get(parts[0], 0)
                cur_y = int(parts[1])
                if cur_m == target_month and cur_y == target_year:
                    break
            self.driver.execute_script(
                "arguments[0].click();",
                self.find_clickable(self.CAL_NEXT)
            )

        # Кликаем на нужный день (исключаем дни из других месяцев)
        day_locator = (
            By.XPATH,
            f"//div[contains(@class,'react-datepicker__day') "
            f"and not(contains(@class,'outside-month')) "
            f"and not(contains(@class,'disabled')) "
            f"and normalize-space(text())='{target_day}']"
        )
        self.click(day_locator)

    def _select_rent_period(self, period_text):
        self.click(self.DROPDOWN_RENT)
        option = (By.XPATH,
                  f"//div[contains(@class,'Dropdown-option') and contains(., '{period_text}')]")
        self.click(option)

    def _select_color(self, color):
        color_map = {
            "чёрный жемчуг": self.LABEL_BLACK,
            "серая безысходность": self.LABEL_GREY,
        }
        self.click(color_map.get(color.lower(), self.LABEL_BLACK))

    def submit_order(self):
        self.click(self.BUTTON_ORDER)
        self.click(self.MODAL_CONFIRM_YES)

    def is_success_modal_shown(self):
        return self.is_visible(self.MODAL_SUCCESS) is not None
