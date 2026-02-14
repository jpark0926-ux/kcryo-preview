#!/bin/bash
# 크론 설정 스크립트 - 터미널에서 직접 실행

echo "🔧 크론 설정 시작..."

# 기존 크론 백업
crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null
echo "✅ 기존 크론 백업 완료"

# 새 크론 내용
cat > /tmp/new_cron.txt << 'EOF'
# OpenClaw 자동화 작업
# 1시간마다 보안 모니터링
0 * * * * /Users/roturnjarvis/.openclaw/workspace/scripts/security-monitor.sh >> /Users/roturnjarvis/.openclaw/workspace/logs/security-monitor.log 2>&1

# 1시간마다 핫토픽 모니터링  
0 * * * * cd /Users/roturnjarvis/.openclaw/workspace && export TELEGRAM_BOT_TOKEN='8551723387:AAGbR3Sqg8SFFGw_16iIqQd1WjdkCTVcjAw' && export TELEGRAM_CHAT_ID='6948605509' && /usr/local/bin/python3 scripts/hot-topics-monitor.py >> logs/hot-topics-cron.log 2>&1
EOF

# 적용
crontab /tmp/new_cron.txt

echo "✅ 크론 설정 완료!"
echo ""
echo "📋 설정된 작업:"
crontab -l | grep -v "^#"
echo ""
echo "⏰ 다음 실행: 정각마다 (17:00, 18:00, 19:00...)"
