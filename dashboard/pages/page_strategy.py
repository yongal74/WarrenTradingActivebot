# -*- coding: utf-8 -*-
"""Strategy Factory 페이지 — 종목별 전략 신호 현황"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config.assets import ALL_ASSETS, PRIMARY_STRATEGY
from core.strategy_factory import get_all_signals
from data.data_loader import load

STRATEGY_DESC = {
    'S01_EMA9_21':    'EMA 9/21 크로스',
    'S02_EMA20_50':   'EMA 20/50 크로스',
    'S03_GoldenCross':'골든/데드크로스 50/200',
    'S04_SuperTrend': 'SuperTrend 추세',
    'S05_HullMA':     'Hull MA 크로스',
    'S06_Ichimoku':   '일목균형표 클라우드',
    'S07_RSI_Trend':  'RSI>50 추세',
    'S08_RSI_Rev':    'RSI 평균회귀',
    'S09_MACD':       'MACD 시그널 크로스',
    'S10_MACDHist':   'MACD 히스토그램',
    'S11_BB_Break':   'BB 상단 돌파',
    'S12_BB_Rev':     'BB 평균회귀',
    'S13_ATR_Break':  'ATR 변동성 돌파',
    'S14_Donchian':   'Donchian 채널 돌파',
    'S15_ZScore':     'Z-Score 평균회귀',
    'S16_SMA_Rev':    'SMA50 이탈 회귀',
    'S17_FVG':        'Fair Value Gap (ICT)',
    'S18_MSB':        'Market Structure Break',
    'S19_Monday':     '월요일 레인지 전략',
    'S20_InsideBar':  'Inside Bar 돌파',
    'S21_Engulfing':  '불리시 엔글핑',
    'S22_VolBreak':   '거래량 돌파',
    'S23_EMA_Ribbon': 'EMA 리본 정배열',
    'S24_CHoCH':      'CHoCH 추세전환',
    'S25_PinBar':     '핀바 망치형',
}

def render():
    st.markdown("## ⚙️ Strategy Factory")
    st.markdown("백테스팅 검증 25개 전략의 현재 신호 현황을 종목별로 확인합니다.")

    # 종목 선택
    ticker_list = list(ALL_ASSETS.keys())
    selected = st.selectbox("종목 선택", ticker_list,
                            format_func=lambda t: f"{t} — {ALL_ASSETS[t]['name']}")

    asset  = ALL_ASSETS[selected]
    market = asset['market']

    df = load(selected, market)
    if df is None or len(df) < 60:
        st.error("데이터 로드 실패"); return

    # 신호 계산
    all_sigs = get_all_signals(df)
    price    = float(df['Close'].iloc[-1])
    pstrat   = PRIMARY_STRATEGY[selected]

    # 요약 정보
    buy_cnt = sum(1 for v in all_sigs.values() if v==1)
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("현재가", f"{price:,.2f}")
    with c2: st.metric("매수 신호", f"{buy_cnt}/25")
    with c3: st.metric("관망 신호", f"{25-buy_cnt}/25")
    with c4: st.metric("1순위 전략", pstrat,
                        delta="매수" if all_sigs.get(pstrat,0)==1 else "관망")

    st.markdown("---")

    # 전략 신호 테이블
    rows = []
    for sname, sig in sorted(all_sigs.items()):
        is_primary = (sname == pstrat)
        rows.append({
            '순위': '⭐ 1순위' if is_primary else '',
            '전략코드': sname,
            '전략명': STRATEGY_DESC.get(sname, sname),
            '신호': '📈 매수' if sig==1 else '⏸ 관망',
            '상태': '활성' if sig==1 else '비활성',
        })
    df_t = pd.DataFrame(rows)

    # 정렬: 매수 신호 먼저
    df_t = df_t.sort_values(['신호'], ascending=False).reset_index(drop=True)
    st.dataframe(df_t, use_container_width=True, hide_index=True,
                 column_config={'순위': st.column_config.TextColumn(width='small'),
                                '신호': st.column_config.TextColumn(width='small')})

    # 신호 히트맵 (전체 종목)
    st.markdown("---")
    st.markdown("#### 🗺️ 전체 종목 × 전략 신호 히트맵")

    with st.spinner("히트맵 계산 중..."):
        heatmap_data = {}
        for t, ast in ALL_ASSETS.items():
            df_t2 = load(t, ast['market'])
            if df_t2 is None or len(df_t2) < 60: continue
            sigs = get_all_signals(df_t2)
            heatmap_data[t] = sigs

    if heatmap_data:
        strategies = list(STRATEGY_DESC.keys())
        tickers    = list(heatmap_data.keys())
        z = [[heatmap_data[t].get(s,0) for s in strategies] for t in tickers]

        fig = go.Figure(go.Heatmap(
            z=z, x=strategies, y=tickers,
            colorscale=[[0,'#21262d'],[1,'#3fb950']],
            showscale=False, zmin=0, zmax=1,
        ))
        fig.update_layout(
            height=max(300, len(tickers)*28),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e6edf3',
            margin=dict(t=10,b=80,l=80,r=10),
            xaxis=dict(tickangle=-45, color='#8b949e'),
            yaxis=dict(color='#8b949e'),
        )
        st.plotly_chart(fig, use_container_width=True)
