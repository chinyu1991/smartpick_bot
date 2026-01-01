# driver/edge_driver.py
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.chrome.options import Options

def create_driver(headless: bool = False) -> webdriver.Edge:
    opt = Options()
    opt.add_argument("--window-size=1280,900")
    opt.add_argument("--disable-notifications")
    # 企业系统建议先不用无头，方便你手动登录/过验证码
    if headless:
        opt.add_argument("--headless=new")

    driver = webdriver.Edge(options=opt)
    driver.implicitly_wait(0)  # 强烈建议不用隐式等待，全部用显式等待
    return driver

def create_driver_chrome(headless: bool = False) -> webdriver.Chrome:
    opt = Options()
    opt.add_argument("--window-size=1280,900")
    opt.add_argument("--disable-notifications")

    # 企业系统 / 登录页，建议先不用 headless
    if headless:
        opt.add_argument("--headless=new")

    driver = webdriver.Chrome(options=opt)
    driver.implicitly_wait(0)  # 强烈建议不用隐式等待
    return driver