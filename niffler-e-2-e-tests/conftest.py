import os

import allure
import pytest
from allure_commons.reporter import AllureReporter
from allure_commons.types import AttachmentType
from allure_pytest.listener import AllureListener
from pytest import FixtureDef, FixtureRequest
from playwright.sync_api import expect
from playwright.sync_api import Page

from databases.spend_db import SpendDb
from models.spend import CategoryAdd
from models.config import Envs

from clients.spends_client import SpendsHttpClient
from dotenv import load_dotenv
from pages.main_page import ProfilePage
from pages.spending_page import SpendingPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.main_page import MainPage


def allure_logger(config) -> AllureReporter:
    listener: AllureListener = config.pluginmanager.get_plugin("allure_listener")
    return listener.allure_logger


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    yield
    logger = allure_logger(request.config)
    item = logger.get_last_item()
    scope_letter = fixturedef.scope[0].upper()
    item.name = f"[{scope_letter}]" + " ".join(fixturedef.argname.split("_")).title()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_teardown(item):
    yield
    reporter = allure_logger(item.config)
    test = reporter.get_test(None)
    test.labels = list(filter(lambda x: x.name not in ("suite", "subSuite", "parentSuite"), test.labels))


@allure.title('Получаем переменные окружения')
@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    envs_instance = Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        auth_url=os.getenv("AUTH_URL"),
        login_url=os.getenv("LOGIN_URL"),
        register_url=os.getenv("REGISTER_URL"),
        profile_url=os.getenv("PROFILE_URL"),
        spending_url=os.getenv("SPENDING_URL"),
        main_page_url=os.getenv("MAIN_PAGE_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        test_password=os.getenv("TEST_PASSWORD"),
        test_username=os.getenv("TEST_USERNAME")
    )
    allure.attach(envs_instance.model_dump_json(indent=2), name="envs.json", attachment_type=AttachmentType.JSON)
    return envs_instance


@allure.title('Http клиент')
@pytest.fixture()
def spends_client(envs, auth, playwright) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, auth, playwright)


@allure.title('Таблица в БД для трат')
@pytest.fixture()
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spend_db_url)


@allure.title('Добавление категории трат')
@pytest.fixture(params=[])
def category(request, spends_client, spend_db):
    category_name = request.param
    category = spends_client.add_category(CategoryAdd(name=category_name))
    yield category.name
    spend_db.delete_category(category.id)


@allure.title('Авторизация и получение токена')
@pytest.fixture(scope="function")
def auth(page, envs):
    page.goto(envs.frontend_url)
    page.get_by_placeholder('Type your username').fill(envs.test_username)
    page.get_by_placeholder('Type your password').fill(envs.test_password)
    page.locator('.form__submit').click()
    page.wait_for_url(f"{envs.frontend_url}/main")
    expect(page.get_by_text("History of Spendings")).to_be_visible()
    token = page.evaluate("() => localStorage.getItem('id_token')")
    allure.attach(token, name="token.txt", attachment_type=AttachmentType.TEXT)
    return token


@allure.title('Добавление траты')
@pytest.fixture(params=[])
def spends(request, spends_client):
    spend = spends_client.add_spends(request.param)
    yield spend
    all_spend = spends_client.get_spends()
    if spend.id in [spend.id for spend in all_spend]:
        spends_client.remove_spends([spend.id])


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
