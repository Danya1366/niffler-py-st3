
from playwright.sync_api import expect
from .base_page import BasePage
from .login_page import LoginPage

class ProfilePage(BasePage):

    URL = "http://frontend.niffler.dc/profile"

    def __init__(self, page):
        super().__init__(page)
        self.person_icon = page.locator('[data-testid="PersonIcon"]')
        self.btn_upload_new_picture = page.locator('.image__input-label')
        self.profile_btn = page.locator('a[href="/profile"]')

    def go_to_profile(self):
        self.page.goto(self.URL)
        # self.profile_btn.click()

        return self




