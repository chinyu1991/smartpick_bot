# run_flow.py
# 業務ロジック実装場所
from common.login_page import LoginPage

# 文件名 类名
from pages.doWith_page import DoWithPage


def run_main_flow(driver):

    login = LoginPage(driver)
    input = DoWithPage(driver)

    # 每次都自动输入账号密码并登录
    login.login_auto()
    print("✅ ログイン実施完了")
    input.atbbInput()
