# Fyers API V3 Documentation URLs and AI Agent Help Guide

## Complete List of Fyers API V3 Documentation URLs

Base URL: https://myapi.fyers.in/docsv3

### Main Sections

1. **Introduction**
   - URL: https://myapi.fyers.in/docsv3#section/Introduction
   - Description: Overview of Fyers API, security features, and introduction to REST-like APIs

2. **Libraries and SDKs**
   - URL: https://myapi.fyers.in/docsv3#section/Libraries-and-SDKs
   - Description: Available libraries for Python, Node.js, Web JS, C#, and Java

3. **Community**
   - URL: https://myapi.fyers.in/docsv3#section/Community
   - Description: Community resources and discussion forums

### General API Information

4. **Request & Response Structure**
   - URL: https://myapi.fyers.in/docsv3#tag/Request-and-Response-Structure
   - Description: Authorization headers, success/failure responses, HTTP status codes, error codes, rate limits

5. **App Creation**
   - URL: https://myapi.fyers.in/docsv3#tag/App-Creation
   - Description: Creating individual apps and third-party apps, redirect URI configuration

### Authentication & Login Flow

6. **Authentication & Login Flow - User Apps**
   - URL: https://myapi.fyers.in/docsv3#tag/Authentication-and-Login-Flow-User-Apps
   - Description: Complete authentication flow for individual user applications

7. **Authentication & Login Flow - Third Party Apps**
   - URL: https://myapi.fyers.in/docsv3#tag/Authentication-and-Login-Flow-Third-Party-Apps
   - Description: OAuth2 authentication flow for third-party applications

8. **Sample Code**
   - URL: https://myapi.fyers.in/docsv3#tag/Sample-Code
   - Description: Postman collections and sample scripts

### User Information

9. **User**
   - URL: https://myapi.fyers.in/docsv3#tag/User
   - Description: User profile, funds, holdings, and logout functionality

### Trading & Transactions

10. **Transaction Info**
    - URL: https://myapi.fyers.in/docsv3#tag/Transaction-Info
    - Description: Orders, trades, positions, and transaction history

11. **Order Placement Guide**
    - URL: https://myapi.fyers.in/docsv3#tag/Order-Placement-Guide
    - Description: Comprehensive guide for placing different types of orders

12. **Order Placement**
    - URL: https://myapi.fyers.in/docsv3#tag/Order-Placement
    - Description: API endpoints for placing, modifying, and canceling orders

13. **GTT Orders**
    - URL: https://myapi.fyers.in/docsv3#tag/GTT-Orders
    - Description: Good Till Triggered (GTT) order functionality

14. **Other Transactions**
    - URL: https://myapi.fyers.in/docsv3#tag/Other-Transactions
    - Description: Position conversion, exit positions, and other transaction types

15. **Margin Calculator**
    - URL: https://myapi.fyers.in/docsv3#tag/Margin-Calculator
    - Description: Calculate margin requirements for different instruments

16. **Broker Config**
    - URL: https://myapi.fyers.in/docsv3#tag/Broker-Config
    - Description: Broker configuration and settings

17. **EDIS**
    - URL: https://myapi.fyers.in/docsv3#tag/EDIS
    - Description: Electronic Delivery Instruction Slip functionality

18. **Postback (Webhooks)**
    - URL: https://myapi.fyers.in/docsv3#tag/Postback
    - Description: Webhook configuration for real-time updates

### Market Data

19. **Data API**
    - URL: https://myapi.fyers.in/docsv3#tag/Data-Api
    - Description: Historical data, quotes, and market depth APIs

20. **Web Socket**
    - URL: https://myapi.fyers.in/docsv3#tag/Web-Socket
    - Description: Real-time data streaming via WebSocket connections

21. **Order Websocket Usage Guide**
    - URL: https://myapi.fyers.in/docsv3#tag/Order-Websocket-Usage-Guide
    - Description: Real-time order updates via WebSocket

22. **Tick-by-Tick (TBT) Websocket Usage Guide**
    - URL: https://myapi.fyers.in/docsv3#tag/Tick-by-Tick-TBT-Websocket-Usage-Guide
    - Description: Live market data streaming with tick-by-tick updates

