import os
from typing import Dict, List

from data.providers.industry_provider import IndustryProvider

# Dynamic Broadened Market Industry Universe
INDUSTRY_UNIVERSE: Dict[str, List[Dict[str, str]]] = IndustryProvider.get_all_industries()

# Ticker -> Company Info + Industry lookup map
SYMBOL_LOOKUP: Dict[str, Dict[str, str]] = IndustryProvider.get_symbol_map()

# Data & Cache Configuration
DEFAULT_HISTORICAL_DAYS = 180  # 6 months historical trend window
CACHE_TTL_CURRENT_SECONDS = 300  # 5 minutes
CACHE_TTL_HISTORICAL_SECONDS = 86400  # 24 hours
DEFAULT_AGGREGATION_METHOD = "equal_weighted"

# LLM Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
DEFAULT_LLM_MODEL = "gemini-2.5-flash"

# Legal Financial Disclaimer Requirement
STANDARD_DISCLAIMER = (
    "Disclaimer: This Stock Advisor Agent is an educational and informational tool. "
    "It does not constitute licensed financial advice, personalized investment recommendations, "
    "or a guarantee of future performance. Always conduct independent research and consult a qualified "
    "financial advisor before making investment decisions."
)
