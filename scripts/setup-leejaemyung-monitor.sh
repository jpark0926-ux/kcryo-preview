#!/bin/bash
# 이재명 모니터링 시스템 설정 스크립트

echo "🤖 이재명 커뮤니티 모니터링 설정"
echo "================================"

# 필요한 패키지 설치 확인
echo "📦 필요한 패키지 확인..."
python3 -c "import requests, bs4, feedparser" 2>/dev/null || {
    echo "필요한 패키지 설치 중..."
    pip3 install requests beautifulsoup4 feedparser
}

# 로그 디렉토리 생성
mkdir -p /Users/roturnjarvis/.openclaw/workspace/logs

# 환경변수 설정 안내
echo ""
echo "⚙️  환경변수 설정 필요:"
echo "   export TELEGRAM_BOT_TOKEN='your_bot_token'"
echo "   export TELEGRAM_CHAT_ID='your_chat_id'"
echo ""
echo "💡 텔레그램 봇 만들기:"
echo "   1. @BotFather 검색 → /newbot"
echo "   2. 봇 이름 입력 → 토큰 받기"
echo "   3. @userinfobot 검색 → 채팅ID 확인"
echo ""

# Cron job 추가
echo "⏰ Cron job 설정 (15분마다 실행)..."
CRON_CMD="*/15 * * * * cd /Users/roturnjarvis/.openclaw/workspace && /usr/local/bin/python3 scripts/leejaemyung-monitor.py >> logs/monitor-cron.log 2>&1"

# 기존 크론 확인
crontab -l 2>/dev/null | grep -q "leejaemyung-monitor" && {
    echo "⚠️  이미 설정되어 있음"
} || {
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    echo "✅ Cron job 추가 완료"
}

echo ""
echo "🚀 테스트 실행..."
cd /Users/roturnjarvis/.openclaw/workspace
/usr/local/bin/python3 scripts/leejaemyung-monitor.py

echo ""
echo "================================"
echo "설정 완료!"
echo "• 실행 주기: 15분마다"
echo "• 로그 위치: logs/community_monitor.log"
echo "• 알림: 텔레그램 (설정 후)"
echo ""
echo "📋 수동 실행:"
echo "   python3 scripts/leejaemyung-monitor.py"
