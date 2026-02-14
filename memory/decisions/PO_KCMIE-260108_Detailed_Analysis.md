# PO#KCMIE-260108 - 심층 분석 보고서

**분석일**: 2026-02-14  
**분석자**: Wayne Manor 🦇  
**상태**: ✅ **주문 확정 / 진행 중**

---

## 📋 Executive Summary

| 항목 | 내용 |
|------|------|
| **PO 번호** | KCMIE-260108 rev.1 |
| **발주일** | 2026-01-08 (최초) → 2026-01-17 (최종 확정) |
| **납기 유형** | 60일 선적 (약 2026-03-17 이전) |
| **공급사** | Thunderbird Metals East (Metal Impact East LLC DBA) |
| **금액 추정** | Unknown (PDF 첨부, 다운로드 불가) |
| **주요 품목** | ME24 (Part Number 수정 이력 있음) |

---

## 🏢 공급사 프로필

### Thunderbird Metals East
- **법적명**: Metal Impact East LLC DBA Thunderbird Metals East
- **주소**: 235 Riverbend Road, Graham, NC 27253
- **업종**: 금속 가공/제조 (알루미늄 surcharges 언급으로 추정)
- **계열사**: Metal Impact (Tadeu Margaria)
- **Korea Cryo와의 관계**: 2025년부터 다수 PO 진행 (see PO History)

### 주요 담당자
| 이름 | 직책 | 연락처 | 역할 |
|------|------|--------|------|
| Vienna Coble | Senior CSR | vienna.coble@tbirdmfg.com | PO 전체 담당 |
| Tadeu Margaria | - | Tadeu.Margaria@metalimpact.com | Metal Impact 담당 |

---

## 📊 PO 이력 분석 (KCMIE 시리즈)

```
2025-03: PO#KCMIE-241218_MD15 (14개 메일) - 초기 거래 시작
2025-04: PO#KCMIE-250218 (11개 메일)  
2025-06: Certificate for PO#KCMIE-250218 (4개 메일)
2025-09: PO#KCMIE-250728_C020 (22개 메일) - 대규모
2025-11: Re: PO#KCMIE-250728_C020 (6개 메일)
2026-01: PO#KCMIE-260108 (12개 메일) ← 현재 주문
```

**패턴 분석:**
- 평균 PO당 10-15개 메일 스레드 (협상이 복잡함)
- 이혜용 책임매니저가 모든 PO 발주 담당
- Vienna Coble가 모든 OA(Order Acknowledgment) 발행
- 주로 Q1, Q3에 집중 발주 (분기별 구매 패턴)

---

## 📧 타임라인 상세 분석

### Phase 1: 초기 발주 (1/8)
- **시간**: 2026-01-08 15:29 KST
- **발신**: 이혜용 (Korea Cryo)
- **수신**: Tadeu Margaria (Metal Impact)
- **내용**: PO#KCMIE-260108 첨부, 확인 요청
- **첨부**: PO PDF (204.3 KB), 이미지 파일

### Phase 2: 협상/수정 (1/14-15)
- **주요 이슈**: ME24 Part Number 수정 필요
- **참여자**: Vienna Coble, Tadeu Margaria, 이혜용
- **CC**: Chris Park, 강대일, 정선희
- **이메일 횟수**: 5개 메일 (1/14 04:05 ~ 1/15 18:22)

### Phase 3: 일시 취소 (1/15 18:23)
- **액션**: 회수 메일 발송
- **원인 추정**: Part number 수정으로 인한 PO 재발행 필요
- **처리자**: 이혜용

### Phase 4: 최종 확정 (1/17 02:28)
- **OA 발행**: Vienna Coble
- **첨부**: 
  - PO#KCMIE-260108rev.1.pdf (204.6 KB)
  - 902121-E.pdf (494.9 KB) - 품목 상세 추정
  - 이미지 파일 5개 (제품 사진/도면 추정)
- **조건**: 
  - ✅ 주문 확정 (Order Acknowledged)
  - ⚠️ Aluminum surcharge 선적 시 적용
  - 🚫 60일 선적 윈도우 내 수정/취소 불가

---

## ⚠️ 리스크 및 주의사항

### 1. 가격 변동 리스크
- **Aluminum Surcharge**: 알루미늄 원자재 가격 변동에 따른 추가 비용
- **시점**: 선적 시 적용 (2026-03 중 예상)
- **대응**: 알루미늄 가격 모니터링 필요

### 2. 납기 리스크
- **Deadlin**: 60일 선적 (2026-03-17 전)
- **제약**: 60일 윈도우 내 수정/취소 불가
- **영향**: 태국 출장 중(2/17-23)에 문제 발생 시 대응 지연

### 3. 품목 리스크
- **ME24**: Part Number 수정 이력 존재
- **확인 필요**: 최종 rev.1의 품목 사양이 요구사항과 일치하는지

---

## 🎯 Action Items

### 즉시 필요 (D-1, 2/16까지)
- [ ] PO#KCMIE-260108rev.1.pdf 다운로드 및 품목/금액 확인
- [ ] ME24 품목 사양 최종 검증
- [ ] 알루미늄 가격 현황 체크 (surcharge 예상액)

### 태국 출장 중 모니터링 (2/17-23)
- [ ] 납기 일정 재확인 (3/17 선적 가능 여부)
- [ ] Thunderbird 측 연락처 확보 (긴급 연락용)
- [ ] 품질 이슈 발생 시 대응 방안

### 장기 관리
- [ ] PO 완료 후 supplier performance 평가
- [ ] 2026 Q2 추가 발주 계획 수립

---

## 🔗 관련 정보

### 연결된 Ontology Entities
```
Chris (참조)
  └── KoreaCryo
       └── 이혜용 (발주 담당)
       ├── 강대일 (영업팀, CC)
       ├── 정선희 (영업팀, CC)
       └── Thunderbird Metals (공급사)
            ├── Vienna Coble (담당자)
            └── Metal Impact (계열사)
```

### 관련 Decision Files
- `memory/decisions/2026-01-17_19ba1246_POKCMIE-260108.md`
- `memory/decisions/2026-01-17_gmail_19ba1246.md`
- `memory/decisions/2026-01-15_19bc0f77_회수_POKCMIE-260108.md`

---

## 📝 메모

**자동화 제안:**
- PO 발주 시 자동으로 OA 만료일 알림 설정
- Aluminum surcharge 변동률 임계값 알림 (예: ±10%)
- Supplier lead time 추적 시스템

**Pattern Recognition:**
- KCMIE 시리즈: Korea Cryo Metal Impact Equipment
- MD15, C020 접미사: 품목 카테고리 코드 추정
- 분기별 집중 발주 패턴 확인됨

---

**Report Generated**: 2026-02-14  
**Next Review**: 2026-02-17 (태국 출발 전)  
**Status**: 🟢 **ON TRACK**
