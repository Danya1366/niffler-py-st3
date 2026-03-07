import allure
import pytest

from clients.spends_client import SpendsHttpClient
from databases.spend_db import SpendDb
from models.config import Envs


@allure.title('Http клиент')
@pytest.fixture()
def spends_client(envs: Envs, auth, playwright) -> SpendsHttpClient:
    return SpendsHttpClient(envs, auth, playwright)


@allure.title('Таблица в БД для трат')
@pytest.fixture()
def spend_db(envs) -> SpendDb:
    return SpendDb(envs)