import allure
from allure import step

import requests
from playwright.sync_api import APIResponse
from typing import Optional, Dict

from models.config import Envs
from models.spend import Spend, SpendAdd, SpendEdit
from models.category import CategorySQL
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

    def get_categories(self) -> list[CategorySQL]:
        with allure.step('оплучить категорию трат по API'):
            response = self.session.get("/api/categories/all")
            return [CategorySQL.model_validate(item) for item in response.json()]

    def add_category(self, name: str) -> CategorySQL:
        response = self.session.post("/api/categories/add", json={
            "name": name
        })
        return CategorySQL.model_validate(response.json())

    def edit_category(self, category):
        category_data = CategorySQL.model_validate(category)
        response = self.session.patch("/api/categories/update", json=category_data.model_dump())
        response.raise_for_status()
        return CategorySQL.model_validate(response.json())

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
            return [Spend.model_validate(item) for item in response.json()["content"]]

    def remove_spends(self, ids: list[str]):
        with allure.step('Удалить трату по API'):
            response = self.session.delete("/api/spends/remove", params={"ids": ids})
            return response

    def delete_all_spendings(self):
        with allure.step('Удалить все траты по API, если они есть'):
            all_spendings = self.get_all_spendings()
            spending_ids = [spending.id for spending in all_spendings]
            if spending_ids:
                self.remove_spends(spending_ids)

    def edit_spend(self, edit_spend: SpendEdit) -> Spend:
        response = self.session.patch("/api/spends/edit", data=edit_spend.model_dump_json())
        print(response.json())
        return Spend.model_validate(response.json())

    @step("Отправить запрос на редактирование категории")
    def edit_category(self, category):
        category_data = CategorySQL.model_validate(category)
        response = self.session.patch("/api/categories/update", json=category_data.model_dump())
        response.raise_for_status()
        return CategorySQL.model_validate(response.json())
