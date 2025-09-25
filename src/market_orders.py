
from .b_client_factory import create_futures_client
from .logger import get_logger
from typing import Dict, Any
import time

logger = get_logger("market_orders")
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

def place_market_order(symbol: str, side: str, quantity: float, reduce_only: bool=False, **kwargs):
    """
    Place a USDT-M futures market order.
    side: BUY or SELL
    quantity: contract quantity (depends on symbol's lotSize)
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
            type="MARKET",
            quantity=quantity,
            reduceOnly=str(reduce_only).lower(),
            recvWindow=60000, 
            timestamp= int(time.time() * 1000) + offset,

        )
        params.update(kwargs)
        logger.debug("Placing market order: %s", params)
        logger.debug(f"Local time: {local_time}, Server time: {server_time['serverTime']}, Offset: {offset}")

        resp = client.futures_create_order(**params)
        _log_response("market_order", resp)
        return resp
    except Exception as e:
        logger.exception("Failed to place market order: %s", e)
        raise
