# -*- coding: utf-8 -*-
"""Overview 페이지 — 포트폴리오 요약 + 실시간 신호"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

def render():
    # 헤더
    st.markdown("""
    <div style='background:linear-gradient(90deg,#238636,#1a7f37);border-radius:10px;
    padding:16px 24px;margin-bottom:20px;'>
    <span style='font-size:24px;font-weight:700;color:white;'>📈 WarrenTradingActivebot</span><br>
    <span style='font-size:13px;color:#b3f0c5;'>Forward Testing Mode — Paper Trading Active</span>
    </div>
    """, unsafe_allow_html=True)

    # 데이터 로드
    try:
        from core.forward_tester import ForwardTester
        ft = ForwardTester()
        status = ft.get_status()
        port   = status['portfolio']
        prices = status['prices']
        signals= status['signals']
        positions = status['positions']
    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")
        _render_demo()
        return

    # ── 핵심 KPI 카드 ──────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)

    tv  = port['total_value']
    ret = port['return_pct']
    mdd = port['mdd_pct']
    wr  = port['win_rate']

    color_ret = "positive" if ret >= 0 else "negative"
    color_mdd = "positive" if mdd >= -5 else ("neutral" if mdd >= -10 else "negative")

    with c1:
        st.markdown(f"""<div class='metric-card'>
        <div class='metric-value'>{tv:,.0f}</div>
        <div class='metric-label'>총 자산 (원)</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='metric-card'>
        <div class='metric-value {color_ret}'>{ret:+.2f}%</div>
        <div class='metric-label'>수익률</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='metric-card'>
        <div class='metric-value {color_mdd}'>{mdd:+.2f}%</div>
        <div class='metric-label'>MDD</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class='metric-card'>
        <div class='metric-value'>{port['open_positions']}</div>
        <div class='metric-label'>오픈 포지션</div></div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class='metric-card'>
        <div class='metric-value positive'>{wr:.1f}%</div>
        <div class='metric-label'>승률 ({port['total_trades']}거래)</div></div>""",
        unsafe_allow_html=True)

    st.markdown("---")

    # ── 실시간 신호 테이블 ─────────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("#### 📡 실시간 전략 신호")
        from config.assets import ALL_ASSETS, PRIMARY_STRATEGY

        rows = []
        for ticker, asset in ALL_ASSETS.items():
            price  = prices.get(ticker, 0)
            asigs  = signals.get(ticker, {})
            pstrat = PRIMARY_STRATEGY[ticker]
            psig   = asigs.get(pstrat, 0)
            buy_cnt= sum(1 for v in asigs.values() if v==1)
            total_s= len(asigs)

            rows.append({
                '종목': f"{ticker}",
                '이름': asset['name'],
                '현재가': f"{price:,.2f}" if price else '-',
                '1순위전략': pstrat,
                '신호': '📈 매수' if psig==1 else '⏸ 관망',
                '동조전략': f"{buy_cnt}/{total_s}",
                '포지션': '✅ 보유' if ticker in positions else '—',
            })

        df_sig = pd.DataFrame(rows)
        st.dataframe(df_sig, use_container_width=True, hide_index=True,
                     column_config={
                         '신호': st.column_config.TextColumn(width='small'),
                         '포지션': st.column_config.TextColumn(width='small'),
                     })

    with col_right:
        st.markdown("#### 💼 오픈 포지션")
        if positions:
            pos_rows = []
            for ticker, pos in positions.items():
                cur_price = prices.get(ticker, pos['entry_price'])
                pnl_pct   = (cur_price - pos['entry_price']) / pos['entry_price'] * 100
                pos_rows.append({
                    '종목': ticker,
                    '진입가': f"{pos['entry_price']:,.2f}",
                    '현재가': f"{cur_price:,.2f}",
                    'PnL': f"{pnl_pct:+.1f}%",
                    '전략': pos['strategy'],
                })
            df_pos = pd.DataFrame(pos_rows)
            st.dataframe(df_pos, use_container_width=True, hide_index=True)
        else:
            st.info("현재 보유 포지션 없음")

        # 신호 분포 도넛차트
        if signals:
            buy_signals = sum(1 for asigs in signals.values()
                             for v in asigs.values() if v==1)
            flat_signals= sum(1 for asigs in signals.values()
                             for v in asigs.values() if v==0)
            fig = go.Figure(go.Pie(
                values=[buy_signals, flat_signals],
                labels=['매수 신호', '관망 신호'],
                hole=0.6,
                marker_colors=['#3fb950','#30363d'],
                textfont_size=13,
            ))
            fig.update_layout(
                showlegend=True, height=200,
                margin=dict(t=10,b=10,l=10,r=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e6edf3',
                legend=dict(font_color='#e6edf3'),
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── 누적 수익률 차트 ────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📈 누적 수익률 추이")
    try:
        from config.settings import TRADE_LOG_PATH
        if TRADE_LOG_PATH.exists():
            trades_df = pd.read_csv(TRADE_LOG_PATH, parse_dates=['date'])
            trades_df = trades_df.sort_values('date')
            trades_df['cum_pnl'] = trades_df['pnl'].cumsum()
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=trades_df['date'], y=trades_df['cum_pnl'],
                fill='tozeroy', name='누적 손익',
                line=dict(color='#3fb950', width=2),
                fillcolor='rgba(63,185,80,0.15)',
            ))
            fig2.update_layout(
                height=250, paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(13,17,23,0.8)',
                font_color='#e6edf3', showlegend=False,
                margin=dict(t=10,b=30,l=40,r=10),
                xaxis=dict(gridcolor='#21262d', color='#8b949e'),
                yaxis=dict(gridcolor='#21262d', color='#8b949e',
                           title='누적 손익 (원)'),
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("거래 내역이 없습니다. 봇을 실행하면 차트가 표시됩니다.")
    except Exception as e:
        st.info(f"차트 준비 중... ({e})")

def _render_demo():
    """데이터 없을 때 데모 화면"""
    st.info("📌 봇이 아직 실행되지 않았습니다. `python main.py` 를 실행하세요.")
    c1,c2,c3,c4,c5 = st.columns(5)
    for col, label, val in zip(
        [c1,c2,c3,c4,c5],
        ['총 자산','수익률','MDD','포지션','승률'],
        ['10,000,000','0.00%','0.00%','0','0.0%']
    ):
        with col:
            st.metric(label, val)
