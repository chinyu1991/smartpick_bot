# login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import ATBB_URL, LOGIN_ID, LOGIN_PASSWORD
import time


class LoginPage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(ATBB_URL)

    def login_auto(self):
        self.open()

        # 等待输入框出现
        user_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "loginFormText"))
        )
        pass_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "passFormText"))
        )

        # 不管有没有内容，全部清掉
        user_input.clear()
        pass_input.clear()

        # 重新输入账号密码
        user_input.send_keys(LOGIN_ID)
        pass_input.send_keys(LOGIN_PASSWORD)

        # 点击登录按钮
        login_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "loginSubmit"))
        )
        login_btn.click()
        time.sleep(4)
        print("➡️ 已自动输入账号密码并点击登录（不做成功判定）")
        
        

   


