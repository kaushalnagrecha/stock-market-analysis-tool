import pandas as pd
import numpy as np
from typing import Dict, Any

def calculate_rsi(series: pd.Series, period: int = 14) -> float:
    """Calculate Relative Strength Index (RSI)."""
    if len(series) < period + 1:
        return 50.0

    delta = series.diff().dropna()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    last_loss = loss.iloc[-1]
    if last_loss == 0:
        return 100.0

    rs = gain.iloc[-1] / last_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return float(rsi)

def calculate_technical_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate RSI, MACD, and Bollinger Bands for a stock DataFrame."""
    if df.empty or "Close" not in df.columns:
        return {}

    close = df["Close"].dropna()
    if len(close) < 20:
        return {}

    rsi_14 = calculate_rsi(close, 14)

    # Bollinger Bands (20-day)
    sma_20 = close.rolling(window=20).mean()
    std_20 = close.rolling(window=20).std()
    upper_band = float(sma_20.iloc[-1] + 2 * std_20.iloc[-1])
    lower_band = float(sma_20.iloc[-1] - 2 * std_20.iloc[-1])

    # MACD (12, 26)
    ema_12 = close.ewm(span=12, adjust=False).mean()
    ema_26 = close.ewm(span=26, adjust=False).mean()
    macd_line = ema_12 - ema_26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    macd_val = float(macd_line.iloc[-1])
    signal_val = float(signal_line.iloc[-1])

    return {
        "rsi_14": round(rsi_14, 2),
        "bollinger_upper": round(upper_band, 2),
        "bollinger_lower": round(lower_band, 2),
        "macd_line": round(macd_val, 2),
        "macd_signal": round(signal_val, 2)
    }
