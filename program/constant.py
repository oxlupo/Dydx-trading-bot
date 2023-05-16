from dydx3.constants import API_HOST_GOERLI, API_HOST_MAINNET
from decouple import config

# !!! SELECT MODE !!!
MODE = "DEVELOPMENT"

# Close all open positions and orders
ABORT_ALL_POSITION = False

# Find cointegrated pairs
FIND_COINTEGRATED = True

# Place Trades
PLACE_TRADES = True

# Resolution
RESOLUTION = "1HOUR"

# Stats Window
WINDOW = 21

# Thresholds - Opening
MAX_HALF_LIFE = 24
ZSCORE_THRESH = 1.5
USD_PER_TRADE = 50
USD_MIN_COLLATERAL = 1880

# Thresholds - Closing
CLOSE_AT_ZSCORE_CROSS = True

# Ethereum Address
ETHEREUM_ADDRESS = "0xE369faf7Cd822b826203e454F6555779872e10c4"

