"""
Verify database data and fix any issues
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.data_fetcher import FyersDataFetcher
from modules.database import Database
import config


def main():
    print("="*80)
    print("PTIP - DATA VERIFICATION & FIX")
    print("="*80)
    
    db = Database()
    
    # Check all stocks
    print("\n📊 Checking stocks in database...")
    stocks_df = db.get_all_stocks()
    
    if stocks_df.empty:
        print("❌ No stocks found in database!")
        return
    
    print(f"✅ Found {len(stocks_df)} stocks:")
    for idx, row in stocks_df.iterrows():
        print(f"   {idx+1}. {row['symbol']} - {row['name']} ({row['exchange']})")
    
    # Check data for each stock
    print("\n📈 Checking price data for each stock...")
    print("-" * 80)
    
    stocks_with_data = []
    stocks_without_data = []
    
    for idx, row in stocks_df.iterrows():
        symbol = row['symbol']
        df = db.get_price_data(symbol)
        
        if df.empty:
            print(f"❌ {symbol}: NO DATA")
            stocks_without_data.append(symbol)
        else:
            print(f"✅ {symbol}: {len(df):,} records")
            print(f"   Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
            print(f"   Duration: {(df['timestamp'].max() - df['timestamp'].min()).days} days")
            stocks_with_data.append(symbol)
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Stocks with data: {len(stocks_with_data)}")
    print(f"Stocks without data: {len(stocks_without_data)}")
    
    # Fix RELIANCE if needed
    if 'NSE:RELIANCE-EQ' in stocks_without_data:
        print("\n⚠️  NSE:RELIANCE-EQ has no data. Attempting to fix...")
        
        # Delete old duplicate data
        print("🗑️  Deleting old RELIANCE data...")
        cursor = db.conn.cursor()
        cursor.execute("DELETE FROM price_data WHERE symbol = 'NSE:RELIANCE-EQ'")
        db.conn.commit()
        print("✅ Old data deleted")
        
        # Fetch fresh data
        token_file = "fyers_access_token.txt"
        if os.path.exists(token_file):
            with open(token_file, 'r') as f:
                access_token = f.read().strip()
            
            fetcher = FyersDataFetcher()
            if fetcher.authenticate(access_token):
                print("✅ Authenticated with Fyers")
                
                end_date = datetime.now()
                start_date = end_date - timedelta(days=90)
                
                print(f"📊 Fetching RELIANCE data from {start_date.strftime('%Y-%m-%d')}...")
                df = fetcher.fetch_historical_data(
                    symbol='NSE:RELIANCE-EQ',
                    from_date=start_date,
                    to_date=end_date,
                    resolution='5'
                )
                
                if not df.empty:
                    print(f"✅ Fetched {len(df)} records")
                    if db.insert_price_data(df, 'NSE:RELIANCE-EQ'):
                        print("✅ RELIANCE data stored successfully!")
                    else:
                        print("❌ Failed to store RELIANCE data")
                else:
                    print("❌ No data fetched for RELIANCE")
    
    # Final verification
    print("\n" + "="*80)
    print("FINAL VERIFICATION")
    print("="*80)
    
    total_records = 0
    for idx, row in stocks_df.iterrows():
        symbol = row['symbol']
        df = db.get_price_data(symbol)
        record_count = len(df)
        total_records += record_count
        
        status = "✅" if record_count > 0 else "❌"
        print(f"{status} {symbol}: {record_count:,} records")
    
    print(f"\n📊 Total records in database: {total_records:,}")
    
    # Data quality checks
    print("\n" + "="*80)
    print("DATA QUALITY CHECKS")
    print("="*80)
    
    for idx, row in stocks_df.iterrows():
        symbol = row['symbol']
        df = db.get_price_data(symbol)
        
        if df.empty:
            continue
        
        print(f"\n{symbol}:")
        
        # Check for NaN values
        nan_count = df.isna().sum().sum()
        print(f"   NaN values: {nan_count}")
        
        # Check OHLC consistency
        invalid_high = (df['high'] < df['low']).sum()
        invalid_open = ((df['open'] > df['high']) | (df['open'] < df['low'])).sum()
        invalid_close = ((df['close'] > df['high']) | (df['close'] < df['low'])).sum()
        
        print(f"   Invalid high/low: {invalid_high}")
        print(f"   Invalid open: {invalid_open}")
        print(f"   Invalid close: {invalid_close}")
        
        # Check for duplicates
        duplicates = df['timestamp'].duplicated().sum()
        print(f"   Duplicate timestamps: {duplicates}")
        
        # Check for gaps
        df_sorted = df.sort_values('timestamp')
        time_diffs = df_sorted['timestamp'].diff()
        gaps = (time_diffs > timedelta(minutes=10)).sum()  # Gaps > 10 minutes
        print(f"   Time gaps (>10 min): {gaps}")
        
        # Price statistics
        print(f"   Price range: ₹{df['low'].min():.2f} - ₹{df['high'].max():.2f}")
        print(f"   Avg volume: {df['volume'].mean():,.0f}")
    
    db.close()
    
    print("\n" + "="*80)
    print("✅ VERIFICATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()

