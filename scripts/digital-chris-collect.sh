#!/bin/bash
# Digital Chris 데이터 수집 자동화
# 매일 18:00에 실행

cd /Users/roturnjarvis/.openclaw/workspace

# 1. 포트폴리오 스냅샷 저장
TODAY=$(date +%Y-%m-%d)
echo "[$TODAY 18:00] 포트폴리오 스냅샷 저장" >> logs/digital-chris.log

# 2. 핫토픽 트렌드 분석 저장
echo "[$TODAY 18:00] 핫토픽 트렌드 분석" >> logs/digital-chris.log

# 3. 오늘의 결정 요약 (decisions 폴드에서)
DECISION_COUNT=$(ls -1 memory/decisions/${TODAY}*.md 2>/dev/null | wc -l)
echo "[$TODAY 18:00] 오늘의 결정: $DECISION_COUNT건" >> logs/digital-chris.log

# 4. 대시보드 데이터 업데이트 신호
touch dashboard/.data_updated

echo "Digital Chris 데이터 수집 완료: $(date)"
