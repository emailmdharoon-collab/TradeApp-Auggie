"""
Simple Fyers API test - direct API call
"""

from fyers_apiv3 import fyersModel
from datetime import datetime, timedelta

# Read access token
with open('fyers_access_token.txt', 'r') as f:
    access_token = f.read().strip()

print("Testing Fyers API...")
print(f"Access Token: {access_token[:30]}...")

# Initialize Fyers model
fyers = fyersModel.FyersModel(
    client_id="8LH008CGEA-100",
    token=access_token,
    log_path=""
)

# Test 1: Get quote (current price)
print("\n" + "="*70)
print("TEST 1: Get Current Quote")
print("="*70)

try:
    data = {"symbols": "NSE:RELIANCE-EQ"}
    response = fyers.quotes(data=data)
    print(f"Response: {response}")
    
    if response['s'] == 'ok':
        print("✅ Quote fetch successful!")
        quote_data = response['d'][0]
        print(f"\nSymbol: {quote_data['n']}")
        print(f"LTP: ₹{quote_data['v']['lp']}")
        print(f"Open: ₹{quote_data['v']['open_price']}")
        print(f"High: ₹{quote_data['v']['high_price']}")
        print(f"Low: ₹{quote_data['v']['low_price']}")
    else:
        print(f"❌ Error: {response.get('message', 'Unknown error')}")
except Exception as e:
    print(f"❌ Exception: {e}")

# Test 2: Get historical data
print("\n" + "="*70)
print("TEST 2: Get Historical Data")
print("="*70)

try:
    # Use dates from 3 months ago
    end_date = datetime(2024, 11, 30)  # Nov 30, 2024
    start_date = datetime(2024, 11, 25)  # Nov 25, 2024
    
    from_timestamp = int(start_date.timestamp())
    to_timestamp = int(end_date.timestamp())
    
    print(f"From: {start_date} (timestamp: {from_timestamp})")
    print(f"To: {end_date} (timestamp: {to_timestamp})")
    
    data = {
        "symbol": "NSE:RELIANCE-EQ",
        "resolution": "D",  # Daily data
        "date_format": "1",
        "range_from": from_timestamp,
        "range_to": to_timestamp,
        "cont_flag": "1"
    }
    
    response = fyers.history(data=data)
    print(f"\nResponse status: {response['s']}")
    
    if response['s'] == 'ok':
        print("✅ Historical data fetch successful!")
        candles = response['candles']
        print(f"Records fetched: {len(candles)}")
        
        if len(candles) > 0:
            print("\nFirst 3 candles:")
            for i, candle in enumerate(candles[:3]):
                dt = datetime.fromtimestamp(candle[0])
                print(f"{i+1}. {dt} - O:{candle[1]} H:{candle[2]} L:{candle[3]} C:{candle[4]} V:{candle[5]}")
    else:
        print(f"❌ Error: {response.get('message', 'Unknown error')}")
        print(f"Full response: {response}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("Test completed!")
print("="*70)

