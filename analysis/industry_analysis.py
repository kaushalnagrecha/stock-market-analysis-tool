import pandas as pd
from typing import Dict, List, Any

from analysis.stock_analysis import analyze_single_stock
from config.settings import INDUSTRY_UNIVERSE

def analyze_industry_performance(
    historical_data: Dict[str, pd.DataFrame]
) -> Dict[str, Dict[str, Any]]:
    """
    Aggregates performance across constituent companies for each industry.
    Returns structured dict mapping industry_name -> analysis metadata & returns.
    """
    industry_results: Dict[str, Dict[str, Any]] = {}

    for industry_name, company_list in INDUSTRY_UNIVERSE.items():
        constituent_returns: List[float] = []
        company_details: List[Dict[str, Any]] = []

        for comp in company_list:
            symbol = comp["symbol"]
            name = comp["name"]
            df = historical_data.get(symbol)

            if df is not None and not df.empty:
                stock_res = analyze_single_stock(symbol, df)
                if "error" not in stock_res:
                    stock_res["name"] = name
                    company_details.append(stock_res)
                    constituent_returns.append(stock_res["percentage_return_6m"])

        if constituent_returns:
            avg_return = sum(constituent_returns) / len(constituent_returns)
            best_company = max(company_details, key=lambda x: x["percentage_return_6m"])
            worst_company = min(company_details, key=lambda x: x["percentage_return_6m"])

            industry_results[industry_name] = {
                "industry_name": industry_name,
                "percentage_return_6m": round(avg_return, 2),
                "aggregation_method": "equal_weighted_constituent_average",
                "constituent_count": len(constituent_returns),
                "top_company": best_company["symbol"],
                "top_company_return": best_company["percentage_return_6m"],
                "worst_company": worst_company["symbol"],
                "worst_company_return": worst_company["percentage_return_6m"],
                "companies": company_details
            }

    return industry_results
