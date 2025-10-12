"""
Test suite for database module
"""

import sys
import os
import pytest
import pandas as pd
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.database import Database
import config


@pytest.fixture
def db():
    """Create a test database instance"""
    # Use a test database
    test_db_path = "data/test_ptip.db"
    
    # Remove test database if it exists
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    # Create test database
    db = Database(db_path=test_db_path)
    yield db
    
    # Cleanup
    db.close()
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


@pytest.fixture
def sample_price_data():
    """Create sample price data for testing"""
    dates = pd.date_range(start='2025-10-01', periods=10, freq='5min')
    data = {
        'timestamp': dates,
        'open': [1300 + i for i in range(10)],
        'high': [1310 + i for i in range(10)],
        'low': [1290 + i for i in range(10)],
        'close': [1305 + i for i in range(10)],
        'volume': [100000 + i*1000 for i in range(10)]
    }
    return pd.DataFrame(data)


class TestDatabaseCreation:
    """Test database creation and initialization"""
    
    def test_database_creation(self, db):
        """Test that database is created successfully"""
        assert db.conn is not None
        assert os.path.exists(db.db_path)
    
    def test_tables_exist(self, db):
        """Test that all required tables are created"""
        cursor = db.conn.cursor()
        
        # Check stocks table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stocks'")
        assert cursor.fetchone() is not None
        
        # Check price_data table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='price_data'")
        assert cursor.fetchone() is not None
        
        # Check signals table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='signals'")
        assert cursor.fetchone() is not None
        
        # Check trades table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trades'")
        assert cursor.fetchone() is not None


class TestStockOperations:
    """Test stock CRUD operations"""
    
    def test_add_stock(self, db):
        """Test adding a stock"""
        result = db.add_stock("NSE:RELIANCE-EQ", "Reliance Industries", "NSE")
        assert result is True
        
        # Verify stock was added
        cursor = db.conn.cursor()
        cursor.execute("SELECT * FROM stocks WHERE symbol = ?", ("NSE:RELIANCE-EQ",))
        stock = cursor.fetchone()
        assert stock is not None
        assert stock[1] == "NSE:RELIANCE-EQ"
        assert stock[2] == "Reliance Industries"
    
    def test_add_duplicate_stock(self, db):
        """Test that duplicate stocks are handled gracefully"""
        db.add_stock("NSE:RELIANCE-EQ", "Reliance Industries", "NSE")
        result = db.add_stock("NSE:RELIANCE-EQ", "Reliance Industries", "NSE")
        
        # Should still return True (idempotent)
        assert result is True
        
        # Verify only one entry exists
        cursor = db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM stocks WHERE symbol = ?", ("NSE:RELIANCE-EQ",))
        count = cursor.fetchone()[0]
        assert count == 1
    
    def test_get_all_stocks(self, db):
        """Test retrieving all stocks"""
        db.add_stock("NSE:RELIANCE-EQ", "Reliance Industries", "NSE")
        db.add_stock("NSE:TCS-EQ", "TCS", "NSE")
        
        stocks = db.get_all_stocks()
        assert len(stocks) == 2
        assert stocks[0][1] in ["NSE:RELIANCE-EQ", "NSE:TCS-EQ"]


class TestPriceDataOperations:
    """Test price data CRUD operations"""
    
    def test_insert_price_data(self, db, sample_price_data):
        """Test inserting price data"""
        # Add stock first
        db.add_stock("NSE:RELIANCE-EQ", "Reliance Industries", "NSE")
        
        # Insert price data
        result = db.insert_price_data(sample_price_data, "NSE:RELIANCE-EQ")
        assert result is True
        
        # Verify data was inserted
        cursor = db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM price_data WHERE symbol = ?", ("NSE:RELIANCE-EQ",))
        count = cursor.fetchone()[0]
        assert count == 10
    
    def test_retrieve_price_data(self, db, sample_price_data):
        """Test retrieving price data"""
        # Add stock and price data
        db.add_stock("NSE:RELIANCE-EQ", "Reliance Industries", "NSE")
        db.insert_price_data(sample_price_data, "NSE:RELIANCE-EQ")
        
        # Retrieve data
        df = db.get_price_data("NSE:RELIANCE-EQ")
        
        assert len(df) == 10
        assert 'timestamp' in df.columns
        assert 'open' in df.columns
        assert 'close' in df.columns
        assert df['close'].iloc[0] == 1305
    
    def test_retrieve_price_data_with_date_range(self, db, sample_price_data):
        """Test retrieving price data with date range"""
        db.add_stock("NSE:RELIANCE-EQ", "Reliance Industries", "NSE")
        db.insert_price_data(sample_price_data, "NSE:RELIANCE-EQ")
        
        # Get data for specific date range
        start_date = datetime(2025, 10, 1, 0, 10)
        end_date = datetime(2025, 10, 1, 0, 30)
        
        df = db.get_price_data("NSE:RELIANCE-EQ", start_date, end_date)
        
        # Should get fewer records
        assert len(df) < 10
        assert len(df) > 0
    
    def test_duplicate_price_data_handling(self, db, sample_price_data):
        """Test that duplicate price data is handled (should replace)"""
        db.add_stock("NSE:RELIANCE-EQ", "Reliance Industries", "NSE")
        
        # Insert same data twice
        db.insert_price_data(sample_price_data, "NSE:RELIANCE-EQ")
        db.insert_price_data(sample_price_data, "NSE:RELIANCE-EQ")
        
        # Should still have only 10 records (duplicates replaced)
        cursor = db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM price_data WHERE symbol = ?", ("NSE:RELIANCE-EQ",))
        count = cursor.fetchone()[0]
        assert count == 10


