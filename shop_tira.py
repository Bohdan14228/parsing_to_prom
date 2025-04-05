from selenium.common import TimeoutException
import copy

from base_page import BasePage
from locators import Locators
from conftest import *
from google_test import write_to_google_sheet, get_all


class ShopTira(BasePage):

    def all_categories(self):
        self.element_is_present(Locators.BUTTON).click()
        all_categories = self.elements_are_present(Locators.CATEGORIES)
        return {i.text: i.get_attribute("href") for i in all_categories}

    def all_product_in_categories(self, all_categories, driver):
        all_products_categories = {}
        for title_cat in all_categories:
            driver.get(all_categories[title_cat])
            products = []
            while True:
                try:
                    products.extend(
                        [i.get_attribute("href") for i in self.elements_are_present(Locators.PRODUCT)
                         ]
                    )
                    next_button = self.element_is_clickable(Locators.NEXT_PAGE)
                    self.move_to_element(element=next_button)
                except TimeoutException:
                    break
            all_products_categories[title_cat] = products
        return all_products_categories

    def info_about_product(self, all_products_categories, driver):
        group_list = get_all("Export Groups Sheet")
        group_list_copy = copy.deepcopy(group_list)
        get_all_info = get_all("Products")
        get_all_info_copy = copy.deepcopy(get_all_info)

        for categories in all_products_categories:

            updated_group = True
            number_group = None
            id_group = None
            for cat_info in group_list:
                if cat_info[1] == categories:
                    updated_group = False
                    number_group = cat_info[0]
                    id_group = cat_info[3]
                    break
            if updated_group:
                number_group = unic_id_search_and_gen(pid=0, data=group_list, pid_gen=9)
                id_group = unic_id_search_and_gen(pid=3, data=group_list, pid_gen=9)

            for prod_url in all_products_categories[categories][:2]:
                driver.get(prod_url)
                title = self.element_is_present(Locators.PRODUCT_TITLE).text
                price = self.element_is_present(Locators.PRODUCT_PRICE).text
                price = int(''.join(price.split(',')[:1]))

                """Обработка описания"""
                try:
                    description = ' '.join([i.text.strip() for i in self.elements_are_present(Locators.PRODUCT_DESCRIPTION)])
                except TimeoutException:
                    description = '-'

                image_s = []
                try:
                    image_s = [i.get_attribute('src') for i in self.elements_are_present(Locators.PRODUCT_IMAGES)]
                except TimeoutException:
                    image_s = [self.element_is_present(Locators.PRODUCT_IMAGE).get_attribute('src')]
                try:
                    image_s.append(self.element_is_present(Locators.PRODUCT_PHOTO).get_attribute('src'))
                except Exception:
                    pass

                images = []
                for index, image in enumerate(image_s, start=1):
                    image = f"{'-'.join(image.split('-')[:-1])}"
                    extensions = download_image(image, prod_url, index + 1)
                    images.append(extensions)
                images_format_prom = ';'.join(images)

                updated = False
                # проверяем изменения
                for row in get_all_info:
                    if row[1] == title and row[15] == categories:
                        if row[5] != price or row[9] != images_format_prom:
                            row[5] = price
                            row[9] = images_format_prom
                            updated = True
                        break
                if not updated:
                    uniq_id = unic_id_search_and_gen(pid=16, data=get_all_info, pid_gen=7)
                    get_all_info.append(
                        [unic_id_search_and_gen(pid=0, data=get_all_info, pid_gen=6), title, title, description,
                         description, price, '-', 'UAH', 'шт.', images_format_prom, '+', 'Є ОПТ!', 'u', "-",
                         number_group, categories, uniq_id, uniq_id, id_group]
                    )

            if updated_group:
                group_list.append(
                    [number_group, categories, categories, id_group]
                )

        if not all(x == y for x, y in zip(get_all_info, get_all_info_copy)):
            print("not update")
        write_to_google_sheet("Products", data=get_all_info)
        if not all(x == y for x, y in zip(group_list, group_list_copy)):
            print("not update")
        write_to_google_sheet("Export Groups Sheet", data=group_list)
