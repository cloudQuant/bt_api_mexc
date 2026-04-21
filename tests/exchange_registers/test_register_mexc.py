"""Tests for exchange_registers/register_mexc.py."""

from __future__ import annotations

from bt_api_mexc.registry_registration import register_mexc


class TestRegisterMexc:
    """Tests for MEXC registration module."""

    def test_module_imports(self):
        """Test module can be imported."""
        assert register_mexc is not None
