import pytest

from clients.spends_client import SpendsHttpClient
from databases.spend_db import SpendDb
from models.config import Envs


@pytest.fixture(scope="session")
def spends_client(envs: Envs, auth) -> SpendsHttpClient:
    return SpendsHttpClient(envs, auth)


@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDb:
    return SpendDb(envs)
