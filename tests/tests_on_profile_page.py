from pages.profile_page import ProfilePage
from pages.elements import WebElement
import pytest
import time
from data import valid_email_1, valid_password, valid_email_2, invalid_password


def test_access_to_my_profile(web_browser):
    """ Check my profile without cookie. Must be an error. """
    page = ProfilePage(web_browser)
    assert page.nickname_button().get_text() != "Войти"

    time.sleep(1)


def test_my_profile_without_cookie(web_browser):
    """ Check my profile without cookie. Must be an error. """
    page = ProfilePage(web_browser)
    page._web_driver.delete_all_cookies()
    page._web_driver.refresh()
    respond = WebElement(web_browser, xpath='//div[@class="message-block__title"]').get_text()
    assert respond == "Ошибка"


@pytest.mark.parametrize("custom_input,expected_respond", [
    (('', '', '', '', '', '', "<script>alert('0');</script>"), "Информация о пользователе успешно сохранена!"),
    (("SeleniumTest1", 'F', '1930+', '', '', '', ''), "Информация о пользователе успешно сохранена!"),
    (("123", "M", "2020", valid_email_1, valid_password, invalid_password, ''), "Информация о пользователе НЕ сохранена!"),
    (("SeleniumTest", "M", "1900", valid_email_1, valid_password, valid_password, ''), "Информация о пользователе успешно сохранена!"),
], ids=["good params", "good params", "bad params", "good params"])
def test_edit_profile(web_browser, custom_input, expected_respond):
    """ Check editing profile. """
    page = ProfilePage(web_browser)

    page.edit_profile(*custom_input[:-1])
    respond = WebElement(web_browser, xpath='//div[@class="page-title"]/h1').get_text()

    assert respond == expected_respond
