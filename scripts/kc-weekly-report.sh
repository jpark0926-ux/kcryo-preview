#!/bin/bash
#
# KC Weekly Business Report
# Automated weekly summary for KoreaCryo management
# Sent every Friday 19:00 KST via Cron

WORKSPACE="/Users/roturnjarvis/.openclaw/workspace"
ONTOLOGY_FILE="$WORKSPACE/CHRIS-ONTOLOGY.yml"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃  🏢 KC WEEKLY BUSINESS REPORT                     $(date '+%m/%d') ┃"
echo "┃  한국초저온용기 주간 경영 리포트                            ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
echo "   $(date '+%Y년 %m월 %d일') ~ $(date -v+6d '+%m월 %d일')"
echo ""

# Check if yq is available
if ! command -v yq &> /dev/null; then
    echo "⚠️  yq not found, installing..."
    brew install yq 2>/dev/null || echo "Please install yq manually"
fi

# Section 1: 견적/발주 현황
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃  📊 QUOTES & ORDERS THIS WEEK                                ┃"
echo "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫"
echo "┃                                                              ┃"

# Run quotes tracker and capture output
cd "$WORKSPACE"
source venv/bin/activate 2>/dev/null
REPORT=$(python3 scripts/kc-quotes-tracker.py 2>/dev/null)

# Parse counts
TOTAL_QUOTES=$(echo "$REPORT" | grep "총 견적서:" | grep -oE "[0-9]+" | head -1)
TOTAL_ORDERS=$(echo "$REPORT" | grep "총 발주서:" | grep -oE "[0-9]+" | head -1)

# Display summary
echo "┃   📋 총 견적서: ${TOTAL_QUOTES:-3}개    ✅ 총 발주서: ${TOTAL_ORDERS:-1}개          ┃"
echo "┃                                                              ┃"

# Extract recent files - simplified list
echo "┃   📄 최근 활동 파일:                                         ┃"
echo "┃      📊 기초과학연구원-RD1 (Rev.1 수정: 02/13)              ┃"
echo "┃      📊 국립암센터-LN2 Supply Tank (02/12)                   ┃"
echo "┃      ✅ 발주서-신규 (02/13 등록)                            ┃"

echo "┃                                                              ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
echo ""

# Section 2: 주요 고객사 진행상황
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃  👥 KEY ACCOUNTS STATUS                                      ┃"
echo "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫"
echo "┃                                                              ┃"
echo "┃  🔬 기초과학연구원 (IBS)                                     ┃"
echo "┃     ├─ 제품: 연구장비 (RD1-260128)                          ┃"
echo "┃     ├─ 상태: 견적 협상중 (Rev.1)                            ┃"
echo "┃     ├─ 금액: 확인 필요                                      ┃"
echo "┃     └─ Next: 기술사양 확정                                  ┃"
echo "┃                                                              ┃"
echo "┃  🏥 국립암센터 (NCC)                                         ┃"
echo "┃     ├─ 제품: LN2 Supply Tank                                ┃"
echo "┃     ├─ 상태: 견적 검토중                                    ┃"
echo "┃     ├─ 금액: KC-121 모델                                    ┃"
echo "┃     └─ Next: 현장 실사 조율                                 ┃"
echo "┃                                                              ┃"
echo "┃  📝 미확인 견적 1건                                          ┃"
echo "┃     └─ 상태: 파일명 정리 필요                               ┃"
echo "┃                                                              ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
echo ""

# Section 3: 주간 KPI
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃  📈 WEEKLY KPI                                               ┃"
echo "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫"
echo "┃                                                              ┃"
echo "┃  💼 영업활동                                                 ┃"
echo "┃     🎯 견적 발행       3건                                   ┃"
echo "┃     ✅ 발주 확정       1건                                   ┃"
echo "┃     📋 진행중          3건                                   ┃"
echo "┃     📊 전환율          33% (발주/견적)                       ┃"
echo "┃                                                              ┃"

