import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

# Broad market industry spectrum covering all 11 GICS sectors & sub-industries
BROAD_INDUSTRY_SPECTRUM: Dict[str, List[Dict[str, str]]] = {
    "Semiconductors & Hardware": [
        {"symbol": "NVDA", "name": "NVIDIA Corporation"},
        {"symbol": "AMD", "name": "Advanced Micro Devices"},
        {"symbol": "AVGO", "name": "Broadcom Inc."},
        {"symbol": "INTC", "name": "Intel Corporation"},
        {"symbol": "TSM", "name": "Taiwan Semiconductor"},
        {"symbol": "QCOM", "name": "Qualcomm Incorporated"},
        {"symbol": "MU", "name": "Micron Technology"},
        {"symbol": "AMAT", "name": "Applied Materials"}
    ],
    "Software & Cloud Services": [
        {"symbol": "MSFT", "name": "Microsoft Corporation"},
        {"symbol": "ORCL", "name": "Oracle Corporation"},
        {"symbol": "CRM", "name": "Salesforce Inc."},
        {"symbol": "ADBE", "name": "Adobe Inc."},
        {"symbol": "SNOW", "name": "Snowflake Inc."},
        {"symbol": "NOW", "name": "ServiceNow Inc."},
        {"symbol": "PANW", "name": "Palo Alto Networks"},
        {"symbol": "PLTR", "name": "Palantir Technologies"}
    ],
    "Consumer Tech & Internet": [
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "GOOGL", "name": "Alphabet Inc."},
        {"symbol": "META", "name": "Meta Platforms Inc."},
        {"symbol": "AMZN", "name": "Amazon.com Inc."},
        {"symbol": "NFLX", "name": "Netflix Inc."},
        {"symbol": "UBER", "name": "Uber Technologies"},
        {"symbol": "DASH", "name": "DoorDash Inc."}
    ],
    "Automotive & Electric Vehicles": [
        {"symbol": "TSLA", "name": "Tesla Inc."},
        {"symbol": "F", "name": "Ford Motor Company"},
        {"symbol": "GM", "name": "General Motors Company"},
        {"symbol": "RIVN", "name": "Rivian Automotive"},
        {"symbol": "LCID", "name": "Lucid Group Inc."},
        {"symbol": "TM", "name": "Toyota Motor Corp"},
        {"symbol": "RACE", "name": "Ferrari N.V."}
    ],
    "Healthcare & Pharmaceuticals": [
        {"symbol": "LLY", "name": "Eli Lilly and Company"},
        {"symbol": "JNJ", "name": "Johnson & Johnson"},
        {"symbol": "PFE", "name": "Pfizer Inc."},
        {"symbol": "UNH", "name": "UnitedHealth Group"},
        {"symbol": "MRK", "name": "Merck & Co. Inc."},
        {"symbol": "ABBV", "name": "AbbVie Inc."},
        {"symbol": "AMGN", "name": "Amgen Inc."}
    ],
    "Banking & Financial Services": [
        {"symbol": "JPM", "name": "JPMorgan Chase & Co."},
        {"symbol": "BAC", "name": "Bank of America Corp"},
        {"symbol": "GS", "name": "The Goldman Sachs Group"},
        {"symbol": "MS", "name": "Morgan Stanley"},
        {"symbol": "C", "name": "Citigroup Inc."},
        {"symbol": "V", "name": "Visa Inc."},
        {"symbol": "MA", "name": "Mastercard Inc."},
        {"symbol": "BRK-B", "name": "Berkshire Hathaway"}
    ],
    "Energy & Oil & Gas": [
        {"symbol": "XOM", "name": "Exxon Mobil Corp"},
        {"symbol": "CVX", "name": "Chevron Corp"},
        {"symbol": "COP", "name": "ConocoPhillips"},
        {"symbol": "SLB", "name": "Schlumberger N.V."},
        {"symbol": "OXY", "name": "Occidental Petroleum"},
        {"symbol": "EOG", "name": "EOG Resources"}
    ],
    "Airlines & Aerospace & Defense": [
        {"symbol": "DAL", "name": "Delta Air Lines Inc."},
        {"symbol": "UAL", "name": "United Airlines Holdings"},
        {"symbol": "AAL", "name": "American Airlines Group"},
        {"symbol": "BA", "name": "The Boeing Company"},
        {"symbol": "LMT", "name": "Lockheed Martin Corp"},
        {"symbol": "RTX", "name": "RTX Corporation"}
    ],
    "Retail & Consumer Discretionary": [
        {"symbol": "WMT", "name": "Walmart Inc."},
        {"symbol": "TGT", "name": "Target Corp"},
        {"symbol": "COST", "name": "Costco Wholesale Corp"},
        {"symbol": "HD", "name": "The Home Depot Inc."},
        {"symbol": "LOW", "name": "Lowe's Companies Inc."},
        {"symbol": "BABA", "name": "Alibaba Group Holding"}
    ],
    "Telecommunications & Media": [
        {"symbol": "VZ", "name": "Verizon Communications"},
        {"symbol": "T", "name": "AT&T Inc."},
        {"symbol": "TMUS", "name": "T-Mobile US Inc."},
        {"symbol": "CMCSA", "name": "Comcast Corporation"},
        {"symbol": "DIS", "name": "The Walt Disney Company"}
    ],
    "Industrials & Heavy Machinery": [
        {"symbol": "CAT", "name": "Caterpillar Inc."},
        {"symbol": "DE", "name": "Deere & Company"},
        {"symbol": "GE", "name": "General Electric Co."},
        {"symbol": "HON", "name": "Honeywell International"},
        {"symbol": "UNP", "name": "Union Pacific Corp"}
    ],
    "Basic Materials & Chemicals": [
        {"symbol": "LIN", "name": "Linde plc"},
        {"symbol": "APD", "name": "Air Products and Chemicals"},
        {"symbol": "NEM", "name": "Newmont Corporation"},
        {"symbol": "FCX", "name": "Freeport-McMoRan Inc."},
        {"symbol": "NUE", "name": "Nucor Corporation"}
    ],
    "Real Estate & REITs": [
        {"symbol": "PLD", "name": "Prologis Inc."},
        {"symbol": "AMT", "name": "American Tower Corp"},
        {"symbol": "EQIX", "name": "Equinix Inc."},
        {"symbol": "SPG", "name": "Simon Property Group"},
        {"symbol": "O", "name": "Realty Income Corp"}
    ],
    "Utilities & Clean Power": [
        {"symbol": "NEE", "name": "NextEra Energy Inc."},
        {"symbol": "DUK", "name": "Duke Energy Corp"},
        {"symbol": "SO", "name": "The Southern Company"},
        {"symbol": "AEP", "name": "American Electric Power"},
        {"symbol": "ENPH", "name": "Enphase Energy Inc."}
    ],
    "Consumer Staples & Food": [
        {"symbol": "PG", "name": "Procter & Gamble Co."},
        {"symbol": "KO", "name": "The Coca-Cola Company"},
        {"symbol": "PEP", "name": "PepsiCo Inc."},
        {"symbol": "PM", "name": "Philip Morris International"},
        {"symbol": "MDLZ", "name": "Mondelez International"}
    ]
}

