from constant import ABORT_ALL_POSITION
from func_connections import connect_dydx

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

        except Exception as exp:
