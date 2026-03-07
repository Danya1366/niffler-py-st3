import allure
import pytest

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.profile_page import ProfilePage
from pages.register_page import RegisterPage
from pages.spending_page import SpendingPage
from playwright.sync_api import Page



@allure.title('Получение main page')
@pytest.fixture()
def main_page(page: Page, auth, envs) -> MainPage:
    main_page = MainPage(page, envs.frontend_url)
    return main_page


@allure.title('Получение profile page')
@pytest.fixture()
def profile_page(page: Page, auth, envs) -> ProfilePage:
    profile_page = ProfilePage(page)
    return profile_page


@allure.title('Открытие profile page')
@pytest.fixture()
def open_profile_page(profile_page, envs):
    profile_page.go_to(envs.profile_url)
    profile_page.wait_for_load()


@allure.title('Получение spending page')
@pytest.fixture()
def spending_page(page: Page, auth, envs) -> SpendingPage:
    spending_page = SpendingPage(page, envs.frontend_url)
    return spending_page


@allure.title('Открытие spending page')
@pytest.fixture()
def open_spending_page(spending_page, envs):
    spending_page.go_to(envs.spending_url)
    spending_page.wait_for_load()


@allure.title('Открытие login page')
@pytest.fixture()
def open_login_page(login_page, envs):
    login_page.go_to(envs.auth_url)
    login_page.wait_for_load()


@allure.title('Получение login page')
@pytest.fixture()
def login_page(page: Page, envs) -> LoginPage:
    login_page = LoginPage(page, envs.frontend_url)
    return login_page


@allure.title('Получение register page')
@pytest.fixture()
def register_page(page: Page, envs) -> RegisterPage:
    register_page = RegisterPage(page, envs.frontend_url)
    return register_page
