import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import plotly.graph_objects as go

# assuming `fig` is your dashboard
st.plotly_chart(fig, use_container_width=True)


# === Configuration ===
symbols = ["EURUSD", "USDJPY", "GBPUSD", "XAUUSD"]
timeframe = mt5.TIMEFRAME_D1
num_bars = 500
rolling_window = 30
sharpe_window = 60
confidence_level = 0.95

# === Risk Metric Functions ===
def rolling_sharpe(returns, window, risk_free_rate=0.0):
    mean_ret = returns.rolling(window).mean()
    std_ret = returns.rolling(window).std()
    sharpe = (mean_ret - risk_free_rate) / std_ret * np.sqrt(252)
    return sharpe

def historical_var(returns, confidence=confidence_level):
    return returns.quantile(1 - confidence)

def historical_cvar(returns, confidence=confidence_level):
    var = historical_var(returns, confidence)
    return returns[returns <= var].mean()

# === Data Fetch + Processing ===
def fetch_and_calc(symbol):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)
    if rates is None:
        print(f"❌ Failed to get rates for {symbol}")
        return None
    df = pd.DataFrame(rates)
    df['Date'] = pd.to_datetime(df['time'], unit='s')
    df.rename(columns={'close': 'Price'}, inplace=True)
    df = df[['Date', 'Price']]
    df.sort_values('Date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    df['DailyReturn'] = df['Price'].pct_change()
    df.dropna(inplace=True)

    df['CumulativeReturn'] = (1 + df['DailyReturn']).cumprod() - 1
    df['CumMax'] = df['CumulativeReturn'].cummax()
    df['Drawdown'] = df['CumulativeReturn'] - df['CumMax']
    df['RollingVolatility'] = df['DailyReturn'].rolling(rolling_window).std() * np.sqrt(252)
    df['RollingSharpe'] = rolling_sharpe(df['DailyReturn'], sharpe_window)
    df['VaR_95'] = df['DailyReturn'].rolling(rolling_window).apply(lambda x: historical_var(x, confidence_level))
    df['CVaR_95'] = df['DailyReturn'].rolling(rolling_window).apply(lambda x: historical_cvar(x, confidence_level))

    return df

# === Initialize MT5 ===
if not mt5.initialize():
    print("🚫 MT5 initialization failed. Error code =", mt5.last_error())
    quit()

# === Fetch Data ===
dfs = {}
for sym in symbols:
    dfs[sym] = fetch_and_calc(sym)

mt5.shutdown()

# === Build Plotly Dashboard ===
fig = go.Figure()

# Visibility mask for dropdown toggle
visibility = []
for i, sym in enumerate(symbols):
    is_visible = (i == 0)  # Show only first symbol
    for _ in range(6):
        visibility.append(is_visible)

# Add data traces
for i, sym in enumerate(symbols):
    df = dfs[sym]
    if df is None:
        for _ in range(6):
            fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name=f"{sym}", visible=False))
        continue

    fig.add_trace(go.Scatter(x=df['Date'], y=df['CumulativeReturn'], mode='lines', name=f"{sym} Cumulative Return", visible=visibility[i*6+0]))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Drawdown'], mode='lines', name=f"{sym} Drawdown", visible=visibility[i*6+1]))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['RollingVolatility'], mode='lines', name=f"{sym} Rolling Volatility", visible=visibility[i*6+2]))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['RollingSharpe'], mode='lines', name=f"{sym} Rolling Sharpe", visible=visibility[i*6+3]))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['VaR_95'], mode='lines', name=f"{sym} VaR 95%", visible=visibility[i*6+4]))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['CVaR_95'], mode='lines', name=f"{sym} CVaR 95%", line=dict(dash='dash'), visible=visibility[i*6+5]))

# === Dropdown Buttons ===
buttons = []
for i, sym in enumerate(symbols):
    vis = [False] * len(symbols) * 6
    for j in range(6):
        vis[i*6 + j] = True
    buttons.append(dict(
        label=sym,
        method="update",
        args=[{"visible": vis},
              {"title": f"📊 Risk Metrics Dashboard for {sym}"}]
    ))

fig.update_layout(
    title="📈 Risk Metrics Dashboard",
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        x=0.1,
        y=1.15,
        xanchor='left',
        yanchor='top'
    )],
    legend_title="Metric",
    height=700,
    width=1100,
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="Value"
)

fig.show()

# assuming `fig` is your dashboard
st.plotly_chart(fig, use_container_width=True)
