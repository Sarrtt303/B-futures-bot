
from ..b_client_factory import create_futures_client
from ..logger import get_logger
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

def place_stop_limit_order(
    symbol: str,
    side: str,
    stop_price: float,
    limit_price: float,
    quantity: float,
    time_in_force: str = "GTC",
    reduce_only: bool = False,
    **kwargs
):
    """
    Place a USDT-M futures stop-limit order.
    side: BUY or SELL
    stop_price: Price that triggers the limit order
    limit_price: Price for the limit order
    quantity: Contract quantity (depends on symbol's lotSize)
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
            type="STOP_LOSS_LIMIT",  # or "TAKE_PROFIT_LIMIT"
            stopPrice=str(stop_price),
            price=str(limit_price),
            quantity=quantity,
            timeInForce=time_in_force,
            reduceOnly=str(reduce_only).lower(),
            recvWindow=60000,
            timestamp=int(time.time() * 1000) + offset,
        )
        params.update(kwargs)
        logger.debug("Placing stop-limit order: %s", params)
        logger.debug(f"Local time: {local_time}, Server time: {server_time['serverTime']}, Offset: {offset}")
        resp = client.futures_create_order(**params)
        _log_response("stop_limit_order", resp)
        return resp
    except Exception as e:
        logger.exception("Failed to place stop-limit order: %s", e)
        raise


