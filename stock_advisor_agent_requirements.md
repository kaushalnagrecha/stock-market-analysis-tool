# Stock Advisor Agent
## Detailed Product & Technical Requirements Specification

**Document Status:** Draft Requirements  
**Target Platform:** Vercel  
**Target UI Framework:** SpringBoot  
**Primary Constraint:** Must run on Vercel free-tier hardware with approximately **30 seconds or less** end-to-end response time for normal dashboard refresh and user-requested analysis workflows.

---

# 1. Executive Summary

The Stock Advisor Agent is an AI-assisted stock and industry analysis application deployed as a Vercel free app. The application will combine market-data retrieval, quantitative/financial analysis, visualization, and natural-language explanation into a single user experience.

The application has two primary experiences:

1. **Dashboard**
   - The default landing tab.
   - Presents a high-level view of current industry and company performance.
   - Displays four KPI cards and three six-month trend-analysis charts.
   - Allows the user to refresh the underlying market data and regenerate the analysis.

2. **AI Stock Advisor Chat**
   - A SpringBoot chatbot.
   - Accepts natural-language questions about stocks, companies, and industries.
   - Routes requests through the appropriate specialized sub-agents.
   - Returns financial analysis in a technically accurate but understandable form.
   - Explains results in language suitable for a non-expert user.

The system should be designed as a lightweight, modular multi-agent application rather than a monolithic chatbot. The three core sub-agents are:

- **Fetching Sub-Agent**
- **Financial Analysis Sub-Agent**
- **Explaining Sub-Agent**

Where appropriate, the system should use **free and publicly available MCP servers/tools** or equivalent free data-access integrations. Any MCP or external data dependency must be evaluated against reliability, rate limits, licensing, and Vercel free-tier performance constraints.

> **Important financial disclaimer:** The application is an educational and informational stock analysis tool. It must not present itself as a licensed financial advisor, guarantee returns, or provide personalized financial advice. The UI and chatbot should clearly communicate that outputs are informational and that users should conduct their own research and consult qualified professionals where appropriate.

---

# 2. Goals

## 2.1 Primary Goals

The application must:

- Provide a fast, visually understandable overview of market and industry performance.
- Identify top-performing and worst-performing industries.
- Identify top-performing and worst-performing companies.
- Analyze six months of historical trends.
- Provide useful visualizations to support financial analysis.
- Allow users to request analysis for:
  - Specific companies/stocks.
  - Multiple stocks.
  - Industries.
  - Companies within an industry.
  - General market or trend questions.
- Explain quantitative analysis in plain, layman-understandable language.
- Support fresh data retrieval through a manual refresh mechanism.
- Operate efficiently on Vercel free-tier hardware.
- Target approximately **30 seconds or less** for the complete dashboard refresh workflow under normal conditions.

## 2.2 Secondary Goals

The application should:

- Minimize redundant API calls.
- Cache reusable market data.
- Separate data acquisition from analysis and explanation.
- Produce deterministic analytical outputs from the same input data.
- Make it easy to replace or add market-data providers.
- Make the agent architecture modular enough to add future sub-agents.
- Provide transparent explanations of how conclusions were reached.

---

# 3. Non-Goals

The initial version should **not** attempt to:

- Execute stock trades.
- Connect to a user's brokerage account.
- Place buy/sell orders.
- Manage portfolios.
- Guarantee investment returns.
- Provide legally binding or fiduciary financial advice.
- Perform high-frequency trading.
- Replace a licensed financial advisor.
- Build a complex portfolio optimization engine unless explicitly added as a future feature.
- Use paid market-data APIs unless separately configured by the application owner.

---

# 4. High-Level User Journey

## 4.1 Landing Experience

When the user opens the Vercel app:

1. The application loads the **Dashboard** tab by default.
2. The system displays:
   - Four KPI cards.
   - Three trend-analysis charts.
   - Last data refresh timestamp.
   - Data source attribution where applicable.
   - A **Refresh Data & Analysis** button.
3. The user can:
   - Explore market/industry trends.
   - Switch to the AI Advisor tab.
   - Refresh the dashboard.
4. The dashboard should not require the user to enter a stock symbol before showing useful information.

## 4.2 Chat Experience

The user switches to the **AI Stock Advisor** tab.

Example questions not restricted to:

