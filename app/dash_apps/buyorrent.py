import pandas as pd
import numpy_financial as npf
from app.dash_apps.city import find_city
import plotly as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots



def buy_or_rent(total_price , rent_payment , income , consume ,invest_rate):


    ####五年平均通膨率
    rate = 1.0338 ** (1/12)
    ###每月貸款月付金
    left = total_price * 0.8
    list_left = []
    list_payment_f =[]
    for i in range(1,361):
        bank_rate = 2.25 * (rate ** i)  
        loan_payment_f = npf.pmt(bank_rate / 1200 , 361-i , -left)
        interest = left  * (bank_rate/1200)
        principal = loan_payment_f - interest
        left = left - principal
        list_payment_f.append(loan_payment_f)
        list_left.append(left)
    

    

    #####投資函數
    def investment_fun(list_invetment, invest_rate_f ,first_payment = 0):

        invest_rate = (invest_rate_f +1) **(1/12)
        list_invest = []
        total_invest = first_payment

        for invest_payment in list_invetment:
            total_invest = (total_invest + invest_payment ) * invest_rate 
            list_invest.append(total_invest)
        return list_invest



    data = pd.DataFrame()
    data['date'] = [str(int(i/12))+'年' +str(i%12)+ '月' for i in range(1,361)]
    ####每月剩餘拿來投資
    data['list_rate'] = [rate ** i for i in range(1,361)]
    ##剩餘本金
    data['principal_left'] = list_left 
    ###房價(隨通膨成長)
    data['house_price'] = total_price * data['list_rate']
    ##收入(隨通膨成長)
    data['income'] = data['list_rate'] * income
    ##消費(隨通膨成長)
    data['consume'] = data['list_rate'] * consume
    ##貸款月付
    data['loan_payment'] =  list_payment_f
    ##租金月付
    data['rent_payment'] = data['list_rate']  * rent_payment
    data['loan_investment'] = data['income'] - data['consume'] - data['loan_payment'] 
    data['total_asset_loan'] = investment_fun(data['loan_investment'] , invest_rate_f= invest_rate,)
    data['total_asset_loan'] = data['total_asset_loan'] + data['house_price'] - data['principal_left']
    data['rent_investment'] = data['income'] - data['consume'] - data['rent_payment'] 
    data['total_asset_rent'] = investment_fun(data['rent_investment'] , invest_rate_f= invest_rate,first_payment= (total_price *0.2)) 

    ###折線圖
    fig_line = make_subplots(specs=[[{"secondary_y": True}]])
    fig_line.add_trace(
    go.Scatter(x= data['date'], y= data['total_asset_loan'],fill='tozeroy' ,name= '買房者資產'),
    secondary_y=False,)

    fig_line.add_trace(
    go.Scatter(x= data['date'], y= data['total_asset_rent'],fill='tozeroy',name= '租房者資產'),
    secondary_y=False,)


  
    fig_line.update_layout( paper_bgcolor='rgba(0,0,0,0)', height=500, width=1000 ,
                            legend=dict(x=0,y=1,  #圖例位置
                            traceorder="normal",
                            font=dict(
                                family="Montserrat",
                                size=12,
                                color="black"),
                            bgcolor="LightSteelBlue",  # 背景颜色，边框颜色和宽度
                            bordercolor="Blue",
                            borderwidth=2))

    fig_line.update_xaxes(nticks=10)


    loan_payment = int(list_payment_f[0])
    value1 = [consume , loan_payment , income - loan_payment]
    value2 = [consume , rent_payment , income - rent_payment]

    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels= ['每月消費', '貸款月付金' , '剩餘投資'], 
            values= value1, name="購屋每月支出分配"),
                1, 1)
    fig.add_trace(go.Pie(labels= ['每月消費', '每月租金' , '剩餘投資'], 
            values= value2, name="租屋每月支出分配"),
                1, 2)

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(
        annotations=[dict(text='購屋', x=0.18, y=0.5, font_size=20, showarrow=False),
                    dict(text='租屋', x=0.82, y=0.5, font_size=20, showarrow=False)])

    
    return fig , fig_line


    





 













