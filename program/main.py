from constant import ABORT_ALL_POSITION, FIND_COINTEGRATED
from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices

if __name__ == "__main__":

    # Connect to Client
    try:
        print("Connecting to Client ...")
        client = connect_dydx()

    except Exception as exp:
        print(f"OOPS! Error Connecting to Client: {exp}")
        exit(1)

    # Abort all open positions
    if ABORT_ALL_POSITION:
        try:
            print("Closing all positions")
            close_orders = abort_all_positions(client)
        except Exception as exp:
            print(f"OOPS! Error Connecting to Client: {exp}")
            exit(1)

    # find Cointegrated Pairs
    if FIND_COINTEGRATED:

        # Construct Market Price
        try:
            print("Fetching market please allow 3 mints...")
            df_market_price = construct_market_prices(client)
        except Exception as e:
            print("Error constructing market prices", e)
            exit(1)