- "What are the top gaining industries right now?"
- "Why has NVIDIA performed well over the last six months?"
- "Compare Apple and Microsoft."
- "What are the biggest risks facing Tesla?"
- "Show me the trend for semiconductor stocks."
- "Which companies are driving growth in the technology sector?"
- "Explain why the healthcare sector has underperformed."
- "Analyze AAPL for me."
- "Compare the top five gainers in technology."
- "What does this analysis mean in simple terms?"

The system determines what data is required, retrieves it, analyzes it, and explains the findings.

---

# 5. System Architecture

## 5.1 Logical Architecture

```text
                         ┌─────────────────────────┐
                         │       Vercel App        │
                         │       React Fluid UI    │
                         └────────────┬────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    ▼                                   ▼
          ┌──────────────────┐                ┌────────────────────┐
          │    Dashboard     │                │  AI Advisor Chat   │
          │      Tab         │                │       Tab           │
          └────────┬─────────┘                └─────────┬──────────┘
                   │                                    │
                   │                                    ▼
                   │                         ┌─────────────────────┐
                   │                         │   Advisor Orchestrator│
                   │                         └──────────┬──────────┘
                   │                                    │
                   │                 ┌──────────────────┼──────────────────┐
                   │                 │                  │                  │
                   ▼                 ▼                  ▼                  │
          ┌────────────────┐  ┌───────────────┐  ┌───────────────┐         │
          │ Fetching       │  │ Financial     │  │ Explaining    │         │
          │ Sub-Agent      │─▶│ Analysis     │─▶│ Sub-Agent     │─────────┘
          │                │  │ Sub-Agent     │  │               │
          └───────┬────────┘  └───────┬───────┘  └───────────────┘
                  │                   │
                  ▼                   ▼
          ┌────────────────┐  ┌────────────────┐
          │ Market Data     │  │ Analysis &     │
          │ Sources / MCPs  │  │ Chart Engine   │
          └────────────────┘  └────────────────┘
```

---

# 6. Agent Architecture

## 6.1 Advisor Orchestrator

Although the required functional sub-agents are the three agents below, the application should include a lightweight orchestration layer responsible for routing requests.

### Responsibilities

The orchestrator should:

1. Receive the user request.
2. Determine the user's intent.
3. Identify required entities:
   - Stock ticker.
   - Company.
   - Industry.
   - Date range.
   - Comparison set.
4. Determine whether fresh data is required.
5. Invoke the Fetching Sub-Agent.
6. Pass normalized data to the Financial Analysis Sub-Agent.
7. Pass the resulting analysis to the Explaining Sub-Agent.
8. Return the final response to the user.

### Example Flow

```text
User:
"Compare Apple and Microsoft over the last 6 months."

        ↓

Intent Detection
        ↓

Entities:
AAPL, MSFT
Date range: 6 months
Analysis: comparative performance
        ↓

Fetching Sub-Agent
        ↓

Historical price + relevant metadata
        ↓

Financial Analysis Sub-Agent
        ↓

Returns, volatility, trend, relative performance
        ↓

Explaining Sub-Agent
        ↓

Plain-language explanation
        ↓

Chatbot Response
```

---

# 7. Sub-Agent 1: Fetching Sub-Agent

## 7.1 Purpose

The Fetching Sub-Agent is responsible for retrieving market and financial data required by the dashboard or chatbot.

It should support:

- All-stock requests.
- Specific-stock requests.
- Industry-level requests.
- Company-level requests.
- Historical data requests.
- Current/latest market data requests.

## 7.2 Inputs

The Fetching Sub-Agent should accept structured parameters:

```json
{
  "entities": [
    {
      "type": "stock",
      "symbol": "AAPL"
    }
  ],
  "industry": null,
  "date_range": {
    "start": "YYYY-MM-DD",
    "end": "YYYY-MM-DD"
  },
  "data_requirements": [
    "historical_prices",
    "current_price",
    "percentage_change",
    "company_metadata"
  ],
  "freshness_required": true
}
```

## 7.3 Required Data Categories

Where available, the agent should retrieve:

### Market Data

- Current/latest price.
- Previous close.
- Daily percentage change.
- Historical OHLCV data.
- Six-month historical prices.
- Market capitalization.
- Trading volume.

### Company Metadata

- Company name.
- Ticker symbol.
- Industry.
- Sector.
- Exchange.

