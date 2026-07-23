from agents.explaining_agent import ExplainingSubAgent
from agents.orchestrator import AdvisorOrchestrator

def test_explaining_agent_fallback():
    agent = ExplainingSubAgent()
    mock_analysis = {
        "analysis_type": "stock_specific",
        "findings": [
            {
                "symbol": "AAPL",
                "company_name": "Apple Inc.",
                "latest_price": 185.50,
                "percentage_return_6m": 12.4,
                "trend_direction": "Bullish",
                "volatility_annualized": 18.2,
                "max_drawdown_percent": -8.5
            }
        ]
    }
    explanation = agent.explain_analysis("Analyze AAPL", mock_analysis)
    assert "Apple Inc." in explanation
    assert "AAPL" in explanation
    assert "+12.4" in explanation or "12.40%" in explanation or "12.4%" in explanation
    assert "Disclaimer" in explanation

def test_orchestrator_entity_extraction():
    orchestrator = AdvisorOrchestrator()
    symbols = orchestrator.extract_entities("Compare Apple and NVIDIA over 6 months")
    assert "AAPL" in symbols
    assert "NVDA" in symbols

def test_orchestrator_industry_keyword_extraction():
    orchestrator = AdvisorOrchestrator()
    symbols = orchestrator.extract_entities("why is the software and cloud industry losing so much?")
    assert "MSFT" in symbols
    assert "ORCL" in symbols
    assert "CRM" in symbols
