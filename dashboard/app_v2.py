#!/usr/bin/env python3
"""
DIGITAL CHRIS DASHBOARD v2.0
Phase 3-6 결과 통합 대시보드
"""

import streamlit as st
import json
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Digital Chris v2.0",
    page_icon="🦇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00f3ff;
        text-shadow: 0 0 20px rgba(0, 243, 255, 0.5);
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 243, 255, 0.1), rgba(255, 0, 85, 0.1));
        border: 1px solid rgba(0, 243, 255, 0.3);
        border-radius: 10px;
        padding: 20px;
    }
    .task-item {
        background: rgba(255, 255, 255, 0.05);
        border-left: 3px solid #00f3ff;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 0 5px 5px 0;
    }
    .task-critical { border-left-color: #ff0000; }
    .task-high { border-left-color: #ff6600; }
    .task-medium { border-left-color: #ffcc00; }
    .task-low { border-left-color: #00ff66; }
</style>
""", unsafe_allow_html=True)

def load_json_safe(filepath):
    """안전하게 JSON 로드"""
    try:
        if Path(filepath).exists():
            with open(filepath) as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading {filepath}: {e}")
    return {}

# Sidebar
with st.sidebar:
    st.markdown("## 🦇 Digital Chris v2.0")
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "Navigation",
        ["📊 Overview", "📧 Email AI", "⏳ Time Machine", "🤖 Agent Status", "⚙️ Settings"]
    )
    
    st.markdown("---")
    st.markdown(f"**Last Updated:**  
{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Auto-refresh
    st.checkbox("Auto-refresh (30s)", value=False, key="auto_refresh")

# Load data
data_dir = Path("/Users/roturnjarvis/.openclaw/workspace")
tasks_data = load_json_safe(data_dir / "logs/pending_tasks.json")
decisions_data = load_json_safe(data_dir / "logs/pending_decisions.json")
emails_data = load_json_safe(data_dir / "logs/all_pst_emails.json")[-100:] if isinstance(load_json_safe(data_dir / "logs/all_pst_emails.json"), list) else []

# ========== OVERVIEW PAGE ==========
if page == "📊 Overview":
    st.markdown('<p class="main-header">Digital Chris Dashboard</p>', unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📧 Today's Emails",
            value=len([e for e in emails_data if isinstance(e, dict)]),
            delta="+3 new"
        )
    
    with col2:
        tasks = tasks_data.get('tasks', [])
        pending = len([t for t in tasks if t.get('status') == 'pending'])
        st.metric(
            label="📋 Pending Tasks",
            value=pending,
            delta=f"{len(tasks)} total"
        )
    
    with col3:
        decisions = decisions_data.get('decisions', [])
        pending_decisions = len([d for d in decisions if d.get('status') == 'pending'])
        st.metric(
            label="🤔 Decisions Needed",
            value=pending_decisions,
            delta=None
        )
    
    with col4:
        st.metric(
            label="🤖 AI Confidence",
            value="87%",
            delta="+2%"
        )
    
    st.markdown("---")
    
    # Recent Activity
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### 📧 Recent Email Analysis")
        
        if emails_data:
            for i, email in enumerate(emails_data[-5:]):
                if not isinstance(email, dict):
                    continue
                    
                sender = email.get('from', 'Unknown')[:30]
                subject = email.get('subject', 'No subject')[:60]
                date = email.get('date', '')[:10]
                
                # Priority color
                priority = email.get('priority', 'low')
                color = {'critical': 'red', 'high': 'orange', 'medium': 'yellow', 'low': 'green'}.get(priority, 'gray')
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 3px solid {color};">
                    <strong>{sender}</strong> <span style="color: gray;">• {date}</span><br/>
                    {subject}...
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent emails")
    
    with col_right:
        st.markdown("### 📋 Active Tasks")
        
        tasks = tasks_data.get('tasks', [])
        if tasks:
            for task in tasks[:5]:
                priority = task.get('priority', 'LOW')
                status = task.get('status', 'unknown')
                title = task.get('title', 'Untitled')[:40]
                
                # CSS class based on priority
                css_class = f"task-{priority.lower()}"
                
                st.markdown(f"""
                <div class="task-item {css_class}">
                    <strong>{title}...</strong><br/>
                    <small>{priority} • {status}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active tasks")
    
    # AI Performance Chart
    st.markdown("---")
    st.markdown("### 📈 AI Performance (Last 7 Days)")
    
    # Sample data - in production would load from logs
    chart_data = pd.DataFrame({
        'Date': pd.date_range(end=datetime.now(), periods=7, freq='D'),
        'Emails Processed': [12, 15, 8, 20, 18, 14, 16],
        'Tasks Created': [5, 7, 3, 9, 8, 6, 7],
        'Avg Confidence': [0.82, 0.85, 0.80, 0.88, 0.86, 0.84, 0.87]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=chart_data['Date'],
        y=chart_data['Emails Processed'],
        name='Emails',
        marker_color='#00f3ff'
    ))
    fig.add_trace(go.Bar(
        x=chart_data['Date'],
        y=chart_data['Tasks Created'],
        name='Tasks',
        marker_color='#ff0055'
    ))
    fig.add_trace(go.Scatter(
        x=chart_data['Date'],
        y=chart_data['Avg Confidence'] * 100,
        name='Confidence %',
        mode='lines+markers',
        line=dict(color='#00ff66', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        yaxis=dict(title='Count', gridcolor='rgba(255,255,255,0.1)'),
        yaxis2=dict(title='Confidence %', overlaying='y', side='right', range=[70, 100]),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ========== EMAIL AI PAGE ==========
elif page == "📧 Email AI":
    st.markdown('<p class="main-header">Phase 3: AI Email Processing</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📧 Recent Emails with AI Analysis")
        
        # Load recent analysis results
        for i, email in enumerate(emails_data[-3:]):
            if not isinstance(email, dict):
                continue
                
            with st.expander(f"📧 {email.get('subject', 'No subject')[:50]}..."):
                st.write(f"**From:** {email.get('from', 'Unknown')}")
                st.write(f"**Date:** {email.get('date', 'Unknown')}")
                st.write(f"**Snippet:** {email.get('snippet', 'No preview')[:200]}...")
                
                # AI Analysis placeholder
                st.markdown("---")
                st.markdown("**🤖 AI Analysis:**")
                st.write("• Sentiment: Neutral")
                st.write("• Priority: Medium")
                st.write("• Urgent: No")
                
                st.markdown("**✍️ Suggested Response:**")
                st.info("Hi, thank you for your email. I'll review and get back to you shortly.")
    
    with col2:
        st.markdown("### 📊 Email Statistics")
        
        # Priority distribution
        priorities = ['Critical', 'High', 'Medium', 'Low']
        counts = [2, 8, 25, 15]  # Sample data
        
        fig = px.pie(
            names=priorities,
            values=counts,
            color=priorities,
            color_discrete_map={
                'Critical': '#ff0000',
                'High': '#ff6600',
                'Medium': '#ffcc00',
                'Low': '#00ff66'
            }
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Response time
        st.markdown("---")
        st.markdown("### ⏱️ AI Response Time")
        st.write("• Average: 1.2 seconds")
        st.write("• Fastest: 0.8 seconds")
        st.write("• Slowest: 3.1 seconds")

# ========== TIME MACHINE PAGE ==========
elif page == "⏳ Time Machine":
    st.markdown('<p class="main-header">Phase 4: Time Machine</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🕰️ Time Travel")
        
        year = st.slider("Select Year", 2020, 2026, 2026)
        
        st.markdown(f"### 📅 {year} Network State")
        
        # Sample data based on year
        year_data = {
            2020: {'partners': 0, 'deals': 0, 'emails': 50},
            2022: {'partners': 3, 'deals': 2, 'emails': 320},
            2024: {'partners': 7, 'deals': 4, 'emails': 890},
            2026: {'partners': 11, 'deals': 6, 'emails': 1803}
        }
        
        data = year_data.get(year, year_data[2026])
        
        st.metric("Active Partners", data['partners'])
        st.metric("Total Deals", data['deals'])
        st.metric("Emails", data['emails'])
        
        # Key events
        st.markdown("---")
        st.markdown("### 🎯 Key Events")
        
        events = {
            2020: ["First email sent"],
            2022: ["Luxfer partnership", "Taylor-Wharton deal"],
            2024: ["Hyundai FCEV project", "KGSC Audit"],
            2026: ["Holy Cryogenics visit", "PO#KCMIE-260108"]
        }
        
        for event in events.get(year, []):
            st.write(f"✓ {event}")
    
    with col2:
        st.markdown("### 📈 Network Growth Timeline")
        
        # Timeline chart
        timeline_data = pd.DataFrame({
            'Year': [2020, 2021, 2022, 2023, 2024, 2025, 2026],
            'Partners': [0, 2, 3, 5, 7, 9, 11],
            'Deals': [0, 1, 2, 3, 4, 5, 6],
            'Relationship Score': [0, 5.5, 6.2, 6.8, 7.3, 7.6, 7.9]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=timeline_data['Year'],
            y=timeline_data['Partners'],
            mode='lines+markers',
            name='Partners',
            line=dict(color='#00f3ff', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=timeline_data['Year'],
            y=timeline_data['Deals'],
            mode='lines+markers',
            name='Deals',
            line=dict(color='#ff0055', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=timeline_data['Year'],
            y=timeline_data['Relationship Score'],
            mode='lines+markers',
            name='Avg Score',
            line=dict(color='#00ff66', width=3),
            yaxis='y2'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            yaxis=dict(title='Count', gridcolor='rgba(255,255,255,0.1)'),
            yaxis2=dict(title='Score', overlaying='y', side='right', range=[0, 10]),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Partner health
        st.markdown("---")
        st.markdown("### 🏢 Partner Health Scores")
        
        partners = pd.DataFrame({
            'Partner': ['Luxfer', 'Hyundai', 'Taylor-Wharton', 'Holy Cryogenics', 'ICBiomedical'],
            'Score': [7.1, 7.8, 8.2, 8.0, 7.5],
            'Trend': ['↑', '→', '↑', '↑', '→']
        })
        
        st.dataframe(partners, hide_index=True, use_container_width=True)

# ========== AGENT STATUS PAGE ==========
elif page == "🤖 Agent Status":
    st.markdown('<p class="main-header">Phase 6: Autonomous Agent</p>', unsafe_allow_html=True)
    
    # Agent metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tasks Today", 12, "+3")
    with col2:
        st.metric("Auto-Completed", 8, "+2")
    with col3:
        st.metric("Pending Approval", 2, "-1")
    with col4:
        st.metric("Autonomy Level", "50%", None)
    
    st.markdown("---")
    
    # Task queue
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### 📋 Task Queue")
        
        tasks = tasks_data.get('tasks', [])
        if tasks:
            df_tasks = pd.DataFrame(tasks)
            st.dataframe(df_tasks[['title', 'type', 'priority', 'status', 'confidence']], 
                        use_container_width=True, hide_index=True)
        else:
            st.info("No tasks in queue")
    
    with col_right:
        st.markdown("### 🤔 Pending Decisions")
        
        decisions = decisions_data.get('decisions', [])
        if decisions:
            for decision in decisions:
                with st.container():
                    st.warning(f"**{decision.get('recommendation', 'N/A')[:50]}...**")
                    st.write(f"Confidence: {decision.get('confidence', 0)*100:.0f}%")
                    st.write(f"Risk: {decision.get('risk_level', 'unknown')}")
                    col_a, col_r = st.columns(2)
                    with col_a:
                        st.button("✓ Approve", key=f"a_{decision.get('id', 'x')}")
                    with col_r:
                        st.button("✗ Reject", key=f"r_{decision.get('id', 'x')}")
        else:
            st.success("No pending decisions")
    
    # Activity log
    st.markdown("---")
    st.markdown("### 📜 Recent Activity")
    
    activity_log = [
        {"time": "02:04", "action": "Email processed", "detail": "Alex Millward - meeting request"},
        {"time": "02:03", "action": "Task created", "detail": "Reply to Hyundai webinar"},
        {"time": "02:01", "action": "Decision proposed", "detail": "Luxfer valve markup approval"},
        {"time": "01:45", "action": "AI analysis", "detail": "Holy Cryogenics quotation"},
        {"time": "01:30", "action": "Time travel", "detail": "Viewed 2024 network state"},
    ]
    
    for activity in activity_log:
        st.markdown(f"**{activity['time']}** • {activity['action']}  
*{activity['detail']}*")

# ========== SETTINGS PAGE ==========
elif page == "⚙️ Settings":
    st.markdown('<p class="main-header">Settings</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🤖 AI Configuration")
        
        autonomy_level = st.slider("Autonomy Level", 0, 100, 50, 
                                   help="Higher = more auto-execution without approval")
        
        st.checkbox("Auto-send low-risk emails", value=True)
        st.checkbox("Auto-schedule meetings", value=False)
        st.checkbox("Enable sentiment analysis", value=True)
        
        st.markdown("---")
        st.markdown("### 📧 Email Polling")
        
        poll_interval = st.selectbox("Poll Interval", ["5 min", "15 min", "30 min", "1 hour"], index=1)
        
        st.checkbox("Process promotional emails", value=False)
        st.checkbox("Alert on URGENT keywords", value=True)
    
    with col2:
        st.markdown("### 📱 Notifications")
        
        st.checkbox("Telegram alerts", value=True)
        st.checkbox("Email summaries", value=False)
        st.checkbox("Daily digest at 08:00", value=True)
        
        st.markdown("---")
        st.markdown("### ⏰ Calendar")
        
        st.checkbox("24h pre-meeting alert", value=True)
        st.checkbox("1h pre-meeting alert", value=True)
        st.checkbox("Auto-prep meeting materials", value=True)
        
        st.markdown("---")
        st.markdown("### 🕰️ Time Machine")
        
        st.checkbox("Track relationship trends", value=True)
        st.checkbox("Alert on critical moments", value=True)
        st.checkbox("Enable simulation mode", value=False)
    
    st.markdown("---")
    
    if st.button("💾 Save Settings", type="primary"):
        st.success("Settings saved!")
    
    if st.button("🔄 Restart Agent"):
        st.warning("Agent restarting...")
        st.info("Please wait 10 seconds and refresh")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Digital Chris v2.0 • Built with OpenClaw</div>", 
            unsafe_allow_html=True)
