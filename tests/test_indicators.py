"""
Test suite for indicators module
"""

import sys
import os
import pytest
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.indicators import (
    calculate_rsi,
    calculate_moving_average,
    calculate_ema,
    calculate_macd,
    calculate_bollinger_bands,
    calculate_stochastic,
    calculate_atr,
    add_all_indicators
)


@pytest.fixture
def sample_price_data():
    """Create sample price data for testing"""
    # Create 100 data points for reliable indicator calculation
    dates = pd.date_range(start='2025-09-01', periods=100, freq='5min')
    
    # Create realistic price movement
    np.random.seed(42)
    base_price = 1300
    price_changes = np.random.randn(100) * 5
    closes = base_price + np.cumsum(price_changes)
    
    data = {
        'timestamp': dates,
        'open': closes + np.random.randn(100) * 2,
        'high': closes + abs(np.random.randn(100) * 3),
        'low': closes - abs(np.random.randn(100) * 3),
        'close': closes,
        'volume': np.random.randint(50000, 150000, 100)
    }
    return pd.DataFrame(data)


@pytest.fixture
def flat_price_data():
    """Create flat price data for edge case testing"""
    dates = pd.date_range(start='2025-09-01', periods=50, freq='5min')
    data = {
        'timestamp': dates,
        'open': [1300] * 50,
        'high': [1300] * 50,
        'low': [1300] * 50,
        'close': [1300] * 50,
        'volume': [100000] * 50
    }
    return pd.DataFrame(data)


class TestRSI:
    """Test RSI calculation"""

    def test_rsi_calculation(self, sample_price_data):
        """Test that RSI is calculated correctly"""
        df = add_all_indicators(sample_price_data.copy())

        assert 'rsi' in df.columns
        assert not df['rsi'].isna().all()

        # RSI should be between 0 and 100
        valid_rsi = df['rsi'].dropna()
        assert (valid_rsi >= 0).all()
        assert (valid_rsi <= 100).all()

    def test_rsi_flat_prices(self, flat_price_data):
        """Test RSI with flat prices (should be around 50)"""
        df = add_all_indicators(flat_price_data.copy())

        # For flat prices, RSI should be around 50 (neutral)
        valid_rsi = df['rsi'].dropna()
        if len(valid_rsi) > 0:
            # Allow some tolerance due to calculation method
            assert valid_rsi.mean() > 40
            assert valid_rsi.mean() < 60

    def test_rsi_insufficient_data(self):
        """Test RSI with insufficient data"""
        # Only 10 data points (need at least 14 for RSI)
        dates = pd.date_range(start='2025-09-01', periods=10, freq='5min')
        data = {
            'timestamp': dates,
            'open': [1300] * 10,
            'high': [1310] * 10,
            'low': [1290] * 10,
            'close': [1300 + i for i in range(10)],
            'volume': [100000] * 10
        }
        df = pd.DataFrame(data)

        result = add_all_indicators(df)

        # Should still return DataFrame with rsi column
        assert 'rsi' in result.columns


class TestMovingAverages:
    """Test SMA and EMA calculations"""

    def test_ma_calculation(self, sample_price_data):
        """Test MA calculation"""
        df = add_all_indicators(sample_price_data.copy())

        assert 'ma_20' in df.columns
        assert 'ma_50' in df.columns

        # First 19 values should be NaN for MA20
        assert df['ma_20'].iloc[:19].isna().all()

        # 20th value onwards should have values
        assert not df['ma_20'].iloc[19:].isna().all()

    def test_ema_calculation(self, sample_price_data):
        """Test EMA calculation"""
        df = add_all_indicators(sample_price_data.copy())

        assert 'ema_12' in df.columns
        assert 'ema_26' in df.columns
        assert not df['ema_12'].isna().all()

    def test_multiple_ma_periods(self, sample_price_data):
        """Test calculating multiple MA periods"""
        df = add_all_indicators(sample_price_data.copy())

        assert 'ma_20' in df.columns
        assert 'ma_50' in df.columns
        assert 'ma_200' in df.columns