### Optional Financial Data

If reliably available from a free source:

- Revenue.
- Earnings.
- EPS.
- P/E ratio.
- Dividend yield.
- Debt metrics.
- Profit margins.

The initial implementation should prioritize **market-price and trend data** because these are essential for the requested dashboard and are more likely to be available reliably through free sources.

## 7.4 Data Source Requirements

The implementation should prefer:

1. Free public market-data APIs.
2. Free-access financial data libraries.
3. Free MCP servers where applicable.
4. Public datasets where appropriate.

The implementation must:

- Abstract the data provider behind a provider interface.
- Handle provider failures.
- Handle missing data.
- Handle API rate limits.
- Avoid unnecessary repeated calls.
- Cache data during a session.
- Clearly identify the timestamp of retrieved data.

## 7.5 Caching

The Fetching Sub-Agent should implement caching.

Recommended cache layers:

```text
L1: In-memory application cache
L2: Session-level cache
L3: Optional persistent cache for dashboard datasets
```

Suggested behavior:

- Current market data: short TTL.
- Historical six-month data: longer TTL.
- Company metadata: longer TTL.
- Dashboard aggregate data: cache until manual refresh.

The **Refresh Data & Analysis** button must invalidate or bypass relevant cached data.

---

# 8. Sub-Agent 2: Financial Analysis Sub-Agent

## 8.1 Purpose

The Financial Analysis Sub-Agent converts raw market data into quantitative insights and visualizations.

It must be responsible for the analytical reasoning layer, not the final layman explanation.

## 8.2 Core Analysis

For individual stocks and companies, the agent should calculate, where data is available:

- Absolute price change.
- Percentage price change.
- Trend direction.
- Six-month return.
- Volatility.
- Moving averages.
- Relative performance.
- Maximum drawdown.
- Trading-volume trends.

Optional:

- RSI.
- MACD.
- Bollinger Bands.

Technical indicators should only be presented when they materially help answer the user's question.

## 8.3 Industry Analysis

The system must support aggregation at the industry level.

For each industry:

```text
Industry Performance =
Aggregate performance of constituent companies
```

The exact aggregation methodology must be explicitly defined and consistently applied.

Preferred initial methodology:

- Use a consistent constituent universe.
- Calculate individual company returns.
- Aggregate using a documented methodology.
- Prefer market-cap weighting where reliable market-cap data is available.
- Fall back to equal weighting if required data is unavailable.
- Record the methodology in the analysis metadata.

The application must not silently mix methodologies.

## 8.4 Ranking

The Financial Analysis Sub-Agent should generate:

- Top Gainer Industry.
- Top Loser Industry.
- Top Gainer Company.
- Top Loser Company.
- Top 5 Gainer Industries.
- Top 5 Gainer Companies within the top 3 gaining industries.
- Top 5 Loser Companies within the top 3 gaining industries.

The ranking period must be clearly defined.

Default ranking period:

- Six months for trend analysis.
- Latest available trading session/day for current snapshot KPIs, unless the application explicitly labels a different period.

The UI must display the relevant period.

---

# 9. Dashboard Requirements

## 9.1 Default Tab

The first tab should be named:

**Market Dashboard**

The dashboard must load automatically when the Space opens.

---

## 9.2 KPI Cards

The dashboard must display exactly four primary KPI cards.

### KPI 1: Top Gainer Industry

Display:

- Industry name.
- Percentage gain.
- Ranking period.
- Optional small supporting metric.

Example:

```text
TOP GAINER INDUSTRY

Semiconductors
+18.42%

6-Month Performance
```

### KPI 2: Top Loser Industry

Display:

- Industry name.
- Percentage loss.
- Ranking period.

Example:

```text
TOP LOSER INDUSTRY

Airlines
-12.35%

6-Month Performance
```

### KPI 3: Top Gainer Company

Display:

- Company name.
- Ticker.
- Percentage gain.
- Ranking period.

### KPI 4: Top Loser Company

Display:

- Company name.
- Ticker.
- Percentage loss.
- Ranking period.

---

# 10. Dashboard Charts

The dashboard must display exactly three primary trend-analysis charts.

All three charts should use a **six-month historical window**.

---

## 10.1 Chart 1: Top 5 Gaining Industries

### Title

**6-Month Trend: Top 5 Gaining Industries**

### Chart Type

