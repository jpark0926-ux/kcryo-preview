#!/usr/bin/env python3
"""
DIGITAL CHRIS v1.0 - MASTER CONTROLLER
Integrates all 6 phases into unified system

Usage:
    python digital_chris_master.py --mode [ai|time|voice|agent|all]
    python digital_chris_master.py --process-email --from "sender" --subject "..." --body "..."
    python digital_chris_master.py --voice "Jarvis, show me Luxfer"
    python digital_chris_master.py --slack "status Hyundai"
"""

import argparse
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

from digital_chris_ai import DigitalChrisAI
from time_machine import TimeMachine
from jarvis_voice_slack import JarvisVoiceInterface, SlackJarvisBot
from autonomous_agent import DigitalChrisAutonomousAgent, TaskPriority


class DigitalChrisMaster:
    """
    Unified interface for all Digital Chris capabilities
    """
    
    def __init__(self, data_dir="/Users/roturnjarvis/.openclaw/workspace"):
        self.data_dir = data_dir
        
        # Initialize all phase modules
        print("[MASTER] Initializing Digital Chris v1.0...")
        self.ai = DigitalChrisAI(data_dir)
        self.time_machine = TimeMachine(data_dir)
        self.voice = JarvisVoiceInterface(data_dir)
        self.slack = SlackJarvisBot()
        self.agent = DigitalChrisAutonomousAgent(data_dir)
        
        print("[MASTER] All systems online")
    
    # ========== PHASE 3: AI ==========
    
    def process_email(self, sender: str, subject: str, body: str) -> dict:
        """Process email with full AI analysis"""
        print(f"\n{'='*60}")
        print("PHASE 3: AI EMAIL PROCESSING")
        print(f"{'='*60}")
        
        result = self.ai.process_email(sender, subject, body)
        
        print(f"\n📧 From: {result['sender']}")
        print(f"📋 Subject: {result['subject']}")
        print(f"\n📊 SENTIMENT:")
        print(f"   Overall: {result['sentiment']['overall']}")
        print(f"   Urgent: {'YES' if result['sentiment']['urgent'] else 'NO'}")
        print(f"   Pos: {result['sentiment']['positive']:.0%}, Neg: {result['sentiment']['negative']:.0%}")
        print(f"\n✍️  AI SUGGESTED RESPONSE:")
        print(f"   Confidence: {result['suggested_response']['confidence']:.0%}")
        print(f"   Tone: {result['suggested_response']['tone']}")
        print(f"\n   \"{result['suggested_response']['response']}\"")
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in result['recommendations']:
            print(f"   [{rec['score']}%] {rec['title']}: {rec['description']}")
        
        return result
    
    def get_partner_health(self, partner: str) -> dict:
        """Get complete partner health report"""
        return self.ai.get_partner_health(partner)
    
    # ========== PHASE 4: TIME MACHINE ==========
    
    def time_travel(self, year: int) -> dict:
        """View network state at specific year"""
        print(f"\n{'='*60}")
        print(f"PHASE 4: TIME MACHINE → {year}")
        print(f"{'='*60}")
        
        state = self.time_machine.get_state_at_date(f"{year}-06-01")
        
        print(f"\n📅 Network State: {year}")
        print(f"   Active Partners: {state['network_size']}")
        print(f"   Total Deals: {state['total_deals']}")
        print(f"   Total Emails: {state['total_emails']}")
        print(f"\n🏢 Partners: {', '.join(state['active_partners'][:10])}")
        print(f"\n📜 Recent Events:")
        for evt in state['key_events'][-3:]:
            print(f"   {evt['date']}: {evt['description']}")
        
        return state
    
    def simulate_scenario(self, scenario: str) -> dict:
        """Run what-if simulation"""
        print(f"\n{'='*60}")
        print("PHASE 4: SIMULATION MODE")
        print(f"{'='*60}")
        
        self.time_machine.start_simulation()
        
        if scenario == 'new_partner':
            self.time_machine.simulate_add_partner("NewHydrogen", "2026-03-01", impact=4)
            self.time_machine.simulate_deal("NewHydrogen", "2026-04-15", "$200K", impact=5)
        elif scenario == 'big_deal':
            self.time_machine.simulate_deal("Luxfer", "2026-03-01", "$500K", impact=5)
            self.time_machine.simulate_deal("Hyundai", "2026-03-15", "$300K", impact=4)
        
        impact = self.time_machine.get_simulation_impact()
        future = self.time_machine.get_state_at_date("2026-06-01")
        
        print(f"\n🔮 Scenario: {scenario}")
        print(f"   New Partners: {len(impact['new_partners'])}")
        print(f"   New Deals: {impact['total_deals_added']}")
        print(f"   Improved Relationships: {len(impact['improved_relationships'])}")
        print(f"\n📊 Projected June 2026:")
        print(f"   Network Size: {future['network_size']}")
        
        self.time_machine.rollback_simulation()
        
        return impact
    
    # ========== PHASE 5: VOICE & SLACK ==========
    
    def voice_command(self, text: str) -> dict:
        """Process voice command"""
        print(f"\n{'='*60}")
        print("PHASE 5: VOICE COMMAND")
        print(f"{'='*60}")
        
        result = self.voice.process_command(text)
        
        print(f"\n🎤 \"{text}\"")
        print(f"   → Command: {result['command']}")
        print(f"   → Action: {result['action']}")
        print(f"   → JARVIS: \"{result['response']}\"")
        
        return result
    
    def slack_command(self, text: str) -> dict:
        """Process Slack command"""
        print(f"\n{'='*60}")
        print("PHASE 5: SLACK COMMAND")
        print(f"{'='*60}")
        
        result = self.slack.process_slack_command(text)
        
        print(f"\n💬 /jarvis {text}")
        print(f"   → {result['text'][:500]}...")
        
        return result
    
    # ========== PHASE 6: AUTONOMOUS AGENT ==========
    
    def start_autonomous_mode(self):
        """Start the autonomous agent"""
        print(f"\n{'='*60}")
        print("PHASE 6: AUTONOMOUS AGENT")
        print(f"{'='*60}")
        
        self.agent.start()
        
        # Set up callbacks
        self.agent.on_decision_needed = lambda p: print(f"\n🤔 DECISION NEEDED: {p.recommendation[:50]}...")
        self.agent.on_task_complete = lambda t: print(f"✓ Completed: {t.title}")
        
        print("\n🤖 Autonomous agent is running...")
        print("   (Press Ctrl+C to stop)")
        
        # Create sample tasks
        self.agent.simulate_incoming_email("yulia@holy-cryo.com", "Follow up on NIE", "normal")
        self.agent.propose_decision(
            context="Sample decision",
            recommendation="Test autonomous decision making",
            confidence=0.8
        )
        
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping agent...")
            self.agent.stop()
    
    def get_agent_status(self) -> dict:
        """Get autonomous agent status"""
        return self.agent.get_metrics()
    
    # ========== FULL WORKFLOW ==========
    
    def full_workflow_demo(self):
        """Demonstrate all phases working together"""
        print("\n" + "="*70)
        print("DIGITAL CHRIS v1.0 - FULL WORKFLOW DEMO")
        print("="*70)
        
        # 1. Email comes in
        print("\n[1] NEW EMAIL ARRIVES")
        email_result = self.process_email(
            "tony@luxfer.com",
            "URGENT: Valve discontinuation timeline",
            "We need to discuss alternative valve solutions ASAP. The current stock will run out by March."
        )
        
        # 2. AI analyzes sentiment (negative + urgent)
        if email_result['sentiment']['urgent']:
            print("\n[2] AI DETECTS URGENCY → CREATES TASK")
            
            # 3. Create autonomous task
            task_id = self.agent.create_task(
                title="Handle Luxfer valve emergency",
                task_type='decision_proposal',
                priority=TaskPriority.CRITICAL,
                params={
                    'context': 'Luxfer valve discontinuation - stock running out by March',
                    'recommendation': 'Schedule emergency video call with Luxfer + notify Hyundai',
                    'risk_level': 'high'
                },
                confidence=0.92
            )
            
            print(f"   Created task: {task_id}")
        
        # 4. Check historical context
        print("\n[3] CHECKING HISTORICAL CONTEXT")
        trends = self.time_machine.get_relationship_trends('Luxfer')
        print(f"   Luxfer relationship trend:")
        for t in trends[-3:]:
            print(f"      {t['date']}: {t['score']}/10")
        
        # 5. Generate voice summary
        print("\n[4] VOICE SUMMARY")
        voice_result = self.voice_command("Jarvis, status of Luxfer")
        
        # 6. Show current status
        print("\n[5] AGENT STATUS")
        status = self.get_agent_status()
        print(f"   Tasks completed: {status['tasks_completed_today']}")
        print(f"   Pending decisions: {status['pending_decisions']}")
        print(f"   Autonomy level: {status['autonomy_level']*100:.0f}%")
        
        print("\n" + "="*70)
        print("WORKFLOW COMPLETE")
        print("="*70)


