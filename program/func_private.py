from datetime import datetime, timedelta

def place_market_order(client, market, side, size, price, reduce_only):
    """Place market order"""
    # Get Position ID
    account_response = client.private.get_account()
    position_id = account_response.data['account']['positionId']

    # Get expiration time
    server_time = client.public.get_time()
    expiration = datetime.fromisoformat(server_time.data["iso"].replace("Z", "")) + timedelta(seconds=70)

    # place and order
    placed_order = client.private.create_order(
        position_id=position_id,  # required for creating the order signature
        market=market,
        side=side,
        order_type="MARKET",
        post_only=False,
        size=size,
        price=price,
        limit_fee='0.015',
        expiration_epoch_seconds=expiration.timestamp(),
        time_in_force="FOK",
        reduce_only=reduce_only
    )
    # Return result
    return placed_order.data


def abort_all_positions(client):
    """Abort all open positions"""
    pass