Line chart.

### X-Axis

Date.

### Y-Axis

Normalized performance or percentage return.

### Series

Five industry-level trend lines.

### Requirement

The chart must make relative performance easy to compare.

Recommended approach:

- Normalize each industry to 100 at the beginning of the six-month period.
- Display indexed performance over time.

Example:

```text
Industry A ───────────────
Industry B ─────────────
Industry C ───────────
Industry D ──────────
Industry E ─────────
```

The exact visual styling should remain accessible and readable in both light and dark UI environments.

---

## 10.2 Chart 2: Top 5 Gaining Companies in Top 3 Gaining Industries

### Title

**6-Month Trend: Top 5 Gaining Companies in the Top 3 Gaining Industries**

### Chart Type

Line chart.

### Selection Logic

1. Identify the top three gaining industries.
2. Identify the top five gaining companies within those industries.
3. Plot the six-month historical trend for those companies.

### Series

Five company-level trend lines.

### Required Metadata

The chart should communicate:

- Company name.
- Ticker.
- Industry.

The user should be able to identify which industry each company belongs to.

---

## 10.3 Chart 3: Top 5 Losing Companies in Top 3 Gaining Industries

### Title

**6-Month Trend: Top 5 Losing Companies in the Top 3 Gaining Industries**

### Chart Type

Line chart.

### Selection Logic

1. Identify the top three gaining industries.
2. Within those industries, identify the five worst-performing companies.
3. Plot the six-month historical trend.

### Purpose

This chart is intended to reveal internal divergence.

It should help answer:

> "Even when an industry is performing well overall, which companies are lagging behind?"

---

# 11. Dashboard Refresh

The dashboard must include a prominent button:

**Refresh Data & Analysis**

## 11.1 Refresh Workflow

When clicked:

```text
User clicks Refresh
        ↓
Invalidate relevant cache
        ↓
Fetch latest market data
        ↓
Recalculate industry rankings
        ↓
Recalculate company rankings
        ↓
Recalculate six-month trends
        ↓
Regenerate charts
        ↓
Update KPI cards
        ↓
Update refresh timestamp
```

## 11.2 UI Behavior

During refresh:

- Disable the refresh button.
- Display a progress/status indicator.
- Show meaningful status messages.

Example:

```text
Fetching latest market data...
Analyzing industry performance...
Generating trend charts...
Updating dashboard...
```

On completion:

```text
Dashboard refreshed successfully.
Last updated: YYYY-MM-DD HH:MM UTC
```

On failure:

```text
Unable to fully refresh the dashboard.
Some data may be unavailable or stale.
```

The system should avoid replacing the entire dashboard with a blank state if only one data source fails.

---

# 12. AI Advisor Chat Tab

## 12.1 Interface

The second primary tab should be named:

**AI Stock Advisor**

The UI should use a Gradio chatbot interface.

Recommended components:

- Chatbot.
- User message input.
- Submit button.
- Clear chat button.
- Optional "Analyze Fresh Data" control.
- Optional example prompts.

## 12.2 Chatbot Capabilities

The chatbot should answer questions about:

- Individual stocks.
- Multiple stocks.
- Industries.
- Sector comparisons.
- Historical trends.
- Relative performance.
- Top gainers.
- Top losers.
- Dashboard insights.
- Financial metrics, when available.
- Risks and caveats.
- Plain-language explanations.

---

# 13. Chatbot Agent Routing

The chatbot should classify requests into one or more intents.

## Intent Examples

### Stock Analysis

```text
"Analyze AAPL."
```

### Comparative Analysis

```text
"Compare AAPL and MSFT."
```

### Industry Analysis

```text
"How is the semiconductor industry doing?"
```

### Ranking

```text
"Which industries are performing best?"
```

### Trend Analysis

```text
"How has Tesla performed over the last six months?"
```

### Explanation

```text
"Explain this in simple terms."
```

### Follow-Up

```text
"Why is that happening?"
```

The agent should retain enough conversational context to resolve follow-up questions.

---

# 14. Explaining Sub-Agent

## 14.1 Purpose

The Explaining Sub-Agent converts technical financial analysis into clear, accessible language.

It should not independently invent numerical findings.

It must ground its explanation in the structured output produced by the Financial Analysis Sub-Agent.

## 14.2 Output Structure

A recommended response format is:

