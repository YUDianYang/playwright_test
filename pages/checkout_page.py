from pages.base_page import BasePage
class CheckoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.checkout_button = page.locator("#checkout")
        self.first_name_input = page.locator("#first-name")
        self.last_name_input = page.locator("#last-name")
        self.postal_code_input = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")
        self.checkout_title = page.locator("[data-test ='title']")
        self.item_total = page.locator("[data-test='subtotal-label']")
        self.complete_header = page.locator("[data-test='complete-header']")
        self.finish_button = page.locator("#finish")
        self.back_home_button =page.locator("[data-test ='back-to-products']")

# 点击结账按钮
    def click_checkout_button(self):
        self.checkout_button.click()
#  填写结账表单信息
    def fill_checkout_form(self, first_name, last_name, zip_code):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(zip_code)
# 点击继续按钮
    def click_continue_button(self):
        self.continue_button.click()

# 获取商品总金额
    def get_item_total_price(self):
        full_text = self.item_total.text_content()
        return float(full_text.split("$")[-1])
    
# 点击完成按钮
    def click_finish_button(self):
        self.finish_button.click()
    
# 获取订单完成标题
    def get_complete_header(self):
        return self.complete_header.text_content()
        
# 点击返回首页按钮
    def click_back_home_button(self):
        self.back_home_button.click()
