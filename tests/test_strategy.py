"""
Test suite for strategy module
"""

import sys
import os
import pytest
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.strategy import ScalpingStrategy
from modules.indicators import add_all_indicators
import config


@pytest.fixture
def strategy():
    """Create a strategy instance"""
    return ScalpingStrategy()


@pytest.fixture
def sample_data_with_indicators():
    """Create sample data with indicators already calculated"""
    dates = pd.date_range(start='2025-09-01', periods=100, freq='5min')
    
    # Create price data
    np.random.seed(42)
    base_price = 1300
    price_changes = np.random.randn(100) * 5
    closes = base_price + np.cumsum(price_changes)
    
    df = pd.DataFrame({
        'timestamp': dates,
        'open': closes + np.random.randn(100) * 2,
        'high': closes + abs(np.random.randn(100) * 3),
        'low': closes - abs(np.random.randn(100) * 3),
        'close': closes,
        'volume': np.random.randint(50000, 150000, 100)
    })
    
    # Add indicators
    df = add_all_indicators(df)
    
    return df


@pytest.fixture
def buy_signal_data():
    """Create data that should generate BUY signal"""
    dates = pd.date_range(start='2025-09-01', periods=50, freq='5min')
    
    df = pd.DataFrame({
        'timestamp': dates,
        'close': [1300] * 50,
        'open': [1300] * 50,
        'high': [1310] * 50,
        'low': [1290] * 50,
        'volume': [100000] * 50
    })
    
    # Add indicators
    df = add_all_indicators(df)
    
    # Manually set conditions for BUY signal
    # RSI < 30 (oversold) and price > MA20
    df.loc[df.index[-1], 'rsi'] = 25.0  # Oversold
    df.loc[df.index[-1], 'ma_20'] = 1290.0  # Price (1300) > MA20 (1290)
    df.loc[df.index[-1], 'ma_50'] = 1280.0
    df.loc[df.index[-1], 'close'] = 1300.0
    
    return df


@pytest.fixture
def sell_signal_data():
    """Create data that should generate SELL signal"""
    dates = pd.date_range(start='2025-09-01', periods=50, freq='5min')
    
    df = pd.DataFrame({
        'timestamp': dates,
        'close': [1300] * 50,
        'open': [1300] * 50,
        'high': [1310] * 50,
        'low': [1290] * 50,
        'volume': [100000] * 50
    })
    
    # Add indicators
    df = add_all_indicators(df)
    
    # Manually set conditions for SELL signal
    # RSI > 70 (overbought)
    df.loc[df.index[-1], 'rsi'] = 75.0  # Overbought
    df.loc[df.index[-1], 'close'] = 1300.0
    
    return df


class TestStrategyInitialization:
    """Test strategy initialization"""
    
    def test_strategy_creation(self, strategy):
        """Test that strategy is created with correct parameters"""
        assert strategy.rsi_period == config.RSI_PERIOD
        assert strategy.rsi_oversold == config.RSI_OVERSOLD
        assert strategy.rsi_overbought == config.RSI_OVERBOUGHT
        assert strategy.ma_short == config.MA_SHORT
        assert strategy.ma_long == config.MA_LONG


class TestSignalGeneration:
    """Test signal generation logic"""
    
    def test_generate_signals_basic(self, strategy, sample_data_with_indicators):
        """Test basic signal generation"""
        df = strategy.generate_signals(sample_data_with_indicators.copy())
        
        # Check that signal columns are added
        assert 'signal' in df.columns
        assert 'confidence' in df.columns
        
        # Signals should be 'BUY', 'SELL', or 'HOLD'
        assert df['signal'].isin(['BUY', 'SELL', 'HOLD']).all()
        
        # Confidence should be between 0 and 1
        assert (df['confidence'] >= 0).all()
        assert (df['confidence'] <= 1).all()
    
    def test_buy_signal_generation(self, strategy, buy_signal_data):
        """Test that BUY signal is generated correctly"""
        df = strategy.generate_signals(buy_signal_data.copy())
        
        # Last row should have BUY signal
        last_signal = df['signal'].iloc[-1]

        # Should be BUY (RSI < 30 and price > MA20)
        if not pd.isna(df['rsi'].iloc[-1]) and not pd.isna(df['ma_20'].iloc[-1]):
            assert last_signal == 'BUY'
            assert df['confidence'].iloc[-1] > 0
    
    def test_sell_signal_generation(self, strategy, sell_signal_data):
        """Test that SELL signal is generated correctly"""
        df = strategy.generate_signals(sell_signal_data.copy())
        
        # Last row should have SELL signal
        last_signal = df['signal'].iloc[-1]
        
        # Should be SELL (RSI > 70)
        if not pd.isna(df['rsi'].iloc[-1]):
            assert last_signal == 'SELL'
            assert df['confidence'].iloc[-1] > 0
    
    def test_hold_signal_generation(self, strategy, sample_data_with_indicators):
        """Test that HOLD signal is generated when no conditions met"""
        df = sample_data_with_indicators.copy()
        
        # Set neutral conditions (RSI around 50)
        df.loc[df.index[-1], 'rsi'] = 50.0
        df.loc[df.index[-1], 'ma_20'] = 1300.0
        df.loc[df.index[-1], 'ma_50'] = 1300.0
        df.loc[df.index[-1], 'close'] = 1300.0
        
        result = strategy.generate_signals(df)
        
        # Last signal should be HOLD
        assert result['signal'].iloc[-1] == 'HOLD'
        assert result['confidence'].iloc[-1] == 0.0


