from pages.search_page import SearchPage
from pages.elements import WebElement, ManyWebElements
import pytest
import time
from data import valid_email_1, valid_password_1, valid_email_2, valid_password_2


def test_access_to_search_page(web_browser):
    """ Test search page. """
    page = SearchPage(web_browser, "Гаджеты", "Мобильные")
    title = WebElement(web_browser,
                       xpath='//div[@class="page-title"]/div')

    assert title.get_text() == "Мобильные телефоны "

    time.sleep(1)


@pytest.mark.parametrize("manufacturer", [
    "Apple", "BQ", "Huawei", "Nokia", "OnePlus", "Samsung", "Xiaomi", "ZTE"]
)
def test_title_of_products(web_browser, manufacturer):
    """ Test that filter correctly show name of products. """
    page = SearchPage(web_browser, "Гаджеты", "Мобильные")
    link = WebElement(web_browser,
                       xpath=f'//div[@class="brands-tags"]/a[@href="/list/122/{manufacturer.lower()}/"]')
    link.click()

    title = WebElement(web_browser,
                       xpath='//div[@class="page-title"]/h1')
    assert title.get_text() == f"Мобильные телефоны {manufacturer}"

    products = ManyWebElements(web_browser,
                       xpath='//a[@class="model-short-title no-u"]/span[@class="u"]')

    product_titles_contains_manufacturer = [manufacturer in title for title in products.get_text()]
    assert all(product_titles_contains_manufacturer)

    time.sleep(1)


@pytest.mark.parametrize("custom_filter", [
    ('', '10000', '15000', [], []),
    ('', '10000', '10000', [], []),
    ('', '15000', '10000', [], []),
    ('Apple', '', '', ['Apple'], []),
    ('', '', '', ['Apple', 'BQ'], []),
    ('', '', '30000', ['Apple', 'BQ'], []),
    ('', '10000', '30000', ['Apple', 'BQ'], []),
], ids=["10000 <= price <= 15000",
        "10000 <= price <= 10000",
        "15000 <= price <= 10000 ????",
        "Apple filter",
        "Apple and BQ filter",
        "Apple and BQ filter with price <= 30000",
        "Apple and BQ filter with 10000 <= price <= 30000",
])
def test_filter_products(web_browser, custom_filter):
    """ Test that filter correctly show products. """
    page = SearchPage(web_browser, "Гаджеты", "Мобильные")
    name, price_min, price_max, manufacturer = custom_filter
    page.filter_products(*custom_filter)
    if price_min or price_max:
        all_prices = ManyWebElements(web_browser, xpath='//div[@class="model-price-range"]/a/span').get_text()

        if price_min:
            all_min_prices = all_prices[0::3]
            assert sum(
                int(price_min) <= int(price.replace(' ', '')) <= int(price_max) for price in all_min_prices) == len(
                all_min_prices), "Smth wrong with min price"

        if price_max:
            all_max_prices = all_prices[1::3]
            assert sum(
                int(price.replace(' ', '')) <= int(price_max) for price in all_max_prices) == len(
                all_max_prices), "Smth wrong with max price"

    if manufacturer:
        products = ManyWebElements(web_browser,
                                   xpath='//a[@class="model-short-title no-u"]/span[@class="u"]')
        product_titles_contains_manufacturer = [any(brand in title for brand in manufacturer) for title in products.get_text()]
        assert all(product_titles_contains_manufacturer)

    time.sleep(1)
