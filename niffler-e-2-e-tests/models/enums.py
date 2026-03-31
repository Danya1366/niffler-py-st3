from dataclasses import dataclass
from utils.datatime_util import get_past_date_iso


@dataclass
class Category:
    SCHOOL = "school"


@dataclass
class Spendings:
    TEST_CATEGORY_1 = "категория 1"
    TEST_CATEGORY_2 = "категория 2"
    description = "QA>GURU Python Advanced 6"

    TestDataSpend = {
        "amount": "108.51",
        "description": description,
        "category":
            {"name": TEST_CATEGORY_1
             },
        "spendDate": "2024-08-08T18:39:27.955Z",
        "currency": "RUB"
    }

    TestDataSpend_1 = {
        "amount": "108.51",
        "description": description,
        "category":
            {"name": TEST_CATEGORY_2
             },
        "spendDate": "2024-08-08T18:39:27.955Z",
        "currency": "RUB"
    }


@dataclass
class Constants:
    TEST_CATEGORY_1 = "категория 1"
    TEST_CATEGORY = "school"
    TEST_CATEGORY_BD = "test_category_bd"

    edited_amount = "200.03"
    edited_category = 'Тестовая для проверки изменений'
    edited_description = 'Тест'

    amount_for_delete = "200.01"
    category_for_delete = "QA_GURU"
    description_for_delete = "Second Product"

    description = 'eddited category'
    amount1 = "108.51"
    amount2 = "99.99"

    amount_to_add = "100"
    category_to_add = "new category"
    description_to_add = "вчерашние траты"


@dataclass
class UserCreds:
    name = "test user"
    edited_name = "edited username"

@dataclass
class Currency:
    RUB = "RUB"
    KZT = "KZT"
    EUR = "EUR"
    USD = "USD"

@dataclass
class DataSpends:
    data_spend = {
        "amount": 101.1,
        "description": "test_description",
        "category": {
            "name": Constants.TEST_CATEGORY
        },
        "spendDate": get_past_date_iso(),
        "currency": Currency.RUB
    }

class CurrencyData:
    currency_data = {
        Currency.RUB: {"amount": 1000.50, "description": "Трата в рублях"},
        Currency.USD: {"amount": 100.75, "description": "Трата в долларах"},
        Currency.EUR: {"amount": 90.25, "description": "Трата в евро"},
        Currency.KZT: {"amount": 50000.00, "description": "Трата в тенге"}
    }

class SpendEditData:
    new_amount = 231
    new_description = "Зарплата"
    new_currency = Currency.EUR

