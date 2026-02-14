#!/bin/bash
# 보안 모니터링 Cron 설정

echo "🛡️  보안 모니터링 설정"
echo "===================="

# 1시간마다 보안 체크 + 매일 00:00 정상 보고
CRON_CMD="0 * * * * /Users/roturnjarvis/.openclaw/workspace/scripts/security-monitor.sh >> /Users/roturnjarvis/.openclaw/workspace/logs/security-monitor.log 2>&1"

# 기존 보안 모니터링 제거 후 추가
(crontab -l 2>/dev/null | grep -v "security-monitor"; echo "$CRON_CMD") | crontab -

echo "✅ Cron 설정 완료"
echo "   • 주기: 1시간마다"
echo "   • 로그: logs/security-monitor.log"
echo "   • 알림: Telegram (@ChrisJarvisHotTopicbot)"
echo ""

# 즉시 테스트
echo "🧪 즉시 테스트 실행..."
/Users/roturnjarvis/.openclaw/workspace/scripts/security-monitor.sh

echo ""
echo "💡 수동 실행:"
echo "   ./scripts/security-monitor.sh"
