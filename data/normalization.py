import pandas as pd
from typing import Dict

def normalize_to_base_100(df_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Normalizes multiple ticker Close price DataFrames to Base 100 on start date.
    Returns a unified DataFrame with Date index and tickers as columns.
    """
    if not df_dict:
        return pd.DataFrame()

    series_dict = {}
    for symbol, df in df_dict.items():
        if df.empty or "Close" not in df.columns:
            continue
        close_series = df["Close"].copy()
        first_valid = close_series.first_valid_index()
        if first_valid is not None and close_series.loc[first_valid] != 0:
            base_val = close_series.loc[first_valid]
            series_dict[symbol] = (close_series / base_val) * 100.0

    if not series_dict:
        return pd.DataFrame()

    combined_df = pd.DataFrame(series_dict)
    combined_df = combined_df.ffill().bfill()
    return combined_df

def calculate_cumulative_return(df: pd.DataFrame) -> float:
    """
    Calculate 6-month cumulative return percentage from a Close price DataFrame.
    """
    if df.empty or "Close" not in df.columns:
        return 0.0

    close = df["Close"].dropna()
    if len(close) < 2:
        return 0.0

    start_price = close.iloc[0]
    end_price = close.iloc[-1]

    if start_price == 0:
        return 0.0

    return float(((end_price - start_price) / start_price) * 100.0)