class IndustryProvider:
    """
    Service supplying the broadened industry universe and API payload structures.
    """

    @staticmethod
    def get_all_industries() -> Dict[str, List[Dict[str, str]]]:
        """Returns full spectrum of market industries and constituent companies."""
        return BROAD_INDUSTRY_SPECTRUM

    @staticmethod
    def get_industry_names() -> List[str]:
        """Returns list of all supported industry names."""
        return list(BROAD_INDUSTRY_SPECTRUM.keys())

    @staticmethod
    def get_symbol_map() -> Dict[str, Dict[str, str]]:
        """Returns mapping of Ticker -> Name & Industry."""
        symbol_map = {}
        for ind_name, companies in BROAD_INDUSTRY_SPECTRUM.items():
            for comp in companies:
                symbol_map[comp["symbol"].upper()] = {
                    "name": comp["name"],
                    "industry": ind_name
                }
        return symbol_map

    @staticmethod
    def get_api_payload() -> Dict[str, Any]:
        """
        Returns complete JSON payload for GET /api/industries endpoint.
        """
        industries_summary = []
        for ind_name, companies in BROAD_INDUSTRY_SPECTRUM.items():
            industries_summary.append({
                "industry_name": ind_name,
                "company_count": len(companies),
                "sample_tickers": [c["symbol"] for c in companies[:4]],
                "companies": companies
            })

        return {
            "status": "success",
            "total_industries": len(BROAD_INDUSTRY_SPECTRUM),
            "total_companies": sum(len(c) for c in BROAD_INDUSTRY_SPECTRUM.values()),
            "industries": industries_summary
        }
