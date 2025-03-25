import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions


@pytest.fixture(scope="function")
def driver():
    options_chrome = webdriver.ChromeOptions()
    # options_chrome.add_argument("--headless")
    # options_chrome.add_argument("--disable-gpu")
    options_chrome.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=options_chrome)
    driver.maximize_window()
    yield driver
    driver.quit()
