#!/usr/bin/env python3
"""
KC Shared Drive Latest Files Monitor
Tracks and reports newly uploaded/modified files
"""

import os
import pickle
import json
from datetime import datetime, timedelta
from googleapiclient.discovery import build

TOKEN_FILE = os.path.expanduser("~/.openclaw/config/google-workspace-token.pickle")
KC_DRIVE_ID = "0AIqOTGfhDoqWUk9PVA"
STATE_FILE = os.path.expanduser("~/.openclaw/config/kc_drive_state.json")

def get_drive_service():
    with open(TOKEN_FILE, 'rb') as f:
        creds = pickle.load(f)
    return build('drive', 'v3', credentials=creds)

def get_all_files(drive_service, drive_id, hours=24):
    """Get all files modified in last N hours"""
    files = []
    
    # Calculate time threshold
    time_threshold = (datetime.utcnow() - timedelta(hours=hours)).isoformat() + 'Z'
    
    page_token = None
    while True:
        try:
            results = drive_service.files().list(
                driveId=drive_id,
                corpora='drive',
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                q=f"modifiedTime > '{time_threshold}' and trashed=false",
                pageSize=100,
                fields="files(id, name, mimeType, modifiedTime, lastModifyingUser, webViewLink)",
                pageToken=page_token
            ).execute()
            
            files.extend(results.get('files', []))
            page_token = results.get('nextPageToken')
            
            if not page_token:
                break
                
        except Exception as e:
            print(f"Error: {e}")
            break
    
    return files

def format_file_info(file_obj):
    """Format file info for display"""
    name = file_obj['name']
    mime = file_obj['mimeType']
    modified = file_obj['modifiedTime']
    
    # Format time
    mod_time = datetime.fromisoformat(modified.replace('Z', '+00:00'))
    time_str = mod_time.strftime('%m/%d %H:%M')
    
    # Icon
    if mime == 'application/vnd.google-apps.folder':
        icon = '📁'
    elif 'spreadsheet' in mime:
        icon = '📊'
    elif 'document' in mime:
        icon = '📝'
    elif 'pdf' in mime:
        icon = '📄'
    elif 'image' in mime or 'photo' in mime:
        icon = '🖼️'
    else:
        icon = '📎'
    
    return f"{icon} {name}\n   🕐 {time_str}"

def main():
    print("📊 KC Shared Drive - Latest Files Monitor")
    print("=" * 60)
    print(f"⏰ Check time: {datetime.now().strftime('%Y-%m-%d %H:%M')} KST\n")
    
    drive = get_drive_service()
    
    # Get files from last 24 hours
    files = get_all_files(drive, KC_DRIVE_ID, hours=24)
    
    if not files:
        print("📭 최근 24시간 내 변경된 파일 없음")
        return
    
    # Sort by modified time (newest first)
    files.sort(key=lambda x: x['modifiedTime'], reverse=True)
    
    # Group by type
    folders = [f for f in files if f['mimeType'] == 'application/vnd.google-apps.folder']
    documents = [f for f in files if 'document' in f['mimeType'] or 'spreadsheet' in f['mimeType'] or 'pdf' in f['mimeType']]
    others = [f for f in files if f not in folders and f not in documents]
    
    print(f"🆕 최근 24시간 변경된 파일: {len(files)}개\n")
    
    if folders:
        print(f"📁 새로운/수정된 폴터 ({len(folders)}개):")
        for f in folders[:5]:
            print(format_file_info(f))
        print()
    
    if documents:
        print(f"📝 새로운/수정된 문서 ({len(documents)}개):")
        for f in documents[:10]:
            print(format_file_info(f))
        print()
    
    if others:
        print(f"📎 기타 파일 ({len(others)}개):")
        for f in others[:5]:
            print(format_file_info(f))
    
    print("\n" + "=" * 60)
    print("💡 팁: 'python3 kc-drive-monitor.py' 로 언제든 확인 가능")

if __name__ == "__main__":
    main()