### Short Answer

One or two sentences summarizing the finding.

### What Happened

Explain the observed trend.

### Why It Matters

Explain the significance.

### What the Data Shows

List key metrics.

### Risks / Caveats

Identify uncertainty and limitations.

### In Simple Terms

Provide a concise layman explanation.

### Disclaimer

For investment-oriented questions, remind users that the analysis is informational and not personalized financial advice.

---

# 15. Structured Agent Contracts

The sub-agents should communicate using structured objects rather than passing unstructured text wherever possible.

## 15.1 Fetching Sub-Agent Output

```json
{
  "status": "success",
  "retrieved_at": "2026-07-22T12:00:00Z",
  "source": "DATA_PROVIDER",
  "data": {
    "entities": [],
    "historical_prices": [],
    "metadata": []
  },
  "warnings": []
}
```

## 15.2 Financial Analysis Output

```json
{
  "status": "success",
  "analysis_type": "stock_comparison",
  "period": "6_months",
  "metrics": {},
  "findings": [],
  "rankings": [],
  "charts": [],
  "methodology": [],
  "warnings": []
}
```

## 15.3 Explaining Sub-Agent Output

```json
{
  "summary": "",
  "key_points": [],
  "plain_language_explanation": "",
  "risks_and_caveats": [],
  "disclaimer": ""
}
```

---

# 16. Chart Generation Requirements

Charts should be generated programmatically.

Preferred chart library:

- Plotly, if performance and package size are acceptable.
- Matplotlib as a fallback.

Charts must:

- Be readable in Gradio.
- Support responsive sizing.
- Include titles.
- Include axis labels.
- Include legends.
- Include hover information where supported.
- Clearly identify the time period.
- Clearly identify whether values are absolute prices, percentage returns, or indexed performance.

For multi-series charts, indexed performance is preferred to prevent high-priced stocks or differently scaled industries from visually dominating the chart.

---

# 17. MCP Requirements

The system should use **free, publicly available MCP servers/tools where applicable**.

Potential MCP use cases may include:

- Market data retrieval.
- Financial data lookup.
- Company information retrieval.
- Search and research.

MCP integrations must be evaluated against:

- Free availability.
- Public accessibility.
- Rate limits.
- Data reliability.
- Response latency.
- Licensing/usage restrictions.
- Hugging Face and Vercel compatibility.
- Ease of deployment.

MCP should not be introduced merely for architectural novelty.

If direct Python/API access is faster and more reliable for a data source, the implementation may use direct access instead.

The final architecture should favor the simplest reliable mechanism that satisfies the requirement.

---

# 18. Performance Requirements

## 18.1 Primary Performance Target

On Vercel free-tier:

**Target end-to-end dashboard refresh time: approximately 30 seconds or less.**

The target includes:

```text
Data retrieval
+
Data normalization
+
Industry aggregation
+
Ranking
+
Financial analysis
+
Chart generation
+
UI update
```

## 18.2 Performance Strategy

The implementation should:

- Avoid fetching every possible stock individually.
- Batch requests where supported.
- Cache historical data.
- Fetch only the minimum required data.
- Use concurrent/asynchronous requests where safe.
- Perform aggregation locally after data retrieval.
- Avoid unnecessary LLM calls.
- Avoid sending raw large datasets to an LLM.
- Use deterministic Python calculations for quantitative analysis.
- Use an LLM only for reasoning, summarization, routing, and explanation where necessary.
- Precompute dashboard data when practical.
- Refresh only changed datasets where possible.

## 18.3 Target Latency Budget

The following is a target allocation, not a guaranteed SLA:

```text
Data retrieval:           5-15 seconds
Data normalization:      1-3 seconds
Financial analysis:      1-5 seconds
Chart generation:        1-3 seconds
UI update:               <2 seconds
Buffer:                  remaining time
```

The implementation should measure actual performance and optimize based on observed bottlenecks.

---

# 19. LLM Usage Requirements

LLMs should not be used for deterministic numerical calculations.

The preferred division of responsibility is:

```text
Python / Analytics Layer
    ↓
Data calculations
    ↓
Statistical analysis
    ↓
Ranking
    ↓
Chart generation
    ↓
Structured findings
    ↓
LLM
    ↓
Explanation
```

The LLM should receive concise structured analysis rather than the full raw market dataset whenever possible.

