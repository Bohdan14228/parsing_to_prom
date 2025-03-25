import time

from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from locators import Locators
from selenium.webdriver.common.action_chains import ActionChains


url = 'https://shop.tira.com.ua/?product=%d0%bd%d0%b0%d0%b1%d0%be%d1%80-%d1%82%d1%8b%d1%87%d0%ba%d0%be%d0%b2%d1%8b%d0%b9-%d0%bd%d0%be%d0%b2%d1%8b%d0%b9'


def test_tt(driver):
    driver.get(url)

    title = wait(driver, 5).until(EC.presence_of_element_located(Locators.PRODUCT_TITLE)).text
    price = wait(driver, 5).until(EC.presence_of_element_located(Locators.PRODUCT_PRICE)).text
    image = [i.get_attribute('src') for i in wait(driver, 5).until(EC.presence_of_all_elements_located(Locators.PRODUCT_IMAGE))]

    print(title)
    print(price)
    print(image)
