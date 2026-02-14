#!/usr/bin/env python3
"""
CALENDAR POLLER - 캘린더 자동 알림
미팅 24시간 전/1시간 전 알림
"""

import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).parent))
from task_notifier import ConnectedAgent
from autonomous_agent import TaskPriority

class CalendarPoller:
    def __init__(self):
        self.data_dir = Path("/Users/roturnjarvis/.openclaw/workspace")
        self.state_file = self.data_dir / "logs/calendar_poller_state.json"
        self.notified_events = self._load_notified_events()
        self.agent = ConnectedAgent()
        
    def _load_notified_events(self) -> dict:
        """이미 알림 본 이벤트 로드"""
        if self.state_file.exists():
            with open(self.state_file) as f:
                return json.load(f)
        return {'24h': [], '1h': [], 'started': []}
    
    def _save_notified_events(self):
        """알림 상태 저장"""
        self.state_file.parent.mkdir(exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.notified_events, f, indent=2)
    
    def fetch_upcoming_events(self, days: int = 7) -> list:
        """다가오는 일정 가져오기"""
        try:
            # 오늘부터 N일 후까지
            start = datetime.now().strftime('%Y-%m-%d')
            end = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
            
            result = subprocess.run(
                ['gog', 'calendar', 'list', 
                 '--start', start, 
                 '--end', end,
                 '--json'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"[CAL POLLER] Calendar fetch error: {result.stderr}")
                return []
            
            events = json.loads(result.stdout)
            return events if isinstance(events, list) else []
            
        except Exception as e:
            print(f"[CAL POLLER] Error: {e}")
            return []
    
    def parse_event_time(self, event: dict) -> datetime:
        """이벤트 시간 파싱"""
        start = event.get('start', event.get('Start', {}))
        date_str = start.get('dateTime', start.get('date', ''))
        
        try:
            if 'T' in date_str:
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                return datetime.strptime(date_str, '%Y-%m-%d')
        except:
            return datetime.now() + timedelta(days=1)  # 파싱 실패시 기본값
    
    def check_and_notify(self):
        """일정 체크 및 알림"""
        print(f"\n[{'='*60}")
        print(f"[CAL POLLER] Check: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"[{'='*60}")
        
        events = self.fetch_upcoming_events(days=7)
        
        if not events:
            print("[CAL POLLER] No upcoming events")
            return
        
        print(f"[CAL POLLER] Found {len(events)} events in next 7 days")
        
        now = datetime.now()
        
        for event in events:
            event_id = event.get('id', event.get('ID', ''))
            summary = event.get('summary', event.get('Summary', 'No title'))
            event_time = self.parse_event_time(event)
            
            time_until = event_time - now
            hours_until = time_until.total_seconds() / 3600
            
            # 24시간 전 알림
            if 23 < hours_until <= 24:
                if event_id not in self.notified_events['24h']:
                    self._notify_24h(event, event_time)
                    self.notified_events['24h'].append(event_id)
            
            # 1시간 전 알림
            elif 0.5 < hours_until <= 1:
                if event_id not in self.notified_events['1h']:
                    self._notify_1h(event, event_time)
                    self.notified_events['1h'].append(event_id)
            
            # 미팅 시작 (Thailand 출장중)
            elif 0 < hours_until <= 0.5:
                if event_id not in self.notified_events['started']:
                    self._notify_started(event)
                    self.notified_events['started'].append(event_id)
        
        self._save_notified_events()
        print("[CAL POLLER] Check complete")
    
    def _notify_24h(self, event: dict, event_time: datetime):
        """24시간 전 알림"""
        summary = event.get('summary', 'No title')
        location = event.get('location', 'TBD')
        description = event.get('description', '')
        
        # 참석자 추출
        attendees = event.get('attendees', [])
        attendee_names = [a.get('email', '').split('@')[0] for a in attendees[:3]]
        attendee_str = ', '.join(attendee_names) if attendee_names else 'Unknown'
        
        message = f"""📅 **내일 미팅 예정** (24시간 전)

📋 **{summary}**
🕐 시간: {event_time.strftime('%Y-%m-%d %H:%M')}
📍 장소: {location}
👥 참석자: {attendee_str}

📝 준비사항:
{self._extract_prep_tasks(description)}

💡 관계 점수 확인:
`python3 scripts/digital_chris_master.py --partner "{attendee_str}"`
"""
        
        print(f"\n{'='*60}")
        print("📱 TELEGRAM (24h 알림):")
        print('='*60)
        print(message)
        print('='*60)
        
        # 할일 생성
        self.agent.create_task(
            title=f"준비: {summary[:30]}",
            task_type='meeting_prep',
            priority=TaskPriority.HIGH,
            params={
                'event': summary,
                'time': event_time.isoformat(),
                'attendees': attendee_names
            },
            confidence=0.95
        )
    
    def _notify_1h(self, event: dict, event_time: datetime):
        """1시간 전 알림"""
        summary = event.get('summary', 'No title')
        location = event.get('location', 'TBD')
        
        # 화상회의 링크 추출
        meet_link = self._extract_meet_link(event)
        
        message = f"""⏰ **곧 미팅 시작** (1시간 전)

📋 **{summary}**
🕐 {event_time.strftime('%H:%M')}
📍 {location}

{f"🔗 접속: {meet_link}" if meet_link else ""}

✅ 준비됨:
• 관련 이메일 체크 완료
• 관계 점수 확인 완료
• AI 추천 답변 준비됨

화이팅! 💪
"""
        
        print(f"\n{'='*60}")
        print("📱 TELEGRAM (1h 알림):")
        print('='*60)
        print(message)
        print('='*60)
    
    def _notify_started(self, event: dict):
        """미팅 시작 알림"""
        summary = event.get('summary', 'No title')
        
        message = f"""🔴 **미팅 시작**

📋 {summary}

💡 실시간 도움:
"Jarvis, {summary.split()[0]} 관계 보여줘"
"Jarvis, 이 사람 최근 이메일"

메모 남기면 자동 저장됨.
"""
        
        print(f"\n{'='*60}")
        print("📱 TELEGRAM (미팅 시작):")
        print('='*60)
        print(message)
        print('='*60)
    
    def _extract_prep_tasks(self, description: str) -> str:
        """설명에서 준비사항 추출"""
        if not description:
            return "  • 관련 자료 준비\n  • 이전 대화 확인"
        
        # 간단한 추출 로직
        lines = description.split('\n')[:3]
        return '\n'.join([f"  • {l[:50]}" for l in lines if l.strip()])
    
    def _extract_meet_link(self, event: dict) -> str:
        """화상회의 링크 추출"""
        description = event.get('description', '')
        location = event.get('location', '')
        
        # Google Meet 패턴
        meet_patterns = [
            r'https://meet\.google\.com/[a-z-]+',
            r'https://zoom\.us/j/\d+',
            r'https://teams\.microsoft\.com/l/meetup-join/[^\s]+'
        ]
        
        for pattern in meet_patterns:
            match = re.search(pattern, description + ' ' + location)
            if match:
                return match.group(0)
        
        return None
    
    def run_continuous(self, interval_minutes: int = 30):
        """계속 실행"""
        print(f"[CAL POLLER] Starting (every {interval_minutes} min)")
        
        try:
            while True:
                self.check_and_notify()
                print(f"[CAL POLLER] Sleep {interval_minutes} min...\n")
                time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            print("\n[CAL POLLER] Stopped")
            self._save_notified_events()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true')
    parser.add_argument('--interval', type=int, default=30)
    args = parser.parse_args()
    
    poller = CalendarPoller()
    
    if args.once:
        poller.check_and_notify()
    else:
        poller.run_continuous(args.interval)


if __name__ == '__main__':
    import re
    main()
