"""MEXC exchange registration on an explicitly supplied registry."""

from __future__ import annotations

from typing import TYPE_CHECKING

from bt_api_base.balance_utils import simple_balance_handler as _mexc_balance_handler

from bt_api_mexc.exchange_data import MexcExchangeDataSpot
from bt_api_mexc.feeds.live_mexc import MexcRequestDataSpot

if TYPE_CHECKING:
    from bt_api_base.registry import ExchangeRegistry


def register_mexc(registry: ExchangeRegistry) -> None:
    """Register MEXC Spot on the loader's isolated registry."""
    registry.register_feed("MEXC___SPOT", MexcRequestDataSpot)
    registry.register_exchange_data("MEXC___SPOT", MexcExchangeDataSpot)
    registry.register_balance_handler("MEXC___SPOT", _mexc_balance_handler)
