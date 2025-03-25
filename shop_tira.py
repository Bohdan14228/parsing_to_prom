import time

from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from locators import Locators

url = 'https://shop.tira.com.ua/'


def test_main(driver):
    # all categories
    driver.get(url)
    wait(driver, 5).until(EC.presence_of_element_located(Locators.BUTTON)).click()
    all_categories = wait(driver, 5).until(EC.presence_of_all_elements_located(Locators.CATEGORIES))
    all_categories = {i.text: i.get_attribute("href") for i in all_categories}

    # products
    all_products_categories = {}
    for link in all_categories:
        driver.get(all_categories[link])
        products = []
        while True:
            try:
                products.extend(
                    [
                        i.get_attribute("href") for i in wait(driver, 5).
                        until(EC.presence_of_all_elements_located(Locators.PRODUCT))
                    ]
                )
                p = wait(driver, 5).until(EC.element_to_be_clickable(Locators.NEXT_PAGE))
                actions = ActionChains(driver)
                actions.move_to_element(p).perform()
                p.click()
            except TimeoutException:
                break
        all_products_categories[link] = products

