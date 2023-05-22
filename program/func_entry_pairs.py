from constant import ZSCORE_THRESH, USD_PER_TRADE, USD_MIN_COLLATERAL
from func_utils import format_number
from func_public import get_candles_recent
from func_cointegration import calculate_zscore
from func_private import is_open_positions
from func_bot_agent import BotAgent
import pandas as pd
import json
from pprint import pprint
from termcolor import colored


# Open positions
def open_positions(client):
    """
    managing findig triggers for trade entry
    Store trades for managing later on exit function
    :param client:
    :return:
    """

    df = pd.read_csv("cointegrated_pairs.csv")
    print(df)

