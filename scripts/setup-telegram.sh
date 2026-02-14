#!/bin/bash
# 핫토픽 모니터링 텔레그램 설정

echo "🔥 텔레그램 설정"
echo "==============="

# 환경변수 설정
export TELEGRAM_BOT_TOKEN='8551723387:AAGbR3Sqg8SFFGw_16iIqQd1WjdkCTVcjAw'
export TELEGRAM_CHAT_ID='6948605509'

# 홈 디렉토리에 .zshrc 또는 .bash_profile에 추가
SHELL_RC="$HOME/.zshrc"
if [ ! -f "$SHELL_RC" ]; then
    SHELL_RC="$HOME/.bash_profile"
fi

# 기존 설정 제거
if grep -q "TELEGRAM_BOT_TOKEN" "$SHELL_RC" 2>/dev/null; then
    sed -i '' '/TELEGRAM_BOT_TOKEN/d' "$SHELL_RC" 2>/dev/null || sed -i '/TELEGRAM_BOT_TOKEN/d' "$SHELL_RC" 2>/dev/null
fi
if grep -q "TELEGRAM_CHAT_ID" "$SHELL_RC" 2>/dev/null; then
    sed -i '' '/TELEGRAM_CHAT_ID/d' "$SHELL_RC" 2>/dev/null || sed -i '/TELEGRAM_CHAT_ID/d' "$SHELL_RC" 2>/dev/null
fi

# 새 설정 추가
echo "" >> "$SHELL_RC"
echo "# Telegram Hot Topics Bot" >> "$SHELL_RC"
echo "export TELEGRAM_BOT_TOKEN='8551723387:AAGbR3Sqg8SFFGw_16iIqQd1WjdkCTVcjAw'" >> "$SHELL_RC"
echo "export TELEGRAM_CHAT_ID='6948605509'" >> "$SHELL_RC"

echo "✅ 환경변수 설정 완료: $SHELL_RC"

# Cron 설정
echo ""
echo "⏰ Cron 설정 (1시간마다)..."
CRON_CMD="0 * * * * cd /Users/roturnjarvis/.openclaw/workspace && export TELEGRAM_BOT_TOKEN='8551723387:AAGbR3Sqg8SFFGw_16iIqQd1WjdkCTVcjAw' && export TELEGRAM_CHAT_ID='6948605509' && /usr/local/bin/python3 scripts/hot-topics-monitor.py >> logs/hot-topics-cron.log 2>&1"

# 기존 크론 제거 후 새로 추가
(crontab -l 2>/dev/null | grep -v "hot-topics-monitor"; echo "$CRON_CMD") | crontab -

echo "✅ Cron 설정 완료"

# 테스트 메시지 별도 스크립트
cat > /tmp/test_telegram.sh << 'EOF'
#!/bin/bash
export TELEGRAM_BOT_TOKEN='8551723387:AAGbR3Sqg8SFFGw_16iIqQd1WjdkCTVcjAw'
export TELEGRAM_CHAT_ID='6948605509'

curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -d "chat_id=$TELEGRAM_CHAT_ID" \
  -d "text=🔥 <b>핫토픽 알림 시스템 연결 완료!</b>%0A%0A1시간마다 커뮤니티 핫토픽을 별사드립니다.%0A• 클리앙 TOP 5%0A• 뽐뿌 TOP 5%0A• 더쿠 TOP 5%0A• 딴지 TOP 5%0A%0A<i>처음 알림은 1시간 내에 도착합니다.</i>" \
  -d "parse_mode=HTML" \
  -d "disable_web_page_preview=true"
EOF

chmod +x /tmp/test_telegram.sh
echo ""
echo "📱 테스트 메시지 전송 중..."
/tmp/test_telegram.sh

echo ""
echo "==============="
echo "✅ 설정 완료!"
echo ""
echo "📋 요약:"
echo "   • Bot: @ChrisJarvisHotTopicbot"
echo "   • Chat ID: 6948605509"
echo "   • 주기: 1시간마다"
echo "   • 첫 알림: 1시간 내 도착"
echo ""
echo "💡 수동 테스트:"
echo "   python3 scripts/hot-topics-monitor.py"
