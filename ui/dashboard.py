import gradio as gr
import plotly.graph_objects as go
from typing import Tuple, Any

from agents.fetching_agent import FetchingSubAgent
from agents.financial_analysis_agent import FinancialAnalysisSubAgent
from config.settings import STANDARD_DISCLAIMER

fetching_agent = FetchingSubAgent()
analysis_agent = FinancialAnalysisSubAgent()

def load_or_refresh_dashboard(force_refresh: bool = False) -> Tuple[
    str, str, str, str, str, go.Figure, go.Figure, go.Figure
]:
    """
    Executes dashboard data pipeline and returns HTML KPI cards, status, and 3 Plotly figures.
    """
    status_msg = "Refreshing market data & running financial calculations..."

    # Step 1: Fetch Data
    fetch_payload = fetching_agent.fetch_dashboard_dataset(force_refresh=force_refresh)

    # Step 2: Financial Analysis & Charts
    analysis_payload = analysis_agent.analyze_dashboard_data(fetch_payload)

    if analysis_payload.get("status") != "success":
        err_fig = go.Figure()
        err_fig.update_layout(title="Data Analysis Error")
        return (
            "<div style='padding:15px; border-radius:8px; background:#2A1B1B;'><b>Error:</b> Data unavailable.</div>",
            "N/A", "N/A", "N/A", "N/A", err_fig, err_fig, err_fig
        )

    rankings = analysis_payload.get("rankings", {})
    retrieved_at = analysis_payload.get("retrieved_at", "Just now")
    charts = analysis_payload.get("charts", {})

    top_ind = rankings.get("top_gainer_industry", {})
    bot_ind = rankings.get("top_loser_industry", {})
    top_comp = rankings.get("top_gainer_company", {})
    bot_comp = rankings.get("top_loser_company", {})

    # Helper function to render styled HTML KPI Cards
    def make_kpi_card(title: str, name: str, value: str, subtext: str, is_positive: bool) -> str:
        color = "#10B981" if is_positive else "#EF4444"
        bg_gradient = "linear-gradient(135deg, #1E293B 0%, #0F172A 100%)"
        return f"""
        <div style="background: {bg_gradient}; border: 1px solid #334155; border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); font-family: sans-serif;">
            <div style="color: #94A3B8; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">{title}</div>
            <div style="color: #F8FAFC; font-size: 1.4rem; font-weight: 700; margin: 8px 0 4px 0;">{name}</div>
            <div style="color: {color}; font-size: 1.8rem; font-weight: 800;">{value}</div>
            <div style="color: #64748B; font-size: 0.75rem; margin-top: 6px;">{subtext}</div>
        </div>
        """

    kpi1_html = make_kpi_card(
        "TOP GAINER INDUSTRY",
        top_ind.get("industry_name", "N/A"),
        f"+{top_ind.get('percentage_return_6m', 0.0):.2f}%",
        "6-Month Cumulative Return",
        True
    )

    kpi2_html = make_kpi_card(
        "TOP LOSER INDUSTRY",
        bot_ind.get("industry_name", "N/A"),
        f"{bot_ind.get('percentage_return_6m', 0.0):.2f}%",
        "6-Month Cumulative Return",
        False
    )

    kpi3_html = make_kpi_card(
        "TOP GAINER COMPANY",
        f"{top_comp.get('name', 'N/A')} ({top_comp.get('symbol', '')})",
        f"+{top_comp.get('percentage_return_6m', 0.0):.2f}%",
        "6-Month Cumulative Return",
        True
    )

    kpi4_html = make_kpi_card(
        "TOP LOSER COMPANY",
        f"{bot_comp.get('name', 'N/A')} ({bot_comp.get('symbol', '')})",
        f"{bot_comp.get('percentage_return_6m', 0.0):.2f}%",
        "6-Month Cumulative Return",
        False
    )

    status_text = f"✅ **Dashboard Refreshed Successfully** | Last Updated: `{retrieved_at}` |<br> Target Latency Budget: < 30s"

    return (
        status_text,
        kpi1_html,
        kpi2_html,
        kpi3_html,
        kpi4_html,
        charts.get("top_5_industry_trends", go.Figure()),
        charts.get("top_5_gainer_company_trends", go.Figure()),
        charts.get("top_5_loser_company_trends", go.Figure())
    )

def create_dashboard_tab() -> None:
    """Builds the Market Dashboard tab layout in Gradio."""
    gr.Markdown("## 📈 Market Dashboard")
    gr.Markdown("High-level overview of industry performance and 6-month historical trends.")

    with gr.Row():
        refresh_btn = gr.Button("🔄 Refresh Data & Analysis", variant="primary", scale=1)
        status_banner = gr.Markdown(
            "Click **Refresh Data & Analysis** to fetch latest prices and re-run calculations.",
            scale=5
        )

    gr.Markdown("### 📊 Key Performance Indicators (6-Month Horizon)")
    with gr.Row():
        kpi1 = gr.HTML(label="KPI 1", show_label=False)
        kpi2 = gr.HTML(label="KPI 2", show_label=False)
        kpi3 = gr.HTML(label="KPI 3", show_label=False)
        kpi4 = gr.HTML(label="KPI 4", show_label=False)

    gr.Markdown("### 📉 6-Month Trend Analysis Charts")
    chart1 = gr.Plot(label=None, show_label=False)

    with gr.Row():
        chart2 = gr.Plot(label=None, show_label=False)
        chart3 = gr.Plot(label=None, show_label=False)

    gr.Markdown(f"*{STANDARD_DISCLAIMER}*")

    # Wire up initial load & refresh button
    dashboard_outputs = [status_banner, kpi1, kpi2, kpi3, kpi4, chart1, chart2, chart3]

    refresh_btn.click(
        fn=lambda: load_or_refresh_dashboard(force_refresh=True),
        outputs=dashboard_outputs
    )

    # Initial load trigger
    def initial_load():
        return load_or_refresh_dashboard(force_refresh=False)

    return initial_load, dashboard_outputs
