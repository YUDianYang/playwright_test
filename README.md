================================================================================
                        Playwright 自动化测试框架说明
================================================================================

一、项目结构
--------------------------------------------------------------------------------
playwright_test/
├── conftest.py                 # pytest 配置文件，定义全局 fixture 和钩子
├── config/
│   ├── config.yaml             # 环境配置文件（test/staging/production）
│   ├── config_reader.py         # 配置读取器（单例模式）
│   └── __init__.py
├── pages/
│   ├── base_page.py             # 页面对象基类，封装公共操作
│   ├── login_page.py            # 登录页面对象
│   ├── product_page.py          # 产品页面对象
│   ├── checkout_page.py         # 结账页面对象
│   └── __init__.py
├── TestCase/
│   ├── test_login.py            # 登录功能测试
│   ├── test_login_out.py        # 登出功能测试
│   ├── test_add_to_cart.py      # 添加购物车测试
│   ├── test_checkout.py         # 结账流程测试
│   └── __init__.py
├── test_data/
│   ├── login_data.yaml          # 登录测试数据
│   ├── test_add_to_cart.yaml    # 购物车测试数据
│   └── test_checkout.yaml       # 结账测试数据
└── hello_playwright.py          # 示例脚本

================================================================================

二、核心组件
--------------------------------------------------------------------------------
1. conftest.py - pytest 全局配置
   - pytest_configure(): 初始化测试环境，清空 allure-results 目录
   - page fixture: 启动浏览器并创建页面实例
   - logged_in_page fixture: 自动登录后的页面
   - pytest_runtest_makereport(): 测试失败时自动截图并附加到 Allure
   - pytest_sessionfinish(): 测试结束后自动生成 Allure 报告

2. config_reader.py - 配置管理（单例模式）
   - 支持多环境：test / staging / production
   - 通过环境变量 TEST_ENV 切换，默认 production
   - 读取 config.yaml 获取各环境配置

3. base_page.py - 页面对象基类
   - 封装 Playwright 公共操作：fill, click, goto, wait_visible 等
   - 统一选择器处理逻辑

4. LoginPage - 登录页面对象
   - 继承 BasePage
   - login(): 执行登录操作
   - logout(): 执行登出操作

================================================================================

三、配置管理
--------------------------------------------------------------------------------
config.yaml 支持的环境：
  - test:      测试环境（无头模式 false，浏览器 chromium）
  - staging:   预发布环境
  - production: 生产环境（无头模式 true）

环境变量：
  - TEST_ENV: 切换环境（默认 production）
  - TEST_USER: 覆盖用户名
  - TEST_PASSWORD: 覆盖密码

================================================================================

四、测试数据
--------------------------------------------------------------------------------
测试数据存储在 test_data/*.yaml 中
支持参数化测试：@pytest.mark.parametrize("case", data)

================================================================================

五、报告生成
--------------------------------------------------------------------------------
1. Allure 报告：
   - 测试结果保存至 allure-results/
   - 报告生成至 allure-report/
   - 查看报告命令：allure serve allure-results

2. 失败截图：
   - 截图保存至 screenshots/*.png
   - 自动附加到 Allure 报告中

3. 环境信息：
   - 自动生成 allure-results/environment.properties

================================================================================

六、运行测试
--------------------------------------------------------------------------------
# 运行所有测试
pytest

# 运行指定测试
pytest TestCase/test_login.py

# 生成 Allure 报告
allure generate allure-results -o allure-report --clean
allure serve allure-results

================================================================================

## CI/CD 学习记录

- 完成 GitHub Pull Request 流程学习。