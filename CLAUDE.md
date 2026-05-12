# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

- **Python:** 3.14, managed by `uv` — use `uv pip` to install packages, never `pip` directly.
- **Virtual env:** `.venv/` in the project root. Always activate before running commands.

## Commands

```powershell
# Activate venv (PowerShell)
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Run the app
streamlit run app.py --browser.gatherUsageStats false

# Run headless (no browser auto-open)
streamlit run app.py --server.headless true --browser.gatherUsageStats false
```

## GitHub Repository

The project is hosted at **https://github.com/lucianartlima/dashboard-acoes-b3**.

A Claude Code Stop hook automatically commits and pushes all changes to GitHub at the end of every session. The hook script is at `.claude/auto-push.sh`.

To push manually at any time:
```powershell
git add -A
git commit -m "your message"
git push
```

`gh` CLI is installed via Scoop at `$env:USERPROFILE\scoop\shims\gh`. Git operations use HTTPS with the stored token.

## Architecture

The app is a Streamlit dashboard with three layers:

**`data.py`** — data fetching and computation  
- `TICKERS` dict maps display name → Yahoo Finance ticker symbol (`PETR4.SA`, `ITUB4.SA`, `VALE3.SA`)
- `carregar_dados` / `carregar_volume` are `@st.cache_data`-decorated and accept `tuple` (not `list`) to ensure correct cache hashing
- Each ticker is downloaded individually via `yf.Ticker().history()` — batch `yf.download()` was avoided because it returns a MultiIndex DataFrame with a named column axis (`name="Ticker"`) that caused Streamlit's cache layer to silently drop tickers

**`charts.py`** — Plotly figure builders  
- Three functions: `grafico_preco`, `grafico_performance`, `grafico_volume`
- Each receives the full DataFrame and a list of visible tickers; missing tickers are silently skipped
- Colors and display names are defined in `CORES` and `NOMES` dicts keyed by ticker symbol

**`app.py`** — Streamlit UI  
- Sidebar controls period and per-ticker visibility
- Always fetches all tickers; filters are applied at render time
- Shows a success/warning banner after load indicating which tickers have data
- `nome_para_ticker` (reverse of `TICKERS`) is used throughout for display labels
