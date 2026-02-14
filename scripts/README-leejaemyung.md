# 이재명 커뮤니티 모니터링 시스템

실시간 커뮤니티 키워드 모니터링 시스템

## 🎯 기능

- **클리앙, 뽐뿌, 더쿠, 볼베드림** 모니터링
- **15분마다** 자동 체크
- **중복 제거** (같은 내용 여러 커뮤니티 중복 방지)
- **감성 분석** (긍정/부정/중립 분류)
- **카테고리 분류** (정책/사법/정치/경제/사회)
- **텔레그램 알림** (실시간 푸시)

## 📁 파일 구조

```
scripts/
├── leejaemyung-monitor.py      # 메인 모니터링 스크립트
├── setup-leejaemyung-monitor.sh # 설치 스크립트
└── README-leejaemyung.md        # 이 파일

logs/
├── seen_posts.json              # 이미 본 게시물 목록
├── community_monitor.log        # 실행 로그
└── monitor-cron.log            # Cron 실행 로그
```

## 🚀 설치 방법

### 1. 필요한 패키지 설치
```bash
pip3 install requests beautifulsoup4 feedparser
```

### 2. 텔레그램 봇 설정
```bash
# 1. @BotFather 에게 /newbot 복사
# 2. 봇 이름 입력 (예: chris_monitor_bot)
# 3. 토큰 복사 (예: 123456789:ABCdefGHIjklMNOpqrSTU)

# 4. @userinfobot 에게 메시지 복사
# 5. 채팅 ID 복사 (예: 6948605509)

# 5. 환경변수 설정
export TELEGRAM_BOT_TOKEN='your_token'
export TELEGRAM_CHAT_ID='your_chat_id'
```

### 3. 설치 스크립트 실행
```bash
cd ~/.openclaw/workspace
./scripts/setup-leejaemyung-monitor.sh
```

### 4. Cron 자동 설정 확인
```bash
# 수동으로 추가하려면
crontab -e

# 다음 줄 추가
*/15 * * * * cd ~/.openclaw/workspace && python3 scripts/leejaemyung-monitor.py
```

## 🎮 사용 방법

### 수동 실행
```bash
python3 scripts/leejaemyung-monitor.py
```

### 출력 예시
```
🔍 이재명 키워드 알림
⏰ 14:30 기준
📊 신규 5개

[정책]
🟢 [클리앙] 이재명 대표, 주택공약 발표...
⚪ [뽐뿌] 부동산 정책 관련 여론조사...

[사법]
🔴 [볼베] 이재명 재판 관련 논란...

[정치]
⚪ [더쿠] 지지율 변화 분석...

감성 분포: 긍정 1 | 부정 1 | 중립 3
```

## ⚙️ 설정 변경

### 키워드 변경
`leejaemyung-monitor.py` 파일 상단의 `CONFIG['keyword']` 수정:

```python
CONFIG = {
    "keyword": "삼성전자",  # ← 변경
    ...
}
```

### 체크 주기 변경
```python
CONFIG = {
    "interval_minutes": 30,  # ← 30분으로 변경
    ...
}
```

### 사이트 추가/제거
`run()` 메서드에서 추가/제거:

```python
def run(self):
    all_posts = []
    all_posts.extend(self.fetch_clien())
    # all_posts.extend(self.fetch_ppomppu())  # ← 뽐뿌 제거
    all_posts.extend(self.fetch_theqoo())
    all_posts.extend(self.fetch_bobaedream())
    # self.fetch_newsite()  # ← 새 사이트 추가
```

## 🔍 로그 확인

```bash
# 실시간 로그 확인
tail -f logs/community_monitor.log

# Cron 실행 로그
tail -f logs/monitor-cron.log

# 본 게시물 목록 확인
cat logs/seen_posts.json | python3 -m json.tool
```

## ⚠️ 주의사항

1. **rate limiting**: 각 사이트마다 2초 대기 (밴 방지)
2. **robots.txt**: 일부 사이트는 크롤링 제한 있을 수 있음
3. **IP 밴**: 너무 자주 요청하면 일시적 차단 가능
4. **정확도**: 감성 분석은 단순 키워드 기반이라 정확도 제한적

## 🐛 문제 해결

### 텔레그램 알림 안 옴
```bash
# 환경변수 확인
echo $TELEGRAM_BOT_TOKEN
echo $TELEGRAM_CHAT_ID

# 봇 테스트
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d "chat_id=<CHAT_ID>&text=test"
```

### Cron 안 됨
```bash
# Cron 로그 확인
tail /var/log/cron.log  # macOS
# 또는
mail  # Cron 에러 메일 확인
```

### 한글이 깨짐
```bash
# locale 확인
locale

# UTF-8 설정
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

## 📝 업데이트 이력

- **2026-02-14**: v1.0.0 초기 버전
  - 4개 커뮤니티 지원
  - 감성 분석, 카테고리 분류
  - 텔레그램 알림
  - 중복 제거

## 🤝 커스터마이징

새로운 사이트 추가하려면 `fetch_사이트명()` 메서드 추가:

```python
def fetch_newsite(self):
    posts = []
    try:
        url = "https://example.com/board"
        response = self.session.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 사이트 구조에 맞게 파싱
        items = soup.find_all('div', class_='post')
        for item in items:
            title = item.find('h2').get_text()
            if CONFIG['keyword'] in title:
                posts.append({
                    'source': '새사이트',
                    'title': title,
                    'url': item.find('a')['href'],
                    'time': datetime.now().strftime('%H:%M')
                })
        
        time.sleep(2)
    except Exception as e:
        self.log(f"새사이트 오류: {e}")
    
    return posts
```

---

**만든이**: Wayne Manor 🦇  
**용도**: Chris의 정보 수집 자동화  
**라이선스**: Private Use Only
