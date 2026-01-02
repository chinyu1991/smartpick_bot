# main.py
from common import edge_driver
from run_flow import run_main_flow


def main():
    # driver = edge_driver.create_driver(headless=False)
    driver = edge_driver.create_driver_chrome(headless=False)
    # run_main_flow(driver)

    try:
        run_main_flow(driver)
        # input("流程结束，按回车关闭浏览器...")
    finally:
        input("プロセス終了...")
        # driver.quit()

if __name__ == "__main__":
    main()
