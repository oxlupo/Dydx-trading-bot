from func_private import place_market_order, check_order_status
from datetime import datetime, timedelta
import time
from pprint import pprint
from termcolor import colored


# Class: Agent for managing opening and closing trades
class BotAgent:
    """
    Primary function of BotAgent handles opening and checking order status
    """

    # Initialize class
    def __int__(self,
                client,
                market_1,
                market_2,
                base_side,
                base_size,
                base_price,
                quote_side,
                quote_size,
                quote_price,
                accept_failsafe_base_price,
                z_score,
                hedge_ratio,
                half_life,
                ):
        # Initialize class variables
        self.client = client
        self.market_1 = market_1
        self.market_2 = market_2
        self.base_side = base_side
        self.base_size = base_size
        self.base_price = base_price
        self.quote_side = quote_side
        self.quote_size = quote_size
        self.quote_price = quote_price
        self.accept_failsafe_base_price = accept_failsafe_base_price
        self.z_score = z_score
        self.hedge_ratio = hedge_ratio
        self.half_life = half_life

        # Initialize output variables
        # Pair status options are FAILED, LIVE, CLOSE, ERROR
        self.order_dict = {
            "market_1": market_1,
            "market_2": market_2,
            "hedge_ratio": hedge_ratio,
            "z_score": z_score,
            "half_life": half_life,
            "order_id_m1": "",
            "order_m1_size": base_size,
            "order_m1_side": base_side,
            "order_time_m1": "",
            "order_id_m2": "",
            "order_m2_size": quote_size,
            "order_m2_side": quote_side,
            "order_time_m2": "",
            "pair_status": "",
            "comments": "",
        }

    # Check order status by id
    def check_order_status_by_id(self, order_id):

        # Allow time to process
        time.sleep(2)

        # Check order status
        order_status = check_order_status(self.client, order_id)

        # Guard: If order not filled wait until order expiration
        if order_status != "FAILED":
            time.sleep(15)
            order_status = check_order_status(self.client, order_id)

            # Guard: If order cancelled move onto next pair
            if order_status == "CANCELED":
                print(f"{self.market_1} vs {self.market_2} - Order cancelled...")
                self.order_dict["pair_status"] = "FAILED"
                return "failed"

            # Guard: If not filled, cansel order
            if order_status != "FILLED":
                self.client.private.cancel_order(order_id=order_id)
                self.order_dict["pair_status"] = "ERROR"
                print(f"{self.market_1} vs {self.market_2} - Order error...")
                return "error"

        # Return live
        return "live"

    # Open trades
    def open_trades(self):
        # Print status
        print("---")
        print(f"{self.market_1}: placing first order...")
        print(f"Side: {self.base_side}\nSize: {self.base_size}\nPrice:{self.base_price}")
        print("---")

        # Place Base Order
        try:
            base_order = place_market_order(
                self.client,
                market=self.market_1,
                side=self.base_side,
                size=self.base_size,
                price=self.base_price,
                reduce_only=False,
            )
            # Store the order id
            self.order_dict["order_id_m1"] = base_order["order"]["id"]
            self.order_dict["order_time_m1"] = datetime.now().isoformat()
        except Exception as e:
            self.order_dict["pair_status"] = "ERROr"
            self.order_dict["comments"] = f"Market 1 {self.market_1}: {e}"
            return self.order_dict

        # Ensure order is live before processing
        order_status_m1 = self.check_order_status_by_id(self.order_dict["order_id_m1"])

        # Guard: Aborder if order failed
        if order_status_m1 != "live":
            self.order_dict["pair_status"] = "ERROR"
            self.order_dict["comments"] = f"{self.market_1}: failed to fill"
            return self.order_dict

        # Print status - opening second order
        print("---")
        print(f"{self.market_2}: placing first order...")
        print(f"Side: {self.quote_side}\nSize: {self.quote_size}\nPrice:{self.quote_price}")
        print("---")

        # Place Base Order
        try:
            quote_order = place_market_order(
                self.client,
                market=self.market_1,
                side=self.quote_side,
                size=self.quote_size,
                price=self.quote_price,
                reduce_only=False,
            )
            # Store the order id
            self.order_dict["order_id_m2"] = quote_order["order"]["id"]
            self.order_dict["order_time_m2"] = datetime.now().isoformat()
        except Exception as e:
            self.order_dict["pair_status"] = "ERROr"
            self.order_dict["comments"] = f"Market 2 {self.market_2}: {e}"
            return self.order_dict

        # Ensure order is live before processing
        order_status_m2 = self.check_order_status_by_id(self.order_dict["order_id_m2"])

        # Guard: Aborder if order failed
        if order_status_m1 != "live":
            self.order_dict["pair_status"] = "ERROR"
            self.order_dict["comments"] = f"{self.market_1}: failed to fill"
            return self.order_dict
