#!/bin/bash
#
# SETUP REAL-TIME POLLERS - Gmail + Calendar 자동화
# cron으로 15분마다 이메일, 30분마다 캘린더 체크
#

WORKSPACE="/Users/roturnjarvis/.openclaw/workspace"
LOGS_DIR="$WORKSPACE/logs"

echo "=========================================="
echo "🔗 REAL-TIME POLLER SETUP"
echo "=========================================="
echo ""

# 1. 로그 디렉토리 생성
mkdir -p "$LOGS_DIR"
echo "✓ Logs directory: $LOGS_DIR"

# 2. Python 스크립트 확인
if [ ! -f "$WORKSPACE/scripts/gmail_poller.py" ]; then
    echo "✗ gmail_poller.py not found!"
    exit 1
fi

if [ ! -f "$WORKSPACE/scripts/calendar_poller.py" ]; then
    echo "✗ calendar_poller.py not found!"
    exit 1
fi

echo "✓ Poller scripts found"

# 3. 실행 권한 부여
chmod +x "$WORKSPACE/scripts/gmail_poller.py"
chmod +x "$WORKSPACE/scripts/calendar_poller.py"
echo "✓ Scripts made executable"

# 4. 현재 crontab 백업
echo ""
echo "📋 Current crontab:"
crontab -l 2>/dev/null | head -20 || echo "(empty)"

# 5. 새 cron job 추가
echo ""
echo "➕ Adding new cron jobs..."

# 임시 파일에 cron job 작성
CRON_FILE=$(mktemp)

# 기존 crontab 복사
crontab -l 2>/dev/null > "$CRON_FILE" || echo "# Digital Chris Poller Jobs" > "$CRON_FILE"

# Digital Chris 주석 추가
if ! grep -q "Digital Chris Auto Polling" "$CRON_FILE"; then
    echo "" >> "$CRON_FILE"
    echo "# Digital Chris Auto Polling - $(date)" >> "$CRON_FILE"
    
    # Gmail poller: 15분마다
    echo "*/15 * * * * cd $WORKSPACE && /usr/local/bin/python3 scripts/gmail_poller.py --once >> $LOGS_DIR/gmail_poller.log 2>&1" >> "$CRON_FILE"
    
    # Calendar poller: 30분마다  
    echo "*/30 * * * * cd $WORKSPACE && /usr/local/bin/python3 scripts/calendar_poller.py --once >> $LOGS_DIR/calendar_poller.log 2>&1" >> "$CRON_FILE"
    
    # Daily summary: 매일 08:00
    echo "0 8 * * * cd $WORKSPACE && /usr/local/bin/python3 scripts/task_notifier.py >> $LOGS_DIR/task_summary.log 2>&1" >> "$CRON_FILE"
    
    # crontab 적용
    crontab "$CRON_FILE"
    echo "✓ Cron jobs added"
else
    echo "⚠ Cron jobs already exist, skipping"
fi

rm "$CRON_FILE"

# 6. 결과 확인
echo ""
echo "=========================================="
echo "📋 Updated crontab:"
echo "=========================================="
crontab -l | grep -A5 "Digital Chris"

echo ""
echo "=========================================="
echo "✅ SETUP COMPLETE"
echo "=========================================="
echo ""
echo "📊 Polling Schedule:"
echo "  • Gmail:     Every 15 minutes"
echo "  • Calendar:  Every 30 minutes"
echo "  • Summary:   Daily at 08:00"
echo ""
echo "📁 Log files:"
echo "  • $LOGS_DIR/gmail_poller.log"
echo "  • $LOGS_DIR/calendar_poller.log"
echo "  • $LOGS_DIR/task_summary.log"
echo ""
echo "🔍 Manual test:"
echo "  python3 scripts/gmail_poller.py --once"
echo "  python3 scripts/calendar_poller.py --once"
echo ""
echo "🛑 To remove:"
echo "  crontab -e  # and delete Digital Chris lines"
echo ""
