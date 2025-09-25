from ..b_client_factory import create_futures_client
from ..logger import get_logger
from typing import Dict, Any, Tuple
import time

logger = get_logger("oco_orders")
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


def get_mark_price(symbol: str) -> float:
    """Fetch the current mark price of a futures symbol"""
    data = client.futures_mark_price(symbol=symbol.upper())
    return float(data["markPrice"])


def validate_oco_prices(side: str, stop_price: float, limit_price: float, mark_price: float):
    """
    Ensure stop/limit prices make sense relative to current market price.
    """
    if side == "BUY":  # long, exit with SELL
        if not (stop_price < mark_price and limit_price > mark_price):
            raise ValueError(
                f"Invalid OCO for LONG @ {mark_price}: "
                f"stop {stop_price} must be < mark, limit {limit_price} must be > mark"
            )
    else:  # SELL (short), exit with BUY
        if not (stop_price > mark_price and limit_price < mark_price):
            raise ValueError(
                f"Invalid OCO for SHORT @ {mark_price}: "
                f"stop {stop_price} must be > mark, limit {limit_price} must be < mark"
            )


def place_oco_order(
    symbol: str,
    side: str,
    stop_price: float,
    limit_price: float,
    quantity: float,
    reduce_only: bool = True,
    **kwargs
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Simulate an OCO (One-Cancels-the-Other) order in Binance USDT-M Futures.
    """

    symbol = symbol.upper()
    side = side.upper()

    if side not in ("BUY", "SELL"):
        raise ValueError("side must be BUY or SELL")
    if not validate_symbol(symbol):
        raise ValueError(f"Unknown symbol {symbol}")

    # 🔎 Validate prices relative to current mark price
    mark_price = get_mark_price(symbol)
    validate_oco_prices(side, stop_price, limit_price, mark_price)

    try:
        base_params = dict(
            symbol=symbol,
            side="SELL" if side == "BUY" else "BUY",  # opposite side to exit
            quantity=quantity,
            recvWindow=60000,
            timestamp=int(time.time() * 1000) + offset,
        )
        base_params.update(kwargs)

        # Stop-loss
        stop_params = base_params.copy()
        stop_params.update(
            dict(
                type="STOP_MARKET",
                stopPrice=str(stop_price),
                closePosition=True,
            )
        )
        logger.debug("Placing STOP_MARKET order: %s", stop_params)
        stop_resp = client.futures_create_order(**stop_params)
        _log_response("stop_loss", stop_resp)

        # Take-profit
        tp_params = base_params.copy()
        tp_params.update(
            dict(
                type="TAKE_PROFIT_MARKET",
                stopPrice=str(limit_price),
                closePosition=True,
            )
        )
        logger.debug("Placing TAKE_PROFIT_MARKET order: %s", tp_params)
        tp_resp = client.futures_create_order(**tp_params)
        _log_response("take_profit", tp_resp)

        return stop_resp, tp_resp

    except Exception as e:
        logger.exception("Failed to place OCO order: %s", e)
        raise
