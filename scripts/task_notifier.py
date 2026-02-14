#!/usr/bin/env python3
"""
TASK NOTIFIER - Telegram 연동
할일 생기면 바로 알림 본내기
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import sys

sys.path.insert(0, str(Path(__file__).parent))
from autonomous_agent import DigitalChrisAutonomousAgent, TaskPriority

class TaskNotifier:
    def __init__(self):
        self.data_dir = Path("/Users/roturnjarvis/.openclaw/workspace")
        self.tasks_file = self.data_dir / "logs/pending_tasks.json"
        self.decisions_file = self.data_dir / "logs/pending_decisions.json"
        self.logs_dir = self.data_dir / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
    def save_tasks(self, tasks: List[Dict]):
        """할일을 JSON 파일로 저장"""
        with open(self.tasks_file, 'w') as f:
            json.dump({
                'updated_at': datetime.now().isoformat(),
                'count': len(tasks),
                'tasks': tasks
            }, f, indent=2)
    
    def save_decisions(self, decisions: List[Dict]):
        """결정사항을 JSON 파일로 저장"""
        with open(self.decisions_file, 'w') as f:
            json.dump({
                'updated_at': datetime.now().isoformat(),
                'count': len(decisions),
                'decisions': decisions
            }, f, indent=2)
    
    def format_telegram_message(self, task: Dict) -> str:
        """Telegram 메시지 포맷팅"""
        emoji_map = {
            'CRITICAL': '🔴',
            'HIGH': '🟠',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }
        
        priority_emoji = emoji_map.get(task.get('priority', 'MEDIUM'), '🟡')
        
        msg = f"""{priority_emoji} **새로운 할일 생성됨**

📋 **{task.get('title', 'Untitled')}**
🎯 타입: {task.get('type', 'unknown')}
⚡ 우선순위: {task.get('priority', 'MEDIUM')}
🤖 신뢰도: {task.get('confidence', 0)*100:.0f}%
🕐 생성: {task.get('created', 'now')}

🔍 확인: `cat ~/.openclaw/workspace/logs/pending_tasks.json`
"""
        return msg
    
    def format_decision_message(self, decision: Dict) -> str:
        """결정 필요 알림 포맷팅"""
        msg = f"""🤔 **결정 필요: {decision.get('recommendation', '')[:40]}...**

📊 상황: {decision.get('context', '')[:100]}...
📈 신뢰도: {decision.get('confidence', 0)*100:.0f}%
⚠️ 리스크: {decision.get('risk_level', 'unknown')}

💡 대안:
"""
        for alt in decision.get('alternatives', []):
            msg += f"  • {alt}\n"
        
        msg += "\n✅ 승인: `/approve {id}`\n❌ 거절: `/reject {id}`"
        return msg
    
    async def notify_telegram(self, message: str):
        """Telegram으로 알림 본내기 (실제로는 message.send 사용)"""
        # 실제 구현은 OpenClaw message.send로 대체
        print(f"\n📱 TELEGRAM 알림:\n{'='*50}")
        print(message)
        print('='*50)
        
        # 실제 전송 (환경변수에서 토큰 가져오기)
        try:
            from message import send
            await send(
                target="@Chrisjpark",
                message=message,
                parse_mode="Markdown"
            )
        except:
            pass  # Telegram 없으면 터미널에만 출력
    
    def get_task_summary(self) -> str:
        """현재 할일 요약"""
        if not self.tasks_file.exists():
            return "📭 할일 없음"
        
        with open(self.tasks_file) as f:
            data = json.load(f)
        
        tasks = data.get('tasks', [])
        pending = [t for t in tasks if t.get('status') == 'pending']
        running = [t for t in tasks if t.get('status') == 'running']
        completed = [t for t in tasks if t.get('status') == 'completed']
        
        msg = f"""📊 **할일 현황** (업데이트: {data.get('updated_at', 'unknown')[:16]})

