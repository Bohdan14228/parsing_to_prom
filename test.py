import json
import time

from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from locators import Locators
from selenium.webdriver.common.action_chains import ActionChains
from conftest import *

# url = "https://shop.tira.com.ua/?product=%d0%ba%d0%b5%d1%80%d0%b0%d0%bc%d0%b1%d0%b8%d1%82-%d0%b4%d0%b5%d1%88%d1%91%d0%b2%d1%8b%d0%b9"


# def test_tt(driver):
#     driver.get(url)
    # data_json = {}
    # title = wait(driver, 5).until(EC.presence_of_element_located(Locators.PRODUCT_TITLE)).text
    # price = wait(driver, 5).until(EC.presence_of_element_located(Locators.PRODUCT_PRICE)).text
    # price = int(''.join(price.split(',')[:1]))
    # description = ' '.join([i.text.strip() for i in wait(driver, 5).
    #                        until(EC.presence_of_all_elements_located(Locators.PRODUCT_DESCRIPTION))])
    # print(description)
#
#     image_s = 'нету фото'
#     try:
#         image_s = [i.get_attribute('src') for i in
#                    wait(driver, 3).until(EC.presence_of_all_elements_located(Locators.PRODUCT_IMAGES))]
#     except TimeoutException:
#         image_s = [
#             wait(driver, 5).until(EC.presence_of_element_located(Locators.PRODUCT_IMAGE)).get_attribute('src')]
#     try:
#         image_s.append(
#             wait(driver, 5).until(EC.presence_of_element_located(Locators.PRODUCT_PHOTO)).get_attribute('src'))
#     except TimeoutException:
#         pass
#
#     id_prod = generate_unique_product_id()
#     images = []
#
#     for index, image in enumerate(image_s, start=1):
#         filename = f"images\\{id_prod}_{index}"
#         image = f"{'-'.join(image.split('-')[:-1])}"
#         download_image(image, filename)
#         images.append(filename)
#
#     data_json[id_prod] = {
#         # 'categories': categories,
#         'title': title,
#         'price': price,
#         'images': images,
#         'url': url
#     }
#
#     print(data_json)
#
#     with open("data.json", "w", encoding="utf-8") as file:
#         json.dump(data_json, file, ensure_ascii=False, indent=4)


# r = 'https://shop.tira.com.ua/wp-content/uploads/2024/09/0-02-05-5ffb3a3fb9d26857c8241f0ced0a90bc4f72f1576a09b670858a8b9f0f288e40_e80639a78326aed1-1-100x100.jpg'
#
# print()

# src="https://shop.tira.com.ua/wp-content/uploads/2024/09/Фон-100x100.jpg"
#
# src = f"{'-'.join(src.split('-')[:-1])}.jpg"
# print(src)

# with open("data.json", "r", encoding="utf-8") as file:
#     data = json.load(file)
#
#
# for i in data:
#     print(data[i]['title'])
    # for y in data[i]:
    #     print(y)

for i in []:
    if i == 1:
        print(1)
print(1)