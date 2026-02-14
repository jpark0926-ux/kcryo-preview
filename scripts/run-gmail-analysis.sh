#!/bin/bash
# Gmail 자동 분석 - 매일 18:00 및 21:00에 실행

cd /Users/roturnjarvis/.openclaw/workspace

# Gmail 분석 실행
python3 scripts/gmail-analyzer.py >> logs/gmail-analyzer.log 2>&1

# 결과가 있으면 텔레그램 알림 (선택적)
if [ -f logs/gmail-analyzer.log ]; then
    NEW_DECISIONS=$(grep -c "✅ 저장" logs/gmail-analyzer.log | tail -1)
    if [ "$NEW_DECISIONS" -gt 0 ]; then
        echo "$NEW_DECISIONS개의 새로운 결정/액션 아이템이 이메일에서 추출됨" >> logs/gmail-analyzer.log
    fi
fi

echo "Gmail 분석 완료: $(date)"
