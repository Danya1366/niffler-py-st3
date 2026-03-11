import allure
from faker import Faker

from marks import Pages
from models.enums import UserCreds

fake = Faker("ru_RU")


@allure.feature('Профиль пользователя')
class TestProfile:
    @allure.story('Имя пользователя')
    @allure.title('Добавление имени для профиля пользователя')
    @Pages.open_profile_page
    def test_add_name(self, profile_page):
        with allure.step('Добавить имя в профиль пользователя'):
            profile_page.add_name_in_profile(UserCreds.name)
        with allure.step('Проверить отображение уведомлений об успешном сохранении'):
            assert profile_page.is_allert_visible

    @allure.story('Имя пользователя')
    @allure.title('Удаление имени профиля пользователя')
    @Pages.open_profile_page
    def test_delete_added_name(self, profile_page):
        with allure.step('Добавить имя в профиль пользователя'):
            profile_page.add_name_in_profile(UserCreds.name)
        with allure.step('Удалить имя из профиля пользователя'):
            profile_page.delete_added_profile_name()
        with allure.step('Првоерить что имя пользователя удалено'):
            assert profile_page.is_profile_name_deleted()

    @allure.story('Имя пользователя')
    @allure.title('Редактирование имени пользователя')
    @Pages.open_profile_page
    def test_edit_added_name(self, profile_page):
        with allure.step('Добавить имя в профиль пользователя'):
            profile_page.add_name_in_profile(UserCreds.name)
        with allure.step('Удалить имя из профиля пользователя'):
            profile_page.delete_profile_name()
        with allure.step('Добавить измененное имя в профиль пользователя'):
            profile_page.add_name_in_profile(UserCreds.edited_name)
        with allure.step('Првоерить что имя пользователя изменено'):
            assert profile_page.is_allert_visible

    @allure.story('Категории UI')
    @allure.title('Добавление категории')
    @Pages.open_profile_page
    def test_add_new_category(self, profile_page):
        category_name = fake.word()

        with allure.step('Добавить новую категорию'):
            profile_page.add_new_category(category_name)
        with allure.step('Проверить что категория добавлена'):
            assert profile_page.is_category_added(category_name)

    @allure.story('Категории UI')
    @allure.title('Архивация категории')
    @Pages.open_profile_page
    def test_archive_category(self, profile_page):
        category_name = fake.word()

        with allure.step('Добавить новую категорию и проверить добавление'):
            profile_page.add_new_category(category_name)
            assert profile_page.is_category_added(category_name)
        with allure.step('архивировать категорию'):
            profile_page.archive_category(category_name)
        with allure.step('Проверить что категория архивирована'):
            assert profile_page.is_category_archived(category_name)
