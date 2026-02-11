import os
from urllib.parse import urljoin

import pytest
from playwright.sync_api import expect

from clients.spends_client import SpendsHttpClient
from dotenv import load_dotenv
from pages.main_page import MainPage
from pages.spending_page import SpendingPage

TEST_USER = "Test User 5"
TEST_PASSWORD = "123321"
EXPECTED_URL_AFTER_LOGIN = "http://frontend.niffler.dc/main"


@pytest.fixture(scope="session")
def envs():
    load_dotenv()


@pytest.fixture(scope="session")
def frontend_url(envs):
    return os.getenv("FRONTEND_URL")


@pytest.fixture(scope="session")
def gateway_url(envs):
    return os.getenv("GATEWAY_URL")


@pytest.fixture(scope="session")
def app_user(envs):
    return os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD")


@pytest.fixture()
def spends_client(gateway_url, auth) -> SpendsHttpClient:
    return SpendsHttpClient(gateway_url, auth)


@pytest.fixture(params=[])
def category(request, spends_client):
    category_name = request.param
    current_categories = spends_client.get_categories()
    category_names = [name["name"] for name in current_categories]
    if category_name not in category_names:
        spends_client.add_category(category_name)
    return category_name


@pytest.fixture(scope="function")
def auth(page, frontend_url, app_user):
    username, password = app_user
    page.goto(frontend_url)
    page.get_by_placeholder('Type your username').fill(username)
    page.get_by_placeholder('Type your password').fill(password)
    page.locator('.form__submit').click()
    page.wait_for_url(f"{frontend_url}/main")
    expect(page.get_by_text("History of Spendings")).to_be_visible()

    token = page.evaluate("() => localStorage.getItem('id_token')")
    return token


@pytest.fixture(params=[])
def spends(request, spends_client):
    spend = spends_client.add_spends(request.param)
    yield spend
    try:
        spends_client.remove_spends([spend["id"]])
    except Exception:
        pass


@pytest.fixture()
def main_page(page, auth, frontend_url):
    page.goto(frontend_url)


@pytest.fixture()
def profile_page(page, auth, frontend_url):
    main_page = MainPage(page)
    main_page.go_to_profile()


@pytest.fixture()
def spending_page(page, auth, frontend_url) -> SpendingPage:
    spending_page = SpendingPage(page, frontend_url + "/spending")
    return spending_page
    # spending_url = urljoin(frontend_url, "/spending")
    # page.goto(spending_url)
