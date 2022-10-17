from datetime import datetime


import re
from statistics import mean


def parse_message(initial_message: str) -> str:

    lines = initial_message.lower().splitlines()

    entry_line_list = [
        line for line in lines if re.compile(r"(?i)trade \d+").search(line)
    ]

    if len(entry_line_list) == 0:
        writter_helper(f"entry_line_list cant be found for message", initial_message)
        return

    elif len(entry_line_list) > 1:
        writter_helper(
            "entry_line_list has more then one lines cant be found for message",
            initial_message,
        )
        return

    entry_line = entry_line_list[0]
    for word in entry_line.split():
        if "usdt" in word:
            other_currency = word.split("usdt")[0]
            other_currency_cleaned = re.sub("[A-Z]", "", other_currency)
            other_currency_upper = other_currency_cleaned.upper()
            currencies = f"{other_currency_upper}-USDT"

    if entry_line.find("short") != -1:
        short_or_long = "short"
    elif entry_line.find("long") != -1:
        short_or_long = "long"
    else:

        writter_helper(
            "short or long not catched, here is the entry_line: {entry_line}",
            initial_message,
        )
        return

    maybe_entry_prices_line = [line for line in lines if line.startswith("entry")]
    # if len(line for line in lines if line.startswith("entry"))
    if len(maybe_entry_prices_line) == 1:
        entry_prices = next(line for line in lines if line.startswith("entry"))
    elif maybe_entry_prices_line:
        writter_helper("multiple ENTRY PRICE found for message", initial_message)
        return

    else:
        writter_helper("Enttry price not found", initial_message)
        return

    prices = re.findall(r"\d.+", entry_prices)[0].split("-")

    if len(prices) == 2:

        price = mean([float(price.replace(",", "")) for price in prices])
    elif len(prices) == 1:
        price = float(prices[0].replace(",", ""))
    else:
        writter_helper("Problem with prices", initial_message)
        return

    price = round(price, 4)

    final = f"frostybot trade:test:{short_or_long} symbol={currencies} price={price}"
    writter_helper(final, "GIVEN ORDER!!!!! : ")
    return final


def writter_helper(helper_message, initial_message):
    with open("myfile.txt", "a") as file1:

        file1.write(
            f"\n{datetime.utcnow().isoformat()}   ::::  INITIAL MESSAGE:\n{initial_message}"
        )
        file1.write(
            f"\n{datetime.utcnow().isoformat()}) ::::: PARSED MESSAGE: {parse_message(helper_message)}\n\n"
        )
    # Writing data to a file
