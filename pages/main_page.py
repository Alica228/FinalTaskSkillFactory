#!/usr/bin/python3
# -*- encoding=utf8 -*-

from pages.base import WebPage
from pages.elements import WebElement, ManyWebElements


class MainPage(WebPage):

    def __init__(self, driver):
        url = "https://www.e-katalog.ru/"
        super().__init__(driver, url)

    def click_enter_button(self):
        enter_button = WebElement(self._web_driver, xpath='//div[@class="header_action_login"]/span')
        enter_button.click()

    def login_with_email(self, email, password):
        enter_button_email = WebElement(self._web_driver, xpath='//div[@class="signin-with signin-with-ek d-flex justify-content-center align-items-center"]')
        enter_button_email.click()

        email_and_password_fields = ManyWebElements(self._web_driver, xpath='//div[@class="signin"]/div/input[@class="ek-form-control" and @type="text"]')
        email_and_password_fields._set_value([email, password])

        login_button = WebElement(self._web_driver, xpath='//button[@class="ek-form-btn blue" and @type="submit"]')
        login_button.click()

    def nickname_button(self):
        nick_name = WebElement(self._web_driver, xpath='//a[@class="info-nick"]')
        return nick_name

    def register_user(self, name, email, password):
        registration_button = WebElement(self._web_driver, xpath='//div[@class="signin-with signin-with-reg d-flex justify-content-center align-items-center"]/span')
        registration_button.click()

        input_fields = ManyWebElements(self._web_driver, xpath='//div[@class="registration"]/div/input[@class="ek-form-control"]')
        input_fields._set_value([name, email, password])

        register_button = WebElement(self._web_driver, xpath='//div[@class="registration-actions r-text"]/button[@class="ek-form-btn blue" and @type="submit"]')
        register_button.click()

    def get_errors(self):
        errors = ManyWebElements(self._web_driver, xpath='//div[@class="ek-form-text"]')
        return errors.get_text()
