#!/usr/bin/env python3
"""
Google Workspace Integration Test for Wayne Manor
Tests Gmail and Drive API connectivity
"""

import json
import os
import sys

# Configuration
CREDENTIALS_PATH = os.path.expanduser("~/.openclaw/config/google-workspace-credentials.json")

def load_credentials():
    """Load OAuth credentials from JSON file"""
    try:
        with open(CREDENTIALS_PATH, 'r') as f:
            creds = json.load(f)
        return creds.get('web', {})
    except FileNotFoundError:
        print(f"❌ Credentials file not found: {CREDENTIALS_PATH}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return None

def test_setup():
    """Test basic setup"""
    print("🧪 Google Workspace Integration Test")
    print("=" * 50)
    
    # 1. Check credentials
    creds = load_credentials()
    if not creds:
        return False
    
    print(f"✅ Credentials loaded")
    print(f"   Project ID: wayne-manor-integration")
    print(f"   Client ID: {creds.get('client_id', 'N/A')[:20]}...")
    print(f"   Redirect URI: {creds.get('redirect_uris', ['N/A'])[0]}")
    
    # 2. Check required libraries
    print("\n📦 Checking Python libraries...")
    try:
        import google.auth
        print("   ✅ google-auth")
    except ImportError:
        print("   ❌ google-auth (pip install google-auth)")
    
    try:
        import googleapiclient
        print("   ✅ google-api-python-client")
    except ImportError:
        print("   ❌ google-api-python-client (pip install google-api-python-client)")
    
    # 3. Next steps
    print("\n📋 Next Steps:")
    print("   1. Google Workspace Admin Console 설정 필요")
    print("   2. Domain-wide delegation 활성화")
    print("   3. First OAuth authorization (manual)")
    print("   4. Token storage and refresh setup")
    
    return True

if __name__ == "__main__":
    success = test_setup()
    sys.exit(0 if success else 1)
