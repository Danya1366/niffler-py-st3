import os
from urllib.parse import urljoin

import pytest
from playwright.sync_api import expect

from databases.spend_db import SpendDb
from models.spend import CategoryAdd
from models.config import Envs

from clients.spends_client import SpendsHttpClient
from dotenv import load_dotenv



TEST_USER = "Test User 5"
TEST_PASSWORD = "123321"
EXPECTED_URL_AFTER_LOGIN = "http://frontend.niffler.dc/main"


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        test_password=os.getenv("TEST_PASSWORD"),
        test_username=os.getenv("TEST_USERNAME")
    )

@pytest.fixture()
def spends_client(envs, auth, playwright) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, auth, playwright)

@pytest.fixture()
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spend_db_url)

@pytest.fixture(params=[])
def category(request, spends_client, spend_db):
    category_name = request.param
    category = spends_client.add_category(CategoryAdd(name=category_name))
    yield category.name
    spend_db.delete_category(category.id)

@pytest.fixture(scope="function")
def auth(page, envs):
    page.goto(envs.frontend_url)
    page.get_by_placeholder('Type your username').fill(envs.test_username)
    page.get_by_placeholder('Type your password').fill(envs.test_password)
    page.locator('.form__submit').click()
    page.wait_for_url(f"{envs.frontend_url}/main")
    expect(page.get_by_text("History of Spendings")).to_be_visible()

    token = page.evaluate("() => localStorage.getItem('id_token')")
    return token

@pytest.fixture(params=[])
def spends(request, spends_client):
    spend = spends_client.add_spends(request.param)
    yield spend
    all_spend = spends_client.get_spends()
    if spend.id in [spend.id for spend in all_spend]:
        spends_client.remove_spends([spend.id])


@pytest.fixture()
def main_page(page, auth, envs):
    page.goto(envs.frontend_url)

@pytest.fixture()
def profile_page(page, auth, envs):
    profile_url = urljoin(envs.frontend_url, "/profile")
    page.goto(profile_url)

@pytest.fixture()
def spending_page(page, auth, envs):
    spending_url = urljoin(envs.frontend_url, "/spending")
    page.goto(spending_url)


