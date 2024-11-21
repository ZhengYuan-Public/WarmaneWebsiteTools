import os
import time
import datetime
import logging

import pytz
import schedule
import toml

from selenium.webdriver.common.action_chains import ActionChains


class ConfigManager:

    CONFIG_CHANGE_EVENT = "config_change"

    def __init__(self, config_path, args):
        self.config_path = config_path
        self.config = self.load_toml_config()
        self.args = args

    def load_toml_config(self):
        if not os.path.exists(self.config_path):
            print("TOML config file not found.")
            return None
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return toml.load(f)

    def save_toml_config(self):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            toml.dump(self.config, f)

    def add_char(self, char_name, realm_name, account_name):
        """Adds a character to the specified account and realm."""
        if account_name not in self.config['accounts']:
            print(f"Account {account_name} not found in config.")
            return

        # Ensure the realm exists for the account
        if realm_name not in self.config['accounts'][account_name]:
            self.config['accounts'][account_name][realm_name] = {"chars": []}

        # Add the character if it doesn't already exist
        if char_name not in self.config['accounts'][account_name][realm_name]['chars']:
            self.config['accounts'][account_name][realm_name]['chars'].append(char_name)
            print(f"Character {char_name} added to realm {realm_name} under account {account_name}.")
            self.save_toml_config()
        else:
            print(f"Character {char_name} already exists in {realm_name}.")

    def del_char(self, char_name, realm_name, account_name):
        """Deletes a character from the specified account and realm."""
        if account_name not in self.config['accounts']:
            print(f"Account {account_name} not found in config.")
            return

        if realm_name not in self.config['accounts'][account_name]:
            print(f"Realm {realm_name} not found for account {account_name}.")
            return

        if char_name in self.config['accounts'][account_name][realm_name]['chars']:
            self.config['accounts'][account_name][realm_name]['chars'].remove(char_name)
            print(f"Character {char_name} removed from realm {realm_name} under account {account_name}.")
            self.save_toml_config()
        else:
            print(f"Character {char_name} not found in {realm_name}.")

    def rename_char(self, old_char_name, new_char_name, realm_name, account_name):
        """Renames a character under the specified account and realm."""
        if account_name not in self.config['accounts']:
            logging.error(f"Account {account_name} not found in config.")
            return

        if realm_name not in self.config['accounts'][account_name]:
            logging.error(f"Realm {realm_name} not found for account {account_name}.")
            return

        chars_list = self.config['accounts'][account_name][realm_name]['chars']

        if old_char_name in chars_list:
            if new_char_name in chars_list:
                logging.error(f"Character {new_char_name} already exists in realm {realm_name}.")
            else:
                # Rename the character
                chars_list[chars_list.index(old_char_name)] = new_char_name
                logging.info(f"Character {old_char_name} renamed to {new_char_name}.")
                self.save_toml_config()
        else:
            logging.error(f"Character {old_char_name} not found in realm {realm_name}.")

    def get_accounts_list(self):
        return list(self.config.get('accounts', {}).keys())

    def get_account_by_realm_and_character(self, realm_name, character_name):
        for account_name, account_data in self.config.get('accounts', {}).items():
            # Check if the realm exists in the account data
            if realm_name in account_data:
                # Check if the character exists in the realm's character list
                if character_name in account_data[realm_name]['chars']:
                    return account_name
        return None

    def update_value(self, **kwargs):
        account_name = kwargs.get('account_name')
        if account_name in self.config['accounts']:
            logging.info(f"Updating account: {account_name}")
            self.config['accounts'][account_name]['cookies_path'] = kwargs.get('cookies_path', '')
            self.config['accounts'][account_name]['last_updated_time'] = kwargs.get('last_updated_time', '')
        else:
            logging.error(f"Account {account_name} not found.")
            return False

        self.write_toml_config()
        logging.info("Config file updated.")
        return True

    def write_toml_config(self):
        """Writes the current config to the TOML file."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            toml.dump(self.config, f)


class TaskScheduler:
    def __init__(self, args, task_function):
        self.args = args
        self.task_function = task_function
        self.schedule = self.setup_schedule()  # Store the schedule instance

    def setup_schedule(self):
        hour_interval = getattr(self.args, 'hour', None)
        minute_interval = getattr(self.args, 'min', None)

        if hour_interval is not None:
            job = schedule.every(hour_interval).hours.do(self.task_function)
            logging.info(f'Scheduled task to run every {hour_interval} hour(s).')
            self.task_function()  # Run immediately for the first time
            return job
        elif minute_interval is not None:
            job = schedule.every(minute_interval).minutes.do(self.task_function)
            logging.info(f'Scheduled task to run every {minute_interval} minute(s).')
            self.task_function()  # Run immediately for the first time
            return job
        else:
            logging.info('No scheduling interval provided. Running the task once.')
            self.task_function()  # Run immediately
            return None

    @staticmethod
    def start_schedule():
        while True:
            schedule.run_pending()  # Runs any pending jobs
            time.sleep(1)


class MiscDriverTools:
    def __init__(self, driver, args):
        self.driver = driver
        self.args = args

    def reset_mouse_coord(self):
        ActionChains(self.driver).move_by_offset(5, 5).perform()


class MiscTools:
    def __init__(self):
        pass

    @staticmethod
    def get_localtime():
        current_time_utc = datetime.datetime.now(pytz.utc)
        china_timezone = pytz.timezone('Asia/Shanghai')
        current_time_local = current_time_utc.astimezone(china_timezone)
        formatted_time = current_time_local.strftime("%Y-%m-%d_%H-%M-%S")
        return formatted_time
