import plotly.graph_objects as go
import pandas as pd

CORES = {
    "PETR4.SA": "#009C3B",
    "ITUB4.SA": "#003087",
    "VALE3.SA": "#FF6B00",
}

NOMES = {
    "PETR4.SA": "Petrobras (PETR4)",
    "ITUB4.SA": "Itaú (ITUB4)",
    "VALE3.SA": "Vale (VALE3)",
}


def grafico_preco(fechamento: pd.DataFrame, tickers_visiveis: list[str]) -> go.Figure:
    fig = go.Figure()
    for ticker in tickers_visiveis:
        if ticker not in fechamento.columns:
            continue
        fig.add_trace(go.Scatter(
            x=fechamento.index,
            y=fechamento[ticker],
            name=NOMES.get(ticker, ticker),
            line=dict(color=CORES.get(ticker, None), width=2),
            hovertemplate="%{x|%d/%m/%Y}<br>R$ %{y:.2f}<extra>" + NOMES.get(ticker, ticker) + "</extra>",
        ))
    fig.update_layout(
        title="Preço de Fechamento (R$)",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white",
        height=420,
    )
    return fig


def grafico_performance(performance: pd.DataFrame, tickers_visiveis: list[str]) -> go.Figure:
    fig = go.Figure()
    for ticker in tickers_visiveis:
        if ticker not in performance.columns:
            continue
        fig.add_trace(go.Scatter(
            x=performance.index,
            y=performance[ticker],
            name=NOMES.get(ticker, ticker),
            line=dict(color=CORES.get(ticker, None), width=2),
            hovertemplate="%{x|%d/%m/%Y}<br>%{y:+.2f}%<extra>" + NOMES.get(ticker, ticker) + "</extra>",
        ))
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    fig.update_layout(
        title="Performance Acumulada em 2025 (%)",
        xaxis_title="Data",
        yaxis_title="Retorno (%)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white",
        height=420,
    )
    return fig


def grafico_volume(volume: pd.DataFrame, tickers_visiveis: list[str]) -> go.Figure:
    fig = go.Figure()
    for ticker in tickers_visiveis:
        if ticker not in volume.columns:
            continue
        fig.add_trace(go.Bar(
            x=volume.index,
            y=volume[ticker],
            name=NOMES.get(ticker, ticker),
            marker_color=CORES.get(ticker, None),
            opacity=0.75,
            hovertemplate="%{x|%d/%m/%Y}<br>Vol: %{y:,.0f}<extra>" + NOMES.get(ticker, ticker) + "</extra>",
        ))
    fig.update_layout(
        title="Volume Negociado (quantidade de ações)",
        xaxis_title="Data",
        yaxis_title="Volume",
        barmode="group",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white",
        height=420,
    )
    return fig
