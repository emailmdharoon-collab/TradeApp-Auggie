"""
Configuration file for PTIP (Personal Trading Intelligence Platform)
Contains all configuration parameters and API credentials
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# FYERS API CONFIGURATION
# ============================================================================
FYERS_CLIENT_ID = os.getenv('FYERS_CLIENT_ID')
FYERS_SECRET_KEY = os.getenv('FYERS_SECRET_KEY')
FYERS_REDIRECT_URI = os.getenv('FYERS_REDIRECT_URI', 'http://localhost:8080')

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
DB_PATH = 'data/ptip.db'

# ============================================================================
# STRATEGY PARAMETERS - SCALPING OPTIONS
# ============================================================================
# RSI Parameters
SCALPING_RSI_PERIOD = 14
SCALPING_RSI_OVERSOLD = 30
SCALPING_RSI_OVERBOUGHT = 70

# Moving Average Parameters
SCALPING_MA_SHORT = 20
SCALPING_MA_LONG = 50

# EMA Parameters
SCALPING_EMA_SHORT = 12
SCALPING_EMA_LONG = 26

# ============================================================================
# BACKTESTING CONFIGURATION
# ============================================================================
INITIAL_CAPITAL = 100000  # Starting capital in INR
POSITION_SIZE_PCT = 0.10  # Use 10% of capital per trade

# ============================================================================
# DATA FETCHING CONFIGURATION
# ============================================================================
# Default stocks to track
DEFAULT_STOCKS = [
    "NSE:RELIANCE-EQ",
    "NSE:TCS-EQ",
    "NSE:INFY-EQ",
    "NSE:HDFCBANK-EQ",
    "NSE:ICICIBANK-EQ"
]

# Historical data period (in days)
HISTORICAL_DATA_DAYS = 90

# Data resolution for Fyers API
# Options: '1' (1 min), '5' (5 min), '15' (15 min), '60' (1 hour), 'D' (1 day)
DATA_RESOLUTION = '5'  # 5-minute candles for scalping

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/ptip.log'

# ============================================================================
# VALIDATION
# ============================================================================
def validate_config():
    """Validate that all required configuration is present"""
    errors = []
    
    if not FYERS_CLIENT_ID:
        errors.append("FYERS_CLIENT_ID is not set in .env file")
    if not FYERS_SECRET_KEY:
        errors.append("FYERS_SECRET_KEY is not set in .env file")
    
    if errors:
        print("❌ Configuration Errors:")
        for error in errors:
            print(f"   - {error}")
        print("\n💡 Please create a .env file with your Fyers API credentials.")
        print("   You can copy .env.template to .env and fill in your credentials.")
        return False
    
    return True

# Validate on import (optional - can be called explicitly)
if __name__ == "__main__":
    if validate_config():
        print("✅ Configuration is valid!")
    else:
        print("❌ Configuration validation failed!")

