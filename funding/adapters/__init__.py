from .binance import BinanceAdapter
from .bybit import BybitAdapter
from .okx import OkxAdapter

ADAPTERS = {"binance": BinanceAdapter, "bybit": BybitAdapter, "okx": OkxAdapter}


def make_adapter(name, exchange=None):
    return ADAPTERS[name](exchange=exchange)
