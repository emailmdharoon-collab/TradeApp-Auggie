# PTIP - Personal Trading Intelligence Platform

[![CI](https://github.com/emailmdharoon-collab/TradeApp-Auggie/actions/workflows/ci.yml/badge.svg)](https://github.com/emailmdharoon-collab/TradeApp-Auggie/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.50.0-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-Personal%20Use-lightgrey.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/emailmdharoon-collab/TradeApp-Auggie/graphs/commit-activity)
[![GitHub last commit](https://img.shields.io/github/last-commit/emailmdharoon-collab/TradeApp-Auggie.svg)](https://github.com/emailmdharoon-collab/TradeApp-Auggie/commits/main)
[![GitHub stars](https://img.shields.io/github/stars/emailmdharoon-collab/TradeApp-Auggie.svg?style=social&label=Star)](https://github.com/emailmdharoon-collab/TradeApp-Auggie)

## 🎯 Project Overview

**PTIP** is a local web-based trading application designed for personal use on Windows PC, focusing on Indian stock markets (NSE, BSE, MCX). This is the **Ultra-MVP** version implementing a single **Scalping Options** strategy.

### Ultra-MVP Features
- ✅ Single Strategy: Scalping Options (RSI + Moving Averages)
- ✅ Single Broker: Fyers API integration
- ✅ Historical Data: 3 months of 5-minute candles
- ✅ Streamlit Dashboard: Interactive web interface
- ✅ Backtesting: Historical performance analysis
- ✅ SQLite Database: Local data storage

---

## 📋 Project Structure

```
PTIP-bmad/
├── .env                    # API credentials (create from .env.template)
├── .env.template          # Template for environment variables
├── .gitignore             # Git ignore rules
├── config.py              # Configuration settings
├── app.py                 # Main Streamlit application (to be created)
├── README.md              # This file
├── PROGRESS.md            # Progress tracker
│
├── data/                  # Database storage
│   └── ptip.db           # SQLite database (auto-created)
│
├── modules/               # Core modules
│   ├── __init__.py       # Package initializer
│   ├── database.py       # Database operations
│   ├── data_fetcher.py   # Fyers API integration
│   ├── indicators.py     # Technical indicators
│   ├── strategy.py       # Scalping strategy
│   └── backtest.py       # Backtesting engine (to be created)
│
├── tests/                 # Test files
│   └── test_basic.py     # Basic tests (to be created)
│
└── logs/                  # Log files (auto-created)
    └── ptip.log
```

---

## 🚀 Getting Started

### Prerequisites
- Windows PC (Lenovo Yoga Pro 7 14IAH10 or similar)
- Python 3.11+ (3.12.0 installed)
- Fyers Trading Account with API access

### Installation

1. **Clone/Navigate to Project Directory**
   ```bash
   cd "C:\Users\haroo\OneDrive\Documents\My Projects\Dev\PTIP-bmad"
   ```

2. **Activate Virtual Environment**
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

3. **Verify Installation**
   ```bash
   python -c "import streamlit; import pandas; import fyers_apiv3; print('All imports successful!')"
   ```

4. **Configure API Credentials**
   - Copy `.env.template` to `.env`
   - Fill in your Fyers API credentials:
     ```
     FYERS_CLIENT_ID=your_client_id_here
     FYERS_SECRET_KEY=your_secret_key_here
     FYERS_REDIRECT_URI=http://localhost:8080
     ```

5. **Test Configuration**
   ```bash
   python config.py
   ```

---

## 📊 Usage

### Testing Individual Modules

**Test Database:**
```bash
python modules/database.py
```

**Test Indicators:**
```bash
python modules/indicators.py
```

**Test Strategy:**
```bash
python modules/strategy.py
```

### Running the Dashboard ✅
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run Streamlit dashboard
streamlit run app.py

# Dashboard will open at http://localhost:8501
```

**Dashboard Features:**
- 📊 Interactive candlestick charts
- 📈 Technical indicators (MA20, MA50, RSI)
- 🎯 BUY/SELL signals visualization
- 📅 Date range filtering
- 📋 Signal history table
- 💹 Real-time metrics

---

## 🔧 Configuration

All configuration is managed in `config.py`:

### Strategy Parameters
- **RSI Period:** 14
- **RSI Oversold:** 30
- **RSI Overbought:** 70
- **MA Short:** 20
- **MA Long:** 50

### Default Stocks
- NSE:RELIANCE-EQ
- NSE:TCS-EQ
- NSE:INFY-EQ
- NSE:HDFCBANK-EQ
- NSE:ICICIBANK-EQ

### Backtesting
- **Initial Capital:** ₹100,000
- **Position Size:** 10% of capital per trade

---

## 📈 Scalping Strategy Logic

### BUY Signal
- RSI < 30 (oversold condition)
- Price > MA20 (uptrend confirmation)
- Confidence score based on:
  - How oversold (lower RSI = higher confidence)
  - Distance above MA20
  - MA20 > MA50 (strong trend)

### SELL Signal
- RSI > 70 (overbought condition)
- Confidence score based on:
  - How overbought (higher RSI = higher confidence)
  - Price below MA20 (trend reversal)

### HOLD
- All other conditions

---

## 🗄️ Database Schema

### Tables

**stocks**
- symbol (PRIMARY KEY)
- name
- exchange
- added_date

**price_data**
- id (PRIMARY KEY)
- symbol (FOREIGN KEY)
- timestamp
- open, high, low, close, volume
- UNIQUE(symbol, timestamp)

**signals**
- id (PRIMARY KEY)
- symbol (FOREIGN KEY)
- strategy
- timestamp
- action (BUY/SELL/HOLD)
- price
- confidence
- executed

**trades**
- id (PRIMARY KEY)
- symbol (FOREIGN KEY)
- strategy
- entry_time, exit_time
- entry_price, exit_price
- quantity
- pnl
- status

---

## 🚀 Current Status

**Overall Progress:** 60% Complete | **Dashboard:** ✅ LIVE at http://localhost:8501

### ✅ Week 1: Setup & Data Fetching (COMPLETE)
- ✅ Environment setup (Python 3.12, 80+ packages)
- ✅ Fyers API authentication working
- ✅ Database setup (SQLite, 4 tables, 3.85 MB)
- ✅ Testing infrastructure (55 tests created)
- ✅ Historical data: **23,250 records** (5 stocks, 88 days, 5-min candles)
- ✅ Data quality: 100% valid (no NaN, no invalid OHLC)
- ✅ Indicators: All 7 working (RSI, MA20/50/200, EMA, MACD, BB, Stoch, ATR)
- ✅ Signals: **2,900+ generated** (4 BUY, 2,896 SELL)

### ✅ Week 3: Dashboard (COMPLETE - Skipped Week 2)
- ✅ Interactive Streamlit dashboard
- ✅ Candlestick charts with Plotly
- ✅ Technical indicators overlay (MA20, MA50, RSI)
- ✅ BUY/SELL signals visualization
- ✅ Metrics panel (price, change, signal counts)
- ✅ Signal history table
- ✅ Date range filtering
- ✅ Stock selector (5 stocks)

### ⏳ Week 4: Backtesting (NEXT)
- [ ] Backtest engine implementation
- [ ] P&L calculation
- [ ] Win rate and performance metrics
- [ ] Strategy optimization

### ⏳ Week 5-6: Testing & Refinement
- [ ] Strategy parameter tuning
- [ ] Dashboard enhancements
- [ ] Error handling improvements
- [ ] Final testing and documentation

---

## 🛠️ Tech Stack

- **Backend:** Python 3.12
- **Frontend:** Streamlit
- **Database:** SQLite
- **API:** Fyers API v3
- **Data Analysis:** Pandas, NumPy
- **Technical Analysis:** Custom indicators + TA library

---

## ⚠️ Important Notes

1. **Personal Use Only:** This application is for personal trading analysis only
2. **No Real-Time Trading:** Ultra-MVP focuses on historical analysis and backtesting
3. **Manual Execution:** Signals are recommendations; execution is manual
4. **Risk Disclaimer:** Trading involves risk. This is a learning/analysis tool.

---

## 📚 Next Steps (Choose One)

### Option 1: Strategy Tuning (Recommended)
Use the dashboard to visually tune strategy parameters:
- Adjust RSI thresholds (currently 30/70)
- Test different MA periods
- Add more confirmation signals
- **Estimated Time:** 1-2 hours

### Option 2: Backtesting (Week 4)
Build backtesting engine to calculate P&L:
- Simulate trades based on signals
- Calculate win rate, profit/loss
- Optimize parameters
- **Estimated Time:** 4-6 hours

### Option 3: Dashboard Enhancements
Add more features to dashboard:
- Volume chart
- More indicators (MACD, Bollinger Bands)
- Multi-timeframe view
- Export signals to CSV
- **Estimated Time:** 2-3 hours

---

## 🤝 Support

For issues or questions:
- Check `PROGRESS.md` for current status
- Review module documentation in code comments
- Test individual modules before integration

---

## 📄 License

Personal use only. Not for distribution.

---

**Version:** 0.1.0 (Ultra-MVP)  
**Last Updated:** 2025-09-30  
**Status:** Day 1 Complete - Environment Setup ✅

