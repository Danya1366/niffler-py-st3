import allure
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ProfilePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.username_input = page.locator("//*[@id='username']")
        self.name_input = page.locator('[name="name"]')
        self.save_changes_btn = page.get_by_text('Save changes')
        self.success_alert = page.get_by_test_id("SuccessOutlinedIcon")
        self.category_input = page.locator('[name="category"]')
        self.alert_added_new_category = page.get_by_role("alert")
        self.category_block = page.locator("div.MuiGrid-item")
        self.archive_checkbox = page.get_by_role("checkbox", name="Show archived")
        self.btn_archive = page.get_by_role('button', name="Archive")

    @allure.step('Заполнить поле name в профиле')
    def input_user_name(self, name: str):
        expect(self.name_input).to_be_visible()
        self.name_input.click()
        self.name_input.fill(name)
        return self

    @allure.step('Удалить данные в поле name')
    def delete_profile_name(self):
        self.name_input.click(click_count=3)
        self.name_input.press('Delete')
        expect(self.name_input).to_have_value('')
        self.save_changes_btn.click()
        expect(self.success_alert).to_be_visible()
        return self

    @allure.step('Добавить новую категорию')
    def add_new_category(self, category_name: str):
        expect(self.category_input).to_be_visible()
        self.category_input.fill(category_name)
        self.category_input.press("Enter")
        return self

    @allure.step('Проверяем, что категория добавлена')
    def expect_added_category(self, category_name: str):
        expect(self.alert_added_new_category).to_contain_text(
            f"You've added new category: {category_name}")
        expect(self.get_category_block_by_name(category_name)).to_be_visible()
        expect(self.get_category_block_by_name(category_name)).to_contain_text(category_name)
        return self

    @allure.step('Получить блок категория по названию')
    def get_category_block_by_name(self, category_name: str):
        return self.category_block.filter(
            has=self.page.get_by_text(category_name, exact=True)
        )

    @allure.step('Проверить данные пользователя')
    def expect_profile_data(self, username: str):
        expect(self.username_input).to_be_visible()
        expect(self.username_input).to_have_value(username)
        return self

    @allure.step('Добавить имя в профиль пользователя и сохранить')
    def add_name_in_profile(self, name: str):
        expect(self.name_input).to_be_visible()
        self.name_input.click()
        self.name_input.fill(name)
        self.save_changes_btn.click()
        expect(self.success_alert).to_be_visible()
        return self

    @allure.step('удалить Имя пользователя и проверить удаление')
    def delete_added_profile_name(self):
        self.delete_profile_name()
        self.page.reload()
        return self

    @allure.step('Проверяем что добавленное имя удалено')
    def expect_deleted_profile_name(self):
        expect(self.name_input).to_be_empty()
        return self

    @allure.step('Заархивировать категорию')
    def archive_category(self, category_name: str):
        archive_button = self.get_category_block_by_name(category_name).get_by_label("Archive category")
        archive_button.click()
        self.btn_archive.click()
        return self

    @allure.step('Проверяем что категория не отображается')
    def expect_arсhive_category(self, category_name: str):
        expect(self.get_category_block_by_name(category_name)).not_to_be_visible()
        return self
