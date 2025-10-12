"""
PTIP - Personal Trading Intelligence Platform
Streamlit Dashboard for Scalping Options Strategy
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add modules to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.database import Database
from modules.indicators import add_all_indicators
from modules.strategy import ScalpingStrategy
import config

# Page configuration
st.set_page_config(
    page_title="PTIP - Trading Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .buy-signal {
        color: #00ff00;
        font-weight: bold;
    }
    .sell-signal {
        color: #ff0000;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database and strategy
@st.cache_resource
def init_components():
    """Initialize database and strategy (cached)"""
    db = Database()
    strategy = ScalpingStrategy()
    return db, strategy

# Load stock data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_stock_data(symbol):
    """Load price data for a stock"""
    db, _ = init_components()
    df = db.get_price_data(symbol)
    return df

# Calculate indicators and signals
@st.cache_data(ttl=300)
def calculate_indicators_and_signals(symbol):
    """Calculate indicators and generate signals"""
    db, strategy = init_components()
    
    # Load data
    df = db.get_price_data(symbol)
    
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
    
    # Add indicators
    df_with_indicators = add_all_indicators(df.copy())
    
    # Generate signals
    signals_df = strategy.generate_signals(df_with_indicators.copy())
    
    return df_with_indicators, signals_df

# Main app
def main():
    # Header
    st.markdown('<div class="main-header">📈 PTIP Trading Dashboard</div>', unsafe_allow_html=True)
    st.markdown("**Personal Trading Intelligence Platform** - Scalping Options Strategy")
    
    # Sidebar
    st.sidebar.title("⚙️ Controls")
    
    # Stock selector
    db, _ = init_components()
    stocks_df = db.get_all_stocks()
    
    if stocks_df.empty:
        st.error("No stocks found in database. Please run data fetching script first.")
        return
    
    stock_options = {f"{row['name']} ({row['symbol']})": row['symbol'] 
                    for _, row in stocks_df.iterrows()}
    
    selected_stock_display = st.sidebar.selectbox(
        "Select Stock",
        options=list(stock_options.keys())
    )
    selected_symbol = stock_options[selected_stock_display]
    
    # Date range filter
    st.sidebar.subheader("📅 Date Range")
    df_raw = load_stock_data(selected_symbol)
    
    if df_raw.empty:
        st.error(f"No data found for {selected_symbol}")
        return
    
    min_date = df_raw['timestamp'].min().date()
    max_date = df_raw['timestamp'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(max_date - timedelta(days=7), max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Indicator toggles
    st.sidebar.subheader("📊 Indicators")
    show_ma20 = st.sidebar.checkbox("MA20", value=True)
    show_ma50 = st.sidebar.checkbox("MA50", value=True)
    show_rsi = st.sidebar.checkbox("RSI", value=True)
    show_signals = st.sidebar.checkbox("Show Signals", value=True)
    
    # Load data with indicators
    df_with_indicators, signals_df = calculate_indicators_and_signals(selected_symbol)
    
    # Filter by date range
    if len(date_range) == 2:
        start_date, end_date = date_range
        mask = (df_with_indicators['timestamp'].dt.date >= start_date) & \
               (df_with_indicators['timestamp'].dt.date <= end_date)
        df_filtered = df_with_indicators[mask].copy()
        
        # Filter signals too
        if not signals_df.empty:
            signals_mask = (signals_df['timestamp'].dt.date >= start_date) & \
                          (signals_df['timestamp'].dt.date <= end_date)
            signals_filtered = signals_df[signals_mask].copy()
        else:
            signals_filtered = signals_df
    else:
        df_filtered = df_with_indicators
        signals_filtered = signals_df
    
    # Metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Candles", f"{len(df_filtered):,}")
    
    with col2:
        if not df_filtered.empty:
            price_change = df_filtered['close'].iloc[-1] - df_filtered['close'].iloc[0]
            price_change_pct = (price_change / df_filtered['close'].iloc[0]) * 100
            st.metric("Price Change", f"₹{price_change:.2f}", f"{price_change_pct:+.2f}%")
    
    with col3:
        if not df_filtered.empty:
            st.metric("Current Price", f"₹{df_filtered['close'].iloc[-1]:.2f}")
    
    with col4:
        buy_count = len(signals_filtered[signals_filtered['action'] == 'BUY']) if not signals_filtered.empty else 0
        st.metric("BUY Signals", buy_count)
    
    with col5:
        sell_count = len(signals_filtered[signals_filtered['action'] == 'SELL']) if not signals_filtered.empty else 0
        st.metric("SELL Signals", sell_count)
    
    # Main chart
    st.subheader(f"📊 {selected_stock_display} - Price Chart")
    
    if df_filtered.empty:
        st.warning("No data available for selected date range")
        return
    
    # Create candlestick chart
    fig = go.Figure()
    
    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df_filtered['timestamp'],
        open=df_filtered['open'],
        high=df_filtered['high'],
        low=df_filtered['low'],
        close=df_filtered['close'],
        name='Price',
        increasing_line_color='#00ff00',
        decreasing_line_color='#ff0000'
    ))
    
    # Add MA20
    if show_ma20 and 'ma_20' in df_filtered.columns:
        fig.add_trace(go.Scatter(
            x=df_filtered['timestamp'],
            y=df_filtered['ma_20'],
            name='MA20',
            line=dict(color='blue', width=1)
        ))
    
    # Add MA50
    if show_ma50 and 'ma_50' in df_filtered.columns:
        fig.add_trace(go.Scatter(
            x=df_filtered['timestamp'],
            y=df_filtered['ma_50'],
            name='MA50',
            line=dict(color='orange', width=1)
        ))
    
    # Add BUY signals
    if show_signals and not signals_filtered.empty:
        buy_signals = signals_filtered[signals_filtered['action'] == 'BUY']
        if not buy_signals.empty:
            fig.add_trace(go.Scatter(
                x=buy_signals['timestamp'],
                y=buy_signals['price'],
                mode='markers',
                name='BUY',
                marker=dict(
                    symbol='triangle-up',
                    size=15,
                    color='green',
                    line=dict(color='darkgreen', width=2)
                )
            ))
        
        # Add SELL signals
        sell_signals = signals_filtered[signals_filtered['action'] == 'SELL']
        if not sell_signals.empty:
            fig.add_trace(go.Scatter(
                x=sell_signals['timestamp'],
                y=sell_signals['price'],
                mode='markers',
                name='SELL',
                marker=dict(
                    symbol='triangle-down',
                    size=15,
                    color='red',
                    line=dict(color='darkred', width=2)
                )
            ))
    
    # Update layout
    fig.update_layout(
        height=600,
        xaxis_title="Time",
        yaxis_title="Price (₹)",
        hovermode='x unified',
        xaxis_rangeslider_visible=False,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # RSI Chart
    if show_rsi and 'rsi' in df_filtered.columns:
        st.subheader("📉 RSI Indicator")
        
        fig_rsi = go.Figure()
        
        fig_rsi.add_trace(go.Scatter(
            x=df_filtered['timestamp'],
            y=df_filtered['rsi'],
            name='RSI',
            line=dict(color='purple', width=2)
        ))
        
        # Add overbought/oversold lines
        fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
        fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
        
        fig_rsi.update_layout(
            height=250,
            xaxis_title="Time",
            yaxis_title="RSI",
            hovermode='x unified',
            template='plotly_white',
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig_rsi, use_container_width=True)
    
    # Signal History Table
    if show_signals and not signals_filtered.empty:
        st.subheader("📋 Recent Signals")
        
        # Format signals for display
        signals_display = signals_filtered[['timestamp', 'action', 'price', 'confidence']].copy()
        signals_display = signals_display.sort_values('timestamp', ascending=False).head(20)
        signals_display['timestamp'] = signals_display['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        signals_display['price'] = signals_display['price'].apply(lambda x: f"₹{x:.2f}")
        signals_display['confidence'] = signals_display['confidence'].apply(lambda x: f"{x:.2%}")
        signals_display.columns = ['Time', 'Signal', 'Price', 'Confidence']
        
        st.dataframe(signals_display, use_container_width=True, hide_index=True)
    
    # Footer
    st.markdown("---")
    st.markdown(f"**Data Range:** {min_date} to {max_date} | **Total Records:** {len(df_raw):,} | **Resolution:** 5-minute candles")
    st.markdown("*PTIP Ultra-MVP - For educational purposes only. Not financial advice.*")


if __name__ == "__main__":
    main()

