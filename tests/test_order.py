"""
Тесты для оформления заказа самоката.

Позитивный сценарий (оба набора данных):
1. Нажать кнопку «Заказать» (верхняя или нижняя — разные точки входа)
2. Заполнить форму — Шаг 1: личные данные
3. Заполнить форму — Шаг 2: детали аренды
4. Подтвердить заказ и проверить всплывающее окно об успехе
5а. Набор 1 (top): проверить, что логотип «Самоката» ведёт на главную
5б. Набор 2 (bottom): проверить, что логотип «Яндекса» открывает Дзен в новой вкладке

Параметризация: два набора данных, две точки входа.
"""

import allure
import pytest
from selenium.webdriver.support.wait import WebDriverWait
from pages.main_page import MainPage
from pages.order_page import OrderPage, OrderPageStep2


# Два набора тестовых данных
ORDER_DATA = [
    {
        "button": "top",
        "name": "Иван",
        "last_name": "Иванов",
        "address": "Москва, улица Ленина, 1",
        "metro": "Черкизовская",
        "phone": "+79991234567",
        "date": "05.04.2026",
        "rent_period": "сутки",
        "color": "чёрный жемчуг",
        "comment": "Тестовый заказ 1",
    },
    {
        "button": "bottom",
        "name": "Мария",
        "last_name": "Петрова",
        "address": "Москва, улица Пушкина, 10",
        "metro": "Сокольники",
        "phone": "+79997654321",
        "date": "06.04.2026",
        "rent_period": "двое суток",
        "color": "серая безысходность",
        "comment": "Тестовый заказ 2",
    },
]


@allure.feature("Оформление заказа самоката")
class TestOrder:
    """Позитивный сценарий заказа самоката — обе точки входа."""

    @allure.title("Полный флоу заказа: кнопка '{button}' + проверка логотипа")
    @pytest.mark.parametrize("order_data", ORDER_DATA, ids=["top_button", "bottom_button"])
    def test_order_full_flow(self, driver, order_data):
        """
        Полный позитивный сценарий:
        - нажать «Заказать» (верх или низ страницы)
        - заполнить форму (шаг 1 и шаг 2)
        - проверить всплывающее окно «Заказ оформлен»
        - проверить логотип: набор 1 → Самокат → главная; набор 2 → Яндекс → Дзен
        """
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        step2 = OrderPageStep2(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step(f"Нажать кнопку «Заказать» ({order_data['button']})"):
            if order_data["button"] == "top":
                main_page.click_order_top()
            else:
                main_page.click_order_bottom()

        with allure.step("Шаг 1 — заполнить личные данные"):
            order_page.fill_step1(
                name=order_data["name"],
                last_name=order_data["last_name"],
                address=order_data["address"],
                metro=order_data["metro"],
                phone=order_data["phone"],
            )

        with allure.step("Шаг 2 — заполнить детали аренды"):
            step2.fill_step2(
                date=order_data["date"],
                rent_period=order_data["rent_period"],
                color=order_data["color"],
                comment=order_data["comment"],
            )

        with allure.step("Нажать «Заказать» и подтвердить в модальном окне"):
            step2.submit_order()

        with allure.step("Проверить: появилось всплывающее окно «Заказ оформлен»"):
            assert step2.is_success_modal_shown(), (
                "Модальное окно об успешном создании заказа не появилось"
            )


        # Набор 1 (top): проверяем логотип «Самоката» → главная страница
        if order_data["button"] == "top":
            with allure.step("Кликнуть логотип «Самоката» и проверить переход на главную"):
                main_page.click_logo_samokat()
                assert driver.current_url == MainPage.BASE_URL, (
                    f"Ожидали {MainPage.BASE_URL}, получили {driver.current_url}"
                )

        # Набор 2 (bottom): проверяем логотип «Яндекса» → Дзен в новой вкладке
        else:
            with allure.step("Кликнуть логотип «Яндекса» и проверить открытие Дзена"):
                original_window = driver.current_window_handle
                main_page.click_logo_yandex()

                wait = WebDriverWait(driver, 15)
                wait.until(lambda d: len(d.window_handles) > 1)

                new_window = [w for w in driver.window_handles if w != original_window][0]
                driver.switch_to.window(new_window)
                wait.until(lambda d: d.current_url != "about:blank")

                current_url = driver.current_url
                assert "yandex" in current_url or "dzen" in current_url, (
                    f"Ожидали URL с 'yandex' или 'dzen', получили: {current_url}"
                )
