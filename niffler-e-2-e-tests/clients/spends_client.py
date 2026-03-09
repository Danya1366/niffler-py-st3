import allure
import json

import requests
from playwright.sync_api import APIResponse
from typing import Optional, Dict

from models.config import Envs
from models.spend import Spend, SpendAdd
from models.category import Category
from utils.sessions import BaseSession


class SpendsHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, envs: Envs, token: str):
        self.session = BaseSession(base_url=envs.gateway_url)
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        )

    def _make_request(self, method: str, url: str, data: Optional[Dict] = None,
                      params: Optional[Dict] = None) -> APIResponse:
        # Логируем запрос
        if data:
            allure.attach(json.dumps(data, indent=2), name="Request body", attachment_type=allure.attachment_type.JSON)
        if params:
            allure.attach(json.dumps(params, indent=2), name="Request params",
                          attachment_type=allure.attachment_type.JSON)

        # Выполняем запрос
        kwargs = {k: v for k, v in [('data', data and json.dumps(data)),
                                    ('params', params)] if v}
        response = getattr(self.session, method.lower())(url, **kwargs)

        # Логируем ответ
        allure.attach(f"Method: {method.upper()}\nURL: {response.url}\nStatus: {response.status}",
                      name="Response Info",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text(), name="Response Body", attachment_type=allure.attachment_type.TEXT)

        return response

    def get_categories(self) -> list[Category]:
        with allure.step('оплучить категорию трат по API'):
            response = self.session.get("/api/categories/all")
            # self.raise_for_status(response)
            return [Category.model_validate(item) for item in response.json()]

    def add_category(self, name: str) -> Category:
        response = self.session.post("/api/categories/add", json={
            "name": name
        })
        return Category.model_validate(response.json())

    def add_spends(self, spend: SpendAdd) -> Spend:
        with allure.step('Добавить трату по API'):
            spend_data = SpendAdd.model_validate(spend)
            response = self.session.post("/api/spends/add", json=spend_data.model_dump())
            return Spend.model_validate(response.json())

    def get_spends(self) -> list[Spend]:
        response = self.session.get("/api/spends/all")
        return [Spend.model_validate(item) for item in response.json()]

    def get_all_spendings(self) -> list[Spend]:
        with allure.step('Получить все траты по API'):
            response = self.session.get("/api/v2/spends/all")
            # self.raise_for_status(response)
            return [Spend.model_validate(item) for item in response.json()["content"]]

    def remove_spends(self, ids: list[str]):
        with allure.step('Удалить трату по API'):
            ids_param = ",".join(ids)
            response = self.session.delete("/api/spends/remove", params={"ids": ids_param})
            # self.raise_for_status(response)

    def delete_all_spendings(self):
        with allure.step('Удалить все траты по API, если они есть'):
            all_spendings = self.get_all_spendings()
            spending_ids = [spending.id for spending in all_spendings]
            if spending_ids:
                self.remove_spends(spending_ids)

    # @staticmethod
    # def raise_for_status(response: APIResponse):
    #     if not response.ok:
    #         raise Exception(f"{response.status_code}")
