# Google Workspace Service Account Setup (완전 자동화)

## 현재 문제
- OAuth는 브라우저 인증 필요 (Chris 개입 필요)
- Service Account는 한 번 설정 후 완전 자동

## 해결책: Service Account 생성

### Step 1: Service Account 만들기 (Chris가 5분)

1. https://console.cloud.google.com/iam-admin/serviceaccounts 접속
2. "서비스 계정 만들기" 클릭
3. 입력:
   - 이름: `wayne-manor-service`
   - 설명: `AI Assistant for Chris`
4. "만들기 및 계속"
5. 역할: "소유자" 또는 "편집자" 선택
6. "완료"

### Step 2: 키 발급 (중요!)

1. 생성된 서비스 계정 클릭
2. "키" 탭 → "키 추가" → "새 키 만들기"
3. JSON 선택 → "만들기"
4. 자동 다운로드됨 (`wayne-manor-*.json`)

### Step 3: Domain-Wide Delegation 활성화

같은 페이지에서:
1. "고급 설정" → "Google 전체 도메인 위임"
2. "Google 전체 도메인 위임 활성화" 체크
3. 다음 범위 추가:
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/drive.readonly`
   - `https://www.googleapis.com/auth/calendar.readonly`
4. "저장"

### Step 4: Admin Console 승인

https://admin.google.com
1. "보안" → "API 제어" → "도메인 전체 위임 관리"
2. 서비스 계정의 Client ID 추가
3. 위와 동일한 범위 입력
4. "승인"

---

## 완료 후

JSON 키 파일을 나에게 별낸면:
- ✅ 영구적 인증 (refresh 필요 없음)
- ✅ 완전 자동화
- ✅ Chris 개입 없이 API 호출 가능

**이 방식이면 한 번만 설정하면 끝!** 🎉
