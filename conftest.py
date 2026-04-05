import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запустить браузер в headless-режиме (без открытия окна)"
    )


@pytest.fixture(scope="function")
def driver(request):
    """Создаём Firefox WebDriver перед каждым тестом и закрываем после."""
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    driver.maximize_window()

    yield driver  # здесь выполняется тест

    driver.quit()
