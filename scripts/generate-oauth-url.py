#!/usr/bin/env python3
"""
Generate OAuth URL for manual authorization
"""
import json
import os

CREDENTIALS_PATH = os.path.expanduser("~/.openclaw/config/google-workspace-credentials.json")
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]

# Load credentials
with open(CREDENTIALS_PATH) as f:
    creds = json.load(f)['web']

client_id = creds['client_id']
redirect_uri = creds['redirect_uris'][0]

# Build OAuth URL
scope_str = '%20'.join(SCOPES)
auth_url = (
    f"https://accounts.google.com/o/oauth2/auth?"
    f"client_id={client_id}&"
    f"redirect_uri={redirect_uri}&"
    f"scope={scope_str}&"
    f"response_type=code&"
    f"access_type=offline&"
    f"prompt=consent"
)

print("🌐 OAuth Authorization URL:")
print("=" * 60)
print(auth_url)
print("=" * 60)
print()
print("📋 Steps:")
print("   1. Copy the URL above")
print("   2. Open in your browser (MacBook)")
print("   3. Login with chrispark@koreacryo.com")
print("   4. Click 'Allow'")
print("   5. You'll be redirected to localhost:3000 (will show error, that's OK)")
print("   6. Copy the 'code' parameter from the URL")
print("   7. Send the code to me")
print()
print("⚠️  Note: The code expires in 10 minutes!")
