# WarmaneGoldPriceScraper

## Get your cookies for headless mode login
```terminal
python main.py --get-cookies
```

## Scrap gold price data
```terminal
$ python .\main.py -help
usage: main.py [-h] [--get-cookies] [--realm REALM] [--char CHAR]

options:
  -h, --help     show this help message and exit
  --get-cookies  Launch in window mode to save cookies.
  --realm REALM  Realm name.
  --char CHAR    Specify character name for trade.
```

Example
```terminal
$ python main.py --realm Icecrown --char Metashadow
```
