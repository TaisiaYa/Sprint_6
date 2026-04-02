import allure
from pages.main_page import MainPage
from pages.order_page import OrderPage, OrderPageStep2
from data import ORDER_DATA_TOP, ORDER_DATA_BOTTOM


@allure.feature("Оформление заказа самоката")
class TestOrder:

    @staticmethod
    def _fill_and_submit_order(driver, order_data):
        """Вспомогательный метод: заполняет форму и подтверждает заказ."""
        order_page = OrderPage(driver)
        step2 = OrderPageStep2(driver)

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

        with allure.step("Нажать Заказать и подтвердить"):
            step2.submit_order()

        with allure.step("Проверить всплывающее окно «Заказ оформлен»"):
            assert step2.is_success_modal_shown(), (
                "Модальное окно об успешном создании заказа не появилось"
            )

        return step2

    @allure.title("Заказ через верхнюю кнопку — проверка логотипа Самоката")
    def test_order_top_button_logo_samokat(self, driver):
        """Верхняя кнопка Заказать → заполнить форму → логотип Самоката → главная."""
        main_page = MainPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Нажать верхнюю кнопку Заказать"):
            main_page.click_order_top()

        self._fill_and_submit_order(driver, ORDER_DATA_TOP)

        with allure.step("Кликнуть логотип Самоката и проверить переход на главную"):
            main_page.click_logo_samokat()
            assert main_page.get_current_url() == main_page.BASE_URL, (
                f"Ожидали {main_page.BASE_URL}, получили {main_page.get_current_url()}"
            )

    @allure.title("Заказ через нижнюю кнопку — проверка логотипа Яндекса")
    def test_order_bottom_button_logo_yandex(self, driver):
        """Нижняя кнопка Заказать → заполнить форму → логотип Яндекса → Дзен."""
        main_page = MainPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Нажать нижнюю кнопку Заказать"):
            main_page.click_order_bottom()

        self._fill_and_submit_order(driver, ORDER_DATA_BOTTOM)

        with allure.step("Кликнуть логотип Яндекса и проверить открытие Дзена"):
            main_page.click_logo_yandex()
            new_url = main_page.switch_to_new_tab()
            assert "yandex" in new_url or "dzen" in new_url, (
                f"Ожидали URL с 'yandex' или 'dzen', получили: {new_url}"
            )