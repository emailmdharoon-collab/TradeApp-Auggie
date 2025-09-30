"""
Trading Strategy module for PTIP
Implements the Scalping Options strategy
"""

import pandas as pd
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.indicators import add_all_indicators
import config


class ScalpingStrategy:
    """
    Scalping Options Trading Strategy
    
    Strategy Logic:
    - BUY Signal: RSI < 30 (oversold) AND price > MA20 (uptrend confirmation)
    - SELL Signal: RSI > 70 (overbought)
    - HOLD: All other conditions
    """
    
    def __init__(self):
        """Initialize Scalping Strategy with parameters from config"""
        self.name = "Scalping Options"
        self.rsi_period = config.SCALPING_RSI_PERIOD
        self.rsi_oversold = config.SCALPING_RSI_OVERSOLD
        self.rsi_overbought = config.SCALPING_RSI_OVERBOUGHT
        self.ma_short = config.SCALPING_MA_SHORT
        self.ma_long = config.SCALPING_MA_LONG
        
        print(f"✅ {self.name} strategy initialized")
        print(f"   RSI Period: {self.rsi_period}")
        print(f"   RSI Oversold: {self.rsi_oversold}")
        print(f"   RSI Overbought: {self.rsi_overbought}")
        print(f"   MA Short: {self.ma_short}, MA Long: {self.ma_long}")
    
    def generate_signals(self, df):
        """
        Generate trading signals based on the strategy
        
        Args:
            df (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            pd.DataFrame: DataFrame with signals (timestamp, action, price, confidence)
        """
        # Add all technical indicators
        df = add_all_indicators(df)
        
        signals = []
        
        # Iterate through data to generate signals
        for i in range(len(df)):
            # Need enough data for MA_50
            if i < self.ma_long:
                continue
            
            row = df.iloc[i]
            
            # Skip if indicators are NaN
            if pd.isna(row['rsi']) or pd.isna(row['ma_20']) or pd.isna(row['ma_50']):
                continue
            
            # BUY Signal: RSI oversold + price above MA20 (trend confirmation)
            if row['rsi'] < self.rsi_oversold and row['close'] > row['ma_20']:
                signals.append({
                    'timestamp': row['timestamp'],
                    'action': 'BUY',
                    'price': row['close'],
                    'confidence': self._calculate_buy_confidence(row),
                    'rsi': row['rsi'],
                    'ma_20': row['ma_20'],
                    'ma_50': row['ma_50']
                })
            
            # SELL Signal: RSI overbought
            elif row['rsi'] > self.rsi_overbought:
                signals.append({
                    'timestamp': row['timestamp'],
                    'action': 'SELL',
                    'price': row['close'],
                    'confidence': self._calculate_sell_confidence(row),
                    'rsi': row['rsi'],
                    'ma_20': row['ma_20'],
                    'ma_50': row['ma_50']
                })
        
        # Convert to DataFrame
        signals_df = pd.DataFrame(signals)
        
        if not signals_df.empty:
            print(f"✅ Generated {len(signals_df)} signals ({len(signals_df[signals_df['action']=='BUY'])} BUY, {len(signals_df[signals_df['action']=='SELL'])} SELL)")
        else:
            print("⚠️  No signals generated for this data")
        
        return signals_df
    
    def _calculate_buy_confidence(self, row):
        """
        Calculate confidence score for BUY signal (0-1)
        
        Higher confidence when:
        - RSI is more oversold (closer to 0)
        - Price is well above MA20
        - MA20 > MA50 (strong uptrend)
        """
        confidence = 0.5  # Base confidence
        
        # RSI component (more oversold = higher confidence)
        rsi_score = (self.rsi_oversold - row['rsi']) / self.rsi_oversold
        confidence += rsi_score * 0.3
        
        # Trend component (price above MA20)
        if row['close'] > row['ma_20']:
            price_above_ma = (row['close'] - row['ma_20']) / row['ma_20']
            confidence += min(price_above_ma * 10, 0.1)  # Cap at 0.1
        
        # Strong uptrend component (MA20 > MA50)
        if row['ma_20'] > row['ma_50']:
            confidence += 0.1
        
        # Ensure confidence is between 0 and 1
        return max(0.0, min(1.0, confidence))
    
    def _calculate_sell_confidence(self, row):
        """
        Calculate confidence score for SELL signal (0-1)
        
        Higher confidence when:
        - RSI is more overbought (closer to 100)
        - Price is below MA20 (trend reversal)
        """
        confidence = 0.5  # Base confidence
        
        # RSI component (more overbought = higher confidence)
        rsi_score = (row['rsi'] - self.rsi_overbought) / (100 - self.rsi_overbought)
        confidence += rsi_score * 0.3
        
        # Trend reversal component (price below MA20)
        if row['close'] < row['ma_20']:
            confidence += 0.2
        
        # Ensure confidence is between 0 and 1
        return max(0.0, min(1.0, confidence))
    
    def get_current_signal(self, df):
        """
        Get the most recent signal from the data
        
        Args:
            df (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            dict: Most recent signal or None
        """
        signals = self.generate_signals(df)
        
        if signals.empty:
            return None
        
        # Return the most recent signal
        return signals.iloc[-1].to_dict()


# Test function
if __name__ == "__main__":
    print("Testing Scalping Strategy module...")
    
    # Create sample data
    import numpy as np
    
    dates = pd.date_range(start='2024-01-01', periods=100, freq='5min')
    np.random.seed(42)
    
    # Generate realistic price data with trend
    base_price = 2500
    trend = np.linspace(0, 100, 100)
    noise = np.random.randn(100) * 10
    close = base_price + trend + noise
    
    high = close + np.random.rand(100) * 5
    low = close - np.random.rand(100) * 5
    open_price = close + np.random.randn(100) * 2
    volume = np.random.randint(100000, 1000000, 100)
    
    df = pd.DataFrame({
        'timestamp': dates,
        'open': open_price,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    })
    
    # Test strategy
    strategy = ScalpingStrategy()
    signals = strategy.generate_signals(df)
    
    if not signals.empty:
        print("\nGenerated Signals:")
        print(signals[['timestamp', 'action', 'price', 'confidence', 'rsi']].head(10))
    
    print("\n✅ Scalping Strategy module test completed!")

