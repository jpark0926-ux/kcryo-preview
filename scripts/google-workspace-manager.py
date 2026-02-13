#!/usr/bin/env python3
"""
Google Workspace Token Manager with Auto-Refresh
Handles automatic token refresh when expired
"""

import json
import os
import pickle
from datetime import datetime, timedelta, timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Configuration
TOKEN_DIR = os.path.expanduser("~/.openclaw/config")
TOKEN_PATH = os.path.join(TOKEN_DIR, "google-workspace-token.pickle")
CREDENTIALS_PATH = os.path.join(TOKEN_DIR, "google-workspace-credentials.json")

class GoogleWorkspaceManager:
    """Manages Google Workspace API connections with auto-refresh"""
    
    def __init__(self):
        self.creds = None
        self._load_credentials()
    
    def _load_credentials(self):
        """Load and refresh credentials if needed"""
        # Check if token exists
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as f:
                self.creds = pickle.load(f)
            
            # Check if expired
            if self.creds and self.creds.expired and self.creds.refresh_token:
                print("🔄 Token expired, refreshing...")
                self._refresh_token()
        else:
            print("❌ No token found. Run initial authorization first.")
            self.creds = None
    
    def _refresh_token(self):
        """Refresh the access token"""
        try:
            self.creds.refresh(Request())
            self._save_credentials()
            print(f"✅ Token refreshed! Valid until: {self.creds.expiry}")
        except Exception as e:
            print(f"❌ Token refresh failed: {e}")
            self.creds = None
    
    def _save_credentials(self):
        """Save credentials to file"""
        with open(TOKEN_PATH, 'wb') as f:
            pickle.dump(self.creds, f)
        os.chmod(TOKEN_PATH, 0o600)
    
    def get_gmail_service(self):
        """Get Gmail API service"""
        if not self.creds or self.creds.expired:
            self._load_credentials()
        if self.creds:
            return build('gmail', 'v1', credentials=self.creds)
        return None
    
    def get_drive_service(self):
        """Get Drive API service"""
        if not self.creds or self.creds.expired:
            self._load_credentials()
        if self.creds:
            return build('drive', 'v3', credentials=self.creds)
        return None
    
    def get_calendar_service(self):
        """Get Calendar API service"""
        if not self.creds or self.creds.expired:
            self._load_credentials()
        if self.creds:
            return build('calendar', 'v3', credentials=self.creds)
        return None
    
    def is_authenticated(self):
        """Check if properly authenticated"""
        return self.creds is not None and not self.creds.expired

# Initialize manager
gw = GoogleWorkspaceManager()

if __name__ == "__main__":
    print("🔄 Google Workspace Token Auto-Refresh Setup")
    print("=" * 50)
    
    if gw.is_authenticated():
        print(f"✅ Authentication active!")
        print(f"   Token valid until: {gw.creds.expiry}")
        print(f"   Auto-refresh: Enabled")
    else:
        print("⚠️  Authentication required")
        print("   Run initial OAuth flow first")
