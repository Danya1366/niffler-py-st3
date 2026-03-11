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
        profile_page.add_name_in_profile(UserCreds.name)
        assert profile_page.is_allert_visible

    @allure.story('Имя пользователя')
    @allure.title('Удаление имени профиля пользователя')
    @Pages.open_profile_page
    def test_delete_added_name(self, profile_page):
        profile_page.add_name_in_profile(UserCreds.name)
        profile_page.delete_added_profile_name()
        assert profile_page.is_profile_name_deleted()

    @allure.story('Имя пользователя')
    @allure.title('Редактирование имени пользователя')
    @Pages.open_profile_page
    def test_edit_added_name(self, profile_page):
        profile_page.add_name_in_profile(UserCreds.name)
        profile_page.delete_profile_name()
        profile_page.add_name_in_profile(UserCreds.edited_name)
        assert profile_page.is_allert_visible

    @allure.story('Категории UI')
    @allure.title('Добавление категории')
    @Pages.open_profile_page
    def test_add_new_category(self, profile_page):
        category_name = fake.word()

        profile_page.add_new_category(category_name)
        assert profile_page.is_category_added(category_name)


    @allure.story('Категории UI')
    @allure.title('Архивация категории')
    @Pages.open_profile_page
    def test_archive_category(self, profile_page):
        category_name = fake.word()

        profile_page.add_new_category(category_name)
        assert profile_page.is_category_added(category_name)
        profile_page.archive_category(category_name)
        assert profile_page.is_category_archived(category_name)
