"""
Test script to fetch real data from Fyers API
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.data_fetcher import FyersDataFetcher
from modules.database import Database
import config

print("="*70)
print("FYERS DATA FETCH TEST")
print("="*70)

# Read access token
try:
    with open('fyers_access_token.txt', 'r') as f:
        access_token = f.read().strip()
    print(f"\n✅ Access token loaded: {access_token[:30]}...")
except FileNotFoundError:
    print("\n❌ Access token file not found!")
    print("Please run authenticate_fyers.py first")
    exit(1)

# Initialize data fetcher
fetcher = FyersDataFetcher()

# Authenticate with token
print("\n🔐 Authenticating with Fyers API...")
if fetcher.authenticate(access_token):
    print("✅ Authentication successful!")
else:
    print("❌ Authentication failed!")
    exit(1)

# Initialize database
db = Database()

# Test: Fetch historical data for RELIANCE
# Using recent dates (October 2025)
symbol = "NSE:RELIANCE-EQ"
end_date = datetime(2025, 10, 10, 15, 30)  # Oct 10, 2025 (market close)
start_date = datetime(2025, 10, 6, 9, 15)  # Oct 6, 2025 (market open)

print(f"\n📊 Fetching test data for {symbol}")
print(f"   From: {start_date.strftime('%Y-%m-%d %H:%M')}")
print(f"   To: {end_date.strftime('%Y-%m-%d %H:%M')}")

# Fetch data
df = fetcher.fetch_historical_data(symbol, start_date, end_date, resolution='5')

if not df.empty:
    print(f"\n✅ Data fetched successfully!")
    print(f"   Records: {len(df)}")
    print(f"\n📋 Sample data:")
    print(df.head(10))
    
    # Add stock to database
    db.add_stock(symbol, "Reliance Industries", "NSE")
    
    # Store in database
    print(f"\n💾 Storing data in database...")
    if db.insert_price_data(df, symbol):
        print("✅ Data stored successfully!")
        
        # Verify retrieval
        print(f"\n🔍 Verifying data retrieval...")
        retrieved_df = db.get_price_data(symbol)
        print(f"✅ Retrieved {len(retrieved_df)} records from database")
        
        print("\n" + "="*70)
        print("TEST COMPLETED SUCCESSFULLY!")
        print("="*70)
        print(f"\n✅ Fyers API is working correctly")
        print(f"✅ Database storage is working")
        print(f"✅ Data retrieval is working")
        print(f"\n🎯 Ready to proceed with full data fetch!")
    else:
        print("❌ Failed to store data in database")
else:
    print("\n❌ No data fetched!")
    print("Possible issues:")
    print("- Market is closed (try fetching older data)")
    print("- Symbol format incorrect")
    print("- API rate limit reached")

print("\n" + "="*70)

