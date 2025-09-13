from cmath import nan
from statistics import mean
import pandas as pd 
from pathlib import Path
import plotly as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots



def plt_trend(city = "臺北市" , check_price = True , check_rent = True , check_index = False , A_price = True , A_rent = True):

    ##縣市名稱
    location = { 'a' : '臺北市', 'b' : '臺中市' , 
                 'c' : '基隆市', 'd' : '臺南市' ,
                 'e' : '高雄市', 'f' : '新北市' ,
                 'g' : '宜蘭縣', 'h' : '桃園市' ,
                 'i' : '嘉義市', 'j' : '新竹縣' ,
                 'k' : '苗栗縣', 'm' : '南投縣' ,
                 'n' : '彰化縣', 'o' : '新竹市' ,
                 'p' : '雲林縣', 'q' : '嘉義縣' ,
                 't' : '屏東縣', 'u' : '花蓮縣' ,
                 'w' : '金門'  , 'x' : '澎湖縣'  }

    try:
        data = pd.read_csv("app/static/assets/date_data.csv", encoding='utf-8-sig')
    except UnicodeDecodeError:
        try:
            data = pd.read_csv("app/static/assets/date_data.csv", encoding='utf-8')
        except UnicodeDecodeError:
            data = pd.read_csv("app/static/assets/date_data.csv", encoding='cp950', errors='ignore')

    price = city + "_房價"
    rent = city + "_租金"

    ####################畫出折線圖#################################

    fig_line = make_subplots(specs=[[{"secondary_y": True}]])
    
    # 檢查列名是否存在，如果不存在則用默認值
    available_columns = data.columns.tolist()
    
    if check_index == True and '物價指數' in available_columns:
        fig_line.add_trace(
            go.Scatter(x= data['季度'], y= data['物價指數'] ,name= '物價指數'),
            secondary_y=True,)
    
    if A_price == True and '房價(元/坪)' in available_columns:
        fig_line.add_trace(
            go.Scatter(x= data['季度'], y= data['房價(元/坪)'] ,name= '全台平均房價(元/坪)'),
            secondary_y=False,)

    if A_rent == True and '租金(元/坪)' in available_columns:    
        fig_line.add_trace(
            go.Scatter(x= data['季度'], y= data['租金(元/坪)'] ,name= '全台平均租金(元/坪)'),
            secondary_y=True,)

    # 總是顯示選中縣市的資料，不依賴checkbox
    if price in available_columns:
        fig_line.add_trace(
            go.Scatter(x= data['季度'], y= data[price] ,name= price +'(元/坪)'),
            secondary_y=False,)

    if rent in available_columns:   
        fig_line.add_trace(
            go.Scatter(x= data['季度'], y= data[rent] ,name= rent +'(元/坪)'),
            secondary_y=True,)

    
    fig_line.update_layout( paper_bgcolor='rgba(0,0,0,0)',
                            height=450, # 只設定高度，讓寬度自動適應
                            margin=dict(l=50, r=50, t=50, b=50), # 設定邊距
                            legend=dict(x=0,y=1,  #圖例位置
                            traceorder="normal",
                            font=dict(
                                family="Montserrat",
                                size=12,
                                color="black"),
                            bgcolor="LightSteelBlue",  #邊框顏色
                            bordercolor="Blue",
                            borderwidth=2))

    fig_line.update_xaxes(nticks=10)


    graphJSON = plt.io.to_json(fig_line)



    return graphJSON 



  
    

