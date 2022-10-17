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



# with open("myfile.txt", "a") as file1:
#     for idx, message in enumerate(list_lomas):
#         file1.write(f"Message index: {idx}")
#         file1.write(
#             f"\n {idx}::::::{datetime.utcnow().isoformat()}   ::::  INITIAL MESSAGE:\n{message}"
#         )
#         file1.write(
#             f"\n{idx}::::::{datetime.utcnow().isoformat()}) ::::: PARSED MESSAGE: {parse_message(message)}\n\n"
#         )
    # Writing data to a file
