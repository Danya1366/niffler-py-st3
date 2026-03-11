import allure

from marks import TestData
from models.enums import TestConstants


@allure.feature('Категории')
class TestCategories:
    @allure.title('Добавление категорий и проверка базы данных')
    @TestData.category(TestConstants.TEST_CATEGORY_BD)
    def test_add_category_and_check_db(self, envs, category, spend_db):
        with allure.step('Получаем список категорий пользователя из бд'):
            user_categories = spend_db.get_user_categories(envs.test_username)
            user_category_names = [category.name for category in user_categories]
        with allure.step('Проверяем, что у пользователя больше одной категории'):
            assert len(user_categories) > 0, "Категорий у этого пользовтаеля нет"
            assert category in user_category_names

    @allure.title('Удаление категории из базы данных')
    def test_delete_category_and_check_db(self, envs, spend_db):
        with allure.step('Добавляем новую категорию пользователю'):
            new_category = spend_db.add_user_category(
                envs.test_username,
                TestConstants.TEST_CATEGORY_BD
            )
        with allure.step('Проверяем, что категория добавлена в БД'):
            search_before_delete = spend_db.get_category_by_id(new_category.id)
        with allure.step('Проверяем, что у пользователя есть категории'):
            assert search_before_delete.name == TestConstants.TEST_CATEGORY_BD
        with allure.step('Удаляем категорию из БД'):
            spend_db.delete_category(new_category.id)
        with allure.step('Проверяем, что у пользователя нет категорий, после удаления'):
            search_after_delete = spend_db.get_category_by_name(
                envs.test_username,
                new_category.name
            )
            assert search_after_delete is None