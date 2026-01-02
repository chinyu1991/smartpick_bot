# login_page.py
from selenium.webdriver.common.by import By

from config.config import ATBB_URL, LOGIN_ID, LOGIN_PASSWORD
from common.selenium_utils import SeleniumHelper


# @dataclass
class LoginLocators:
    user_input: tuple = (By.ID, "loginFormText")
    pass_input: tuple = (By.ID, "passFormText")
    login_btn: tuple = (By.ID, "loginSubmit")

    # 下面两个你可以按实际页面改：
    # 登录后才会出现的元素（用来判断已登录）
    logged_in_marker: tuple = (By.CSS_SELECTOR, "body")  # TODO: 改成登录后独有元素更稳
    # 登录中/加载遮罩（如果页面有的话）
    loading: tuple = (By.CSS_SELECTOR, ".loading")

class LoginPage:
    def __init__(self, driver):
        print('LoginPage')
        self.driver = driver
        self.seleniumUtil = SeleniumHelper(driver)
        self.loc = LoginLocators()

        # self.wait = WebDriverWait(driver, timeout)

    def open(self):

        self.driver.get(ATBB_URL)

    def login_auto(self):
        self.open()
        # 输入账户
        self.seleniumUtil.input_text((self.loc.user_input), LOGIN_ID, clear=True)
        # 输入密码
        self.seleniumUtil.input_text((self.loc.pass_input), LOGIN_PASSWORD, clear=True)
        # 点击登录
        self.seleniumUtil.click(self.loc.login_btn)

        print("➡️ 已自动输入账号密码并点击登录（不做成功判定）")
        
        

   


