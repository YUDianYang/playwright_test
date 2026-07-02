"""
测试添加商品到购物车功能
流程:
1.自动登录（通过 fixture）
2.添加商品到购物车
3.返回首页
4.验证购物车数量增加
5.点击购物车图标
6.验证购物车商品信息正确
"""
import sys
import os
import yaml
import pytest
from playwright.sync_api import expect

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.product_page import ProductPage
import allure


def load_add_to_cart_data():
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_data/test_add_to_cart.yaml")
    with open(data_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)["add_to_cart_tests"]


@pytest.fixture(params=load_add_to_cart_data())
def add_to_cart_case(request):
    return request.param


@allure.step("验证添加商品到购物车商品信息正确")
def test_add_to_cart(logged_in_page, add_to_cart_case):
    test_data = add_to_cart_case
    # 使用 logged_in_page fixture，自动完成登录
    product_page = ProductPage(logged_in_page)
    
    allure.dynamic.title(test_data["name"])

    with allure.step("验证商品名称正确价格正确"):
        expect(product_page.get_product_name_by_index(test_data["product_index"])).to_have_text(test_data["product_name"])
        expect(product_page.get_product_price_by_index(test_data["product_index"])).to_have_text(test_data["product_price"])
    
    with allure.step("点击商品"):
        product_page.click_product_by_index(test_data["product_index"])
    
    with allure.step("添加商品到购物车"):
        product_page.add_to_cart()
    
    with allure.step("点击返回首页按钮"):
        product_page.back_to_products()
    
    with allure.step("等待并验证购物车数量为1"):
        product_page.wait_visible(product_page.cart_count)
        expect(product_page.cart_count).to_have_text("1")
    
    with allure.step("点击购物车图标"):
        product_page.click_cart()

    with allure.step("验证购物车商品可见且名称正确"):
        product_page.wait_visible(product_page.cart_item)
        expect(product_page.cart_item).to_be_visible()
        expect(product_page.cart_item_name).to_have_text(test_data["product_name"])

    with allure.step("验证购物车商品价格正确"):
        expect(product_page.cart_item_price).to_have_text(test_data["product_price"])
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
