import allure
import pytest

from clients.spends_client import SpendsHttpClient
from databases.spend_db import SpendDb
from models.config import Envs


# @allure.title('Http клиент')
@pytest.fixture(scope="session")
def spends_client(envs: Envs, auth) -> SpendsHttpClient:
    return SpendsHttpClient(envs, auth)


# @allure.title('Таблица в БД для трат')
@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDb:
    return SpendDb(envs)