from shop_tira import ShopTira


class TestShopTira:

    def test_shop_tira(self, driver):
        page = ShopTira(driver, 'https://shop.tira.com.ua/')
        page.open()
        all_categories = page.all_categories()
        products = page.all_product_in_categories(all_categories, driver)
        page.info_about_product(products, driver)