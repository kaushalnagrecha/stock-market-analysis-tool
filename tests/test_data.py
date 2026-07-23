import pandas as pd
import numpy as np
import pytest

from data.normalization import normalize_to_base_100, calculate_cumulative_return
from data.cache import MarketDataCache

def test_calculate_cumulative_return():
    df = pd.DataFrame({"Close": [100.0, 110.0, 120.0, 150.0]})
    ret = calculate_cumulative_return(df)
    assert pytest.approx(ret, 0.01) == 50.0

def test_normalize_to_base_100():
    df_a = pd.DataFrame({"Close": [50.0, 55.0, 60.0]}, index=pd.date_range("2026-01-01", periods=3))
    df_b = pd.DataFrame({"Close": [200.0, 180.0, 220.0]}, index=pd.date_range("2026-01-01", periods=3))

    normalized = normalize_to_base_100({"AAPL": df_a, "MSFT": df_b})
    assert not normalized.empty
    assert pytest.approx(normalized["AAPL"].iloc[0], 0.01) == 100.0
    assert pytest.approx(normalized["AAPL"].iloc[-1], 0.01) == 120.0
    assert pytest.approx(normalized["MSFT"].iloc[0], 0.01) == 100.0
    assert pytest.approx(normalized["MSFT"].iloc[-1], 0.01) == 110.0

def test_market_data_cache():
    cache = MarketDataCache()
    cache.set("test_key", {"data": 123}, ttl_seconds=10)
    assert cache.get("test_key") == {"data": 123}
    cache.invalidate("test")
    assert cache.get("test_key") is None
