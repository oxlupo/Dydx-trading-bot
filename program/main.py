from constant import ABORT_ALL_POSITION, FIND_COINTEGRATED
from func_connections import connect_dydx
from func_cointegration import store_cointegration_results
from func_private import abort_all_positions
from func_public import construct_market_prices
from termcolor import colored


if __name__ == "__main__":

    # Connect to Client
    try:
        print(colored("Connecting to Client ...", "yellow"))
        client = connect_dydx()

    except Exception as exp:
        print(colored(f"OOPS! Error Connecting to Client: {exp}", "red"))
        exit(1)

    # Abort all open positions
    if ABORT_ALL_POSITION:
        try:
            print("Closing all positions")
            close_orders = abort_all_positions(client)
        except Exception as exp:
            print(colored(f"OOPS! Error Connecting to Client: {exp}", "red"))
            exit(1)

    # find Cointegrated Pairs
    if FIND_COINTEGRATED:

        # Stored Market Price
        try:
            print(colored("Storing cointegrated pairs Please wait (maybe 3 mints) ... ", "yellow"))
            df_market_price = construct_market_prices(client)
            store_result = store_cointegration_results(df_market_price)
            if store_result != "saved":
                print(colored("Error saving cointegrated pairs", "red"))
                exit(1)

        except Exception as e:
            print(colored(f"Error saving cointegrated pairs: {e}", "red"))
            exit(1)
