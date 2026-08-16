"""MEXC ticker data containers."""

from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base._compat import Self
from bt_api_base.containers.tickers.ticker import TickerData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class MexcTickerData(TickerData):
    """Class MexcTickerData"""
    def __init__(self, ticker_info, symbol_name, asset_type, has_been_json_encoded=False) -> None:
        """__init__ method"""
        super().__init__(ticker_info, has_been_json_encoded)
        self.exchange_name = "MEXC"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.ticker_data: dict[str, Any] | None = (
            ticker_info if has_been_json_encoded and isinstance(ticker_info, dict) else None
        )
        self.ticker_symbol_name: str | None = None
        self.server_time: float | None = None
        self.bid_price: float | None = None
        self.ask_price: float | None = None
        self.bid_volume: float | None = None
        self.ask_volume: float | None = None
        self.last_price: float | None = None
        self.last_volume: float | None = None
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self) -> Self:
        """init_data method"""
        if not self.has_been_json_encoded:
            if isinstance(self.ticker_info, str):
                self.ticker_data = json.loads(self.ticker_info)
            else:
                self.ticker_data = self.ticker_info

        if self.ticker_data:
            td = self.ticker_data
            self.server_time = td.get("serverTime")
            self.bid_price = from_dict_get_float(td, "bidPrice", 0.0)
            self.ask_price = from_dict_get_float(td, "askPrice", 0.0)
            self.bid_volume = from_dict_get_float(td, "bidQty", 0.0)
            self.ask_volume = from_dict_get_float(td, "askQty", 0.0)
            self.last_price = from_dict_get_float(td, "lastPrice", 0.0)
            self.last_volume = from_dict_get_float(td, "lastQty", 0.0)
            self.ticker_symbol_name = from_dict_get_string(td, "symbol")

        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        """get_all_data method"""
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "ticker_symbol_name": self.ticker_symbol_name,
                "server_time": self.server_time,
                "bid_price": self.bid_price,
                "ask_price": self.ask_price,
                "bid_volume": self.bid_volume,
                "ask_volume": self.ask_volume,
                "last_price": self.last_price,
                "last_volume": self.last_volume,
            }
        return self.all_data or {}

    def __str__(self) -> str:
        self.init_data()
        return str(json.dumps(self.get_all_data()))

    def __repr__(self) -> str:
        return str(self.__str__())

    def get_exchange_name(self) -> str:
        """get_exchange_name method"""
        return str(self.exchange_name)

    def get_local_update_time(self) -> float:
        """get_local_update_time method"""
        return float(self.local_update_time)

    def get_symbol_name(self) -> str:
        """get_symbol_name method"""
        return str(self.symbol_name)

    def get_asset_type(self) -> str:
        """get_asset_type method"""
        return str(self.asset_type)

    def get_server_time(self) -> float | None:
        """get_server_time method"""
        if not self.has_been_init_data:
            self.init_data()
        return self.server_time

    def get_bid_price(self) -> float | None:
        """get_bid_price method"""
        if not self.has_been_init_data:
            self.init_data()
        return self.bid_price

    def get_ask_price(self) -> float | None:
        """get_ask_price method"""
        if not self.has_been_init_data:
            self.init_data()
        return self.ask_price

    def get_last_price(self) -> float | None:
        """get_last_price method"""
        if not self.has_been_init_data:
            self.init_data()
        return self.last_price

    def get_last_volume(self) -> float | None:
        """get_last_volume method"""
        if not self.has_been_init_data:
            self.init_data()
        return self.last_volume

    def get_bid_volume(self) -> float | None:
        """get_bid_volume method"""
        if not self.has_been_init_data:
            self.init_data()
        return self.bid_volume

    def get_ask_volume(self) -> float | None:
        """get_ask_volume method"""
        if not self.has_been_init_data:
            self.init_data()
        return self.ask_volume

    def get_ticker_symbol_name(self) -> str | None:
        """get_ticker_symbol_name method"""
        if not self.has_been_init_data:
            self.init_data()
        return self.ticker_symbol_name


class MexcWssTickerData(MexcTickerData):
    """Class MexcWssTickerData"""
    def init_data(self) -> Self:
        """init_data method"""
        if not self.has_been_json_encoded:
            self.ticker_data = json.loads(self.ticker_info)
            self.has_been_json_encoded = True

        if self.ticker_data and "data" in self.ticker_data:
            ticker = self.ticker_data["data"]
            self.server_time = self.ticker_data.get("ts")
            self.bid_price = from_dict_get_float(ticker, "buy", 0.0)
            self.ask_price = from_dict_get_float(ticker, "sell", 0.0)
            self.last_price = from_dict_get_float(ticker, "last", 0.0)
            self.ticker_symbol_name = from_dict_get_string(ticker, "symbol")

        self.has_been_init_data = True
        return self


class MexcRequestTickerData(MexcTickerData):
    """Class MexcRequestTickerData"""
    def init_data(self) -> Self:
        """init_data method"""
        if not self.has_been_json_encoded:
            if isinstance(self.ticker_info, str):
                self.ticker_data = json.loads(self.ticker_info)
            else:
                self.ticker_data = self.ticker_info

        if self.ticker_data:
            self.server_time = self.ticker_data.get("closeTime")
            self.last_price = from_dict_get_float(self.ticker_data, "lastPrice", 0.0)
            self.last_volume = from_dict_get_float(self.ticker_data, "lastQty", 0.0)
            self.bid_price = from_dict_get_float(self.ticker_data, "bidPrice", 0.0)
            self.ask_price = from_dict_get_float(self.ticker_data, "askPrice", 0.0)
            self.bid_volume = from_dict_get_float(self.ticker_data, "bidQty", 0.0)
            self.ask_volume = from_dict_get_float(self.ticker_data, "askQty", 0.0)
            self.ticker_symbol_name = from_dict_get_string(self.ticker_data, "symbol")

        self.has_been_init_data = True
        return self