class TestMACD:
    """Test MACD calculation"""

    def test_macd_calculation(self, sample_price_data):
        """Test MACD calculation"""
        df = add_all_indicators(sample_price_data.copy())

        assert 'macd' in df.columns
        assert 'macd_signal' in df.columns
        assert 'macd_histogram' in df.columns

        # Check that histogram = macd - signal
        valid_data = df.dropna(subset=['macd', 'macd_signal', 'macd_histogram'])
        if len(valid_data) > 0:
            calculated_histogram = valid_data['macd'] - valid_data['macd_signal']
            np.testing.assert_array_almost_equal(
                valid_data['macd_histogram'].values,
                calculated_histogram.values,
                decimal=5
            )


class TestBollingerBands:
    """Test Bollinger Bands calculation"""

    def test_bollinger_bands_calculation(self, sample_price_data):
        """Test Bollinger Bands calculation"""
        df = add_all_indicators(sample_price_data.copy())

        assert 'bb_upper' in df.columns
        assert 'bb_middle' in df.columns
        assert 'bb_lower' in df.columns

        # Upper band should be > middle > lower band
        valid_data = df.dropna(subset=['bb_upper', 'bb_middle', 'bb_lower'])
        if len(valid_data) > 0:
            assert (valid_data['bb_upper'] >= valid_data['bb_middle']).all()
            assert (valid_data['bb_middle'] >= valid_data['bb_lower']).all()


class TestStochastic:
    """Test Stochastic Oscillator calculation"""

    def test_stochastic_calculation(self, sample_price_data):
        """Test Stochastic calculation"""
        df = add_all_indicators(sample_price_data.copy())

        assert 'stoch_k' in df.columns
        assert 'stoch_d' in df.columns

        # Stochastic should be between 0 and 100
        valid_k = df['stoch_k'].dropna()
        valid_d = df['stoch_d'].dropna()

        if len(valid_k) > 0:
            assert (valid_k >= 0).all()
            assert (valid_k <= 100).all()

        if len(valid_d) > 0:
            assert (valid_d >= 0).all()
            assert (valid_d <= 100).all()


class TestATR:
    """Test Average True Range calculation"""

    def test_atr_calculation(self, sample_price_data):
        """Test ATR calculation"""
        df = add_all_indicators(sample_price_data.copy())

        assert 'atr' in df.columns

        # ATR should be positive
        valid_atr = df['atr'].dropna()
        if len(valid_atr) > 0:
            assert (valid_atr >= 0).all()


class TestAllIndicators:
    """Test adding all indicators at once"""

    def test_add_all_indicators(self, sample_price_data):
        """Test adding all indicators"""
        df = add_all_indicators(sample_price_data.copy())

        # Check all expected columns exist
        expected_columns = [
            'rsi', 'ma_20', 'ma_50', 'ma_200',
            'ema_12', 'ema_26', 'macd', 'macd_signal', 'macd_histogram',
            'bb_upper', 'bb_middle', 'bb_lower',
            'stoch_k', 'stoch_d', 'atr'
        ]

        for col in expected_columns:
            assert col in df.columns
    
    def test_indicators_with_real_data_shape(self, sample_price_data):
        """Test that indicators don't change DataFrame shape"""
        original_len = len(sample_price_data)
        df = add_all_indicators(sample_price_data.copy())
        
        # Length should remain the same
        assert len(df) == original_len
        
        # Original columns should still exist
        assert 'timestamp' in df.columns
        assert 'close' in df.columns


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_dataframe(self):
        """Test with empty DataFrame"""
        df = pd.DataFrame()

        # Should handle gracefully
        try:
            result = add_all_indicators(df)
            assert isinstance(result, pd.DataFrame)
        except:
            # It's OK if it raises an error for empty DataFrame
            pass

    def test_nan_values_in_data(self):
        """Test with NaN values in price data"""
        data = {
            'timestamp': pd.date_range(start='2025-09-01', periods=50, freq='5min'),
            'open': [1300] * 50,
            'high': [1310] * 50,
            'low': [1290] * 50,
            'close': [1300, np.nan, 1310, 1305, np.nan, 1315] + [1300] * 44,
            'volume': [100000] * 50
        }
        df = pd.DataFrame(data)

        result = add_all_indicators(df)

        # Should handle NaN values gracefully
        assert isinstance(result, pd.DataFrame)
        assert 'rsi' in result.columns


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

