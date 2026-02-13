#!/usr/bin/env python3
"""
Dart API Search - Korean Stock Disclosure
Hybrid Bash/Python implementation for optimal performance
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
CACHE_AGE = 86400  # 24 hours

def download_corp_list():
    """Download and cache corporate list"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # Check cache
    if os.path.exists(CACHE_FILE):
        mtime = os.path.getmtime(CACHE_FILE)
        if datetime.now().timestamp() - mtime < CACHE_AGE:
            print("   💾 캐시된 목록 사용 중...")
            return True
    
    print("   🌐 최신 기업 목록 다운로드 중...")
    url = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={API_KEY}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
        
        # Save zip
        zip_path = os.path.join(CACHE_DIR, "corp_list.zip")
        with open(zip_path, 'wb') as f:
            f.write(data)
        
        # Extract
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(CACHE_DIR)
        
        # Rename
        os.rename(os.path.join(CACHE_DIR, "CORPCODE.xml"), CACHE_FILE)
        os.remove(zip_path)
        
        return True
    except Exception as e:
        print(f"   ❌ 다운로드 실패: {e}")
        return False

def search_company(query):
    """Search company by name or stock code"""
    if not os.path.exists(CACHE_FILE):
        return None
    
    try:
        tree = ET.parse(CACHE_FILE)
        root = tree.getroot()
        
        # Check if query is stock code (6 digits)
        is_stock_code = query.isdigit() and len(query) == 6
        
        for company in root.findall('.//list'):
            corp_code = company.find('corp_code')
            corp_name = company.find('corp_name')
            stock_code = company.find('stock_code')
            
            if corp_code is None or corp_name is None:
                continue
            
            corp_code_text = corp_code.text or ''
            corp_name_text = corp_name.text or ''
            stock_code_text = (stock_code.text or '').strip()
            
            if is_stock_code:
                # Search by stock code
                if stock_code_text == query:
                    return {
                        'corp_code': corp_code_text,
                        'corp_name': corp_name_text,
                        'stock_code': stock_code_text
                    }
            else:
                # Search by company name (exact match first)
                if corp_name_text == query:
                    return {
                        'corp_code': corp_code_text,
                        'corp_name': corp_name_text,
                        'stock_code': stock_code_text
                    }
        
        # Partial match fallback
        if not is_stock_code:
            matches = []
            for company in root.findall('.//list'):
                corp_name = company.find('corp_name')
                stock_code = company.find('stock_code')
                if corp_name is not None and query.lower() in (corp_name.text or '').lower():
                    matches.append({
                        'corp_name': corp_name.text,
                        'stock_code': (stock_code.text or '').strip()
                    })
                    if len(matches) >= 5:
                        break
            
            if matches:
                print("\n📝 유사한 기업 목록:")
                for m in matches:
                    stock_info = f" (종목코드: {m['stock_code']})" if m['stock_code'] else ""
                    print(f"   📌 {m['corp_name']}{stock_info}")
                print("\n💡 정확한 기업명이나 종목코드(6자리)를 입력하세요")
        
        return None
    except Exception as e:
        print(f"   ❌ 검색 오류: {e}")
        return None

def get_disclosures(corp_code, limit=10):
    """Get recent disclosures"""
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
    
    url = f"https://opendart.fss.or.kr/api/list.json?crtfc_key={API_KEY}&corp_code={corp_code}&bgn_de={start_date}&end_de={end_date}&page_no=1&page_count={limit}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        if data.get('status') == '000':
            items = data.get('list', [])
            if items:
                for item in items[:limit]:
                    report_nm = item.get('report_nm', 'N/A')
                    rcept_dt = item.get('rcept_dt', '')
                    rm = item.get('rm') or '일반'
                    
                    # Format date
                    if len(rcept_dt) == 8:
                        rcept_dt = f"{rcept_dt[:4]}-{rcept_dt[4:6]}-{rcept_dt[6:]}"
                    
                    print(f"📌 {report_nm}")
                    print(f"   일자: {rcept_dt}")
                    print(f"   유형: {rm}")
                    print()
            else:
                print("📭 최근 30일간 공시 없음")
        else:
            print(f"❌ 오류: {data.get('message', 'API 호출 실패')}")
    except Exception as e:
        print(f"⚠️  공시 조회 오류: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 dart-search.py \"기업명\" [공시개수]")
        print("       python3 dart-search.py \"005930\" 10")
        sys.exit(1)
    
    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    print(f"📊 Dart API Search: {query}")
    print("---")
    
    if not API_KEY:
        print("❌ DART_API_KEY 환경변수를 설정하세요")
        sys.exit(1)
    
    print("🔍 기업 정보 확인 중...")
    
    # Download corp list
    if not download_corp_list():
        print("❌ 기업 목록 다운로드 실패")
        sys.exit(1)
    
    # Search company
    company = search_company(query)
    
    if not company:
        print("❌ 기업을 찾을 수 없습니다")
        sys.exit(1)
    
    print("✅ 기업 발견:")
    print(f"   기업명: {company['corp_name']}")
    print(f"   고유번호: {company['corp_code']}")
    print(f"   종목코드: {company['stock_code'] or '비상장'}")
    print()
    
    print(f"📋 최근 공시 목록 ({limit}건):")
    print("---")
    get_disclosures(company['corp_code'], limit)
    
    print("✅ 검색 완료")

if __name__ == "__main__":
    main()
