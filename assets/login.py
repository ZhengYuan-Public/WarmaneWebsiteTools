from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle
import time
from assets.tools import safe_exit


def create_driver(get_cookies=False, url='https://www.warmane.com'):
    options = Options()

    if not get_cookies:
        options.add_argument('--headless=new')

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)
    try:
        driver.find_element("xpath", "//a[@title='Login']")
        print(f"Connected to {url}, proceeding to login.")
        return driver
    except Exception:
        print(f"Failed to connect to {url}, exiting...")
        safe_exit(driver)

def is_logged_in(driver):
    try:
        driver.find_element(By.XPATH, '//a[@href="/account/logout" and @title="Logout"]')
        return True
    except Exception:
        return False

def wait_for_manual_login(driver, timeout=120):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_logged_in(driver):
            print('Manual login detected. Cookies will be updated.')
            return True
        # Check every 5 seconds
        time.sleep(5)
    return False

def save_cookies(driver):
    with open('./cookies.pkl', 'wb') as file:
        pickle.dump(driver.get_cookies(), file)
    print('Manual login successful. Cookies saved.')

def load_cookies(driver):
    print('Attempting to login using cookies...')
    try:
        with open('./cookies.pkl', 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(3)
        return True
    except FileNotFoundError:
        return False
