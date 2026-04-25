# -*- coding: utf-8 -*-
"""Trade Log 페이지"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
from config.settings import TRADE_LOG_PATH

def render():
    st.markdown("## 📋 Trade Log")

    if not TRADE_LOG_PATH.exists():
        st.info("아직 거래 내역이 없습니다. 봇을 실행하면 여기에 기록됩니다.")
        return

    df = pd.read_csv(TRADE_LOG_PATH)
    if df.empty:
        st.info("거래 내역 없음"); return

    sells = df[df['action']=='SELL'].copy() if 'action' in df.columns else pd.DataFrame()

    # 요약 KPI
    if not sells.empty and 'pnl' in sells.columns:
        total_pnl = sells['pnl'].sum()
        win_rate  = (sells['pnl']>0).mean()*100
        avg_pnl   = sells['pnl'].mean()
        c1,c2,c3,c4 = st.columns(4)
        with c1: st.metric("총 손익",f"{total_pnl:+,.0f}원",
                            delta="수익" if total_pnl>0 else "손실")
        with c2: st.metric("승률",f"{win_rate:.1f}%")
        with c3: st.metric("평균 손익",f"{avg_pnl:+,.0f}원")
        with c4: st.metric("총 거래",f"{len(sells)}회")

        # 손익 히스토그램
        fig = px.histogram(sells, x='pnl', nbins=20,
            color_discrete_sequence=['#58a6ff'],
            title='거래별 손익 분포')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(13,17,23,0.8)', font_color='#e6edf3',
            margin=dict(t=40,b=30,l=40,r=10))
        st.plotly_chart(fig, use_container_width=True)

    # 전체 거래 테이블
    st.markdown("#### 거래 내역 전체")
    st.dataframe(df.sort_values('date',ascending=False).head(200),
                 use_container_width=True, hide_index=True)

    # CSV 다운로드
    st.download_button("📥 CSV 다운로드", df.to_csv(index=False).encode('utf-8-sig'),
                       file_name="trade_log.csv", mime="text/csv")
