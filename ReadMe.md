# WarmaneWebsiteTools

## Example arg-config.toml

```toml
# Arguments Required
# ------------------------------------------------------------------------------------- #
# args.realm: {'Onyxia', 'Lordaeron', 'Icecrown', 'Blackrock', 'Frostwolf'}
# args.char: The character name.
# args.trade_type: {'Item Trade', 'Character Trade'}
# args.trade_action: {'Buy', 'Sell'}
# ------------------------------------------------------------------------------------- #
# 1. Mandatory arguments for > mode = 'Gold Price'
mode = 'Gold'
realm = 'Icecrown'
char = 'MyCharacterName'
trade_type = 'Item Trade'
trade_action = 'Buy'

# 2. Mantadory arguments for > mode = 'Points'
# mode = 'Points'

# ------------------------------------------------------------------------------------- #
acc_config = 'acc-config.toml'
url = 'https://www.warmane.com/account'
trade_url = 'https://www.warmane.com/account/trade'
# ------------------------------------------------------------------------------------- #
# Directory where CSV files should be saved
csv_dir = './csv'
cookies_dir = './cookies'

# ------------------------------------------------------------------------------------- #
# Frequency to run the script
# hour = 1
min = 15

```

## Example acc-config.toml

```toml
[accounts]

[accounts.MyAccountName]
cookies_path = ''
last_updated_time = ''
passwd = ''
[accounts.MyAccountName.MyRealm]
chars = ["MyCharacterName1", "MyCharacterName2", "MyCharacterName3"]
```