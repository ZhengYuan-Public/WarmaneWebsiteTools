import os
import pickle
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from src.Tools import MiscTools


class DriverManager:
    """
    Needed args from argparse:
    - args.url: The URL to connect to (e.g., 'https://www.warmane.com').
    - args.account_name: The account name used for saving/loading cookies.
    """
    def __init__(self, args):
        self.args = args

        self.base_options, self.full_options = self.creat_options()

        # Connectivity test in headless mode
        self.driver = self.create_driver(self.full_options)

        # Cookies Login
        ## Try to load cookies to login
        AuthStatueHandler(self.driver, self.args).cookies_login()
        if not AuthStatueHandler(self.driver, self.args).is_logged_in():
            # Cookies not exist OR expire, then start in windows mode and update cookies
            self.driver.quit()
            self.driver = self.create_driver(self.base_options)
            AuthStatueHandler(self.driver, self.args).manual_login()
            CookiesManager(self.driver, args).update_cookies()

    def create_driver(self, options):
        _driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        _driver.get(self.args.url)
        if AuthStatueHandler(_driver, self.args).is_connected():
            return _driver

    @staticmethod
    def creat_options():
        base_options = Options()

        base_options.add_argument('--no-sandbox')
        base_options.add_argument('--disable-dev-shm-usage')
        base_options.add_argument('--disable-extensions')
        base_options.add_argument('--disable-gpu')
        base_options.add_argument('--log-level=3')  # Reduce log verbosity
        base_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )

        full_options = Options()
        full_options.arguments.extend(base_options.arguments)
        full_options.add_argument('--headless')

        return base_options, full_options


class AuthStatueHandler:
    def __init__(self, _driver, args):
        self.driver = _driver
        self.args = args

    def is_connected(self):
        try:
            self.driver.find_element("xpath", "//a[@title='Login']")
            print(f"Connected to {self.driver.current_url}, proceeding to login.")
            return True
        except NoSuchElementException:
            print(f"Failed to connect to {self.driver.current_url}, exiting...")
            self.driver.quit()

    def is_logged_in(self):
        try:
            self.driver.find_element(By.XPATH, '//a[@href="/account/logout" and @title="Logout"]')
            try:
                self.driver.find_element(By.XPATH,
                                         '//a[@href="/account/authentication" and contains(@class, "active")]')
                print(f'Two factor authentication detected, waiting for authentication...')
                return False
            except NoSuchElementException:
                return True
        except NoSuchElementException:
            return False

    def cookies_login(self):
        CookiesManager(self.driver, self.args).load_cookies()
        if self.is_logged_in():
            print('Cookies login successfully.')
            return True
        else:
            print('Cookies has expired. Starting in windows mode to update cookies...')
            return False

    def manual_login(self):

        def wait_for_manual_login(timeout=600):
            start_time = time.time()
            print('Please manually login within 5 minutes.')
            while time.time() - start_time < timeout:
                if self.is_logged_in():
                    print('Waiting for manual login...')
                    return True
                # Check every 5 seconds
                time.sleep(5)
            return False

        if not wait_for_manual_login():
            print('Manual login timed out.')
            self.driver.quit()
        else:
            return True


class CookiesManager:
    def __init__(self, _driver, args):
        """
        Cookie for one account.
        """
        self.driver = _driver
        self.args = args
        self.account_name = args.account_name
        self.cookies_path = os.path.join(self.args.cookies_dir, self.account_name, 'cookies.pkl')

    def load_cookies(self):
        if not os.path.exists(self.cookies_path):
            print(f'Cookies for {self.account_name} not found. Starting in windows mode to get cookies...')
            return False
        try:
            with open(self.cookies_path, 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            self.driver.refresh()
            time.sleep(3)
            return True
        except Exception as e:
            print(f"Failed to load cookies: {e}")
            return False

    def update_cookies(self):
        try:
            cookies = self.driver.get_cookies()
            os.makedirs(os.path.dirname(self.cookies_path), exist_ok=True)

            with open(self.cookies_path, 'wb') as file:
                pickle.dump(cookies, file)
            self.args.update_time = MiscTools.get_localtime()
            print(f'Cookies for {self.account_name} updated @{self.args.update_time}.')
        except Exception as e:
            print(f"Failed to update cookies for {self.account_name}: {e}")
