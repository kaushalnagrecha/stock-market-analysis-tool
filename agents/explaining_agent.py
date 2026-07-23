import os
import json
import logging
from typing import Dict, Any

from config.settings import GEMINI_API_KEY, DEFAULT_LLM_MODEL, STANDARD_DISCLAIMER

logger = logging.getLogger(__name__)

class ExplainingSubAgent:
    """
    Sub-Agent 3: Explaining Sub-Agent
    Translates structured quantitative analysis into plain-language explanations.
    """

    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.model = DEFAULT_LLM_MODEL
        self.prompt_template = self._load_prompt_template()

    def _load_prompt_template(self) -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "explaining_agent.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return "Explain the following financial data clearly in layman's terms."

    def explain_analysis(
        self,
        query: str,
        structured_analysis: Dict[str, Any]
    ) -> str:
        """
        Generates a human-friendly explanation grounded in structured financial analysis.
        """
        # Prepare context payload
        context_str = json.dumps(structured_analysis, indent=2)

        # Check if API key is available for LLM generation
        if self.api_key:
            try:
                from google import genai
                client = genai.Client(api_key=self.api_key)
                prompt = (
                    f"{self.prompt_template}\n\n"
                    f"User Question: {query}\n\n"
                    f"Structured Financial Data:\n{context_str}\n\n"
                    "Generate plain-language explanation following the specified response structure."
                )
                response = client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                logger.warning("LLM API call failed, falling back to deterministic explanation: %s", str(e))

        # Fallback Deterministic Generator
        return self._generate_fallback_explanation(query, structured_analysis)

    def _generate_fallback_explanation(
        self,
        query: str,
        analysis: Dict[str, Any]
    ) -> str:
        """
        Fallback structured plain-language generator when LLM API key is not supplied.
        """
        findings = analysis.get("findings", [])

        if not findings:
            return (
                "### Short Answer\n"
                "Data for your query was processed, but no detailed findings were returned.\n\n"
                "### What Happened\n"
                "The system queried market sources for the specified symbols or industries.\n\n"
                "### Risks / Caveats\n"
                "- Ticker symbols may be incorrect or market data temporarily unavailable.\n\n"
                f"### Disclaimer\n{STANDARD_DISCLAIMER}"
            )

        lines = [f"### Analysis Summary for: '{query}'\n"]

        for item in findings:
            sym = item.get("symbol", "Asset")
            name = item.get("company_name", sym)
            ret_6m = item.get("percentage_return_6m", 0.0)
            price = item.get("latest_price", 0.0)
            trend = item.get("trend_direction", "Neutral")
            vol = item.get("volatility_annualized", 0.0)
            mdd = item.get("max_drawdown_percent", 0.0)
            rsi = item.get("rsi_14", None)

            lines.append(f"#### **{name} ({sym})**")
            lines.append(f"- **Current Price**: ${price:.2f}")
            lines.append(f"- **6-Month Performance**: **{ret_6m:+.2f}%**")
            lines.append(f"- **Overall Trend**: {trend}")
            lines.append(f"- **Annualized Volatility**: {vol:.2f}%")
            lines.append(f"- **Max 6-Month Drawdown**: {mdd:.2f}%")
            if rsi:
                lines.append(f"- **RSI (14-day)**: {rsi:.2f}")
            lines.append("")

        lines.append("### In Simple Terms")
        if len(findings) == 1:
            item = findings[0]
            ret = item.get("percentage_return_6m", 0)
            sym = item.get("symbol", "")
            if ret > 10:
                lines.append(f"{sym} has experienced strong positive momentum (+{ret:.1f}%) over the past 6 months.")
            elif ret < -10:
                lines.append(f"{sym} has faced significant downward pressure ({ret:.1f}%) over the past 6 months.")
            else:
                lines.append(f"{sym} has traded in a relatively stable range ({ret:+.1f}%) over the past 6 months.")
        else:
            lines.append("Comparing the selected stocks shows clear relative performance divergence over the 6-month historical period.")

        lines.append("\n### Risks & Caveats")
        lines.append("- Historical trend performance does not guarantee future stock price results.")
        lines.append("- Short-term volatility and macroeconomic sector headwinds can impact performance.")

        lines.append(f"\n### Disclaimer\n{STANDARD_DISCLAIMER}")

        return "\n".join(lines)
