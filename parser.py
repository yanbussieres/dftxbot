s = """
@everyone RSRUSDT - SHORT

Entry: 0.9110-0.945
Stop Loss: H1 close above 0.96 or 0.99 on a wick
Risk: 1-2.5% [keep your risk low - this COULD get volatile leading into Mainnet hype (lol)]

Target 1: 0.80-0.815
Target 2: TBD [possibly like 0.71 but we'll see as prices develop]

"""


"""
   frostybot trade:mystub:short symbol=BTC/USD size=2000 price=7600  ($2000 limit sell at $7600 on FTX BTC/USD)

"""

"""
Trade 23: LUNCBUSD - LONG

Entry: 0.3035
Size: $250K
Stop Loss: H1 close below 0.30 or wick below 0.29

Target:  0.328-0.335

Chart: https://www.tradingview.com/x/e4O036S7/

Starting Balance: $1,554,700

Ending Balance: TBD
LDO - USDT
RSRUSDT

"""


"""

"""

import re
from statistics import mean
import logging


def parse_message(initial_message: str) -> str:

    lines = initial_message.lower().splitlines()

    entry_line = next(line for line in lines if line.startswith("@everyone")).lower()
    for word in entry_line.split():
        if "usdt" in word:
            other_currency = word.split("usdt")[0]
            other_currency_cleaned = re.sub("[^A-Z]", "", other_currency)
            currencies = f"{other_currency_cleaned}/USDT"

    if entry_line.find("short") != -1:
        short_or_long = "short"
    elif entry_line.find("long") != -1:
        short_or_long = "long"
    else:
        logging.warning(
            f"short or long not catched, here is the entry_line: {entry_line}\
            \n initial_message: {initial_message}"
        )

    entry_prices = next(line for line in lines if line.startswith("entry"))

    prices = re.findall(r"\d.+", entry_prices)[0].split("-")

    if len(prices) == 2:
        price = mean([float(price) for price in prices])
    elif len(prices) == 1:
        price = prices[0]
    else:
        return

    price = round(price, 4)

    final = f"frostybot accounts:add stub=mystub:{short_or_long} symbol={currencies} price={price}"
    print(final)

    #  frostybot trade:mystub:short symbol=BTC/USD size=2000 price=7600


parse_message(s)
