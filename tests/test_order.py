import allure
from pages.main_page import MainPage
from pages.order_page import OrderPage, OrderPageStep2
from data import ORDER_DATA_TOP, ORDER_DATA_BOTTOM


@allure.feature("Оформление заказа самоката")
class TestOrder:

    @allure.title("Заказ через верхнюю кнопку — проверка логотипа Самоката")
    def test_order_top_button_logo_samokat(self, driver):
        """Верхняя кнопка Заказать → заполнить форму → логотип Самоката → главная."""
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        step2 = OrderPageStep2(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Нажать верхнюю кнопку Заказать"):
            main_page.click_order_top()

        with allure.step("Шаг 1 — заполнить личные данные"):
            order_page.fill_step1(
                name=ORDER_DATA_TOP["name"],
                last_name=ORDER_DATA_TOP["last_name"],
                address=ORDER_DATA_TOP["address"],
                metro=ORDER_DATA_TOP["metro"],
                phone=ORDER_DATA_TOP["phone"],
            )

        with allure.step("Шаг 2 — заполнить детали аренды"):
            step2.fill_step2(
                date=ORDER_DATA_TOP["date"],
                rent_period=ORDER_DATA_TOP["rent_period"],
                color=ORDER_DATA_TOP["color"],
                comment=ORDER_DATA_TOP["comment"],
            )

        with allure.step("Нажать Заказать и подтвердить"):
            step2.submit_order()

        with allure.step("Проверить всплывающее окно «Заказ оформлен»"):
            assert step2.is_success_modal_shown(), (
                "Модальное окно об успешном создании заказа не появилось"
            )

        with allure.step("Кликнуть логотип Самоката и проверить переход на главную"):
            main_page.click_logo_samokat()
            assert main_page.get_current_url() == main_page.BASE_URL, (
                f"Ожидали {main_page.BASE_URL}, получили {main_page.get_current_url()}"
            )

    @allure.title("Заказ через нижнюю кнопку — проверка логотипа Яндекса")
    def test_order_bottom_button_logo_yandex(self, driver):
        """Нижняя кнопка Заказать → заполнить форму → логотип Яндекса → Дзен."""
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        step2 = OrderPageStep2(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Нажать нижнюю кнопку Заказать"):
            main_page.click_order_bottom()

        with allure.step("Шаг 1 — заполнить личные данные"):
            order_page.fill_step1(
                name=ORDER_DATA_BOTTOM["name"],
                last_name=ORDER_DATA_BOTTOM["last_name"],
                address=ORDER_DATA_BOTTOM["address"],
                metro=ORDER_DATA_BOTTOM["metro"],
                phone=ORDER_DATA_BOTTOM["phone"],
            )

        with allure.step("Шаг 2 — заполнить детали аренды"):
            step2.fill_step2(
                date=ORDER_DATA_BOTTOM["date"],
                rent_period=ORDER_DATA_BOTTOM["rent_period"],
                color=ORDER_DATA_BOTTOM["color"],
                comment=ORDER_DATA_BOTTOM["comment"],
            )

        with allure.step("Нажать Заказать и подтвердить"):
            step2.submit_order()

        with allure.step("Проверить всплывающее окно «Заказ оформлен»"):
            assert step2.is_success_modal_shown(), (
                "Модальное окно об успешном создании заказа не появилось"
            )

        with allure.step("Кликнуть логотип Яндекса и проверить открытие Дзена"):
            main_page.click_logo_yandex()
            new_url = main_page.switch_to_new_tab()
            assert "yandex" in new_url or "dzen" in new_url, (
                f"Ожидали URL с 'yandex' или 'dzen', получили: {new_url}"
            )
