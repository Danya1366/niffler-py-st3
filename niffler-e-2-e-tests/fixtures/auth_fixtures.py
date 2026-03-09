# import allure
# import pytest
# from allure_commons.types import AttachmentType
# from playwright.async_api import expect
#
#
# @allure.title('Авторизация и получение токена')
# @pytest.fixture(scope="function")
# def auth(page, envs):
#     page.goto(envs.frontend_url)
#     page.get_by_placeholder('Type your username').fill(envs.test_username)
#     page.get_by_placeholder('Type your password').fill(envs.test_password)
#     page.locator('.form__submit').click()
#     page.wait_for_url(f"{envs.frontend_url}/main")
#     expect(page.get_by_text("History of Spendings")).to_be_visible()
#     token = page.evaluate("() => localStorage.getItem('id_token')")
#     allure.attach(token, name="token.txt", attachment_type=AttachmentType.TEXT)
#     return token

import pytest
from clients.oauth_client import OAuthClient
from models.config import Envs


@pytest.fixture(scope="session")
def auth(envs: Envs):
    return OAuthClient(envs).get_token(envs.test_username, envs.test_password)