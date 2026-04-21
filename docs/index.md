# MEXC Documentation

## English

Welcome to the MEXC documentation for bt_api.

### Quick Start

```bash
pip install bt_api_mexc
```

```python
from bt_api_mexc import MexcApi
feed = MexcApi(api_key="your_key", secret="your_secret")
ticker = feed.get_ticker("BTCUSDT")
```

## 中文

欢迎使用 bt_api 的 MEXC 文档。

### 快速开始

```bash
pip install bt_api_mexc
```

```python
from bt_api_mexc import MexcApi
feed = MexcApi(api_key="your_key", secret="your_secret")
ticker = feed.get_ticker("BTCUSDT")
```

## API Reference

See source code in `src/bt_api_mexc/` for detailed API documentation.
