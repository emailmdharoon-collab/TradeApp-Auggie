"""
Database module for PTIP
Handles SQLite database operations for storing price data, signals, and trades
"""

import sqlite3
import pandas as pd
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class Database:
    """Database handler for PTIP application"""
    
    def __init__(self, db_path=None):
        """
        Initialize database connection
        
        Args:
            db_path (str): Path to SQLite database file. If None, uses config.DB_PATH
        """
        self.db_path = db_path or config.DB_PATH
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Connect to database
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        
        # Create tables
        self.create_tables()
        
        print(f"✅ Database initialized: {self.db_path}")
    
    def create_tables(self):
        """Create all necessary database tables"""
        cursor = self.conn.cursor()
        
        # Stocks table - stores stock information
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                symbol TEXT PRIMARY KEY,
                name TEXT,
                exchange TEXT,
                added_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Price data table - stores historical OHLCV data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                open REAL NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL,
                close REAL NOT NULL,
                volume INTEGER,
                UNIQUE(symbol, timestamp),
                FOREIGN KEY (symbol) REFERENCES stocks(symbol)
            )
        ''')
        
        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_price_data_symbol_timestamp 
            ON price_data(symbol, timestamp)
        ''')
        
        # Signals table - stores trading signals
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                strategy TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                action TEXT NOT NULL,
                price REAL NOT NULL,
                confidence REAL,
                executed BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (symbol) REFERENCES stocks(symbol)
            )
        ''')
        
        # Trades table - stores executed trades (for future use)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                strategy TEXT NOT NULL,
                entry_time DATETIME NOT NULL,
                exit_time DATETIME,
                entry_price REAL NOT NULL,
                exit_price REAL,
                quantity INTEGER NOT NULL,
                pnl REAL,
                status TEXT DEFAULT 'OPEN',
                FOREIGN KEY (symbol) REFERENCES stocks(symbol)
            )
        ''')
        
        self.conn.commit()
        print("✅ Database tables created/verified")
    
    def add_stock(self, symbol, name=None, exchange=None):
        """
        Add a stock to the stocks table
        
        Args:
            symbol (str): Stock symbol (e.g., 'NSE:RELIANCE-EQ')
            name (str): Stock name (optional)
            exchange (str): Exchange name (optional)
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO stocks (symbol, name, exchange)
                VALUES (?, ?, ?)
            ''', (symbol, name, exchange))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error adding stock {symbol}: {e}")
            return False
    
    def insert_price_data(self, df, symbol):
        """
        Insert price data from DataFrame into database
        
        Args:
            df (pd.DataFrame): DataFrame with columns: timestamp, open, high, low, close, volume
            symbol (str): Stock symbol
        """
        try:
            # Add symbol column
            df_copy = df.copy()
            df_copy['symbol'] = symbol
            
            # Ensure timestamp is in correct format
            if 'timestamp' in df_copy.columns:
                df_copy['timestamp'] = pd.to_datetime(df_copy['timestamp'])
            
            # Insert data (ignore duplicates)
            df_copy.to_sql('price_data', self.conn, if_exists='append', index=False)
            
            print(f"✅ Inserted {len(df_copy)} records for {symbol}")
            return True
        except Exception as e:
            print(f"❌ Error inserting price data for {symbol}: {e}")
            return False
    
    def get_price_data(self, symbol, start_date=None, end_date=None, limit=None):
        """
        Retrieve price data for a symbol
        
        Args:
            symbol (str): Stock symbol
            start_date (str): Start date (YYYY-MM-DD format)
            end_date (str): End date (YYYY-MM-DD format)
            limit (int): Maximum number of records to return
            
        Returns:
            pd.DataFrame: Price data
        """
        query = f"SELECT * FROM price_data WHERE symbol = '{symbol}'"
        
        if start_date:
            query += f" AND timestamp >= '{start_date}'"
        if end_date:
            query += f" AND timestamp <= '{end_date}'"
        
        query += " ORDER BY timestamp ASC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        try:
            df = pd.read_sql_query(query, self.conn)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            print(f"❌ Error retrieving price data for {symbol}: {e}")
            return pd.DataFrame()
    
    def insert_signal(self, symbol, strategy, timestamp, action, price, confidence=None):
        """
        Insert a trading signal into the database
        
        Args:
            symbol (str): Stock symbol
            strategy (str): Strategy name
            timestamp (datetime): Signal timestamp
            action (str): 'BUY', 'SELL', or 'HOLD'
            price (float): Price at signal
            confidence (float): Signal confidence (0-1)
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO signals (symbol, strategy, timestamp, action, price, confidence)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (symbol, strategy, timestamp, action, price, confidence))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error inserting signal: {e}")
            return False
    
    def get_signals(self, symbol=None, strategy=None, limit=None):
        """
        Retrieve trading signals
        
        Args:
            symbol (str): Filter by symbol (optional)
            strategy (str): Filter by strategy (optional)
            limit (int): Maximum number of records
            
        Returns:
            pd.DataFrame: Signals data
        """
        query = "SELECT * FROM signals WHERE 1=1"
        
        if symbol:
            query += f" AND symbol = '{symbol}'"
        if strategy:
            query += f" AND strategy = '{strategy}'"
        
        query += " ORDER BY timestamp DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        try:
            df = pd.read_sql_query(query, self.conn)
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            print(f"❌ Error retrieving signals: {e}")
            return pd.DataFrame()
    
    def get_all_stocks(self):
        """Get list of all stocks in database"""
        try:
            df = pd.read_sql_query("SELECT * FROM stocks", self.conn)
            return df
        except Exception as e:
            print(f"❌ Error retrieving stocks: {e}")
            return pd.DataFrame()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✅ Database connection closed")
    
    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()


# Test function
if __name__ == "__main__":
    print("Testing Database module...")
    db = Database()
    
    # Test adding a stock
    db.add_stock("NSE:RELIANCE-EQ", "Reliance Industries", "NSE")
    
    # Test retrieving stocks
    stocks = db.get_all_stocks()
    print(f"\nStocks in database: {len(stocks)}")
    print(stocks)
    
    print("\n✅ Database module test completed!")

