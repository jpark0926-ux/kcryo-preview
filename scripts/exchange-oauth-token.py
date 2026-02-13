#!/usr/bin/env python3
"""
Exchange authorization code for tokens
"""
import json
import os
import sys
import requests

# Configuration
CREDENTIALS_PATH = os.path.expanduser("~/.openclaw/config/google-workspace-credentials.json")
TOKEN_PATH = os.path.expanduser("~/.openclaw/config/google-workspace-token.pickle")

def exchange_code_for_token(auth_code):
    """Exchange authorization code for access/refresh tokens"""
    
    # Load credentials
    with open(CREDENTIALS_PATH) as f:
        creds = json.load(f)['web']
    
    client_id = creds['client_id']
    client_secret = creds['client_secret']
    redirect_uri = creds['redirect_uris'][0]
    
    # Token endpoint
    token_url = "https://oauth2.googleapis.com/token"
    
    # Request payload
    data = {
        'code': auth_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    
    print("🔄 Exchanging authorization code for tokens...")
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        tokens = response.json()
        print("✅ Token exchange successful!")
        print(f"   Access token: {tokens['access_token'][:20]}...")
        print(f"   Refresh token: {'Present' if 'refresh_token' in tokens else 'Missing'}")
        print(f"   Expires in: {tokens.get('expires_in', 'N/A')} seconds")
        return tokens
    else:
        print(f"❌ Token exchange failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def save_tokens(tokens):
    """Save tokens to file"""
    import pickle
    
    # Create a simple token object
    class TokenStorage:
        def __init__(self, token_data):
            self.token = token_data['access_token']
            self.refresh_token = token_data.get('refresh_token')
            self.token_uri = "https://oauth2.googleapis.com/token"
            self.client_id = token_data.get('client_id', '')
            self.client_secret = token_data.get('client_secret', '')
            self.scopes = token_data.get('scope', '').split()
            
            # Calculate expiry
            import datetime
            expires_in = token_data.get('expires_in', 3600)
            self.expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    
    token_storage = TokenStorage(tokens)
    
    with open(TOKEN_PATH, 'wb') as f:
        pickle.dump(token_storage, f)
    
    os.chmod(TOKEN_PATH, 0o600)
    print(f"✅ Tokens saved to: {TOKEN_PATH}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 exchange-token.py '<auth_code>'")
        print("Note: Include the full code including any special characters")
        sys.exit(1)
    
    auth_code = sys.argv[1]
    # Remove &scope=... if included
    if '&' in auth_code:
        auth_code = auth_code.split('&')[0]
    
    tokens = exchange_code_for_token(auth_code)
    if tokens:
        save_tokens(tokens)
        print("\n🎉 Authentication complete!")
        print("   Wayne Manor is now authorized to access Google Workspace!")
        sys.exit(0)
    else:
        sys.exit(1)