class TestConfidenceScoring:
    """Test confidence score calculation"""
    
    def test_buy_confidence_high(self, strategy):
        """Test high confidence BUY signal"""
        # Create row with strong BUY conditions
        row = pd.Series({
            'rsi': 20.0,  # Very oversold
            'ma_20': 1290.0,
            'ma_50': 1280.0,
            'close': 1300.0,  # Price well above MAs
            'macd_histogram': 5.0  # Positive MACD
        })
        
        confidence = strategy._calculate_buy_confidence(row)
        
        # Should have high confidence
        assert confidence > 0.5
    
    def test_buy_confidence_low(self, strategy):
        """Test low confidence BUY signal"""
        # Create row with weak BUY conditions
        row = pd.Series({
            'rsi': 29.0,  # Just barely oversold
            'ma_20': 1299.0,
            'ma_50': 1300.0,
            'close': 1300.0,  # Price barely above MA20
            'macd_histogram': -1.0  # Negative MACD
        })
        
        confidence = strategy._calculate_buy_confidence(row)
        
        # Should have lower confidence
        assert confidence < 0.5
    
    def test_sell_confidence_high(self, strategy):
        """Test high confidence SELL signal"""
        # Create row with strong SELL conditions
        row = pd.Series({
            'rsi': 80.0,  # Very overbought
            'ma_20': 1310.0,
            'ma_50': 1320.0,
            'close': 1300.0,  # Price below MAs
            'macd_histogram': -5.0  # Negative MACD
        })
        
        confidence = strategy._calculate_sell_confidence(row)
        
        # Should have high confidence
        assert confidence > 0.5
    
    def test_sell_confidence_low(self, strategy):
        """Test low confidence SELL signal"""
        # Create row with weak SELL conditions
        row = pd.Series({
            'rsi': 71.0,  # Just barely overbought
            'ma_20': 1300.0,
            'ma_50': 1300.0,
            'close': 1300.0,
            'macd_histogram': 1.0  # Positive MACD
        })
        
        confidence = strategy._calculate_sell_confidence(row)
        
        # Should have lower confidence
        assert confidence < 0.5


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_dataframe(self, strategy):
        """Test with empty DataFrame"""
        df = pd.DataFrame()
        
        result = strategy.generate_signals(df)
        
        # Should return empty DataFrame with signal columns
        assert isinstance(result, pd.DataFrame)
    
    def test_missing_indicators(self, strategy):
        """Test with missing indicator columns"""
        df = pd.DataFrame({
            'timestamp': pd.date_range(start='2025-09-01', periods=10, freq='5min'),
            'close': [1300] * 10
        })
        
        result = strategy.generate_signals(df)
        
        # Should handle gracefully (all HOLD signals)
        assert 'signal' in result.columns
        assert (result['signal'] == 'HOLD').all()
    
    def test_nan_indicators(self, strategy, sample_data_with_indicators):
        """Test with NaN values in indicators"""
        df = sample_data_with_indicators.copy()
        
        # Set some indicators to NaN
        df.loc[df.index[-1], 'rsi'] = np.nan
        
        result = strategy.generate_signals(df)
        
        # Should handle NaN gracefully (HOLD signal)
        assert result['signal'].iloc[-1] == 'HOLD'


class TestSignalCounts:
    """Test signal distribution"""
    
    def test_signal_distribution(self, strategy, sample_data_with_indicators):
        """Test that signals are distributed reasonably"""
        df = strategy.generate_signals(sample_data_with_indicators.copy())
        
        signal_counts = df['signal'].value_counts()
        
        # Should have mostly HOLD signals (normal market conditions)
        assert signal_counts.get('HOLD', 0) > signal_counts.get('BUY', 0)
        assert signal_counts.get('HOLD', 0) > signal_counts.get('SELL', 0)
        
        # Should have at least some signals (not all HOLD)
        total_signals = signal_counts.get('BUY', 0) + signal_counts.get('SELL', 0)
        assert total_signals > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