This reduces:

- Token usage.
- Latency.
- Hallucination risk.
- Computational overhead.

---

# 20. Error Handling

The system must gracefully handle:

- Invalid ticker symbols.
- Unknown companies.
- Unknown industries.
- API timeouts.
- Rate limits.
- Missing historical data.
- Partial datasets.
- Market holidays.
- Delisted stocks.
- Provider outages.
- Empty search results.
- LLM failures.

Example:

```text
I couldn't retrieve reliable data for XYZ at the moment.
Please check the ticker symbol or try again later.
```

The system should never fabricate missing market data.

---

# 21. Data Quality Requirements

Every analytical response should maintain traceability to:

- Data source.
- Retrieval timestamp.
- Analysis period.
- Calculation methodology.

The application should distinguish between:

- Latest available data.
- Intraday data.
- End-of-day data.
- Historical data.

The UI should not imply real-time pricing unless the underlying source genuinely provides real-time data.

---

# 22. Financial Safety Requirements

The chatbot must not:

- Guarantee profits.
- Claim certainty about future stock prices.
- Present speculation as fact.
- Imply insider knowledge.
- Encourage reckless trading.
- Claim to be a licensed financial advisor.

When asked:

> "Should I buy this stock?"

The response should provide an evidence-based summary of relevant factors and explicitly state that the tool cannot make personalized investment decisions for the user.

The agent may say:

- "The data suggests..."
- "Historically..."
- "Based on the available six-month trend..."
- "Potential risks include..."

It should avoid:

- "You should definitely buy..."
- "This stock will go up..."
- "You are guaranteed to make money..."

---

# 23. Dashboard Data Model

The dashboard should maintain a structured state similar to:

```python
dashboard_state = {
    "last_updated": "...",
    "ranking_period": "6_months",
    "top_gainer_industry": {},
    "top_loser_industry": {},
    "top_gainer_company": {},
    "top_loser_company": {},
    "top_5_gainer_industries": [],
    "top_3_gainer_industries": [],
    "top_5_gainer_companies": [],
    "top_5_loser_companies": [],
    "charts": {
        "industry_trends": None,
        "gainer_company_trends": None,
        "loser_company_trends": None
    },
    "warnings": []
}
```

---

# 24. Suggested Project Structure

```text
stock-advisor/
│
├── app.py
├── requirements.txt
├── README.md
├── README_HF.md
│
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── fetching_agent.py
│   ├── financial_analysis_agent.py
│   └── explaining_agent.py
│
├── data/
│   ├── __init__.py
│   ├── providers/
│   │   ├── base.py
│   │   └── market_data_provider.py
│   ├── cache.py
│   └── normalization.py
│
├── analysis/
│   ├── __init__.py
│   ├── stock_analysis.py
│   ├── industry_analysis.py
│   ├── rankings.py
│   └── indicators.py
│
├── charts/
│   ├── __init__.py
│   ├── industry_trends.py
│   └── company_trends.py
│
├── ui/
│   ├── __init__.py
│   ├── dashboard.py
│   └── chatbot.py
│
├── prompts/
│   ├── explaining_agent.txt
│   └── advisor_system.txt
│
├── config/
│   └── settings.py
│
└── tests/
    ├── test_data.py
    ├── test_analysis.py
    ├── test_rankings.py
    └── test_agents.py
```

---

# 25. Recommended Execution Model

The dashboard should use a precomputed pipeline:

```text
Application startup
        ↓
Check cache
        ↓
Load dashboard dataset
        ↓
If valid → render immediately
        ↓
If invalid → fetch and compute
        ↓
Cache result
        ↓
Render dashboard
```

Manual refresh:

```text
Refresh clicked
        ↓
Fetch fresh data
        ↓
Recalculate everything
        ↓
Replace cached dashboard state
        ↓
Render updated dashboard
```

Chat:

```text
User question
        ↓
Orchestrator
        ↓
Intent + entity extraction
        ↓
Check existing cached data
        ↓
Fetch only missing data
        ↓
Financial analysis
        ↓
Explanation
        ↓
Response
```

---

# 26. Acceptance Criteria

## Dashboard

