"""
Technical Indicators module for PTIP
Calculates various technical indicators for trading strategies
"""

import pandas as pd
import numpy as np


def calculate_rsi(prices, period=14):
    """
    Calculate Relative Strength Index (RSI)
    
    Args:
        prices (pd.Series): Price series (typically close prices)
        period (int): RSI period (default: 14)
        
    Returns:
        pd.Series: RSI values
    """
    # Calculate price changes
    delta = prices.diff()
    
    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Calculate average gain and loss
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    
    # Calculate RS and RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_moving_average(prices, period):
    """
    Calculate Simple Moving Average (SMA)
    
    Args:
        prices (pd.Series): Price series
        period (int): MA period
        
    Returns:
        pd.Series: Moving average values
    """
    return prices.rolling(window=period, min_periods=period).mean()


def calculate_ema(prices, period):
    """
    Calculate Exponential Moving Average (EMA)
    
    Args:
        prices (pd.Series): Price series
        period (int): EMA period
        
    Returns:
        pd.Series: EMA values
    """
    return prices.ewm(span=period, adjust=False).mean()


def calculate_macd(prices, fast_period=12, slow_period=26, signal_period=9):
    """
    Calculate MACD (Moving Average Convergence Divergence)
    
    Args:
        prices (pd.Series): Price series
        fast_period (int): Fast EMA period (default: 12)
        slow_period (int): Slow EMA period (default: 26)
        signal_period (int): Signal line period (default: 9)
        
    Returns:
        tuple: (macd_line, signal_line, histogram)
    """
    # Calculate EMAs
    ema_fast = calculate_ema(prices, fast_period)
    ema_slow = calculate_ema(prices, slow_period)
    
    # MACD line
    macd_line = ema_fast - ema_slow
    
    # Signal line
    signal_line = calculate_ema(macd_line, signal_period)
    
    # Histogram
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram


def calculate_bollinger_bands(prices, period=20, num_std=2):
    """
    Calculate Bollinger Bands
    
    Args:
        prices (pd.Series): Price series
        period (int): MA period (default: 20)
        num_std (int): Number of standard deviations (default: 2)
        
    Returns:
        tuple: (upper_band, middle_band, lower_band)
    """
    # Middle band (SMA)
    middle_band = calculate_moving_average(prices, period)
    
    # Standard deviation
    std = prices.rolling(window=period, min_periods=period).std()
    
    # Upper and lower bands
    upper_band = middle_band + (std * num_std)
    lower_band = middle_band - (std * num_std)
    
    return upper_band, middle_band, lower_band


def calculate_stochastic(high, low, close, k_period=14, d_period=3):
    """
    Calculate Stochastic Oscillator
    
    Args:
        high (pd.Series): High prices
        low (pd.Series): Low prices
        close (pd.Series): Close prices
        k_period (int): %K period (default: 14)
        d_period (int): %D period (default: 3)
        
    Returns:
        tuple: (%K, %D)
    """
    # Lowest low and highest high over the period
    lowest_low = low.rolling(window=k_period, min_periods=k_period).min()
    highest_high = high.rolling(window=k_period, min_periods=k_period).max()
    
    # %K
    k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    
    # %D (SMA of %K)
    d = k.rolling(window=d_period, min_periods=d_period).mean()
    
    return k, d


def calculate_atr(high, low, close, period=14):
    """
    Calculate Average True Range (ATR)
    
    Args:
        high (pd.Series): High prices
        low (pd.Series): Low prices
        close (pd.Series): Close prices
        period (int): ATR period (default: 14)
        
    Returns:
        pd.Series: ATR values
    """
    # True Range components
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    
    # True Range (maximum of the three)
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # ATR (moving average of TR)
    atr = tr.rolling(window=period, min_periods=period).mean()
    
    return atr


def add_all_indicators(df):
    """
    Add all technical indicators to a DataFrame
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        
    Returns:
        pd.DataFrame: DataFrame with added indicator columns
    """
    # Make a copy to avoid modifying original
    df = df.copy()
    
    # RSI
    df['rsi'] = calculate_rsi(df['close'], period=14)
    
    # Moving Averages
    df['ma_20'] = calculate_moving_average(df['close'], period=20)
    df['ma_50'] = calculate_moving_average(df['close'], period=50)
    df['ma_200'] = calculate_moving_average(df['close'], period=200)
    
    # EMAs
    df['ema_12'] = calculate_ema(df['close'], period=12)
    df['ema_26'] = calculate_ema(df['close'], period=26)
    
    # MACD
    df['macd'], df['macd_signal'], df['macd_histogram'] = calculate_macd(df['close'])
    
    # Bollinger Bands
    df['bb_upper'], df['bb_middle'], df['bb_lower'] = calculate_bollinger_bands(df['close'])
    
    # Stochastic
    df['stoch_k'], df['stoch_d'] = calculate_stochastic(df['high'], df['low'], df['close'])
    
    # ATR
    df['atr'] = calculate_atr(df['high'], df['low'], df['close'])
    
    return df


# Test function
if __name__ == "__main__":
    print("Testing Technical Indicators module...")
    
    # Create sample data
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    np.random.seed(42)
    
    # Generate random OHLCV data
    close = 100 + np.cumsum(np.random.randn(100) * 2)
    high = close + np.random.rand(100) * 2
    low = close - np.random.rand(100) * 2
    open_price = close + np.random.randn(100)
    volume = np.random.randint(1000000, 10000000, 100)
    
    df = pd.DataFrame({
        'timestamp': dates,
        'open': open_price,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    })
    
    # Add indicators
    df = add_all_indicators(df)
    
    # Display results
    print("\nSample data with indicators:")
    print(df[['timestamp', 'close', 'rsi', 'ma_20', 'ma_50', 'macd']].tail(10))
    
    print("\n✅ Technical Indicators module test completed!")

