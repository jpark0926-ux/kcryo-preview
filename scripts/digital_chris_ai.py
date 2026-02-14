#!/usr/bin/env python3
"""
PHASE 3: AI Core - Digital Chris v0.2
 sentiment analysis + AI response generation + recommendation engine
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import random

class DigitalChrisAI:
    def __init__(self, data_dir="/Users/roturnjarvis/.openclaw/workspace"):
        self.data_dir = Path(data_dir)
        self.decisions_dir = self.data_dir / "memory/decisions"
        self.logs_dir = self.data_dir / "logs"
        
        # Sentiment keywords (Korean + English)
        self.sentiment_positive = [
            '감사', '좋습니다', 'great', 'excellent', 'confirmed', 'approved',
            'completed', 'successful', 'perfect', 'thanks', 'appreciate',
            'looking forward', 'positive', 'opportunity', 'interested'
        ]
        self.sentiment_negative = [
            '문제', 'urgent', 'issue', 'problem', 'delay', 'concerned',
            'disappointed', 'failed', 'cancelled', 'error', 'complaint',
            'discontinued', 'obsolete', 'shortage', 'critical', 'emergency'
        ]
        self.sentiment_urgent = [
            'ASAP', 'immediately', 'today', 'deadline', 'expired',
            'overdue', 'tomorrow', 'this week', 'urgent', 'critical'
        ]
        
        # Response templates by context
        self.response_templates = {
            'follow_up': [
                'Hi {name}, just following up on our previous discussion about {topic}. Any updates on your end?',
                '{name}, hope you\'re doing well. Wanted to check in regarding {topic}. Let me know if you need any clarification.',
                'Hi {name}, following up on {topic}. Please let me know the status when you have a moment.'
            ],
            'quotation': [
                'Hi {name}, thank you for your inquiry. I\'ve attached our quotation for {topic}. Please review and let me know if you have any questions.',
                '{name}, please find attached our pricing for {topic}. Lead time is approximately {lead_time} weeks. Looking forward to your feedback.'
            ],
            'urgent': [
                'Hi {name}, this requires urgent attention regarding {topic}. Can we schedule a brief call today or tomorrow?',
                '{name}, we need to address {topic} immediately. Please respond with your availability for an emergency discussion.'
            ],
            'meeting_request': [
                'Hi {name}, I\'d like to schedule a meeting to discuss {topic}. My availability this week: {availability}. What works for you?',
                '{name}, shall we have a video call to align on {topic}? I\'m flexible on timing this week.'
            ]
        }
        
        self.relationship_scores = {}
        self.load_data()
    
    def load_data(self):
        """Load existing partner data from decisions"""
        if not self.decisions_dir.exists():
            return
        
        for file in self.decisions_dir.glob("*.md"):
            content = file.read_text()
            # Extract partner name from filename or content
            partner = file.stem.replace('_', ' ').title()
            
            # Calculate relationship score based on file content
            score = self._calculate_relationship_score(content)
            self.relationship_scores[partner.lower()] = {
                'score': score,
                'last_contact': self._extract_date(content),
                'file': str(file)
            }
    
    def _calculate_relationship_score(self, content):
        """Calculate relationship health score 0-10"""
        score = 7.0  # baseline
        
        # Positive signals
        if any(w in content.lower() for w in self.sentiment_positive):
            score += 1.5
        if 'PO' in content or 'order' in content.lower():
            score += 1.0
        if 'confirmed' in content.lower():
            score += 0.5
        
        # Negative signals
        if any(w in content.lower() for w in self.sentiment_negative):
            score -= 2.0
        if 'delay' in content.lower():
            score -= 1.0
        if 'complaint' in content.lower() or 'issue' in content.lower():
            score -= 1.5
        
        # Recency penalty
        date = self._extract_date(content)
        if date:
            days_ago = (datetime.now() - date).days
            if days_ago > 30:
                score -= 1.0
            if days_ago > 60:
                score -= 2.0
        
        return max(0, min(10, score))
    
    def _extract_date(self, content):
        """Extract date from content"""
        # Look for YYYY-MM-DD patterns
        match = re.search(r'\d{4}-\d{2}-\d{2}', content)
        if match:
            try:
                return datetime.strptime(match.group(), '%Y-%m-%d')
            except:
                pass
        return None
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of email/text
        Returns: {
            'positive': float (0-1),
            'neutral': float (0-1), 
            'negative': float (0-1),
            'urgent': bool,
            'overall': 'positive'|'neutral'|'negative'
        }
        """
        text_lower = text.lower()
        
        pos_count = sum(1 for w in self.sentiment_positive if w in text_lower)
        neg_count = sum(1 for w in self.sentiment_negative if w in text_lower)
        urgent_count = sum(1 for w in self.sentiment_urgent if w in text_lower)
        
        total = pos_count + neg_count + 1  # +1 for neutral baseline
        
        positive = pos_count / total
        negative = neg_count / total
        neutral = 1 - positive - negative
        
        # Determine overall
        if negative > 0.3:
            overall = 'negative'
        elif positive > 0.3:
            overall = 'positive'
        else:
            overall = 'neutral'
        
        return {
            'positive': round(positive, 2),
            'neutral': round(neutral, 2),
            'negative': round(negative, 2),
            'urgent': urgent_count > 0 or negative > 0.5,
            'overall': overall
        }
    
    def generate_response(self, partner_name, context_type='follow_up', **kwargs):
        """
        Generate AI-suggested response
        
        Args:
            partner_name: Name of recipient
            context_type: 'follow_up', 'quotation', 'urgent', 'meeting_request'
            **kwargs: topic, lead_time, availability, etc.
        """
        templates = self.response_templates.get(context_type, self.response_templates['follow_up'])
        template = random.choice(templates)
        
        # Fill in template
        params = {
            'name': partner_name.split()[0] if ' ' in partner_name else partner_name,
            'topic': kwargs.get('topic', 'our ongoing project'),
            'lead_time': kwargs.get('lead_time', '4-6'),
            'availability': kwargs.get('availability', 'Tue-Thu afternoons')
        }
        
        try:
            response = template.format(**params)
        except:
            response = template.format(name=params['name'], topic=params['topic'])
        
        # Calculate confidence
        confidence = self._calculate_confidence(context_type, partner_name)
        
        return {
            'response': response,
            'confidence': confidence,
            'tone': self._determine_tone(context_type),
            'context_type': context_type
        }
    
    def _calculate_confidence(self, context_type, partner_name):
        """Calculate confidence score for AI response"""
        base = 0.75
        
        # Higher confidence for known partners
        partner_key = partner_name.lower().replace(' ', '_')
        if any(partner_key in k for k in self.relationship_scores.keys()):
            base += 0.10
        
        # Context-specific adjustments
        if context_type == 'follow_up':
            base += 0.05
        elif context_type == 'urgent':
            base -= 0.05  # Lower confidence for urgent - needs human review
        
        return min(0.95, base)
    
    def _determine_tone(self, context_type):
        """Determine tone of response"""
        tones = {
            'follow_up': 'Professional/Friendly',
            'quotation': 'Business/Formal',
            'urgent': 'Direct/Urgent',
            'meeting_request': 'Collaborative'
        }
        return tones.get(context_type, 'Professional')
    
    def get_recommendations(self, partner_name=None, limit=3):
        """
        Get AI recommendations for follow-ups
        
        Returns list of recommendations with scores
        """
        recommendations = []
        
        if partner_name:
            # Specific partner recommendations
            partner_data = self.relationship_scores.get(partner_name.lower(), {})
            if partner_data:
                score = partner_data['score']
                last_contact = partner_data.get('last_contact')
                
                if score < 5:
                    recommendations.append({
                        'type': 'attention_needed',
                        'title': 'Relationship Repair Required',
                        'description': f'Score is low ({score}/10). Suggest direct call.',
                        'score': 95,
                        'action': 'schedule_call'
                    })
                
                if last_contact and (datetime.now() - last_contact).days > 14:
                    recommendations.append({
                        'type': 'follow_up',
                        'title': 'Check-in Overdue',
                        'description': f'No contact for {(datetime.now() - last_contact).days} days',
                        'score': 85,
                        'action': 'send_email'
                    })
        else:
            # Global recommendations across all partners
            for name, data in self.relationship_scores.items():
                if data['score'] < 6:
                    recommendations.append({
                        'type': 'attention_needed',
                        'partner': name,
                        'title': f'{name.title()} Needs Attention',
                        'description': f'Relationship score: {data["score"]}/10',
                        'score': 90 + (6 - data['score']) * 2,
                        'action': 'review_and_contact'
                    })
                
                if data.get('last_contact'):
                    days = (datetime.now() - data['last_contact']).days
                    if days > 21:
                        recommendations.append({
                            'type': 'follow_up',
                            'partner': name,
                            'title': f'Reconnect with {name.title()}',
                            'description': f'Last contact: {days} days ago',
                            'score': 70 + min(20, days - 21),
                            'action': 'send_email'
                        })
        
        # Sort by score descending
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:limit]
    
    def get_partner_health(self, partner_name):
        """Get complete health report for a partner"""
        partner_key = partner_name.lower().replace(' ', '_')
        
        # Find matching partner
        data = None
        for k, v in self.relationship_scores.items():
            if partner_key in k or k in partner_key:
                data = v
                data['name'] = k
                break
        
        if not data:
            return None
        
        days_since_contact = None
        if data.get('last_contact'):
            days_since_contact = (datetime.now() - data['last_contact']).days
        
        return {
            'name': data['name'],
            'health_score': data['score'],
            'status': 'healthy' if data['score'] > 7 else 'at_risk' if data['score'] > 4 else 'critical',
            'last_contact_days': days_since_contact,
            'recommendations': self.get_recommendations(data['name'], limit=2)
        }
    
    def process_email(self, sender, subject, body):
        """
        Process incoming email and return analysis + suggested response
        
        Returns complete AI analysis package
        """
        full_text = f"{subject} {body}"
        
        # Sentiment analysis
        sentiment = self.analyze_sentiment(full_text)
        
        # Determine context type
        context_type = 'follow_up'
        if sentiment['urgent'] or sentiment['overall'] == 'negative':
            context_type = 'urgent'
        elif 'quote' in full_text.lower() or 'price' in full_text.lower():
            context_type = 'quotation'
        elif 'meeting' in full_text.lower() or 'call' in full_text.lower():
            context_type = 'meeting_request'
        
        # Extract topic
        topic = self._extract_topic(subject, body)
        
        # Generate response
        response = self.generate_response(sender, context_type, topic=topic)
        
        # Get recommendations
        recommendations = self.get_recommendations(sender, limit=2)
        
        return {
            'sender': sender,
            'subject': subject,
            'sentiment': sentiment,
            'suggested_response': response,
            'recommendations': recommendations,
            'priority': 'high' if sentiment['urgent'] else 'medium' if sentiment['overall'] == 'negative' else 'low',
            'timestamp': datetime.now().isoformat()
        }
    
    def _extract_topic(self, subject, body):
        """Extract main topic from email"""
        # Common business topics
        topics = {
            'valve': 'valve delivery timeline',
            'PO': 'purchase order',
            'quotation': 'quotation request',
            'delivery': 'delivery schedule',
            'meeting': 'upcoming meeting',
            'payment': 'payment terms',
            'invoice': 'invoice processing'
        }
        
        text = f"{subject} {body}".lower()
        for keyword, topic in topics.items():
            if keyword.lower() in text:
                return topic
        
        return 'our ongoing collaboration'


