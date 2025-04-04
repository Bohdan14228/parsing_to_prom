from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from base_page import BasePage
from locators import Locators
from conftest import *
from google_test import write_to_google_sheet, get_all


class ShopTira(BasePage):

    def all_categories(self):
        # all categories
        # wait(driver, 5).until(EC.presence_of_element_located(Locators.BUTTON)).click()
        self.element_is_present(Locators.BUTTON).click()
        # all_categories = wait(driver, 5).until(EC.presence_of_all_elements_located(Locators.CATEGORIES))
        all_categories = self.elements_are_present(Locators.CATEGORIES)
        return {i.text: i.get_attribute("href") for i in all_categories}

    def all_product_in_categories(self, all_categories, driver):
        # products
        all_products_categories = {}
        for title_cat in all_categories:
            driver.get(all_categories[title_cat])
            products = []
            while True:
                try:
                    products.extend(
                        [i.get_attribute("href") for i in self.elements_are_present(Locators.PRODUCT)
                         # i.get_attribute("href") for i in wait(driver, 5).
                         # until(EC.presence_of_all_elements_located(Locators.PRODUCT))
                         ]
                    )
                    # p = wait(driver, 5).until(EC.element_to_be_clickable(Locators.NEXT_PAGE))
                    next_button = self.element_is_clickable(Locators.NEXT_PAGE)
                    # actions = ActionChains(driver)
                    # actions.move_to_element(p).perform()
                    # p.click()
                    self.move_to_element(element=next_button)
                    # next_button.click()
                except TimeoutException:
                    break
            all_products_categories[title_cat] = products
        return all_products_categories

    def info_about_product(self, all_products_categories, driver):
        group_list = []
        get_all_info = get_all("Products")
        for categories in all_products_categories:

            id_group = generate_unique_product_id(k=8)
            number_group = generate_unique_product_id(k=8)

            for prod_url in all_products_categories[categories][:2]:

                driver.get(prod_url)

                # title = wait(driver, 5).until(EC.presence_of_element_located(Locators.PRODUCT_TITLE)).text
                title = self.element_is_present(Locators.PRODUCT_TITLE).text
                # price = wait(driver, 5).until(EC.presence_of_element_located(Locators.PRODUCT_PRICE)).text
                price = self.element_is_present(Locators.PRODUCT_PRICE).text
                price = int(''.join(price.split(',')[:1]))

                """Обработка описания"""
                try:
                    description = ' '.join([i.text.strip() for i in self.elements_are_present(Locators.PRODUCT_DESCRIPTION)])
                except TimeoutException:
                    description = '-'

                image_s = 'нету фото'
                try:  # wait(driver, 3).until(EC.presence_of_all_elements_located(Locators.PRODUCT_IMAGES))
                    image_s = [i.get_attribute('src') for i in self.elements_are_present(Locators.PRODUCT_IMAGES)]
                except TimeoutException:
                    image_s = [self.element_is_present(Locators.PRODUCT_IMAGE).get_attribute('src')
                               # wait(driver, 5).until(EC.presence_of_element_located(Locators.PRODUCT_IMAGE)).get_attribute(
                               #     'src')
                               ]
                try:
                    image_s.append(self.element_is_present(Locators.PRODUCT_PHOTO).get_attribute('src'))
                        # wait(driver, 5).until(EC.presence_of_element_located(Locators.PRODUCT_PHOTO)).get_attribute(
                        #     'src'))
                except:
                    pass

                images = []
                for index, image in enumerate(image_s, start=1):
                    image = f"{'-'.join(image.split('-')[:-1])}"
                    extensions = download_image(image, prod_url, index + 1)
                    images.append(extensions)
                images = ';'.join(images)

                # проверяем изменения
                for row in get_all_info:
                    if row[1] == title:
                        is_subset = all(item in row for item in [description, price, images, categories])
                        if not is_subset:
                        # if row[3] != description or row[5] != price or row[9] != images or row[15] != categories:
                            row[3] = description
                            row[4] = description
                            row[5] = price
                            row[9] = images
                            row[15] = categories
                        break

                uniq_id = generate_unique_product_id(k=8)
                get_all_info.append(
                    [generate_unique_product_id(), title, title, description, description, price, '-', 'UAH', 'шт.',
                     images, '+', 'Є ОПТ!', 'u', "-", number_group, categories, uniq_id,
                     uniq_id, id_group]
                )

            group_list.append(
                [number_group, categories, categories, id_group]
            )

        write_to_google_sheet("Products", data=get_all_info)
        write_to_google_sheet("Export Groups Sheet", data=group_list)
