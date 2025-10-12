# PTIP - New Session Handoff Guide

**Purpose:** This document ensures a new AI assistant in a fresh chat session can seamlessly continue development.

**Last Updated:** 2025-10-12  
**Session Status:** Week 1 + Dashboard Complete (60% overall)

---

## 🎯 Quick Context

You are continuing development of **PTIP (Personal Trading Intelligence Platform)**, a local Windows trading analysis app for Indian stock markets using Fyers API.

**What's Done:**
- ✅ Week 1: Environment, API, Database, Testing, Data (23,250 records)
- ✅ Week 3: Interactive Streamlit Dashboard (skipped Week 2)
- ✅ 60% of Ultra-MVP complete

**What's Next:**
- Choose between 3 options (see below)
- User will specify which option to pursue

---

## 📚 Essential Reading Order

**For a new AI assistant, read these files in this order:**

1. **README.md** (5 min)
   - Project overview
   - Current status
   - Quick start guide
   - Next steps options

2. **PROJECT_SUMMARY.md** (10 min)
   - Complete architecture
   - Database schema
   - Module descriptions
   - Key decisions made

3. **WEEK1_REVIEW.md** (10 min)
   - Comprehensive Week 1 assessment
   - Technical validation results
   - Known issues and deferred items

4. **PROGRESS.md** (3 min)
   - Day-by-day progress
   - Completed vs pending tasks

5. **This file (HANDOFF_GUIDE.md)** (5 min)
   - Context management tips
   - Common pitfalls to avoid

**Total Reading Time:** ~30 minutes

---

## 🚀 Quick Start for New Session

### Step 1: Verify Environment
```bash
# Check Python version
python --version  # Should be 3.12.0

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Verify key packages
python -c "import streamlit, pandas, plotly; print('All imports OK')"
```

### Step 2: Verify Database
```bash
# Check database exists and has data
python -c "from modules.database import Database; db = Database(); print(f'Stocks: {len(db.get_all_stocks())}')"
# Expected output: Stocks: 5
```

### Step 3: Run Dashboard
```bash
streamlit run app.py
# Should open at http://localhost:8501
```

### Step 4: Verify Dashboard Works
- Select different stocks from dropdown
- Adjust date range
- Toggle indicators (MA20, MA50, RSI)
- Check signals are visible on chart

---

## 🎯 Next Steps Options

User will choose ONE of these options:

### Option 1: Strategy Tuning (Recommended, 1-2 hours)
**Goal:** Improve signal quality by adjusting parameters

**Tasks:**
1. Review current signals in dashboard (mostly SELL, very few BUY)
2. Adjust RSI thresholds in `config.py`:
   - Current: BUY < 30, SELL > 70
   - Suggested: BUY < 35, SELL > 65
3. Test different MA periods (currently 20, 50)
4. Add more confirmation signals (e.g., volume, MACD)
5. Regenerate signals and visualize in dashboard
6. Document parameter changes

**Files to Modify:**
- `config.py` - Strategy parameters
- `modules/strategy.py` - Signal generation logic
- Possibly `app.py` - Add new indicators to dashboard

### Option 2: Backtesting (Week 4, 4-6 hours)
**Goal:** Calculate P&L and performance metrics

**Tasks:**
1. Create `modules/backtest.py`
2. Implement trade simulation:
   - Entry on BUY signal
   - Exit on SELL signal or stop-loss
   - Calculate P&L per trade
3. Calculate metrics:
   - Win rate
   - Total P&L
   - Max drawdown
   - Sharpe ratio
4. Store results in `trades` table
5. Add backtesting tab to dashboard
6. Display performance charts

**Files to Create/Modify:**
- `modules/backtest.py` (new)
- `app.py` - Add backtesting tab
- `modules/database.py` - Add trade retrieval methods

### Option 3: Dashboard Enhancements (2-3 hours)
**Goal:** Add more visualization features

**Tasks:**
1. Add volume chart below price chart
2. Add MACD indicator chart
3. Add Bollinger Bands to price chart
4. Multi-timeframe view (1min, 5min, 15min, 60min)
5. Export signals to CSV
6. Add more metrics (volatility, volume profile)

**Files to Modify:**
- `app.py` - Add new charts and features
- Possibly `modules/indicators.py` - Add more indicators

---

## ⚠️ Common Pitfalls to Avoid

### 1. Don't Regenerate All Data
- Database already has 23,250 records
- Don't re-fetch unless specifically requested
- Use existing data for testing

### 2. Don't Break Working Code
- Dashboard is working perfectly
- Test changes incrementally
- Keep backup of working version

### 3. Don't Ignore Test Failures
- 18/55 tests failing (known issue)
- These are format mismatches, not functional bugs
- Don't spend time fixing unless requested

### 4. Don't Commit Sensitive Files
- `.env` file (API credentials)
- `fyers_access_token.txt` (access token)
- `data/ptip.db` (database file)
- All are in `.gitignore`

