#!/usr/bin/python3
# -*- encoding=utf8 -*-

from pages.main_page import MainPage
from pages.elements import WebElement, ManyWebElements
from data import valid_email_1, valid_password_1


class ProfilePage(MainPage):

    def __init__(self, web_driver):
        super().__init__(web_driver)
        self.click_enter_button()
        self.login_with_email(valid_email_1, valid_password_1)
        self.nickname_button().click()

    def edit_profile(self, new_name='', gender='', birthyear='', email='', new_password='', confirm_password='', about_me=''):
        edit_button = WebElement(self._web_driver, xpath='//a[@class="user-menu__edit"]')
        edit_button.click()

        if new_name:
            nickname_field = WebElement(self._web_driver, xpath='//div[@class="ek-form-group"]/input[@class="ek-form-control"]')
            nickname_field.send_keys(new_name)

        gender = '' # TODO: not implemented
        if gender in ('M', 'F'):
            gender_button = WebElement(self._web_driver, id=f'geradio{gender.lower()}')
            gender_button.click()

        if birthyear:
            birthyears_select_list = ManyWebElements(self._web_driver, xpath=f'//select[@class="ek-form-control"]/option')
            if birthyear in birthyears_select_list.get_text():
                idx = birthyears_select_list.get_text().index(birthyear)
                birthyears_select_list[idx].click()
            else:
                pass

        if email:
            email_field = WebElement(self._web_driver, xpath='//input[@class="ek-form-control" and @type="email"]')
            email_field.send_keys(email)

        if new_password or confirm_password:
            WebElement(self._web_driver, xpath='//span[@class="j-wrap grey"]/em').click()
            passwords_field = ManyWebElements(self._web_driver, xpath='//div[@class="ek-form-group"]/input[@class="ek-form-control" and @type="password"]')
            passwords_field._set_value([new_password, confirm_password])

        if about_me:
            about_me_field = WebElement(self._web_driver, xpath='//textarea[@class="ek-form-control"]')
            about_me_field.send_keys(about_me)

        save_button = WebElement(self._web_driver, xpath='//div[@class="fl-r"]/button[@class="ek-form-btn blue"]')
        save_button.click()

