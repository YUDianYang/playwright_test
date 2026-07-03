import sys
import os
import yaml
import pytest
from playwright.sync_api import expect

# 添加项目根目录到路径（解决直接运行时的模块导入问题）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.login_page import LoginPage

print(os.getenv("TEST_USER"))

def load_logout_data():
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_data/login_data.yaml")
    with open(data_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)["login_out_tests"]


@pytest.fixture(params=load_logout_data())
def logout_case(request):
    return request.param


def test_login_out(logout_case, page):
    login_page = LoginPage(page)
    login_page.login(logout_case["username"], logout_case["password"])
    login_page.logout()
    expect(login_page.login_button).to_be_visible()

if __name__ == "__main__":
    pytest.main([__file__])