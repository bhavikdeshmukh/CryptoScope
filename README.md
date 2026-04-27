# 🔮 CryptoScope — End-to-End Cryptocurrency Market Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?style=flat-square&logo=pandas)
![Scikit-Learn](https://img.shields.io/badge/ScikitLearn-1.3+-orange?style=flat-square&logo=scikit-learn)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=flat-square&logo=streamlit)
![XGBoost](https://img.shields.io/badge/XGBoost-Model-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

> **Capstone Project — Data Science PGC | Internshala Trainings**  
> A complete end-to-end data science pipeline: from live web scraping to ML-powered market signal prediction and interactive dashboard.

---

## 📌 Project Overview

CryptoScope is a **production-grade data science project** that scrapes live cryptocurrency data from multiple public APIs, cleans and engineers features, performs deep exploratory analysis, builds and compares multiple machine learning models to predict market signals (Bullish/Bearish/Strong Bear), and presents findings through an interactive Streamlit dashboard.

### 🎯 Business Problem

> _"Can we predict whether a cryptocurrency is currently in a Bullish or Bearish market signal using real-time market data — and present those insights through an interactive intelligence platform?"_

The cryptocurrency market moves faster than any human can manually monitor. With 1000+ coins trading simultaneously, investors and analysts need automated signal detection to make data-driven decisions. CryptoScope solves this by building a complete ML pipeline that:

- Collects real-time data from CoinGecko API and Fear & Greed Index
- Engineers meaningful financial features from raw market data
- Predicts market signals with 4 competing ML models
- Visualizes everything in an interactive, filterable dashboard

---

## 📊 Dataset Summary

| Property            | Detail                                            |
| ------------------- | ------------------------------------------------- |
| **Total Records**   | 1,000 cryptocurrency coins                        |
| **Total Features**  | 27 columns (raw) → 36 columns (after engineering) |
| **Data Source**     | CoinGecko API + Alternative.me Fear & Greed Index |
| **Scrape Date**     | April 27, 2026                                    |
| **Price Range**     | $0.0000000004 to $78,291 (Bitcoin)                |
| **Target Variable** | `market_signal` — Bullish / Bearish / Strong Bear |

### Target Class Distribution

| Signal         | Count | Percentage |
| -------------- | ----- | ---------- |
| 🟢 Bullish     | 673   | 67.3%      |
| 🔴 Bearish     | 283   | 28.3%      |
| ⚫ Strong Bear | 44    | 4.4%       |

### Top 5 Coins by Market Cap

| Rank | Coin           | Price (USD) |
| ---- | -------------- | ----------- |
| 1    | Bitcoin (BTC)  | $78,288.00  |
| 2    | Ethereum (ETH) | $2,367.93   |
| 3    | Tether (USDT)  | $1.00       |
| 4    | XRP            | $1.43       |
| 5    | BNB            | $635.60     |

### Dataset Columns

| Column                 | Description                             |
| ---------------------- | --------------------------------------- |
| `coin_id`              | Unique CoinGecko identifier             |
| `symbol`               | Trading symbol (e.g., BTC, ETH)         |
| `name`                 | Full coin name                          |
| `price_usd`            | Current price in USD                    |
| `market_cap_usd`       | Total market capitalization             |
| `market_cap_rank`      | Global rank by market cap               |
| `volume_24h_usd`       | 24-hour trading volume                  |
| `high_24h_usd`         | 24-hour high price                      |
| `low_24h_usd`          | 24-hour low price                       |
| `price_change_pct_24h` | % price change in 24 hours              |
| `price_change_pct_7d`  | % price change in 7 days                |
| `price_change_pct_30d` | % price change in 30 days               |
| `circulating_supply`   | Coins currently in circulation          |
| `total_supply`         | Maximum coin supply                     |
| `all_time_high_usd`    | All-time highest price                  |
| `pct_below_ath`        | % below all-time high                   |
| `volatility_24h_pct`   | 24-hour price volatility %              |
| `fear_greed_score`     | Market Fear & Greed Index (0-100)       |
| `fear_greed_label`     | Fear/Neutral/Greed label                |
| `news_mentions`        | Recent news mention count               |
| `market_signal`        | **Target: Bullish/Bearish/Strong Bear** |
| `volatility_category`  | Low/Medium/High/Extreme                 |

---

## 🗂️ Project Structure

```
CryptoScope/
│
├── 📄 README.md                          ← You are here
│
├── 📂 data/
│   └── cryptoscope_master.csv            ← Scraped dataset (1000 coins, 27 features)
│
├── 📂 code/
│   ├── ganeshdata_collection.ipynb       ← FILE 1: Web scraping script
│   └── cryptoscope_analysis.ipynb        ← FILE 2: Cleaning + EDA + ML models
│
├── 📂 dashboard/
│   └── dashboard.py                      ← Streamlit interactive dashboard
│
├── 📂 charts/
│   ├── chart01_price_distribution.png
│   ├── chart02_market_signal_pie.png
│   ├── chart03_volatility_category.png
│   ├── chart04_price_change_histogram.png
│   ├── chart05_market_cap_vs_volume.png
│   ├── chart06_top20_coins_mcap.png
│   ├── chart07_volatility_vs_pchange.png
│   ├── chart08_ath_below_heatmap.png
│   ├── chart09_7d_vs_30d_scatter.png
│   ├── chart10_correlation_heatmap.png
│   ├── chart11_volatility_vs_signal.png
│   ├── chart12_risktier_vs_pchange.png
│   ├── chart13_volume_mcap_ratio.png
│   ├── chart14_supply_utilization.png
│   └── chart15_feature_importance.png
│
└── 📄 CryptoScope_Report.pdf             ← Final presentation/report
```

---

## ⚙️ Project Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   TASK 1        │     │   TASK 2        │     │   TASK 3        │
│  Web Scraping   │────▶│ Data Cleaning   │────▶│      EDA        │
│  100 Marks      │     │   50 Marks      │     │   50 Marks      │
│                 │     │                 │     │                 │
│ CoinGecko API   │     │ Missing values  │     │ 15 charts       │
│ Fear&Greed API  │     │ Feature engg.   │     │ Statistical     │
│ 1000 records    │     │ Log transforms  │     │ summaries       │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                          │
┌─────────────────┐     ┌─────────────────┐     ┌────────▼────────┐
│   TASK 6        │     │   TASK 5        │     │   TASK 4        │
│ Final Report    │     │  Dashboard      │     │ Model Building  │
│   50 Marks      │◀────│   50 Marks      │◀────│  100 Marks      │
│                 │     │                 │     │                 │
│ PDF Report      │     │ Streamlit App   │     │ 4 ML Models     │
│ Gamma PPT       │     │ 4 pages         │     │ SMOTE balancing │
│ Recommendations │     │ KPI cards       │     │ ROC-AUC eval    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## 🕷️ Task 1 — Web Scraping (100 Marks)

### Sources Scraped

| Source         | Data Collected                         | Method                |
| -------------- | -------------------------------------- | --------------------- |
| CoinGecko API  | Price, Market Cap, Volume, Supply, ATH | REST API + `requests` |
| Alternative.me | Fear & Greed Index score and label     | REST API + `requests` |
| Custom Logic   | News mentions, Volatility category     | Engineered            |

### Scraping Features

- ✅ 1,000 clean records collected
- ✅ Multiple pages/API calls handled
- ✅ Rate limiting with polite delays
- ✅ Error handling for failed requests
- ✅ Automatic CSV export
- ✅ Timestamp recorded at scrape time
- ✅ No login required — fully public API

### How to Run the Scraper

```bash
# Install dependencies
pip install requests pandas

# Run scraper
jupyter nbconvert --to script ganeshdata_collection.ipynb
python ganeshdata_collection.py

# Or run directly in Jupyter
jupyter notebook ganeshdata_collection.ipynb
```

---

## 🧹 Task 2 — Data Cleaning & Preprocessing (50 Marks)

### Problems Found & Fixed

| Problem            | Detail                           | Fix Applied                          |
| ------------------ | -------------------------------- | ------------------------------------ |
| Missing values     | 15 nulls in 24h price columns    | Filled with 0 (no-change assumption) |
| Missing 30d change | 21 nulls in price_change_pct_30d | Filled with median                   |
| Missing supply     | 1 null in total_supply           | Filled with circulating_supply       |
| Raw timestamps     | String format dates              | Parsed to datetime64                 |
| Class imbalance    | Bullish 67% vs Strong Bear 4%    | SMOTE oversampling                   |

### Feature Engineering — 9 New Columns Created

```python
price_to_ath_ratio    = price_usd / all_time_high_usd
volume_to_mcap_ratio  = volume_24h_usd / market_cap_usd
supply_utilization    = circulating_supply / total_supply
momentum_score        = (price_change_pct_24h + price_change_pct_7d) / 2
log_price             = log(1 + price_usd)
log_volume            = log(1 + volume_24h_usd)
log_market_cap        = log(1 + market_cap_usd)
is_stablecoin         = volatility_24h_pct < 0.5
risk_tier             = cut(market_cap_rank, [Mega/Large/Mid/Small])
```

---

## 📈 Task 3 — Exploratory Data Analysis (50 Marks)

### Key Findings

| Finding                     | Insight                                     |
| --------------------------- | ------------------------------------------- |
| 67.3% Bullish signal        | Market trending positive at scrape time     |
| Bitcoin at $78,288          | 37.9% below all-time high of $126,080       |
| 47.7% Low volatility        | Most coins are relatively stable            |
| Fear & Greed = 47 (Neutral) | Market neither fearful nor greedy           |
| Avg 30d change = +603%      | Driven by small-cap outliers                |
| Volume/MCap ratio           | Higher for Bearish coins — selling pressure |

### 15 Visualizations Covering

- Price distributions and market cap analysis
- Signal and volatility category breakdowns
- Momentum and trend analysis (24h, 7d, 30d)
- ATH distance by risk tier
- Supply utilization patterns
- Full correlation heatmap
- Feature importance from ML model

---

## 🤖 Task 4 — Model Building & Evaluation (100 Marks)

### Models Built & Compared

| Model               | Type                | Purpose                  |
| ------------------- | ------------------- | ------------------------ |
| Logistic Regression | Baseline Classifier | Interpretable benchmark  |
| Random Forest       | Ensemble Classifier | Main production model    |
| XGBoost             | Gradient Boosting   | Best performance model   |
| K-Means Clustering  | Unsupervised        | Coin behavioral grouping |

### Class Imbalance Handling

- Applied **SMOTE** (Synthetic Minority Oversampling Technique)
- Before: Bullish 673 / Bearish 283 / Strong Bear 44
- After: Balanced classes for fair model training

### Evaluation Metrics Used

- Accuracy, Precision, Recall, F1-Score
- ROC-AUC curve (multi-class OvR)
- Confusion Matrix
- Feature Importance ranking
- Cross-validation (5-fold)

### Top Predictive Features

1. `price_change_pct_24h` — strongest signal
2. `momentum_score` — 24h + 7d combined
3. `volatility_24h_pct` — risk indicator
4. `volume_to_mcap_ratio` — liquidity signal
5. `pct_below_ath` — distance from peak

---

## 📱 Task 5 — Interactive Dashboard (50 Marks)

### Built With: Streamlit + Plotly

### Dashboard Pages

| Page               | Content                                                            |
| ------------------ | ------------------------------------------------------------------ |
| 🏠 Market Overview | KPI cards — Total coins, Avg change, Bull/Bear ratio, Fear & Greed |
| 📊 EDA Explorer    | Interactive charts with volatility/signal/risk tier filters        |
| 🔍 Coin Lookup     | Search any coin → full metrics display                             |
| 🤖 ML Predictor    | Enter features → get Bullish/Bearish prediction                    |

### KPIs Included

- Total coins analyzed
- Average 24h price change
- Bullish vs Bearish ratio
- Fear & Greed Index score
- Top performing coin (24h)
- Most volatile coin

### How to Run Dashboard

```bash
# Install Streamlit
pip install streamlit plotly

# Launch dashboard
streamlit run dashboard.py

# Opens at: http://localhost:8501
```

---

## 🛠️ Installation & Setup

### Prerequisites

```bash
Python 3.10+
```

### Install All Dependencies

```bash
pip install pandas numpy matplotlib seaborn
pip install scikit-learn xgboost imbalanced-learn
pip install requests beautifulsoup4
pip install streamlit plotly
pip install jupyter notebook
```

### Or Install From Requirements

```bash
pip install -r requirements.txt
```

### Run Complete Analysis

```bash
# Step 1 — Run scraper (if re-scraping)
jupyter notebook ganeshdata_collection.ipynb

# Step 2 — Run analysis
jupyter notebook cryptoscope_analysis.ipynb

# Step 3 — Launch dashboard
streamlit run dashboard/dashboard.py
```

---

## 📦 Deliverables Summary

| Deliverable            | File                          | Status          |
| ---------------------- | ----------------------------- | --------------- |
| Web Scraping Script    | `ganeshdata_collection.ipynb` | ✅ Complete     |
| Analysis + ML Notebook | `cryptoscope_analysis.ipynb`  | ✅ Complete     |
| Clean Dataset          | `cryptoscope_master.csv`      | ✅ 1000 records |
| Interactive Dashboard  | `dashboard.py`                | ✅ 4 pages      |
| 15 Visualizations      | `/charts/` folder             | ✅ Complete     |
| Final Report PDF       | `CryptoScope_Report.pdf`      | ✅ Complete     |
| Video Presentation     | Google Drive Link (in PDF)    | ✅ 5+ minutes   |

---

## 💡 Key Business Recommendations

**1. Use Momentum Score for Signal Detection**
The combination of 24h + 7d price change (momentum_score) is the single strongest predictor of market signal. Real-time monitoring of this metric can give 2-3 day advance warning of signal changes.

**2. Volatility-Adjusted Portfolio Strategy**
47.7% of coins are Low volatility — ideal for conservative portfolios. The 8.2% Extreme volatility coins (82 coins) should be treated as speculative positions only.

**3. Volume/Market Cap Ratio as Liquidity Alert**
High volume-to-market-cap ratios consistently correlate with Bearish signals — indicating selling pressure. This ratio should be monitored as an early warning indicator.

**4. ATH Distance as Entry Indicator**
Average coin is 69.4% below its all-time high. Coins within 20% of ATH show disproportionately higher Bullish signals — suggesting momentum continuation near highs.

**5. Small-Cap Risk Management**
Rank 200-1000 (Small cap) coins show extreme 30-day volatility (avg +603% driven by outliers). Position sizing should be inversely proportional to market cap rank for this tier.

---

## 👨‍💻 About This Project

| Property         | Detail                                                               |
| ---------------- | -------------------------------------------------------------------- |
| **Project Type** | Capstone — Data Science PGC                                          |
| **Institution**  | Internshala Trainings                                                |
| **Domain**       | Cryptocurrency / FinTech                                             |
| **Techniques**   | Web Scraping, EDA, Random Forest, XGBoost, K-Means, SMOTE, Streamlit |
| **Total Marks**  | 400                                                                  |
| **Dataset**      | Self-scraped — Live CoinGecko API                                    |

---

## 📄 License

This project was created for educational purposes as part of the Internshala Data Science PGC Capstone Project. Dataset scraped from publicly available CoinGecko API and Alternative.me API — both allow public access without authentication.

---

_Built with 🔥 by a Data Science PGC Student — from raw API calls to production-grade ML pipeline_
