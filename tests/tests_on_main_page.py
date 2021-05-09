from pages.main_page import MainPage
from pages.elements import WebElement, ManyWebElements
from data import valid_email_1, valid_password, valid_email_2, invalid_password
from data import iduw
import pytest
import time


def test_access_to_main_page(web_browser):
    """ Check that page is accessable. """
    page = MainPage(web_browser)

    assert "e-katalog" in page.get_current_url()
    time.sleep(1)


@pytest.mark.parametrize("custom_input", [
    ("SeleniumTest", valid_email_1, valid_password),
    ("SeleniumTest1", valid_email_1, valid_password),
    ("SeleniumTest2", valid_email_2, valid_password),
], ids=["good params", "good params with another nick", "good params"])
def test_register_user_good_input(web_browser, custom_input):
    """ Trying to register with my data. """
    page = MainPage(web_browser)
    page.click_enter_button()
    page.register_user(*custom_input)

    assert page.nickname_button().get_text() != "Войти"


@pytest.mark.parametrize("custom_input,error", [
    (("SeleniumTest", valid_email_1, invalid_password), 'На этот email уже зарегистрирован аккаунт'),
    (("SeleniumTest1", valid_email_2, invalid_password), 'На этот email уже зарегистрирован аккаунт'),
    (("<script>alert('0');</script>", valid_email_1, invalid_password), 'Поле "Имя" содержит недопустимые символы'),
], ids=["bad params", "bad params","good params with bad nick"])
def test_register_user_bad_input(web_browser, custom_input, error):
    """ Trying to register with my data. """
    page = MainPage(web_browser)
    page.click_enter_button()
    page.register_user(*custom_input)
    errors = ManyWebElements(web_browser, xpath='//div[@class="ek-form-text"]')

    assert error in errors.get_text()
