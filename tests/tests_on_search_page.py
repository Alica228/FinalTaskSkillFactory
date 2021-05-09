from pages.search_page import SearchPage
from pages.elements import WebElement, ManyWebElements
import pytest
import time
from random import sample
from data import filters


@pytest.mark.parametrize("my_input,expected_title", [
    (("Гаджеты", "Мобильные"), "Мобильные телефоны "),
    (("Компьютеры", "Ноутбуки"), "Ноутбуки "),
    (("Фото", "Фотоаппараты"), "Фотоаппараты "),
    ((" TV ", "Телевизоры"), "Телевизоры "),
    (("Аудио", "Наушники"), "Наушники "),
    (("Бытовая техника", "Встраиваемая техника"), "Встраиваемая техника"),
    (("Климат", "Кондиционеры"), "Кондиционеры "),
    (("Дом", "Сантехника"), "Сантехника"),
    (("Детские товары", "Коляски"), "Коляски "),
])
def test_access_to_search_page(web_browser, my_input, expected_title):
    """ Test search page is accessable. """
    page = SearchPage(web_browser, *my_input)
    title = WebElement(web_browser, xpath='//div[@class="page-title"]/div').get_text() or \
            WebElement(web_browser, xpath='//div[@class="page-title"]/h1').get_text()

    assert title == expected_title


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


@pytest.mark.parametrize("custom_filter", [
    pytest.param(('', '10000', '15000', [], []), marks=pytest.mark.xfail(reason="there bug with prices. If we choice min price 15000, system will show us products with min price >= 15000")),
    pytest.param(('', '10000', '-15000', [], []), marks=pytest.mark.xfail(reason="there bug with prices. If we choice min price 15000, system will show us products with min price >= 15000")),
    pytest.param(('', '10000', '10000', [], []), marks=pytest.mark.xfail(reason="there bug with prices. If we choice min price 15000, system will show us products with min price >= 15000")),
    pytest.param(('', 'AAAAAAA', '10000', [], []), marks=pytest.mark.xfail(reason="there bug with prices. If we choice min price 15000, system will show us products with min price >= 15000")),
    pytest.param(('', '15000', '10000', [], []), marks=pytest.mark.xfail(reason="there bug with prices. If we choice min price 15000, system will show us products with min price >= 15000")),
    ('Apple', '', '', ['Apple'], []),
    ('', '', '', ['Apple', 'BQ'], []),
    pytest.param(('', '', '30000', ['Apple', 'BQ'], []),marks=pytest.mark.xfail(reason="there bug with prices. If we choice min price 15000, system will show us products with min price >= 15000")),
    pytest.param(('', '10000', '30000', ['Apple', 'BQ'], []), marks=pytest.mark.xfail(reason="there bug with prices. If we choice min price 15000, system will show us products with min price >= 15000")),
    ('', '', '', [], sample(filters, 1)),
    pytest.param(('', '5000', '', [], sample(filters, 1)), marks=pytest.mark.xfail(reason="there bug with prices. If we choice min price 15000, system will show us products with min price >= 15000")),
    pytest.param(('', '', '20000', [], sample(filters, 1)),marks=pytest.mark.xfail(reason="there bug with prices. If we choice min price 15000, system will show us products with min price >= 15000")),
    pytest.param(('', '10000', '40000', [], sample(filters, 1)), marks=pytest.mark.xfail(reason="there bug with prices. If we choice min price 15000, system will show us products with min price >= 15000")),
    ('', '', '', [], sample(filters, 1)),
    ('', '', '', [], sample(filters, 1)),
    ('', '', '', [], sample(filters, 1)),
    ('', '', '', [], sample(filters, 1)),
    ('', '', '', [], sample(filters, 1)),
    ('', '', '', [], sample(filters, 1)),
    ('', '', '', [], sample(filters, 1)),
    ('', '', '', [], sample(filters, 1)),
    ('', '', '', [], sample(filters, 1)),
    ('', '', '', [], sample(filters, 1)),
    ('', '', '', [], sample(filters, 1)),
], ids=["10000 <= price <= 15000",
        "10000 <= price <= -15000 ????",
        "10000 <= price <= 10000",
        "AAAAAAA <= price <= 10000 ????",
        "15000 <= price <= 10000 ????",
        "Apple filter",
        "Apple and BQ filter",
        "Apple and BQ filter with price <= 30000",
        "Apple and BQ filter with 10000 <= price <= 30000",
        "Random filters",
        "Random filters with 5000 <= price",
        "Random filters with price <= 20000",
        "Random filters with 10000 <= price <= 40000",
        "Another random filters",
        "Another random filters",
        "Another random filters",
        "Another random filters",
        "Another random filters",
        "Another random filters",
        "Another random filters",
        "Another random filters",
        "Another random filters",
        "Another random filters",
        "Another random filters",
])
def test_filter_products(web_browser, custom_filter):
    """ Test that filter correctly show products. """
    page = SearchPage(web_browser, "Гаджеты", "Мобильные")
    name, price_min, price_max, manufacturer, my_filters = custom_filter
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

    if my_filters:
        products = ManyWebElements(web_browser,
                                   xpath='//a[@class="model-short-title no-u"]/span[@class="u"]')

        assert len(products) > 0
