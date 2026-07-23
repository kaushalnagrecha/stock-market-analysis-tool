# Stock Advisor Agent

An AI-assisted stock and industry analysis application built with Python, Gradio, Plotly, and yfinance.

## Architecture

The system is built as a modular multi-agent application:
- **Fetching Sub-Agent**: Data acquisition layer with caching and market provider abstractions.
- **Financial Analysis Sub-Agent**: Deterministic quantitative analysis layer (6m returns, volatility, drawdowns, rankings) and Plotly chart generator.
- **Explaining Sub-Agent**: Plain-language explanation layer grounded strictly in quantitative findings.
- **Advisor Orchestrator**: Natural-language routing and entity extraction layer.

## User Interface

1. **Market Dashboard Tab**: 4 KPI Cards (Top Gainer/Loser Industry, Top Gainer/Loser Company) and 3 six-month Base-100 normalized trend charts. Includes manual data refresh with status tracking.
2. **AI Stock Advisor Tab**: Gradio chatbot interface supporting natural-language questions about stocks, companies, industries, and market trends.

## Setup & Running

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open `http://localhost:7860` in your browser.

## Testing

```bash
pytest
```
