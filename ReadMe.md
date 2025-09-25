
 # Starting the App:
 Include API keys and secret
 Make a python enviornment using:
  1. python -m venv venv   to create python venv module
  2. ./venv/Scripts/activate  to activate the virtual enviornment in your cli
  3. Then run the main commands, configure according to your trade.

A main app can be made at the end of each order function, and the file can be called in terminal - python filename(example in oco orders).
The functions are connected to cli command entry point, there are options that configure trade information according to cli input. 

# Usage Commands:
Each command can be understood as python->entry to cli options->symbol representing the stock you want to trade->Whether to buy or sell(pick a side)->quantity of stocks->
Here, 
```
For MARKET Orders(order at market price):
python -m src.cli_entry market --symbol BTCUSDT --side BUY --quantity 0.001       
For LIMIT orders(order at market price upto a limit):
python -m src.cli_entry limit --symbol BTCUSDT --side SELL --quantity 0.001 --price 60000
For OCO orders:
python -m src.cli_entry oco --symbol BTCUSDT --side BUY --stop-price 110000 --limit-price 120000 --quantity 0.001
```

Binance does not have support for oco orders for future trading, only spot trading.


Additional commands:

Check version of cli(can be used CI/CD management):
```
python -m src.cli_entry version
```



```plaintext
project_root/
├── src/
│   ├── advanced_orders/
│   │    ├── oco_order.py           Make OCO orders
│   │    └── stop_limit_order.py    Make stop-limit orders
│   ├── __init__.py
│   ├── config.py              load API keys + settings
│   ├── logger.py              structured logging setup
│   ├── b_client_factory.py    create configured Binance client
│   ├── market_orders.py       market order functions
│   ├── limit_orders.py        limit order functions
│   └── cli_entry.py                 CLI entrypoint (argparse / click)
├── bot.log                    runtime logs (created by logger)
├── README.md
└── requirements.txt
```

# API SETUP:
Some credentials from binance futures tesnet page, others are set values you need to pass as parameters.
Make a .env file and add these variables, use python-dotenv library in your virtual enviornment, and call the variables using load.env().

1. BINANCE_API_KEY=d6........
2. BINANCE_API_SECRET=w4...
3. USE_TESTNET=true
4. TESTNET_REST="https://testnet.binancefuture.com"



# First Functional Trade:

