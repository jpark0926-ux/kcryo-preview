#!/usr/bin/env python3
"""Debug eCount API response"""
import os
import json
import urllib.request

com_code = os.getenv('ECOUNT_COM_CODE', '82532')
user_id = os.getenv('ECOUNT_USER_ID', 'hrlee')
api_key = os.getenv('ECOUNT_API_KEY', '')
zone = os.getenv('ECOUNT_ZONE', 'CC')

print(f"Testing with:")
print(f"  Company: {com_code}")
print(f"  User: {user_id}")
print(f"  Zone: {zone}")
print()

data = {
    "COM_CODE": com_code,
    "USER_ID": user_id,
    "API_CERT_KEY": api_key,
    "LAN_TYPE": "ko-KR",
    "ZONE": zone
}

url = f"https://sboapi{zone}.ecount.com/OAPI/V2/OAPILogin"
print(f"URL: {url}")
print(f"Request: {json.dumps(data, indent=2)}")
print()

try:
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=json_data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("Response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if 'Data' in result:
            print("\nData structure:")
            print(json.dumps(result['Data'], indent=2, ensure_ascii=False)[:500])
        
except Exception as e:
    print(f"Error: {e}")
