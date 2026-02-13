#!/usr/bin/env python3
"""
Dart Disclosure Monitor - Automated tracking for key stocks
Monitors important disclosures and sends alerts
"""

import os
import sys
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import urllib.request
import urllib.error
import zipfile

# Configuration
API_KEY = os.environ.get('DART_API_KEY', '')
CACHE_DIR = "/tmp/dart_cache"
CACHE_FILE = os.path.join(CACHE_DIR, "corp_list.xml")

# Watchlist - companies to monitor
WATCHLIST = {
    "00126380": {"name": "삼성전자", "code": "005930", "priority": "high"},
    "00164779": {"name": "SK하이닉스", "code": "000660", "priority": "high"},
    "00164742": {"name": "현대자동차", "code": "005380", "priority": "medium"},
    "00159616": {"name": "두산에너빌리티", "code": "034020", "priority": "high"},  # Nuclear
}

# Important disclosure keywords
HIGH_PRIORITY_KEYWORDS = [
    "매출액또는손익구조",  # Revenue/profit change 30%+
    "유상증자",           # Capital increase
    "타법인주식및출자증권취득",  # M&A
    "영업양수",           # Business acquisition
    "분기보고서",         # Quarterly report
    "사업보고서",         # Annual report
]

ALERT_KEYWORDS = [
    "주주총회",           # Shareholder meeting
    "기업설명회",         # IR
    "임원ㆍ주요주주",     # Insider trading
    "주요사항",           # Material event
]

def ensure_corp_list():
    """Download corporate list if needed"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    if not os.path.exists(CACHE_FILE):
        print("🌐 Downloading corporate list...")
        url = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={API_KEY}"
        
        try:
            req_obj = urllib.request.Request(url)
            with urllib.request.urlopen(req_obj, timeout=30) as response:
                data = response.read()
            
            zip_path = os.path.join(CACHE_DIR, "corp_list.zip")
            with open(zip_path, 'wb') as f:
                f.write(data)
            
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(CACHE_DIR)
            
            os.rename(os.path.join(CACHE_DIR, "CORPCODE.xml"), CACHE_FILE)
            os.remove(zip_path)
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False
    
    return True

def get_disclosures(corp_code, days=3):
    """Get recent disclosures for a company"""
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
    
    url = f"https://opendart.fss.or.kr/api/list.json?crtfc_key={API_KEY}&corp_code={corp_code}&bgn_de={start_date}&end_de={end_date}&page_no=1&page_count=20"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        if data.get('status') == '000':
            return data.get('list', [])
        return []
    except Exception as e:
        print(f"⚠️  API error: {e}")
        return []

def analyze_importance(report_nm):
    """Analyze disclosure importance"""
    report_nm_lower = report_nm.lower()
    
    # Check high priority
    for keyword in HIGH_PRIORITY_KEYWORDS:
        if keyword in report_nm:
            return "🔴 HIGH", f"Contains: {keyword}"
    
    # Check alert level
    for keyword in ALERT_KEYWORDS:
        if keyword in report_nm:
            return "🟡 ALERT", f"Contains: {keyword}"
    
    return "🟢 NORMAL", ""

def monitor_watchlist():
    """Monitor all watchlist companies"""
    if not ensure_corp_list():
        print("❌ Cannot load corporate list")
        return
    
    print("📊 Dart Disclosure Monitor")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')} KST")
    print("=" * 60)
    print()
    
    alerts = []
    all_disclosures = []
    
    for corp_code, info in WATCHLIST.items():
        disclosures = get_disclosures(corp_code, days=3)
        
        if disclosures:
            print(f"📈 {info['name']} ({info['code']})")
            
            for item in disclosures[:5]:  # Top 5 recent
                report_nm = item.get('report_nm', 'N/A')
                rcept_dt = item.get('rcept_dt', '')
                
                # Format date
                if len(rcept_dt) == 8:
                    rcept_dt = f"{rcept_dt[4:6]}/{rcept_dt[6:]}"
                
                importance, reason = analyze_importance(report_nm)
                
                print(f"   {importance} {report_nm}")
                print(f"      📅 {rcept_dt} | {reason}")
                
                # Collect alerts
                if "HIGH" in importance or "ALERT" in importance:
                    alerts.append({
                        'company': info['name'],
                        'code': info['code'],
                        'report': report_nm,
                        'date': rcept_dt,
                        'importance': importance,
                        'reason': reason
                    })
                
                all_disclosures.append({
                    'company': info['name'],
                    'report': report_nm,
                    'date': rcept_dt,
                    'importance': importance
                })
            
            print()
    
    # Summary
    print("=" * 60)
    if alerts:
        print(f"🚨 {len(alerts)} IMPORTANT DISCLOSURES FOUND")
        print()
        for alert in alerts:
            print(f"{alert['importance']} {alert['company']}")
            print(f"   📋 {alert['report']}")
            print(f"   📅 {alert['date']}")
            print()
    else:
        print("✅ No high-priority disclosures in last 3 days")
    
    print(f"📊 Total monitored: {len(WATCHLIST)} companies, {len(all_disclosures)} disclosures")
    
    return alerts

if __name__ == "__main__":
    if not API_KEY:
        print("❌ DART_API_KEY not set")
        sys.exit(1)
    
    monitor_watchlist()
