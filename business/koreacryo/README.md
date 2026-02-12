# KoreaCryo 웹사이트 리뉴얼

**목표**: 한국초저온용기(주) 웹사이트 현대화 (모바일 대응, HTTPS, 고급스러운 디자인)

## 현황
- **기존 사이트**: koreacryo.com (ASP, HTTP only, 모바일 미지원)
- **프로토타입**: https://jpark0926-ux.github.io/kcryo-preview/
- **상태**: 🟡 프로토타입 제작중
- **마지막 업데이트**: 2026-02-12

## 회사 정보
- **상호**: 한국초저온용기(주) → **케이크라이오(주) / K-Cryo** 변경 추진중
- **대표**: 이희란
- **위치**: 성남 중원구
- **사업**: 초저온장비, 바이오장비, 헬스케어, 가스엔지니어링

## 완료된 작업
- ✅ GitHub Pages 배포 (jpark0926-ux.github.io/kcryo-preview/)
- ✅ 반응형 디자인 적용 (모바일/태블릿/데스크톱)
- ✅ 제품 카테고리 4개 페이지 제작
  - 초저온장비 (Cryogenic Equipment)
  - 바이오뱅킹 (Biobanking)
  - 헬스케어 (Healthcare)
  - 가스엔지니어링 (Gas Engineering) - 대폭 업그레이드
- ✅ 해외 거래선 8곳 정리
  - Taylor-Wharton, Luxfer, TOMCO2, Cryofab, PureAire
  - **Turbines Inc.** (TMC 극저온 유량계 공급사)
  - Thunderbird Cylinders
  - ~~Liquid Controls~~ (더이상 취급 안 함)
- ✅ K-Cryo 로고 시안 12종 제작 (v1~v12)
- ✅ 임직원 시연 완료
- ✅ 이미지 배경 제거 작업 (api4ai AI 서비스 사용)
- ✅ PPT 자료 분석 완료 (image1~59)

## 진행중
- ⏳ 가스엔지니어링 페이지 현장사진 추가 (image53~56)
- ⏳ 바이오뱅킹 페이지 현장사진 추가 (image57~59)
- ⏳ 최종 디자인 피드백 대기

## 다음 스텝
1. 현장사진 삽입 완료
2. Chris 최종 검토
3. 실제 도메인 배포 방안 결정
4. 호스팅 이전 (가비아 → ?)
5. HTTPS 적용
6. SEO 최적화

## 파일 구조
```
koreacryo-prototype/           # 메인 프로토타입
├── index.html                # 홈페이지
├── cryo-equipment.html       # 초저온장비
├── biobanking.html           # 바이오뱅킹
├── healthcare.html           # 헬스케어
├── gas-engineering.html      # 가스엔지니어링
├── specialty-gas.html        # 특수가스 (추가됨)
├── liquid-helium.html        # 액체헬륨 (추가됨)
├── ppt-images/               # PPT 추출 이미지 (image1~59)
├── site-images/              # 사이트용 이미지
├── lc-images/                # Liquid Controls (아카이브)
├── ti-images/                # Turbines Inc. 자료
└── logo-kcryo-v*.png         # K-Cryo 로고 시안 12종

kcryo-preview/                # GitHub Pages 배포 버전
```

## 기술 스택
- 순수 HTML/CSS/JavaScript (프레임워크 없음)
- 반응형 디자인 (미디어쿼리)
- GitHub Pages 호스팅
- api4ai 이미지 배경 제거 API

## 디자인 컨셉
- 고급스러운 기업 이미지
- 깔끔한 레이아웃
- 제품 중심 구성
- 해외 거래선 강조 (신뢰도)
- 모바일 최적화 필수

## 참고
- 기존 사이트: http://koreacryo.com (가비아 호스팅)
- 상호변경 검토: 케이크라이오(주) / K-Cryo (인터넷등기소 0건, KIPRIS 상표 0건)
