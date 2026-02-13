#!/usr/bin/env python3
"""
Google Workspace OAuth Flow and API Test
First-time authorization + API connectivity test
"""

import json
import os
import sys
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Configuration
CREDENTIALS_PATH = os.path.expanduser("~/.openclaw/config/google-workspace-credentials.json")
TOKEN_PATH = os.path.expanduser("~/.openclaw/config/google-workspace-token.pickle")
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def get_credentials():
    """Get or create credentials via OAuth flow"""
    creds = None
    
    # Check if token exists
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, do OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing token...")
            creds.refresh(Request())
        else:
            print("🔐 Starting OAuth flow...")
            print("   A browser will open. Please authorize the application.")
            print("   After authorization, return here.")
            print()
            
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=3000)
            print("✅ OAuth authorization completed!")
        
        # Save token
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
        os.chmod(TOKEN_PATH, 0o600)
        print(f"   Token saved to: {TOKEN_PATH}")
    
    return creds

def test_gmail(service):
    """Test Gmail API"""
    print("\n📧 Testing Gmail API...")
    try:
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        print(f"   ✅ Gmail connected! Found {len(labels)} labels")
        print(f"   📁 First 5 labels: {[l['name'] for l in labels[:5]]}")
        return True
    except Exception as e:
        print(f"   ❌ Gmail error: {e}")
        return False

def test_drive(service):
    """Test Drive API"""
    print("\n📁 Testing Drive API...")
    try:
        results = service.files().list(pageSize=10, fields="files(name, mimeType)").execute()
        files = results.get('files', [])
        print(f"   ✅ Drive connected! Found {len(files)} files")
        if files:
            print(f"   📄 Recent files: {[f['name'] for f in files[:3]]}")
        return True
    except Exception as e:
        print(f"   ❌ Drive error: {e}")
        return False

def test_calendar(service):
    """Test Calendar API"""
    print("\n📅 Testing Calendar API...")
    try:
        calendars = service.calendarList().list().execute()
        items = calendars.get('items', [])
        print(f"   ✅ Calendar connected! Found {len(items)} calendars")
        if items:
            print(f"   📆 Primary calendar: {items[0].get('summary', 'N/A')}")
        return True
    except Exception as e:
        print(f"   ❌ Calendar error: {e}")
        return False

def main():
    print("🚀 Google Workspace Integration Test")
    print("=" * 50)
    
    # Get credentials
    try:
        creds = get_credentials()
    except Exception as e:
        print(f"❌ OAuth failed: {e}")
        return False
    
    print("\n✅ Authentication successful!")
    print(f"   Token valid until: {creds.expiry}")
    
    # Test APIs
    results = {}
    
    # Gmail
    gmail_service = build('gmail', 'v1', credentials=creds)
    results['gmail'] = test_gmail(gmail_service)
    
    # Drive
    drive_service = build('drive', 'v3', credentials=creds)
    results['drive'] = test_drive(drive_service)
    
    # Calendar
    calendar_service = build('calendar', 'v3', credentials=creds)
    results['calendar'] = test_calendar(calendar_service)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    for service, success in results.items():
        status = "✅" if success else "❌"
        print(f"   {status} {service.capitalize()}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 All systems operational!")
        print("   Wayne Manor is now connected to Google Workspace!")
    else:
        print("\n⚠️  Some services failed. Check errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
