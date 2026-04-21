"""MEXC balance data containers."""

from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.balances.balance import BalanceData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class MexcBalanceData(BalanceData):
    def __init__(
        self,
        balance_info: dict[str, Any] | str,
        symbol_name: str | None = None,
        asset_type: str | None = None,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(balance_info, has_been_json_encoded)
        self.exchange_name = "MEXC"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.balance_data: dict[str, Any] | None = (
            balance_info if has_been_json_encoded and isinstance(balance_info, dict) else None
        )
        self.asset: str | None = None
        self.free: float | None = None
        self.locked: float | None = None
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self) -> MexcBalanceData:
        if not self.has_been_json_encoded:
            if isinstance(self.balance_info, str):
                self.balance_data = json.loads(self.balance_info)
            else:
                self.balance_data = self.balance_info

        if self.balance_data:
            self.asset = from_dict_get_string(self.balance_data, "asset")
            self.free = from_dict_get_float(self.balance_data, "free", 0.0)
            self.locked = from_dict_get_float(self.balance_data, "locked", 0.0)

        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "asset": self.asset,
                "free": self.free,
                "locked": self.locked,
                "total": self.free + self.locked if self.free and self.locked else 0.0,
            }
        return self.all_data

    def __str__(self) -> str:
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_local_update_time(self) -> float:
        return self.local_update_time

    def get_symbol_name(self) -> str | None:
        return self.symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type if self.asset_type is not None else ""

    def get_asset(self) -> str | None:
        if not self.has_been_init_data:
            self.init_data()
        return self.asset

    def get_free(self) -> float | None:
        if not self.has_been_init_data:
            self.init_data()
        return self.free

    def get_locked(self) -> float | None:
        if not self.has_been_init_data:
            self.init_data()
        return self.locked

    def get_total(self) -> float:
        if not self.has_been_init_data:
            self.init_data()
        if self.free is not None and self.locked is not None:
            return self.free + self.locked
        return 0.0

    def get_available(self) -> float:
        if not self.has_been_init_data:
            self.init_data()
        return self.free if self.free is not None else 0.0

    def get_frozen(self) -> float:
        if not self.has_been_init_data:
            self.init_data()
        return self.locked if self.locked is not None else 0.0

    def is_zero(self) -> bool:
        return self.get_total() == 0.0

    def has_available(self) -> bool:
        return self.get_available() > 0.0

    def has_frozen(self) -> bool:
        return self.get_frozen() > 0.0


class MexcRequestBalanceData(MexcBalanceData):
    def __init__(
        self,
        balance_info: dict[str, Any] | str,
        symbol_name: str | None = None,
        asset_type: str | None = None,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(balance_info, symbol_name, asset_type, has_been_json_encoded)

    def init_data(self) -> MexcRequestBalanceData:
        super().init_data()
        return self


class MexcAccountData(BalanceData):
    def __init__(
        self,
        account_info: dict[str, Any] | str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(account_info, has_been_json_encoded)
        self.exchange_name = "MEXC"
        self.local_update_time = time.time()
        self.asset_type = asset_type
        self.account_data: dict[str, Any] | None = (
            account_info if has_been_json_encoded and isinstance(account_info, dict) else None
        )
        self.maker_commission: int | None = None
        self.taker_commission: int | None = None
        self.buyer_commission: int | None = None
        self.seller_commission: int | None = None
        self.can_trade: bool | None = None
        self.can_withdraw: bool | None = None
        self.can_deposit: bool | None = None
        self.account_type: str | None = None
        self.balances: list[MexcBalanceData] = []
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self) -> MexcAccountData:
        if self.has_been_init_data:
            return self

        if not self.has_been_json_encoded:
            if isinstance(self.account_info, str):
                self.account_data = json.loads(self.account_info)
            else:
                self.account_data = self.account_info
            self.has_been_json_encoded = True

        if self.account_data and isinstance(self.account_data, dict):
            self.maker_commission = int(
                from_dict_get_float(self.account_data, "makerCommission", 0)
            )
            self.taker_commission = int(
                from_dict_get_float(self.account_data, "takerCommission", 0)
            )
            self.buyer_commission = int(
                from_dict_get_float(self.account_data, "buyerCommission", 0)
            )
            self.seller_commission = int(
                from_dict_get_float(self.account_data, "sellerCommission", 0)
            )
            self.can_trade = self.account_data.get("canTrade", False)
            self.can_withdraw = self.account_data.get("canWithdraw", False)
            self.can_deposit = self.account_data.get("canDeposit", False)
            self.account_type = from_dict_get_string(self.account_data, "accountType")

            balances_data = self.account_data.get("balances", [])
            if isinstance(balances_data, list):
                for balance_dict in balances_data:
                    if isinstance(balance_dict, dict):
                        balance = MexcBalanceData(
                            balance_dict,
                            symbol_name=None,
                            asset_type=self.asset_type,
                            has_been_json_encoded=True,
                        )
                        balance.init_data()
                        self.balances.append(balance)

        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "maker_commission": self.maker_commission,
                "taker_commission": self.taker_commission,
                "buyer_commission": self.buyer_commission,
                "seller_commission": self.seller_commission,
                "can_trade": self.can_trade,
                "can_withdraw": self.can_withdraw,
                "can_deposit": self.can_deposit,
                "account_type": self.account_type,
                "balances": [b.get_all_data() for b in self.balances],
            }
        return self.all_data

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_local_update_time(self) -> float:
        return self.local_update_time

    def get_balances(self) -> list[MexcBalanceData]:
        self.init_data()
        return self.balances

    def get_balance_by_asset(self, asset: str) -> MexcBalanceData | None:
        self.init_data()
        for balance in self.balances:
            if balance.get_asset() == asset:
                return balance
        return None

    def get_total_balance_by_asset(self, asset: str) -> float:
        balance = self.get_balance_by_asset(asset)
        return balance.get_total() if balance else 0.0

    def get_maker_commission(self) -> int | None:
        self.init_data()
        return self.maker_commission

    def get_taker_commission(self) -> int | None:
        self.init_data()
        return self.taker_commission

    def get_buyer_commission(self) -> int | None:
        self.init_data()
        return self.buyer_commission

    def get_seller_commission(self) -> int | None:
        self.init_data()
        return self.seller_commission

    def get_can_trade(self) -> bool | None:
        self.init_data()
        return self.can_trade

    def get_can_withdraw(self) -> bool | None:
        self.init_data()
        return self.can_withdraw

    def get_can_deposit(self) -> bool | None:
        self.init_data()
        return self.can_deposit

    def get_account_type(self) -> str | None:
        self.init_data()
        return self.account_type

    def get_available_balance_by_asset(self, asset: str) -> float:
        balance = self.get_balance_by_asset(asset)
        return balance.get_available() if balance else 0.0

    def get_frozen_balance_by_asset(self, asset: str) -> float:
        balance = self.get_balance_by_asset(asset)
        return balance.get_frozen() if balance else 0.0