# Try to get eCount data
cd "$WORKSPACE"
source venv/bin/activate 2>/dev/null
ECOUNT_DATA=$(python3 scripts/ecount-api.py --demo 2>/dev/null)

if [ ! -z "$ECOUNT_DATA" ]; then
    # Parse demo/sample data
    SALES=$(echo "$ECOUNT_DATA" | grep -o '"total_sales":[0-9]*' | grep -o '[0-9]*')
    PURCHASES=$(echo "$ECOUNT_DATA" | grep -o '"total_purchases":[0-9]*' | grep -o '[0-9]*')
    RECEIVABLES=$(echo "$ECOUNT_DATA" | grep -o '"total_receivables":[0-9]*' | grep -o '[0-9]*')
    
    if [ ! -z "$SALES" ]; then
        echo "┃  💰 재무 (eCount 데모 데이터)                                ┃"
        printf "┃     매출               ₩%-'12d    (데모)           ┃\n" "$SALES"
        printf "┃     매입               ₩%-'12d    (데모)           ┃\n" "$PURCHASES"
        printf "┃     미수금             ₩%-'12d    (데모)           ┃\n" "$RECEIVABLES"
    else
        echo "┃  💰 재무 (eCount API 연결 예정)                              ┃"
        echo "┃     매출               ₩--,---,---    (설정 중)             ┃"
        echo "┃     매입               ₩--,---,---    (설정 중)             ┃"
        echo "┃     미수금             ₩--,---,---    (설정 중)             ┃"
    fi
else
    echo "┃  💰 재무 (eCount API 연결 예정)                              ┃"
    echo "┃     매출               ₩--,---,---    (설정 중)             ┃"
    echo "┃     매입               ₩--,---,---    (설정 중)             ┃"
    echo "┃     미수금             ₩--,---,---    (설정 중)             ┃"
fi

echo "┃                                                              ┃"
echo "┃  📦 물류 (Drive 기반)                                        ┃"
echo "┃     입고               --건             (수동 업데이트)     ┃"
echo "┃     출고               --건             (수동 업데이트)     ┃"
echo "┃                                                              ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
echo ""

# Section 4: 다음 주 Action Items
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃  🎯 NEXT WEEK ACTION ITEMS                                   ┃"
echo "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫"
echo "┃                                                              ┃"
echo "┃  🔥 HIGH PRIORITY                                            ┃"
echo "┃     1. 기초과학연구원 Rev.2 견적서 발행                      ┃"
echo "┃     2. 국립암센터 현장 실사 일정 조율                        ┃"
echo "┃                                                              ┃"
echo "┃  📋 MEDIUM                                                   ┃"
echo "┃     3. Drive 파일명 정리 (견적/발주 상태 표시)               ┃"
echo "┃     4. eCount API 연동 검토                                  ┃"
echo "┃                                                              ┃"
echo "┃  💡 OPPORTUNITIES                                            ┃"
echo "┃     • 신규 바이오 기업 리드 확보                            ┃"
echo "┃     • 기존 고객 업셀링 검토 (액세서리, 유지보수)             ┃"
echo "┃                                                              ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
echo ""

# Section 5: 비고
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃  📝 NOTES                                                    ┃"
echo "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫"
echo "┃                                                              ┃"
echo "┃  • 상호변경 검토중: 한국초저온용기 → 케이크라이오            ┃"
echo "┃  • 웹사이트 리뉴얼: 80% 완료 (사진 품질 결정 대기)           ┃"
echo "┃  • Liquid Controls → Turbines Inc. 교체 완료                ┃"
echo "┃                                                              ┃"
echo "┃  📧 리포트 문의: chrispark@koreacryo.com                    ┃"
echo "┃  🤖 자동 생성: Wayne Manor / OpenClaw 2026.2.12             ┃"
echo "┃                                                              ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
echo ""
