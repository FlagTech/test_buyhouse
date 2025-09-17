import pandas as pd
import plotly as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from functools import lru_cache
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "static" / "assets" / "date_data.csv"


@lru_cache(maxsize=1)
def _load_dataset() -> pd.DataFrame:
    """Load the Plotly trend dataset once and cache it in-memory."""
    for encoding, extra_kwargs in (
        ("utf-8-sig", {}),
        ("utf-8", {}),
        ("cp950", {"errors": "ignore"}),
    ):
        try:
            return pd.read_csv(DATA_FILE, encoding=encoding, **extra_kwargs)
        except UnicodeDecodeError:
            continue
    # Final attempt so the underlying exception surfaces for easier debugging.
    return pd.read_csv(DATA_FILE, encoding="utf-8")


def plt_trend(city="臺北市", check_price=True, check_rent=True,
              check_index=False, A_price=True, A_rent=True):

    data = _load_dataset()

    price = city + "_房價"
    rent = city + "_租金"

    # 畫出折線圖

    fig_line = make_subplots(specs=[[{"secondary_y": True}]])

    # 檢查列名是否存在，如果不存在則用默認值
    available_columns = data.columns.tolist()

    if check_index is True and '物價指數' in available_columns:
        fig_line.add_trace(
            go.Scatter(x=data['季度'], y=data['物價指數'], name='物價指數'),
            secondary_y=True,)

    if A_price is True and '房價(元/坪)' in available_columns:
        fig_line.add_trace(
            go.Scatter(x=data['季度'], y=data['房價(元/坪)'],
                      name='全台平均房價(元/坪)'),
            secondary_y=False,)

    if A_rent is True and '租金(元/坪)' in available_columns:
        fig_line.add_trace(
            go.Scatter(x=data['季度'], y=data['租金(元/坪)'],
                      name='全台平均租金(元/坪)'),
            secondary_y=True,)

    if check_price is True and price in available_columns:
        fig_line.add_trace(
            go.Scatter(x=data['季度'], y=data[price],
                      name=price + '(元/坪)'),
            secondary_y=False,)

    if check_rent is True and rent in available_columns:
        fig_line.add_trace(
            go.Scatter(x=data['季度'], y=data[rent],
                      name=rent + '(元/坪)'),
            secondary_y=True,)


    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,  # 只設定高度，讓寬度自動適應
        margin=dict(l=50, r=50, t=50, b=50),  # 設定邊距
        legend=dict(
            x=0, y=1,  # 圖例位置
            traceorder="normal",
            font=dict(
                family="Montserrat",
                size=12,
                color="black"),
            bgcolor="LightSteelBlue",  # 邊框顏色
            bordercolor="Blue",
            borderwidth=2))

    fig_line.update_xaxes(nticks=10)


    graphJSON = plt.io.to_json(fig_line)

    return graphJSON
