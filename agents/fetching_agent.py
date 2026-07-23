import datetime
import logging
from typing import Dict, List, Any

from data.providers.market_data_provider import YFinanceMarketDataProvider
from data.cache import global_cache
from config.settings import (
    INDUSTRY_UNIVERSE,
    CACHE_TTL_HISTORICAL_SECONDS,
    CACHE_TTL_CURRENT_SECONDS
)

logger = logging.getLogger(__name__)

class FetchingSubAgent:
    """
    Sub-Agent 1: Fetching Sub-Agent
    Retrieves and caches market data required by the dashboard or chatbot.
    """

    def __init__(self):
        self.provider = YFinanceMarketDataProvider()

    def get_full_universe_tickers(self) -> List[str]:
        """Collect all unique ticker symbols from the configured industry universe."""
        tickers = set()
        for companies in INDUSTRY_UNIVERSE.values():
            for comp in companies:
                tickers.add(comp["symbol"])
        return sorted(list(tickers))

    def fetch_dashboard_dataset(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Fetch historical and snapshot market data for the entire universe.
        Implements L1/L2 caching and force_refresh invalidation for the Refresh button.
        """
        cache_key = "dashboard_universe_historical_6m"

        if force_refresh:
            logger.info("Force refresh requested. Invalidating cache...")
            global_cache.invalidate(cache_key)

        cached_data = global_cache.get(cache_key)
        if cached_data is not None:
            logger.info("Dashboard dataset loaded from cache.")
            return {
                "status": "success",
                "retrieved_at": cached_data["retrieved_at"],
                "source": "cache",
                "data": cached_data["data"],
                "warnings": []
            }

        logger.info("Fetching fresh dataset from market data provider...")
        tickers = self.get_full_universe_tickers()
        hist_prices = self.provider.fetch_historical_prices(tickers, days=180)

        retrieved_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        data_payload = {
            "tickers": tickers,
            "historical_prices": hist_prices,
            "count": len(hist_prices)
        }

        # Cache the result
        global_cache.set(
            cache_key,
            {"retrieved_at": retrieved_time, "data": data_payload},
            ttl_seconds=CACHE_TTL_HISTORICAL_SECONDS
        )

        return {
            "status": "success" if hist_prices else "partial_success",
            "retrieved_at": retrieved_time,
            "source": "yfinance_api",
            "data": data_payload,
            "warnings": [] if hist_prices else ["Some ticker data could not be retrieved."]
        }

    def fetch_specific_tickers(self, tickers: List[str], days: int = 180) -> Dict[str, Any]:
        """
        Fetch historical prices and current snapshots for user-requested tickers in chat.
        """
        tickers = [t.upper() for t in tickers]
        hist_prices = self.provider.fetch_historical_prices(tickers, days=days)
        snapshots = self.provider.fetch_current_snapshot(tickers)

        return {
            "status": "success" if hist_prices else "error",
            "retrieved_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "source": "yfinance_api",
            "data": {
                "historical_prices": hist_prices,
                "snapshots": snapshots
            },
            "warnings": []
        }
