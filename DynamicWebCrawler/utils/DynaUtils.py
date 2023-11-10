import os
import platform

from scrapy.utils.project import get_project_settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class Utils:

    @staticmethod
    def is_windows_os():
        if platform.system().lower() == 'windows':
            return True
        else:
            return False
    @staticmethod
    def close_chrome():
        if Utils.is_windows_os():
            os.system('chcp 65001 > nul')
            os.system('taskkill /f /t /im chromedriver.exe')
            # os.system('taskkill /f /t /im chrome.exe')
        else:
            os.system("pkill -9 chrome")
            os.system("pkill -9 chromedriver")

    @staticmethod
    def init_broswer_driver():
        settings = get_project_settings()
        # chrome_driver_path = settings.get('CHROME_DRIVER_PATH')
        options = webdriver.ChromeOptions()
        # options.add_argument('--start-maximized')  # 浏览器窗口最大化
        options.page_load_strategy = 'eager'
        options.add_experimental_option('detach', False)
        options.binary_location = r'chrome/chrome.exe'
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument('blink-settings=imagesEnabled=false')
        return webdriver.Chrome(service=Service('chromedriver.exe'), options=options)
