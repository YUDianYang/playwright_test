from playwright.sync_api import Page
from .base_page import BasePage
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config_reader import config

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.main_logout_button = page.get_by_role("button", name="Logout")
        self.error_message = page.locator("[data-test='error']")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.sidebar_logout_button = page.locator("#logout_sidebar_link")

    def login(self, username: str, password: str):
        self.goto(config.base_url)
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)

    def logout(self):
        self.click(self.menu_button)
        self.click(self.sidebar_logout_button)