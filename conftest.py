import pytest
import subprocess
import sys
import os
import shutil
import allure
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config_reader import config as test_config
from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)


def pytest_configure(config):
    """在 pytest 配置阶段设置结果目录"""
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.environ["PYTHONUTF8"] = "1"
    
    if os.path.exists("allure-results"):
        shutil.rmtree("allure-results")
    os.makedirs("allure-results", exist_ok=True)

    os.environ["ALLURE_RESULTS_DIR"] = "allure-results"

    logger.info(f"当前测试环境: {test_config.current_env}")
    logger.info(f"当前环境URL: {test_config.base_url}")
    logger.info(f"浏览器模式: {'无头模式' if test_config.headless else '有头模式'}")
    logger.info("本次测试数据将保存到: allure-results")


@pytest.fixture(scope="session")
def playwright_session():
    """Playwright 会话，整个测试周期只启动一次"""
    p = sync_playwright().start()
    yield p
    p.stop()

@pytest.fixture(scope="session")
def browser(playwright_session):
    """浏览器实例，整个测试周期复用"""
    headless = os.getenv(
        "HEADLESS",
        str(test_config.headless)
    ).lower() == "true"

    browser_name = os.getenv(
        "BROWSER",
        test_config.browser
)
    logger.info(f"浏览器: {browser_name}")
    logger.info(f"Headless: {headless}")

    browser = getattr(
        playwright_session,
        browser_name
    ).launch(headless=headless)

    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    """每个测试函数创建新页面"""
    page = browser.new_page()
    page.set_default_timeout(test_config.timeout)
    yield page
    page.close()


@pytest.fixture(scope="function")
def logged_in_page(page):
    """自动登录后的页面对象"""
    login_page = LoginPage(page)
    username = os.getenv("TEST_USER", test_config.username)
    password = os.getenv("TEST_PASSWORD", test_config.password)
    login_page.login(username, password)
    logger.info(f"已自动登录用户: {username}")
    yield page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图并附加到 Allure 报告"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        os.makedirs("screenshots", exist_ok=True)
        page = item.funcargs.get("page")
        if page:
            screenshot_path = f"screenshots/{item.name}.png"
            try:
                page.screenshot(path=screenshot_path, full_page=True, timeout=15000)
                logger.error(f"\n截图已保存: {screenshot_path}")

                with open(screenshot_path, "rb") as image_file:
                    allure.attach(
                        image_file.read(),
                        name=f"Failed_Screenshot_{item.name}",
                        attachment_type=allure.attachment_type.PNG
                    )
            except Exception as e:
                logger.error(f"\n截图失败: {e}")


def pytest_sessionfinish(session, exitstatus):
    """测试会话结束后自动生成报告"""
    # 创建 environment.properties 文件
    env_file_path = os.path.join("allure-results", "environment.properties")
    # 从环境变量或配置中获取浏览器信息
    browser_name = os.getenv("BROWSER", test_config.browser)
    headless = os.getenv("HEADLESS", str(test_config.headless)).lower() == "true"
    with open(env_file_path, "w", encoding="utf-8") as f:
        f.write(f"Environment={test_config.current_env}\n")
        f.write(f"BaseURL={test_config.base_url}\n")
        f.write(f"Browser={browser_name}\n")
        f.write(f"Headless={headless}\n")
        f.write(f"Timeout={test_config.timeout}\n")
        f.write(f"PythonVersion=3.12\n")
        f.write(f"PytestVersion=8.4.1\n")

    # 保存 history 到 allure-results（支持 Trend 功能）
    history_src = os.path.join("allure-report", "history")
    history_dest = os.path.join("allure-results", "history")
    if os.path.exists(history_src):
        if os.path.exists(history_dest):
            shutil.rmtree(history_dest)
        shutil.copytree(history_src, history_dest)

    logger.info("\n正在生成 Allure 报告...")
    try:
        result = subprocess.run(
            "allure generate allure-results -o allure-report --clean",
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            logger.info("报告生成完成！数据来源: allure-results")
            logger.info("报告已保存到: allure-report")
            logger.info("如需查看报告，请手动运行: allure serve allure-results")
        else:
            logger.error(f"报告生成失败: {result.stderr}")
    except Exception as e:
        logger.error(f"生成报告时出错: {e}")