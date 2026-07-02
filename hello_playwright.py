
import pytest
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect, Page

# with sync_playwright() as p:
#     # 打开浏览器
#      browser = p.chromium.launch(headless=False)
#      page = browser.new_page()
def test_login_failed(page: Page):
    # 打开SauceDemo练习网站
     page.goto("https://www.saucedemo.com")
    
 # 输入用户名和密码
    #  page.get_by_role("textbox",name="Username").fill("standard_user")
    #  page.get_by_role("textbox",name="Password").fill("secret_sauce")
    #  page.get_by_placeholder("Username").fill("standard_user")
    #  page.get_by_placeholder("Password").fill("secret_sauce")
     page.locator("//*[@id='user-name']").fill("standard_user")
     page.locator("#password").fill("secret_sauce")

    
    # 点击登录按钮
    #  page.click("#login-button")
     page.locator("#login-button").click()
     # 打印页面标题，确认登录成功
     
    #  print("登录成功！" if "Products" in page.content() else "登录失败")
     expect(page.locator(".title")).to_have_text("Products123")
     expect(page.locator(".inventory_item")).to_have_count(5)
     items = page.locator(".inventory_item")
     print(f"页面上有 {items.count()} 个商品")
   
    # # 关闭浏览器
    #  browser.close()