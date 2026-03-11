import allure
from models.category import CategorySQL
from models.enums import TestConstants
from utils.api_assertions import assertEqual, assertIsNotNone


@allure.feature('Категории')
@allure.story('API')
class TestCategoryApi:
    @allure.title('Создание категории через API')
    def test_add_category_api(self, spends_client, envs, clean_categories):

        added_category = spends_client.add_category(TestConstants.TEST_CATEGORY)

        assertEqual(added_category.name, TestConstants.TEST_CATEGORY,
                    "В ответе приходит имя категории, которое передавали при создании")
        assertEqual(added_category.username, envs.test_username,
                    "Категория закреплена за тестовым пользователем")

    @allure.title('Получение списка категорий через API')
    def test_get_categories_api(self, spends_client, envs, clean_categories):
        added_category_1 = spends_client.add_category(TestConstants.TEST_CATEGORY)
        added_category_2 = spends_client.add_category(TestConstants.TEST_CATEGORY_1)

        categories_list = spends_client.get_categories()

        assertIsNotNone(categories_list, "Список не пустой")
        assertEqual(added_category_1.name, categories_list[0].name, "Категория 1 есть в ответе")
        assertEqual(added_category_2.name, categories_list[1].name, "Категория 2 есть в ответе")

    @allure.title('Редактирование названия категории через API')
    def test_edit_category_name_api(self, spends_client, envs, clean_categories):
        added_category = spends_client.add_category(TestConstants.TEST_CATEGORY)

        edit_data = CategorySQL(id=added_category.id,
                                name=TestConstants.TEST_CATEGORY_1,
                                username=added_category.username,
                                archived=False)
        category_with_new_name = spends_client.edit_category(edit_data)

        assertEqual(category_with_new_name.name, TestConstants.TEST_CATEGORY_1,
                    "В ответе приходит имя категории, которое передавали при изменении")

    @allure.title('Помещение в архив категории через API')
    def test_edit_category_archive_api(self, spends_client, envs, clean_categories):
        added_category = spends_client.add_category(TestConstants.TEST_CATEGORY)

        edit_data = CategorySQL(id=added_category.id,
                                name=TestConstants.TEST_CATEGORY_1,
                                username=added_category.username,
                                archived=True)
        category_archived = spends_client.edit_category(edit_data)

        assertEqual(category_archived.archived, True, "Категория в архиве")