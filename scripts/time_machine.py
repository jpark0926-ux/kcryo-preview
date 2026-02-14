#!/usr/bin/env python3
"""
PHASE 4: Time Machine - Historical Analysis & Simulation
 2020-2026 timeline + what-if scenarios
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import random

@dataclass
class TimelineEvent:
    date: str
    type: str  # 'partner_added', 'email', 'meeting', 'deal', 'project'
    partner: str
    description: str
    impact: int  # -5 to +5, relationship impact
    metadata: Dict

@dataclass
class PartnerState:
    name: str
    first_contact: str
    email_count: int = 0
    meeting_count: int = 0
    deal_count: int = 0
    relationship_score: float = 5.0  # 0-10
    status: str = 'active'  # active, dormant, critical, lost

class TimeMachine:
    def __init__(self, data_dir="/Users/roturnjarvis/.openclaw/workspace"):
        self.data_dir = Path(data_dir)
        self.timeline_file = self.data_dir / "logs/timeline_events.json"
        
        # Historical reconstruction (2020-2026)
        self.events = self._build_timeline()
        self.partners = self._reconstruct_partner_states()
        
        # Simulation state
        self.simulation_mode = False
        self.simulated_events = []
        self.backup_events = []
    
    def _build_timeline(self) -> List[TimelineEvent]:
        """Build historical timeline from 2020-2026"""
        events = []
        
        # Based on actual email corpus analysis
        timeline_data = [
            # 2020 - Foundation year
            ("2020-09-26", "partner_added", "Taylor-Wharton", "Initial contact established", 3, {}),
            ("2020-10-15", "meeting", "Taylor-Wharton", "First partnership discussion", 2, {}),
            
            # 2021 - Expansion
            ("2021-03-12", "partner_added", "Luxfer", "Hydrogen valve inquiry", 4, {}),
            ("2021-06-20", "deal", "Taylor-Wharton", "First PO confirmed", 5, {"value": "$50K"}),
            ("2021-09-15", "partner_added", "Hyundai", "FCEV project introduction", 4, {}),
            
            # 2022 - Growth
            ("2022-01-10", "deal", "Luxfer", "Valve supply agreement", 5, {"value": "$120K"}),
            ("2022-04-22", "meeting", "Hyundai", "Technical review meeting", 3, {}),
            ("2022-08-30", "partner_added", "ICBiomedical", "Dewar supplier contact", 3, {}),
            
            # 2023 - Scale
            ("2023-02-14", "deal", "Hyundai", "Pilot order confirmed", 4, {"value": "$80K"}),
            ("2023-06-18", "project", "KoreaCryo", "KGSC audit completed", 3, {}),
            ("2023-11-05", "deal", "Taylor-Wharton", "Annual contract renewal", 4, {}),
            
            # 2024 - Diversification
            ("2024-01-20", "investment", "PLTR", "Position opened", 0, {"shares": 500}),
            ("2024-03-15", "partner_added", "Holy Cryogenics", "China market entry", 3, {}),
            ("2024-07-08", "meeting", "Holy Cryogenics", "Factory visit", 4, {}),
            ("2024-10-12", "investment", "BTC", "Strategic position", 0, {"btc": 0.5}),
            
            # 2025 - Peak activity
            ("2025-01-15", "deal", "Holy Cryogenics", "$15K quotation", 3, {}),
            ("2025-03-20", "project", "Digital Chris", "AI clone project started", 5, {}),
            ("2025-06-30", "milestone", "KoreaCryo", "Record quarter", 5, {}),
            ("2025-09-10", "email", "Luxfer", "Valve discontinuation notice", -4, {"urgent": True}),
            ("2025-11-22", "email", "Hyundai", "Solenoid valve inquiry", 3, {}),
            ("2025-12-15", "meeting", "Holy Cryogenics", "Chengdu factory visit", 4, {}),
            
            # 2026 - Current
            ("2026-01-05", "PO", "Thunderbird", "PO#KCMIE-260108 confirmed", 4, {}),
            ("2026-01-17", "email", "Luxfer", "Video call scheduled post-trip", 2, {}),
            ("2026-02-01", "milestone", "Digital Chris", "1803 emails analyzed", 5, {}),
            ("2026-02-15", "trip", "Myanmar", "Field trip preparation", 0, {"location": "Mae Sot"}),
        ]
        
        for date, type_, partner, desc, impact, meta in timeline_data:
            events.append(TimelineEvent(
                date=date,
                type=type_,
                partner=partner,
                description=desc,
                impact=impact,
                metadata=meta
            ))
        
        return sorted(events, key=lambda x: x.date)
    
    def _reconstruct_partner_states(self) -> Dict[str, PartnerState]:
        """Reconstruct partner states from timeline"""
        partners = {}
        
        for event in self.events:
            if event.partner not in partners:
                partners[event.partner] = PartnerState(
                    name=event.partner,
                    first_contact=event.date
                )
            
            p = partners[event.partner]
            
            if event.type == 'email':
                p.email_count += 1
            elif event.type == 'meeting':
                p.meeting_count += 1
            elif event.type in ['deal', 'PO']:
                p.deal_count += 1
            
            # Update relationship score
            p.relationship_score = max(0, min(10, p.relationship_score + event.impact * 0.3))
            
            # Determine status
            days_since = (datetime.now() - datetime.strptime(event.date, "%Y-%m-%d")).days
            if days_since > 180:
                p.status = 'dormant'
            if p.relationship_score < 3:
                p.status = 'critical'
            if p.relationship_score > 7:
                p.status = 'strong'
        
        return partners
    
    def get_state_at_date(self, date_str: str) -> Dict:
        """
        Get complete system state at a specific date
        Returns network structure, partner states, key metrics
        """
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        # Filter events up to target date
        active_events = [e for e in self.events if datetime.strptime(e.date, "%Y-%m-%d") <= target_date]
        
        # Rebuild state
        state = {
            'date': date_str,
            'active_partners': set(),
            'total_deals': 0,
            'total_emails': 0,
            'network_size': 0,
            'key_events': []
        }
        
        partner_scores = defaultdict(lambda: {'score': 5.0, 'emails': 0, 'deals': 0})
        
        for event in active_events:
            state['active_partners'].add(event.partner)
            
            if event.type == 'email':
                state['total_emails'] += 1
                partner_scores[event.partner]['emails'] += 1
            elif event.type in ['deal', 'PO']:
                state['total_deals'] += 1
                partner_scores[event.partner]['deals'] += 1
            
            partner_scores[event.partner]['score'] = max(0, min(10, 
                partner_scores[event.partner]['score'] + event.impact * 0.3))
        
        state['active_partners'] = list(state['active_partners'])
        state['network_size'] = len(state['active_partners'])
        state['key_events'] = [asdict(e) for e in active_events[-5:]]  # Last 5 events
        state['partner_scores'] = dict(partner_scores)
        
        return state
    
    def get_timeline_range(self) -> tuple:
        """Get min and max dates in timeline"""
        dates = [datetime.strptime(e.date, "%Y-%m-%d") for e in self.events]
        return (min(dates).strftime("%Y-%m-%d"), max(dates).strftime("%Y-%m-%d"))
    
    def get_events_between(self, start: str, end: str) -> List[TimelineEvent]:
        """Get events between two dates"""
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")
        
        return [e for e in self.events 
                if start_dt <= datetime.strptime(e.date, "%Y-%m-%d") <= end_dt]
    
    # ========== SIMULATION MODE ==========
    
    def start_simulation(self):
        """Enter simulation mode - changes don't affect real timeline"""
        self.simulation_mode = True
        self.backup_events = self.events.copy()
        self.simulated_events = []
        print("[TIMEMACHINE] Simulation mode ACTIVATED")
        print("[TIMEMACHINE] Changes are temporary until commit()")
    
    def add_simulated_event(self, date: str, type_: str, partner: str, 
                           description: str, impact: int = 0, metadata: Dict = None):
        """Add a hypothetical event in simulation mode"""
        if not self.simulation_mode:
            raise RuntimeError("Must call start_simulation() first")
        
        event = TimelineEvent(
            date=date,
            type=type_,
            partner=partner,
            description=f"[SIM] {description}",
            impact=impact,
            metadata=metadata or {}
        )
        
        self.simulated_events.append(event)
        self.events = sorted(self.backup_events + self.simulated_events, 
                            key=lambda x: x.date)
        
        # Rebuild partner states
        self.partners = self._reconstruct_partner_states()
        
        return event
    
    def simulate_add_partner(self, partner_name: str, date: str, impact: int = 3):
        """Quick helper to simulate adding a new partner"""
        return self.add_simulated_event(
            date=date,
            type_='partner_added',
            partner=partner_name,
            description=f"New partner {partner_name} added",
            impact=impact
        )
    
    def simulate_deal(self, partner: str, date: str, value: str, impact: int = 5):
        """Quick helper to simulate closing a deal"""
        return self.add_simulated_event(
            date=date,
            type_='deal',
            partner=partner,
            description=f"Deal closed: {value}",
            impact=impact,
            metadata={"value": value}
        )
    
    def get_simulation_impact(self) -> Dict:
        """Get impact analysis of simulated changes"""
        if not self.simulation_mode:
            return {}
        
        current_state = self._reconstruct_partner_states()
        
        # Temporarily restore backup to compare
        self.events = self.backup_events
        original_state = self._reconstruct_partner_states()
        self.events = self.backup_events + self.simulated_events
        
        impact = {
            'new_partners': [],
            'improved_relationships': [],
            'declined_relationships': [],
            'total_deals_added': 0
        }
        
        for name, state in current_state.items():
            if name not in original_state:
                impact['new_partners'].append(name)
            else:
                orig = original_state[name]
                if state.relationship_score > orig.relationship_score:
                    impact['improved_relationships'].append({
                        'partner': name,
                        'change': round(state.relationship_score - orig.relationship_score, 1)
                    })
                elif state.relationship_score < orig.relationship_score:
                    impact['declined_relationships'].append({
                        'partner': name,
                        'change': round(state.relationship_score - orig.relationship_score, 1)
                    })
        
        impact['total_deals_added'] = len([e for e in self.simulated_events if e.type in ['deal', 'PO']])
        
        return impact
    
    def commit_simulation(self):
        """Commit simulation changes to permanent timeline"""
        if not self.simulation_mode:
            return
        
        self.backup_events = self.events.copy()
        self.simulated_events = []
        self.simulation_mode = False
        print("[TIMEMACHINE] Simulation COMMITTED to timeline")
    
    def rollback_simulation(self):
        """Discard simulation changes"""
        if not self.simulation_mode:
            return
        
        self.events = self.backup_events
        self.simulated_events = []
        self.simulation_mode = False
        self.partners = self._reconstruct_partner_states()
        print("[TIMEMACHINE] Simulation ROLLED BACK")
    
    # ========== ANALYSIS FEATURES ==========
    
    def get_relationship_trends(self, partner: str) -> List[Dict]:
        """Get relationship score trend over time for a partner"""
        partner_events = [e for e in self.events if e.partner == partner]
        
        trends = []
        score = 5.0
        
        for event in sorted(partner_events, key=lambda x: x.date):
            score = max(0, min(10, score + event.impact * 0.3))
            trends.append({
                'date': event.date,
                'score': round(score, 2),
                'event': event.description
            })
        
        return trends
    
    def find_critical_moments(self) -> List[Dict]:
        """Find moments with high impact (both positive and negative)"""
        critical = []
        
        for event in self.events:
            if abs(event.impact) >= 4:
                critical.append({
                    'date': event.date,
                    'partner': event.partner,
                    'impact': event.impact,
                    'description': event.description,
                    'type': 'positive' if event.impact > 0 else 'negative'
                })
        
        return sorted(critical, key=lambda x: abs(x['impact']), reverse=True)
    
    def generate_future_projection(self, months: int = 6) -> List[Dict]:
        """Generate projected future events based on patterns"""
        projections = []
        
        # Get active partners
        recent_cutoff = datetime.now() - timedelta(days=90)
        recent_partners = set()
        
        for event in reversed(self.events):
            event_date = datetime.strptime(event.date, "%Y-%m-%d")
            if event_date >= recent_cutoff:
                recent_partners.add(event.partner)
        
        # Project follow-ups needed
        for partner in recent_partners:
            p_state = self.partners.get(partner)
            if p_state and p_state.status in ['dormant', 'at_risk']:
                projections.append({
                    'projected_date': (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                    'type': 'action_required',
                    'partner': partner,
                    'description': f"Follow-up needed with {partner} (status: {p_state.status})",
                    'confidence': 0.8
                })
        
        return projections


def main():
    """Demo the Time Machine"""
    tm = TimeMachine()
    
    print("=" * 70)
    print("TIME MACHINE v1.0 - Historical Analysis & Simulation")
    print("=" * 70)
    
    # Timeline range
    start, end = tm.get_timeline_range()
    print(f"\n📅 TIMELINE RANGE: {start} → {end}")
    print(f"   Total Events: {len(tm.events)}")
    print(f"   Active Partners: {len(tm.partners)}")
    
    # State at specific dates
    print("\n\n🔍 STATE AT KEY DATES:")
    for year in [2020, 2022, 2024, 2026]:
        state = tm.get_state_at_date(f"{year}-06-01")
        print(f"\n   {year}:")
        print(f"      Network Size: {state['network_size']} partners")
        print(f"      Total Deals: {state['total_deals']}")
        print(f"      Total Emails: {state['total_emails']}")
    
    # Partner trends
    print("\n\n📈 LUXFER RELATIONSHIP TREND:")
    trends = tm.get_relationship_trends('Luxfer')
    for t in trends[:5]:
        print(f"   {t['date']}: {t['score']}/10 - {t['event'][:40]}...")
    
    # Critical moments
    print("\n\n⚡ CRITICAL MOMENTS:")
    critical = tm.find_critical_moments()
    for c in critical[:5]:
        emoji = "✅" if c['type'] == 'positive' else "⚠️"
        print(f"   {emoji} {c['date']} | {c['partner']} | Impact: {c['impact']:+d}")
        print(f"      {c['description']}")
    
    # Simulation demo
    print("\n\n🔮 SIMULATION MODE:")
    tm.start_simulation()
    
    # Add hypothetical scenarios
    tm.simulate_add_partner("NewHydrogen", "2026-03-01", impact=4)
    tm.simulate_deal("NewHydrogen", "2026-04-15", "$200K", impact=5)
    tm.simulate_deal("Holy Cryogenics", "2026-03-20", "$50K", impact=3)
    
    impact = tm.get_simulation_impact()
    print(f"   New Partners: {impact['new_partners']}")
    print(f"   Deals Added: {impact['total_deals_added']}")
    print(f"   Improved Relationships: {len(impact['improved_relationships'])}")
    
    # Current state with simulation
    future_state = tm.get_state_at_date("2026-06-01")
    print(f"\n   Projected June 2026 Network Size: {future_state['network_size']}")
    
    tm.rollback_simulation()
    print("\n   [Simulation rolled back]")
    
    # Future projections
    print("\n\n🔮 FUTURE PROJECTIONS (Next 6 months):")
    projections = tm.generate_future_projection(6)
    for p in projections[:5]:
        print(f"   📌 {p['projected_date']}: {p['description']}")
    
    print("\n" + "=" * 70)
    print("TIME MACHINE READY")
    print("=" * 70)


if __name__ == '__main__':
    main()
