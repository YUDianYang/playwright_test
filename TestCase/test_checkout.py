"""
测试结账功能
流程:
1.自动登录(通过 fixture)
2.添加商品到购物车
3.点击结账按钮
4.填写结账表单信息
5.点击继续按钮
6.验证商品总金额正确
7.点击完成按钮
8.验证订单信息正确
9.点击返回首页按钮
10.验证购物车数量减少
"""


from typing import Any


import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.checkout_page import CheckoutPage
from pages.product_page import ProductPage
import allure
import yaml
from playwright.sync_api import expect
from utils.logger import get_logger

logger = get_logger(__name__)

def load_checkout_data():
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_data/test_checkout.yaml")
    with open(data_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)["checkout"]


@pytest.fixture(params=load_checkout_data())
def checkout_case(request):
    return request.param


@allure.title("结账功能测试")
def test_checkout(logged_in_page, checkout_case):
    test_data = checkout_case
    # 使用 logged_in_page fixture，自动完成登录
   
    product_page = ProductPage(logged_in_page)
    
    product_indices = test_data["product_indices"]
    expected_count = len(product_indices)
    
    with allure.step(f"获取{expected_count}个商品价格并计算总价"):
        prices = []
        for i, index in enumerate[Any](product_indices):
            price = product_page.get_product_price_text_by_index(index)
            prices.append(price)
            logger.info(f"商品{i+1}价格: ${price}")
        expected_total = sum(prices)
        logger.info(f"预期总价: ${expected_total}")

    with allure.step(f"添加{expected_count}个商品到购物车"):
        for index in product_indices:
            product_page.add_to_cart_by_index(index)

    with allure.step(f"验证购物车图标数量为{expected_count}个"):
        expect(product_page.cart_count).to_be_visible()
        expect(product_page.cart_count).to_have_text(str(expected_count))
        
    with allure.step("点击购物车图标"):
        product_page.click_cart()
        
    checkout_page = CheckoutPage(logged_in_page)
    with allure.step("点击结账按钮"):
        checkout_page.click_checkout_button()

    with allure.step("填写结账表单信息"):
        checkout_page.fill_checkout_form(test_data["first_name"], test_data["last_name"], test_data["zip_code"])

    with allure.step("点击继续按钮"):
        checkout_page.click_continue_button()

    with allure.step("验证商品总金额正确"):
        actual_total = checkout_page.get_item_total_price()
        logger.info(f"实际总价: ${actual_total}")
        assert actual_total == expected_total, f"总价不匹配: 期望 ${expected_total}, 实际 ${actual_total}"
        
    with allure.step("点击完成按钮"):
        checkout_page.click_finish_button()

    with allure.step("验证订单完成标题正确"):
        logger.info(f"订单完成标题: {checkout_page.get_complete_header()}")
        assert checkout_page.get_complete_header() == test_data["complete_header"]

    with allure.step("点击返回首页按钮"):
        checkout_page.click_back_home_button()

    with allure.step("验证购物车图标数量清空"):
        expect(product_page.cart_count).not_to_be_visible()

    allure.dynamic.title(test_data["name"])

if __name__ == "__main__":
    pytest.main([__file__, "-v"])