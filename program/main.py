from constant import ABORT_ALL_POSITION
from func_connections import connect_dydx
from func_private import abort_all_positions

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
