#!/usr/bin/env python3
"""
Google Workspace Manager for Wayne Manor
Auto-refresh + Gmail/Drive/Calendar operations
"""

import os
import pickle
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

CONFIG_DIR = os.path.expanduser("~/.openclaw/config")
TOKEN_FILE = os.path.join(CONFIG_DIR, "google-workspace-token.pickle")

class GoogleWorkspaceManager:
    def __init__(self):
        self.creds = self._load_and_refresh_credentials()
        self.gmail_service = None
        self.drive_service = None
        self.calendar_service = None
    
    def _load_and_refresh_credentials(self):
        """Load credentials and refresh if needed"""
        if not os.path.exists(TOKEN_FILE):
            raise Exception("No token found. Run oauth-setup.py first.")
        
        with open(TOKEN_FILE, 'rb') as f:
            creds = pickle.load(f)
        
        # Refresh if expired
        if creds.expired and creds.refresh_token:
            print("🔄 Refreshing token...")
            creds.refresh(Request())
            with open(TOKEN_FILE, 'wb') as f:
                pickle.dump(creds, f)
            os.chmod(TOKEN_FILE, 0o600)
            print(f"✅ Token refreshed! Valid until: {creds.expiry}")
        
        return creds
    
    def get_gmail(self):
        """Get Gmail service"""
        if not self.gmail_service:
            self.gmail_service = build('gmail', 'v1', credentials=self.creds)
        return self.gmail_service
    
    def get_drive(self):
        """Get Drive service"""
        if not self.drive_service:
            self.drive_service = build('drive', 'v3', credentials=self.creds)
        return self.drive_service
    
    def get_calendar(self):
        """Get Calendar service"""
        if not self.calendar_service:
            self.calendar_service = build('calendar', 'v3', credentials=self.creds)
        return self.calendar_service
    
    def search_gmail(self, query, max_results=10):
        """Search Gmail"""
        try:
            gmail = self.get_gmail()
            results = gmail.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
            messages = results.get('messages', [])
            
            print(f"📧 Found {len(messages)} emails for: '{query}'")
            for msg in messages[:5]:
                detail = gmail.users().messages().get(userId='me', id=msg['id'], format='metadata').execute()
                headers = detail.get('payload', {}).get('headers', [])
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                print(f"   📨 {subject[:50]}... | From: {sender[:30]}")
            
            return messages
        except Exception as e:
            print(f"❌ Gmail search error: {e}")
            return []
    
    def search_drive(self, query, max_results=10):
        """Search Drive"""
        try:
            drive = self.get_drive()
            results = drive.files().list(
                q=f"name contains '{query}'",
                pageSize=max_results,
                fields="files(name, id, mimeType, modifiedTime)"
            ).execute()
            files = results.get('files', [])
            
            print(f"📁 Found {len(files)} files for: '{query}'")
            for f in files[:5]:
                print(f"   📄 {f['name']} ({f['mimeType'].split('/')[-1]})")
            
            return files
        except Exception as e:
            print(f"❌ Drive search error: {e}")
            return []

if __name__ == "__main__":
    print("🔐 Google Workspace Manager")
    print("=" * 50)
    
    try:
        gw = GoogleWorkspaceManager()
        print("✅ Connected to Google Workspace!")
        print()
        
        # Example usage
        print("📝 Example searches:")
        print("-" * 50)
        gw.search_gmail("from:noreply@koreacryo.com", max_results=3)
        print()
        gw.search_drive("출장", max_results=3)
        
    except Exception as e:
        print(f"❌ Error: {e}")
