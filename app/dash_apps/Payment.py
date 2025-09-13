import pandas as pd
import numpy_financial as npf
from app.dash_apps.city import find_city




def Payment(city= '臺北市'  , building_type = '住宅大樓(11層含以上有電梯)' , year = '五年以下' , sq = 30):

    #####每坪房價租金
    price , rent , g= find_city(city , building_type ,  year)

    #####房屋總價
    total_price = int(price[1:]) * int(sq)

    First_payment = total_price * 0.2

    #####每期租金
    rent_payment =  int(rent[1:]) * int(sq)

    #####利率
    rate = 1.75
    loan_amount = total_price * 0.8
    term = 360

    #####計算貸款年金
    loan_payment = npf.pmt(rate / 1200 , term , -loan_amount)
    loan_payment = int(loan_payment)

    total_price = '$' + str(total_price)
    First_payment = '$' + str(First_payment)
    loan_payment = '$' + str(loan_payment)
    rent_payment = '$' + str(rent_payment)

    return total_price , First_payment , loan_payment , rent_payment

    








