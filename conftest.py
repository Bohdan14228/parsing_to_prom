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


def download_image(url, filename, number):
    data = ['.jpg', '.bmp', '.png']
    for i in data:
        response = requests.get(f"{url}{i}", stream=True)
        if response.status_code == 200:
            return response.url
    print(f"Фото #{number} не загрузилось\n{filename}")


# existing_ids = set()


def generate_id(k=6):
    # chars = string.ascii_lowercase + string.digits
    chars = string.digits
    return ''.join(random.choices(chars, k=k))


def unic_id_search_and_gen(pid: int, data: list, pid_gen: int):
    l = [i[pid] for i in data]
    while True:
        new_id = generate_id(pid_gen)
        if new_id not in l:
            return new_id


def search_load_data(pid: int, categories: str, data: list):
    l = [i[pid] for i in data]
    if categories in l:
        return True
    return False
