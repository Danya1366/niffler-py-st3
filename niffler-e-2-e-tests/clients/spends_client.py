from urllib.parse import urljoin
from playwright.sync_api import APIResponse

from models.spend import Category, Spend, CategoryAdd, SpendAdd


class SpendsHttpClient:
    base_url: str

    def __init__(self, base_url: str, token: str, playwright):
        self.base_url = base_url
        self.session = playwright.request.new_context(
            base_url=base_url,
            extra_http_headers={
                'Accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )

    def get_categories(self) -> list[CategoryAdd]:
        response = self.session.get("/api/categories/all")
        self.raise_for_status(response)
        return [CategoryAdd.model_validate(item) for item in response.json()]

    def add_category(self, category: CategoryAdd) -> Category:
        response = self.session.post("/api/categories/add", data=category.model_dump())
        self.raise_for_status(response)
        return Category.model_validate(response.json())

    def add_spends(self, spend: dict) -> Spend:
        spend_data = SpendAdd.model_validate(spend)
        response = self.session.post("/api/spends/add", data=spend_data.model_dump())
        self.raise_for_status(response)
        return Spend.model_validate(response.json())

    def get_spends(self) -> list[Spend]:
        url = urljoin(self.base_url, "/api/spends/all")
        response = self.session.get(url)
        self.raise_for_status(response)
        return [Spend.model_validate(item) for item in response.json()]

    def get_all_spendings(self) -> list[Spend]:
        response = self.session.get("/api/v2/spends/all")
        self.raise_for_status(response)
        return [Spend.model_validate(item) for item in response.json()["content"]]

    def remove_spends(self, ids: list[str]):
        ids_param = ",".join(ids)
        response = self.session.delete("/api/spends/remove", params={"ids": ids_param})
        self.raise_for_status(response)

    @staticmethod
    def raise_for_status(response: APIResponse):
        if not response.ok:
            raise Exception(f"{response.status}")
