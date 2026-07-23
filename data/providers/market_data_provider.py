import logging
from typing import Dict, List, Any
import datetime
import pandas as pd
import yfinance as yf

from data.providers.base import BaseMarketDataProvider
from config.settings import SYMBOL_LOOKUP

logger = logging.getLogger(__name__)

class YFinanceMarketDataProvider(BaseMarketDataProvider):
    """
    Market Data Provider implemented using yfinance.
    Optimized for bulk/batch fetching to meet Vercel 30-second budget.
    """

    def fetch_historical_prices(self, tickers: List[str], days: int = 180) -> Dict[str, pd.DataFrame]:
        """
        Fetch historical daily prices for multiple tickers in a single batch call.
        """
        if not tickers:
            return {}

        period = f"{days}d"
        results: Dict[str, pd.DataFrame] = {}

        try:
            # Batch download for speed
            data = yf.download(
                tickers=tickers,
                period=period,
                interval="1d",
                group_by="ticker",
                auto_adjust=True,
                progress=False,
                threads=True
            )

            if data.empty:
                logger.warning("yfinance returned empty dataset for tickers: %s", tickers)
                return {}

            for ticker in tickers:
                symbol = ticker.upper()
                try:
                    if len(tickers) == 1:
                        df = data.copy()
                    elif symbol in data.columns.levels[0]:
                        df = data[symbol].copy()
                    else:
                        continue

                    # Clean dataframe
                    df = df.dropna(subset=["Close"])
                    if not df.empty:
                        results[symbol] = df
                except Exception as e:
                    logger.warning("Error parsing history for %s: %s", symbol, str(e))

        except Exception as e:
            logger.error("Failed batch fetching historical prices: %s", str(e))

        return results

    def fetch_current_snapshot(self, tickers: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Fetch snapshot information (latest price, prev close, % change) for tickers.
        """
        hist_data = self.fetch_historical_prices(tickers, days=7)
        snapshots: Dict[str, Dict[str, Any]] = {}

        for ticker in tickers:
            symbol = ticker.upper()
            if symbol in hist_data and not hist_data[symbol].empty:
                df = hist_data[symbol]
                if len(df) >= 1:
                    latest_close = float(df["Close"].iloc[-1])
                    prev_close = float(df["Close"].iloc[-2]) if len(df) >= 2 else latest_close
                    pct_change = ((latest_close - prev_close) / prev_close * 100.0) if prev_close != 0 else 0.0

                    snapshots[symbol] = {
                        "symbol": symbol,
                        "current_price": round(latest_close, 2),
                        "previous_close": round(prev_close, 2),
                        "change_percent": round(pct_change, 2),
                        "timestamp": df.index[-1].strftime("%Y-%m-%d"),
                        "company_name": SYMBOL_LOOKUP.get(symbol, {}).get("name", symbol),
                        "industry": SYMBOL_LOOKUP.get(symbol, {}).get("industry", "Unknown")
                    }

        return snapshots

    def fetch_company_metadata(self, ticker: str) -> Dict[str, Any]:
        """
        Fetch metadata for a single company.
        """
        symbol = ticker.upper()
        meta = SYMBOL_LOOKUP.get(symbol, {"name": symbol, "industry": "Unknown"})

        try:
            yt = yf.Ticker(symbol)
            info = yt.info or {}
            return {
                "symbol": symbol,
                "name": info.get("longName", meta["name"]),
                "industry": info.get("industry", meta["industry"]),
                "sector": info.get("sector", "Technology"),
                "market_cap": info.get("marketCap", 0),
                "summary": info.get("longBusinessSummary", "No summary available.")
            }
        except Exception as e:
            logger.warning("Error fetching metadata for %s: %s", symbol, str(e))
            return {
                "symbol": symbol,
                "name": meta["name"],
                "industry": meta["industry"],
                "sector": "General",
                "market_cap": 0,
                "summary": "Information unavailable."
            }
