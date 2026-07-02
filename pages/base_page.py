import time
from playwright.sync_api import Page, Locator
from playwright._impl._errors import TimeoutError
from config.config_reader import config

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self._timeout = config.timeout
        self._navigation_timeout = config.navigation_timeout

    def _get_locator(self, locator_or_selector):
        """统一处理选择器或 Locator 对象"""
        if isinstance(locator_or_selector, Locator):
            return locator_or_selector
        return self.page.locator(locator_or_selector)

    def wait_visible(self, locator, timeout=None):
        """等待元素可见"""
        if timeout is None:
            timeout = self._timeout
        self._get_locator(locator).wait_for(
            state="visible",
            timeout=timeout
        )

    def fill(self, locator, value: str):
        """填充输入框"""
        self._get_locator(locator).fill(value=value)

    def click(self, locator):
        """点击元素"""
        self._get_locator(locator).click()

    def goto(self, url: str, timeout: int = None, wait_until: str = "domcontentloaded"):
        """导航到指定 URL，包含重试逻辑"""
        if timeout is None:
            timeout = self._navigation_timeout
        max_retries = 2
        retry_interval = 2
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                self.page.goto(url, timeout=timeout, wait_until=wait_until)
                return
            except TimeoutError as e:
                last_error = e
                if attempt < max_retries:
                    time.sleep(retry_interval)
        raise last_error

    def verify_element_exists(self, locator):
        """验证元素存在"""
        self._get_locator(locator).wait_for(
            state="visible",
            timeout=self._timeout
        )

    def get_text(self, locator):
        """获取元素文本"""
        return self._get_locator(locator).inner_text()

    def refresh(self):
        """刷新页面"""
        self.page.reload()

    def back(self):
        """返回上一页"""
        self.page.go_back()

    def forward(self):
        """前进下一页"""
        self.page.go_forward()