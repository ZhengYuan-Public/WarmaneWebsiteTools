# WarmaneWebsiteTools

## Example arg-config.toml

```toml
# Mandatory Arguments
debug = true

csv_dir = './csv'
cookies_dir = './cookies'
acc_config = 'acc-config.toml'
url = 'https://www.warmane.com/account'
trade_url = 'https://www.warmane.com/account/trade'

# 1. Arguments for mode ==> 'GoldPrice'
# args.realm: {'Onyxia', 'Lordaeron', 'Icecrown', 'Blackrock', 'Frostwolf'}
# args.char: The character name.
# args.trade_type: {'Item Trade', 'Character Trade'}
# args.trade_action: {'Buy', 'Sell'}

mode = 'GoldPrice'
realm = 'Icecrown'
char = 'char_name'
trade_type = 'Item Trade'
trade_action = 'Buy'

hour = 1
min = 15

# 2. Arguments for mode ==> 'CollectPoint'
mode = 'CollectPoint'
account_names = ['char_name_1', 'char_name_2', 'char_name_3']
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