"""MEXC exchange data configuration - hardcoded defaults, no YAML."""

from __future__ import annotations

from typing import Any

from bt_api_base.containers.exchanges.exchange_data import ExchangeData


class MexcExchangeData(ExchangeData):
    """Base class for all MEXC exchange types."""

    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "mexc"
        self.rest_url = ""
        self.acct_wss_url = ""
        self.wss_url = ""
        self.rest_paths: dict[str, str] = {}
        self.wss_paths: dict[str, Any] = {}

        self.kline_periods = {
            "1s": "1s",
            "1m": "1m",
            "3m": "3m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "1h",
            "2h": "2h",
            "4h": "4h",
            "6h": "6h",
            "8h": "8h",
            "12h": "12h",
            "1d": "1d",
            "3d": "3d",
            "1w": "1w",
            "1M": "1M",
        }
        self.reverse_kline_periods = {v: k for k, v in self.kline_periods.items()}

        self.legal_currency = [
            "USDT",
            "USD",
            "BTC",
            "ETH",
        ]

    # noinspection PyMethodMayBeStatic
    def get_symbol(self, symbol: str) -> str:
        return symbol.replace("-", "").replace("/", "")

    def account_wss_symbol(self, symbol: str) -> str:
        for lc in self.legal_currency:
            if lc in symbol:
                symbol = f"{symbol.split(lc)[0]}/{lc}".lower()
                break
        return symbol

    # noinspection PyMethodMayBeStatic
    def get_period(self, key: str) -> str:
        if key in self.kline_periods:
            return self.kline_periods[key]
        return key

    def get_rest_path(self, key: str, **kwargs: Any) -> str:
        if key not in self.rest_paths or self.rest_paths[key] == "":
            raise ValueError(f"REST path not found for key: {key} on exchange {self.exchange_name}")
        return str(self.rest_paths[key])

    def get_wss_path(self, **kwargs) -> str:
        """Get WSS subscription path for given topic."""
        import json

        key = kwargs.get("topic", "")
        if "symbol" in kwargs:
            kwargs["symbol"] = self.get_symbol(kwargs["symbol"])
        if "pair" in kwargs:
            kwargs["pair"] = self.get_symbol(kwargs["pair"])
        if "period" in kwargs:
            kwargs["period"] = self.get_period(kwargs["period"])

        if key not in self.wss_paths or self.wss_paths[key] == "":
            raise ValueError(f"WSS path not found for key: {key} on exchange {self.exchange_name}")
        req = self.wss_paths[key].copy()
        req_key = list(req.keys())[0]
        for k, v in kwargs.items():
            if isinstance(v, str):
                req[req_key] = [req[req_key][0].replace(f"<{k}>", v.lower())]
        new_value = []
        if "symbol_list" in kwargs:
            for symbol in kwargs["symbol_list"]:
                value = req[req_key]
                new_value.append(value[0].replace("<symbol>", self.get_symbol(symbol).lower()))
            req[req_key] = new_value
        return json.dumps(req)


