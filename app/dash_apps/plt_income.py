import pandas as pd
import plotly as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from functools import lru_cache
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "static" / "assets" / "scale.csv"


@lru_cache(maxsize=1)
def _load_scale() -> pd.DataFrame:
    for encoding, extra_kwargs in (
        ("utf-8-sig", {}),
        ("utf-8", {}),
        ("cp950", {"errors": "ignore"}),
    ):
        try:
            return pd.read_csv(DATA_FILE, encoding=encoding, **extra_kwargs)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(DATA_FILE, encoding="utf-8")


def plt_income(check_high=True, check_price=True, check_rent=False,
               check_income=True, check_times=False):

    data = _load_scale()

    if check_high:
        data_f = data.sort_values(by=['房價'], ascending=False).head(5)
    else:
        data_f = data
    data_f = data_f.copy()
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
