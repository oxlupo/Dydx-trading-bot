from func_utils import get_ISO_times
from constant import RESOLUTION
import pandas as pd
import numpy as np
import time
from pprint import pprint


# Get relavant time periods for ISO from and to
ISO_TIMES = get_ISO_times()
print(ISO_TIMES)


def get_candles_historical(client, market):
    """ get candles historical """

    # Define output
    close_prices = []

    # Extract historical data for each timeframe

    for timeframe in ISO_TIMES.keys():

        # Confirm time needed
        tf_obj = ISO_TIMES[timeframe]
        from_iso = tf_obj["from_iso"]
        to_iso = tf_obj["to_iso"]

        # protect rate limits
        time.sleep(0.2)

        # Get data
        candles = client.public.get_candles(
            market=market,
            resolution=RESOLUTION,
            from_iso=from_iso,
            to_iso=to_iso,
            limit=100
        )

        # Structure Data
        for candle in candles.data["candles"]:
            close_prices.append({"datetime": candle["startAt"], market: candle["close"]})

    # Construct and return DataFrame
    close_prices.reverse()
    return close_prices


def construct_market_prices(client):
    """ Construct market prices """

    # Declare variables
    tradeable_markets = []
    markets = client.public.get_markets()

    for market in markets.data["markets"].keys():
        market_info = market.data["market"][market]
        if market_info["status"] == "ONLINE" and market_info["type"] == "PERPETUAL":
            tradeable_markets.append(market)

    # Set initial DataFrame
    close_prices = get_candles_historical(client, tradeable_markets, tradeable_markets[0])
    # df = pd.DataFrame(close_prices)
    # df.set_index("datetime", inplace=True)
    pprint(close_prices)


