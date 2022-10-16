from datetime import datetime


import re
from statistics import mean
import logging


def parse_message(initial_message: str) -> str:

    lines = initial_message.lower().splitlines()

    entry_line_list = [
        line for line in lines if re.compile(r"(?i)trade \d+").search(line)
    ]

    if len(entry_line_list) == 0:
        return f"entry_line_list cant be found for message"

    elif len(entry_line_list) > 1:
        return f"entry_line_list has more then one lines cant be found for message"

    entry_line = entry_line_list[0]
    for word in entry_line.split():
        if "usdt" in word:
            other_currency = word.split("usdt")[0]
            print(other_currency)
            other_currency_cleaned = re.sub("[A-Z]", "", other_currency)
            other_currency_upper = other_currency_cleaned.upper()
            currencies = f"{other_currency_upper}-USDT"

    if entry_line.find("short") != -1:
        short_or_long = "short"
    elif entry_line.find("long") != -1:
        short_or_long = "long"
    else:
        logging.warning(
            f"short or long not catched, here is the entry_line: {entry_line}\
            \n initial_message: {initial_message}"
        )

    maybe_entry_prices_line = [line for line in lines if line.startswith("entry")]
    # if len(line for line in lines if line.startswith("entry"))
    if len(maybe_entry_prices_line) == 1:
        entry_prices = next(line for line in lines if line.startswith("entry"))
    elif maybe_entry_prices_line:
        return "multiple ENTRY PRICE found for message"

    else:
        return "ENTRY PRICE NOT found for message"

    prices = re.findall(r"\d.+", entry_prices)[0].split("-")

    if len(prices) == 2:

        price = mean([float(price.replace(",", "")) for price in prices])
    elif len(prices) == 1:
        price = float(prices[0].replace(",", ""))
    else:
        return

    price = round(price, 4)

    final = f"frostybot trade:test:{short_or_long} symbol={currencies} price={price}"
    return final


# with open("myfile.txt", "w") as file1:
#     # Writing data to a file
#     for message in s.split(""""

list_lomas = [
    """
@everyone Trade 25: ETHUSDT - LONG

Closed at $1296 for a ~1.5% loss.

Still think longs are decent bets here but not going to take anything overnight. If my curse with ETH continues, that only means that it's going to pump tonight (within the next 8 hours).

""",
    """

@everyone Trade 26: RSRUSDT - SHORT

Entry: 0.008561
Size: $170K (size restriction + hasn’t actually broken down)
Stop Loss: above 0.0088 on 15min close

Target 1: 0.008-0081

Chart: mobile

Reason for entry: h1 distrib (sweep + momentum slowing)

""",
    """

@everyone Trade 27: ETHUSDT - SHORT

Entry: $1327.50
Size: $500K (adding up to 1348-$1.5M)
Stop Loss: H1 close above $1350

Target: $1290-1295
Target 2: a lot lower (cascade)

Chart: Mobile (h1 resistance)

""",
    """

I’m filled and scared
Please whoever is casting the curse, end it
Current position(s) update @everyone
IMG.JPG

""",
    """

ZERO

""",
    """

ZERO

""",
    """

ZERO

""",
    """

Both trades have hit targets and closed! @everyone

""",
    """

@everyone Trade 28: XRPUSDT - SHORT

Entry: 0.489
Size: $750K (keep risk low—this is about 2%)
Stop: H1 above 0.50

Target: 0.45-0.455

Chart: Mobile

Reason for Entry: SEC news playing out, think it pulls back now that there’s no narrative. (LTF 15min setup)

""",
    """

@everyone Closed XRP early at 0.477, gotta head out for dinner can’t sit and watch the charts

""",
    """

THIS ONE WAS HTML - STRIKED
@everyone Trade 30: RSRUSDT - SHORT 
STOPPED OUT
Entry: 0.8295
Size: $250K
Stop Loss: H1 above 0.85

Target: 0.72-0.74

Chart: Mobile

Reason for Entry: either momentum dissipates here or it’s going significantly higher so R:R is actually very nice.

Also wanted the 30 trades a month goal to be hit (1 average every day)

""",
    """

I lied that was 29, ima find another trade tmrw goddamnit

""",
    """

@everyone placing some asks on LUNC. Opened a starter position around $250k

Asks spread through about 38, heading to sleep after a long ass day but just wanted to share so there’s no hindsight tmrw morning

""",
    """

@everyone Ah, weekends over.

Official LUNC position is currently:

Entry: $0.346
Size: $520K

We're also looking to short RSR once again as well, I think it's fucked. This mainnet lunch + influencer pumps are almost always a fast ticket to poverty.

""",
    """

@everyone Alright, closed LUNC at ~0.31ish so I can record the video recap for September.
This trade is taking too long and it's killing my vibe on the journal.
So going to do the recap video, screenshots and what not tomorrow and we begin October trading.

""",
    """

Trades 15-30 and recap will be uploaded tomorrow morning. Roughly 12p PST.

They'll be uploaded individually into this channel cause I tried looking for various diff. ways to do it and... unfortunately nothing too great. 

Maybe I'll make a separate tab to upload the journal stuff.

""",
    """

@everyone Closing XRP trade at literal entry (5240).

Too resilient here, remember. We don’t wait for the market to prove us wrong. If it’s not showing us we’re right within a reasonable amount of time, it doesn’t make sense to stay in it.

Exit and will look for a diff setup soon.

""",
    """

@everyone Trade 31: SUSHIUSDT - LONG

Entry: 1.248
Size: $475K
Stop Loss: H1 close below $1.21 or wick below $1.18

Target: $1.36-1.38

Starting Balance: $1
Ending Balance: HIGHER!

Chart: https://www.tradingview.com/x/FhjnO5jb/

""",
    """

Still in LUNC, stopped on SUSHI. @everyone

""",
    """

@everyone Trade 32: LUNCUSDT - SHORT

Entry: 0.284
Size: $475K
Stop Loss: H1 close above $0.294

Target 1: 0.25-0.26
Target 2: 0.18-0.19

Starting Balance: $1
Ending Balance: HIGHER!

Reason for Entry: Basically looking at a pair trade here between 2 shit coins with terrible recent news (horse finger ??? + zero usage burns)

Chart: https://www.tradingview.com/x/Yf5oMZhw/

""",
    """

@everyone Trade 33: BTCUSDT - SHORT

Entry: $18
Stop Loss: $19.4K
Size: $2M

Target 1: $17-17.5K

Chart: Mobile (H1 retest of range)
""",
]

with open("myfile.txt", "a") as file1:
    for idx, message in enumerate(list_lomas):
        file1.write(f"Message index: {idx}")
        file1.write(
            f"\n {idx}::::::{datetime.utcnow().isoformat()}   ::::  INITIAL MESSAGE:\n{message}"
        )
        file1.write(
            f"\n{idx}::::::{datetime.utcnow().isoformat()}) ::::: PARSED MESSAGE: {parse_message(message)}\n\n"
        )
    # Writing data to a file
