from playwright.sync_api import Page, expect


class ProfilePage:
    def __init__(self, page: Page):
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

    def input_user_name(self, name: str):
        expect(self.name_input).to_be_visible()
        self.name_input.click()
        self.name_input.fill(name)
        return self

    def delete_profile_name(self):
        self.name_input.click(click_count=3)
        self.name_input.press('Delete')
        expect(self.name_input).to_have_value('')
        self.save_changes_btn.click()
        expect(self.success_alert).to_be_visible()
        return self

    def add_new_category(self, category_name: str):
        expect(self.category_input).to_be_visible()
        self.category_input.fill(category_name)
        self.category_input.press("Enter")
        expect(self.alert_added_new_category).to_contain_text(
            f"You've added new category: {category_name}")
        return self

    def get_category_block_by_name(self, category_name: str):
        return self.category_block.filter(
            has=self.page.get_by_text(category_name, exact=True)
        )
