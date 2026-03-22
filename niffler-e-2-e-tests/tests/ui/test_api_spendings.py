import allure

from marks import Pages, TestData
from models.enums import Spendings
from fixtures.pages_fixtures import main_page


@allure.feature('Добавление траты по api')
class TestSpendApi:
    @allure.title('Добавляем новую трату по апи и удаляем через ui')
    @Pages.open_main_page
    @TestData.category(Spendings.TEST_CATEGORY_1)
    @TestData.spends(Spendings.TestDataSpend)
    def test_spending_should_be_deleted(self, category, spends, main_page):
            assert main_page.is_description_in_table(Spendings.description)
            main_page.delete_spend(Spendings.TEST_CATEGORY_1)
            assert main_page.is_description_absent_in_table(Spendings.description)
