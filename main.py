import argparse
import logging
import copy

from concurrent.futures import ThreadPoolExecutor

from src.Login import DriverManager
from src.Trade import GoldParser
from src.Point import PointCollector
from src.Tools import ConfigManager, TaskScheduler
from src.Logging import ProjectLogging


# Instantiate Logger
ProjectLogging()

# CLI Args
cli_parser = argparse.ArgumentParser()
cli_parser.add_argument('--arg-config-path', default='arg-config.toml')
cli_parser.add_argument('--mode', default='Login', help='Login, GoldPrice, or CollectPoint')

arg_manager = ConfigManager(cli_parser)
args = arg_manager.args

if __name__ == '__main__':
    if args.mode == 'Login':
        account_names = args.account_names

        for account_name in account_names:
            args.account_name = account_name
            warmane_page = DriverManager(args)

    elif args.mode == 'GoldPrice':
        args.account_name = arg_manager.get_account_by_realm_and_character(args.realm, args.char)
        logging.info(f'Account-Realm-Character: {args.account_name}-{args.realm}-{args.char}')
        warmane_page = DriverManager(args)

        def run_gold_parsing_task():
            GoldParser(warmane_page.driver, args)

        scheduler = TaskScheduler(args, run_gold_parsing_task)
        scheduler.start_schedule()

    elif args.mode == 'CollectPoint':
        account_names = args.account_names

        def async_collect_points(_account_name, _args):
            per_args = copy.deepcopy(_args)
            per_args.account_name = _account_name
            per_warmane_page = DriverManager(per_args)
            pc = PointCollector(per_warmane_page.driver, per_args)
            pc.collect()
            per_warmane_page.driver.quit()

        try:
            with ThreadPoolExecutor() as executor:
                executor.map(lambda acc: async_collect_points(acc, args), account_names)
        except KeyboardInterrupt:
            logging.info("Execution interrupted by user.")
