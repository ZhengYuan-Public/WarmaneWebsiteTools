import argparse
from assets.Login import DriverManager
from assets.Trade import GoldParser
from assets.Tools import ConfigManager, TaskScheduler


parser = argparse.ArgumentParser()
parser.add_argument('--mode', help='<Gold Price> or <Points>.')
parser.add_argument('--arg-config', default='arg-config.toml', help='Argparse configuration file.')
temp_args = parser.parse_args()

arg_manager = ConfigManager(temp_args.arg_config, temp_args)
parser.set_defaults(**arg_manager.config)
args = parser.parse_args()

acc_manager = ConfigManager(args.acc_config, args)

if __name__ == '__main__':
    if args.mode == 'Gold':
        args.account_name = acc_manager.get_account_by_realm_and_character(args.realm, args.char)
        print(f'Account-Realm-Character: {args.account_name}-{args.realm}-{args.char}')
        warmane_page = DriverManager(args)

        def run_gold_parsing_task():
            GoldParser(warmane_page.driver, args)

        schedular = TaskScheduler(args, run_gold_parsing_task)
        schedular.start_schedule()

    elif args.mode == 'Points':
        args.account_names = acc_manager.get_accounts_list()
        # TODO