# doWith_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import os
import re
from common.selenium_utils import SeleniumHelper
from config.config import READ_FILE
from common.common import get_project_root

class DoWithPage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.seleniumUtil = SeleniumHelper(driver)

    def atbbInput(self):
        # 记住当前 tab
        current = self.driver.current_window_handle
        print('当前的tab1 = '+current)

        # 点击：物件・会社検索
        self.seleniumUtil.click((By.XPATH, "//a[contains(.,'物件・会社検索')]"))
        print('物件・会社検索')

        # 点击：流通物件検索
        self.seleniumUtil.click((By.XPATH, "//div[@data-action='/atbb/nyushuSearch?from=global_menu_bukkenKensaku']"), timeout = 3)
        print("已点击：流通物件検索")

        # 入口画面ログアウト
        self.seleniumUtil.click((By.XPATH, "//button[contains(text(),'ログアウト')]"))
        print("ログアウト")

        # # 获取当前所有tab
        handles = self.driver.window_handles
        # 切到最后一个（新 tab）
        self.driver.switch_to.window(handles[-1])
        current = self.driver.current_window_handle
        print('当前的tab2 = ' + current)

        # 点击：「賃貸居住用」radioボタン
        self.seleniumUtil.click((By.XPATH, "//table//label[contains(string(), '賃貸居住用')]"), timeout=3)
        print("ログアウト")

        # 读取input文件的内容
        out_text = None
        with open(get_project_root() / "config/" / READ_FILE, "r", encoding="utf-8") as f:
            for line in f:
                out_text = line.strip()  # 去掉换行符
            print('物件关键字 = ' + out_text)

        # 入力：フリーワード検索
        self.seleniumUtil.input_text((By.XPATH, "//input[@id='freeWordSearchSubject']"), out_text, clear=True)
        # 点击：检索
        self.seleniumUtil.click((By.XPATH, '//input[@value="検索"]'))
        # 点击：详细
        self.seleniumUtil.click((By.XPATH, "//button[@id='shosai_0']"))

        # 保存图片
        images = self.seleniumUtil.get_text((By.XPATH, "//p[@class='box_title']//span"))
        count = int(re.search(r"\d+", images).group())
        print("画面点数 = " + str(count))
        # 点击：すべての画像を表示する
        self.seleniumUtil.click((By.XPATH, "//a[@class='allphoto']"))

        # 先切 iframe，用来点缩略图
        self.seleniumUtil.switch_to_frame((By.CSS_SELECTOR, "iframe.designCboxIframe"), timeout=10)

        for i in range(count):
            imageElementCnt = "//div[@class='image-list']//ul//li[" + str(i+1) + "]"
            self.seleniumUtil.click((By.XPATH, imageElementCnt))
            # print(imageElementCnt, i)
            self.seleniumUtil.screenshot(get_project_root() / "output" / "image" / f"{i}.png")

        # time.sleep(100)


