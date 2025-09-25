# src/cli.py
import click
from .market_orders import place_market_order
from .limit_orders import place_limit_order
from .advanced_orders.oco_order import place_oco_order
from .advanced_orders.stop_limit_order import place_stop_limit_order
from .logger import get_logger

logger = get_logger("cli_entry")

@click.group()
def cli():
    """Simple CLI for placing futures orders on Binance Testnet"""
    pass

@cli.command()
def version():
    """Display the CLI version."""
    click.echo("Binance Trade Bot v1.0.0")


@cli.command()
@click.option("--symbol", required=True, help="Trading symbol like BTCUSDT")
@click.option("--side", required=True, type=click.Choice(["BUY", "SELL"], case_sensitive=False))
@click.option("--quantity", required=True, type=float)
def market(symbol, side, quantity):
    """Place a market order"""
    logger.info("CLI: market %s %s %s", symbol, side, quantity)
    resp = place_market_order(symbol, side, quantity)
    click.echo(resp)


@cli.command()
@click.option("--symbol", required=True)
@click.option("--side", required=True, type=click.Choice(["BUY", "SELL"], case_sensitive=False))
@click.option("--quantity", required=True, type=float)
@click.option("--price", required=True, type=float)
@click.option("--post-only", is_flag=True, default=False)
def limit(symbol, side, quantity, price, post_only):
    """Place a limit order"""
    logger.info("CLI: limit %s %s %s @ %s", symbol, side, quantity, price)
    resp = place_limit_order(symbol, side, quantity, price, post_only=post_only)
    click.echo(resp)

@cli.command()
@click.option("--symbol", required=True, help="Trading pair symbol, e.g. BTCUSDT")
@click.option("--side", required=True, type=click.Choice(["BUY", "SELL"], case_sensitive=False))
@click.option("--stop-price", type=float, required=True, help="Stop trigger price for stop-loss")
@click.option("--limit-price", type=float, required=True, help="Trigger price for take-profit")
@click.option("--quantity", type=float, required=True, help="Contract quantity")
def oco(symbol, side, stop_price, limit_price, quantity):
    """
    Place a simulated OCO (One-Cancels-the-Other) order in Futures.
    Creates both STOP_MARKET and TAKE_PROFIT_MARKET orders.
    """
    try:
        logger.info("CLI: oco %s %s %s %s %s", symbol, side, stop_price, limit_price, quantity)
        stop_resp, tp_resp = place_oco_order(
            symbol=symbol,
            side=side,
            stop_price=stop_price,
            limit_price=limit_price,
            quantity=quantity,
        )
        click.echo("STOP_MARKET order placed:\n{}".format(stop_resp))
        click.echo("TAKE_PROFIT_MARKET order placed:\n{}".format(tp_resp))
    except Exception as e:
        logger.exception("Error placing OCO order: %s", e)
        raise

@cli.command()
@click.option("--symbol", required=True)
@click.option("--side", required=True, type=click.Choice(["BUY", "SELL"], case_sensitive=False))
@click.option("--stop-price", type=float, required=True)
@click.option("--limit-price", type=float, required=True)
@click.option("--quantity", type=float, required=True)
def stoplimit(symbol, side, stop_price, limit_price, quantity):
    """Place a stop-limit order."""
    try:
        logger.info("CLI: stoplimit %s %s %s %s %s", symbol, side, stop_price, limit_price, quantity)
        resp = place_stop_limit_order(
            symbol=symbol,
            side=side,
            stop_price=stop_price,
            limit_price=limit_price,
            quantity=quantity,
        )
        click.echo(resp)
    except Exception as e:
        logger.exception("Error placing stop-limit order: %s", e)
        raise




if __name__ == "__main__":
    cli()
