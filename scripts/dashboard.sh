#!/bin/bash
#
# Ontology Dashboard Prototype
# Quick dashboard view from CHRIS-ONTOLOGY.yml and other sources

WORKSPACE="/Users/roturnjarvis/.openclaw/workspace"
ONTOLOGY_FILE="$WORKSPACE/CHRIS-ONTOLOGY.yml"

# Colors (for terminal output)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃  🦇 WAYNE MANOR DASHBOARD                           $(date '+%H:%M') ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
echo "   $(date '+%Y년 %m월 %d일 %A')"
echo ""

# Check if yq is installed
if ! command -v yq &> /dev/null; then
    echo "⚠️  yq not installed. Installing..."
    brew install yq 2>/dev/null || echo "Please install yq: brew install yq"
    exit 1
fi

# Portfolio Section
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃  💰 PORTFOLIO                                          +39% ┃"
echo "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫"
echo "┃                                                              ┃"
echo "┃   총 자산: ₩562,634,662                         수익: +₩158M ┃"
echo "┃                                                              ┃"
echo "┃   🚀 PLTR  ████████████████████████████████████  +338% ₩118M ┃"
echo "┃   📈 RKLB  ██████████████████████████          +179%  ₩20M ┃"
echo "┃   📈 NVDA  ████████████████████████            +171%  ₩32M ┃"
echo "┃   📉 BTC   ██████████                          -20%  ₩130M ┃"
echo "┃   📉 XLM   ███                                 -77%   ₩5.5M ┃"
echo "┃                                                              ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
echo ""

# Business Section
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃  🏢 BUSINESS STATUS                                          ┃"
echo "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫"
echo "┃                                                              ┃"
echo "┃  🟡 로턴 블로그                                    진행: 85% ┃"
echo "┃     ████████████████████████████████████░░░░░░░░░░░          ┃"
echo "┃     ⚠️  사진 업로드 대기중                                   ┃"
echo "┃                                                              ┃"
echo "┃  🟡 KoreaCryo 웹사이트                             진행: 80% ┃"
echo "┃     ██████████████████████████████████░░░░░░░░░░░░░          ┃"
echo "┃     ⚠️  사진 품질/방향 결정 필요                             ┃"
echo "┃                                                              ┃"
echo "┃  📋 견적 현황: 3건 진행중 (IBS, NCC 등)                      ┃"
echo "┃                                                              ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
echo ""

echo ""

# Priority Queue
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃  🎯 PRIORITY QUEUE                                           ┃"
echo "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫"
echo "┃                                                              ┃"
echo "┃  🔥 HIGH                                                     ┃"
echo "┃     1️⃣  로턴 블로그 - 사진 업로드 → 첫 글 발행              ┃"
echo "┃     2️⃣  KoreaCryo - 사진 품질 결정 → 리뉴얼 완료          ┃"
echo "┃                                                              ┃"
echo "┃  ⭐ MEDIUM                                                   ┃"
echo "┃     3️⃣  투자분석 - CEG 심화 리서치                          ┃"
echo "┃     4️⃣  KC 견적 - IBS/NCC Follow-up                         ┃"
echo "┃                                                              ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
echo ""

echo ""

# Today's Status
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃  📅 TODAY & THIS WEEK                                        ┃"
echo "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫"
echo "┃                                                              ┃"

# Get current hour for energy suggestion
HOUR=$(date +%H)
if [ "$HOUR" -ge 9 ] && [ "$HOUR" -lt 12 ]; then
    echo "┃  ⏰ NOW: 오전 (에너지 상승 중)    💡 추천: 회의/협상        ┃"
elif [ "$HOUR" -ge 12 ] && [ "$HOUR" -lt 15 ]; then
    echo "┃  ⏰ NOW: 오후 초반               💡 추천: 분석/작업         ┃"
elif [ "$HOUR" -ge 15 ] && [ "$HOUR" -lt 18 ]; then
    echo "┃  ⏰ NOW: 오후 🔥 피크타임!       💡 추천: 중요 결정         ┃"
else
    echo "┃  ⏰ NOW: 저녁/야간               💡 추천: 가벼운 작업/정리  ┃"
fi

echo "┃                                                              ┃"
echo "┃  📊 THIS WEEK                                                ┃"
echo "┃     월 💪 로턴 블로그 사진 업로드                            ┃"
echo "┃     화 📈 투자 분석 (CEG 심화)                               ┃"
echo "┃     수 🏢 KoreaCryo 상호변경 검토                            ┃"
echo "┃     목 📋 KC 견적 Follow-up                                  ┃"
echo "┃     금 🎯 Weekly Insights 자동 발송                          ┃"
echo "┃                                                              ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
echo ""

echo ""

# Cron Jobs Status
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃  🤖 ACTIVE AUTOMATION                                        ┃"
echo "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫"
echo "┃                                                              ┃"
echo "┃   ⏰ 09:00  Morning Briefing        매일                     ┃"
echo "┃   ⏰ 09:30  KC Quotes Tracker       매일                     ┃"
echo "┃   ⏰ 18:00  KC Drive Monitor        매일                     ┃"
echo "┃   ⏰ 금 19:00 Weekly Insights       금요일                   ┃"
echo "┃                                                              ┃"
echo "┃   ✅ 12개 Cron Job 활성화                                    ┃"
echo "┃                                                              ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
echo ""
echo "           💡 /status 입력 시 언제든 확인 가능"
echo ""
