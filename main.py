import argparse
from src.Login import DriverManager
from src.Trade import GoldParser
from src.Point import PointCollector
from src.Tools import ConfigManager, TaskScheduler
from src.Logging import ProjectLogging


ProjectLogging()

parser = argparse.ArgumentParser()
parser.add_argument('--mode', help='<Gold> or <Points>.')
parser.add_argument('--arg-config', default='arg-config.toml', help='Argparse configuration file.')
temp_args = parser.parse_args()

arg_manager = ConfigManager(temp_args.arg_config, temp_args)
parser.set_defaults(**arg_manager.config)
args = parser.parse_args()

acc_manager = ConfigManager(args.acc_config, args)

if __name__ == '__main__':
    if args.mode == 'GoldPrice':
        args.account_name = acc_manager.get_account_by_realm_and_character(args.realm, args.char)
        print(f'Account-Realm-Character: {args.account_name}-{args.realm}-{args.char}')
        warmane_page = DriverManager(args)

        def run_gold_parsing_task():
            GoldParser(warmane_page.driver, args)

        scheduler = TaskScheduler(args, run_gold_parsing_task)
        scheduler.start_schedule()

    elif args.mode == 'CollectPoint':
        account_names = args.account_names
        for account_name in account_names:
            args.account_name = account_name
            warmane_page = DriverManager(args)
            pc = PointCollector(warmane_page.driver, args)
            pc.collect()
            warmane_page.driver.quit()
