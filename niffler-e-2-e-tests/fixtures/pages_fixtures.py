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
def main_page(envs, page_with_auth: Page) -> MainPage:
    return MainPage(page_with_auth, envs.frontend_url)


@allure.title('Получение profile page')
@pytest.fixture()
def profile_page(page_with_auth: Page, envs) -> ProfilePage:
    return ProfilePage(page_with_auth)


@allure.title('Открытие spending page')
@pytest.fixture()
def spending_page(page_with_auth: Page, envs) -> SpendingPage:
    return SpendingPage(page_with_auth, envs.frontend_url)


@allure.title('Получение login page')
@pytest.fixture()
def login_page(page, envs) -> LoginPage:
    return LoginPage(page, envs.frontend_url)

@allure.title('Получение login page')
@pytest.fixture()
def register_page(page: Page, envs) -> RegisterPage:
    return RegisterPage(page, envs.frontend_url)

@allure.title('Open main page')
@pytest.fixture()
def open_main_page(page_with_auth: Page, envs):
    page_with_auth.goto(envs.main_page_url)

@allure.title('Open spending page')
@pytest.fixture()
def open_spending_page(page_with_auth: Page, envs):
    page_with_auth.goto(envs.spending_url)

@allure.title('Открытие login page')
@pytest.fixture()
def open_login_page(page: Page, envs):
    page.goto(envs.login_url)

@allure.title('Открытие register page')
@pytest.fixture()
def open_register_page(page: Page, envs):
    page.goto(envs.register_url)


@allure.title('Открытие profile page')
@pytest.fixture()
def open_profile_page(page_with_auth: Page, envs):
    page_with_auth.goto(envs.profile_url)
