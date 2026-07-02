from pages.base_page import BasePage
class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.product_list = page.locator("[data-test='inventory-list'] .inventory_item")
        self.add_to_cart_button = page.locator("#add-to-cart")
        self.back_to_products_button = page.locator("#back-to-products")
        self.cart_button = page.locator("[data-test='shopping-cart-link']")
        self.cart_count = page.locator("[data-test='shopping-cart-badge']")
        self.cart_item = page.locator("[data-test='inventory-item']")
        self.cart_item_name = page.locator("[data-test='inventory-item-name']")
        self.cart_item_price = page.locator("[data-test='inventory-item-price']")
        
        

#   获取商品列表
    def get_product_by_index(self, index):
        return self.product_list.nth(index)
#   获取商品名称
    def get_product_name_by_index(self, index):
        return self.product_list.nth(index).locator(".inventory_item_name")
#   获取商品价格
    def get_product_price_by_index(self, index):
        return self.product_list.nth(index).locator(".inventory_item_price")
#   获取商品价格文本
    def get_product_price_text_by_index(self, index):
        price_text = self.product_list.nth(index).locator(".inventory_item_price").text_content()
        return float(price_text.split("$")[-1])

#   点击商品
    def click_product_by_index(self, index):
        self.product_list.nth(index).locator(".inventory_item_name").click()
#   在列表中点击添加到购物车按钮
    def add_to_cart_by_index(self, index):
        self.product_list.nth(index).locator("button").click()
#   在详情页点击添加到购物车按钮
    def add_to_cart(self):
        self.click(self.add_to_cart_button)
#   点击购物车图标
    def click_cart(self):
        self.click(self.cart_button)
#   获取商品数量
    def get_product_count(self):
        return self.product_list.count()
#   返回首页
    def back_to_products(self):
        self.click(self.back_to_products_button)
        
       
        
        



