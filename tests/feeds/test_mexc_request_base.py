from unittest.mock import AsyncMock, MagicMock
import pytest
from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_mexc.feeds.live_mexc.request_base import MexcRequestData


def test_mexc_defaults_exchange_name_for_http_client() -> None:
    request_data = MexcRequestData(public_key="public-key", private_key="secret-key")

    assert request_data.exchange_name == "MEXC___SPOT"
    assert request_data._http_client._venue == "MEXC___SPOT"


def test_mexc_disconnect_closes_http_client() -> None:
    request_data = MexcRequestData(public_key="public-key", private_key="secret-key")
    request_data._http_client.close = MagicMock()

    request_data.disconnect()

    request_data._http_client.close.assert_called_once_with()


async def test_mexc_async_request_allows_missing_extra_data(monkeypatch) -> None:
    request_data = MexcRequestData(
        public_key="public-key",
        private_key="secret-key",
        exchange_name="MEXC___SPOT",
    )

    async_request_mock = AsyncMock(return_value={"code": 0, "data": []})
    monkeypatch.setattr(request_data._http_client, "async_request", async_request_mock)

    result = await request_data.async_request("GET /api/v3/time", is_sign=False)

    assert isinstance(result, RequestData)
    assert result.get_extra_data() == {}
    assert result.get_input_data() == {"code": 0, "data": []}


def test_mexc_accepts_api_key_and_api_secret_aliases() -> None:
    request_data = MexcRequestData(api_key="public-key", api_secret="secret-key")

    assert request_data.public_key == "public-key"
    assert request_data.private_key == "secret-key"
