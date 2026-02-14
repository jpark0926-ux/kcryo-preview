#!/usr/bin/env python3
import subprocess
import json
import time
import sys

def fetch_all_pst_emails():
    """PST 받은편지함 모든 이메일 가져오기"""
    all_threads = []
    token = None
    page = 1
    
    print("📧 PST 이메일 수집 시작...")
    
    while True:
        cmd = [
            "/usr/local/bin/gog", "gmail", "search",
            "in:chrispark@koreacryo.com.pst/받은 편지함",
            "--json", "--max=500"
        ]
        if token:
            cmd.extend(["--page", token])
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"❌ 오류: {result.stderr[:100]}")
            break
        
        try:
            data = json.loads(result.stdout)
        except:
            print("❌ JSON 파싱 오류")
            break
        
        threads = data.get('threads') or []
        if not threads:
            break
        
        all_threads.extend(threads)
        print(f"  페이지 {page}: {len(threads)}개 (누적: {len(all_threads)}개)")
        
        token = data.get('nextPageToken')
        if not token:
            print("  ✅ 마지막 페이지")
            break
        
        page += 1
        if page > 10:  # 안전장치 (최대 5000개)
            print("  ⚠️ 최대 페이지 도달")
            break
        
        time.sleep(0.5)
    
    return all_threads

if __name__ == "__main__":
    threads = fetch_all_pst_emails()
    
    print(f"\n{'='*50}")
    print(f"✅ 총 {len(threads)}개 이메일 수집 완료")
    
    # 날짜 범위 확인
    if threads:
        dates = [t.get('date', '') for t in threads if t.get('date')]
        if dates:
            print(f"📅 날짜 범위: {min(dates)} ~ {max(dates)}")
        
        # 파일로 저장
        with open('/Users/roturnjarvis/.openclaw/workspace/logs/pst_emails.json', 'w') as f:
            json.dump(threads, f, indent=2, ensure_ascii=False)
        print(f"💾 저장 완료: logs/pst_emails.json")
