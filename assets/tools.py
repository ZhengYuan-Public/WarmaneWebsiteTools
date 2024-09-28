import os
from typing import List
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import pytz


def print_html(contents: List[WebElement], dump=False):
    for index, content in enumerate(contents):
        content_html = content.get_attribute('outerHTML')
        print(content_html)
        print('-' * 10)
        if dump:
            os.makedirs('html', exist_ok=True)
            # Use a valid file name
            file_name = f'html/content_{index}.html'
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(content_html)

def get_localtime():
    current_time_utc = datetime.datetime.now(pytz.utc)
    china_timezone = pytz.timezone('Asia/Shanghai')
    current_time_local = current_time_utc.astimezone(china_timezone)
    formatted_time = current_time_local.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def reset_mouse_coord(driver):
    ActionChains(driver).move_by_offset(5, 5).perform()

def safe_exit(driver):
    driver.quit()
    exit(1)
