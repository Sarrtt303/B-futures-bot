
from .b_client_factory import create_futures_client
from .logger import get_logger
from typing import Dict, Any
import time

logger = get_logger("limit_orders")
client = create_futures_client()
server_time = client.get_server_time()
local_time = int(time.time() * 1000)
offset = server_time["serverTime"] - local_time

def _log_response(action: str, resp: Dict[str, Any]):
    logger.info("%s response: %s", action, resp)

def validate_symbol(symbol: str) -> bool:
    info = client.futures_exchange_info()
    symbols = {s['symbol'] for s in info.get('symbols', [])}
    return symbol.upper() in symbols

def place_limit_order(symbol: str, side: str, quantity: float, price: float, time_in_force: str="GTC", post_only: bool=False, reduce_only: bool=False, **kwargs):
    """
    Place a USDT-M futures LIMIT order.
    time_in_force: GTC, IOC, or FOK
    """
    symbol = symbol.upper()
    side = side.upper()
    if side not in ("BUY", "SELL"):
        raise ValueError("side must be BUY or SELL")

    if not validate_symbol(symbol):
        raise ValueError(f"Unknown symbol {symbol}")

    try:
        params = dict(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce=time_in_force,
            quantity=quantity,
            price=str(price),
            newOrderRespType="RESULT",
            reduceOnly=str(reduce_only).lower(),
            recvWindow=60000, 
            timestamp= int(time.time() * 1000) + offset
        )
        if post_only:
            params["type"] = "LIMIT_MAKER"
        params.update(kwargs)
        logger.debug("Placing limit order: %s", params)
        resp = client.futures_create_order(**params)
        _log_response("limit_order", resp)
        return resp
    except Exception as e:
        logger.exception("Failed to place limit order: %s", e)
        raise