23. **True Data V2**
    - URL: https://myapi.fyers.in/docsv3#tag/True-Data-V2
    - Description: Enhanced market data services

### Reference Information

24. **Appendix**
    - URL: https://myapi.fyers.in/docsv3#tag/Appendix
    - Description: Reference data including exchanges, segments, instrument types, fytoken format

25. **Change Log**
    - URL: https://myapi.fyers.in/docsv3#tag/Change-Log
    - Description: API version history and updates

---

## AI Agent Help Guide for Fyers API V3

### Authentication and Login Flow

#### For User Apps (Individual Applications)

**Step 1: Generate Auth Code**
- **Endpoint**: `GET https://api-t1.fyers.in/api/v3/generate-authcode`
- **Parameters**:
  - `client_id`: Your app_id (e.g., "qwerty-100")
  - `redirect_uri`: Your redirect URL
  - `response_type`: "code"
  - `state`: Random value for security

**Step 2: Validate Auth Code**
- **Endpoint**: `POST https://api-t1.fyers.in/api/v3/validate-authcode`
- **Headers**: `Content-Type: application/json`
- **Body**:
  ```json
  {
    "grant_type": "authorization_code",
    "appIdHash": "SHA-256 of api_id:app_secret",
    "code": "auth_code_from_step_1"
  }
  ```
- **Response**: Returns `access_token` and `refresh_token`

**Using Refresh Token**
- **Endpoint**: `POST https://api-t1.fyers.in/api/v3/validate-refresh-token`
- **Body**:
  ```json
  {
    "grant_type": "refresh_token",
    "appIdHash": "SHA-256 of api_id:app_secret",
    "refresh_token": "your_refresh_token",
    "pin": "user_pin"
  }
  ```

#### For Third Party Apps (OAuth2 Flow)

**Step 1: Redirect User for Authentication**
- Navigate user to: `https://api-t1.fyers.in/api/v3/generate-authcode?client_id={app_id}&redirect_uri={redirect_uri}&response_type=code&state={random_state}`

**Step 2: Handle Callback and Validate**
- **Endpoint**: `POST https://api-t1.fyers.in/api/v3/validate-authcode`
- Same payload as user apps but for third-party applications

#### Authentication Headers
All subsequent API calls require:
```
Authorization: api_id:access_token
```
Example: `Authorization: aaa-99:bbb`

### Market Data Access

#### Available Instrument Types

1. **Equity (Stocks)**
   - Exchange: NSE (10), BSE (11)
   - Symbol Format: `NSE:RELIANCE-EQ`
   - Segment: 10 (Equity)

2. **Futures & Options (F&O)**
   - Exchange: NSE (10), BSE (11)
   - Symbol Format: `NSE:NIFTY24DECFUT`, `NSE:NIFTY24DEC21000CE`
   - Segment: 11 (Derivatives)

3. **Currency**
   - Exchange: NSE (10)
   - Symbol Format: `NSE:USDINR24DECFUT`
   - Segment: 12 (Currency)

4. **Commodities**
   - Exchange: MCX (20)
   - Symbol Format: `MCX:GOLD24DECFUT`
   - Segment: 20 (Commodity)

#### Market Data APIs

**1. Historical Data**
- **Endpoint**: `GET https://api-t1.fyers.in/data-rest/v3/historical/{symbol}`
- **Parameters**:
  - `symbol`: Instrument symbol
  - `resolution`: 1, 2, 3, 5, 10, 15, 30, 45, 60, 120, 180, 240, 1D
  - `date_format`: 0 (timestamp) or 1 (date string)
  - `range_from`: Start date
  - `range_to`: End date
  - `cont_flag`: 0 (normal) or 1 (continuous for F&O)

**2. Market Quotes**
- **Endpoint**: `GET https://api-t1.fyers.in/data-rest/v3/quotes`
- **Parameters**: `symbols={symbol1},{symbol2},...`

**3. Market Depth**
- **Endpoint**: `GET https://api-t1.fyers.in/data-rest/v3/depth`
- **Parameters**: `symbol={symbol}&ohlcv_flag=1`

