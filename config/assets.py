# -*- coding: utf-8 -*-
"""
백테스팅 결과 기반 종목별 전략 배정
(거래수>=5, PF<100 필터 통과한 신뢰 가능 전략만)
"""

# 해외 종목 (yfinance)
OVERSEAS_ASSETS = {
    'JEPI':  {'name':'JEPI(JPM커버드콜)',       'strategies':['S12_BB_Rev','S07_RSI_Trend','S19_Monday']},
    'JEPQ':  {'name':'JEPQ(JPM나스닥커버드콜)', 'strategies':['S07_RSI_Trend','S02_EMA20_50','S01_EMA9_21']},
    'QDVO':  {'name':'QDVO(Amplify배당커버드콜)','strategies':['S24_CHoCH','S01_EMA9_21','S06_Ichimoku']},
    'JFLI':  {'name':'JFLI(JPM나스닥프리미엄)', 'strategies':['S07_RSI_Trend','S24_CHoCH','S17_FVG']},
    'ULTY':  {'name':'ULTY(YieldMax울트라)',     'strategies':['S25_PinBar','S06_Ichimoku','S05_HullMA']},
    'QQQI':  {'name':'QQQI(NEOS나스닥100)',     'strategies':['S01_EMA9_21','S07_RSI_Trend','S06_Ichimoku']},
    'NVDA':  {'name':'NVDA(엔비디아)',           'strategies':['S02_EMA20_50','S01_EMA9_21','S07_RSI_Trend']},
    'PLTR':  {'name':'PLTR(팔란티어)',           'strategies':['S02_EMA20_50','S17_FVG','S07_RSI_Trend']},
    'QQQ':   {'name':'QQQ(나스닥100)',           'strategies':['S14_Donchian','S07_RSI_Trend','S01_EMA9_21']},
    'SOXX':  {'name':'SOXX(반도체ETF)',          'strategies':['S02_EMA20_50','S01_EMA9_21','S14_Donchian']},
    'SPY':   {'name':'SPY(S&P500)',              'strategies':['S01_EMA9_21','S06_Ichimoku','S07_RSI_Trend']},
    'TSLA':  {'name':'TSLA(테슬라)',             'strategies':['S09_MACD','S10_MACDHist','S02_EMA20_50']},
}

# 국내 ETF (FinanceDataReader)
KR_ASSETS = {
    '475080':{'name':'KODEX테슬라커버드콜채권',      'strategies':['S07_RSI_Trend','S06_Ichimoku','S01_EMA9_21']},
    '498400':{'name':'KODEX200타겟위클리커버드콜',   'strategies':['S01_EMA9_21','S17_FVG','S23_EMA_Ribbon']},
    '472150':{'name':'TIGER배당커버드콜액티브',       'strategies':['S17_FVG','S06_Ichimoku','S01_EMA9_21']},
}

# 전체 통합
ALL_ASSETS = {}
for t, v in OVERSEAS_ASSETS.items():
    ALL_ASSETS[t] = {**v, 'market': 'US'}
for t, v in KR_ASSETS.items():
    ALL_ASSETS[t] = {**v, 'market': 'KR'}

# Forward Testing: 종목별 1순위 전략만 사용
PRIMARY_STRATEGY = {t: v['strategies'][0] for t, v in ALL_ASSETS.items()}
