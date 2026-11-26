"""Routes for base Flask app"""
from flask import request
from flask import Blueprint, render_template ,jsonify, make_response
import plotly as plt
import time
from app.dash_apps.plt_trend import plt_trend
from app.dash_apps.city import find_city, normalize_city, DURATIONS
from app.dash_apps.plt_income import plt_income
from app.dash_apps.Payment import Payment


def bad_request(message):
    """參數錯誤時回傳 400，避免後端拋出例外變成 500"""
    return jsonify(error=message), 400


def get_city_args():
    """讀取並檢查 city / type / duration 參數，回傳 (city, type, duration, error)"""
    city = normalize_city(request.args.get('city'))
    if city is None:
        return None, None, None, bad_request('請先選擇有效的縣市')

    building_type = request.args.get('type') or '住宅大樓(11層含以上有電梯)'
    duration = request.args.get('duration') or '五年以下'
    if duration not in DURATIONS:
        return None, None, None, bad_request('屋齡參數錯誤')

    return city, building_type, duration, None



#####base_app#####
base_app = Blueprint("base_app", __name__)

@base_app.route("/")
def index():
    graphJSON = plt_trend(check_index=True)
    graphBAR = plt_income()
    price_location , rent_location , graphBOX = find_city()
    timestamp = str(int(time.time()))
    response = make_response(render_template("index.html" , graphJSON = graphJSON , graphBOX = graphBOX , graphBAR = graphBAR, timestamp = timestamp))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@base_app.route("/plt")
def cb():
    city = normalize_city(request.args.get('city'))
    if city is None:
        return bad_request('請先選擇有效的縣市')
    price = request.args.get('price')
    rent = request.args.get('rent')
    index = request.args.get('index')
    A_price = request.args.get('A_price')
    A_rent = request.args.get('A_rent')
    

    if price is None:
        price = False
    else :
        price = True
    
    if rent is None:
        rent = False
    else :
        rent = True

    if index is None:
        index = False
    else :
        index = True

    if A_price  is None:
        A_price  = False
    else :
        A_price  = True

    if A_rent is None:
        A_rent = False
    else :
        A_rent = True

    graphJSON = plt_trend(city , price , rent , index , A_price , A_rent)

    return graphJSON


@base_app.route("/cb2")
def cb2():

    city, type, duration, error = get_city_args()
    if error:
        return error

    price_location , rent_location  ,graphBOX = find_city(city , type , duration)

    return jsonify(price_location = price_location , rent_location = rent_location)

#箱型圖
@base_app.route("/pltbox")
def cb3():

    city, type, duration, error = get_city_args()
    if error:
        return error

    price_location , rent_location , graphBOX = find_city(city , type , duration)

    return graphBOX

##長條圖
@base_app.route("/pltbar")
def cb4():
    high = request.args.get('high')
    price = request.args.get('price')
    rent = request.args.get('rent')
    income = request.args.get('income')
    times = request.args.get('times')

    if high is None:
        high = False
    else :
        high = True

    if price is None:
        price = False
    else :
        price = True
    
    if rent is None:
        rent = False
    else :
        rent = True

    if income  is None:
        income  = False
    else :
        income  = True

    if times is None:
        times = False
    else :
        times = True

    
    graphBAR = plt_income( high ,price , rent , income , times)

    return graphBAR




#####buy_house_app##########
base_app_buying = Blueprint("base_app_buying", __name__)

@base_app_buying.route("/buy_or_rent")
def index_buying():
    
    return render_template("buyhouse.html" )

@base_app_buying.route("/buy_or_rent/cb")
def cb_buyhouse():
    
    city, type, duration, error = get_city_args()
    if error:
        return error

    sq = request.args.get('sq', '30')
    if not sq.isdigit() or not 0 <= int(sq) <= 1000:
        return bad_request('坪數參數錯誤')

    total_price , First_payment , loan_payment , rent_payment = Payment(city , type ,duration ,sq)

    return jsonify(total_price = total_price , First_payment = First_payment , loan_payment = loan_payment ,rent_payment = rent_payment)