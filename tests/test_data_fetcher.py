"""
Test suite for data_fetcher module - includes REAL Fyers API tests
"""

import sys
import os
import pytest
import pandas as pd
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.data_fetcher import FyersDataFetcher
import config


@pytest.fixture
def fetcher():
    """Create a data fetcher instance"""
    return FyersDataFetcher()


@pytest.fixture
def access_token():
    """Load access token from file"""
    token_file = "fyers_access_token.txt"
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            return f.read().strip()
    else:
        pytest.skip("Access token file not found. Run authenticate_fyers.py first.")


class TestFetcherInitialization:
    """Test data fetcher initialization"""
    
    def test_fetcher_creation(self, fetcher):
        """Test that fetcher is created successfully"""
        assert fetcher is not None
        assert fetcher.client_id == config.FYERS_CLIENT_ID
        assert fetcher.fyers is None  # Not authenticated yet


class TestAuthentication:
    """Test Fyers API authentication"""
    
    def test_authentication_with_valid_token(self, fetcher, access_token):
        """Test authentication with valid access token"""
        result = fetcher.authenticate(access_token)
        
        assert result is True
        assert fetcher.fyers is not None
        assert fetcher.is_authenticated is True
    
    def test_authentication_with_invalid_token(self, fetcher):
        """Test authentication with invalid token"""
        result = fetcher.authenticate("invalid_token_12345")
        
        # Should return False or handle gracefully
        assert result is False or fetcher.is_authenticated is False


class TestRealAPIDataFetching:
    """Test REAL Fyers API data fetching (requires valid token)"""
    
    def test_fetch_current_quote(self, fetcher, access_token):
        """Test fetching current quote for a stock"""
        fetcher.authenticate(access_token)
        
        # Fetch quote for RELIANCE
        symbol = "NSE:RELIANCE-EQ"
        
        try:
            # Use the quotes API
            data = {"symbols": symbol}
            response = fetcher.fyers.quotes(data=data)
            
            assert response is not None
            assert response['s'] == 'ok'
            assert 'd' in response
            assert len(response['d']) > 0
            
            # Check quote data structure
            quote = response['d'][0]
            assert 'v' in quote
            assert 'lp' in quote['v']  # Last price
            
            print(f"\n✅ Current price of {symbol}: ₹{quote['v']['lp']}")
            
        except Exception as e:
            pytest.fail(f"Failed to fetch quote: {e}")
    
    def test_fetch_historical_data_daily(self, fetcher, access_token):
        """Test fetching daily historical data"""
        fetcher.authenticate(access_token)
        
        symbol = "NSE:RELIANCE-EQ"
        
        # Fetch last 10 days of daily data
        end_date = datetime(2025, 10, 11)  # Recent date
        start_date = datetime(2025, 10, 1)  # 10 days ago
        
        df = fetcher.fetch_historical_data(
            symbol=symbol,
            from_date=start_date,
            to_date=end_date,
            resolution='D'  # Daily
        )
        
        assert not df.empty
        assert 'timestamp' in df.columns
        assert 'open' in df.columns
        assert 'high' in df.columns
        assert 'low' in df.columns
        assert 'close' in df.columns
        assert 'volume' in df.columns
        
        # Should have data (market days only)
        assert len(df) > 0
        assert len(df) <= 10  # Max 10 days (some might be holidays)
        
        print(f"\n✅ Fetched {len(df)} days of data for {symbol}")
        print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    
    def test_fetch_historical_data_intraday(self, fetcher, access_token):
        """Test fetching 5-minute intraday data"""
        fetcher.authenticate(access_token)
        
        symbol = "NSE:RELIANCE-EQ"
        
        # Fetch last 3 days of 5-minute data
        end_date = datetime(2025, 10, 11)
        start_date = datetime(2025, 10, 8)
        
        df = fetcher.fetch_historical_data(
            symbol=symbol,
            from_date=start_date,
            to_date=end_date,
            resolution='5'  # 5-minute candles
        )
        
        assert not df.empty
        
        # Should have multiple candles per day
        assert len(df) > 10
        
        # Verify data quality
        assert (df['high'] >= df['low']).all()
        assert (df['high'] >= df['open']).all()
        assert (df['high'] >= df['close']).all()
        assert (df['low'] <= df['open']).all()
        assert (df['low'] <= df['close']).all()
        assert (df['volume'] >= 0).all()
        
        print(f"\n✅ Fetched {len(df)} 5-minute candles for {symbol}")
        print(f"Sample data:\n{df.head()}")
    
    def test_fetch_multiple_stocks(self, fetcher, access_token):
        """Test fetching data for multiple stocks"""
        fetcher.authenticate(access_token)
        
        symbols = ["NSE:RELIANCE-EQ", "NSE:TCS-EQ"]
        end_date = datetime(2025, 10, 11)
        start_date = datetime(2025, 10, 10)
        
        results = fetcher.fetch_multiple_stocks(
            symbols=symbols,
            from_date=start_date,
            to_date=end_date,
            resolution='D'
        )
        
        assert len(results) == 2
        
        for symbol, df in results.items():
            assert symbol in symbols
            assert not df.empty
            print(f"\n✅ Fetched {len(df)} records for {symbol}")
    
    def test_fetch_with_different_resolutions(self, fetcher, access_token):
        """Test fetching data with different time resolutions"""
        fetcher.authenticate(access_token)
        
        symbol = "NSE:RELIANCE-EQ"
        end_date = datetime(2025, 10, 11)
        start_date = datetime(2025, 10, 10)
        
        resolutions = ['1', '5', '15', '60', 'D']
        
        for resolution in resolutions:
            df = fetcher.fetch_historical_data(
                symbol=symbol,
                from_date=start_date,
                to_date=end_date,
                resolution=resolution
            )
            
            if not df.empty:
                print(f"\n✅ Resolution {resolution}: {len(df)} candles")
                assert 'timestamp' in df.columns
                assert 'close' in df.columns


