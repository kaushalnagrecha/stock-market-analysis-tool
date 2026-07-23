import pandas as pd
import plotly.graph_objects as go
from typing import Dict, List, Any

from data.normalization import normalize_to_base_100

def create_company_trends_chart(
    companies: List[Dict[str, Any]],
    historical_data: Dict[str, pd.DataFrame],
    title: str,
    subtitle: str
) -> go.Figure:
    """
    Creates Chart 2 or Chart 3: 6-Month Company Trends (Base 100 Normalized Line Chart).
    Consistent horizontal center-aligned legend format matching industry charts.
    """
    fig = go.Figure()

    if not companies:
        fig.update_layout(
            title=f"{title} (No Data Available)",
            template="plotly_dark",
            height=600
        )
        return fig

    comp_tickers = [c["symbol"] for c in companies]
    comp_df_dict = {t: historical_data[t] for t in comp_tickers if t in historical_data}
    normalized_df = normalize_to_base_100(comp_df_dict)

    if not normalized_df.empty:
        for comp in companies:
            symbol = comp["symbol"]
            name = comp.get("name", symbol)
            industry = comp.get("industry", "")
            ret = comp.get("percentage_return_6m", 0.0)

            if symbol in normalized_df.columns:
                series = normalized_df[symbol]
                fig.add_trace(go.Scatter(
                    x=series.index,
                    y=series.values,
                    mode="lines",
                    name=f"{symbol} [{ret:+.1f}%]",
                    line=dict(width=2.5),
                    hovertemplate="%{x|%b %d, %Y}<br><b>" + symbol + " (" + name + ")</b><br>Industry: " + industry + "<br>Performance: %{y:.2f} (Base 100)<extra></extra>"
                ))

    fig.update_layout(
        title={
            'text': f"<b>{title}</b><br><sup>{subtitle}</sup>",
            'y': 0.96, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'
        },
        xaxis_title="Date",
        yaxis_title="Indexed Performance (Base 100)",
        template="plotly_dark",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=11)
        ),
        margin=dict(l=45, r=45, t=110, b=45),
        height=600
    )

    return fig
