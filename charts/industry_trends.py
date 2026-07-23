import pandas as pd
import plotly.graph_objects as go
from typing import Dict, List, Any

from data.normalization import normalize_to_base_100
from config.settings import INDUSTRY_UNIVERSE

def create_top_5_industry_trends_chart(
    top_5_industries: List[Dict[str, Any]],
    historical_data: Dict[str, pd.DataFrame]
) -> go.Figure:
    """
    Creates Chart 1: 6-Month Trend: Top 5 Gainer Industries (Base 100 Normalized Line Chart).
    Consistent horizontal center-aligned legend format.
    """
    fig = go.Figure()

    if not top_5_industries:
        fig.update_layout(
            title="6-Month Trend: Top 5 Gainer Industries (No Data Available)",
            template="plotly_dark",
            height=600
        )
        return fig

    for ind in top_5_industries:
        ind_name = ind["industry_name"]
        companies = INDUSTRY_UNIVERSE.get(ind_name, [])
        ind_tickers = [c["symbol"] for c in companies]

        # Gather constituent data & normalize
        ind_df_dict = {t: historical_data[t] for t in ind_tickers if t in historical_data}
        normalized_df = normalize_to_base_100(ind_df_dict)

        if not normalized_df.empty:
            # Aggregate average across constituent companies for each trading date
            industry_avg_series = normalized_df.mean(axis=1)

            fig.add_trace(go.Scatter(
                x=industry_avg_series.index,
                y=industry_avg_series.values,
                mode="lines",
                name=f"{ind_name} [{ind['percentage_return_6m']:+.1f}%]",
                line=dict(width=3.0),
                hovertemplate="%{x|%b %d, %Y}<br><b>" + ind_name + "</b>: %{y:.2f} (Base 100)<extra></extra>"
            ))

    fig.update_layout(
        title={
            'text': "<b>6-Month Trend: Top 5 Gainer Industries</b> (Indexed to 100)",
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
        margin=dict(l=45, r=45, t=100, b=45),
        height=600
    )

    return fig
