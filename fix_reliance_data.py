"""
Fix RELIANCE data - delete old and fetch fresh 3 months
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.data_fetcher import FyersDataFetcher
from modules.database import Database


def main():
    print("="*80)
    print("FIXING RELIANCE DATA")
    print("="*80)
    
    db = Database()
    
    # Check current RELIANCE data
    print("\n📊 Current RELIANCE data:")
    df_old = db.get_price_data('NSE:RELIANCE-EQ')
    print(f"   Records: {len(df_old)}")
    if not df_old.empty:
        print(f"   Date range: {df_old['timestamp'].min()} to {df_old['timestamp'].max()}")
    
    # Delete old data
    print("\n🗑️  Deleting old RELIANCE data...")
    cursor = db.conn.cursor()
    cursor.execute("DELETE FROM price_data WHERE symbol = 'NSE:RELIANCE-EQ'")
    db.conn.commit()
    print("✅ Old data deleted")
    
    # Load access token
    token_file = "fyers_access_token.txt"
    with open(token_file, 'r') as f:
        access_token = f.read().strip()
    
    # Fetch fresh data
    fetcher = FyersDataFetcher()
    fetcher.authenticate(access_token)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    print(f"\n📊 Fetching fresh RELIANCE data...")
    print(f"   From: {start_date.strftime('%Y-%m-%d')}")
    print(f"   To: {end_date.strftime('%Y-%m-%d')}")
    
    df = fetcher.fetch_historical_data(
        symbol='NSE:RELIANCE-EQ',
        from_date=start_date,
        to_date=end_date,
        resolution='5'
    )
    
    if df.empty:
        print("❌ No data fetched!")
        return
    
    print(f"✅ Fetched {len(df)} records")
    
    # Store in database
    print("\n💾 Storing in database...")
    if db.insert_price_data(df, 'NSE:RELIANCE-EQ'):
        print("✅ Data stored successfully!")
        
        # Verify
        df_new = db.get_price_data('NSE:RELIANCE-EQ')
        print(f"\n✅ Verification:")
        print(f"   Records: {len(df_new)}")
        print(f"   Date range: {df_new['timestamp'].min()} to {df_new['timestamp'].max()}")
        print(f"   Duration: {(df_new['timestamp'].max() - df_new['timestamp'].min()).days} days")
    else:
        print("❌ Failed to store data")
    
    db.close()
    print("\n✅ RELIANCE data fixed!")


if __name__ == "__main__":
    main()

