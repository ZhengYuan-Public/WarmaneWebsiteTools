import argparse
import schedule
from assets.login import *
from assets.trade import *
import time


parser = argparse.ArgumentParser()
parser.add_argument('--get-cookies',action='store_true', help='Launch in windows mode to save cookies')
parser.add_argument('--realm', default='Icecrown', help='Realm name')
parser.add_argument('--char', help='Character name')
parser.add_argument('--hour', type=int, help='Run the script every <n> hour(s).')
parser.add_argument('--min', type=int, help='Run the script every <n> minute(s).')
args = parser.parse_args()


def collect_data():
    if args.get_cookies:
        # Launch in windows mode to save cookies
        driver = create_driver(get_cookies=True)

        print('Please login manually within 2 minutes...')
        wait_for_manual_login(driver)
        if not wait_for_manual_login(driver):
            print('Manual login timed out.')
            safe_exit(driver)
        else:
            print('Manual login successful.')
            save_cookies(driver)

            ## Try to collect points
            collect_daily_points(driver)
            safe_exit(driver)
    else:
        # Launch in headless mode to scrap data
        driver = create_driver()
        load_cookies(driver)
        driver.refresh()
        time.sleep(3)

        log_in_status = is_logged_in(driver)
        if log_in_status:
            print('Cookies login successful.')
            jump_to_trade(driver)
            sel_realm(driver, args.realm)
            sel_char(driver, args.char)
            sel_service(driver)
            sel_trade_option(driver)
            jump_to_gold(driver)

            # Save to csv
            df = get_gold_df(driver)
            # YYYY-MM-DD_HH-MM-SS.csv
            file_path = get_localtime().replace(':', '-').replace(' ', '_') + '.csv'
            df.to_csv(file_path, index=False)

            ## Try to collect points
            collect_daily_points(driver)
            safe_exit(driver)
        else:
            print("Cookies login failed. Please launch in Windows mode to update your cookies.")
            safe_exit(driver)


collect_data()

if args.hour is not None and args.hour > 0:
    run_interval = args.hour
    print(f'WarmaneGoldPriceScraper is scheduled to run every {run_interval} hour(s).')
    schedule.every(run_interval).hours.do(lambda: collect_data())
elif args.min is not None and args.min > 0:
    run_interval = args.min
    print(f'WarmaneGoldPriceScraper is scheduled to run every {run_interval} minute(s).')
    schedule.every(run_interval).minutes.do(lambda: collect_data())


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for a short time to prevent busy-waiting
