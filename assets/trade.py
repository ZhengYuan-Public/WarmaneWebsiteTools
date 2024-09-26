from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
from assets.tools import *


def jump_to_trade(driver):
    driver.get('https://www.warmane.com/account/trade')
    time.sleep(5)

def sel_realm(driver, realm_name):
    wait = WebDriverWait(driver, 10)
    drop_down = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="realmselector_msdd"]')))
    drop_down.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="realmselector_child"]')))
    realm_name_option = wait.until(EC.element_to_be_clickable((By.XPATH, f'//li[.//span[text()="{realm_name}"]]')))
    realm_name_option.click()
    print(f"{realm_name} realm selected.")
    reset_mouse_coord(driver)
    time.sleep(3)

def sel_char(driver, char_name):
    wait = WebDriverWait(driver, 10)
    char_drop_down = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="characterselector_msdd"]')))
    char_drop_down.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="characterselector_child"]')))
    char_name_option = wait.until(EC.element_to_be_clickable((By.XPATH, f'//li[.//span[text()="{char_name}"]]')))
    char_name_option.click()
    print(f"Character '{char_name}' selected.")
    reset_mouse_coord(driver)
    time.sleep(3)

def sel_service(driver, service_name='Item Trade'):
    wait = WebDriverWait(driver, 10)
    service_drop_down = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="serviceselector_msdd"]')))
    service_drop_down.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="serviceselector_child"]')))
    service_name_option = wait.until(EC.element_to_be_clickable((By.XPATH, f'//li[.//span[text()="{service_name}"]]')))
    service_name_option.click()
    print(f"Service '{service_name}' selected.")
    reset_mouse_coord(driver)
    time.sleep(3)

def sel_trade_option(driver, trade_option='Buy'):
    wait = WebDriverWait(driver, 10)
    trade_option_drop_down = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="trade-option_msdd"]')))
    trade_option_drop_down.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="trade-option_child"]')))
    trade_option_option = wait.until(EC.element_to_be_clickable((By.XPATH, f'//li[.//span[text()="{trade_option}"]]')))
    trade_option_option.click()
    print(f"Trade option '{trade_option}' selected.")
    reset_mouse_coord(driver)
    time.sleep(3)

def jump_to_gold(driver):
    # Wait for items to load
    time.sleep(5)
    wait = WebDriverWait(driver, 10)
    gold_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="sideBtn" and .//p[text()="Gold"]]')))
    gold_option.click()
    print("Jumped to gold sell page.")
    reset_mouse_coord(driver)
    time.sleep(3)

def get_gold_df(driver):
    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.ID, "data-table")))
    table_html = table.get_attribute('outerHTML')

    soup = BeautifulSoup(table_html, 'html.parser')
    rows = soup.select('tbody > tr[role="row"].odd, tbody > tr[role="row"].even')

    df = pd.DataFrame(columns=['Time', 'Gold Value', 'Coin Value', 'Duration', 'Seller'])
    for row in rows:
        row_tds = row.find_all('td')
        # gold_value = row.find('td', class_='name').find('span', class_='numeric').text
        # coin_value = row.find('td', class_='costValues').find('span', class_='numeric').text
        gold_value = row_tds[1].find('span', class_='numeric').text
        coin_value = row_tds[6].find('span', class_='numeric').text
        duration = row_tds[3].text
        seller = row_tds[4].text
        data = pd.DataFrame([get_localtime(), gold_value, coin_value, duration, seller], index=df.columns)
        df = pd.concat([df, data.T], ignore_index=True)
    return df

# --------------------------------------------------------------------------------------------------------------- #

def get_points(driver):
    wait = WebDriverWait(driver, 10)
    driver.get('https://www.warmane.com/account')
    print("Trying to collect points...")
    try:
        collect_points_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Collect points")))
        collect_points_button.click()
        print("Points collected successfully!")
    except:
        print("No points to collect.")
