#!/usr/bin/env python3
"""
한국 커뮤니티 핫토픽 모니터링 시스템 (랭킹 기반)
- 대상: 클리앙, 뽐뿌, 더쿠, 딴지일보
- 주기: 1시간
- 기준: 조회수/댓글수/추천수 TOP
"""

import requests
import json
import time
import hashlib
import os
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote

# 설정
CONFIG = {
    "interval_minutes": 60,
    "top_n": 10,  # 각 사이트당 TOP N
    "min_views": 1000,  # 최소 조회수 필터
    "min_comments": 10,  # 최소 댓글수 필터
    "telegram_token": os.getenv('TELEGRAM_BOT_TOKEN'),
    "telegram_chat_id": os.getenv('TELEGRAM_CHAT_ID'),
    "seen_posts_file": "/Users/roturnjarvis/.openclaw/workspace/logs/hot_topics_seen.json",
    "log_file": "/Users/roturnjarvis/.openclaw/workspace/logs/hot_topics_monitor.log",
    "trends_file": "/Users/roturnjarvis/.openclaw/workspace/logs/hot_topics_trends.json"
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

class HotTopicsMonitor:
    def __init__(self):
        self.seen_posts = self.load_seen_posts()
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.trends = self.load_trends()

    def load_seen_posts(self):
        try:
            with open(CONFIG['seen_posts_file'], 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except:
            return set()

    def save_seen_posts(self):
        os.makedirs(os.path.dirname(CONFIG['seen_posts_file']), exist_ok=True)
        with open(CONFIG['seen_posts_file'], 'w', encoding='utf-8') as f:
            json.dump(list(self.seen_posts), f, ensure_ascii=False)

    def load_trends(self):
        try:
            with open(CONFIG['trends_file'], 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"hourly": {}, "daily": {}}

    def save_trends(self):
        os.makedirs(os.path.dirname(CONFIG['trends_file']), exist_ok=True)
        with open(CONFIG['trends_file'], 'w', encoding='utf-8') as f:
            json.dump(self.trends, f, ensure_ascii=False, indent=2)

    def generate_post_id(self, title, url, source):
        content = f"{source}:{title}:{url}"
        return hashlib.md5(content.encode()).hexdigest()[:16]

    def log(self, message):
        os.makedirs(os.path.dirname(CONFIG['log_file']), exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        with open(CONFIG['log_file'], 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')

    def send_telegram(self, message):
        if not CONFIG['telegram_token'] or not CONFIG['telegram_chat_id']:
            print(f"[알림] {message[:200]}...")
            return

        url = f"https://api.telegram.org/bot{CONFIG['telegram_token']}/sendMessage"
        payload = {
            'chat_id': CONFIG['telegram_chat_id'],
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.json()
        except Exception as e:
            self.log(f"텔레그램 실패: {e}")

    def extract_content_summary(self, text, max_length=150):
        """게시물 내용 요약"""
        # HTML 제거
        soup = BeautifulSoup(text, 'html.parser')
        clean_text = soup.get_text(separator=' ', strip=True)
        # 앞부분만 추출
        summary = clean_text[:max_length].replace('\n', ' ').replace('\r', '')
        if len(clean_text) > max_length:
            summary += "..."
        return summary

    def analyze_sentiment_detailed(self, title, content=""):
        """상세 감성 분석"""
        text = f"{title} {content}".lower()

        positive_keywords = ['지지', '응원', '환호', '승리', '우세', '호재', '성공', '긍정', '희망', '개선']
        negative_keywords = ['비판', '문제', '논란', '의혹', '피해', '반대', '악재', '실패', '부정', '우려', '사과', '규탄']
        angry_keywords = ['분노', '격분', '환장', '미친', '개XX', '좌파', '우파', '극우', '극좌']

        pos_count = sum(1 for word in positive_keywords if word in text)
        neg_count = sum(1 for word in negative_keywords if word in text)
        angry_count = sum(1 for word in angry_keywords if word in text)

        if angry_count > 0:
            return {'sentiment': '격앙', 'emoji': '🔥', 'score': -2}
        elif neg_count > pos_count:
            return {'sentiment': '부정', 'emoji': '🔴', 'score': -1}
        elif pos_count > neg_count:
            return {'sentiment': '긍정', 'emoji': '🟢', 'score': 1}
        else:
            return {'sentiment': '중립', 'emoji': '⚪', 'score': 0}

    def categorize_topic(self, title):
        """토픽 카테고리 분류"""
        categories = {
            '정치': ['이재명', '윤석열', '국힘', '민주당', '대선', '선거', '국회', '정부', '대통령', '야당', '여당'],
            '경제': ['주식', '증시', '코인', '부동산', '집값', '금리', '환율', '물가', '경기', '기업', '산업'],
            '사회': ['사건', '사고', '범죄', '법원', '재판', '경찰', '소방', '재난', '안전'],
            '노동': ['노조', '파업', '최저임금', '근로', '해고', '노동자', '직장'],
            '교육': ['학교', '수능', '대학', '학생', '교사', '교육', '입시'],
            'IT/테크': ['AI', '인공지능', '애플', '구글', '삼성', '카카오', '네이버', '스타트업', '기술'],
            '국제': ['미국', '중국', '일본', '북한', '우크라이나', '중동', '전쟁', '외교'],
            '문화': ['영화', '드라마', '연예', '음악', '예술', '스포츠', '축구', '야구']
        }

        title_lower = title.lower()
        for cat, keywords in categories.items():
            if any(kw in title_lower for kw in keywords):
                return cat
        return '기타'

    def fetch_clien_hot(self):
        """클리앙 인기 게시물"""
        posts = []
        try:
            # 추천 많은 순
            url = "https://www.clien.net/service/board/park?&od=T33"  # 공감 순
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            items = soup.find_all('div', class_='list_item')
            for item in items[:CONFIG['top_n']]:
                try:
                    title_elem = item.find('span', class_='subject_fixed')
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)
                    link_elem = title_elem.find_parent('a')
                    url = link_elem['href'] if link_elem else ''
                    if url and not url.startswith('http'):
                        url = f"https://www.clien.net{url}"

                    # 조회수, 댓글, 추천
                    hit_elem = item.find('span', class_='hit')
                    comment_elem = item.find('span', class_='rSymph05')
                    like_elem = item.find('span', class_='recommend')

                    views = int(hit_elem.get_text().replace(',', '')) if hit_elem else 0
                    comments = int(comment_elem.get_text()) if comment_elem else 0
                    likes = int(like_elem.get_text()) if like_elem else 0

                    if views >= CONFIG['min_views'] or comments >= CONFIG['min_comments']:
                        posts.append({
                            'source': '클리앙',
                            'title': title,
                            'url': url,
                            'views': views,
                            'comments': comments,
                            'likes': likes,
                            'time': datetime.now().strftime('%H:%M')
                        })
                except Exception as e:
                    continue

            time.sleep(2)
        except Exception as e:
            self.log(f"클리앙 오류: {e}")

        return posts

    def fetch_ppomppu_hot(self):
        """뽐뿌 인기 게시물"""
        posts = []
        try:
            # 인기글 조회순 정렬
            url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=freeboard&sort=read_num&how=desc"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 실제 게시물 tr 찾기 (조회수가 1000 이상인)
            all_tr = soup.find_all('tr')
            
            for tr in all_tr:
                try:
                    tds = tr.find_all('td')
                    if len(tds) < 5:
                        continue
                    
                    # 마지막 td가 조회수인지 확인
                    views_text = tds[-1].get_text(strip=True).replace(',', '')
                    if not views_text.isdigit():
                        continue
                    
                    views = int(views_text)
                    
                    # 조회수 500 이상만
                    if views < 500:
                        continue
                    
                    # 제목 찾기 (보통 td[1])
                    title_td = None
                    for td in tds[1:4]:
                        link = td.find('a', href=True)
                        if link:
                            title_text = link.get_text(strip=True)
                            if len(title_text) > 5 and 'javascript' not in link.get('href', ''):
                                title_td = td
                                break
                    
                    if not title_td:
                        continue
                    
                    link = title_td.find('a', href=True)
                    title = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    # 댓글 수 찾기 (제목에 [n] 형태)
                    comments = 0
                    import re
                    comment_match = re.search(r'\[(\d+)\]$', title)
                    if comment_match:
                        comments = int(comment_match.group(1))
                        title = re.sub(r'\[\d+\]$', '', title).strip()
                    
                    # 공지/규칙 제외
                    skip_keywords = ['규칙', '공지', '필독', '이용안내', '운영원칙']
                    if any(kw in title for kw in skip_keywords):
                        continue
                    
                    # 작성자 (td[2] 또는 td[3])
                    author = ""
                    for td in tds[2:4]:
                        text = td.get_text(strip=True)
                        if text and not text.isdigit():
                            author = text
                            break
                    
                    full_url = href if href.startswith('http') else f"https://www.ppomppu.co.kr/zboard/{href}"
                    
                    posts.append({
                        'source': '뽐뿌',
                        'title': title,
                        'url': full_url,
                        'views': views,
                        'comments': comments,
                        'likes': 0,
                        'time': datetime.now().strftime('%H:%M')
                    })
                    
                    if len(posts) >= CONFIG['top_n']:
                        break
                        
                except Exception as e:
                    continue
            
            time.sleep(2)
        except Exception as e:
            self.log(f"뽐뿌 오류: {e}")
        
        return posts

    def fetch_theqoo_hot(self):
        """더쿠 인기 게시물"""
        posts = []
        try:
            url = "https://theqoo.net/hot"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 테이블에서 tr 추출
            tables = soup.find_all('table', {'class': lambda x: x})
            if not tables:
                return posts
            
            all_tr = tables[0].find_all('tr')
            
            for tr in all_tr:
                try:
                    tds = tr.find_all('td')
                    if len(tds) < 5:
                        continue
                    
                    # td[0]: 번호, td[1]: 카테고리, td[2]: 제목, td[3]: 시간, td[4]: 조회수
                    # 번호가 숫자인지 확인 (공지 제외)
                    no_text = tds[0].get_text(strip=True)
                    if not no_text.isdigit():
                        continue
                    
                    # 제목 td에서 링크 추출
                    title_td = tds[2]
                    link = title_td.find('a', href=True)
                    if not link:
                        continue
                    
                    title = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    # 카테고리
                    category = tds[1].get_text(strip=True)
                    
                    # 조회수
                    views_text = tds[4].get_text(strip=True).replace(',', '')
                    views = int(views_text) if views_text.isdigit() else 0
                    
                    if views < 500:
                        continue
                    
                    # 댓글 수 (제목에 [n] 형태)
                    comments = 0
                    import re
                    comment_match = re.search(r'\[(\d+)\]$', title)
                    if comment_match:
                        comments = int(comment_match.group(1))
                        title = re.sub(r'\[\d+\]$', '', title).strip()
                    
                    posts.append({
                        'source': '더쿠',
                        'title': title,
                        'url': href if href.startswith('http') else f"https://theqoo.net{href}",
                        'views': views,
                        'comments': comments,
                        'likes': 0,
                        'category_tag': category,
                        'time': datetime.now().strftime('%H:%M')
                    })
                    
                    if len(posts) >= CONFIG['top_n']:
                        break
                        
                except Exception as e:
                    continue
            
            time.sleep(2)
        except Exception as e:
            self.log(f"더쿠 오류: {e}")
        
        return posts

    def fetch_ddanzi_hot(self):
        """딴지일보 인기 게시물"""
        posts = []
        try:
            url = "https://www.ddanzi.com/free?sort_index=readed_count"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 딴지는 /free/NUMBER 형태의 링크
            import re
            all_links = soup.find_all('a', href=True)
            seen_titles = set()
            
            for link in all_links:
                try:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    
                    # 패턴: /free/숫자
                    if not re.match(r'.*/free/\d+$', href):
                        continue
                    
                    # 제목 길이 체크
                    if len(title) < 10 or len(title) > 200:
                        continue
                    
                    # 중복 제거
                    if title in seen_titles:
                        continue
                    seen_titles.add(title)
                    
                    # 부모 요소에서 메타 정보 찾기
                    parent = link.find_parent(['li', 'div', 'tr'])
                    views = 0
                    comments = 0
                    
                    if parent:
                        parent_text = parent.get_text()
                        # 조회수: 숫자,숫자회
                        view_match = re.search(r'([\d,]+)\s*회', parent_text)
                        if view_match:
                            views = int(view_match.group(1).replace(',', ''))
                    
                    # 댓글: 제목에서 [n] 추출
                    comment_match = re.search(r'\[(\d+)\]', title)
                    if comment_match:
                        comments = int(comment_match.group(1))
                        title = re.sub(r'\[\d+\]', '', title).strip()
                    
                    # URL 처리
                    full_url = href if href.startswith('http') else f"https://www.ddanzi.com{href}"
                    
                    posts.append({
                        'source': '딴지',
                        'title': title,
                        'url': full_url,
                        'views': views,
                        'comments': comments,
                        'likes': 0,
                        'time': datetime.now().strftime('%H:%M')
                    })
                    
                    if len(posts) >= CONFIG['top_n']:
                        break
                        
                except Exception as e:
                    continue
            
            time.sleep(2)
        except Exception as e:
            self.log(f"딴지 오류: {e}")
        
        return posts

    def run(self):
        """메인 실행"""
        self.log("핫토픽 모니터링 시작")

        all_posts = []
        all_posts.extend(self.fetch_clien_hot())
        all_posts.extend(self.fetch_ppomppu_hot())
        all_posts.extend(self.fetch_theqoo_hot())
        all_posts.extend(self.fetch_ddanzi_hot())

        # 인기도 점수 계산 (조회수 + 댓글수*10)
        for post in all_posts:
            post['score'] = post['views'] + (post['comments'] * 10)
            post['sentiment'] = self.analyze_sentiment_detailed(post['title'])
            post['category'] = self.categorize_topic(post['title'])
            post['post_id'] = self.generate_post_id(post['title'], post['url'], post['source'])

        # 점수순 정렬
        all_posts.sort(key=lambda x: x['score'], reverse=True)

        # 중복 제거 및 신규 포스트 필터링
        new_posts = []
        for post in all_posts:
            if post['post_id'] not in self.seen_posts:
                self.seen_posts.add(post['post_id'])
                new_posts.append(post)

        self.save_seen_posts()

        # 트렌드 업데이트
        hour = datetime.now().strftime('%H:00')
        if hour not in self.trends['hourly']:
            self.trends['hourly'][hour] = []
        self.trends['hourly'][hour].extend([p['category'] for p in new_posts])
        self.save_trends()

        # 결과 출력 및 알림
        if new_posts:
            self.log(f"신규 핫토픽 {len(new_posts)}개 발견")
            self.send_notification(new_posts)
        else:
            self.log("신규 핫토픽 없음")

        return new_posts

    def send_notification(self, posts):
        """알림 메시지 생성 및 전송 - 커뮤별 TOP 5"""
        # 출처별 그룹화
        by_source = {'클리앙': [], '뽐뿌': [], '더쿠': [], '딴지': []}
        for post in posts:
            source = post['source']
            if source in by_source:
                by_source[source].append(post)
        
        # 메시지 생성 (HTML 형식으로 클릭 가능한 링크)
        message = f"🔥 <b>실시간 핫토픽</b>\n"
        message += f"⏰ {datetime.now().strftime('%H:%M')} 기준\n\n"
        
        # 커뮤별 TOP 5
        for source, source_posts in by_source.items():
            if not source_posts:
                continue
            
            # 점수순 정렬 후 TOP 5
            source_posts.sort(key=lambda x: x.get('score', x['views']), reverse=True)
            top_posts = source_posts[:5]
            
            message += f"<b>📌 {source} TOP {len(top_posts)}</b>\n"
            
            for i, post in enumerate(top_posts, 1):
                emoji = post['sentiment']['emoji']
                title = post['title'][:30] + "..." if len(post['title']) > 30 else post['title']
                views = f"{post['views']:,}" if post['views'] > 0 else "N/A"
                comments = f"💬{post['comments']}" if post['comments'] > 0 else ""
                
                # 클릭 가능한 링크 (HTML)
                message += f"{i}. {emoji} <a href='{post['url']}'>{title}</a>\n"
                message += f"   👁 {views} {comments}\n"
            
            message += "\n"
        
        # 전체 통계
        total_posts = sum(len(v) for v in by_source.values())
        total_views = sum(sum(p['views'] for p in v) for v in by_source.values())
        
        message += f"<b>📊 전체:</b> {total_posts}개 게시물, 총 {total_views:,} 조회\n"
        message += f"<i>1시간마다 업데이트</i>"
        
        print("\n" + "="*70)
        print(message.replace('<b>', '').replace('</b>', '').replace('<a href=\'', '[').replace('\'>', '] ').replace('</a>', '').replace('<i>', '').replace('</i>', ''))
        print("="*70)
        
        self.send_telegram(message)

if __name__ == "__main__":
    monitor = HotTopicsMonitor()
    monitor.run()
