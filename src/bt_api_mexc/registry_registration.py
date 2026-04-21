"""MEXC exchange auto-registration."""

try:
    from bt_api_base.balance_utils import simple_balance_handler as _mexc_balance_handler
except ImportError:
    _mexc_balance_handler = None

try:
    from bt_api_base.registry import ExchangeRegistry
except ImportError:
    ExchangeRegistry = None  # type: ignore

from bt_api_mexc.exchange_data import MexcExchangeDataSpot
from bt_api_mexc.feeds.live_mexc import MexcRequestDataSpot


def register_mexc():
    if ExchangeRegistry is None:
        return
    ExchangeRegistry.register_feed("MEXC___SPOT", MexcRequestDataSpot)
    ExchangeRegistry.register_exchange_data("MEXC___SPOT", MexcExchangeDataSpot)
    if _mexc_balance_handler is not None:
        ExchangeRegistry.register_balance_handler("MEXC___SPOT", _mexc_balance_handler)


register_mexc()
