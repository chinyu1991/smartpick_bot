# main.py
from common import engine_driver
from run_flow import run_main_flow


def main(browser_engine):
    if browser_engine == "chrome":
        driver = engine_driver.create_driver_chrome(headless=False)
    if browser_engine == "edge":
        driver = engine_driver.create_driver(headless=False)
    else:
        print('没找到可执行的网页引擎')
    # run_main_flow(driver)

    try:
        run_main_flow(driver)
        # input("流程结束，按回车关闭浏览器...")
    finally:
        input("プロセス終了...")
        # driver.quit()

if __name__ == "__main__":
    browser_engine = 'chrome'
    # browser_engine = 'edge'
    main(browser_engine)