class TestDataValidation:
    """Test data validation and quality checks"""
    
    def test_data_completeness(self, fetcher, access_token):
        """Test that fetched data has all required columns"""
        fetcher.authenticate(access_token)
        
        symbol = "NSE:RELIANCE-EQ"
        end_date = datetime(2025, 10, 11)
        start_date = datetime(2025, 10, 10)
        
        df = fetcher.fetch_historical_data(symbol, start_date, end_date, 'D')
        
        required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        
        for col in required_columns:
            assert col in df.columns, f"Missing column: {col}"
    
    def test_ohlc_consistency(self, fetcher, access_token):
        """Test OHLC data consistency"""
        fetcher.authenticate(access_token)
        
        symbol = "NSE:RELIANCE-EQ"
        end_date = datetime(2025, 10, 11)
        start_date = datetime(2025, 10, 8)
        
        df = fetcher.fetch_historical_data(symbol, start_date, end_date, '5')
        
        if not df.empty:
            # High should be >= all other prices
            assert (df['high'] >= df['open']).all()
            assert (df['high'] >= df['close']).all()
            assert (df['high'] >= df['low']).all()
            
            # Low should be <= all other prices
            assert (df['low'] <= df['open']).all()
            assert (df['low'] <= df['close']).all()
            assert (df['low'] <= df['high']).all()
    
    def test_no_duplicate_timestamps(self, fetcher, access_token):
        """Test that there are no duplicate timestamps"""
        fetcher.authenticate(access_token)
        
        symbol = "NSE:RELIANCE-EQ"
        end_date = datetime(2025, 10, 11)
        start_date = datetime(2025, 10, 8)
        
        df = fetcher.fetch_historical_data(symbol, start_date, end_date, '5')
        
        if not df.empty:
            # Check for duplicates
            duplicates = df['timestamp'].duplicated().sum()
            assert duplicates == 0, f"Found {duplicates} duplicate timestamps"


class TestErrorHandling:
    """Test error handling"""
    
    def test_invalid_symbol(self, fetcher, access_token):
        """Test fetching data for invalid symbol"""
        fetcher.authenticate(access_token)
        
        symbol = "INVALID:SYMBOL-EQ"
        end_date = datetime(2025, 10, 11)
        start_date = datetime(2025, 10, 10)
        
        df = fetcher.fetch_historical_data(symbol, start_date, end_date, 'D')
        
        # Should return empty DataFrame or handle gracefully
        assert isinstance(df, pd.DataFrame)
    
    def test_future_dates(self, fetcher, access_token):
        """Test fetching data for future dates"""
        fetcher.authenticate(access_token)
        
        symbol = "NSE:RELIANCE-EQ"
        
        # Try to fetch future data
        start_date = datetime(2026, 1, 1)
        end_date = datetime(2026, 1, 10)
        
        df = fetcher.fetch_historical_data(symbol, start_date, end_date, 'D')
        
        # Should return empty DataFrame
        assert df.empty or len(df) == 0
    
    def test_invalid_date_range(self, fetcher, access_token):
        """Test with end_date before start_date"""
        fetcher.authenticate(access_token)
        
        symbol = "NSE:RELIANCE-EQ"
        start_date = datetime(2025, 10, 11)
        end_date = datetime(2025, 10, 1)  # Before start_date
        
        df = fetcher.fetch_historical_data(symbol, start_date, end_date, 'D')
        
        # Should handle gracefully
        assert isinstance(df, pd.DataFrame)


class TestRateLimiting:
    """Test rate limiting behavior"""
    
    def test_multiple_requests_with_delay(self, fetcher, access_token):
        """Test that rate limiting delay works"""
        fetcher.authenticate(access_token)
        
        symbol = "NSE:RELIANCE-EQ"
        end_date = datetime(2025, 10, 11)
        start_date = datetime(2025, 10, 10)
        
        import time
        
        # Make 3 requests
        start_time = time.time()
        
        for i in range(3):
            df = fetcher.fetch_historical_data(symbol, start_date, end_date, 'D')
            assert not df.empty
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should take at least 2 seconds (1 second delay between requests)
        # But not too long (< 10 seconds)
        assert elapsed >= 2.0
        assert elapsed < 10.0
        
        print(f"\n✅ 3 requests completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    # Run with verbose output
    pytest.main([__file__, "-v", "-s"])