⏳ 대기중: {len(pending)}개
▶️ 진행중: {len(running)}개  
✅ 완료: {len(completed)}개
"""
        
        if pending:
            msg += "\n📋 **대기중인 할일:**\n"
            for t in pending[:5]:
                emoji = {'CRITICAL':'🔴','HIGH':'🟠','MEDIUM':'🟡','LOW':'🟢'}.get(t.get('priority'), '🟡')
                msg += f"{emoji} {t.get('title', 'Untitled')[:40]}\n"
        
        return msg


class ConnectedAgent(DigitalChrisAutonomousAgent):
    """Telegram 연결된 에이전트"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notifier = TaskNotifier()
        
        # 콜백 연결
        self.on_task_complete = self._on_task_done
        self.on_decision_needed = self._on_decision
    
    def _on_task_done(self, task):
        """할일 완료시"""
        self._sync_to_file()
        print(f"✅ 완료: {task.title}")
    
    def _on_decision(self, proposal):
        """결정 필요시"""
        self._sync_to_file()
        msg = self.notifier.format_decision_message({
            'recommendation': proposal.recommendation,
            'context': proposal.context,
            'confidence': proposal.confidence,
            'risk_level': proposal.risk_level,
            'alternatives': proposal.alternatives,
            'id': proposal.id
        })
        print(f"\n🤔 결정 필요:\n{msg}")
    
    def _sync_to_file(self):
        """파일에 동기화"""
        tasks = self.get_task_queue()
        self.notifier.save_tasks(tasks)
        
        decisions = [{
            'id': d.id,
            'recommendation': d.recommendation,
            'context': d.context,
            'confidence': d.confidence,
            'risk_level': d.risk_level,
            'alternatives': d.alternatives,
            'status': d.status
        } for d in self.get_pending_decisions()]
        self.notifier.save_decisions(decisions)
    
    def create_task(self, *args, **kwargs):
        """할일 생성 + 알림"""
        task_id = super().create_task(*args, **kwargs)
        
        # 파일 저장
        self._sync_to_file()
        
        # 알림 (새로 생성된 task 찾아서)
        task = self.tasks.get(task_id)
        if task:
            msg = self.notifier.format_telegram_message({
                'title': task.title,
                'type': task.type,
                'priority': task.priority.name,
                'confidence': task.confidence,
                'created': task.created_at.isoformat(),
                'id': task_id
            })
            print(f"\n📱 알림 전송됨:\n{msg}")
        
        return task_id
    
    def get_summary(self) -> str:
        """요약 정보"""
        return self.notifier.get_task_summary()


def demo_connected_system():
    """연결된 시스템 데모"""
    print("="*60)
    print("🔗 CONNECTED AGENT - 실시간 연결 데모")
    print("="*60)
    
    agent = ConnectedAgent()
    agent.start()
    
    print("\n📩 시나리오: 이메일 3개 동시 도착")
    print("-"*60)
    
    # 이메일 1: 긴급
    print("\n1️⃣ URGENT: Luxfer 밸브 단종")
    task1 = agent.create_task(
        title="럭스퍼 밸브 단종 대응",
        task_type='email_response',
        priority=TaskPriority.CRITICAL,
        params={
            'recipient': 'tony@luxfer.com',
            'subject': 'URGENT: Valve discontinuation',
            'topic': 'emergency valve sourcing'
        },
        confidence=0.95,
        requires_approval=True
    )
    
    # 이메일 2: 일반
    print("\n2️⃣ Holy Cryogenics 견적 문의")
    task2 = agent.create_task(
        title="홀리크라이오 NIE 견적 답변",
        task_type='quotation_response',
        priority=TaskPriority.MEDIUM,
        params={
            'recipient': 'yulia@holy-cryo.com',
            'subject': 'RE: NIE System Quotation'
        },
        confidence=0.88
    )
    
    # 이메일 3: 낮은 우선순위
    print("\n3️⃣ 뉴스레터 구독")
    task3 = agent.create_task(
        title="주간 뉴스레터 읽기",
        task_type='read_later',
        priority=TaskPriority.LOW,
        params={'type': 'newsletter'},
        confidence=0.99
    )
    
    # 결정 필요 상황
    print("\n🤔 결정 필요 상황 발생")
    agent.propose_decision(
        context="Luxfer가 대체 밸브 20% 할증 요청",
        recommendation="20% 할증 승인 (관계 유지를 위해)",
        confidence=0.87,
        risk_level='medium',
        alternatives=["15% 할증 (표준)", "25% 할증 (긴급 할증)"]
    )
    
    # 상태 확인
    print("\n" + "="*60)
    print(agent.get_summary())
    print("="*60)
    
    # 파일 확인 방법
    print("\n💾 저장 위치:")
    print(f"   할일: ~/.openclaw/workspace/logs/pending_tasks.json")
    print(f"   결정: ~/.openclaw/workspace/logs/pending_decisions.json")
    
    print("\n📱 Telegram 연결시 실시간 알림 수신 가능")
    
    agent.stop()


if __name__ == '__main__':
    demo_connected_system()