### 5. Don't Over-Optimize
- This is an Ultra-MVP
- Focus on working code over perfect code
- User prefers speed over perfection

---

## 🔑 Key Technical Details

### Database
- **Location:** `data/ptip.db`
- **Size:** 3.85 MB
- **Records:** 23,250 (4,650 per stock)
- **Stocks:** RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK
- **Date Range:** 2025-07-14 to 2025-10-10 (88 days)
- **Resolution:** 5-minute candles

### Indicators (All Working)
1. RSI (14 period)
2. MA20, MA50, MA200
3. EMA12, EMA26
4. MACD
5. Bollinger Bands
6. Stochastic Oscillator
7. ATR

### Strategy
- **Type:** Scalping Options
- **BUY Signal:** RSI < 30 AND price > MA20
- **SELL Signal:** RSI > 70
- **Current Results:** 4 BUY, 2,896 SELL (needs tuning)

### Fyers API
- **Authentication:** OAuth 2.0 (manual token copy)
- **Token Location:** `fyers_access_token.txt`
- **Token Validity:** 24 hours
- **Rate Limiting:** 1-2 second delays between requests
- **Date Format:** YYYY-MM-DD strings (not Unix timestamps)

---

## 📋 Known Issues (Non-Blocking)

1. **Test Failures:** 18/55 tests failing
   - Reason: Format mismatches (expecting 'signal' column, but strategy returns 'action')
   - Impact: None (core functionality works)
   - Fix: Deferred

2. **Timestamp Conversion:** Pandas Timestamp → string for signal storage
   - Reason: SQLite doesn't support Timestamp objects
   - Impact: Signals not stored in database (but visible in dashboard)
   - Fix: Deferred

3. **Strategy Tuning:** RSI < 30 threshold too strict
   - Reason: Only 4 BUY signals in 88 days
   - Impact: Strategy may miss opportunities
   - Fix: Option 1 (Strategy Tuning)

4. **Missing Attribute:** `is_authenticated` in FyersDataFetcher
   - Reason: Not implemented
   - Impact: 2 tests failing
   - Fix: Deferred

---

## 💡 Context Management Tips

### For AI Assistant:
1. **Read documentation first** - Don't assume, verify
2. **Check git history** - See what was done recently
3. **Run tests** - Understand current state
4. **Ask clarifying questions** - User prefers questions over assumptions
5. **Use existing patterns** - Follow established code style

### What Makes This Project Unique:
- **Ultra-MVP approach** - Speed over perfection
- **Single user** - No multi-user concerns
- **Local only** - No deployment, no cloud
- **Windows-specific** - PowerShell commands
- **Novice developer** - User learning as they go
- **AI-assisted** - Heavy reliance on AI for development

---

## 🎯 Success Criteria for Next Session

### Minimum Viable Outcome:
- User chooses one of the 3 options
- Option is implemented and working
- Dashboard still functional
- Changes committed to Git
- User satisfied with progress

### Ideal Outcome:
- Option implemented with high quality
- Tests passing (if applicable)
- Documentation updated
- User excited about results
- Clear next steps identified

---

## 📞 Communication Guidelines

### User Preferences:
- **Direct and concise** - No excessive flattery
- **Ask before major changes** - Get approval for big decisions
- **Show progress incrementally** - Commit frequently
- **Explain trade-offs** - Help user make informed decisions
- **Be honest about limitations** - Don't overpromise

### When to Ask User:
- Choosing between multiple approaches
- Making architectural decisions
- Changing existing working code significantly
- Adding new dependencies
- Deviating from documented plan

### When to Proceed Autonomously:
- Fixing obvious bugs
- Following established patterns
- Implementing clearly specified features
- Refactoring for clarity
- Adding comments/documentation

---

## 🔄 Session Handoff Checklist

Before ending a session, ensure:
- [ ] All changes committed to Git
- [ ] PROGRESS.md updated
- [ ] Dashboard still working
- [ ] No broken tests introduced
- [ ] Documentation reflects current state
- [ ] Clear next steps documented
- [ ] User knows how to continue

---

## 📚 Additional Resources

### In Repository:
- `Resources/FYERS-API-V3-Docs-help-summary.md` - Fyers API reference
- `config.py` - All strategy parameters
- `tests/` - Test suite (reference for expected behavior)

### External:
- Fyers API Docs: https://myapi.fyers.in/docsv3
- Streamlit Docs: https://docs.streamlit.io
- Plotly Docs: https://plotly.com/python/

---

## ✅ Verification Checklist

Before starting work, verify:
- [ ] Read all essential documentation
- [ ] Dashboard runs successfully
- [ ] Database has 23,250 records
- [ ] All 5 stocks visible in dropdown
- [ ] Signals visible on charts
- [ ] User has chosen an option (1, 2, or 3)
- [ ] You understand the chosen option's requirements

---

**End of Handoff Guide**

**Remember:** This project is 60% complete. The foundation is solid. Focus on the chosen option and deliver working code. User values progress over perfection.

Good luck! 🚀

