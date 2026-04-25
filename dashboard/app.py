# -*- coding: utf-8 -*-
"""
WarrenTradingActivebot — Streamlit 메인 대시보드
AI Pathways "Claude Will Change Trading Forever" 스타일
실행: streamlit run dashboard/app.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="WarrenTradingActivebot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 다크테마 CSS (AI Pathways 스타일) ─────────────────────────
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp { background-color: #0d1117; color: #e6edf3; }
    section[data-testid="stSidebar"] { background-color: #161b22; }

    /* 메트릭 카드 */
    .metric-card {
        background: linear-gradient(135deg, #1c2128, #21262d);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 6px 0;
    }
    .metric-value { font-size: 28px; font-weight: 700; }
    .metric-label { font-size: 13px; color: #8b949e; margin-top: 4px; }
    .positive { color: #3fb950; }
    .negative { color: #f85149; }
    .neutral  { color: #e3b341; }

    /* 헤더 */
    .main-header {
        background: linear-gradient(90deg, #238636, #1a7f37);
        border-radius: 10px; padding: 16px 24px; margin-bottom: 20px;
        display: flex; align-items: center; gap: 12px;
    }
    .header-title { font-size: 24px; font-weight: 700; color: white; }
    .header-sub   { font-size: 13px; color: #b3f0c5; }

    /* 신호 배지 */
    .signal-buy  { background:#238636; color:white; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }
    .signal-flat { background:#30363d; color:#8b949e; padding:3px 10px; border-radius:12px; font-size:12px; }

    /* 전략 테이블 */
    .stDataFrame { border-radius: 8px; }
    div[data-testid="stMetric"] { background:#1c2128; border-radius:8px; padding:12px; }

    /* 버튼 */
    .stButton>button { background:#238636; color:white; border:none; border-radius:6px; font-weight:600; }
    .stButton>button:hover { background:#2ea043; }
</style>
""", unsafe_allow_html=True)

# ── 사이드바 네비게이션 ────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📈 WarrenTradingActivebot")
    st.markdown("---")
    page = st.radio(
        "Navigation",
        ["🏠 Overview", "🧠 Market Brain", "⚙️ Strategy Factory",
         "📊 Backtest Results", "🔬 Asset Analysis", "📋 Trade Log", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown(f"**모드:** `PAPER TRADING`")
    st.markdown(f"**업데이트:** {datetime.now().strftime('%H:%M:%S')}")
    if st.button("🔄 새로고침"):
        st.rerun()

# ── 페이지 라우팅 ─────────────────────────────────────────────
if   "Overview"  in page: from dashboard.pages import page_overview;  page_overview.render()
elif "Market"    in page: from dashboard.pages import page_brain;     page_brain.render()
elif "Strategy"  in page: from dashboard.pages import page_strategy;  page_strategy.render()
elif "Backtest"  in page: from dashboard.pages import page_backtest;  page_backtest.render()
elif "Analysis"  in page: from dashboard.pages import page_analysis;  page_analysis.render()
elif "Trade Log" in page: from dashboard.pages import page_trades;    page_trades.render()
elif "Settings"  in page: from dashboard.pages import page_settings;  page_settings.render()
