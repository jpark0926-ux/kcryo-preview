#!/bin/bash
# 핫토픽 모니터링 시스템 설정 (랭킹 기반)

echo "🔥 커뮤니티 핫토픽 모니터링 설정"
echo "================================"

# 기존 크론 제거 (키워드 기반)
echo "🗑️  기존 키워드 모니터링 제거..."
crontab -l 2>/dev/null | grep -v "leejaemyung-monitor" | crontab -

# 필요한 패키지 확인
echo "📦 패키지 확인..."
python3 -c "import requests, bs4" 2>/dev/null || {
    echo "필요한 패키지 설치 중..."
    pip3 install requests beautifulsoup4 --break-system-packages
}

# 로그 디렉토리
mkdir -p /Users/roturnjarvis/.openclaw/workspace/logs

# 환경변수 안내
echo ""
echo "⚙️  텔레그램 설정 (선택):"
echo "   export TELEGRAM_BOT_TOKEN='your_token'"
echo "   export TELEGRAM_CHAT_ID='6948605509'"
echo ""

# Cron job 추가 (랭킹 기반)
echo "⏰ Cron 설정 (1시간마다)..."
CRON_CMD="0 * * * * cd /Users/roturnjarvis/.openclaw/workspace && /usr/local/bin/python3 scripts/hot-topics-monitor.py >> logs/hot-topics-cron.log 2>&1"

(crontab -l 2>/dev/null | grep -v "hot-topics-monitor"; echo "$CRON_CMD") | crontab -

echo "✅ Cron 설정 완료"

echo ""
echo "🚀 테스트 실행..."
cd /Users/roturnjarvis/.openclaw/workspace
/usr/local/bin/python3 scripts/hot-topics-monitor.py

echo ""
echo "================================"
echo "설정 완료!"
echo ""
echo "📊 모니터링 대상:"
echo "   • 클리앙 (추천/조회수 순)"
echo "   • 뽐뿌 (조회수 순)"
echo "   • 더쿠 (인기글)"
echo "   • 딴지일보 (조회수 순)"
echo ""
echo "🎯 기준: 조회수 500+ 또는 댓글 5+"
echo "⏰ 주기: 1시간마다"
echo "📝 로그: logs/hot_topics_monitor.log"
echo ""
echo "📋 수동 실행:"
echo "   python3 scripts/hot-topics-monitor.py"