## For market orders(with above command):
```
BTCUSDT --side BUY --quantity 0.001
2025-09-24 02:09:14 | INFO    | client_factory | Created futures client in TESTNET mode with base https://testnet.binancefuture.com
2025-09-24 02:09:15 | INFO    | client_factory | Created futures client in TESTNET mode with base https://testnet.binancefuture.com
2025-09-24 02:09:15 | INFO    | cli | CLI: market BTCUSDT BUY 0.001
2025-09-24 02:09:16 | DEBUG   | market_orders | Placing market order: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.001, 'reduceOnly': 'false', 'recvWindow': 60000, 'timestamp': 1758659956285}
2025-09-24 02:09:16 | DEBUG   | market_orders | Local time: 1758659955017, Server time: 1758659954937, Offset: -80
2025-09-24 02:09:16 | INFO    | market_orders | market_order response: {'orderId': 5677536210, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'x-Cb7ytekJ1b23510c279785b80e9bfb', 'price': '0.00', 'avgPrice': '0.00', 'origQty': '0.001', 'executedQty': '0.000', 'cumQty': '0.000', 'cumQuote': '0.00000', 'timeInForce': 'GTC', 'type': 'MARKET', 'reduceOnly': False, 'closePosition': False, 'side': 'BUY', 'positionSide': 'BOTH', 'stopPrice': '0.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'MARKET', 'priceMatch': 'NONE', 'selfTradePreventionMode': 'EXPIRE_MAKER', 'goodTillDate': 0, 'updateTime': 1758659956725}
{'orderId': 5677536210, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'x-Cb7ytekJ1b23510c279785b80e9bfb', 'price': '0.00', 'avgPrice': '0.00', 'origQty': '0.001', 'executedQty': '0.000', 'cumQty': '0.000', 'cumQuote': '0.00000', 'timeInForce': 'GTC', 'type': 'MARKET', 'reduceOnly': False, 'closePosition': False, 'side': 'BUY', 'positionSide': 'BOTH', 'stopPrice': '0.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'MARKET', 'priceMatch': 'NONE', 'selfTradePreventionMode': 'EXPIRE_MAKER', 'goodTillDate': 0, 'updateTime': 1758659956725}
```
## For limit orders:
```
BTCUSDT --side SELL --quantity 0.001 --price 200000   
2025-09-24 02:13:54 | INFO    | client_factory | Created futures client in TESTNET mode with base https://testnet.binancefuture.com
2025-09-24 02:13:54 | INFO    | client_factory | Created futures client in TESTNET mode with base https://testnet.binancefuture.com
2025-09-24 02:13:55 | INFO    | cli | CLI: limit BTCUSDT SELL 0.001 @ 200000.0
2025-09-24 02:13:56 | DEBUG   | limit_orders | Placing limit order: {'symbol': 'BTCUSDT', 'side': 'SELL', 'type': 'LIMIT', 'timeInForce': 'GTC', 'quantity': 0.001, 'price': '200000.0', 'newOrderRespType': 'RESULT', 'reduceOnly': 'false', 'recvWindow': 60000, 'timestamp': 1758660236106}
2025-09-24 02:13:56 | INFO    | limit_orders | limit_order response: {'orderId': 5677539917, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'x-Cb7ytekJ21cc64b33bef07a95ab2ba', 'price': '200000.00', 'avgPrice': '0.00', 'origQty': '0.001', 'executedQty': '0.000', 'cumQty': '0.000', 'cumQuote': '0.00000', 'timeInForce': 'GTC', 'type': 'LIMIT', 'reduceOnly': False, 'closePosition': False, 'side': 'SELL', 'positionSide': 'BOTH', 'stopPrice': '0.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'LIMIT', 'priceMatch': 'NONE', 'selfTradePreventionMode': 'EXPIRE_MAKER', 'goodTillDate': 0, 'updateTime': 1758660236553}
{'orderId': 5677539917, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'x-Cb7ytekJ21cc64b33bef07a95ab2ba', 'price': '200000.00', 'avgPrice': '0.00', 'origQty': '0.001', 'executedQty': '0.000', 'cumQty': '0.000', 'cumQuote': '0.00000', 'timeInForce': 'GTC', 'type': 'LIMIT', 'reduceOnly': False, 'closePosition': False, 'side': 'SELL', 'positionSide': 'BOTH', 'stopPrice': '0.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'LIMIT', 'priceMatch': 'NONE', 'selfTradePreventionMode': 'EXPIRE_MAKER', 'goodTillDate': 0, 'updateTime': 1758660236553}
```

Decided to implement  OCO orders. Binance does not have OCO order support in itself so a combination of stop-market and take-profit is used get the same effect as oco orders, we start with defining base parameters and  place two exit orders (STOP_MARKET + TAKE_PROFIT_MARKET, both closePosition=True).Listen for order fills and cancels the remaining order when one executes. like an if statement with an or condition.


