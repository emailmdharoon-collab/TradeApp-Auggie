# PTIP - Personal Trading Intelligence Platform

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

### Running the Application (Coming Soon)
```bash
streamlit run app.py
```

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

## 📝 Development Timeline

### Week 1: Setup & Data Fetching (Days 1-7)
- ✅ Day 1: Environment setup
- ⏳ Day 2: Fyers authentication
- ⏳ Day 3-4: Database setup
- ⏳ Day 5-7: Data fetching

### Week 2: Indicators & Strategy (Days 8-14)
- ⏳ Day 8-10: Technical indicators
- ⏳ Day 11-14: Strategy implementation

### Week 3: Dashboard (Days 15-21)
- ⏳ Streamlit UI development

### Week 4: Backtesting (Days 22-28)
- ⏳ Backtest engine
- ⏳ Performance metrics

### Week 5-6: Testing & Refinement (Days 29-42)
- ⏳ Testing and optimization
- ⏳ Documentation

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

## 📚 Next Steps

1. ✅ Complete Day 1: Environment Setup
2. ⏳ Day 2: Configure Fyers API credentials
3. ⏳ Day 3: Test database operations
4. ⏳ Day 4: Fetch historical data
5. ⏳ Day 5: Implement strategy
6. ⏳ Day 6: Build dashboard

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

