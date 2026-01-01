# login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

class DoWithPage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
    
    def atbbInput(self):
        # 点击：物件登録・公開
        btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'物件登録・公開')]"))
        )
        btn.click()
        time.sleep(2)
        # 点击：物件・会社検索
        btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'物件・会社検索')]"))
        )
        btn.click()
        time.sleep(3)
        div_btn = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@data-action='/atbb/nyushuSearch?from=global_menu_bukkenKensaku']")
            )
        )
        self.driver.execute_script("arguments[0].click();", div_btn)
        print("已点击：流通物件検索")

        # 入口画面ログアウト、閉じる
        logout_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit' and normalize-space()='ログアウト']")
            )    
        )
        self.driver.execute_script("arguments[0].click();", logout_btn)
        time.sleep(1)
        # Tab閉じる
        target_title = "加盟店専用サイト"
        current = self.driver.current_window_handle
        handles = self.driver.window_handles
        for h in handles:
            self.driver.switch_to.window(h)
            if target_title in self.driver.title:
                self.driver.close()
                break
        # self.driver.switch_to.window(current)
        print("閉じました。。。。。")

        # 关键：切回一个存在的窗口
        remaining = self.driver.window_handles
        if current in remaining:
            self.driver.switch_to.window(current)
        else:
            self.driver.switch_to.window(remaining[0])
    
        # 「賃貸居住用」radioボタン
        # 1) 找到所有 radio 点击value等于6的
        radios = self.driver.find_elements(
            By.CSS_SELECTOR,
            "input[type='radio'][name='atbbShumokuDaibunrui']"
        )
        print("radio count =", len(radios))
        for i, r in enumerate(radios, start=1):
            value = r.get_attribute("value")
            print(i, value)
        r6 = self.driver.find_element(By.CSS_SELECTOR, "input[name='atbbShumokuDaibunrui'][value='06']")
        self.driver.execute_script("arguments[0].click();", r6)

        # 读取input文件的内容

        #







    

    
