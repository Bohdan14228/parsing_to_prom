class Locators:
    BUTTON = ('xpath', '//button[@class="cat-btn"]')
    CATEGORIES = ("xpath", "//div[@class='home_product_cat']/h4/a")
    PRODUCT = ('xpath', "//ul[@class='products columns-4']/li/a[1]")
    NEXT_PAGE = ('xpath', '//*[contains(@class, "next") and contains(@class, "page-numbers")]')

    PRODUCT_TITLE = ("xpath", '//h1[contains(@class, "product_title") and contains(@class, "entry-title")]')
    PRODUCT_PRICE = ("xpath", "//p[@class='price']")
    PRODUCT_IMAGE = ("xpath", '(//div[@class="slick-track"])[2]/div/img')

    @staticmethod
    def head(count):
        return "xpath", f"(//div[@class='accordeon-element__title'])[{count}]"
