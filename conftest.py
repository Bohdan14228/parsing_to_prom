import pytest
from selenium import webdriver
import requests
import random
import string


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


def download_image(url, filename):
    data = ['.jpg', '.bmp', '.png']
    for i in data:
        response = requests.get(f"{url}{i}", stream=True)
        if response.status_code == 200:
            with open(f"{filename}{i}", 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return i
    print(f"Фото не загрузилось\n{filename}")


existing_ids = set()


def generate_unique_product_id(k=6):
    # chars = string.ascii_lowercase + string.digits
    chars = string.ascii_lowercase
    while True:
        new_id = ''.join(random.choices(chars, k=k))
        if new_id not in existing_ids:
            existing_ids.add(new_id)
            return new_id
