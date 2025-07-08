# 🧮 Multi-Symbol Risk Dashboard with MT5 Data and Plotly

This Jupyter notebook fetches historical Forex and commodities data using the MetaTrader5 API and computes multiple risk metrics with beautiful Plotly visualizations.

## 📊 Visualized Metrics

- 📈 **Cumulative Returns** (line chart)
- 📉 **Drawdown** (area chart)
- 📏 **Rolling Volatility** (line chart)
- 📊 **Rolling Sharpe Ratio** (bar chart)
- ⚠️ **Value at Risk (VaR 95%)** (bar chart)
- 🔥 **Conditional Value at Risk (CVaR 95%)** (bar chart)

Supports **multiple symbols** with an interactive dropdown selector.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://github.com/yadavvinay77/risk_dashboard/blob/main/risk_dashboard.ipynb)


---

## 🚀 How to Run

1. 📥 Install required packages:

```bash
pip install MetaTrader5 pandas numpy plotly
```

2. 📡 Open MetaTrader5 on your machine and ensure it's running.

3. ▶️ Run `multi_symbol_risk_dashboard.ipynb` in **Jupyter Notebook**, **JupyterLab**, or **VS Code**.

---

## 🖼️ Preview

> Add a screenshot or GIF of your notebook's output here (optional).

---

## 📁 Repository Contents

```
multi_symbol_risk_dashboard.ipynb
README.md
.gitignore
```

---

## 🛡️ License

Licensed under the MIT License. See `LICENSE` file for details.

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/foo`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/foo`)
5. Create a new Pull Request