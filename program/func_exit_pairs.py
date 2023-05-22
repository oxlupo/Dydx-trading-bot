from constant import CLOSE_AT_ZSCORE_CROSS
from func_utils import format_number
from func_public import get_candles_recent
from func_private import place_market_order
from func_cointegration import calculate_zscore
from func_bot_agent import BotAgent
import json
import time
from pprint import pprint
from termcolor import colored


# Close positions
def manage_trade_exits(client):
    """
    Manage exiting open positions
    Based upon criteria set in constant
    :param client:
    :return:
    """

    # Initialize saving output
    save_output = []

    # Opening Json file
    try:
        open_positions_file = open("bot_agents.json")
        open_positions_dict = json.load(open_positions_file)
    except:
        return "complete"

    # Guard: Exit if no open positions in file
    if len(open_positions_dict) < 1:
        return "complete"

    # Get all open positions per trading platform
    exchange_pos = client.private.get_posiotions(status="OPEN")
    all_exc_pos = exchange_pos.data["positions"]
    markets_live = []
    for p in all_exc_pos:
        markets_live.append(p["market"])

    # Protect API
    time.sleep(0.5)
    pprint(markets_live)
    # Check all saved positions match order record
    # Exit trade according to any exit trade rules
    for position in open_positions_dict:

        # Initialize is_close trigger
        is_close = False

        # Extract positions matching information from file - market 1
        position_market_m1 = position["market_1"]
        position_size_m1 = position["order_m1_size"]
        position_side_m1 = position["order_m1_side"]

        # Extract positions matching information from file - market 2
        position_market_m2 = position["market_2"]
        position_size_m2 = position["order_m2_size"]
        position_side_m2 = position["order_m2_side"]

        # Protect API
        time.sleep(0.5)

        # Get order info m1 per exchange
        order_m1 = client.private.get_order_by_id(position["order_id_m1"])
        order_market_m1 = order_m1.data["order"]["market"]
        order_size_m1 = order_m1.data["order"]["size"]
        order_side_m1 = order_m1.data["order"]["side"]

        order_m2 = client.private.get_order_by_id(position["order_id_m2"])
        order_market_m2 = order_m2.data["order"]["market"]
        order_size_m2 = order_m2.data["order"]["size"]
        order_side_m2 = order_m2.data["order"]["side"]

        # Perform matching checks
        check_m1 = position_market_m1 == order_market_m1 and position_size_m1 == order_size_m1 and position_side_m1 == order_side_m1
        check_m2 = position_market_m2 == order_market_m2 and position_size_m2 == order_size_m2 and position_side_m2 == order_side_m2
        check_live = position_market_m1 in markets_live and position_market_m2 in markets_live

