#!/usr/bin/env python3
"""
KC Quotes & Orders Tracker
Tracks estimates (견적서) and purchase orders (발주서) in KC Shared Drive
"""

import os
import pickle
import re
from datetime import datetime, timedelta
from googleapiclient.discovery import build

TOKEN_FILE = os.path.expanduser("~/.openclaw/config/google-workspace-token.pickle")
KC_DRIVE_ID = "0AIqOTGfhDoqWUk9PVA"

def get_drive_service():
    with open(TOKEN_FILE, 'rb') as f:
        creds = pickle.load(f)
    return build('drive', 'v3', credentials=creds)

def search_quotes_orders(drive_service, drive_id):
    """Search for quote and order documents"""
    
    # Keywords to search for
    quote_keywords = ['견적', 'quote', 'quotation', 'estimate', 'estimation']
    order_keywords = ['발주', 'order', 'purchase', '구매', 'PO']
    
    all_files = []
    
    # Search in specific folders first
    target_folders = [
        "01. 연도별 입출고 및 견적서",
        "02. 국내 거래처", 
        "03. 해외업체"
    ]
    
    # Get all files from drive
    page_token = None
    while True:
        try:
            results = drive_service.files().list(
                driveId=drive_id,
                corpora='drive',
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                q="trashed=false",
                pageSize=200,
                fields="files(id, name, mimeType, modifiedTime, parents, webViewLink)",
                pageToken=page_token
            ).execute()
            
            all_files.extend(results.get('files', []))
            page_token = results.get('nextPageToken')
            
            if not page_token:
                break
                
        except Exception as e:
            print(f"Error: {e}")
            break
    
    # Filter for quotes and orders
    quotes = []
    orders = []
    
    for f in all_files:
        name = f['name'].lower()
        
        # Check if it's a quote
        if any(kw in name for kw in quote_keywords):
            quotes.append(f)
        
        # Check if it's an order
        elif any(kw in name for kw in order_keywords):
            orders.append(f)
    
    return quotes, orders

def categorize_by_status(files):
    """Categorize files by status based on naming patterns"""
    
    categories = {
        'in_progress': [],      # 진행중
        'completed': [],        # 완료
        'pending': [],          # 대기
        'unknown': []           # 미확인
    }
    
    for f in files:
        name = f['name'].lower()
        
        # Check for status indicators
        if any(x in name for x in ['완료', 'completed', 'done', '확정', '최종']):
            categories['completed'].append(f)
        elif any(x in name for x in ['진행', 'progress', 'ing', '작성중']):
            categories['in_progress'].append(f)
        elif any(x in name for x in ['대기', 'pending', 'hold', '임시']):
            categories['pending'].append(f)
        else:
            categories['unknown'].append(f)
    
    return categories

def format_file_list(files, max_items=10):
    """Format file list for display"""
    if not files:
        return "   (없음)"
    
    result = []
    for f in files[:max_items]:
        name = f['name']
        modified = f.get('modifiedTime', '')
        
        # Format time
        if modified:
            try:
                mod_time = datetime.fromisoformat(modified.replace('Z', '+00:00'))
                time_str = mod_time.strftime('%m/%d')
            except:
                time_str = modified[:10]
        else:
            time_str = 'N/A'
        
        result.append(f"   📄 {name}\n      └─ 수정: {time_str}")
    
    if len(files) > max_items:
        result.append(f"   ... 외 {len(files) - max_items}개")
    
    return '\n'.join(result)

def main():
    print("📋 KC 견적/발주 현황 트래커")
    print("=" * 70)
    print(f"⏰ 조회 시간: {datetime.now().strftime('%Y-%m-%d %H:%M')} KST\n")
    
    drive = get_drive_service()
    
    # Search for quotes and orders
    quotes, orders = search_quotes_orders(drive, KC_DRIVE_ID)
    
    print(f"📊 검색 결과\n")
    print(f"   총 견적서: {len(quotes)}개")
    print(f"   총 발주서: {len(orders)}개\n")
    
    # Categorize quotes
    if quotes:
        print("📄 견적서 현황")
        print("-" * 70)
        
        quote_cats = categorize_by_status(quotes)
        
        print(f"\n   ✅ 확정/완료: {len(quote_cats['completed'])}개")
        print(format_file_list(quote_cats['completed'], 3))
        
        print(f"\n   🔄 진행중: {len(quote_cats['in_progress'])}개")
        print(format_file_list(quote_cats['in_progress'], 5))
        
        print(f"\n   ⏸️  대기/보류: {len(quote_cats['pending'])}개")
        print(format_file_list(quote_cats['pending'], 3))
        
        print(f"\n   ❓ 상태 미확인: {len(quote_cats['unknown'])}개")
        print(format_file_list(quote_cats['unknown'], 3))
    
    # Categorize orders
    if orders:
        print("\n" + "=" * 70)
        print("📦 발주서 현황")
        print("-" * 70)
        
        order_cats = categorize_by_status(orders)
        
        print(f"\n   ✅ 완료/납품: {len(order_cats['completed'])}개")
        print(format_file_list(order_cats['completed'], 3))
        
        print(f"\n   🔄 진행중: {len(order_cats['in_progress'])}개")
        print(format_file_list(order_cats['in_progress'], 5))
        
        print(f"\n   ⏸️  대기: {len(order_cats['pending'])}개")
        print(format_file_list(order_cats['pending'], 3))
    
    print("\n" + "=" * 70)
    
    # Recent activity (last 7 days)
    print("\n📅 최근 7일간 활동")
    print("-" * 70)
    
    recent_threshold = (datetime.utcnow() - timedelta(days=7)).isoformat() + 'Z'
    
    recent_quotes = [q for q in quotes if q.get('modifiedTime', '') > recent_threshold]
    recent_orders = [o for o in orders if o.get('modifiedTime', '') > recent_threshold]
    
    if recent_quotes:
        print(f"\n   📄 새로운/수정된 견적서: {len(recent_quotes)}개")
        for q in sorted(recent_quotes, key=lambda x: x['modifiedTime'], reverse=True)[:5]:
            mod_time = datetime.fromisoformat(q['modifiedTime'].replace('Z', '+00:00'))
            print(f"      • {q['name']} ({mod_time.strftime('%m/%d')})")
    
    if recent_orders:
        print(f"\n   📦 새로운/수정된 발주서: {len(recent_orders)}개")
        for o in sorted(recent_orders, key=lambda x: x['modifiedTime'], reverse=True)[:5]:
            mod_time = datetime.fromisoformat(o['modifiedTime'].replace('Z', '+00:00'))
            print(f"      • {o['name']} ({mod_time.strftime('%m/%d')})")
    
    if not recent_quotes and not recent_orders:
        print("   📭 최근 7일간 변경사항 없음")
    
    print("\n" + "=" * 70)
    print("💡 활용법:")
    print("   • '완료', '확정' 키워드 = 이미 확정된 건")
    print("   • '진행', '작성중' 키워드 = 진행중인 건")
    print("   • 파일명에 상태 표시 권장 (예: '견적_확정_고객명')")

if __name__ == "__main__":
    main()
