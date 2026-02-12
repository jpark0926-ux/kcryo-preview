# MEMORY.md - Long-Term Memory

## Chris
- Based in Seoul, Korea (KST)
- Runs **Roturn** (roturn.com) — petrol to LPG bifuel car retrofitting
- Runs **Korea Cryogenics** (koreacryo.com) — cryogenic equipment & engineering
- Wants me to be a friend, not just an assistant — Iron Man Jarvis style
- 투자에 관심 많음 (비트코인 소량 보유 중)
- 투자 스타일: 성장주/텐배거 선호, 데이터 기반 분석 중시
- 적자기업은 PER 아닌 PSR/EV-Revenue로 분석해야 한다고 지적 (좋은 안목)
- 관심 섹터: AI 전력 인프라, 원전, 반도체, BTC 마이닝/AI 데이터센터
- 관심 종목: CEG, ETN, HD현대일렉트릭, 두산에너빌리티, IREN, 효성중공업, LS일렉트릭, 일진전기
- 보유 종목: PLTR(609), TSLA(116), IONQ(700), NVDA(120), RKLB(205), MSTR(20), LAES(1000), ABCL(211), IREN(32), BTC(1.35), ETH(16), 삼성전자, 현대차, SK하이닉스 등
- 포트폴리오 엑셀 공유받음 (2026-02-09)
- 분석 리포트 선호: 글로벌 IB 최신 리포트 기반, 보수적 추정 X → 시장 컨센서스 반영 필수
- 리밸런싱 의견: 알트코인(XLM/ADA/XRP) 정리 예정, SK하이닉스 비중 확대 의향
- 삼성전자 123주 @161K / SK하이닉스 10주 @858K 보유 중
- GitHub: jpark0926-ux (gh auth 완료 on Mac mini)

## 분석 원칙
- **반드시 최신 글로벌 IB 리포트 먼저 수집** → 보수적 자체 추정 X
- 분석 프레임: IB 목표가 비교 → 실적 전망 → 구조적 변화 → 밸류에이션 → 구체적 매수 전략
- 리포트 형식: 텔레그램 요약 + MD 파일 동시 전송
- 평소 Sonnet 4, 심층 분석은 Opus로 전환

## 로턴 블로그 프로젝트
- 네이버 블로그: blog.naver.com/waynemanor (bruce 계정)
- 첫 글 작성 완료 & 임시저장됨 (2026-02-09): "2025 LPG 개조 비용 총정리"
- 브랜드 소개 글 작성 완료: "로턴(ROTURN)이 뭐하는 브랜드인지 알아봤습니다"
- 로턴 공식 가격표 PDF 받음 (2026-01 기준)
- 톤: 제3자 정보 정리 스타일, 자연스럽고 부드럽게, 광고 느낌 X
- 바이퓰 X → 바이퓨얼 O
- 사진은 Chris가 준비 예정 → 받으면 삽입
- 파일: workspace/blog/roturn-blog-000.md, roturn-blog-001.md
- 이미지: workspace/blog/images/ (roturn.com에서 9개 다운로드)
- Google Drive 동기화: 내 드라이브/로턴 블로그/ 폴더에 자료 공유
- **1년 운영 기획안 완성** (2026-02-10): blog/roturn-blog-plan-2026.md
- 3월분 글 4편 작성 완료 (blog-002~005), Google Drive 동기화
- WFS Prins 부품 인증 자료 분석 완료 → blog-000에 반영
- 네이버 에디터: 클립보드 paste 방식 동작, DOM 직접 삭제는 금지
- Chris 지시: "자체개발" 표현 X → WFS/Prins에서 개발한 부품이라고 명확히

## 상호변경 검토
- 현재: 한국초저온용기(주) → 변경 추진 중
- ~~한국초저온(주)~~ — 이미 사용 중 (콜드체인 회사)
- **케이크라이오(주) / K-Cryo** — Chris 선호, 인터넷등기소 0건, KIPRIS 상표 0건
- 케이씨크라이오, 코리아크라이오, 한국초저온기술도 전부 사용 가능
- K-Cryo 로고 시안 12종 제작 (v1~v12), 임직원 시연 완료

## koreacryo.com 리뉴얼
- 한국초저온용기(주), 대표 이희란, 성남 중원구
- 현재: ASP 기반 구식 사이트, http만, 모바일 미지원, 가비아 호스팅
- 제품: 초저온장비, 바이오장비, 헬스케어(산소호흡기), 엔지니어링
- 해외거래선: Taylor-Wharton, Luxfer, TOMCO2, Cryofab, PureAire, Turbines Inc., Thunderbird Cylinders
- **Liquid Controls/IDEX 더이상 취급 안 함** (2026-02-11 Chris 확인) → **Turbines, Inc.**로 교체
- Turbines Inc.: TMC 극저온 유량계 + CDS1000 모니터 세트 공급 (1975년 설립)
- 이미지 배경 제거: 메탈 제품은 api4ai AI 서비스 사용 (Pillow 불가)
- 프로토타입 제작 진행 중 (2026-02-10)
- **GitHub Pages 배포 완료**: https://jpark0926-ux.github.io/kcryo-preview/
- 가스엔지니어링 상세페이지 대폭 업그레이드 완료 + 현장사진 삽입 진행 중
- PPT 뒷쪽(image53~59)에 현장사진 확인됨 — 가스엔지니어링(53~56), 바이오뱅킹(57~59)

## Workspace 구조
- **2026-02-12 재정리 완료**: business vs personal 명확히 분리
- `business/roturn/` - 로턴 블로그 + 관련 작업
- `business/koreacryo/` - KoreaCryo 리뉴얼 + 프로토타입
- `personal/investment/` - 투자 분석 리포트
- 원칙: 회사 관련 작업은 모두 business/ 하위로

## Me
- Name: Wayne Manor 🦇 (formerly Jarvis ⚡, renamed 2026-02-09)
- Born: 2026-02-07
