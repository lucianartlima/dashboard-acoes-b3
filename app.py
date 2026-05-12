import streamlit as st
import pandas as pd
from datetime import date

from data import TICKERS, carregar_dados, carregar_volume, calcular_performance, metricas_resumo
from charts import grafico_preco, grafico_performance, grafico_volume

st.set_page_config(
    page_title="Cotacoes B3 2025",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Dashboard de Ações B3 — 2025")
st.caption("Acompanhe a performance da Petrobras, Itaú e Vale ao longo de 2025.")

# --- Sidebar ---
with st.sidebar:
    st.header("Filtros")

    data_inicio = st.date_input(
        "Data início",
        value=date(2025, 1, 2),
        min_value=date(2025, 1, 2),
        max_value=date.today(),
    )
    data_fim = st.date_input(
        "Data fim",
        value=date.today(),
        min_value=date(2025, 1, 2),
        max_value=date.today(),
    )

    st.divider()
    st.subheader("Ações visíveis")
    acoes_selecionadas = []
    for nome, ticker in TICKERS.items():
        if st.checkbox(nome, value=True):
            acoes_selecionadas.append(ticker)

    st.divider()
    st.info("Dados fornecidos pelo Yahoo Finance via yfinance.")

if data_inicio >= data_fim:
    st.error("A data de início deve ser anterior à data fim.")
    st.stop()

if not acoes_selecionadas:
    st.warning("Selecione ao menos uma ação no painel lateral.")
    st.stop()

# --- Carrega dados ---
todos_tickers = tuple(TICKERS.values())
inicio_str = data_inicio.strftime("%Y-%m-%d")
fim_str = data_fim.strftime("%Y-%m-%d")

with st.spinner("Buscando dados..."):
    fechamento = carregar_dados(todos_tickers, inicio_str, fim_str)
    volume = carregar_volume(todos_tickers, inicio_str, fim_str)

if fechamento.empty:
    st.error("Não foi possível obter dados para o período selecionado.")
    st.stop()

# Aviso de disponibilidade por ação
tickers_sem_dados = [t for t in todos_tickers if t not in fechamento.columns or fechamento[t].dropna().empty]
tickers_com_dados = [t for t in todos_tickers if t not in tickers_sem_dados]
nome_para_ticker = {v: k for k, v in TICKERS.items()}

if tickers_sem_dados:
    nomes_faltando = ", ".join(nome_para_ticker.get(t, t) for t in tickers_sem_dados)
    st.warning(
        f"Não foi possível carregar dados para: **{nomes_faltando}**. "
        "Verifique sua conexão ou tente novamente em instantes."
    )
else:
    nomes_ok = " | ".join(nome_para_ticker.get(t, t) for t in tickers_com_dados)
    st.success(f"Dados carregados com sucesso: {nomes_ok}")

performance = calcular_performance(fechamento)

# --- Métricas ---
st.subheader("Resumo do Período")
colunas = st.columns(len(acoes_selecionadas))

for i, ticker in enumerate(acoes_selecionadas):
    m = metricas_resumo(fechamento, ticker)
    if not m:
        continue
    with colunas[i]:
        st.metric(
            label=nome_para_ticker.get(ticker, ticker),
            value=f"R$ {m['preco_atual']:.2f}",
            delta=f"{m['variacao_dia']:+.2f}% no dia",
        )
        st.write(f"**Retorno YTD:** {m['retorno_ytd']:+.2f}%")
        st.write(f"**Máximo:** R$ {m['maximo']:.2f}")
        st.write(f"**Mínimo:** R$ {m['minimo']:.2f}")

st.divider()

# --- Gráficos ---
st.subheader("Preço de Fechamento")
st.plotly_chart(grafico_preco(fechamento, acoes_selecionadas), use_container_width=True)

st.subheader("Performance Acumulada (%)")
st.plotly_chart(grafico_performance(performance, acoes_selecionadas), use_container_width=True)

st.subheader("Volume Negociado")
st.plotly_chart(grafico_volume(volume, acoes_selecionadas), use_container_width=True)

st.divider()

# --- Download CSV ---
st.subheader("Download dos Dados")
df_export = fechamento[acoes_selecionadas].copy()
df_export.columns = [nome_para_ticker.get(t, t) for t in df_export.columns]
df_export.index.name = "Data"
csv = df_export.to_csv().encode("utf-8")
st.download_button(
    label="Baixar dados em CSV",
    data=csv,
    file_name="acoes_2025.csv",
    mime="text/csv",
)