def main():
    parser = argparse.ArgumentParser(description='Digital Chris v1.0 Master Controller')
    parser.add_argument('--mode', choices=['ai', 'time', 'voice', 'agent', 'all'], 
                       default='all', help='Which phase to run')
    parser.add_argument('--process-email', action='store_true', help='Process an email')
    parser.add_argument('--from', dest='sender', help='Email sender')
    parser.add_argument('--subject', help='Email subject')
    parser.add_argument('--body', help='Email body')
    parser.add_argument('--voice', help='Voice command text')
    parser.add_argument('--slack', help='Slack command text')
    parser.add_argument('--time-travel', type=int, help='Year to travel to')
    parser.add_argument('--simulate', help='Simulation scenario')
    parser.add_argument('--partner', help='Partner name for health check')
    
    args = parser.parse_args()
    
    # Initialize master controller
    master = DigitalChrisMaster()
    
    # Process specific commands
    if args.process_email and args.sender and args.subject:
        master.process_email(args.sender, args.subject, args.body or "")
        return
    
    if args.voice:
        master.voice_command(args.voice)
        return
    
    if args.slack:
        master.slack_command(args.slack)
        return
    
    if args.time_travel:
        master.time_travel(args.time_travel)
        return
    
    if args.simulate:
        master.simulate_scenario(args.simulate)
        return
    
    if args.partner:
        health = master.get_partner_health(args.partner)
        print(f"\nPartner Health: {args.partner}")
        print(json.dumps(health, indent=2))
        return
    
    # Run based on mode
    if args.mode == 'all':
        master.full_workflow_demo()
    elif args.mode == 'ai':
        master.process_email("test@example.com", "Test subject", "Test body content")
    elif args.mode == 'time':
        master.time_travel(2024)
        master.simulate_scenario('new_partner')
    elif args.mode == 'voice':
        master.voice_command("Jarvis, show me Luxfer")
        master.slack_command("status Hyundai")
    elif args.mode == 'agent':
        master.start_autonomous_mode()


if __name__ == '__main__':
    main()
