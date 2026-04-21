"""MEXC orderbook data containers."""

from __future__ import annotations

import json
import time

from bt_api_base.containers.orderbooks.orderbook import OrderBookData


class MexcOrderBookData(OrderBookData):
    def __init__(self, orderbook_info, symbol_name, asset_type, has_been_json_encoded=False):
        super().__init__(orderbook_info, has_been_json_encoded)
        self.exchange_name = "MEXC"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.orderbook_data = orderbook_info if has_been_json_encoded else None
        self.bids = []
        self.asks = []
        self.timestamp = None
        self.all_data = None
        self.has_been_init_data = False

    def init_data(self):
        if not self.has_been_json_encoded:
            if isinstance(self.order_book_info, str):
                self.orderbook_data = json.loads(self.order_book_info)
            else:
                self.orderbook_data = self.order_book_info

        if self.orderbook_data:
            self.timestamp = self.orderbook_data.get("time")

            self.bids = []
            for bid in self.orderbook_data.get("bids", []):
                if len(bid) >= 2:
                    price = float(bid[0])
                    quantity = float(bid[1])
                    self.bids.append([price, quantity])

            self.asks = []
            for ask in self.orderbook_data.get("asks", []):
                if len(ask) >= 2:
                    price = float(ask[0])
                    quantity = float(ask[1])
                    self.asks.append([price, quantity])

        self.has_been_init_data = True
        return self

    def get_all_data(self):
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "timestamp": self.timestamp,
                "bids": self.bids,
                "asks": self.asks,
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

    def get_timestamp(self):
        if not self.has_been_init_data:
            self.init_data()
        return self.timestamp

    def get_bids(self):
        if not self.has_been_init_data:
            self.init_data()
        return self.bids

    def get_asks(self):
        if not self.has_been_init_data:
            self.init_data()
        return self.asks

    def get_best_bid(self):
        if not self.has_been_init_data:
            self.init_data()
        return self.bids[0][0] if self.bids else None

    def get_best_ask(self):
        if not self.has_been_init_data:
            self.init_data()
        return self.asks[0][0] if self.asks else None


class MexcWssOrderBookData(MexcOrderBookData):
    def init_data(self):
        if not self.has_been_json_encoded:
            self.orderbook_data = json.loads(self.order_book_info)
            self.has_been_json_encoded = True

        if self.orderbook_data and "data" in self.orderbook_data:
            pass

        self.has_been_init_data = True
        return self


class MexcRequestOrderBookData(MexcOrderBookData):
    def init_data(self):
        if not self.has_been_json_encoded:
            if isinstance(self.order_book_info, str):
                self.orderbook_data = json.loads(self.order_book_info)
            else:
                self.orderbook_data = self.order_book_info

        if self.orderbook_data:
            self.timestamp = self.orderbook_data.get("time")

            self.bids = []
            for bid in self.orderbook_data.get("bids", []):
                if len(bid) >= 2:
                    price = float(bid[0])
                    quantity = float(bid[1])
                    self.bids.append([price, quantity])

            self.asks = []
            for ask in self.orderbook_data.get("asks", []):
                if len(ask) >= 2:
                    price = float(ask[0])
                    quantity = float(ask[1])
                    self.asks.append([price, quantity])

        self.has_been_init_data = True
        return self