def main():
    """Demo/test the AI system"""
    ai = DigitalChrisAI()
    
    print("=" * 60)
    print("DIGITAL CHRIS v0.2 - AI CORE TEST")
    print("=" * 60)
    
    # Test sentiment analysis
    test_texts = [
        "Thank you for the update. Everything looks great! Looking forward to next steps.",
        "URGENT: We have a critical issue with the valve delivery. This needs immediate attention.",
        "Please review the attached quotation and let me know your thoughts."
    ]
    
    print("\n📊 SENTIMENT ANALYSIS TEST")
    for text in test_texts:
        result = ai.analyze_sentiment(text)
        print(f"\nText: {text[:50]}...")
        print(f"  Overall: {result['overall']} | Urgent: {result['urgent']}")
        print(f"  Pos: {result['positive']}, Neu: {result['neutral']}, Neg: {result['negative']}")
    
    # Test response generation
    print("\n\n🤖 AI RESPONSE GENERATION TEST")
    contexts = ['follow_up', 'urgent', 'quotation']
    for ctx in contexts:
        result = ai.generate_response('Tony', ctx, topic='valve shipment')
        print(f"\n{ctx.upper()}:")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Tone: {result['tone']}")
        print(f"  Response: {result['response'][:80]}...")
    
    # Test recommendations
    print("\n\n💡 GLOBAL RECOMMENDATIONS")
    recs = ai.get_recommendations(limit=5)
    for rec in recs:
        print(f"  [{rec['score']}%] {rec['title']}: {rec['description']}")
    
    # Test full email processing
    print("\n\n📧 FULL EMAIL PROCESSING TEST")
    result = ai.process_email(
        'Yulia@holy-cryo.com',
        'RE: Quotation for NIE System',
        'Hi Chris, can we schedule a call to discuss the pricing? Also, is there any flexibility on the delivery timeline?'
    )
    print(f"  Sender: {result['sender']}")
    print(f"  Priority: {result['priority']}")
    print(f"  Sentiment: {result['sentiment']['overall']}")
    print(f"  AI Response: {result['suggested_response']['response'][:100]}...")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
