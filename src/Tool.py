import os
import re
import time
import datetime
import logging

import pytz
import schedule
import toml

from selenium.webdriver.common.action_chains import ActionChains


class ConfigManager:
    def __init__(self, cli_parser):
        """
        :param cli_parser: contains cli args <mode> and <arg_config_path>
        """
        self.parser = cli_parser
        self.args = self.parser.parse_args()

        # 1. Update self.parser
        # Get project args from file, then extract args for a particular mode
        self.arg_config_dict = self.load_toml_config(self.args.arg_config_path)
        self.acc_config_dict = self.load_toml_config(self.arg_config_dict['acc_config'])

        self.parser.set_defaults(**{**self.arg_config_dict, **self.acc_config_dict})

        # 2. Update self.args
        self.args = self.parser.parse_args()


    @staticmethod
    def load_toml_config(toml_config_path):
        if not os.path.exists(toml_config_path):
            logging.info("TOML config file not found.")
            return None
        with open(toml_config_path, 'r', encoding='utf-8') as f:
            return toml.load(f)

    # @staticmethod
    # def extract_mode_args(_arg_config_dict, _mode):
    #     _modes = _arg_config_dict.pop('modes')
    #     _mode_dict = _modes[_mode]
    #     return {**_mode_dict, **_arg_config_dict}

    # def get_accounts_list(self):
    #     return list(self.arg_config_all.get('accounts', {}).keys())

    # def get_account_by_realm_and_character(self, realm_name, character_name):
    #     for account_name, account_data in self.arg_config_all.get('accounts', {}).items():
    #         # Check if the realm exists in the account data
    #         if realm_name in account_data:
    #             # Check if the character exists in the realm's character list
    #             if character_name in account_data[realm_name]['chars']:
    #                 return account_name
    #     return None

    # def add_char(self, char_name, realm_name, account_name):
    #     """Adds a character to the specified account and realm."""
    #     if account_name not in self.arg_config_all['accounts']:
    #         logging.error(f"Account {account_name} not found in config.")
    #         return
    #
    #     # Ensure the realm exists for the account
    #     if realm_name not in self.arg_config_all['accounts'][account_name]:
    #         self.arg_config_all['accounts'][account_name][realm_name] = {"chars": []}
    #
    #     # Add the character if it doesn't already exist
    #     if char_name not in self.arg_config_all['accounts'][account_name][realm_name]['chars']:
    #         self.arg_config_all['accounts'][account_name][realm_name]['chars'].append(char_name)
    #         logging.info(f"Character {char_name} added to realm {realm_name} under account {account_name}.")
    #         self.write_toml_config()
    #     else:
    #         logging.info(f"Character {char_name} already exists in {realm_name}.")
    #
    # def del_char(self, char_name, realm_name, account_name):
    #     """Deletes a character from the specified account and realm."""
    #     if account_name not in self.arg_config_all['accounts']:
    #         logging.error(f"Account {account_name} not found in config.")
    #         return
    #
    #     if realm_name not in self.arg_config_all['accounts'][account_name]:
    #         logging.error(f"Realm {realm_name} not found for account {account_name}.")
    #         return
    #
    #     if char_name in self.arg_config_all['accounts'][account_name][realm_name]['chars']:
    #         self.arg_config_all['accounts'][account_name][realm_name]['chars'].remove(char_name)
    #         logging.info(f"Character {char_name} removed from realm {realm_name} under account {account_name}.")
    #         self.write_toml_config()
    #     else:
    #         logging.error(f"Character {char_name} not found in {realm_name}.")
    #
    # def rename_char(self, old_char_name, new_char_name, realm_name, account_name):
    #     """Renames a character under the specified account and realm."""
    #     if account_name not in self.arg_config_all['accounts']:
    #         logging.error(f"Account {account_name} not found in config.")
    #         return
    #
    #     if realm_name not in self.arg_config_all['accounts'][account_name]:
    #         logging.error(f"Realm {realm_name} not found for account {account_name}.")
    #         return
    #
    #     chars_list = self.arg_config_all['accounts'][account_name][realm_name]['chars']
    #
    #     if old_char_name in chars_list:
    #         if new_char_name in chars_list:
    #             logging.error(f"Character {new_char_name} already exists in realm {realm_name}.")
    #         else:
    #             # Rename the character
    #             chars_list[chars_list.index(old_char_name)] = new_char_name
    #             logging.info(f"Character {old_char_name} renamed to {new_char_name}.")
    #             self.write_toml_config()
    #     else:
    #         logging.error(f"Character {old_char_name} not found in realm {realm_name}.")
    #
    # def update_value(self, **kwargs):
    #     account_name = kwargs.get('account_name')
    #     if account_name in self.arg_config_all['accounts']:
    #         logging.info(f"Updating account: {account_name}")
    #         self.arg_config_all['accounts'][account_name]['cookies_path'] = kwargs.get('cookies_path', '')
    #         self.arg_config_all['accounts'][account_name]['last_updated_time'] = kwargs.get('last_updated_time', '')
    #     else:
    #         logging.error(f"Account {account_name} not found.")
    #         return False
    #
    #     self.write_toml_config()
    #     logging.info("Config file updated.")
    #     return True
    #
    # def write_toml_config(self):
    #     with open(self.args.arg_config_path, 'w', encoding='utf-8') as f:
    #         toml.dump(self.arg_config_all, f)


class TaskScheduler:
    def __init__(self, args, task_function):
        self.args = args
        self.task_function = task_function
        self.schedule = self.setup_schedule()  # Store the schedule instance

    def setup_schedule(self):
        schedule_interval = self.args.schedule_interval
        if schedule_interval:
            job = schedule.every(schedule_interval).minutes.do(self.task_function)
            logging.info(f'Scheduled task to run every {schedule_interval} minutes.')
            # Run immediately for current time
            self.task_function()
            return job
        else:
            logging.info('No scheduling interval provided. Running the task once.')
            # Run immediately for current time
            self.task_function()
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
    @staticmethod
    def get_localtime():
        current_time_utc = datetime.datetime.now(pytz.utc)
        china_timezone = pytz.timezone('Asia/Shanghai')
        current_time_local = current_time_utc.astimezone(china_timezone)
        formatted_time = current_time_local.strftime("%Y-%m-%d_%H-%M-%S")
        return formatted_time

    @staticmethod
    def regex_match_float(_text: str):
        match = re.search(r"Points:\s*([\d.]+)", _text)
        if match:
            return float(match.group(1))
        return None
