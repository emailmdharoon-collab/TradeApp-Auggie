"""
Fyers API Authentication Helper
Generates access token for Fyers API access
"""

import config
from fyers_apiv3 import fyersModel
import webbrowser
from urllib.parse import urlparse, parse_qs

print("="*70)
print("FYERS API AUTHENTICATION")
print("="*70)

# Validate configuration
if not config.validate_config():
    print("\n❌ Configuration validation failed!")
    exit(1)

print(f"\n📋 Configuration:")
print(f"   Client ID: {config.FYERS_CLIENT_ID}")
print(f"   Redirect URI: {config.FYERS_REDIRECT_URI}")

# Create session model
session = fyersModel.SessionModel(
    client_id=config.FYERS_CLIENT_ID,
    secret_key=config.FYERS_SECRET_KEY,
    redirect_uri=config.FYERS_REDIRECT_URI,
    response_type="code",
    grant_type="authorization_code"
)

# Generate auth code URL
auth_url = session.generate_authcode()

print("\n" + "="*70)
print("STEP 1: AUTHORIZE APPLICATION")
print("="*70)
print("\n🌐 Opening browser for Fyers login...")
print(f"\nIf browser doesn't open automatically, visit this URL:")
print(f"\n{auth_url}\n")

# Open browser
try:
    webbrowser.open(auth_url)
    print("✅ Browser opened successfully")
except Exception as e:
    print(f"⚠️  Could not open browser automatically: {e}")
    print("Please copy the URL above and paste it in your browser")

print("\n" + "="*70)
print("STEP 2: GET AUTHORIZATION CODE")
print("="*70)
print("\nAfter logging in to Fyers:")
print("1. You'll be redirected to a page")
print("2. Look at the URL in your browser's address bar")
print("3. The URL will contain '?auth_code=XXXXX' or '&auth_code=XXXXX'")
print("4. Copy the ENTIRE URL from your browser")
print("\nExample URL:")
print("https://trade.fyers.in/api-login/redirect-uri/index.html?auth_code=eyJ0eXAiOiJKV1...")

print("\n" + "="*70)
auth_code_url = input("\n📋 Paste the FULL redirect URL here: ").strip()

# Extract auth code from URL
try:
    parsed_url = urlparse(auth_code_url)
    query_params = parse_qs(parsed_url.query)
    
    if 'auth_code' in query_params:
        auth_code = query_params['auth_code'][0]
        print(f"\n✅ Auth code extracted: {auth_code[:20]}...")
    else:
        print("\n❌ Could not find 'auth_code' in the URL")
        print("Please make sure you copied the complete URL after login")
        exit(1)
        
except Exception as e:
    print(f"\n❌ Error parsing URL: {e}")
    print("Please make sure you pasted the complete redirect URL")
    exit(1)

# Set auth code
session.set_token(auth_code)

# Generate access token
print("\n" + "="*70)
print("STEP 3: GENERATE ACCESS TOKEN")
print("="*70)
print("\n🔄 Exchanging auth code for access token...")

try:
    response = session.generate_token()
    
    if 'access_token' in response:
        access_token = response['access_token']
        print(f"\n✅ ACCESS TOKEN GENERATED SUCCESSFULLY!")
        print(f"\n🔑 Your Access Token:")
        print(f"{access_token}")
        
        # Save to file for easy access
        with open('fyers_access_token.txt', 'w') as f:
            f.write(access_token)
        
        print(f"\n💾 Token saved to: fyers_access_token.txt")
        
        print("\n" + "="*70)
        print("NEXT STEPS")
        print("="*70)
        print("\n1. Copy the access token above")
        print("2. Use it in your data fetching scripts")
        print("3. Token is valid for 24 hours")
        print("4. Re-run this script when token expires")
        
        print("\n✅ Authentication completed successfully!")
        
    else:
        print(f"\n❌ Failed to generate access token")
        print(f"Response: {response}")
        
except Exception as e:
    print(f"\n❌ Error generating access token: {e}")
    print("\nPossible issues:")
    print("- Auth code may have expired (they expire quickly)")
    print("- Network connectivity issues")
    print("- Invalid credentials")
    print("\nTry running the script again")

print("\n" + "="*70)

