from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import pandas as pd

class BaseMarketDataProvider(ABC):
    """Abstract interface for market data providers."""

    @abstractmethod
    def fetch_historical_prices(self, tickers: List[str], days: int = 180) -> Dict[str, pd.DataFrame]:
        """
        Fetch historical OHLCV data for a list of tickers.
        Returns a dictionary mapping ticker to DataFrame with DatetimeIndex and Close columns.
        """
        pass

    @abstractmethod
    def fetch_current_snapshot(self, tickers: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Fetch latest market snapshot (price, change, prev_close, market_cap) for tickers.
        """
        pass

    @abstractmethod
    def fetch_company_metadata(self, ticker: str) -> Dict[str, Any]:
        """
        Fetch company metadata (Name, Sector, Industry, Summary, Market Cap).
        """
        pass
