
from binance.client import Client
from  .config import API_KEY, API_SECRET, USE_TESTNET, TESTNET_REST
from .logger import get_logger
from dotenv import load_dotenv
import os

load_dotenv()


logger = get_logger("client_factory")

def create_futures_client():
    """
    Create and return a python-binance Client configured for USDT-M futures testnet.
    The python-binance library supports `testnet=True` parameter.
    """
    client = Client(API_KEY, API_SECRET, testnet=USE_TESTNET)
    if USE_TESTNET:
        # ensure futures/testnet endpoint is used (python-binance sets this when testnet=True)
        # but as a safety we set the futures URL override for the client
        client.FUTURES_URL = TESTNET_REST
        logger.info("Created futures client in TESTNET mode with base %s", TESTNET_REST)
    else:
        logger.info("Created futures client in LIVE mode")
    return client
