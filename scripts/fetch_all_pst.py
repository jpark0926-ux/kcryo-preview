#!/usr/bin/env python3
import subprocess
import json
import time
import os

def fetch_all_emails():
    """모든 PST 이메일 가져와서 저장"""
    all_threads = []
    token = None
    page = 1
    
    print("📧 PST 이메일 전체 수집 시작...", flush=True)
    
    while page <= 20:  # 최대 2000개
        cmd = [
            "/usr/local/bin/gog", "gmail", "search",
            "in:chrispark@koreacryo.com.pst/받은 편지함",
            "--json", "--max=100"
        ]
        if token:
            cmd.extend(["--page", token])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                print(f"페이지 {page} 오류: {result.stderr[:100]}", flush=True)
                break
            
            data = json.loads(result.stdout)
            threads = data.get('threads') or []
            
            if not threads:
                print(f"페이지 {page}: 데이터 없음 (종료)", flush=True)
                break
            
            all_threads.extend(threads)
            print(f"페이지 {page}: {len(threads)}개 수집 (총 {len(all_threads)}개)", flush=True)
            
            token = data.get('nextPageToken')
            if not token:
                print("마지막 페이지 도달", flush=True)
                break
            
            page += 1
            time.sleep(0.5)
            
        except Exception as e:
            print(f"예외 발생: {e}", flush=True)
            break
    
    # 저장
    os.makedirs('/Users/roturnjarvis/.openclaw/workspace/logs', exist_ok=True)
    with open('/Users/roturnjarvis/.openclaw/workspace/logs/all_pst_emails.json', 'w', encoding='utf-8') as f:
        json.dump(all_threads, f, ensure_ascii=False, indent=2)
    
    # 요약 저장
    summary = {
        'total': len(all_threads),
        'pages': page,
        'date_range': {
            'oldest': min(t.get('date', '') for t in all_threads) if all_threads else '',
            'newest': max(t.get('date', '') for t in all_threads) if all_threads else ''
        },
        'important_count': len([t for t in all_threads if 'IMPORTANT' in t.get('labels', [])])
    }
    
    with open('/Users/roturnjarvis/.openclaw/workspace/logs/pst_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n✅ 완료: 총 {len(all_threads)}개 이메일", flush=True)
    print(f"💾 저장: logs/all_pst_emails.json", flush=True)
    print(f"📊 요약: logs/pst_summary.json", flush=True)

if __name__ == "__main__":
    fetch_all_emails()
