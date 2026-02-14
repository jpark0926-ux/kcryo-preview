#!/usr/bin/env python3
"""
PHASE 6: AUTONOMOUS AGENT - Digital Chris v1.0
Self-running task execution + decision recommendations + human approval workflow
"""

import json
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import queue

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class AutonomousTask:
    id: str
    title: str
    description: str
    type: str  # 'email_response', 'schedule_meeting', 'send_reminder', 'generate_report', 'decision_proposal'
    priority: TaskPriority
    status: TaskStatus
    created_at: datetime
    assigned_to: str  # 'auto' or specific agent
    params: Dict
    
    # For autonomous execution
    confidence: float = 0.0  # AI confidence 0-1
    requires_approval: bool = False
    approval_reason: str = ""
    
    # Execution tracking
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict] = None
    error: Optional[str] = None

@dataclass
class DecisionProposal:
    id: str
    context: str
    recommendation: str
    confidence: float
    risk_level: str  # 'low', 'medium', 'high'
    alternatives: List[str]
    auto_approve_threshold: float = 0.9  # Auto-approve if confidence > this
    
    status: str = "pending"  # pending, approved, rejected, modified
    human_decision: Optional[str] = None
    human_notes: Optional[str] = None


class DigitalChrisAutonomousAgent:
    """
    Fully autonomous agent that can:
    1. Monitor incoming data (emails, calendar, etc.)
    2. Create and prioritize tasks
    3. Execute low-risk tasks automatically
    4. Request human approval for high-risk decisions
    5. Learn from human feedback
    """
    
    def __init__(self, data_dir="/Users/roturnjarvis/.openclaw/workspace"):
        self.data_dir = Path(data_dir)
        self.decisions_dir = self.data_dir / "memory/decisions"
        self.logs_dir = self.data_dir / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        # Task management
        self.task_queue: queue.PriorityQueue = queue.PriorityQueue()
        self.tasks: Dict[str, AutonomousTask] = {}
        self.decisions: Dict[str, DecisionProposal] = {}
        
        # Agent state
        self.is_running = False
        self.autonomy_level = 0.5  # 0 = full manual, 1 = full auto
        self.metrics = {
            'tasks_completed_today': 0,
            'emails_auto_responded': 0,
            'meetings_scheduled': 0,
            'decisions_proposed': 0,
            'decisions_approved': 0,
            'avg_confidence': 0.0
        }
        
        # Activity log
        self.activity_log: List[Dict] = []
        
        # Callbacks for integration
        self.on_decision_needed: Optional[Callable] = None
        self.on_task_complete: Optional[Callable] = None
        
        # Load existing state
        self._load_state()
    
    def _load_state(self):
        """Load persisted state"""
        state_file = self.logs_dir / "agent_state.json"
        if state_file.exists():
            try:
                with open(state_file) as f:
                    data = json.load(f)
                    self.metrics = data.get('metrics', self.metrics)
                    self.autonomy_level = data.get('autonomy_level', 0.5)
            except:
                pass
    
    def _save_state(self):
        """Persist agent state"""
        state_file = self.logs_dir / "agent_state.json"
        with open(state_file, 'w') as f:
            json.dump({
                'metrics': self.metrics,
                'autonomy_level': self.autonomy_level,
                'last_saved': datetime.now().isoformat()
            }, f, indent=2)
    
    def start(self):
        """Start the autonomous agent"""
        self.is_running = True
        self._log_activity("AGENT", "Autonomous agent started")
        
        # Start background worker thread
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        
        print(f"[AGENT] Digital Chris v1.0 started")
        print(f"[AGENT] Autonomy level: {self.autonomy_level*100:.0f}%")
        print(f"[AGENT] Task queue: {self.task_queue.qsize()} pending")
    
    def stop(self):
        """Stop the agent"""
        self.is_running = False
        self._save_state()
        self._log_activity("AGENT", "Autonomous agent stopped")
        print("[AGENT] Stopped")
    
    def _worker_loop(self):
        """Background worker that processes tasks"""
        while self.is_running:
            try:
                # Get next task (with timeout to allow checking is_running)
                priority, task_id = self.task_queue.get(timeout=1)
                task = self.tasks.get(task_id)
                
                if task and task.status == TaskStatus.PENDING:
                    self._execute_task(task)
                
            except queue.Empty:
                continue
            except Exception as e:
                self._log_activity("ERROR", f"Worker error: {str(e)}")
    
    def _execute_task(self, task: AutonomousTask):
        """Execute a single task"""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        
        self._log_activity("TASK", f"Executing: {task.title}")
        
        try:
            # Route to appropriate handler
            handlers = {
                'email_response': self._handle_email_response,
                'schedule_meeting': self._handle_schedule_meeting,
                'send_reminder': self._handle_send_reminder,
                'generate_report': self._handle_generate_report,
                'decision_proposal': self._handle_decision_proposal
            }
            
            handler = handlers.get(task.type)
            if handler:
                result = handler(task)
                task.result = result
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                self.metrics['tasks_completed_today'] += 1
                
                if self.on_task_complete:
                    self.on_task_complete(task)
                
                self._log_activity("TASK", f"Completed: {task.title}")
            else:
                raise ValueError(f"Unknown task type: {task.type}")
                
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            self._log_activity("ERROR", f"Task failed: {task.title} - {str(e)}")
    
    # ========== TASK HANDLERS ==========
    
    def _handle_email_response(self, task: AutonomousTask) -> Dict:
        """Generate and optionally send email response"""
        params = task.params
        
        # Generate response (would call Phase 3 AI in production)
        response = f"""Hi {params.get('recipient', 'there')},

Thank you for your email regarding {params.get('topic', 'our discussion')}.

{params.get('context', 'I will review and get back to you shortly.')}

Best regards,
Chris
"""
        
        # Auto-send if confidence high enough
        if task.confidence > self.autonomy_level:
            self.metrics['emails_auto_responded'] += 1
            return {
                'action': 'sent',
                'response': response,
                'auto_sent': True
            }
        else:
            return {
                'action': 'drafted',
                'response': response,
                'auto_sent': False,
                'reason': 'Confidence below autonomy threshold'
            }
    
    def _handle_schedule_meeting(self, task: AutonomousTask) -> Dict:
        """Schedule a meeting"""
        params = task.params
        
        # Would integrate with Google Calendar in production
        self.metrics['meetings_scheduled'] += 1
        
        return {
            'action': 'scheduled',
            'with': params.get('attendee'),
            'topic': params.get('topic'),
            'proposed_times': ['2026-02-25 10:00', '2026-02-25 14:00']
        }
    
    def _handle_send_reminder(self, task: AutonomousTask) -> Dict:
        """Send a reminder"""
        return {
            'action': 'reminder_sent',
            'to': task.params.get('recipient'),
            'message': task.params.get('message')
        }
    
    def _handle_generate_report(self, task: AutonomousTask) -> Dict:
        """Generate a report"""
        report_type = task.params.get('report_type', 'daily')
        
        report = f"""=== {report_type.upper()} REPORT ===
Generated: {datetime.now().isoformat()}

Tasks Completed: {self.metrics['tasks_completed_today']}
Emails Processed: {self.metrics['emails_auto_responded']}
Decisions Pending: {len([d for d in self.decisions.values() if d.status == 'pending'])}
"""
        
        return {
            'action': 'report_generated',
            'type': report_type,
            'content': report
        }
    
    def _handle_decision_proposal(self, task: AutonomousTask) -> Dict:
        """Create a decision proposal for human review"""
        params = task.params
        
        proposal = DecisionProposal(
            id=f"DEC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            context=params.get('context', ''),
            recommendation=params.get('recommendation', ''),
            confidence=task.confidence,
            risk_level=params.get('risk_level', 'medium'),
            alternatives=params.get('alternatives', [])
        )
        
        self.decisions[proposal.id] = proposal
        self.metrics['decisions_proposed'] += 1
        
        # Check if we can auto-approve
        if proposal.confidence >= proposal.auto_approve_threshold and proposal.risk_level == 'low':
            proposal.status = 'approved'
            proposal.human_decision = 'approved'
            proposal.human_notes = 'Auto-approved by system'
            self.metrics['decisions_approved'] += 1
            
            return {
                'action': 'auto_approved',
                'proposal_id': proposal.id,
                'decision': proposal.recommendation
            }
        else:
            # Queue for human approval
            proposal.status = 'pending'
            
            if self.on_decision_needed:
                self.on_decision_needed(proposal)
            
            return {
                'action': 'awaiting_approval',
                'proposal_id': proposal.id,
                'confidence': proposal.confidence,
                'risk': proposal.risk_level
            }
    
    # ========== PUBLIC API ==========
    
    def create_task(self, title: str, task_type: str, priority: TaskPriority = TaskPriority.MEDIUM,
                   params: Dict = None, confidence: float = 0.0, requires_approval: bool = False) -> str:
        """Create a new task"""
        task_id = f"TASK_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000,9999)}"
        
        task = AutonomousTask(
            id=task_id,
            title=title,
            description=params.get('description', title) if params else title,
            type=task_type,
            priority=priority,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            assigned_to='auto',
            params=params or {},
            confidence=confidence,
            requires_approval=requires_approval
        )
        
        self.tasks[task_id] = task
        self.task_queue.put((priority.value, task_id))
        
        self._log_activity("TASK", f"Created: {title} (ID: {task_id})")
        
        return task_id
    
    def propose_decision(self, context: str, recommendation: str, confidence: float,
                        risk_level: str = 'medium', alternatives: List[str] = None) -> str:
        """Propose a decision for human review"""
        task_id = self.create_task(
            title=f"Decision: {recommendation[:50]}...",
            task_type='decision_proposal',
            priority=TaskPriority.HIGH if risk_level == 'high' else TaskPriority.MEDIUM,
            params={
                'context': context,
                'recommendation': recommendation,
                'risk_level': risk_level,
                'alternatives': alternatives or []
            },
            confidence=confidence,
            requires_approval=True
        )
        return task_id
    
    def approve_decision(self, decision_id: str, approved: bool = True, notes: str = "") -> bool:
        """Human approves or rejects a decision"""
        # Find the decision
        proposal = self.decisions.get(decision_id)
        if not proposal:
            return False
        
        proposal.status = 'approved' if approved else 'rejected'
        proposal.human_decision = 'approved' if approved else 'rejected'
        proposal.human_notes = notes
        
        if approved:
            self.metrics['decisions_approved'] += 1
        
        self._log_activity("DECISION", f"{decision_id}: {'APPROVED' if approved else 'REJECTED'}")
        
        return True
    
    def get_pending_decisions(self) -> List[DecisionProposal]:
        """Get all pending decisions"""
        return [d for d in self.decisions.values() if d.status == 'pending']
    
    def get_task_queue(self) -> List[Dict]:
        """Get current task queue status"""
        result = []
        for task in self.tasks.values():
            result.append({
                'id': task.id,
                'title': task.title,
                'type': task.type,
                'priority': task.priority.name,
                'status': task.status.value,
                'confidence': task.confidence,
                'created': task.created_at.isoformat()
            })
        return sorted(result, key=lambda x: x['created'], reverse=True)
    
    def get_metrics(self) -> Dict:
        """Get current metrics"""
        return {
            **self.metrics,
            'queue_size': self.task_queue.qsize(),
            'pending_decisions': len(self.get_pending_decisions()),
            'autonomy_level': self.autonomy_level,
            'is_running': self.is_running
        }
    
    def get_activity_log(self, limit: int = 20) -> List[Dict]:
        """Get recent activity"""
        return self.activity_log[-limit:]
    
    def _log_activity(self, category: str, message: str):
        """Log activity"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'category': category,
            'message': message
        }
        self.activity_log.append(entry)
        
        # Keep log manageable
        if len(self.activity_log) > 1000:
            self.activity_log = self.activity_log[-500:]
    
    def simulate_incoming_email(self, sender: str, subject: str, urgency: str = 'normal'):
        """Simulate receiving an email (for demo)"""
        priority = TaskPriority.HIGH if urgency == 'urgent' else TaskPriority.MEDIUM
        confidence = 0.9 if urgency == 'normal' else 0.6
        
        task_id = self.create_task(
            title=f"Reply to: {subject[:40]}",
            task_type='email_response',
            priority=priority,
            params={
                'recipient': sender,
                'subject': subject,
                'topic': subject,
                'urgency': urgency
            },
            confidence=confidence,
            requires_approval=(urgency == 'urgent')
        )
        
        return task_id


def main():
    """Demo the autonomous agent"""
    print("=" * 70)
    print("PHASE 6: AUTONOMOUS AGENT - Digital Chris v1.0")
    print("=" * 70)
    
    agent = DigitalChrisAutonomousAgent()
    
    # Set up callbacks
    def on_decision(proposal):
        print(f"\n[DECISION NEEDED] {proposal.recommendation[:60]}...")
        print(f"                  Confidence: {proposal.confidence:.0%} | Risk: {proposal.risk_level}")
    
    def on_task_complete(task):
        print(f"[✓] Task completed: {task.title}")
    
    agent.on_decision_needed = on_decision
    agent.on_task_complete = on_task_complete
    
    # Start agent
    agent.start()
    
    # Simulate various tasks
    print("\n📥 SIMULATING INCOMING TASKS...")
    print("-" * 50)
    
    # 1. Regular email (should auto-process)
    agent.simulate_incoming_email(
        "yulia@holy-cryo.com",
        "Following up on NIE quotation",
        urgency='normal'
    )
    
    # 2. Urgent email (needs approval)
    agent.simulate_incoming_email(
        "tony@luxfer.com",
        "URGENT: Valve shortage",
        urgency='urgent'
    )
    
    # 3. Decision proposal
    agent.propose_decision(
        context="Luxfer requesting emergency pricing for alternative valves",
        recommendation="Approve 20% markup (middle ground) to maintain relationship",
        confidence=0.87,
        risk_level='medium',
        alternatives=["15% markup (standard)", "25% markup (urgency premium)"]
    )
    
    # 4. Meeting scheduling
    agent.create_task(
        title="Schedule Hyundai follow-up",
        task_type='schedule_meeting',
        priority=TaskPriority.MEDIUM,
        params={'attendee': 'Hyundai', 'topic': 'FCEV solenoid valve update'},
        confidence=0.85
    )
    
    # 5. Generate report
    agent.create_task(
        title="Generate weekly summary",
        task_type='generate_report',
        priority=TaskPriority.LOW,
        params={'report_type': 'weekly'},
        confidence=0.95
    )
    
    # Wait for tasks to process
    print("\n⏳ Processing tasks...")
    time.sleep(2)
    
    # Show status
    print("\n📊 CURRENT STATUS:")
    print("-" * 50)
    metrics = agent.get_metrics()
    print(f"  Tasks completed today: {metrics['tasks_completed_today']}")
    print(f"  Emails auto-responded: {metrics['emails_auto_responded']}")
    print(f"  Meetings scheduled: {metrics['meetings_scheduled']}")
    print(f"  Decisions pending: {metrics['pending_decisions']}")
    print(f"  Queue size: {metrics['queue_size']}")
    
    # Show pending decisions
    print("\n🤔 PENDING DECISIONS:")
    print("-" * 50)
    for d in agent.get_pending_decisions():
        print(f"\n  [{d.id}]")
        print(f"  Context: {d.context}")
        print(f"  AI Says: {d.recommendation}")
        print(f"  Confidence: {d.confidence:.0%} | Risk: {d.risk_level}")
        print(f"  Alternatives: {', '.join(d.alternatives) if d.alternatives else 'None'}")
    
    # Show activity log
    print("\n📜 RECENT ACTIVITY:")
    print("-" * 50)
    for act in agent.get_activity_log(10):
        ts = act['timestamp'][11:19]
        print(f"  [{ts}] {act['category']:8} | {act['message'][:50]}...")
    
    # Simulate human approval
    print("\n✅ SIMULATING HUMAN APPROVAL...")
    for d in agent.get_pending_decisions():
        agent.approve_decision(d.id, approved=True, notes="Approved for execution")
        print(f"  Approved: {d.id}")
    
    # Stop agent
    agent.stop()
    
    print("\n" + "=" * 70)
    print("PHASE 6 COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    main()
