#!/usr/bin/env python3
"""
Gmail 자동 분석 및 결정 추출 시스템
Digital Chris - Seamless Data Collection
"""

import subprocess
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
import hashlib

class GmailAnalyzer:
    def __init__(self):
        self.workspace = Path("/Users/roturnjarvis/.openclaw/workspace")
        self.decisions_dir = self.workspace / "memory" / "decisions"
        self.decisions_dir.mkdir(parents=True, exist_ok=True)
        self.processed_file = self.workspace / "logs" / "gmail_processed.json"
        self.processed_ids = self.load_processed()
        
    def load_processed(self):
        """이미 처리한 이메일 ID 로드"""
        if self.processed_file.exists():
            with open(self.processed_file) as f:
                return json.load(f)
        return []
    
    def save_processed(self):
        """처리한 이메일 ID 저장"""
        self.processed_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.processed_file, 'w') as f:
            json.dump(self.processed_ids, f, indent=2)
    
    def run_gog(self, command):
        """gog CLI 실행"""
        try:
            result = subprocess.run(
                ["/usr/local/bin/gog"] + command,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return result.stdout
            else:
                print(f"Error: {result.stderr}")
                return None
        except Exception as e:
            print(f"Exception: {e}")
            return None
    
    def get_recent_emails(self, hours=24, days=None):
        """최근 N시간 또는 N일 이메일 가져오기"""
        if days:
            since_date = (datetime.now() - timedelta(days=days)).strftime("%Y/%m/%d")
        else:
            since_date = (datetime.now() - timedelta(hours=hours)).strftime("%Y/%m/%d")
        query = f"after:{since_date} in:inbox"
        
        result = self.run_gog(["gmail", "search", query, "--json"])
        if not result:
            return []
        
        try:
            threads = json.loads(result)
            # threads가 list가 아니면 list로 변환
            if isinstance(threads, dict):
                threads = threads.get('threads', [])
            if not isinstance(threads, list):
                threads = [threads] if threads else []
            return threads
        except Exception as e:
            print(f"JSON parse error: {e}")
            return []
    
    def get_message_content(self, message_id):
        """이메일 내용 가져오기"""
        result = self.run_gog(["gmail", "get", message_id, "--json"])
        if not result:
            return None
        
        try:
            message = json.loads(result)
            return message
        except:
            return None
    
    def extract_decision_patterns(self, subject, body, sender, date):
        """결정/액션 패턴 추출"""
        text = f"{subject} {body}".lower()
        decisions = []
        
        # 패턴 매칭
        patterns = {
            "투자": [
                r"(매수|매도|추가매수|익절|손절|보유)",
                r"(주식|코인|비트|eth|btc|삼성|현대)",
                r"(\d+%|(\d+원))"
            ],
            "비즈니스": [
                r"(계약|계약서|견적|제안|수락|거절|미팅|회의)",
                r"(로턴|크라이오|koreacryo)",
                r"(~까지|마감|일정|예약)"
            ],
            "일정": [
                r"(약속|만남|일정|예약|변경|취소|연기)",
                r"(월요일|화요일|수요일|목요일|금요일|내일|모레)"
            ],
            "재무": [
                r"(대출|이자|납부|결제|입금|출금|송금)",
                r"(은행|금리|환율)"
            ]
        }
        
        detected_categories = []
        for category, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, text):
                    detected_categories.append(category)
                    break
        
        if not detected_categories:
            return None
        
        # 중요도 판단
        importance = self.calculate_importance(subject, body, sender, detected_categories)
        
        return {
            "categories": list(set(detected_categories)),
            "importance": importance,
            "subject": subject,
            "sender": sender,
            "date": date,
            "extracted_text": self.extract_key_sentences(subject, body)
        }
    
    def calculate_importance(self, subject, body, sender, categories):
        """중요도 계산 (HIGH/MEDIUM/LOW)"""
        score = 0
        
        # 발신자
        important_senders = ["@koreacryo.com", "@roturn.com", "은행", "법무", "세무"]
        for s in important_senders:
            if s in sender.lower():
                score += 3
        
        # 카테고리
        if "투자" in categories:
            score += 3
        if "비즈니스" in categories:
            score += 2
        
        # 키워드
        urgent_keywords = ["긴급", "중요", "마감", "오늘", "바로", "즉시", "필수"]
        text = (subject + body).lower()
        for kw in urgent_keywords:
            if kw in text:
                score += 2
        
        # 마감일
        if re.search(r"(~까지|까지回复|까지 답변)", text):
            score += 2
        
        if score >= 5:
            return "HIGH"
        elif score >= 2:
            return "MEDIUM"
        return "LOW"
    
    def extract_key_sentences(self, subject, body):
        """중요 문장 추출"""
        sentences = []
        text = f"{subject}. {body}"
        
        # 액션 문장 추출
        action_patterns = [
            r"[^.]*?(확인|검토|회신|답변|연락|진행)[^.]*?",
            r"[^.]*?(수락|거절|보류|연기|취소)[^.]*?",
            r"[^.]*?(예약|일정|약속|미팅)[^.]*?"
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern + r"[.!?]", text[:500])  # 앞부분만
            sentences.extend(matches[:2])  # 최대 2개
        
        return " | ".join(sentences[:3]) if sentences else subject
    
    def save_decision(self, decision, message_id):
        """결정 정보 저장"""
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"{today}_gmail_{message_id[:8]}.md"
        filepath = self.decisions_dir / filename
        
        content = f"""# 이메일 자동 분석

## 메타데이터
- **날짜**: {decision['date']}
- **유형**: {', '.join(decision['categories'])}
- **중요도**: {decision['importance']}
- **발신자**: {decision['sender']}
- **제목**: {decision['subject']}
- **출처**: Gmail 자동 분석

## 추출 내용
{decision['extracted_text']}

## 액션 아이템
- [ ] 확인 필요
- [ ] 후속 조치 예정

## 태그
#{decision['categories'][0] if decision['categories'] else '분류전'} #자동수집 #이메일
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def run_analysis(self):
        """메인 분석 실행"""
        print(f"🔍 Gmail 분석 시작: {datetime.now()}")
        
        # 최근 24시간 이메일
        threads = self.get_recent_emails(24)
        if not threads:
            print("새 이메일 없음")
            return []
        
        print(f"📧 {len(threads)}개 스레드 발견")
        
        new_decisions = []
        for thread in threads:
            thread_id = thread.get('id')
            if not thread_id or thread_id in self.processed_ids:
                continue
            
            # 메시지 내용 가져오기
            message = self.get_message_content(thread_id)
            if not message:
                continue
            
            # 내용 추출
            subject = message.get('subject', '')
            sender = message.get('from', '')
            date = message.get('date', '')
            body = message.get('snippet', '')  # 요약본
            
            # 결정 패턴 추출
            decision = self.extract_decision_patterns(subject, body, sender, date)
            if decision and decision['importance'] in ['HIGH', 'MEDIUM']:
                # 저장
                filepath = self.save_decision(decision, thread_id)
                new_decisions.append({
                    'file': str(filepath),
                    'decision': decision
                })
                print(f"✅ 저장: {subject[:30]}... [{decision['importance']}]")
            
            # 처리 완료 표시
            self.processed_ids.append(thread_id)
        
        # 저장
        self.save_processed()
        
        print(f"📊 분석 완료: {len(new_decisions)}개 저장")
        return new_decisions

if __name__ == "__main__":
    analyzer = GmailAnalyzer()
    decisions = analyzer.run_analysis()
    
    # 텔레그램 알림 (선택적)
    if decisions:
        print(f"\n🚨 중요 이메일 {len(decisions)}건 감지됨")
        for d in decisions:
            print(f"  - [{d['decision']['importance']}] {d['decision']['subject'][:40]}")
