import time
import logging

from bs4 import BeautifulSoup
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class PointCollector:
    def __init__(self, _driver, args):
        self.driver = _driver
        self.args = args

    def collect(self):
        wait = WebDriverWait(self.driver, 10)
        self.driver.get(self.args.url)
        time.sleep(2)
        acc_name, acc_coin, acc_points = self.get_acc_info()

        logging.info(f'====== Trying to collect point for {acc_name} ======')
        try:
            collect_points_button = wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Collect points")))
            logging.info(f"Points haven't been collected yet. Points: {acc_points}")
        except TimeoutException:
            collect_points_button = None
            logging.info("Points already collected.")

        if collect_points_button:
            collect_points_button.click()
            time.sleep(2)
            _, _, new_acc_points = self.get_acc_info()
            if new_acc_points > acc_points:
                logging.info(f"Collected {new_acc_points - acc_points} points")
            else:
                logging.info(f"Not eligible to collect points.")

    def get_acc_info(self):
        acc_element = self.driver.find_element(By.XPATH, "(//div[contains(@class, 'content-inner')])[1]")
        acc_element_html = acc_element.get_attribute("outerHTML")

        soup = BeautifulSoup(acc_element_html, "html.parser")
        _tds = soup.find_all('td')
        acc_name = _tds[1].text.split(' ')[-1]
        acc_coin = float(_tds[2].text.split(":")[-1].strip())
        acc_point = float(_tds[3].text.split(":")[-1].strip())

        return acc_name, acc_coin, acc_point
