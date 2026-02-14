#!/usr/bin/env python3
"""
이재명 키워드 실시간 커뮤니티 모니터링 시스템
- 대상: 클리앙, 뽐뿌, 더쿠, 볼베드림
- 주기: 15분
- 알림: 텔레그램
"""

import requests
import json
import time
import hashlib
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import feedparser
import re
from urllib.parse import quote

# 설정
CONFIG = {
    "keyword": "이재명",
    "interval_minutes": 15,
    "telegram_token": None,  # 환경변수에서 로드
    "telegram_chat_id": None,  # 환경변수에서 로드
    "seen_posts_file": "/Users/roturnjarvis/.openclaw/workspace/logs/seen_posts.json",
    "log_file": "/Users/roturnjarvis/.openclaw/workspace/logs/community_monitor.log"
}

# 헤더 (봇 차단 회피)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

class CommunityMonitor:
    def __init__(self):
        self.seen_posts = self.load_seen_posts()
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
    def load_seen_posts(self):
        """이미 본 게시물 로드"""
        try:
            with open(CONFIG['seen_posts_file'], 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            return set()
    
    def save_seen_posts(self):
        """본 게시물 저장"""
        import os
        os.makedirs(os.path.dirname(CONFIG['seen_posts_file']), exist_ok=True)
        with open(CONFIG['seen_posts_file'], 'w', encoding='utf-8') as f:
            json.dump(list(self.seen_posts), f, ensure_ascii=False)
    
    def generate_post_id(self, title, url, source):
        """게시물 고유 ID 생성 (중복 제거용)"""
        content = f"{source}:{title}:{url}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def send_telegram(self, message):
        """텔레그램 알림 전송"""
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not token or not chat_id:
            print(f"[알림] 텔레그램 설정 없음: {message[:100]}...")
            return
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"텔레그램 전송 실패: {e}")
    
    def log(self, message):
        """로그 기록"""
        import os
        os.makedirs(os.path.dirname(CONFIG['log_file']), exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        with open(CONFIG['log_file'], 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')

    def fetch_clien(self):
        """클리앙 정치/사회 게시판"""
        posts = []
        try:
            # 클리앙 RSS
            url = f"https://www.clien.net/service/board/park?&od=T31&po=0"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            items = soup.find_all('span', class_='subject_fixed')
            for item in items[:10]:  # 최근 10개만
                title = item.get_text(strip=True)
                if CONFIG['keyword'] in title:
                    link_elem = item.find_parent('a')
                    if link_elem:
                        href = link_elem.get('href', '')
                        full_url = f"https://www.clien.net{href}" if href.startswith('/') else href
                        posts.append({
                            'source': '클리앙',
                            'title': title,
                            'url': full_url,
                            'time': datetime.now().strftime('%H:%M')
                        })
            
            time.sleep(2)  # rate limiting
        except Exception as e:
            self.log(f"클리앙 오류: {e}")
        
        return posts

    def fetch_ppomppu(self):
        """뽐뿌 정치 자유게시판"""
        posts = []
        try:
            url = "http://www.ppomppu.co.kr/zboard/zboard.php?id=freeboard"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 뽐뿌는 테이블 구조
            rows = soup.find_all('tr', class_=['list1', 'list0'])
            for row in rows[:15]:
                title_elem = row.find('td', class_='eng list_vspace')
                if title_elem:
                    link = title_elem.find('a')
                    if link:
                        title = link.get_text(strip=True)
                        if CONFIG['keyword'] in title:
                            href = link.get('href', '')
                            posts.append({
                                'source': '뽐뿌',
                                'title': title,
                                'url': href if href.startswith('http') else f"http://www.ppomppu.co.kr/zboard/{href}",
                                'time': datetime.now().strftime('%H:%M')
                            })
            
            time.sleep(2)
        except Exception as e:
            self.log(f"뽐뿌 오류: {e}")
        
        return posts

    def fetch_theqoo(self):
        """더쿠 정치/사회"""
        posts = []
        try:
            # 더쿠는 검색 기능 사용
            encoded_keyword = quote(CONFIG['keyword'])
            url = f"https://theqoo.net/index?mid=hot&search_keyword={encoded_keyword}&search_target=title"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            items = soup.find_all('td', class_='title')
            for item in items[:10]:
                link = item.find('a')
                if link:
                    title = link.get_text(strip=True)
                    href = link.get('href', '')
                    posts.append({
                        'source': '더쿠',
                        'title': title,
                        'url': href if href.startswith('http') else f"https://theqoo.net{href}",
                        'time': datetime.now().strftime('%H:%M')
                    })
            
            time.sleep(2)
        except Exception as e:
            self.log(f"더쿠 오류: {e}")
        
        return posts

    def fetch_bobaedream(self):
        """보배드림 정치 게시판"""
        posts = []
        try:
            url = "https://www.bobaedream.co.kr/list?code=politic"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            items = soup.find_all('a', class_='bsubject')
            for item in items[:15]:
                title = item.get_text(strip=True)
                if CONFIG['keyword'] in title:
                    href = item.get('href', '')
                    posts.append({
                        'source': '보배',
                        'title': title,
                        'url': href if href.startswith('http') else f"https://www.bobaedream.co.kr{href}",
                        'time': datetime.now().strftime('%H:%M')
                    })
            
            time.sleep(2)
        except Exception as e:
            self.log(f"보배 오류: {e}")
        
        return posts

    def analyze_sentiment(self, title):
        """간단한 감성 분석"""
        positive_words = ['지지', '응원', '환호', '승리', '우세', '호재']
        negative_words = ['비판', '문제', '논란', '의혹', '피해', '반대', '악재', '형', '재판', '구속']
        
        pos_count = sum(1 for word in positive_words if word in title)
        neg_count = sum(1 for word in negative_words if word in title)
        
        if pos_count > neg_count:
            return '긍정'
        elif neg_count > pos_count:
            return '부정'
        else:
            return '중립'

    def categorize_post(self, title):
        """게시물 카테고리 분류"""
        categories = {
            '정책': ['정책', '법안', '예산', '세금', '복지', '부동산', '주택'],
            '사법': ['재판', '형', '구속', '기소', '검찰', '법원', '1심', '2심'],
            '정치': ['당', '지지율', '선거', '대표', '이재명', '민주당', '국힘'],
            '경제': ['주식', '증시', '기업', '경제', '투자'],
            '사회': ['논란', '사건', '사고', '여론']
        }
        
        for cat, keywords in categories.items():
            if any(kw in title for kw in keywords):
                return cat
        return '기타'

    def run(self):
        """메인 실행"""
        self.log(f"모니터링 시작: 키워드 '{CONFIG['keyword']}'")
        
        all_posts = []
        
        # 각 사이트 수집
        all_posts.extend(self.fetch_clien())
        all_posts.extend(self.fetch_ppomppu())
        all_posts.extend(self.fetch_theqoo())
        all_posts.extend(self.fetch_bobaedream())
        
        # 중복 제거 및 필터링
        new_posts = []
        for post in all_posts:
            post_id = self.generate_post_id(post['title'], post['url'], post['source'])
            if post_id not in self.seen_posts:
                self.seen_posts.add(post_id)
                post['sentiment'] = self.analyze_sentiment(post['title'])
                post['category'] = self.categorize_post(post['title'])
                new_posts.append(post)
        
        # 저장
        self.save_seen_posts()
        
        # 결과 출력 및 알림
        if new_posts:
            self.log(f"신규 게시물 {len(new_posts)}개 발견")
            
            # 요약 메시지 생성
            summary = f"🔍 <b>이재명 키워드 알림</b>\n"
            summary += f"⏰ {datetime.now().strftime('%H:%M')} 기준\n"
            summary += f"📊 신규 {len(new_posts)}개\n\n"
            
            # 카테고리별 정렬
            by_category = {}
            for post in new_posts:
                cat = post['category']
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(post)
            
            for cat, posts in by_category.items():
                summary += f"<b>[{cat}]</b>\n"
                for post in posts[:3]:  # 카테고리당 최대 3개
                    emoji = {'긍정': '🟢', '부정': '🔴', '중립': '⚪'}[post['sentiment']]
                    summary += f"{emoji} [{post['source']}] {post['title'][:40]}...\n"
                    summary += f"   └ {post['url'][:60]}...\n"
                summary += "\n"
            
            # 전체 통계
            sentiment_counts = {}
            for post in new_posts:
                s = post['sentiment']
                sentiment_counts[s] = sentiment_counts.get(s, 0) + 1
            
            summary += f"<b>감성 분포:</b> "
            summary += f"긍정 {sentiment_counts.get('긍정', 0)} | "
            summary += f"부정 {sentiment_counts.get('부정', 0)} | "
            summary += f"중립 {sentiment_counts.get('중립', 0)}"
            
            print("\n" + "="*60)
            print(summary)
            print("="*60)
            
            # 텔레그램 전송
            self.send_telegram(summary)
        else:
            self.log("신규 게시물 없음")
        
        return new_posts

if __name__ == "__main__":
    import os
    monitor = CommunityMonitor()
    monitor.run()
