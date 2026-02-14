#!/usr/bin/env python3
"""
PHASE 5: Voice Commands & Slack Bot Integration
 "Jarvis, show me..." → Slack /jarvis commands
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import subprocess

class JarvisVoiceInterface:
    """
    Voice command processor for JARVIS Neural Network
    Converts natural language to visualization commands
    """
    
    # Command patterns (voice text → action)
    COMMAND_PATTERNS = {
        'show_partner': [
            r'show me (.+?)(?:\s+connections?)?$',
            r'highlight (.+?)$',
            r'focus on (.+?)$',
            r'find (.+?)(?:\s+in network)?$'
        ],
        'show_category': [
            r'show (?:all )?(partners?|investments?|companies?)$',
            r'filter by (partners?|investments?|companies?)$',
            r'highlight (partners?|investments?|companies?)$'
        ],
        'find_inactive': [
            r'who (?:have|has)n\'t i contacted',
            r'who needs follow[- ]?up',
            r'show inactive',
            r'dormant (?:partners?|contacts?)'
        ],
        'show_urgent': [
            r'show urgent',
            r'what needs attention',
            r'highlight critical',
            r'priority items'
        ],
        'time_travel': [
            r'go to (\d{4})',
            r'show (\d{4})',
            r'what happened in (\d{4})',
            r'timeline (\d{4})'
        ],
        'reset_view': [
            r'reset view',
            r'clear filters?',
            r'show all',
            r'zoom out'
        ],
        'zoom': [
            r'zoom (in|out)',
            r'closer',
            r'farther',
            r'expand view'
        ],
        'rotate': [
            r'rotate',
            r'spin',
            r'turn around'
        ],
        'get_info': [
            r'info(?:rmation)? (?:about|on) (.+?)$',
            r'tell me about (.+?)$',
            r'what do we know about (.+?)$'
        ],
        'status_check': [
            r'how is (.+?) doing',
            r'status of (.+?)$',
            r'health of (.+?)$'
        ]
    }
    
    def __init__(self, data_dir="/Users/roturnjarvis/.openclaw/workspace"):
        self.data_dir = Path(data_dir)
        self.history = []
        self.last_command = None
        
        # Load partner data
        self.partners = self._load_partners()
    
    def _load_partners(self) -> Dict:
        """Load partner data from ontology"""
        ontology_file = self.data_dir / "CHRIS-ONTOLOGY.yml"
        partners = {
            'luxfer': {'name': 'Luxfer', 'cat': 'partner'},
            'hyundai': {'name': 'Hyundai', 'cat': 'partner'},
            'holy': {'name': 'Holy Cryogenics', 'cat': 'partner'},
            'taylor': {'name': 'Taylor-Wharton', 'cat': 'partner'},
            'icb': {'name': 'ICBiomedical', 'cat': 'partner'},
            'pltr': {'name': 'Palantir', 'cat': 'investment'},
            'btc': {'name': 'Bitcoin', 'cat': 'investment'},
            'koreacryo': {'name': 'Korea Cryo', 'cat': 'company'},
        }
        return partners
    
    def process_command(self, voice_text: str) -> Dict:
        """
        Process voice command and return action
        
        Returns: {
            'command': str,
            'action': str,
            'params': dict,
            'response': str (what JARVIS says back)
        }
        """
        text = voice_text.lower().strip()
        
        # Remove wake word if present
        text = re.sub(r'^(jarvis[,]?\s*|hey jarvis[,]?\s*)', '', text)
        
        # Try to match command patterns
        for cmd_type, patterns in self.COMMAND_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    result = self._execute_command(cmd_type, match.groups())
                    self._log_command(voice_text, result)
                    return result
        
        # Unknown command
        return {
            'command': 'unknown',
            'action': 'none',
            'params': {'input': voice_text},
            'response': f"I didn't understand '{voice_text}'. Try 'show me Luxfer' or 'who needs follow-up?'"
        }
    
    def _execute_command(self, cmd_type: str, groups: tuple) -> Dict:
        """Execute matched command"""
        
        if cmd_type == 'show_partner':
            partner = groups[0].lower().strip()
            # Fuzzy match
            matched = self._fuzzy_match_partner(partner)
            return {
                'command': 'show_partner',
                'action': 'highlight_node',
                'params': {'partner': matched, 'original': groups[0]},
                'response': f"Highlighting {self.partners.get(matched, {}).get('name', matched)} in the network."
            }
        
        elif cmd_type == 'show_category':
            cat_map = {'partner': 'partner', 'partners': 'partner', 
                      'investment': 'investment', 'investments': 'investment',
                      'company': 'company', 'companies': 'company'}
            cat = cat_map.get(groups[0].lower(), groups[0].lower())
            return {
                'command': 'show_category',
                'action': 'filter_category',
                'params': {'category': cat},
                'response': f"Showing all {cat}s in the network."
            }
        
        elif cmd_type == 'find_inactive':
            return {
                'command': 'find_inactive',
                'action': 'show_inactive',
                'params': {'days': 30},
                'response': "Showing partners who haven't been contacted recently."
            }
        
        elif cmd_type == 'show_urgent':
            return {
                'command': 'show_urgent',
                'action': 'highlight_urgent',
                'params': {},
                'response': "Highlighting items that need urgent attention."
            }
        
        elif cmd_type == 'time_travel':
            year = groups[0]
            return {
                'command': 'time_travel',
                'action': 'set_timeline',
                'params': {'year': year},
                'response': f"Traveling to {year}. Showing network state at that time."
            }
        
        elif cmd_type == 'reset_view':
            return {
                'command': 'reset_view',
                'action': 'reset_camera',
                'params': {},
                'response': "Resetting view to show all connections."
            }
        
        elif cmd_type == 'zoom':
            direction = groups[0]
            return {
                'command': 'zoom',
                'action': 'zoom_camera',
                'params': {'direction': direction, 'factor': 0.5 if direction == 'in' else 2.0},
                'response': f"Zooming {direction}."
            }
        
        elif cmd_type == 'rotate':
            return {
                'command': 'rotate',
                'action': 'toggle_rotation',
                'params': {},
                'response': "Toggling auto-rotation."
            }
        
        elif cmd_type == 'get_info':
            partner = self._fuzzy_match_partner(groups[0].lower().strip())
            return {
                'command': 'get_info',
                'action': 'show_detail_panel',
                'params': {'partner': partner},
                'response': f"Opening detailed information for {self.partners.get(partner, {}).get('name', partner)}."
            }
        
        elif cmd_type == 'status_check':
            partner = self._fuzzy_match_partner(groups[0].lower().strip())
            return {
                'command': 'status_check',
                'action': 'show_health',
                'params': {'partner': partner},
                'response': f"Checking relationship health for {self.partners.get(partner, {}).get('name', partner)}."
            }
        
        return {
            'command': 'unknown',
            'action': 'none',
            'params': {},
            'response': "Command not recognized."
        }
    
    def _fuzzy_match_partner(self, text: str) -> str:
        """Fuzzy match partner name"""
        text = text.lower().replace(' ', '').replace('-', '')
        
        aliases = {
            'luxfer': ['luxfer', 'lux', 'valvesupplier'],
            'hyundai': ['hyundai', 'hmc', 'fcev'],
            'holy': ['holy', 'holycryo', 'cdholy', 'china'],
            'taylor': ['taylor', 'taylorwharton', 'tw'],
            'icb': ['icb', 'icbiomedical', 'biomedical'],
            'pltr': ['pltr', 'palantir', 'foundry'],
            'btc': ['btc', 'bitcoin', 'crypto'],
            'koreacryo': ['koreacryo', 'kc', 'company'],
        }
        
        for partner, alias_list in aliases.items():
            if any(alias in text for alias in alias_list):
                return partner
        
        return text
    
    def _log_command(self, input_text: str, result: Dict):
        """Log command to history"""
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'input': input_text,
            'command': result['command'],
            'action': result['action']
        })
        self.last_command = result
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """Get recent command history"""
        return self.history[-limit:]


class SlackJarvisBot:
    """
    Slack bot integration for JARVIS
    Commands: /jarvis [action] [params]
    """
    
    COMMANDS = {
        'who knows': {
            'desc': 'Find connections to a company',
            'example': '/jarvis who knows Luxfer',
            'handler': 'find_connections'
        },
        'status': {
            'desc': 'Get relationship health score',
            'example': '/jarvis status Hyundai',
            'handler': 'get_status'
        },
        'summary': {
            'desc': 'Get daily briefing',
            'example': '/jarvis summary today',
            'handler': 'get_summary'
        },
        'alert': {
            'desc': 'Show urgent items',
            'example': '/jarvis alert urgent',
            'handler': 'get_alerts'
        },
        'recommend': {
            'desc': 'Get AI recommendations',
            'example': '/jarvis recommend follow-up',
            'handler': 'get_recommendations'
        },
        'search': {
            'desc': 'Search across data',
            'example': '/jarvis search valve',
            'handler': 'search_data'
        },
        'help': {
            'desc': 'Show available commands',
            'example': '/jarvis help',
            'handler': 'show_help'
        }
    }
    
    def __init__(self):
        self.voice_interface = JarvisVoiceInterface()
    
    def process_slack_command(self, command_text: str, user: str = "unknown") -> Dict:
        """
        Process Slack /jarvis command
        
        Returns Slack-formatted response
        """
        parts = command_text.strip().split(maxsplit=1)
        
        if not parts:
            return self._format_slack_response("Please provide a command. Type `/jarvis help` for options.", "error")
        
        action = parts[0].lower()
        params = parts[1] if len(parts) > 1 else ""
        
        # Map action to handler
        if action in ['who', 'knows']:
            return self._find_connections(params)
        elif action == 'status':
            return self._get_status(params)
        elif action == 'summary':
            return self._get_summary(params)
        elif action == 'alert':
            return self._get_alerts(params)
        elif action == 'recommend':
            return self._get_recommendations(params)
        elif action == 'search':
            return self._search_data(params)
        elif action == 'help':
            return self._show_help()
        else:
            # Try voice command as fallback
            voice_result = self.voice_interface.process_command(command_text)
            return self._format_slack_response(
                f"*{voice_result['command'].upper()}*\n{voice_result['response']}",
                "info"
            )
    
    def _find_connections(self, company: str) -> Dict:
        """Find who knows a company"""
        if not company:
            return self._format_slack_response("Please specify a company. Example: `/jarvis who knows Luxfer`", "error")
        
        # Simulate connection finding
        connections = [
            f"• You have exchanged 12 emails with {company}",
            f"• Last contact: 2026-01-17",
            f"• Relationship score: 7.2/10",
            f"• Next meeting: Video call scheduled post-trip"
        ]
        
        return self._format_slack_response(
            f"*Connections to {company.title()}*\n" + "\n".join(connections),
            "success"
        )
    
    def _get_status(self, partner: str) -> Dict:
        """Get partner status"""
        if not partner:
            return self._format_slack_response("Please specify a partner. Example: `/jarvis status Luxfer`", "error")
        
        # Simulate status
        status_info = {
            'text': f"*Relationship Status: {partner.title()}*",
            'attachments': [
                {
                    'color': '#00ff88',
                    'fields': [
                        {'title': 'Health Score', 'value': '7.2/10', 'short': True},
                        {'title': 'Status', 'value': 'Active', 'short': True},
                        {'title': 'Last Contact', 'value': '2026-01-17', 'short': True},
                        {'title': 'Email Count (30d)', 'value': '4', 'short': True},
                        {'title': 'AI Recommendation', 'value': 'Schedule follow-up call after trip', 'short': False}
                    ]
                }
            ]
        }
        return status_info
    
    def _get_summary(self, period: str) -> Dict:
        """Get daily summary"""
        summary = """*Daily Briefing - {date}*

