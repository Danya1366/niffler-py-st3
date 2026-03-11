import allure
from allure import step

import requests

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

    @allure.step('оплучить категорию трат по API')
    def get_categories(self) -> list[CategorySQL]:
        response = self.session.get("/api/categories/all")
        return [CategorySQL.model_validate(item) for item in response.json()]

    @allure.step('Добавить категорию')
    def add_category(self, name: str) -> CategorySQL:
        response = self.session.post("/api/categories/add", json={
            "name": name
        })
        return CategorySQL.model_validate(response.json())

    @allure.step('Изменить категорию')
    def edit_category(self, category):
        category_data = CategorySQL.model_validate(category)
        response = self.session.patch("/api/categories/update", json=category_data.model_dump())
        response.raise_for_status()
        return CategorySQL.model_validate(response.json())

    @allure.step('Добавить трату по API')
    def add_spends(self, spend: SpendAdd) -> Spend:
        spend_data = SpendAdd.model_validate(spend)
        response = self.session.post("/api/spends/add", json=spend_data.model_dump())
        return Spend.model_validate(response.json())

    @allure.step('Выполнить запрос на траты')
    def get_spends(self) -> list[Spend]:
        response = self.session.get("/api/spends/all")
        return [Spend.model_validate(item) for item in response.json()]

    @allure.step('Получить все траты по API')
    def get_all_spendings(self) -> list[Spend]:
        response = self.session.get("/api/v2/spends/all")
        return [Spend.model_validate(item) for item in response.json()["content"]]

    @allure.step('Удалить трату по API')
    def remove_spends(self, ids: list[str]):
        response = self.session.delete("/api/spends/remove", params={"ids": ids})
        return response

    @allure.step('Удалить все траты по API, если они есть')
    def delete_all_spendings(self):
        all_spendings = self.get_all_spendings()
        spending_ids = [spending.id for spending in all_spendings]
        if spending_ids:
            self.remove_spends(spending_ids)

    @allure.step('Обновить трату')
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
