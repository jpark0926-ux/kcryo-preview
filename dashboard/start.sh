#!/bin/bash
# Digital Chris Dashboard 설치 및 실행 스크립트

echo "🦇 Digital Chris Dashboard 설치"
echo "================================"

# 가상환경 생성
cd /Users/roturnjarvis/.openclaw/workspace/dashboard
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
echo "📦 패키지 설치 중..."
pip install -r requirements.txt -q

# 실행
echo "🚀 대시보드 시작 중..."
echo "브라우저에서 http://localhost:8501 접속"
echo ""
echo "중지하려면 Ctrl+C"
echo "================================"

streamlit run app.py
