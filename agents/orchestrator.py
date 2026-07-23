import re
import logging
from typing import Dict, List, Any

from agents.fetching_agent import FetchingSubAgent
from agents.financial_analysis_agent import FinancialAnalysisSubAgent
from agents.explaining_agent import ExplainingSubAgent
from config.settings import SYMBOL_LOOKUP, INDUSTRY_UNIVERSE

logger = logging.getLogger(__name__)

# Common English words that happen to be ticker symbols
STOPWORD_TICKERS = {"SO", "A", "FOR", "IS", "ON", "IT", "BE", "ALL", "CAN", "NOW", "ONE", "HAS", "ANY", "BIG"}

class AdvisorOrchestrator:
    """
    Advisor Orchestrator
    Lightweight orchestration layer routing natural-language queries through sub-agents.
    """

    def __init__(self):
        self.fetching_agent = FetchingSubAgent()
        self.analysis_agent = FinancialAnalysisSubAgent()
        self.explaining_agent = ExplainingSubAgent()

    def extract_entities(self, query: str) -> List[str]:
        """
        Extract stock symbols or industry constituent tickers mentioned in user query.
        """
        query_upper = query.upper()
        found_symbols = set()

        # 1. Check explicit stock symbols in SYMBOL_LOOKUP (excluding stop words unless uppercase/prefixed)
        for symbol in SYMBOL_LOOKUP.keys():
            if symbol in STOPWORD_TICKERS:
                # Require $TICKER or exact match in original case
                if f"${symbol}" in query_upper or re.search(r'\b' + symbol + r'\b', query):
                    found_symbols.add(symbol)
            else:
                if re.search(r'\b' + re.escape(symbol) + r'\b', query_upper):
                    found_symbols.add(symbol)

        # 2. Check company names
        for symbol, info in SYMBOL_LOOKUP.items():
            name_parts = info["name"].upper().split()
            first_name = name_parts[0]
            if len(first_name) > 3 and first_name not in {"CORP", "INC.", "THE", "GROUP", "PLC"}:
                if re.search(r'\b' + re.escape(first_name) + r'\b', query_upper):
                    found_symbols.add(symbol)

        # 3. Check industry keywords
        industry_keywords_map = {
            "SOFTWARE": "Software & Cloud Services",
            "CLOUD": "Software & Cloud Services",
            "SEMICONDUCTOR": "Semiconductors & Hardware",
            "CHIP": "Semiconductors & Hardware",
            "HARDWARE": "Semiconductors & Hardware",
            "AUTO": "Automotive & Electric Vehicles",
            "AUTOMOTIVE": "Automotive & Electric Vehicles",
            "EV": "Automotive & Electric Vehicles",
            "HEALTHCARE": "Healthcare & Pharmaceuticals",
            "PHARMA": "Healthcare & Pharmaceuticals",
            "BANK": "Banking & Financial Services",
            "BANKING": "Banking & Financial Services",
            "FINANCE": "Banking & Financial Services",
            "ENERGY": "Energy & Oil & Gas",
            "OIL": "Energy & Oil & Gas",
            "AIRLINE": "Airlines & Aerospace & Defense",
            "DEFENSE": "Airlines & Aerospace & Defense",
            "RETAIL": "Retail & Consumer Discretionary",
            "TELECOM": "Telecommunications & Media",
            "INDUSTRIAL": "Industrials & Heavy Machinery",
            "MATERIALS": "Basic Materials & Chemicals",
            "REAL ESTATE": "Real Estate & REITs",
            "REIT": "Real Estate & REITs",
            "UTILITIES": "Utilities & Clean Power",
            "STAPLES": "Consumer Staples & Food"
        }

        for keyword, ind_name in industry_keywords_map.items():
            if re.search(r'\b' + re.escape(keyword) + r'\b', query_upper):
                companies = INDUSTRY_UNIVERSE.get(ind_name, [])
                for c in companies:
                    found_symbols.add(c["symbol"])

        return sorted(list(found_symbols))

    def process_chat_query(self, query: str) -> str:
        """
        Main orchestration workflow for user chat queries.
        """
        if not query or not query.strip():
            return "Please enter a question about stocks, industries, or market trends."

        extracted_symbols = self.extract_entities(query)

        # Fallback to top tickers if no explicit symbol or industry is matched
        if not extracted_symbols:
            extracted_symbols = ["NVDA", "AAPL", "MSFT"]

        logger.info("Orchestrator routed query '%s' for tickers: %s", query, extracted_symbols)

        # 1. Fetching Sub-Agent
        fetch_payload = self.fetching_agent.fetch_specific_tickers(extracted_symbols, days=180)

        # 2. Financial Analysis Sub-Agent
        analysis_payload = self.analysis_agent.analyze_specific_stocks(extracted_symbols, fetch_payload)

        # 3. Explaining Sub-Agent
        final_explanation = self.explaining_agent.explain_analysis(query, analysis_payload)

        return final_explanation