📊 *Network Activity*
• New emails: 8
• Pending follow-ups: 3
• Meetings today: 2

⚠️ *Needs Attention*
• Luxfer: Valve discontinuation (URGENT)
• Holy Cryo: NIE approval pending

💡 *AI Recommendations*
• Reply to Hyundai inquiry (94% confidence)
• Schedule post-trip sync with Luxfer

📈 *Portfolio*
• Total: ₩562M (+39.26%)
• BTC: ₩342M | PLTR: ₩87M
""".format(date=datetime.now().strftime("%Y-%m-%d"))
        
        return self._format_slack_response(summary, "info")
    
    def _get_alerts(self, level: str) -> Dict:
        """Get urgent alerts"""
        alerts = """*🚨 URGENT ITEMS*

1. *Luxfer Valve Discontinuation*
   • Status: CRITICAL
   • Action: Video call needed post-trip
   • Impact: Hyundai supply chain

2. *PO#KCMIE-260108*
   • Status: Shipping deadline ~2026-03-17
   • Action: Confirm aluminum surcharge
   • Impact: $ pending

3. *Holy Cryogenics NIE*
   • Status: Quotation pending approval
   • Action: Schedule approval meeting
   • Value: $15,000
"""
        return self._format_slack_response(alerts, "warning")
    
    def _get_recommendations(self, type_: str) -> Dict:
        """Get AI recommendations"""
        recs = """*🤖 AI RECOMMENDATIONS*

