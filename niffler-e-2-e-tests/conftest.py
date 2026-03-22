import os

import allure
import pytest
from allure_commons.reporter import AllureReporter
from allure_commons.types import AttachmentType
from allure_pytest.listener import AllureListener
from pytest import FixtureDef, FixtureRequest
from playwright.sync_api import Browser

from clients.kafka_client import KafkaClient
from models.config import Envs
from dotenv import load_dotenv
from pages.login_page import LoginPage

pytest_plugins = [
    "fixtures.pages_fixtures"
]


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
        auth_db_url=os.getenv("AUTH_DB_URL"),
        test_password=os.getenv("TEST_PASSWORD"),
        test_username=os.getenv("TEST_USERNAME"),
        kafka_address=os.getenv("KAFKA_ADDRESS")
    )
    allure.attach(envs_instance.model_dump_json(indent=2), name="envs.json", attachment_type=AttachmentType.JSON)
    return envs_instance


@pytest.fixture(scope="session")
def setup_auth_state(browser: Browser, envs, tmp_path_factory):
    """Автоматически создает файл с состоянием авторизации перед всеми тестами"""
    temp_dir = tmp_path_factory.mktemp("auth_data")
    state_path = temp_dir / "niffler_user.json"

    context = browser.new_context()
    page = context.new_page()

    login_page = LoginPage(page, envs.frontend_url)
    login_page.go_to(envs.auth_url)
    login_page.log_in(envs.test_username, envs.test_password)
    login_page.expect_log_in(envs)

    context.storage_state(path=str(state_path))
    context.close()

    yield state_path


@allure.title('Страница с предустановленной авторизацией')
@pytest.fixture(scope="function")
def page_with_auth(browser: Browser, setup_auth_state):
    context = browser.new_context(storage_state=str(setup_auth_state))
    page = context.new_page()

    yield page

    context.close()


@allure.title('Удаление всех трат до и после теста')
@pytest.fixture(scope="function")
def clean_spendings_setup(spends_client):
    yield

    spends_client.delete_all_spendings()


@pytest.fixture(scope="session")
def kafka(envs):
    """Взаимодействие с Kafka"""
    with KafkaClient(envs) as k:
        yield k
