from locale import currency

import allure

from grpc_proto.internal.pb.niffler_currency_pb2 import CurrencyValues
from grpc_proto.internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from google.protobuf import empty_pb2


@allure.feature('Вся валюта')
@allure.story('grpc')
class TestGrpcAllCurrencies:
    @allure.title('Получение всех доступных валют')
    def test_get_all_currencies(self, grpc_client: NifflerCurrencyServiceClient) -> None:
        response = grpc_client.get_all_currencies(empty_pb2.Empty())
        assert len(response.allCurrencies) == 4
        currency = [c.currency for c in response.allCurrencies]
        assert CurrencyValues.KZT in currency
        assert CurrencyValues.USD in currency
        assert CurrencyValues.EUR in currency
        assert CurrencyValues.RUB in currency

    @allure.title('Получаем значения всех валют')
    def test_get_currency_rate(self, grpc_client: NifflerCurrencyServiceClient) -> None:
        expected_currencies_rate = {
            CurrencyValues.RUB: 0.015,
            CurrencyValues.KZT: 0.0021,
            CurrencyValues.EUR: 1.08,
            CurrencyValues.USD: 1.0
        }
        response = grpc_client.get_all_currencies(empty_pb2.Empty())
        response_currencies = {c.currency: c.currencyRate for c in response.allCurrencies}
        assert response_currencies[CurrencyValues.RUB] == expected_currencies_rate[CurrencyValues.RUB]
        assert response_currencies[CurrencyValues.KZT] == expected_currencies_rate[CurrencyValues.KZT]
        assert response_currencies[CurrencyValues.EUR] == expected_currencies_rate[CurrencyValues.EUR]
        assert response_currencies[CurrencyValues.USD] == expected_currencies_rate[CurrencyValues.USD]
