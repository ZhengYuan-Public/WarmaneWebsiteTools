import time
import logging

import subprocess
import psutil
import pyautogui

from src.Login import TwoFactorAuthHandler


class WowLogin:
    def __init__(self, args):
        """
        :param args: Need a single args.account_name from main
        """
        self.args = args
        self.get_wow_config()
        self.wow_instance = self.start_wow()

    def get_wow_config(self):
        _lang = self.args.wow['lang']
        for _category, _img_dict in self.args.wow['img'].items():
            for _img_key, _img_val in _img_dict.items():
                self.args.wow['img'][_category][_img_key] = _img_val.replace('LANG', _lang)

    def get_login_info(self):
        _acc = self.args.account_name
        _pwd = self.args.accounts[_acc]['secret']
        return _acc, _pwd

    def get_2fa_totp(self):
        return TwoFactorAuthHandler(self.args).get_totp(self.args.account_name)

    def start_wow(self):
        process = subprocess.Popen(self.args.wow['exe'])
        while True:
            if process.pid is not None:
                logging.info(f"Wow.exe has started successfully. PID: {process.pid}")
                return process
            time.sleep(1)

    def quit_wow(self):
        psutil.Process(self.wow_instance.pid).terminate()

    def status_handler(self):
        login_images = self.args.wow['img']['login']
        totp_images = self.args.wow['img']['totp']

        chars_images = self.args.wow['img']['chars']

    @staticmethod
    def get_img_loc(img_path):
        return pyautogui.locateOnScreen(img_path)