class MexcExchangeDataSpot(MexcExchangeData):
    """MEXC Spot Trading Data Configuration."""

    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "SPOT"
        self.exchange_name = "MEXC___SPOT"
        self.rest_url = "https://api.mexc.com"
        self.wss_url = "wss://wbs.mexc.com/ws"
        self.acct_wss_url = "wss://wbs.mexc.com/ws"

        # REST API paths
        self.rest_paths = {
            # General
            "ping": "GET /api/v3/ping",
            "get_server_time": "GET /api/v3/time",
            "get_contract": "GET /api/v3/exchangeInfo",
            "get_exchange_info": "GET /api/v3/exchangeInfo",
            # Market Data
            "get_tick": "GET /api/v3/ticker/bookTicker",
            "get_depth": "GET /api/v3/depth",
            "get_order_book": "GET /api/v3/depth",
            "get_incre_depth": "GET /api/v1/depth",
            "get_kline": "GET /api/v3/klines",
            "get_klines": "GET /api/v3/klines",
            "get_avg_price": "GET /api/v3/avgPrice",
            "get_info": "GET /api/v3/ticker/24hr",
            "get_24hr_ticker": "GET /api/v3/ticker/24hr",
            "get_market": "GET /api/v3/ticker/price",
            "get_ticker": "GET /api/v3/ticker",
            "get_new_price": "GET /api/v3/trades",
            "get_recent_trades": "GET /api/v3/trades",
            "get_historical_trades": "GET /api/v3/historicalTrades",
            "get_agg_trades": "GET /api/v3/aggTrades",
            # Account
            "get_account": "GET /api/v3/account",
            "get_balance": "GET /api/v3/account",
            "get_fee": "GET /sapi/v1/asset/tradeFee",
            "get_commission": "GET /api/v3/account/commission",
            "get_order_rate_limit": "GET /api/v3/rateLimit/order",
            # Trade
            "make_order": "POST /api/v3/order",
            "make_order_test": "POST /api/v3/order/test",
            "cancel_order": "DELETE /api/v3/order",
            "cancel_all": "DELETE /api/v3/openOrders",
            "cancel_replace_order": "POST /api/v3/order/cancelReplace",
            "amend_keep_priority": "PUT /api/v3/order/amend/keepPriority",
            "query_order": "GET /api/v3/order",
            "get_order": "GET /api/v3/order",
            "get_open_orders": "GET /api/v3/openOrders",
            "get_all_orders": "GET /api/v3/allOrders",
            "get_deals": "GET /api/v3/myTrades",
            # OCO / OTO / OTOCO
            "make_oco_order": "POST /api/v3/order/oco",
            "get_order_list": "GET /api/v3/orderList",
            "get_all_order_lists": "GET /api/v3/allOrderList",
            "get_open_order_lists": "GET /api/v3/openOrderList",
            "cancel_order_list": "DELETE /api/v3/orderList",
            # Listen Key
            "get_listen_key": "POST /sapi/v1/userListenToken",
            "refresh_listen_key": "POST /sapi/v1/userListenToken",
        }

        # WebSocket paths
        self.wss_paths = {
            # Market Streams
            "agg_trade": {"params": ["<symbol>@aggTrade"], "method": "SUBSCRIBE", "id": 1},
            "trade": {"params": ["<symbol>@trade"], "method": "SUBSCRIBE", "id": 1},
            "kline": {"params": ["<symbol>@kline_<period>"], "method": "SUBSCRIBE", "id": 1},
            "mini_ticker": {"params": ["<symbol>@miniTicker"], "method": "SUBSCRIBE", "id": 1},
            "ticker": {"params": ["<symbol>@ticker"], "method": "SUBSCRIBE", "id": 1},
            "ticker_window": {
                "params": ["<symbol>@ticker_<window>"],
                "method": "SUBSCRIBE",
                "id": 1,
            },
            "book_ticker": {"params": ["<symbol>@bookTicker"], "method": "SUBSCRIBE", "id": 1},
            "avg_price": {"params": ["<symbol>@avgPrice"], "method": "SUBSCRIBE", "id": 1},
            "depth": {"params": ["<symbol>@depth20@100ms"], "method": "SUBSCRIBE", "id": 1},
            "depth_partial": {
                "params": ["<symbol>@depth<level>@100ms"],
                "method": "SUBSCRIBE",
                "id": 1,
            },
            "increDepthFlow": {"params": ["<symbol>@depth@100ms"], "method": "SUBSCRIBE", "id": 1},
            "force_order": {"params": ["<symbol>@forceOrder"], "method": "SUBSCRIBE", "id": 1},
            "kline_timezone": {
                "params": ["<symbol>@kline_<period>@+08:00"],
                "method": "SUBSCRIBE",
                "id": 1,
            },
            # All Market Streams
            "all_mini_ticker": {"params": ["!miniTicker@arr"], "method": "SUBSCRIBE", "id": 1},
            "all_ticker": {"params": ["!ticker@arr"], "method": "SUBSCRIBE", "id": 1},
            "all_ticker_window": {
                "params": ["!ticker_<window>@arr"],
                "method": "SUBSCRIBE",
                "id": 1,
            },
            "all_book_ticker": {"params": ["!bookTicker"], "method": "SUBSCRIBE", "id": 1},
            # Aliases
            "tick": {"params": ["<symbol>@bookTicker"], "method": "SUBSCRIBE", "id": 1},
            "tick_all": {"params": ["!bookTicker"], "method": "SUBSCRIBE", "id": 1},
            "ticks": {"params": ["!ticker@arr"], "method": "SUBSCRIBE", "id": 1},
            "market": {"params": ["!bookTicker"], "method": "SUBSCRIBE", "id": 1},
            "bidAsk": {"params": ["<symbol>@bookTicker"], "method": "SUBSCRIBE", "id": 1},
            "liquidation": {"params": ["<symbol>@forceOrder"], "method": "SUBSCRIBE", "id": 1},
            "liquidation_order": {
                "params": ["<symbol>@forceOrder"],
                "method": "SUBSCRIBE",
                "id": 1,
            },
            # User Data Streams
            "orders": {"params": [""], "method": "SUBSCRIBE", "id": 1},
            "deals": {"params": [""], "method": "SUBSCRIBE", "id": 1},
            "balance": {"params": [""], "method": "SUBSCRIBE", "id": 1},
            "position": {"params": [""], "method": "SUBSCRIBE", "id": 1},
        }


