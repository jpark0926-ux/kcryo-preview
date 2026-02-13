# Google Workspace × Wayne Manor 전체 설정 가이드

## 목표
Gmail + Drive + Calendar + Sheets에 AI 연동

---

## Phase 1: Google Cloud Console 설정 (Chris가 해야 함)

### Step 1: 프로젝트 생성
1. https://console.cloud.google.com 접속
2. 상단 프로젝트 선택 → "새 프로젝트"
3. 이름: `wayne-manor-integration`
4. "만들기"

### Step 2: API 활성화
왼쪽 메뉴 → "API 및 서비스" → "라이브러리"

활성화할 API (4개):
- ✅ Gmail API
- ✅ Google Drive API
- ✅ Google Calendar API
- ✅ Google Sheets API

각각 검색 → "사용 설정"

### Step 3: Service Account 생성
1. "API 및 서비스" → "사용자 인증 정보"
2. "사용자 인증 정보 만들기" → "서비스 계정"
3. 이름: `wayne-manor-service`
4. "만들기 및 계속"
5. "완료"

### Step 4: 키 발급
1. 생성된 서비스 계정 클릭
2. "키" 탭 → "키 추가" → "새 키 만들기"
3. JSON 선택 → "만들기"
4. 자동 다운로드됨 (`wayne-manor-*.json`)

**이 파일을 나에게 전송** (Telegram 파일로)

### Step 5: Domain-wide Delegation (중요)
1. 서비스 계정 → "고급 설정" → "Google 전체 도메인 위임"
2. "Google 전체 도메인 위임 활성화" 체크
3. 다음 OAuth 범위 추가:

```
https://mail.google.com/
https://www.googleapis.com/auth/drive
https://www.googleapis.com/auth/calendar
https://www.googleapis.com/auth/spreadsheets
```

---

## Phase 2: Admin Console 설정 (Chris가 해야 함)

https://admin.google.com

1. "보안" → "API 제어"
2. "도메인 전체 위임 관리"
3. "새로 추가"
4. Step 4의 Client ID 입력
5. OAuth 범위 (위와 동일) 입력
6. "승인"

---

## Phase 3: Wayne Manor 연동 (내가 처리)

Chris가 JSON 키 파일을 별내주면:
1. 키 파일을 Mac mini에 안전하게 저장
2. OpenClaw 설정에 Google Workspace API 추가
3. 테스트: Gmail 읽기 테스트
4. 테스트: Drive 파일 목록 조회
5. 테스트: Calendar 이벤트 조회

---

## 예상 소요 시간

| 단계 | 시간 | 누가 |
|------|------|------|
| Phase 1 | 15분 | Chris |
| Phase 2 | 5분 | Chris |
| Phase 3 | 20분 | Wayne |
| **총계** | **40분** | |

---

## 다음 테스트 (설정 후)

1. **Gmail 테스트**: "오늘 메일 3줄 요약"
2. **Drive 테스트**: "KC 폼더 파일 목록"
3. **Calendar 테스트**: "이번 주 일정 충돌 체크"
4. **통합 테스트**: "오늘 보고서 생성"

---

**시작할까요?** Phase 1부터?
