#!/usr/bin/env python3
"""
TELEGRAM NOTIFIER - 실제 Telegram 메시지 전송
@ChrisJarvisHotTopicbot 또는 메인 계정으로 알림
"""

import json
import os
from datetime import datetime
from pathlib import Path
import sys

# 환경변수에서 토큰 가져오기
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8551723387:AAGbR3Sqg8SFFGw_16iIqQd1WjdkCTVcjAw')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '6948605509')

class TelegramNotifier:
    def __init__(self):
        self.data_dir = Path("/Users/roturnjarvis/.openclaw/workspace")
        self.log_file = self.data_dir / "logs/telegram_notifications.json"
        
        # message tool 사용을 위한 설정
        self.gateway_url = os.getenv('GATEWAY_URL', 'http://localhost:8080')
        self.gateway_token = os.getenv('GATEWAY_TOKEN', '')
    
    def send_message(self, message: str, parse_mode: str = "Markdown") -> bool:
        """실제 Telegram 메시지 전송"""
        try:
            # OpenClaw의 message.send 기능 사용
            # 참고: 실제 환경에서는 exec로 curl 또는 requests 사용
            import subprocess
            
            # 메시지 내용 정리 (JSON escaping)
            safe_message = message.replace('"', '\\"').replace('\n', '\\n')
            
            # Telegram API 직접 호출
            curl_cmd = [
                'curl', '-s', '-X', 'POST',
                f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps({
                    'chat_id': CHAT_ID,
                    'text': message,
                    'parse_mode': parse_mode,
                    'disable_web_page_preview': True
                })
            ]
            
            result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                response = json.loads(result.stdout)
                if response.get('ok'):
                    self._log_notification(message, True)
                    print(f"[TELEGRAM] ✓ Message sent successfully")
                    return True
                else:
                    error = response.get('description', 'Unknown error')
                    print(f"[TELEGRAM] ✗ API error: {error}")
                    self._log_notification(message, False, error)
                    return False
            else:
                print(f"[TELEGRAM] ✗ Curl failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[TELEGRAM] ✗ Error: {e}")
            self._log_notification(message, False, str(e))
            return False
    
    def send_notification(self, title: str, body: str, priority: str = "normal"):
        """우선순위별 알림 전송"""
        emoji_map = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢',
            'normal': '⚪'
        }
        emoji = emoji_map.get(priority, '⚪')
        
        message = f"""{emoji} **{title}**

{body}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')} KST"""
        
        return self.send_message(message)
    
    def send_task_notification(self, task: dict):
        """할일 생성 알림"""
        priority = task.get('priority', 'MEDIUM')
        emoji_map = {
            'CRITICAL': '🔴',
            'HIGH': '🟠',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }
        emoji = emoji_map.get(priority, '🟡')
        
        title = task.get('title', 'New Task')
        task_type = task.get('type', 'unknown')
        confidence = task.get('confidence', 0)
        
        message = f"""{emoji} **새로운 할일 생성됨**

📋 **{title}**
🎯 타입: {task_type}
⚡ 우선순위: {priority}
🤖 신뢰도: {confidence*100:.0f}%

✅ 확인: pending_tasks.json 파일 참고"""
        
        return self.send_message(message)
    
    def send_decision_notification(self, decision: dict):
        """결정 필요 알림"""
        confidence = decision.get('confidence', 0)
        risk = decision.get('risk_level', 'medium')
        
        # 위험도에 따른 이모지
        risk_emoji = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}
        
        message = f"""🤔 **결정 필요**

💡 추천: {decision.get('recommendation', 'N/A')[:80]}{'...' if len(decision.get('recommendation', '')) > 80 else ''}

📊 상황: {decision.get('context', 'N/A')[:100]}{'...' if len(decision.get('context', '')) > 100 else ''}
📈 신뢰도: {confidence*100:.0f}%
⚠️ 리스크: {risk_emoji.get(risk, '🟡')} {risk}

💬 대안:
"""
        for alt in decision.get('alternatives', [])[:3]:
            message += f"  • {alt}\n"
        
        message += f"\n⏰ {datetime.now().strftime('%H:%M')}까지 결정 필요"
        
        return self.send_message(message)
    
    def send_email_notification(self, email_analysis: dict):
        """이메일 분석 결과 알림"""
        sender = email_analysis.get('sender', 'Unknown')
        subject = email_analysis.get('subject', 'No subject')
        analysis = email_analysis.get('analysis', {})
        
        sentiment = analysis.get('sentiment', {})
        priority = analysis.get('priority', 'medium')
        
        # 우선순위 이모지
        emoji_map = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}
        emoji = emoji_map.get(priority, '🟡')
        
        # 긴급 표시
        urgent_text = "⚡ 긴급! " if sentiment.get('urgent') else ""
        
        message = f"""{emoji} {urgent_text}새 이메일 분석 완료

📧 **{sender}**
📝 {subject[:100]}{'...' if len(subject) > 100 else ''}

📊 분석 결과:
• 감정: {sentiment.get('overall', 'neutral')}
• 우선순위: {priority.upper()}
• 긴급: {'예' if sentiment.get('urgent') else '아니오'}

✍️ AI 답변:
_{analysis.get('suggested_response', {}).get('response', 'N/A')[:150]}..._

💡 추천 액션:
{(analysis.get('recommendations') or [{'title': '수동 확인 필요'}])[0].get('title', '확인 필요')}

📂 할일 확인: `cat logs/pending_tasks.json`"""
        
        return self.send_message(message)
    
    def send_daily_summary(self, metrics: dict):
        """일일 요약 알림"""
        message = f"""📊 **일일 리포트** ({datetime.now().strftime('%Y-%m-%d')})

📧 이메일:
• 새 이메일: {metrics.get('new_emails', 0)}개
• 자동 처리: {metrics.get('auto_processed', 0)}개
• 수동 확인 필요: {metrics.get('manual_review', 0)}개

📋 할일:
• 생성됨: {metrics.get('tasks_created', 0)}개
• 완료: {metrics.get('tasks_completed', 0)}개
• 대기중: {metrics.get('tasks_pending', 0)}개

🤔 결정:
• 제안됨: {metrics.get('decisions_proposed', 0)}개
• 승인 대기: {metrics.get('decisions_pending', 0)}개

💰 포트폴리오:
• 총 자산: ₩{metrics.get('portfolio_value', 0):,}
• 변동: {metrics.get('portfolio_change', 0):+.2f}%

────────────────
💡 오늘의 추천: {metrics.get('daily_tip', '없음')}"""
        
        return self.send_message(message)
    
    def _log_notification(self, message: str, success: bool, error: str = None):
        """알림 로그 저장"""
        self.log_file.parent.mkdir(exist_ok=True)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'message_preview': message[:100],
            'success': success,
            'error': error
        }
        
        logs = []
        if self.log_file.exists():
            try:
                with open(self.log_file) as f:
                    logs = json.load(f)
            except:
                pass
        
        logs.append(log_entry)
        
        # 최근 100개만 유지
        if len(logs) > 100:
            logs = logs[-100:]
        
        with open(self.log_file, 'w') as f:
            json.dump(logs, f, indent=2)