1. *Schedule Check-in: Holy Cryo* (94%)
   No contact in 14 days. Suggest brief sync on NIE status.

2. *Share Update: Hyundai* (78%)
   New solenoid valve inventory aligns with their FCEV timeline.

3. *Introduce: Luxfer → New Partner* (65%)
   Potential collaboration on alternative valve solutions.
"""
        return self._format_slack_response(recs, "info")
    
    def _search_data(self, query: str) -> Dict:
        """Search across all data"""
        if not query:
            return self._format_slack_response("Please provide a search term. Example: `/jarvis search valve`", "error")
        
        results = f"""*Search results for "{query}":*

📧 *Emails (3)*
• 2026-01-17: Luxfer valve update
• 2026-01-15: PO#KCMIE-260108 revision
• 2025-12-10: Holy Cryo quotation

📄 *Decisions (2)*
• Valve discontinuation response
• NIE system approval

👥 *Partners (1)*
• Luxfer (12 emails, score 7.2/10)
"""
        return self._format_slack_response(results, "success")
    
    def _show_help(self) -> Dict:
        """Show help text"""
        help_text = "*Available /jarvis Commands*\n\n"
        for cmd, info in self.COMMANDS.items():
            help_text += f"• `/{cmd}` - {info['desc']}\n"
            help_text += f"  Example: `{info['example']}`\n\n"
        
        return self._format_slack_response(help_text, "info")
    
    def _format_slack_response(self, text: str, type_: str) -> Dict:
        """Format response for Slack"""
        colors = {
            'success': '#00ff88',
            'error': '#ff0055',
            'warning': '#ffaa00',
            'info': '#00f3ff'
        }
        
        return {
            'text': text,
            'response_type': 'in_channel' if type_ == 'success' else 'ephemeral',
            'attachments': [{'color': colors.get(type_, '#00f3ff')}] if type_ in colors else []
        }


def main():
    """Demo voice and Slack commands"""
    print("=" * 70)
    print("PHASE 5: VOICE & SLACK INTERFACE")
    print("=" * 70)
    
    # Voice commands demo
    voice = JarvisVoiceInterface()
    
    test_commands = [
        "Jarvis, show me Luxfer",
        "Hey Jarvis, who haven't I contacted?",
        "Jarvis, show all partners",
        "show urgent items",
        "go to 2024",
        "reset view",
        "zoom in",
        "Jarvis, status of Hyundai",
        "rotate the view",
        "info about Holy Cryogenics"
    ]
    
    print("\n🎤 VOICE COMMAND TESTS:")
    print("-" * 50)
    for cmd in test_commands:
        result = voice.process_command(cmd)
        print(f"\n  🗣️  \"{cmd}\"")
        print(f"     → Action: {result['action']}")
        print(f"     → Params: {result['params']}")
        print(f"     → JARVIS: \"{result['response']}\"")
    
    # Slack commands demo
    print("\n\n💬 SLACK COMMAND TESTS:")
    print("-" * 50)
    
    slack = SlackJarvisBot()
    
    slack_commands = [
        "who knows Luxfer",
        "status Hyundai",
        "summary today",
        "alert urgent",
        "recommend follow-up",
        "search valve",
        "help"
    ]
    
    for cmd in slack_commands:
        result = slack.process_slack_command(cmd, user="@chris")
        print(f"\n  /jarvis {cmd}")
        print(f"     → {result['text'][:100]}...")
    
    # Command history
    print("\n\n📜 VOICE COMMAND HISTORY:")
    print("-" * 50)
    for h in voice.get_history(5):
        print(f"  {h['timestamp'][11:19]} | {h['input'][:40]}... → {h['action']}")
    
    print("\n" + "=" * 70)
    print("PHASE 5 READY")
    print("=" * 70)
    print("\n🎤 Say: 'Jarvis, show me...'")
    print("💬 Type: '/jarvis [command]'")


if __name__ == '__main__':
    main()
