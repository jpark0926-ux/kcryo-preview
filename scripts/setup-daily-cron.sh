#!/bin/bash
# Setup daily morning summary via OpenClaw cron

echo "Setting up daily morning summary..."
echo "Every day at 09:00 KST, you'll get an automatic summary!"
echo ""
echo "Command to create cron job:"
echo ""
echo "openclaw cron add \\"
echo "  --schedule 'cron:0 9 * * * Asia/Seoul' \\"
echo "  --session isolated \\"
echo "  --task 'Read CHRIS-ONTOLOGY.yml and send daily summary with: priorities, blockers, portfolio highlights, and energy-optimized suggestion' \\"
echo "  --name 'Daily Morning Summary' \\"
echo "  --delivery announce"
