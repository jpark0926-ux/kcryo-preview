# Google Sheets 자동화 설정 가이드

## 🎯 기능
- 실시간 포트폴리오 데이터
- 자동 차트 생성
- 텔레그램 알림 연동
- API로 데이터 자동 업데이트

## 📋 시트 구조

### Sheet 1: Holdings (보유 종목)
| 종목 | 티커 | 보유량 | 매입단가 | 현재가 | 평가액 | 수익률 | 변동 | 메모 |
|------|------|--------|----------|--------|--------|--------|------|------|
| Palantir | PLTR | 609 | $44,456 | $131.41 | ₩114.6M | 338% | -3.1% | AI/정부 |
| Tesla | TSLA | 116 | $284,358 | $417.44 | ₩69.2M | 116% | -2.6% | EV |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

### Sheet 2: Summary (요약)
| 항목 | 금액 | 비중 | 변동 | 차트 |
|------|------|------|------|------|
| 총 자산 | ₩554.8M | 100% | -1.4% | [파이차트] |
| 미국 주식 | ₩280M | 50.5% | -3.2% | |
| 암호화폐 | ₩189.7M | 34.2% | +0.8% | |
| 한국 | ₩85.1M | 15.3% | - | |

### Sheet 3: Altcoin Goal (잡코인 목표)
| 코인 | 보유량 | 현재가 | 평가액 | 목표 | 진척도 | 차트 |
|------|--------|--------|--------|------|--------|------|
| XRP | 1,841 | $1.40 | ₩3.7M | | | [진행바] |
| XLM | 24,000 | $0.166 | ₩5.7M | | | [진행바] |
| ADA | 9,500 | $0.24 | ₩3.3M | | | [진행바] |
| 합계 | | | ₩12.7M | ₩15M | 85% | [총 진행바] |

### Sheet 4: 10x Tracker (텐배거 추적)
| 종목 | 발견일 | 현재가 | 10x 목표 | 진척도 | 뉴스 | 메모 |
|------|--------|--------|----------|--------|------|------|
| PLTR | 2025.x | $131 | $444,560 | 33.8% | - | AI 정부 계약 |
| IONQ | 2025.x | $34 | $214,490 | 12.5% | AWS 파트너십 | 양자컴퓨팅 |
| RKLB | 2025.x | $67 | $358,530 | 17.9% | - | 우주 발사체 |

## 🔧 설정 방법

### 1. 새 Google Sheets 생성
```
https://sheets.new
```

### 2. Apps Script 연동 (Extensions → Apps Script)
```javascript
function updatePortfolio() {
  // API로 데이터 가져오기
  const sheet = SpreadsheetApp.getActiveSpreadsheet();
  const holdingsSheet = sheet.getSheetByName('Holdings');
  
  // Yahoo Finance API 연동 (묣)
  // CoinGecko API 연동 (암호화폐)
  // 가져와서 시트 업데이트
}

// 매일 오전 9시 자동 실행
timeUpdatePortfolio() {
  ScriptApp.newTrigger('updatePortfolio')
    .timeBased()
    .everyDays(1)
    .atHour(9)
    .create();
}
```

### 3. 텔레그램 봇 연동
```javascript
function sendTelegramAlert() {
  const botToken = 'YOUR_BOT_TOKEN';
  const chatId = '-1003339356591';
  
  const summary = getPortfolioSummary();
  const url = `https://api.telegram.org/bot${botToken}/sendMessage`;
  
  UrlFetchApp.fetch(url, {
    method: 'POST',
    payload: {
      chat_id: chatId,
      text: summary,
      parse_mode: 'HTML'
    }
  });
}
```

### 4. 차트 자동 생성
- Insert → Chart
- Pie Chart: 포트폴리오 구성
- Bar Chart: 종목별 변동률
- Line Chart: 자산 추이 (시간별)

## 🎨 템플릿 스타일

### 셀 서식
- 총 자산: 큰 글씨 + 볼드
- 수익률: 조걶 서식 (양수=초록, 음수=빨강)
- 진행도: 데이터 바 (시각적)

### 조걶 서식 예시
```
수익률 > 0% → 배경색 초록
수익률 < 0% → 배경색 빨강
변동률 > 5% → 글씨 굵게 + 배경 노랑
```

## 📱 앱 연동

### Google Sheets 모바일 앱
- 실시간 푸시 알림
- 위젯 지원 (홈화면에 자산 표시)
- 오프라인 모드

### 대안: Notion Database
- 더 예쁜 UI
- 데이터베이스 기능
- API 연동 가능

## ✅ 장점/단점

| 장점 | 단점 |
|------|------|
| 묣 | API 제한 있음 (일일 100회) |
| 템플릿 공유 가능 | 실시간은 아님 (수분 지연) |
| 모바일 앱 우수 | 복잡한 계산은 느림 |
| 텔레그램 연동 쉬움 | Apps Script 학습 필요 |

## 🚀 다음 단계

구현하려면:
1. Chris가 Google Sheets 템플릿 선택
2. API 키 발급 (Yahoo Finance, CoinGecko)
3. Apps Script 코드 작성 (제가 도움)
4. 테스트 및 텔레그램 연동

**시작할까요?**