## OCO order:
```
2025-09-25 02:35:04 | INFO    | client_factory | Created futures client in TESTNET mode with base https://testnet.binancefuture.com
2025-09-25 02:35:05 | INFO    | client_factory | Created futures client in TESTNET mode with base https://testnet.binancefuture.com
2025-09-25 02:35:06 | INFO    | client_factory | Created futures client in TESTNET mode with base https://testnet.binancefuture.com
2025-09-25 02:35:06 | INFO    | client_factory | Created futures client in TESTNET mode with base https://testnet.binancefuture.com
2025-09-25 02:35:07 | INFO    | cli_entry | CLI: oco BTCUSDT BUY 110000.0 120000.0 0.001
2025-09-25 02:35:08 | DEBUG   | oco_orders | Placing STOP_MARKET order: {'symbol': 'BTCUSDT', 'side': 'SELL', 'quantity': 0.001, 'recvWindow': 60000, 'timestamp': 1758747909518, 'type': 'STOP_MARKET', 'stopPrice': '110000.0', 'closePosition': True}
2025-09-25 02:35:08 | INFO    | oco_orders | stop_loss response: {'orderId': 5678560335, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'x-Cb7ytekJc3aa19572e0928d31c60f4', 'price': '0.00', 'avgPrice': '0.00', 'origQty': '0.000', 'executedQty': '0.000', 'cumQty': '0.000', 'cumQuote': '0.00000', 'timeInForce': 'GTC', 'type': 'STOP_MARKET', 'reduceOnly': True, 'closePosition': True, 'side': 'SELL', 'positionSide': 'BOTH', 'stopPrice': '110000.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'STOP_MARKET', 'priceMatch': 'NONE', 'selfTradePreventionMode': 'EXPIRE_MAKER', 'goodTillDate': 0, 'updateTime': 1758747909960}
2025-09-25 02:35:08 | DEBUG   | oco_orders | Placing TAKE_PROFIT_MARKET order: {'symbol': 'BTCUSDT', 'side': 'SELL', 'quantity': 0.001, 'recvWindow': 60000, 'timestamp': 1758747909518, 'type': 'TAKE_PROFIT_MARKET', 'stopPrice': '120000.0', 'closePosition': True}
2025-09-25 02:35:09 | INFO    | oco_orders | take_profit response: {'orderId': 5678560338, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'x-Cb7ytekJ23c8133e9533af66109a01', 'price': '0.00', 'avgPrice': '0.00', 'origQty': '0.000', 'executedQty': '0.000', 'cumQty': '0.000', 'cumQuote': '0.00000', 'timeInForce': 'GTC', 'type': 'TAKE_PROFIT_MARKET', 'reduceOnly': True, 'closePosition': True, 'side': 'SELL', 'positionSide': 'BOTH', 'stopPrice': '120000.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'TAKE_PROFIT_MARKET', 'priceMatch': 'NONE', 'selfTradePreventionMode': 'EXPIRE_MAKER', 'goodTillDate': 0, 'updateTime': 1758747910400}
STOP_MARKET order placed:
{'orderId': 5678560335, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'x-Cb7ytekJc3aa19572e0928d31c60f4', 'price': '0.00', 'avgPrice': '0.00', 'origQty': '0.000', 'executedQty': '0.000', 'cumQty': '0.000', 'cumQuote': '0.00000', 'timeInForce': 'GTC', 'type': 'STOP_MARKET', 'reduceOnly': True, 'closePosition': True, 'side': 'SELL', 'positionSide': 'BOTH', 'stopPrice': '110000.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'STOP_MARKET', 'priceMatch': 'NONE', 'selfTradePreventionMode': 'EXPIRE_MAKER', 'goodTillDate': 0, 'updateTime': 1758747909960}
TAKE_PROFIT_MARKET order placed:
{'orderId': 5678560338, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'x-Cb7ytekJ23c8133e9533af66109a01', 'price': '0.00', 'avgPrice': '0.00', 'origQty': '0.000', 'executedQty': '0.000', 'cumQty': '0.000', 'cumQuote': '0.00000', 'timeInForce': 'GTC', 'type': 'TAKE_PROFIT_MARKET', 'reduceOnly': True, 'closePosition': True, 'side': 'SELL', 'positionSide': 'BOTH', 'stopPrice': '120000.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'TAKE_PROFIT_MARKET', 'priceMatch': 'NONE', 'selfTradePreventionMode': 'EXPIRE_MAKER', 'goodTillDate': 0, 'updateTime': 1758747910400}
```

**Important:** Always set `USE_TESTNET=true` before trading.  
*Tip:* Run `--help` to see all options.