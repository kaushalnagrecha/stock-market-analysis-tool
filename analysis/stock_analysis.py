import numpy as np
import pandas as pd
from typing import Dict, Any

from data.normalization import calculate_cumulative_return

def analyze_single_stock(symbol: str, df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform deterministic quantitative analysis on a single stock's daily OHLCV DataFrame.
    """
    symbol = symbol.upper()
    if df.empty or "Close" not in df.columns:
        return {
            "symbol": symbol,
            "error": f"Insufficient data for {symbol}"
        }

    close = df["Close"].dropna()
    if len(close) < 2:
        return {
            "symbol": symbol,
            "error": f"Not enough price points for {symbol}"
        }

    start_price = float(close.iloc[0])
    latest_price = float(close.iloc[-1])
    abs_change = latest_price - start_price
    pct_return = calculate_cumulative_return(df)

    # Daily returns & volatility
    daily_returns = close.pct_change().dropna()
    volatility = float(daily_returns.std() * np.sqrt(252) * 100.0) if len(daily_returns) > 1 else 0.0

    # Max drawdown calculation
    cummax = close.cummax()
    drawdown = (close - cummax) / cummax
    max_drawdown = float(drawdown.min() * 100.0) if not drawdown.empty else 0.0

    # Moving averages
    sma_20 = float(close.tail(20).mean()) if len(close) >= 20 else latest_price
    sma_50 = float(close.tail(50).mean()) if len(close) >= 50 else latest_price

    # Trend direction based on SMA and 6m return
    trend = "Bullish" if pct_return > 5.0 and latest_price >= sma_20 else (
        "Bearish" if pct_return < -5.0 and latest_price <= sma_20 else "Neutral/Sideways"
    )

    return {
        "symbol": symbol,
        "start_price": round(start_price, 2),
        "latest_price": round(latest_price, 2),
        "absolute_change": round(abs_change, 2),
        "percentage_return_6m": round(pct_return, 2),
        "volatility_annualized": round(volatility, 2),
        "max_drawdown_percent": round(max_drawdown, 2),
        "sma_20": round(sma_20, 2),
        "sma_50": round(sma_50, 2),
        "trend_direction": trend,
        "trading_days": len(close)
    }
