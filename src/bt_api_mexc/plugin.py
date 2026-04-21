try:
    from bt_api_base.plugins.protocol import PluginInfo, PluginMetadata, PluginVersion
except ImportError:
    PluginInfo = None  # type: ignore
    PluginMetadata = None  # type: ignore
    PluginVersion = None  # type: ignore

from bt_api_mexc.exchange_data import MexcExchangeDataSpot
from bt_api_mexc.feeds.live_mexc import MexcRequestDataSpot


def _get_mexc_metadata():
    if PluginMetadata is None:
        return None
    return PluginMetadata(
        name="MEXC Exchange Plugin",
        version=PluginVersion(major=0, minor=1, patch=0),
        description="MEXC Spot trading support for bt_api_py",
        supported_exchanges=["MEXC___SPOT"],
        dependencies=["bt_api_base>=0.15,<1.0"],
    )


MEXC_PLUGIN_INFO = (
    PluginInfo(
        name="mexc",
        metadata=_get_mexc_metadata(),
        feed_class=MexcRequestDataSpot,
        exchange_data_class=MexcExchangeDataSpot,
    )
    if PluginInfo is not None
    else None
)
