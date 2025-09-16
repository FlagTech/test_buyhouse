"""Routes for base Flask app"""
from flask import request
from flask import Blueprint, render_template, jsonify, make_response
import plotly as plt
import time
import json
from app.dash_apps.plt_trend import plt_trend
from app.dash_apps.city import find_city
from app.dash_apps.plt_income import plt_income
from app.dash_apps.Payment import Payment
from app.dash_apps.buyorrent import buy_or_rent



# base_app
base_app = Blueprint("base_app", __name__)

@base_app.route("/")
def index():
    graphJSON = plt_trend(check_index=True)
    graphBAR = plt_income()
    price_location, rent_location, graphBOX = find_city()
    timestamp = str(int(time.time()))
    response = make_response(render_template(
        "index.html",
        graphJSON=graphJSON,
        graphBOX=graphBOX,
        graphBAR=graphBAR,
        timestamp=timestamp
    ))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@base_app.route("/plt")
def cb():
    city = request.args.get('city')
    price = request.args.get('price')
    rent = request.args.get('rent')
    index = request.args.get('index')
    A_price = request.args.get('A_price')
    A_rent = request.args.get('A_rent')
    

    if price is None:
        price = False
    else:
        price = True

    if rent is None:
        rent = False
    else:
        rent = True

    if index is None:
        index = False
    else:
        index = True

    if A_price is None:
        A_price = False
    else:
        A_price = True

    if A_rent is None:
        A_rent = False
    else:
        A_rent = True

    graphJSON = plt_trend(city, price, rent, index, A_price, A_rent)

    return graphJSON


@base_app.route("/cb2")
def cb2():

    city = request.args.get('city')
    type = request.args.get('type')
    duration = request.args.get('duration')

    price_location, rent_location, graphBOX = find_city(city, type, duration)

    return jsonify(price_location=price_location, rent_location=rent_location)

# 箱型圖
@base_app.route("/pltbox")
def cb3():

    city = request.args.get('city')
    type = request.args.get('type')
    duration = request.args.get('duration')

    price_location, rent_location, graphBOX = find_city(city, type, duration)

    return graphBOX

# 長條圖
@base_app.route("/pltbar")
def cb4():
    high = request.args.get('high')
    price = request.args.get('price')
    rent = request.args.get('rent')
    income = request.args.get('income')
    times = request.args.get('times')

    if high is None:
        high = False
    else:
        high = True

    if price is None:
        price = False
    else:
        price = True

    if rent is None:
        rent = False
    else:
        rent = True

    if income is None:
        income = False
    else:
        income = True

    if times is None:
        times = False
    else:
        times = True

    graphBAR = plt_income(high, price, rent, income, times)

    return graphBAR



# buy_house_app
base_app_buying = Blueprint("base_app_buying", __name__)

@base_app_buying.route("/buy_or_rent")
def index_buying():
    return render_template("buyhouse.html")

@base_app_buying.route("/buy_or_rent/cb")
def cb_buyhouse():
    city = request.args.get('city')
    type = request.args.get('type')
    duration = request.args.get('duration')
    sq = request.args.get('sq')

    total_price, First_payment, loan_payment, rent_payment = Payment(
        city, type, duration, sq
    )

    return jsonify(
        total_price=total_price,
        First_payment=First_payment,
        loan_payment=loan_payment,
        rent_payment=rent_payment
    )

@base_app_buying.route("/buy_or_rent/charts")
def get_charts():
    city = request.args.get('city', '臺北市')
    type = request.args.get('type', '住宅大樓(11層含以上有電梯)')
    duration = request.args.get('duration', '五年以下')
    sq = request.args.get('sq', '30')
    income = request.args.get('income', '60000')
    consume = request.args.get('consume', '30000')
    invest_rate = request.args.get('invest_rate', '0.05')

    try:
        total_price, _, _, rent_payment = Payment(city, type, duration, sq)

        # 移除 $ 符號並轉換為數字
        total_price_num = int(total_price.replace('$', '').replace(',', ''))
        rent_payment_num = int(rent_payment.replace('$', '').replace(',', ''))
        income_num = int(income)
        consume_num = int(consume)
        invest_rate_num = float(invest_rate)

        fig_pie, fig_line = buy_or_rent(
            total_price_num, rent_payment_num, income_num,
            consume_num, invest_rate_num
        )

        return jsonify(
            pie_chart=json.loads(fig_pie.to_json()),
            line_chart=json.loads(fig_line.to_json())
        )
    except Exception as e:
        return jsonify(error=str(e)), 500