#!/usr/bin/env python3
"""
Google Workspace OAuth Setup with Auto-Refresh
Complete automation for Wayne Manor
"""

import json
import os
import pickle
import sys
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# Configuration
CONFIG_DIR = os.path.expanduser("~/.openclaw/config")
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, "google-workspace-credentials.json")
TOKEN_FILE = os.path.join(CONFIG_DIR, "google-workspace-token.pickle")

# Scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def load_credentials():
    """Load credentials from file or return None"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as f:
            return pickle.load(f)
    return None

def save_credentials(creds):
    """Save credentials to file"""
    with open(TOKEN_FILE, 'wb') as f:
        pickle.dump(creds, f)
    os.chmod(TOKEN_FILE, 0o600)

def generate_auth_url():
    """Generate OAuth authorization URL"""
    # Load client config
    with open(CREDENTIALS_FILE) as f:
        client_config = json.load(f)
    
    # Create flow
    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri='http://localhost:3000/oauth2callback'
    )
    
    # Generate URL
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    return auth_url, flow

def exchange_code(flow, code):
    """Exchange authorization code for tokens"""
    try:
        flow.fetch_token(code=code)
        creds = flow.credentials
        save_credentials(creds)
        return creds
    except Exception as e:
        print(f"❌ Token exchange failed: {e}")
        return None

def refresh_if_needed(creds):
    """Refresh token if expired"""
    if creds and creds.expired and creds.refresh_token:
        print("🔄 Refreshing access token...")
        try:
            creds.refresh(Request())
            save_credentials(creds)
            print(f"✅ Token refreshed! Valid until: {creds.expiry}")
            return creds
        except Exception as e:
            print(f"❌ Refresh failed: {e}")
            return None
    return creds

def test_apis(creds):
    """Test all APIs"""
    print("\n🧪 Testing Google Workspace APIs...")
    print("=" * 50)
    
    # Test Gmail
    try:
        gmail = build('gmail', 'v1', credentials=creds)
        results = gmail.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        print(f"📧 Gmail: ✅ Connected! ({len(labels)} labels)")
    except Exception as e:
        print(f"📧 Gmail: ❌ {str(e)[:60]}")
    
    # Test Drive
    try:
        drive = build('drive', 'v3', credentials=creds)
        results = drive.files().list(pageSize=5, fields="files(name)").execute()
        files = results.get('files', [])
        print(f"📁 Drive: ✅ Connected! ({len(files)} files)")
        for f in files[:2]:
            print(f"      📄 {f['name']}")
    except Exception as e:
        print(f"📁 Drive: ❌ {str(e)[:60]}")
    
    # Test Calendar
    try:
        calendar = build('calendar', 'v3', credentials=creds)
        calendars = calendar.calendarList().list().execute()
        items = calendars.get('items', [])
        print(f"📅 Calendar: ✅ Connected! ({len(items)} calendars)")
        for c in items[:2]:
            print(f"      📆 {c.get('summary', 'N/A')}")
    except Exception as e:
        print(f"📅 Calendar: ❌ {str(e)[:60]}")
    
    print("=" * 50)

def main():
    print("🔐 Google Workspace OAuth Setup")
    print("=" * 50)
    
    # Check existing credentials
    creds = load_credentials()
    
    if creds:
        print(f"📂 Existing token found")
        print(f"   Expires: {creds.expiry}")
        print(f"   Expired: {creds.expired}")
        
        # Try to refresh if expired
        if creds.expired:
            creds = refresh_if_needed(creds)
            if not creds:
                print("\n🔄 Need to re-authorize")
                creds = None
    
    if not creds:
        print("\n📋 Step 1: Generate Authorization URL")
        print("-" * 50)
        
        try:
            auth_url, flow = generate_auth_url()
            print(f"✅ Authorization URL generated!")
            print(f"\n🔗 Open this URL in your browser:")
            print(f"\n{auth_url}\n")
            print("-" * 50)
            print("After authorization, you'll see an error page.")
            print("Copy the CODE from the URL (code=... part)")
            print("and run: python3 oauth-setup.py <code>")
            
            # Save flow for later
            with open('/tmp/oauth_flow.pkl', 'wb') as f:
                pickle.dump(flow, f)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return
    
    else:
        print("\n✅ Already authenticated!")
        test_apis(creds)
        print("\n🎉 Wayne Manor is connected to Google Workspace!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Exchange code
        code = sys.argv[1]
        if '&' in code:
            code = code.split('&')[0]
        
        print(f"🔄 Exchanging code: {code[:20]}...")
        
        try:
            with open('/tmp/oauth_flow.pkl', 'rb') as f:
                flow = pickle.load(f)
            
            creds = exchange_code(flow, code)
            if creds:
                print(f"✅ Authentication successful!")
                print(f"   Token valid until: {creds.expiry}")
                print(f"   Refresh token: {'Present' if creds.refresh_token else 'Missing'}")
                test_apis(creds)
                print("\n🎉 Wayne Manor is now connected!")
                os.remove('/tmp/oauth_flow.pkl')
            else:
                print("❌ Authentication failed")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        main()
