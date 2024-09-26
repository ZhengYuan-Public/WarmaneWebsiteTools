import argparse
from assets.login import *
from assets.trade import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--get-cookies',action='store_true', help='Launch in windows mode to save cookies')
    parser.add_argument('--realm', help='Realm name')
    parser.add_argument('--char', help='Character name')
    args = parser.parse_args()

    match args.get_cookies:
        case True:
            # Launch in windows mode to save cookies
            driver = create_driver(get_cookies=True)

            print('Please login manually within 2 minutes...')
            wait_for_manual_login(driver)
            if not wait_for_manual_login(driver):
                print('Manual login timed out.')
                driver.quit()
                exit(1)
            else:
                print('Manual login successful.')
                save_cookies(driver)

                ## Try to collect points
                get_points(driver)
                driver.quit()
                exit(1)
        case False:
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
                get_points(driver)
            else:
                print("Cookies login failed. Please launch in Windows mode to update your cookies.")

if __name__ == '__main__':
    main()
