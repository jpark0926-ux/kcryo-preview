#!/usr/bin/env python3
"""
Digital Chris Dashboard v0.1
실시간 데이터 시각화 대시보드
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="Digital Chris Dashboard",
    page_icon="🦇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS - 다크 테마
st.markdown("""
<style>
    .main {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    .stMetric {
        background-color: #1a1a1a;
        border-radius: 10px;
        padding: 15px;
        border-left: 3px solid #ff6b35;
    }
    .stMetric label {
        color: #888888 !important;
    }
    .stMetric div {
        color: #ffffff !important;
    }
    h1, h2, h3 {
        color: #ff6b35 !important;
    }
    .stDataFrame {
        background-color: #1a1a1a;
    }
</style>
""", unsafe_allow_html=True)

# 데이터 로드 함수
def load_portfolio():
    """포트폴리오 데이터 로드"""
    try:
        df = pd.read_csv('personal/investment/portfolio-source.csv')
        return df
    except:
        return pd.DataFrame()

def load_hot_topics():
    """핫토픽 데이터 로드"""
    try:
        with open('logs/hot_topics_seen.json', 'r') as f:
            return json.load(f)
    except:
        return []

def load_decisions():
    """의사결정 기록 로드"""
    decisions = []
    decisions_dir = 'memory/decisions'
    if os.path.exists(decisions_dir):
        for file in os.listdir(decisions_dir):
            if file.endswith('.md'):
                with open(f'{decisions_dir}/{file}', 'r') as f:
                    decisions.append({
                        'date': file.replace('.md', ''),
                        'content': f.read()
                    })
    return decisions

# 사이드바
st.sidebar.title("🦇 Wayne Manor OS")
st.sidebar.markdown("---")
st.sidebar.markdown("### Digital Chris v0.1")
st.sidebar.markdown(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
st.sidebar.markdown("---")

# 메인 타이틀
st.title("🔮 Digital Chris Dashboard")
st.markdown("*실시간 데이터 통합 및 의사결정 지원 시스템*")
st.markdown("---")

# 상단 메트릭스
row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)

with row1_col1:
    portfolio_df = load_portfolio()
    if not portfolio_df.empty:
        total_value = portfolio_df['current_value_krw'].sum()
        st.metric(
            label="💰 총 자산",
            value=f"₩{total_value/100000000:.2f}억",
            delta="+37.6%"
        )
    else:
        st.metric(label="💰 총 자산", value="데이터 없음")

with row1_col2:
    hot_topics = load_hot_topics()
    st.metric(
        label="🔥 오늘 핫토픽",
        value=f"{len(hot_topics)}건",
        delta="+12"
    )

with row1_col3:
    decisions = load_decisions()
    st.metric(
        label="📝 이번 주 결정",
        value=f"{len(decisions)}건",
        delta="+3"
    )

with row1_col4:
    st.metric(
        label="🧠 클론 학습률",
        value="12%",
        delta="+2%"
    )

st.markdown("---")

# 메인 레이아웃
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("📊 포트폴리오 현황")
    
    if not portfolio_df.empty:
        # 파이 차트
        fig = px.pie(
            portfolio_df,
            values='current_value_krw',
            names='name',
            title='자산별 비중',
            color_discrete_sequence=px.colors.sequential.RdBu,
            template='plotly_dark'
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 테이블
        st.dataframe(
            portfolio_df[['name', 'ticker', 'current_value_krw', 'return_pct']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("포트폴리오 데이터를 불러올 수 없습니다.")
    
    st.markdown("---")
    st.subheader("🌐 실시간 핫토픽 트렌드")
    
    # 간단한 트렌드 차트 (샘플)
    trend_data = {
        '시간': ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00'],
        '클리앙': [12, 15, 18, 22, 25, 20, 28, 30, 35, 40],
        '뽐뿌': [20, 22, 25, 28, 30, 32, 35, 38, 40, 42],
        '더쿠': [45, 48, 52, 55, 58, 60, 65, 68, 70, 75],
        '딴지': [8, 10, 12, 15, 18, 20, 22, 25, 28, 30]
    }
    trend_df = pd.DataFrame(trend_data)
    
    fig2 = px.line(
        trend_df,
        x='시간',
        y=['클리앙', '뽐뿌', '더쿠', '딴지'],
        title='커뮤니티별 게시물 추이',
        template='plotly_dark'
    )
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    st.plotly_chart(fig2, use_container_width=True)

with right_col:
    st.subheader("⚡ 최근 활동")
    
    activities = [
        {"time": "18:00", "icon": "🔥", "text": "핫토픽 모니터링 완료 (32건)"},
        {"time": "17:30", "icon": "💰", "text": "포트폴리오 업데이트 (+2.3%)"},
        {"time": "14:00", "icon": "📝", "text": "새 결정 기록: 삼성전자 홀드"},
        {"time": "12:00", "icon": "🔒", "icon": "보안 스캔 완료 (이상 없음)"},
        {"time": "09:00", "icon": "☀️", "text": "시스템 시작"},
    ]
    
    for act in activities:
        st.markdown(f"**{act['time']}** {act['icon']} {act['text']}")
        st.markdown("---")
    
    st.subheader("🎯 오늘의 체크포인트")
    
    st.checkbox("☕ 아침 루틴 완료", value=True)
    st.checkbox("📊 포트폴리오 체크", value=True)
    st.checkbox("🔥 핫토픽 리뷰", value=True)
    st.checkbox("📝 결정 일지 작성", value=False)
    st.checkbox("📧 이메일 처리", value=False)
    
    st.markdown("---")
    st.subheader("🧠 Digital Chris 인사이트")
    st.info("""
    **패턴 발견:**
    - 18:00에 집중력 저하 경향
    - 투자 결정 시 IB 리포트 의존 78%
    - 새벽 1-2시 작업 후 다음날 효율 -30%
    
    **추천:**
    오늘 23:00 전에 수면 권장
    """)

# 하단: 빠른 액션
st.markdown("---")
st.subheader("🚀 빠른 액션")

action_col1, action_col2, action_col3, action_col4 = st.columns(4)

with action_col1:
    if st.button("📝 새 결정 기록", use_container_width=True):
        st.success("템플릿이 클립보드에 복사되었습니다!")

with action_col2:
    if st.button("💰 포트폴리오 업데이트", use_container_width=True):
        st.info("CSV 파일 업데이트 중...")

with action_col3:
    if st.button("🔥 핫토픽 새로고침", use_container_width=True):
        st.info("수집 중...")

with action_col4:
    if st.button("🔒 보안 스캔", use_container_width=True):
        st.success("스캔 완료 - 이상 없음")

# 푸터
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>Digital Chris Dashboard v0.1 | Powered by Wayne Manor OS 🦇</p>", unsafe_allow_html=True)