def test_telegram_connection():
    """Telegram 연결 테스트"""
    print("="*60)
    print("📱 TELEGRAM CONNECTION TEST")
    print("="*60)
    
    notifier = TelegramNotifier()
    
    # 테스트 메시지
    test_msg = f"""🧪 **Telegram 연결 테스트**

이 메시지가 보이면 연결 성공!

⏰ 테스트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} KST
🤖 발신: Digital Chris v1.0
📍 위치: Mac mini (로턴자비스)"""
    
    result = notifier.send_message(test_msg)
    
    if result:
        print("\n✅ Telegram 연결 성공!")
        print(f"   Bot: @ChrisJarvisHotTopicbot")
        print(f"   Chat: {CHAT_ID}")
    else:
        print("\n❌ Telegram 연결 실패")
        print("   토큰/Chat ID 확인 필요")
    
    return result


def demo_notifications():
    """모든 알림 타입 데모"""
    print("="*60)
    print("📱 ALL NOTIFICATION TYPES DEMO")
    print("="*60)
    
    notifier = TelegramNotifier()
    
    # 1. 할일 알림
    print("\n1️⃣ Task notification...")
    notifier.send_task_notification({
        'title': '럭스퍼 밸브 긴급 대응',
        'type': 'email_response',
        'priority': 'CRITICAL',
        'confidence': 0.95
    })
    
    # 2. 결정 알림
    print("\n2️⃣ Decision notification...")
    notifier.send_decision_notification({
        'recommendation': '20% 할증 승인',
        'context': 'Luxfer 대체 밸브 긴급 요청',
        'confidence': 0.87,
        'risk_level': 'medium',
        'alternatives': ['15% 할증', '25% 할증']
    })
    
    # 3. 이메일 알림
    print("\n3️⃣ Email notification...")
    notifier.send_email_notification({
        'sender': 'tony@luxfer.com',
        'subject': 'URGENT: Valve discontinuation timeline',
        'analysis': {
            'sentiment': {'overall': 'negative', 'urgent': True},
            'priority': 'critical',
            'suggested_response': {
                'response': 'We need to address this immediately. When are you available for an emergency call?'
            },
            'recommendations': [{'title': 'Schedule emergency meeting'}]
        }
    })
    
    # 4. 일일 요약
    print("\n4️⃣ Daily summary...")
    notifier.send_daily_summary({
        'new_emails': 12,
        'auto_processed': 8,
        'manual_review': 4,
        'tasks_created': 6,
        'tasks_completed': 4,
        'tasks_pending': 2,
        'decisions_proposed': 2,
        'decisions_pending': 1,
        'portfolio_value': 562634662,
        'portfolio_change': 2.35,
        'daily_tip': 'Holy Cryogenics PO 승인 대기중'
    })
    
    print("\n" + "="*60)
    print("✅ All notifications sent!")
    print("="*60)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', help='Test connection')
    parser.add_argument('--demo', action='store_true', help='Demo all notification types')
    parser.add_argument('--message', help='Send custom message')
    args = parser.parse_args()
    
    if args.test:
        test_telegram_connection()
    elif args.demo:
        demo_notifications()
    elif args.message:
        notifier = TelegramNotifier()
        notifier.send_message(args.message)
    else:
        # 기본: 연결 테스트
        test_telegram_connection()
