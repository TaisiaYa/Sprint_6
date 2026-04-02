import allure
import pytest
from pages.main_page import MainPage
from data import FAQ_DATA


@allure.feature("FAQ — Вопросы о важном")
class TestFAQ:

    @allure.title("Вопрос {index}: '{question}' — проверка открытия ответа")
    @pytest.mark.parametrize("index, question, expected_text", FAQ_DATA)
    def test_faq_question_opens_answer(self, driver, index, question, expected_text):
        """
        Проверяем, что при клике на вопрос FAQ открывается текст ответа,
        содержащий ожидаемый фрагмент.
        """
        with allure.step("Открыть главную страницу"):
            page = MainPage(driver)
            page.open()

        with allure.step(f"Прокрутить до вопроса №{index + 1}: «{question}»"):
            page.click_faq_question(index)

        with allure.step(f"Проверить, что ответ содержит: «{expected_text}»"):
            answer_text = page.get_faq_answer_text(index)
            assert expected_text in answer_text, (
                f"Ожидали «{expected_text}», получили: «{answer_text}»"
            )