**4. Real-time Data via WebSocket**

```python
# Python WebSocket Example
from fyers_apiv3.FyersWebsocket import data_ws

def onmessage(message):
    print("Response:", message)

def onerror(message):
    print("Error:", message)

def onclose(message):
    print("Connection closed:", message)

def onopen():
    data_type = "symbolData"
    symbols = ["NSE:RELIANCE-EQ", "NSE:NIFTY50-INDEX"]
    fyers.subscribe(symbols=symbols, data_type=data_type)

fyers = data_ws.FyersDataSocket(
    access_token="your_access_token",
    log_path="",
    litemode=False,
    onmessage=onmessage,
    onerror=onerror,
    onclose=onclose,
    onopen=onopen
)

fyers.connect()
```

#### Symbol Format Guidelines

**Equity**: `EXCHANGE:SYMBOL-EQ`
- Example: `NSE:RELIANCE-EQ`, `BSE:RELIANCE-EQ`

**Index**: `EXCHANGE:INDEX-INDEX`
- Example: `NSE:NIFTY50-INDEX`, `BSE:SENSEX-INDEX`

**Futures**: `EXCHANGE:SYMBOL{YY}{MMM}FUT`
- Example: `NSE:RELIANCE24DECFUT`, `MCX:GOLD24DECFUT`

**Options**: `EXCHANGE:SYMBOL{YY}{MMM}{STRIKE}{CE/PE}`
- Example: `NSE:NIFTY24DEC21000CE`, `NSE:RELIANCE24DEC2500PE`

**Currency**: `EXCHANGE:PAIR{YY}{MMM}FUT`
- Example: `NSE:USDINR24DECFUT`

### Best Practices for AI Agents

1. **Authentication Management**
   - Store app_secret securely
   - Implement refresh token mechanism
   - Handle token expiry gracefully

2. **Rate Limiting**
   - Per Second: 10 requests
   - Per Minute: 200 requests
   - Per Day: 1000 requests
   - Implement exponential backoff

3. **Error Handling**
   - Check for error codes: -8, -15, -16, -17 (token issues)
   - Handle HTTP status codes: 400, 401, 403, 429, 500
   - Implement retry logic for transient failures

4. **Data Processing**
   - Use fytoken for efficient symbol identification
   - Parse timestamp formats correctly
   - Handle market holidays and trading hours

5. **WebSocket Management**
   - Implement reconnection logic
   - Handle subscription/unsubscription properly
   - Monitor connection health

### Common Use Cases

1. **Portfolio Tracking**
   - Get holdings: `/api/v3/holdings`
   - Get positions: `/api/v3/positions`
   - Get funds: `/api/v3/funds`

2. **Market Analysis**
   - Historical data for backtesting
   - Real-time quotes for current prices
   - Market depth for order book analysis

3. **Automated Trading**
   - Order placement: `/api/v3/orders`
   - Order modification: `/api/v3/orders/{order_id}`
   - Position exit: `/api/v3/exit-positions`

4. **Risk Management**
   - Margin calculation before order placement
   - Real-time P&L monitoring
   - Stop-loss order management

####Symbol Master Json
You can get all the latest symbols of all the exchanges from the symbol master json files

NSE – Currency Derivatives:
https://public.fyers.in/sym_details/NSE_CD_sym_master.json
NSE – Equity Derivatives:
https://public.fyers.in/sym_details/NSE_FO_sym_master.json
NSE – Commodity:
https://public.fyers.in/sym_details/NSE_COM_sym_master.json
NSE – Capital Market:
https://public.fyers.in/sym_details/NSE_CM_sym_master.json
BSE – Capital Market:
https://public.fyers.in/sym_details/BSE_CM_sym_master.json
BSE - Equity Derivatives:
https://public.fyers.in/sym_details/BSE_FO_sym_master.json
MCX - Commodity:
https://public.fyers.in/sym_details/MCX_COM_sym_master.json

This guide provides comprehensive information for AI agents to effectively use the Fyers API V3 for authentication, market data access, and trading operations across all supported instruments including stocks, F&O, commodities, and currency derivatives.