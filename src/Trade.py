import os
import time
import logging
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from src.Tool import MiscDriverTools, MiscTools


class ItemSelector:
    def __init__(self, _driver, args):
        self.driver = _driver
        self.args = args

        # Unpack args
        self.trade_url = self.args.warmane['trade_url']

        self.account_name = self.args.account_name
        self.realm = self.args.modes['GoldPrice']['realm']
        self.char = self.args.modes['GoldPrice']['char']
        self.trade_type = self.args.modes['GoldPrice']['trade_type']
        self.trade_action = self.args.modes['GoldPrice']['trade_action']
        self.sidebar_item = self.args.sidebar_item

        self.jump_to_trade()
        self.realm_selector()
        self.char_selector()
        self.trade_type_selector()
        self.trade_action_selector()
        self.sidebar_gold_selector()

    def jump_to_trade(self):
        self.driver.get(self.trade_url)
        logging.info(f'Jumping to trade page {self.trade_url}...')
        time.sleep(3)

    def realm_selector(self):
        self._select_dropdown_option(
            dropdown_cat="Realm",
            dropdown_text=self.realm,
            dropdown_cat_xpath='//div[@id="realmselector_msdd"]',
            dropdown_text_xpath='//div[@id="realmselector_child"]'
        )

    def char_selector(self):
        self._select_dropdown_option(
            dropdown_cat="Character",
            dropdown_text=self.char,
            dropdown_cat_xpath='//div[@id="characterselector_msdd"]',
            dropdown_text_xpath='//div[@id="characterselector_child"]'
        )

    def trade_type_selector(self,):
        self._select_dropdown_option(
            dropdown_cat="Trade type",
            dropdown_text=self.trade_type,
            dropdown_cat_xpath='//div[@id="serviceselector_msdd"]',
            dropdown_text_xpath='//div[@id="serviceselector_child"]',
        )

    def trade_action_selector(self):
        self._select_dropdown_option(
            dropdown_cat="Trade option",
            dropdown_text=self.trade_action,
            dropdown_cat_xpath='//div[@id="trade-option_msdd"]',
            dropdown_text_xpath='//div[@id="trade-option_child"]',
        )

    def sidebar_gold_selector(self):
        self._sidebar_item_selector(self.sidebar_item)

    def _select_dropdown_option(self, dropdown_cat, dropdown_text, dropdown_cat_xpath, dropdown_text_xpath):
        wait = WebDriverWait(self.driver, 10)
        drop_down = wait.until(ec.element_to_be_clickable((By.XPATH, dropdown_cat_xpath)))
        drop_down.click()
        wait.until(ec.visibility_of_element_located((By.XPATH, dropdown_text_xpath)))
        option = wait.until(ec.element_to_be_clickable((By.XPATH, f'//li[.//span[text()="{dropdown_text}"]]')))
        option.click()
        logging.info(f"{dropdown_cat} '{dropdown_text}' selected.")
        MiscDriverTools(self.driver, self.args).reset_mouse_coord()
        time.sleep(3)

    def _sidebar_item_selector(self, menu_name):
        wait = WebDriverWait(self.driver, 10)
        item_btn = wait.until(ec.element_to_be_clickable(
            (By.XPATH, f'//div[@class="sideBtn"]//p[text()="{menu_name}"]')
        ))
        item_btn.click()
        logging.info(f"Sidebar item '{menu_name}' selected.")
        MiscDriverTools(self.driver, self.args).reset_mouse_coord()
        time.sleep(3)


class GoldParser:
    def __init__(self, _driver, args):
        self.driver = _driver
        self.args = args

        self.parse_time = MiscTools.get_localtime()

        # Unpack some args
        self.csv_dir_path = self.args.warmane['csv_dir']
        self.csv_path = os.path.join(self.csv_dir_path, f'{self.parse_time}.csv')

        self.data = self.parse_table()
        self.save_to_csv()

    def parse_table(self):
        ItemSelector(self.driver, self.args)
        # Check if csv_dir is valid before proceeding
        if not self.args.warmane['csv_dir']:
            raise ValueError("csv_dir is not set or is None")

        wait = WebDriverWait(self.driver, 10)
        table = wait.until(ec.presence_of_element_located((By.ID, "data-table")))
        table_html = table.get_attribute('outerHTML')

        soup = BeautifulSoup(table_html, 'html.parser')
        rows = soup.select('tbody > tr[role="row"].odd, tbody > tr[role="row"].even')

        logging.info(f'Acquiring gold price @{self.parse_time}')
        logging.info(f'Processing {len(rows)} entries...')

        df = pd.DataFrame(columns=['Time', 'Gold Value', 'Coin Value', 'Duration', 'Seller'])
        for row in tqdm(rows):
            row_tds = row.find_all('td')
            # Extract necessary values with proper checks
            gold_value = row_tds[1].find('span', class_='numeric').text \
                if row_tds[1].find('span', class_='numeric') else ''
            coin_value = row_tds[6].find('span', class_='numeric').text \
                if row_tds[6].find('span', class_='numeric') else ''
            duration = row_tds[3].text if row_tds[3] else ''
            seller = row_tds[4].text if row_tds[4] else ''

            # Prepare data in a DataFrame
            data = pd.DataFrame([[self.parse_time, gold_value, coin_value, duration, seller]], columns=df.columns)
            df = pd.concat([df, data], ignore_index=True)
        return df

    def save_to_csv(self):
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        self.data.to_csv(self.csv_path, index=False)
        logging.info(f'Gold price saved to {self.csv_path}.')
