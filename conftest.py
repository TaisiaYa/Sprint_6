import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


@pytest.fixture(scope="function")
def driver():
    """Создаём Firefox WebDriver перед каждым тестом и закрываем после."""
    options = Options()
    # Раскомментируй строку ниже, если нужен headless-режим (без открытия браузера):
    # options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    driver.maximize_window()

    yield driver  # здесь выполняется тест

    driver.quit()
