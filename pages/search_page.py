#!/usr/bin/python3
# -*- encoding=utf8 -*-

import time
from pages.main_page import MainPage
from pages.elements import WebElement, ManyWebElements


class SearchPage(MainPage):

    def __init__(self, web_driver, category_1, category_2):
        super().__init__(web_driver)
        all_categories_1 = ManyWebElements(self._web_driver,
                                           xpath='//ul[@class="mainmenu-list ff-roboto"]/li/a')
        if category_1 not in all_categories_1.get_text():
            msg = 'Category {0} not found'
            raise AttributeError(msg.format(category_1))
        idx = all_categories_1.get_text().index(category_1)
        all_categories_1[idx].click()

        all_categories_2 = ManyWebElements(self._web_driver,
                                           xpath='//div[@class="mainmenu-sublist"]/a')
        if category_2 not in all_categories_2.get_text():
            msg = 'Category {0} not found'
            raise AttributeError(msg.format(category_2))
        idx = all_categories_2.get_text().index(category_2)
        all_categories_2[idx].click()

    def filter_products(self, name='', price_min='', price_max='', manufacturer=[], other=[]):
        """ Filter products by filters. """

        if name:
            search_field = WebElement(self._web_driver,
                                      xpath='//input[@class="rm-search-presets-input ek-form-control"]')
            search_field.send_keys(name)

        if price_min:
            price_min_field = WebElement(self._web_driver,
                                         id="minPrice_")
            price_min_field.send_keys(price_min)

        if price_max:
            price_max_field = WebElement(self._web_driver,
                                         id="maxPrice_")
            price_max_field.send_keys(price_max)

        if manufacturer:
            for brand in manufacturer:
                link = WebElement(self._web_driver,
                                  xpath=f'//div[@id="manufacturers_presets"]//a[@href="/list/122/{brand.lower()}/"]')
                link.click()

        if other:

            # Need to delete this element from page
            WebElement(self._web_driver,
                       xpath='//div[@class="bottom-goods-menu"]').delete()

            all_features = ManyWebElements(self._web_driver,
                                          xpath='//form[@id="form_match"]/div/ul/li')

            for feature in other:

                if feature not in all_features.get_text():
                    msg = 'Feature {0} not found'
                    raise AttributeError(msg.format(feature))

                idx = all_features.get_text().index(feature)
                all_features[idx].click()

        time.sleep(1)
        try:
            show_button = WebElement(self._web_driver, timeout=20,
                                 xpath='//a[@class="show-models"]')
            show_button.click()
        except:
            show_button = WebElement(self._web_driver, timeout=20,
                                 xpath='//a[@class="show-models"]')
            show_button.click()

    # Хотел сделать ещё проверку закладок и сравнения цен, но эти элементы не видны,
    # пока не наведёшь на них, поэтому обычный click не срабатывает
    def mark_product(self, locator):
        """ Mark a product. TODO """
        all_products = ManyWebElements(self._web_driver,
                                       xpath='//tr[@valign="top"]')