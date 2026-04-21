"""MEXC trade data containers."""

from __future__ import annotations

import json
import time

from bt_api_base.containers.trades.trade import TradeData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_int, from_dict_get_string


class MexcTradeData(TradeData):
    def __init__(self, trade_info, symbol_name, asset_type, has_been_json_encoded=False):
        super().__init__(trade_info, has_been_json_encoded)
        self.exchange_name = "MEXC"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.trade_data = trade_info if has_been_json_encoded else None
        self.trade_id = None
        self.order_id = None
        self.price = None
        self.quantity = None
        self.quote_quantity = None
        self.commission = None
        self.commission_asset = None
        self.time = None
        self.is_buyer = None
        self.is_maker = None
        self.is_best_match = None
        self.all_data = None
        self.has_been_init_data = False

    def init_data(self):
        if not self.has_been_json_encoded:
            if isinstance(self.trade_info, str):
                self.trade_data = json.loads(self.trade_info)
            else:
                self.trade_data = self.trade_info

        if self.trade_data:
            self.trade_id = from_dict_get_int(self.trade_data, "id")
            self.order_id = from_dict_get_int(self.trade_data, "orderId")
            self.price = from_dict_get_float(self.trade_data, "price", 0.0)
            self.quantity = from_dict_get_float(self.trade_data, "qty", 0.0)
            self.quote_quantity = from_dict_get_float(self.trade_data, "quoteQty", 0.0)
            self.commission = from_dict_get_float(self.trade_data, "commission", 0.0)
            self.commission_asset = from_dict_get_string(self.trade_data, "commissionAsset")
            self.time = from_dict_get_int(self.trade_data, "time")
            self.is_buyer = self.trade_data.get("isBuyer", False)
            self.is_maker = self.trade_data.get("isMaker", False)
            self.is_best_match = self.trade_data.get("isBestMatch", False)

        self.has_been_init_data = True

    def get_all_data(self):
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "trade_id": self.trade_id,
                "order_id": self.order_id,
                "price": self.price,
                "quantity": self.quantity,
                "quote_quantity": self.quote_quantity,
                "commission": self.commission,
                "commission_asset": self.commission_asset,
                "time": self.time,
                "is_buyer": self.is_buyer,
                "is_maker": self.is_maker,
                "is_best_match": self.is_best_match,
            }
        return self.all_data

    def __str__(self):
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self):
        return self.__str__()

    def get_exchange_name(self):
        return self.exchange_name

    def get_local_update_time(self):
        return self.local_update_time

    def get_symbol_name(self):
        return self.symbol_name

    def get_asset_type(self):
        return self.asset_type

    def get_trade_id(self):
        return self.trade_id

    def get_price(self):
        return self.price

    def get_quantity(self):
        return self.quantity

    def get_time(self):
        return self.time

    def get_side(self):
        return "BUY" if self.is_buyer else "SELL"


class MexcWssTradeData(MexcTradeData):
    def init_data(self):
        if not self.has_been_json_encoded:
            self.trade_data = json.loads(self.trade_info)
            self.has_been_json_encoded = True

        if self.trade_data and "data" in self.trade_data:
            trade = self.trade_data["data"]
            self.trade_id = from_dict_get_int(trade, "t")
            self.price = from_dict_get_float(trade, "p", 0.0)
            self.quantity = from_dict_get_float(trade, "q", 0.0)
            self.is_buyer = trade.get("b", False)
            self.time = from_dict_get_int(self.trade_data, "E")

        self.has_been_init_data = True


class MexcRequestTradeData(MexcTradeData):
    def init_data(self):
        if not self.has_been_json_encoded:
            if isinstance(self.trade_info, str):
                self.trade_data = json.loads(self.trade_info)
            else:
                self.trade_data = self.trade_info

        if self.trade_data:
            self.trade_id = from_dict_get_int(self.trade_data, "id")
            self.order_id = from_dict_get_int(self.trade_data, "orderId")
            self.price = from_dict_get_float(self.trade_data, "price", 0.0)
            self.quantity = from_dict_get_float(self.trade_data, "qty", 0.0)
            self.quote_quantity = from_dict_get_float(self.trade_data, "quoteQty", 0.0)
            self.commission = from_dict_get_float(self.trade_data, "commission", 0.0)
            self.commission_asset = from_dict_get_string(self.trade_data, "commissionAsset")
            self.time = from_dict_get_int(self.trade_data, "time")
            self.is_buyer = self.trade_data.get("isBuyer", False)
            self.is_maker = self.trade_data.get("isMaker", False)
            self.is_best_match = self.trade_data.get("isBestMatch", False)

        self.has_been_init_data = True
