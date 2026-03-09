import allure
import pytest

from fixtures.client_fixtures import spends_client, spend_db

pytest_plugins = [
    "fixtures.auth_fixtures"
]


@allure.title('Добавление категории трат')
@pytest.fixture(params=[])
def category(request, spends_client, spend_db):
    category_name = request.param
    category = spends_client.add_category(category_name)
    yield category.name
    spend_db.delete_category(category.id)


@allure.title('Добавление траты')
@pytest.fixture(params=[])
def spends(request, spends_client):
    spend = spends_client.add_spends(request.param)
    yield spend
    all_spend = spends_client.get_spends()
    if spend.id in [spend.id for spend in all_spend]:
        spends_client.remove_spends([spend.id])

