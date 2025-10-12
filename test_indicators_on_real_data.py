"""
Test indicators and strategy on real historical data
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.database import Database
from modules.indicators import add_all_indicators
from modules.strategy import ScalpingStrategy
import config


def main():
    print("="*80)
    print("TESTING INDICATORS & STRATEGY ON REAL DATA")
    print("="*80)
    
    db = Database()
    strategy = ScalpingStrategy()
    
    # Get all stocks
    stocks_df = db.get_all_stocks()
    
    print(f"\n📊 Testing on {len(stocks_df)} stocks:")
    
    for idx, row in stocks_df.iterrows():
        symbol = row['symbol']
        stock_name = row['name']
        
        print(f"\n{'='*80}")
        print(f"[{idx+1}/{len(stocks_df)}] {stock_name} ({symbol})")
        print('='*80)
        
        # Get price data
        df = db.get_price_data(symbol)
        
        if df.empty:
            print(f"❌ No data for {symbol}")
            continue
        
        print(f"✅ Loaded {len(df)} records")
        print(f"   Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        
        # Add indicators
        print(f"\n📊 Calculating indicators...")
        df_with_indicators = add_all_indicators(df.copy())
        
        # Check if indicators were added
        indicator_cols = ['rsi', 'ma_20', 'ma_50', 'ma_200', 'ema_12', 'ema_26', 
                         'macd', 'macd_signal', 'bb_upper', 'bb_lower', 'stoch_k', 'atr']
        
        missing_indicators = [col for col in indicator_cols if col not in df_with_indicators.columns]
        
        if missing_indicators:
            print(f"❌ Missing indicators: {missing_indicators}")
            continue
        
        print(f"✅ All indicators calculated")
        
        # Show indicator statistics
        print(f"\n📈 Indicator Statistics:")
        print(f"   RSI: min={df_with_indicators['rsi'].min():.2f}, max={df_with_indicators['rsi'].max():.2f}, avg={df_with_indicators['rsi'].mean():.2f}")
        print(f"   MA20: min={df_with_indicators['ma_20'].min():.2f}, max={df_with_indicators['ma_20'].max():.2f}")
        print(f"   MA50: min={df_with_indicators['ma_50'].min():.2f}, max={df_with_indicators['ma_50'].max():.2f}")
        print(f"   MACD: min={df_with_indicators['macd'].min():.2f}, max={df_with_indicators['macd'].max():.2f}")
        print(f"   ATR: min={df_with_indicators['atr'].min():.2f}, max={df_with_indicators['atr'].max():.2f}")
        
        # Generate signals
        print(f"\n🎯 Generating trading signals...")
        signals_df = strategy.generate_signals(df_with_indicators.copy())

        if signals_df.empty:
            print(f"⚠️  No signals generated (all HOLD)")
            continue

        print(f"✅ Signals generated")

        # Count signals (strategy returns 'action' column with BUY/SELL only)
        buy_signals = (signals_df['action'] == 'BUY').sum()
        sell_signals = (signals_df['action'] == 'SELL').sum()
        total_candles = len(df_with_indicators)
        
        print(f"\n📊 Signal Summary:")
        print(f"   Total candles: {total_candles}")
        print(f"   BUY signals: {buy_signals} ({buy_signals/total_candles*100:.2f}%)")
        print(f"   SELL signals: {sell_signals} ({sell_signals/total_candles*100:.2f}%)")
        print(f"   HOLD (no signal): {total_candles - buy_signals - sell_signals} ({(total_candles - buy_signals - sell_signals)/total_candles*100:.2f}%)")

        # Show recent signals
        print(f"\n🔍 Recent Trading Signals (last 10):")
        recent_signals = signals_df.tail(10)

        for _, sig_row in recent_signals.iterrows():
            signal_type = sig_row['action']
            timestamp = sig_row['timestamp']
            price = sig_row['price']
            confidence = sig_row.get('confidence', 0)

            emoji = "🟢" if signal_type == 'BUY' else "🔴"
            print(f"   {emoji} {signal_type} at {timestamp} | Price: ₹{price:.2f} | Confidence: {confidence:.2f}")

        # Store signals in database
        print(f"\n💾 Storing signals in database...")
        signals_to_store = signals_df.copy()
        
        if not signals_to_store.empty:
            for _, sig_row in signals_to_store.iterrows():
                db.insert_signal(
                    symbol=symbol,
                    strategy='Scalping Options',
                    timestamp=sig_row['timestamp'],
                    action=sig_row['action'],
                    price=sig_row['price'],
                    confidence=sig_row.get('confidence', 0.0)
                )
            print(f"✅ Stored {len(signals_to_store)} signals in database")
        else:
            print(f"⚠️  No signals to store")

    # Overall summary
    print(f"\n{'='*80}")
    print("OVERALL SUMMARY")
    print('='*80)

    all_signals = db.get_signals()
    print(f"\n📊 Total signals in database: {len(all_signals)}")
    
    if not all_signals.empty:
        buy_count = (all_signals['action'] == 'BUY').sum()
        sell_count = (all_signals['action'] == 'SELL').sum()
        
        print(f"   BUY signals: {buy_count}")
        print(f"   SELL signals: {sell_count}")
        
        # Signals by stock
        print(f"\n📈 Signals by stock:")
        for symbol in all_signals['symbol'].unique():
            stock_signals = all_signals[all_signals['symbol'] == symbol]
            print(f"   {symbol}: {len(stock_signals)} signals")
    
    db.close()
    
    print(f"\n{'='*80}")
    print("✅ TESTING COMPLETE")
    print('='*80)
    
    print(f"\n📋 Next Steps:")
    print("   1. Review signal quality")
    print("   2. Adjust strategy parameters if needed")
    print("   3. Proceed to backtesting (Week 4)")
    print("   4. Build Streamlit dashboard (Week 3)")


if __name__ == "__main__":
    main()

