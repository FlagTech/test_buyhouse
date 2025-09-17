import pandas as pd
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Optional, Tuple

import plotly as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

DATA_ROOT = Path(__file__).resolve().parents[1] / "static" / "assets" / "data"
MAX_QUARTERS = 5

LOCATION = {
    '臺北市': 'a', '臺中市': 'b',
    '基隆市': 'c', '臺南市': 'd',
    '高雄市': 'e', '新北市': 'f',
    '宜蘭縣': 'g', '桃園市': 'h',
    '嘉義市': 'i', '新竹縣': 'j',
    '苗栗縣': 'k', '南投縣': 'm',
    '彰化縣': 'n', '新竹市': 'o',
    '雲林縣': 'p', '嘉義縣': 'q',
    '屏東縣': 't', '花蓮縣': 'u',
    '臺東縣': 'v', '金門': 'w',
    '澎湖縣': 'x'
}

DURATION = {
    '五年以下': (0, 50_000),
    '五年至十五年': (50_000, 150_000),
    '十五年至三十年': (150_000, 300_000),
    '三十年以上': (300_000, 1_000_000),
}

PRICE_TARGETS = {
    '房地(土地+建物)',
    '房地(土地+建物)+車位',
}

RENT_TARGETS = {
    '房地(土地+建物)',
    '房地(土地+建物)+車位',
    '租賃房屋',
    '租賃房屋+車位',
}


def _current_time_marker() -> int:
    return int(datetime.now().strftime("%Y%m%d")) - 19110000


def _recent_quarters(limit: int = MAX_QUARTERS) -> Tuple[str, ...]:
    if not DATA_ROOT.exists():
        return tuple()
    quarters = sorted(
        (p.name for p in DATA_ROOT.iterdir() if p.is_dir()),
        reverse=True,
    )
    return tuple(list(quarters)[:limit])


def _read_quarter_files(path: Path, pattern: str) -> list[pd.DataFrame]:
    frames: list[pd.DataFrame] = []
    for file in sorted(path.glob(pattern)):
        frames.append(pd.read_csv(file, low_memory=False))
    return frames


@lru_cache(maxsize=None)
def _load_city_frames(city_code: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    quarters = _recent_quarters()
    price_frames: list[pd.DataFrame] = []
    rent_frames: list[pd.DataFrame] = []

    for quarter in quarters:
        quarter_path = DATA_ROOT / quarter
        price_frames.extend(_read_quarter_files(quarter_path, f"{city_code}*a.csv"))
        rent_frames.extend(_read_quarter_files(quarter_path, f"{city_code}*c.csv"))

    price_df = pd.concat(price_frames, ignore_index=True) if price_frames else pd.DataFrame()
    rent_df = pd.concat(rent_frames, ignore_index=True) if rent_frames else pd.DataFrame()
    return price_df, rent_df


def _prepare_series(
    df: pd.DataFrame,
    allowed_targets: Iterable[str],
    building_type: str,
    year_range: Tuple[int, int],
    time_marker: int,
) -> pd.Series:
    if df.empty:
        return pd.Series(dtype="int64")

    filtered = df[df['交易標的'].isin(allowed_targets)].copy()
    if filtered.empty:
        return pd.Series(dtype="int64")

    filtered['建築完成年月'] = filtered['建築完成年月'].fillna('0500000')
    filtered['建築完成年月'] = pd.to_numeric(filtered['建築完成年月'], errors='coerce').fillna(500000).astype(int)
    filtered['屋齡'] = time_marker - filtered['建築完成年月']

    if '建物型態' not in filtered.columns:
        return pd.Series(dtype="int64")

    if building_type and '建物型態' in filtered.columns:
        filtered_by_type = filtered[filtered['建物型態'] == building_type]
        if not filtered_by_type.empty:
            filtered = filtered_by_type
    filtered = filtered[filtered['屋齡'].between(year_range[0], year_range[1])]
    filtered = filtered[filtered['屋齡'].between(year_range[0], year_range[1])]
    if filtered.empty:
        return pd.Series(dtype="int64")

    values = pd.to_numeric(filtered['單價元平方公尺'], errors='coerce')
    values = values[values > 0]
    if values.empty:
        return pd.Series(dtype="int64")

    values = (values / 0.3025).astype(int)
    return values.reset_index(drop=True)


def _mean_int(values: pd.Series) -> Optional[int]:
    if values.empty:
        return None
    return int(values.mean())


def _format_currency(value: Optional[int]) -> str:
    if value is None:
        return '資料不足'
    return f"${value}"


def _build_box(price_values: pd.Series, rent_values: pd.Series) -> go.Figure:
    fig_box = make_subplots(specs=[[{"secondary_y": True}]])

    if not price_values.empty:
        fig_box.add_trace(
            go.Box(y=price_values.tolist(), name='房價'), secondary_y=False,
        )

    if not rent_values.empty:
        fig_box.add_trace(
            go.Box(y=rent_values.tolist(), name='租金'), secondary_y=True,
        )

    fig_box.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=50, r=50, t=50, b=50),
        legend=dict(
            x=0, y=1,
            traceorder="normal",
            font=dict(
                family="Montserrat",
                size=12,
                color="black"),
            bgcolor="LightSteelBlue",
            bordercolor="Blue",
            borderwidth=2))

    return fig_box


@lru_cache(maxsize=256)
def find_city(city: str = '臺北市', building_type: str = '住宅大樓(11層含以上有電梯)', year: str = '五年以下'):
    if city not in LOCATION:
        raise ValueError(f"未知縣市: {city}")
    if year not in DURATION:
        raise ValueError(f"未知屋齡範圍: {year}")

    city_code = LOCATION[city]
    time_marker = _current_time_marker()
    year_range = DURATION[year]

    data_price, data_rent = _load_city_frames(city_code)

    price_values = _prepare_series(data_price, PRICE_TARGETS, building_type, year_range, time_marker)
    rent_values = _prepare_series(data_rent, RENT_TARGETS, building_type, year_range, time_marker)

    price = _format_currency(_mean_int(price_values))
    rent = _format_currency(_mean_int(rent_values))

    graph_box = _build_box(price_values, rent_values)

    return price, rent, plt.io.to_json(graph_box)
