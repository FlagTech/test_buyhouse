import pandas as pd
from datetime import datetime
from pathlib import Path

import plotly as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots




def find_city(city='臺北市', building_type='住宅大樓(11層含以上有電梯)', year='五年以下'):
    # 縣市名稱
    location = {
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

    # 時間
    duration = {'五年以下': (0, 50000), '五年至十五年': (50000, 150000),
                '十五年至三十年': (150000, 300000), '三十年以上': (300000, 1000000)}
    time = int(datetime.now().strftime("%Y%m%d")) - 19110000


    data_price = pd.DataFrame()
    data_rent = pd.DataFrame()

    # 尋找檔案
    date = ['114Q2', '114Q1', '113Q4', '113Q3', '113Q2']
    for i in date:
        path = Path.cwd() / "app/static/assets/data" / i
        x = list(path.glob(location[city] + '*a.csv'))[0]
        y = list(path.glob(location[city] + '*c.csv'))[0]
        data_x = pd.read_csv(x, low_memory=False)
        data_y = pd.read_csv(y, low_memory=False)
        # 房價資料
        data_price = pd.concat([data_price, data_x])
        # 租金資料
        data_rent = pd.concat([data_rent, data_y])



    # 首次過濾
    filter_row = ((data_price['交易標的'] == '房地(土地+建物)') |
                  (data_price['交易標的'] == '房地(土地+建物)+車位'))
    filter_col = ['鄉鎮市區', '交易標的', '交易年月日', '移轉層次', '總樓層數',
                  '建物型態', '建築完成年月', '總價元', '單價元平方公尺']
    f_df = data_price.loc[filter_row, filter_col]
    f_df = f_df.dropna(subset=['單價元平方公尺'])
    f_df = f_df.copy()
    f_df['建築完成年月'] = f_df['建築完成年月'].fillna(value='0500000')
    f_df['建築完成年月'] = (pd.to_numeric(f_df['建築完成年月'], errors='coerce')
                        .fillna(500000).astype(int))
    f_df['屋齡'] = time - f_df['建築完成年月']
    # 二次過濾
    filter_row = ((f_df['建物型態'] == building_type) &
                  (f_df['屋齡'].between(duration[year][0], duration[year][1])))
    filter_col = ['鄉鎮市區', '建物型態', '建築完成年月', '單價元平方公尺']
    f_df = f_df.loc[filter_row, filter_col]


    # 數值轉換，處理非數值資料
    f_df = f_df[pd.to_numeric(f_df['單價元平方公尺'], errors='coerce') > 0]
    f_df['單價元坪'] = (pd.to_numeric(f_df['單價元平方公尺'], errors='coerce') /
                      0.3025)
    f_df['單價元坪'] = f_df['單價元坪'].apply(int)

    price = f_df['單價元坪'].mean()
    price = int(price)



    # 首次過濾
    filter_row = ((data_rent['交易標的'] == '房地(土地+建物)') |
                  (data_rent['交易標的'] == '房地(土地+建物)+車位') |
                  (data_rent['交易標的'] == '租賃房屋') |
                  (data_rent['交易標的'] == '租賃房屋+車位'))
    filter_col = ['鄉鎮市區', '交易標的', '總樓層數', '建物型態',
                  '建築完成年月', '單價元平方公尺']
    f_df_rent = data_rent.loc[filter_row, filter_col]
    f_df_rent = f_df_rent.dropna(subset=['單價元平方公尺'])
    f_df_rent = f_df_rent.copy()
    f_df_rent['建築完成年月'] = f_df_rent['建築完成年月'].fillna(value='0500000')
    f_df_rent['建築完成年月'] = (pd.to_numeric(f_df_rent['建築完成年月'], errors='coerce')
                               .fillna(500000).astype(int))
    f_df_rent['屋齡'] = time - f_df_rent['建築完成年月']
    # 二次過濾
    filter_row = ((f_df_rent['建物型態'] == building_type) &
                  (f_df_rent['屋齡'].between(duration[year][0], duration[year][1])))
    filter_col = ['鄉鎮市區', '建物型態', '建築完成年月', '單價元平方公尺']
    f_df_rent = f_df_rent.loc[filter_row, filter_col]


    # 數值轉換，處理非數值資料
    f_df_rent = f_df_rent[pd.to_numeric(f_df_rent['單價元平方公尺'], errors='coerce') > 0]
    f_df_rent['單價元坪'] = (pd.to_numeric(f_df_rent['單價元平方公尺'], errors='coerce') /
                           0.3025)
    f_df_rent['單價元坪'] = f_df_rent['單價元坪'].apply(int)

    rent = f_df_rent['單價元坪'].mean()
    if pd.isna(rent):
        rent = '資料不足'
    else:
        rent = int(rent)


    price = '$' + str(price)
    rent = '$' + str(rent)


    # 箱型圖
    fig_box = make_subplots(specs=[[{"secondary_y": True}]])

    fig_box.add_trace(
        go.Box(y=f_df['單價元坪'], name='房價'), secondary_y=False,)

    fig_box.add_trace(
        go.Box(y=f_df_rent['單價元坪'], name='租金'), secondary_y=True,)

    fig_box.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,  # 只設定高度
        margin=dict(l=50, r=50, t=50, b=50),  # 設定邊距
        legend=dict(
            x=0, y=1,  # 圖例位置
            traceorder="normal",
            font=dict(
                family="Montserrat",
                size=12,
                color="black"),
            bgcolor="LightSteelBlue",  # 背景顏色，邊框顏色和寬度
            bordercolor="Blue",
            borderwidth=2))

    graphBOX = plt.io.to_json(fig_box)


    return price, rent, graphBOX




    


