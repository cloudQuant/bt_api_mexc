# bt_api_mexc

MEXC exchange package for `bt_api`, supporting Spot and USDT-M Perpetual trading.

## Features

- **Spot Trading**: Full REST API support for account, orders, market data
- **USDT-M Swap**: REST API for perpetual futures trading
- **HMAC SHA256 Authentication**: Secure API key handling
- **Hardcoded Configuration**: No YAML dependency — all exchange paths are defined in code

## Installation

```bash
pip install bt_api_mexc
```

Or install from source:

```bash
cd packages/bt_api_mexc
pip install -e .
```

## Quick Usage

```python
from bt_api_py import BtApi

api = BtApi(
    exchange_kwargs={
        "MEXC___SPOT": {
            "api_key": "your_api_key",
            "secret_key": "your_secret",
        }
    }
)

# Query ticker
ticker = api.get_tick("MEXC___SPOT", "BTCUSDT")
print(ticker)

# Place order
order = api.make_order(
    exchange_name="MEXC___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=50000,
    order_type="buy-limit",
)
print(order)
```

## Architecture

```
bt_api_mexc/
├── __init__.py
├── exchange_data/
│   └── __init__.py          # MexcExchangeData, MexcExchangeDataSpot, MexcExchangeDataSwap
├── errors/
│   ├── __init__.py          # MexcErrorTranslator (re-export)
│   └── mexc_translator.py   # Error code mapping extending ErrorTranslator
├── containers/
│   ├── __init__.py
│   ├── balances/
│   │   ├── __init__.py
│   │   └── mexc_balance.py  # MexcBalanceData, MexcRequestBalanceData
│   ├── orders/
│   │   ├── __init__.py
│   │   └── mexc_order.py    # MexcOrderData, MexcWssOrderData, MexcRequestOrderData
│   ├── tickers/
│   │   ├── __init__.py
│   │   └── mexc_ticker.py   # MexcTickerData, MexcWssTickerData, MexcRequestTickerData
│   ├── orderbooks/
│   │   ├── __init__.py
│   │   └── mexc_orderbook.py # MexcOrderBookData, MexcWssOrderBookData, MexcRequestOrderBookData
│   └── trades/
│       ├── __init__.py
│       └── mexc_trade.py    # MexcTradeData, MexcWssTradeData, MexcRequestTradeData
├── feeds/
│   └── live_mexc/
│       ├── __init__.py
│       ├── request_base.py  # MexcRequestData (HMAC auth base)
│       └── spot.py          # MexcRequestDataSpot
├── registry_registration.py  # Auto-registers with ExchangeRegistry
└── plugin.py                  # Plugin entrypoint for unified loading
```

## Dependencies

- `bt_api_base>=0.15,<1.0`
- Python 3.9+

## Supported Endpoints

### Spot

| Method | Description |
|--------|-------------|
| `get_ticker` / `get_tick` | Query ticker data |
| `get_depth` / `get_orderbook` | Order book depth |
| `get_kline` / `get_klines` | K-line/candlestick data |
| `get_server_time` | Server time |
| `get_exchange_info` / `get_symbols` | Exchange symbols |
| `get_balance` | Account balances |
| `get_account` | Account info |
| `make_order` | Place order |
| `cancel_order` | Cancel order |
| `query_order` | Query order status |
| `get_open_orders` | Get open orders |
| `get_deals` | Recent trades |

### Swap (USDT-M)

Same as Spot with swap-specific endpoints.

## WebSocket

WebSocket classes are placeholder stubs. Full WebSocket implementation is pending.

## Error Codes

`MexcErrorTranslator` maps MEXC API error messages to unified `UnifiedErrorCode` values from `bt_api_base.error`.