class MexcExchangeDataSwap(MexcExchangeData):
    """MEXC USDT-M Futures (swap) Data Configuration."""

    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "MEXC___SWAP"
        self.asset_type = "SWAP"
        self.rest_url = "https://api.mexc.com"
        self.wss_url = "wss://wbs.mexc.com/ws"
        self.acct_wss_url = "wss://wbs.mexc.com/ws"

        # REST API paths
        self.rest_paths = {
            # General
            "ping": "GET /api/v1/ping",
            "get_server_time": "GET /api/v1/time",
            "get_contract": "GET /api/v1/exchangeInfo",
            # Market Data
            "get_tick": "GET /api/v1/ticker/bookTicker",
            "get_info": "GET /api/v1/ticker/24hr",
            "get_new_price": "GET /api/v1/trades",
            "get_historical_trades": "GET /api/v1/historicalTrades",
            "get_depth": "GET /api/v1/depth",
            "get_incre_depth": "GET /api/v1/depth",
            "get_kline": "GET /api/v1/klines",
            "get_agg_trades": "GET /api/v1/aggTrades",
            "get_funding_rate": "GET /api/v1/premiumIndex",
            "get_clear_price": "GET /api/v1/premiumIndex",
            "get_mark_price": "GET /api/v1/premiumIndex",
            "get_history_funding_rate": "GET /api/v1/fundingRate",
            "get_market_rate": "GET /api/v1/premiumIndex",
            "get_funding_info": "GET /api/v1/fundingInfo",
            "get_continuous_kline": "GET /api/v1/continuousKlines",
            "get_index_price_kline": "GET /api/v1/indexPriceKlines",
            "get_mark_price_kline": "GET /api/v1/markPriceKlines",
            "get_price_ticker": "GET /api/v2/ticker/price",
            "get_avg_price": "GET /api/v1/avgPrice",
            "get_ticker": "GET /api/v1/ticker",
            "get_open_interest": "GET /api/v1/openInterest",
            "get_delivery_price": "GET /api/v1/deliveryPrice",
            "get_long_short_ratio": "GET /futures/data/globalLongShortAccountRatio",
            "get_top_long_short_account_ratio": "GET /futures/data/topLongShortAccountRatio",
            "get_top_long_short_position_ratio": "GET /futures/data/topLongShortPositionRatio",
            "get_taker_buy_sell_volume": "GET /futures/data/takerlongshortRatio",
            "get_open_interest_hist": "GET /futures/data/openInterestHist",
            "get_index_constituents": "GET /api/v1/constituents",
            # Account
            "get_account": "GET /api/v2/account",
            "get_balance": "GET /api/v2/balance",
            "get_position": "GET /api/v2/positionRisk",
            "get_fee": "GET /api/v1/commissionRate",
            "get_income": "GET /api/v1/income",
            "get_adl_quantile": "GET /api/v1/adlQuantile",
            "get_leverage_bracket": "GET /api/v1/leverageBracket",
            "get_position_mode": "GET /api/v1/positionSide/dual",
            "get_multi_assets_mode": "GET /api/v1/multiAssetsMargin",
            "get_api_trading_status": "GET /api/v1/apiTradingStatus",
            "get_api_key_permission": "GET /api/v1/apiKeyPermission",
            "get_order_rate_limit": "GET /api/v1/rateLimit/order",
            "get_force_orders": "GET /api/v1/forceOrders",
            "get_symbol_config": "GET /api/v1/symbolConfig",
            "get_account_config": "GET /api/v1/accountConfig",
            # Trade
            "make_order": "POST /api/v1/order",
            "make_order_test": "POST /api/v1/order/test",
            "make_orders": "POST /api/v1/batchOrders",
            "modify_order": "PUT /api/v1/order",
            "modify_orders": "PUT /api/v1/batchOrders",
            "cancel_order": "DELETE /api/v1/order",
            "cancel_orders": "DELETE /api/v1/batchOrders",
            "cancel_all": "DELETE /api/v1/allOpenOrders",
            "auto_cancel_all": "POST /api/v1/countdownCancelAll",
            "query_order": "GET /api/v1/order",
            "get_open_orders": "GET /api/v1/openOrders",
            "get_all_orders": "GET /api/v1/allOrders",
            "get_deals": "GET /api/v1/userTrades",
            "change_leverage": "POST /api/v1/leverage",
            "change_margin_type": "POST /api/v1/marginType",
            "change_position_mode": "POST /api/v1/positionSide/dual",
            "change_multi_assets_mode": "POST /api/v1/multiAssetsMargin",
            "modify_isolated_position_margin": "POST /api/v1/positionMargin",
            "get_position_margin_history": "GET /api/v1/positionMargin/history",
            # OCO
            "make_oco_order": "POST /api/v1/order/oco",
            "get_order_list": "GET /api/v1/orderList",
            "get_all_order_lists": "GET /api/v1/allOrderList",
            "get_open_order_lists": "GET /api/v1/openOrderList",
            "cancel_order_list": "DELETE /api/v1/orderList",
            # Listen Key
            "get_listen_key": "POST /api/v1/listenKey",
            "refresh_listen_key": "PUT /api/v1/listenKey",
            "close_listen_key": "DELETE /api/v1/listenKey",
        }

        # WebSocket paths
        self.wss_paths = {
            # Market Streams
            "agg_trade": {"params": ["<symbol>@aggTrade"], "method": "SUBSCRIBE", "id": 1},
            "trade": {"params": ["<symbol>@trade"], "method": "SUBSCRIBE", "id": 1},
            "kline": {"params": ["<symbol>@kline_<period>"], "method": "SUBSCRIBE", "id": 1},
            "continuous_kline": {
                "params": ["<pair>_perpetual@continuousKline_<period>"],
                "method": "SUBSCRIBE",
                "id": 1,
            },
            "mini_ticker": {"params": ["<symbol>@miniTicker"], "method": "SUBSCRIBE", "id": 1},
            "ticker": {"params": ["<symbol>@ticker"], "method": "SUBSCRIBE", "id": 1},
            "ticker_window": {
                "params": ["<symbol>@ticker_<window>"],
                "method": "SUBSCRIBE",
                "id": 1,
            },
            "book_ticker": {"params": ["<symbol>@bookTicker"], "method": "SUBSCRIBE", "id": 1},
            "depth": {"params": ["<symbol>@depth20@100ms"], "method": "SUBSCRIBE", "id": 1},
            "depth500": {"params": ["<symbol>@depth5@500ms"], "method": "SUBSCRIBE", "id": 1},
            "depth_partial": {
                "params": ["<symbol>@depth<level>@100ms"],
                "method": "SUBSCRIBE",
                "id": 1,
            },
            "increDepthFlow": {"params": ["<symbol>@depth@100ms"], "method": "SUBSCRIBE", "id": 1},
            "mark_price": {"params": ["<symbol>@markPrice@1s"], "method": "SUBSCRIBE", "id": 1},
            "funding_rate": {"params": ["<symbol>@markPrice@1s"], "method": "SUBSCRIBE", "id": 1},
            "force_order": {"params": ["<symbol>@forceOrder"], "method": "SUBSCRIBE", "id": 1},
            # All Market Streams
            "all_force_order": {"params": ["!forceOrder@arr"], "method": "SUBSCRIBE", "id": 1},
            "all_mini_ticker": {"params": ["!miniTicker@arr"], "method": "SUBSCRIBE", "id": 1},
            "all_ticker": {"params": ["!ticker@arr"], "method": "SUBSCRIBE", "id": 1},
            "all_ticker_window": {
                "params": ["!ticker_<window>@arr"],
                "method": "SUBSCRIBE",
                "id": 1,
            },
            "all_mark_price": {"params": ["!markPrice@arr@1s"], "method": "SUBSCRIBE", "id": 1},
            "all_book_ticker": {"params": ["!bookTicker"], "method": "SUBSCRIBE", "id": 1},
            # Aliases
            "tick": {"params": ["<symbol>@bookTicker"], "method": "SUBSCRIBE", "id": 1},
            "tick_all": {"params": ["!bookTicker"], "method": "SUBSCRIBE", "id": 1},
            "ticks": {"params": ["!ticker@arr"], "method": "SUBSCRIBE", "id": 1},
            "tickers": {"params": ["!ticker@arr"], "method": "SUBSCRIBE", "id": 1},
            "market": {"params": ["!bookTicker"], "method": "SUBSCRIBE", "id": 1},
            "bidAsk": {"params": ["<symbol>@bookTicker"], "method": "SUBSCRIBE", "id": 1},
            "clearPrice": {"params": ["<symbol>@markPrice@1s"], "method": "SUBSCRIBE", "id": 1},
            "liquidation": {"params": ["<symbol>@forceOrder"], "method": "SUBSCRIBE", "id": 1},
            "liquidation_order": {
                "params": ["<symbol>@forceOrder"],
                "method": "SUBSCRIBE",
                "id": 1,
            },
            "contract_info": {"params": ["!contractInfo"], "method": "SUBSCRIBE", "id": 1},
            # User Data Streams
            "listen_key": {"params": [""], "method": "SUBSCRIBE", "id": 1},
            "orders": {"params": [""], "method": "SUBSCRIBE", "id": 1},
            "deals": {"params": [""], "method": "SUBSCRIBE", "id": 1},
            "balance": {"params": [""], "method": "SUBSCRIBE", "id": 1},
            "position": {"params": [""], "method": "SUBSCRIBE", "id": 1},
            "account": {"params": [""], "method": "SUBSCRIBE", "id": 1},
            "portfolio": {"params": [""], "method": "SUBSCRIBE", "id": 1},
        }
