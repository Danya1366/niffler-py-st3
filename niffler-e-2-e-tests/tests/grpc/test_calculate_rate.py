import allure
import grpc
import pytest

from grpc_proto.internal.pb.niffler_currency_pb2 import CalculateRequest, CurrencyValues
from grpc_proto.internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient


@allure.feature('Обмен валюты')
@allure.story('GRPC')
class TestGrpc:
    @allure.title('Обмен валюты из EUR в RUB')
    def test_calculate_rate(self, grpc_client: NifflerCurrencyServiceClient) -> None:
        response = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=CurrencyValues.EUR,
                desiredCurrency=CurrencyValues.RUB,
                amount=100.0
            )
        )
        assert response.calculatedAmount == 7200, "Expected 7200"

    @allure.title('Обмен валюты из RUB, в неуказанную валюту')
    def test_calculate_rate_without_desired_currency(self, grpc_client: NifflerCurrencyServiceClient) -> None:
        try:
            response = grpc_client.calculate_rate(
                request=CalculateRequest(
                    desiredCurrency=CurrencyValues.RUB,
                    amount=100.0
                )
            )
        except grpc.RpcError as e:
            assert e.code() == grpc.StatusCode.UNKNOWN
            assert e.details() == "Application error processing RPC"

    @pytest.mark.parametrize("spend, spend_currency, desired_currency, expected_result", [
        (100.0, CurrencyValues.USD, CurrencyValues.RUB, 6666.67),
        (100.0, CurrencyValues.RUB, CurrencyValues.USD, 1.5),
        (100.0, CurrencyValues.USD, CurrencyValues.USD, 100.0), ],
                             ids=["USD_to_RUB", "RUB_to_USD", "USD_to_USD"])
    def test_currency_conversion(self, grpc_client: NifflerCurrencyServiceClient, spend: float,
                                 spend_currency: CurrencyValues,
                                 desired_currency: CurrencyValues, expected_result: float):
        allure.dynamic.title(f'Обмен валюты из валюты {spend_currency} в валюту {desired_currency}')
        response = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=spend_currency,
                desiredCurrency=desired_currency,
                amount=spend
            )
        )
        assert response.calculatedAmount == expected_result, f"Expected {expected_result}"

    @allure.title('Обмен валюты из KZT в USD, с отрицательным значением')
    def test_currency_exchange_negative_amount(self, grpc_client: NifflerCurrencyServiceClient):
        response = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=CurrencyValues.KZT,
                desiredCurrency=CurrencyValues.USD,
                amount=-99.9
            )
        )
        assert response.calculatedAmount == -0.21, "Expected -0.21"

    @allure.title('Обмен валюты из KZT в USD, c нулевым значение')
    def test_currency_exchange_zero_amount(self, grpc_client: NifflerCurrencyServiceClient):
        response = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=CurrencyValues.KZT,
                desiredCurrency=CurrencyValues.USD,
                amount=0
            )
        )
        assert response.calculatedAmount == 0, "Expected 0"
