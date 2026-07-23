import logging
from typing import Dict, List, Any

from analysis.industry_analysis import analyze_industry_performance
from analysis.stock_analysis import analyze_single_stock
from analysis.rankings import compute_rankings
from analysis.indicators import calculate_technical_indicators
from charts.industry_trends import create_top_5_industry_trends_chart
from charts.company_trends import create_company_trends_chart

logger = logging.getLogger(__name__)

class FinancialAnalysisSubAgent:
    """
    Sub-Agent 2: Financial Analysis Sub-Agent
    Performs deterministic quantitative calculations and generates Plotly visualizations.
    """

    def analyze_dashboard_data(self, fetch_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes full universe market data, computes KPI rankings, and builds 3 Plotly trend charts.
        """
        hist_data = fetch_payload.get("data", {}).get("historical_prices", {})
        retrieved_at = fetch_payload.get("retrieved_at", "Unknown")

        if not hist_data:
            return {
                "status": "error",
                "warnings": ["No historical market data available for analysis."]
            }

        # 1. Perform Industry Level Performance & Aggregation
        industry_perf = analyze_industry_performance(hist_data)

        # 2. Compute Rankings for KPIs and Charts
        rankings = compute_rankings(industry_perf)

        # 3. Generate Chart 1: Top 5 Gaining Industries
        chart_1 = create_top_5_industry_trends_chart(
            rankings.get("top_5_gainer_industries", []),
            hist_data
        )

        # 4. Generate Chart 2: Top 5 Gaining Companies in Top 3 Gaining Industries
        chart_2 = create_company_trends_chart(
            rankings.get("top_5_gaining_companies_in_top_3_industries", []),
            hist_data,
            title="6-Month Trend: Top 5 Gainers",
            subtitle="Filtered within the Top 3 Overall Gaining Industries"
        )

        # 5. Generate Chart 3: Top 5 Losing Companies in Top 3 Gaining Industries
        chart_3 = create_company_trends_chart(
            rankings.get("top_5_losing_companies_in_top_3_industries", []),
            hist_data,
            title="6-Month Trend: Top 5 Losers",
            subtitle="Revealing Internal Divergence within the Top 3 Overall Gainer Industries"
        )

        return {
            "status": "success",
            "retrieved_at": retrieved_at,
            "period": "6_months",
            "methodology": "Equal-weighted constituent average per industry; Base-100 indexed trend comparison",
            "rankings": rankings,
            "industry_analysis": industry_perf,
            "charts": {
                "top_5_industry_trends": chart_1,
                "top_5_gainer_company_trends": chart_2,
                "top_5_loser_company_trends": chart_3
            },
            "warnings": []
        }

    def analyze_specific_stocks(
        self,
        tickers: List[str],
        fetch_payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Performs stock-level and comparative analysis for natural-language chat queries.
        """
        hist_data = fetch_payload.get("data", {}).get("historical_prices", {})
        snapshots = fetch_payload.get("data", {}).get("snapshots", {})

        stock_findings = []
        for symbol in tickers:
            symbol = symbol.upper()
            df = hist_data.get(symbol)
            if df is not None and not df.empty:
                analysis = analyze_single_stock(symbol, df)
                indicators = calculate_technical_indicators(df)
                snap = snapshots.get(symbol, {})

                analysis.update(indicators)
                analysis.update(snap)
                stock_findings.append(analysis)

        return {
            "status": "success",
            "analysis_type": "stock_specific" if len(tickers) == 1 else "stock_comparison",
            "period": "6_months",
            "findings": stock_findings,
            "warnings": []
        }