class TestSignalOperations:
    """Test signal storage and retrieval"""
    
    def test_insert_signal(self, db):
        """Test inserting a signal"""
        db.add_stock("NSE:RELIANCE-EQ", "Reliance Industries", "NSE")
        
        signal_data = {
            'symbol': 'NSE:RELIANCE-EQ',
            'timestamp': datetime.now(),
            'signal_type': 'BUY',
            'price': 1350.50,
            'confidence': 0.85,
            'rsi': 28.5,
            'ma20': 1340.0,
            'ma50': 1330.0
        }
        
        result = db.insert_signal(signal_data)
        assert result is True
        
        # Verify signal was inserted
        cursor = db.conn.cursor()
        cursor.execute("SELECT * FROM signals WHERE symbol = ?", ("NSE:RELIANCE-EQ",))
        signal = cursor.fetchone()
        assert signal is not None
        assert signal[2] == 'BUY'
        assert signal[4] == 0.85


class TestPerformance:
    """Test database performance with larger datasets"""
    
    def test_large_insert_performance(self, db):
        """Test inserting 1000 records"""
        db.add_stock("NSE:RELIANCE-EQ", "Reliance Industries", "NSE")
        
        # Create 1000 records
        dates = pd.date_range(start='2025-09-01', periods=1000, freq='5min')
        data = {
            'timestamp': dates,
            'open': [1300 + i*0.1 for i in range(1000)],
            'high': [1310 + i*0.1 for i in range(1000)],
            'low': [1290 + i*0.1 for i in range(1000)],
            'close': [1305 + i*0.1 for i in range(1000)],
            'volume': [100000 + i*100 for i in range(1000)]
        }
        df = pd.DataFrame(data)
        
        # Insert and measure time
        import time
        start_time = time.time()
        result = db.insert_price_data(df, "NSE:RELIANCE-EQ")
        end_time = time.time()
        
        assert result is True
        
        # Should complete in reasonable time (< 5 seconds)
        assert (end_time - start_time) < 5.0
        
        # Verify count
        cursor = db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM price_data WHERE symbol = ?", ("NSE:RELIANCE-EQ",))
        count = cursor.fetchone()[0]
        assert count == 1000
    
    def test_query_performance(self, db):
        """Test query performance on 1000 records"""
        db.add_stock("NSE:RELIANCE-EQ", "Reliance Industries", "NSE")
        
        # Insert 1000 records
        dates = pd.date_range(start='2025-09-01', periods=1000, freq='5min')
        data = {
            'timestamp': dates,
            'open': [1300 + i*0.1 for i in range(1000)],
            'high': [1310 + i*0.1 for i in range(1000)],
            'low': [1290 + i*0.1 for i in range(1000)],
            'close': [1305 + i*0.1 for i in range(1000)],
            'volume': [100000 + i*100 for i in range(1000)]
        }
        df = pd.DataFrame(data)
        db.insert_price_data(df, "NSE:RELIANCE-EQ")
        
        # Query and measure time
        import time
        start_time = time.time()
        result_df = db.get_price_data("NSE:RELIANCE-EQ")
        end_time = time.time()
        
        assert len(result_df) == 1000
        
        # Should complete in reasonable time (< 1 second)
        assert (end_time - start_time) < 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

