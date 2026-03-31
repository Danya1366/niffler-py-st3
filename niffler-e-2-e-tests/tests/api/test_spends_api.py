import allure
import pytest
from models.enums import Currency, Constants, DataSpends, CurrencyData, SpendEditData
from models.spend import SpendEdit
from utils.api_assertions import assertEqual, assertNotIn
from utils.datatime_util import get_past_date_iso

@pytest.mark.xdist_group("group2")
@allure.feature('Таблица трат')
@allure.story('API')
class TestSpendsApi:
    @allure.title('Создание траты через API')
    def test_add_spend_api(self, spends_client, envs, clean_categories, clean_spendings_setup):
        new_spend = spends_client.add_spends(DataSpends.data_spend)

        assertEqual(new_spend.amount, DataSpends.data_spend["amount"],
                    "В ответе приходит сумма, которую передавали при создании")
        assertEqual(new_spend.description, DataSpends.data_spend["description"],
                    "В ответе приходит описание, которое передавали при создании")
        assertEqual(new_spend.category.name, DataSpends.data_spend["category"]["name"],
                    "В ответе приходит имя категории, которое передавали при создании")
        assertEqual(str(new_spend.spendDate)[:10], DataSpends.data_spend["spendDate"][:10],
                    "В ответе приходит дата, которую передавали при создании")
        assertEqual(new_spend.currency, DataSpends.data_spend["currency"],
                    "В ответе приходит валюта, которую передавали при создании")

    @allure.title('Удаление траты через API')
    def test_delete_spend_api(self, spends_client, spend_db, envs, clean_categories):
        new_spend = spends_client.add_spends(DataSpends.data_spend)
        spends_client.remove_spends(new_spend.id)
        all_spends = spends_client.get_spends()

        assertNotIn(new_spend.id, [s.id for s in all_spends], "Созданная трата отсутствует")

    @allure.title('Редактирование траты через API')
    def test_edit_spend_api(self, spends_client, envs, clean_categories, clean_spendings_setup):
        new_spend = spends_client.add_spends(DataSpends.data_spend)

        edit_data = SpendEdit(id=new_spend.id,
                              spendDate=get_past_date_iso(),
                              amount=SpendEditData.new_amount,
                              category={
                                  "name": Constants.TEST_CATEGORY
                              },
                              description=SpendEditData.new_description,
                              currency=SpendEditData.new_currency)
        edited_spend = spends_client.edit_spend(edit_data)

        assertEqual(edited_spend.amount, SpendEditData.new_amount,
                    "В ответе приходит новая сумма для траты")
        assertEqual(edited_spend.description, SpendEditData.new_description,
                    "В ответе приходит новое описание")
        assertEqual(edited_spend.currency, SpendEditData.new_currency,
                    "В ответе приходит новая валюта")

    @allure.title('Создание траты со всеми поддерживаемыми валютами через API')
    @pytest.mark.parametrize("currency", [
        Currency.RUB,
        Currency.USD,
        Currency.EUR,
        Currency.KZT
    ])
    def test_add_spend_all_currencies_api(self, spends_client, envs, clean_categories, clean_spendings_setup, currency):
        amount = CurrencyData.currency_data[currency]["amount"]
        description = CurrencyData.currency_data[currency]["description"]
        currency_str = str(currency)

        data = {
            "amount": amount,
            "description": description,
            "category": {
                "name": Constants.TEST_CATEGORY
            },
            "spendDate": get_past_date_iso(),
            "currency": currency_str
        }
        new_spend = spends_client.add_spends(data)

        assertEqual(new_spend.amount, data["amount"],
                    "В ответе приходит сумма, которую передавали при создании")
        assertEqual(new_spend.description, data["description"],
                    "В ответе приходит описание, которое передавали при создании")
        assertEqual(new_spend.category.name, data["category"]["name"],
                    "В ответе приходит имя категории, которое передавали при создании")
        assertEqual(str(new_spend.spendDate)[:10], data["spendDate"][:10],
                    "В ответе приходит дата, которую передавали при создании")
        assertEqual(new_spend.currency, data["currency"],
                    "В ответе приходит валюта, которую передавали при создании")
