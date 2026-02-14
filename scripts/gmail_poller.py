#!/usr/bin/env python3
"""
GMAIL POLLER - 실시간 이메일 자동화
15분마다 새 이메일 확인 → AI 분석 → Telegram 알림
"""

import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import sys
import time

# 상위 디렉토리 추가
sys.path.insert(0, str(Path(__file__).parent))

from digital_chris_ai import DigitalChrisAI
from autonomous_agent import DigitalChrisAutonomousAgent, TaskPriority
from task_notifier import ConnectedAgent

class GmailPoller:
    def __init__(self):
        self.data_dir = Path("/Users/roturnjarvis/.openclaw/workspace")
        self.state_file = self.data_dir / "logs/gmail_poller_state.json"
        self.processed_ids = self._load_processed_ids()
        self.ai = DigitalChrisAI()
        self.agent = ConnectedAgent()
        
    def _load_processed_ids(self) -> set:
        """이미 처리한 이메일 ID 로드"""
        if self.state_file.exists():
            with open(self.state_file) as f:
                data = json.load(f)
                return set(data.get('processed_ids', []))
        return set()
    
    def _save_processed_ids(self):
        """처리한 이메일 ID 저장"""
        self.state_file.parent.mkdir(exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump({
                'last_check': datetime.now().isoformat(),
                'processed_count': len(self.processed_ids),
                'processed_ids': list(self.processed_ids)
            }, f, indent=2)
    
    def fetch_recent_emails(self, hours: int = 1) -> list:
        """최근 이메일 가져오기"""
        # 저장된 이메일 데이터 사용 (1803개)
        email_file = self.data_dir / "logs/all_pst_emails.json"
        if email_file.exists():
            try:
                with open(email_file) as f:
                    all_emails = json.load(f)
                
                # 마지막 3개만 (데모용)
                recent = all_emails[-3:] if len(all_emails) > 3 else all_emails
                
                # 형식 통일
                formatted = []
                for e in recent:
                    formatted.append({
                        'ID': e.get('id', str(hash(str(e)))),
                        'Date': e.get('date', datetime.now().isoformat()),
                        'From': e.get('from', 'unknown'),
                        'Subject': e.get('subject', 'No subject'),
                        'Body': e.get('body', e.get('snippet', '')),
                        'Snippet': e.get('snippet', '')
                    })
                return formatted
                
            except Exception as e:
                print(f"[POLLER] Error: {e}")
        
        return []
    
    def process_email(self, email: dict) -> dict:
        """이메일 분석 및 처리"""
        email_id = email.get('ID', '')
        sender = email.get('From', 'unknown')
        subject = email.get('Subject', 'No subject')
        body = email.get('Body', email.get('Snippet', ''))
        
        # 중복 체크
        if email_id in self.processed_ids:
            return None
        
        print(f"[POLLER] Processing: {sender} - {subject[:50]}...")
        
        # Phase 3: AI 분석
        analysis = self.ai.process_email(sender, subject, body)
        
        # 결과 저장
        result = {
            'email_id': email_id,
            'sender': sender,
            'subject': subject,
            'analysis': analysis,
            'processed_at': datetime.now().isoformat()
        }
        
        # 처리된 ID 추가
        self.processed_ids.add(email_id)
        
        return result
    
    def create_tasks_from_email(self, result: dict):
        """이메일 분석 결과로 할일 생성"""
        analysis = result['analysis']
        sender = result['sender']
        subject = result['subject']
        
        priority_map = {
            'critical': TaskPriority.CRITICAL,
            'high': TaskPriority.HIGH,
            'medium': TaskPriority.MEDIUM,
            'low': TaskPriority.LOW
        }
        
        priority = priority_map.get(analysis.get('priority', 'medium'), TaskPriority.MEDIUM)
        sentiment = analysis.get('sentiment', {})
        
        # 긴급 이메일이면 CRITICAL로 업그레이드
        if sentiment.get('urgent', False) and priority != TaskPriority.CRITICAL:
            priority = TaskPriority.HIGH
        
        confidence = analysis.get('suggested_response', {}).get('confidence', 0.7)
        
        # 할일 생성
        task_type = 'email_response'
        if 'quotation' in subject.lower() or 'quote' in subject.lower():
            task_type = 'quotation_response'
        elif 'meeting' in subject.lower():
            task_type = 'schedule_meeting'
        
        requires_approval = confidence < 0.8 or priority == TaskPriority.CRITICAL
        
        task_id = self.agent.create_task(
            title=f"Reply: {subject[:40]}",
            task_type=task_type,
            priority=priority,
            params={
                'recipient': sender,
                'subject': subject,
                'ai_analysis': analysis,
                'suggested_response': analysis.get('suggested_response', {}).get('response', '')
            },
            confidence=confidence,
            requires_approval=requires_approval
        )
        
        print(f"[POLLER] Task created: {task_id[:20]}... (Priority: {priority.name})")
        
        # 긴급/중요 이메일은 결정 제안도 생성
        if priority in [TaskPriority.CRITICAL, TaskPriority.HIGH]:
            self.agent.propose_decision(
                context=f"Email from {sender}: {subject}",
                recommendation=f"Respond with AI-suggested reply (confidence: {confidence:.0%})",
                confidence=confidence,
                risk_level='high' if priority == TaskPriority.CRITICAL else 'medium',
                alternatives=["Respond manually", "Schedule call", "Delegate"]
            )
            print(f"[POLLER] Decision proposal created")
    
    def send_telegram_notification(self, result: dict):
        """Telegram 알림 전송"""
        analysis = result['analysis']
        sender = result['sender']
        subject = result['subject']
        
        sentiment = analysis.get('sentiment', {})
        priority = analysis.get('priority', 'medium')
        
        emoji_map = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}
        emoji = emoji_map.get(priority, '🟡')
        urgent_text = "⚡ 긴급! " if sentiment.get('urgent') else ""
        
        message = f"""{emoji} {urgent_text}새 이메일

📧 **{sender}**
📝 {subject[:100]}{'...' if len(subject) > 100 else ''}

📊 분석:
• 감정: {sentiment.get('overall', 'neutral')}
• 우선순위: {priority.upper()}
• 긴급: {'예' if sentiment.get('urgent') else '아니오'}

✍️ AI 답변:
_{analysis.get('suggested_response', {}).get('response', 'N/A')[:150]}..._

💡 추천: {(analysis.get('recommendations') or [{'title': 'N/A'}])[0].get('title', 'N/A')}

📂 확인: `cat logs/pending_tasks.json`
"""
        
        print(f"\n{'='*60}")
        print("📱 TELEGRAM 알림:")
        print('='*60)
        print(message)
        print('='*60)
    
    def run_once(self):
        """한 번 실행"""
        print(f"\n[{'='*60}")
        print(f"[POLLER] Gmail check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[{'='*60}")
        
        self.agent.start()
        
        emails = self.fetch_recent_emails(hours=1)
        
        if not emails:
            print("[POLLER] No emails to process")
            self.agent.stop()
            return
        
        print(f"[POLLER] Checking {len(emails)} emails...")
        
        new_count = 0
        for email in emails:
            email_id = email.get('ID', '')
            
            if email_id in self.processed_ids:
                print(f"[POLLER] Already processed: {email_id[:20]}...")
                continue
            
            result = self.process_email(email)
            if result:
                self.create_tasks_from_email(result)
                self.send_telegram_notification(result)
                new_count += 1
        
        self._save_processed_ids()
        self.agent.stop()
        
        print(f"[POLLER] Processed {new_count} new emails")
        print(f"[POLLER] Total processed: {len(self.processed_ids)}")
    
    def run_continuous(self, interval_minutes: int = 15):
        """계속 실행"""
        print(f"[POLLER] Starting (every {interval_minutes} min)")
        print("[POLLER] Press Ctrl+C to stop")
        
        try:
            while True:
                self.run_once()
                print(f"[POLLER] Sleep {interval_minutes} min...\n")
                time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            print("\n[POLLER] Stopped")
            self._save_processed_ids()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--interval', type=int, default=15, help='Polling interval in minutes')
    args = parser.parse_args()
    
    poller = GmailPoller()
    
    if args.once:
        poller.run_once()
    else:
        poller.run_continuous(args.interval)


if __name__ == '__main__':
    main()
