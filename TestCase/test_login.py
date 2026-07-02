import sys
import os
import yaml
import pytest
from playwright.sync_api import expect

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.login_page import LoginPage  
from config.config_reader import config as test_config


def load_login_data():
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_data/login_data.yaml")
    with open(data_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["login_tests"]


@pytest.fixture(params=load_login_data())
def login_case(request):
    return request.param


def test_login(page, login_case):
    login_page = LoginPage(page)
    login_page.login(login_case["username"], login_case["password"])
    
    if login_case["test_type"] == "success":
        expect(page).to_have_title(login_case["expected_title"])
    else:
        expect(login_page.error_message).to_have_text(login_case["expected_error"])
        expect(login_page.error_message).to_be_visible()

# if __name__ == "__main__":
#     pytest.main([__file__])



