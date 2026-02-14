#!/bin/bash
# Digital Chris 전체 설정

echo "🦇 Digital Chris 설정 시작"
echo "=========================="

# 1. 결정 일지 디렉토리 생성
mkdir -p memory/decisions
mkdir -p logs
mkdir -p dashboard

# 2. 대시보드 의존성 설치
cd dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -q
echo "✅ 대시보드 패키지 설치 완료"

# 3. 크론 설정 (기존에 추가)
(crontab -l 2>/dev/null; echo "0 18 * * * /Users/roturnjarvis/.openclaw/workspace/scripts/digital-chris-collect.sh >> /Users/roturnjarvis/.openclaw/workspace/logs/digital-chris.log 2>&1") | crontab -
echo "✅ 데이터 수집 크론 설정 완료"

# 4. 샘플 결정 기록 생성
TODAY=$(date +%Y-%m-%d)
cat > memory/decisions/${TODAY}_sample.md << 'EOF'
# 의사결정 기록 샘플

## 메타데이터
- **날짜**: 2026-02-14
- **시간**: 20:15
- **결정 유형**: 시스템 개발
- **에너지 레벨**: 8/10
- **감정 상태**: 😊

---

## 상황
Digital Chris 프로젝트를 어디서부터 시작할지 결정해야 했음

## 선택
**Phase 0부터 시작**: 데이터 수집 + 간단한 시각화

## 근거
- 큰 그림은 알겠는데, 바로 3D UI는 무리
- 데이터 없이는 클론화 안 됨
- 빠른 피드백 루프가 중요

## 예상 결과
- 1주일 내에 데이터 패턴 확인 가능
- 1개월 후 첫 인사이트 도출
- 3개월 후 "Chris 같은" 추천 가능

## 태그
#DigitalChris #시스템설계 #데이터수집
EOF
echo "✅ 샘플 결정 기록 생성 완료"

echo ""
echo "=========================="
echo "🎉 설정 완료!"
echo ""
echo "다음 단계:"
echo "1. 터미널에서 ./dashboard/start.sh 실행"
echo "2. 브라우저에서 http://localhost:8501 접속"
echo "3. 매일 결정이 있을 때마다 templates/decision-journal.md 사용"
echo "4. 파일은 memory/decisions/에 YYYY-MM-DD_번호.md 형식으로 저장"
echo "=========================="
