import pandas as pd
import numpy as np
import pytest

from analysis.stock_analysis import analyze_single_stock
from analysis.indicators import calculate_technical_indicators

def test_analyze_single_stock():
    prices = [100.0 + i for i in range(30)]
    df = pd.DataFrame({"Close": prices})
    res = analyze_single_stock("TEST", df)

    assert res["symbol"] == "TEST"
    assert res["start_price"] == 100.0
    assert res["latest_price"] == 129.0
    assert res["percentage_return_6m"] == 29.0
    assert res["trend_direction"] == "Bullish"

def test_calculate_technical_indicators():
    prices = [100.0 + (i % 5) for i in range(30)]
    df = pd.DataFrame({"Close": prices})
    inds = calculate_technical_indicators(df)

    assert "rsi_14" in inds
    assert "bollinger_upper" in inds
    assert "macd_line" in inds