- [ ] Vercel App opens to the Market Dashboard.
- [ ] Dashboard displays exactly four KPI cards.
- [ ] Dashboard displays exactly three trend-analysis charts.
- [ ] All three charts use a six-month historical period.
- [ ] Chart 1 shows top five gaining industries.
- [ ] Chart 2 shows top five gaining companies within the top three gaining industries.
- [ ] Chart 3 shows top five losing companies within the top three gaining industries.
- [ ] KPI rankings are calculated consistently.
- [ ] Dashboard displays last-refresh timestamp.
- [ ] Refresh button retrieves fresh data and regenerates analysis.
- [ ] Dashboard handles partial data failures gracefully.

## Chatbot

- [ ] Gradio chatbot is available in a separate tab.
- [ ] User can ask about specific stocks.
- [ ] User can ask about industries.
- [ ] User can compare stocks.
- [ ] User can ask follow-up questions.
- [ ] Chatbot invokes the relevant sub-agents.
- [ ] Quantitative analysis is performed deterministically.
- [ ] Financial findings are converted into plain-language explanations.
- [ ] Chatbot does not fabricate unavailable data.
- [ ] Chatbot provides appropriate financial disclaimers.

## Performance

- [ ] Dashboard refresh targets approximately 30 seconds or less on Vercel free-tier hardware.
- [ ] Historical data is cached.
- [ ] Redundant API requests are minimized.
- [ ] LLM calls are minimized.
- [ ] Large raw datasets are not unnecessarily sent to the LLM.
- [ ] Performance timings are logged for each pipeline stage.

## Data Quality

- [ ] Data source is identifiable.
- [ ] Retrieval timestamp is recorded.
- [ ] Analysis period is explicit.
- [ ] Ranking methodology is documented.
- [ ] Missing data is clearly surfaced.
- [ ] The system does not fabricate market data.

---

# 27. Testing Requirements

## Unit Tests

Test:

- Percentage return calculations.
- Industry aggregation.
- Industry ranking.
- Company ranking.
- Six-month date filtering.
- Moving-average calculations.
- Missing data handling.

## Integration Tests

Test:

- Data provider → Fetching Sub-Agent.
- Fetching Sub-Agent → Financial Analysis Sub-Agent.
- Financial Analysis Sub-Agent → Explaining Sub-Agent.
- Dashboard refresh pipeline.
- Chatbot orchestration.

## Performance Tests

Measure:

- Cold-start dashboard load.
- Cached dashboard load.
- Full refresh.
- Individual stock analysis.
- Multi-stock comparison.
- Industry analysis.

Performance logs should capture:

```text
request_id
operation
data_fetch_time
analysis_time
chart_time
llm_time
total_time
cache_hit
status
```

---

# 28. Observability

The application should log:

- Request ID.
- Timestamp.
- User query category.
- Data-provider latency.
- Cache hits/misses.
- Agent execution time.
- LLM execution time.
- Total request time.
- Errors.
- Warnings.

Logs should avoid storing sensitive user information unnecessarily.

---

# 29. Future Enhancements

Potential future sub-agents:

### News & Sentiment Sub-Agent

Analyzes recent news and market sentiment.

### Risk Analysis Sub-Agent

Analyzes volatility, drawdown, and downside risk.

### Fundamental Analysis Sub-Agent

Analyzes financial statements and valuation metrics.

### Portfolio Analysis Sub-Agent

Analyzes a user-provided portfolio.

### Recommendation Sub-Agent

Provides evidence-based watchlists while maintaining appropriate financial disclaimers.

### Alert Sub-Agent

Monitors selected stocks and notifies users of significant changes.

These are outside the scope of the initial implementation.

---

# 30. Final Architecture Principle

The Stock Advisor Agent should follow this fundamental design:

```text
Reliable Data
      ↓
Deterministic Financial Analysis
      ↓
Clear Visualizations
      ↓
Structured Findings
      ↓
LLM-Powered Explanation
      ↓
Human-Friendly Advisor Experience
```

The system should use AI where AI adds value and conventional software where conventional software is more reliable.

In particular:

- **Data retrieval should be tool-driven.**
- **Numerical calculations should be deterministic.**
- **Charts should be generated from structured data.**
- **LLMs should explain and contextualize results.**
- **The dashboard should be precomputed/cached wherever possible.**
- **The application should optimize aggressively for Vercel free-tier constraints.**

The result should feel like a single intelligent Stock Advisor to the user, while internally remaining a modular system of specialized agents with clear responsibilities and measurable performance.
