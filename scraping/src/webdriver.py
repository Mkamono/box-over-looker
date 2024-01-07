import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.webelement import WebElement

Driver = webdriver.Remote
WebElement = WebElement


def make_driver() -> Driver:
    # ドライバの設定
    options = ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-automation")
    options.add_argument("--headless")  # モニタリングなし
    options.page_load_strategy = "eager"  #  読み込み省略(画像省略)
    driver = Driver(command_executor=os.environ["SELENIUM_URL"], options=options)
    return driver
