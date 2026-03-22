import pytest
from clients.oauth_client import OAuthClient
from models.config import Envs


@pytest.fixture(scope="session")
def auth_token(envs: Envs, create_test_user_before_run):
    return OAuthClient(envs).get_token(envs.test_username, envs.test_password)


@pytest.fixture(scope="session")
def auth_client(envs: Envs) -> OAuthClient:
    return OAuthClient(envs)
