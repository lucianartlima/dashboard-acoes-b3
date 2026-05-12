import yfinance as yf
import pandas as pd
import streamlit as st

TICKERS = {
    "Petrobras (PETR4)": "PETR4.SA",
    "Itaú (ITUB4)": "ITUB4.SA",
    "Vale (VALE3)": "VALE3.SA",
}

def _baixar_serie(ticker: str, inicio: str, fim: str, campo: str) -> pd.Series:
    try:
        df = yf.Ticker(ticker).history(start=inicio, end=fim, auto_adjust=True)
        if df.empty or campo not in df.columns:
            return pd.Series(dtype=float, name=ticker)
        serie = df[campo].rename(ticker)
        serie.index = pd.to_datetime(serie.index).tz_localize(None)
        return serie
    except Exception:
        return pd.Series(dtype=float, name=ticker)

@st.cache_data(ttl=3600)
def carregar_dados(tickers: tuple, inicio: str, fim: str) -> pd.DataFrame:
    series = [_baixar_serie(t, inicio, fim, "Close") for t in tickers]
    df = pd.concat(series, axis=1)
    df.columns.name = None
    return df

@st.cache_data(ttl=3600)
def carregar_volume(tickers: tuple, inicio: str, fim: str) -> pd.DataFrame:
    series = [_baixar_serie(t, inicio, fim, "Volume") for t in tickers]
    df = pd.concat(series, axis=1)
    df.columns.name = None
    return df

def calcular_performance(fechamento: pd.DataFrame) -> pd.DataFrame:
    primeiro_valido = fechamento.apply(lambda col: col.dropna().iloc[0] if not col.dropna().empty else None)
    performance = (fechamento / primeiro_valido - 1) * 100
    return performance

def metricas_resumo(fechamento: pd.DataFrame, nome_ticker: str) -> dict:
    col = fechamento[nome_ticker].dropna()
    if col.empty:
        return {}
    retorno = ((col.iloc[-1] / col.iloc[0]) - 1) * 100
    preco_atual = col.iloc[-1]
    preco_anterior = col.iloc[-2] if len(col) > 1 else col.iloc[0]
    variacao_dia = ((preco_atual / preco_anterior) - 1) * 100
    return {
        "preco_atual": preco_atual,
        "variacao_dia": variacao_dia,
        "retorno_ytd": retorno,
        "maximo": col.max(),
        "minimo": col.min(),
    }
