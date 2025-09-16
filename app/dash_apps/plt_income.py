import pandas as pd

import plotly as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plt_income(check_high=True, check_price=True, check_rent=False,
               check_income=True, check_times=False):



    try:
        data = pd.read_csv("app/static/assets/scale.csv", encoding='utf-8-sig')
    except UnicodeDecodeError:
        try:
            data = pd.read_csv("app/static/assets/scale.csv", encoding='utf-8')
        except UnicodeDecodeError:
            data = pd.read_csv("app/static/assets/scale.csv", encoding='cp950', errors='ignore')

    if check_high:
        data_f = data.sort_values(by=['房價'], ascending=False)
        data_f = data_f.iloc[:5, :]
    else:
        data_f = data
    data_f['x'] = 0

    fig_bar = make_subplots(specs=[[{"secondary_y": True}]])
    fig_bar.add_trace(
        go.Bar(x=data_f['城市'], y=data_f['x']),
        secondary_y=True,)

    if check_price:
        fig_bar.add_trace(
            go.Bar(x=data_f['城市'], y=data_f['房價'], name='房價(元/坪)'),
            secondary_y=False,)
    if check_rent:
        fig_bar.add_trace(
            go.Bar(x=data_f['城市'], y=data_f['租金'], name='租金(元/坪)'),
            secondary_y=True,)

    if check_income:
        fig_bar.add_trace(
            go.Bar(x=data_f['城市'], y=data_f['月薪'], name='每月薪資'),
            secondary_y=True,)

    if check_times:
        fig_bar.add_trace(
            go.Bar(x=data_f['城市'], y=data_f['房價收入比(20坪)'], name='房價收入比(20坪)'),
            secondary_y=True,)

    fig_bar.update_layout(
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,  # 只設定高度
        margin=dict(l=40, r=40, t=50, b=80),  # 設定邊距，底部多留空間給標籤
        legend=dict(
            x=0, y=1,  # 圖例位置
            traceorder="normal",
            font=dict(
                family="Montserrat",
                size=10,  # 減小字體
                color="black"),
            bgcolor="LightSteelBlue",
            bordercolor="Blue",
            borderwidth=2))


    graphBAR = plt.io.to_json(fig_bar)

    return graphBAR



  