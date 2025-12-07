import pytest
from pages.login_page import LoginPage
from config import TestUsers, URLs

TEST_USER = "Test User 5"
TEST_PASSWORD = "123321"
EXPECTED_URL_AFTER_LOGIN = "http://frontend.niffler.dc/main"


@pytest.fixture
def auth(page):
    login_page = LoginPage(page)
    login_page.navigate_to_login().verify_form_visible()
    login_page.login(TestUsers.USER_2["username"], TestUsers.USER_2["password"])

    page.wait_for_url(URLs.base_URL + URLs.main, timeout=10000)

    return page



