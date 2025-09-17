"""Routes for base Flask app"""
import json
import time
from typing import Tuple

from flask import Blueprint, jsonify, make_response, render_template, request

from app.dash_apps.Payment import Payment
from app.dash_apps.buyorrent import buy_or_rent
from app.dash_apps.city import find_city
from app.dash_apps.plt_income import plt_income
from app.dash_apps.plt_trend import plt_trend


DEFAULT_CITY = '臺北市'
DEFAULT_BUILDING = '住宅大樓(11層含以上有電梯)'
DEFAULT_DURATION = '五年以下'


def _flag(name: str) -> bool:
    value = request.args.get(name)
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip().lower() not in {"false", "0", "off", ""}
    return bool(value)


def _city_params() -> Tuple[str, str, str]:
    city = request.args.get('city') or DEFAULT_CITY
    building_type = request.args.get('type') or DEFAULT_BUILDING
    duration = request.args.get('duration') or DEFAULT_DURATION
    return city, building_type, duration


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
    city = request.args.get('city') or DEFAULT_CITY
    graphJSON = plt_trend(
        city,
        _flag('price'),
        _flag('rent'),
        _flag('index'),
        _flag('A_price'),
        _flag('A_rent'),
    )
    return graphJSON


@base_app.route("/cb2")
def cb2():
    city, building_type, duration = _city_params()
    price_location, rent_location, _ = find_city(city, building_type, duration)
    return jsonify(price_location=price_location, rent_location=rent_location)


@base_app.route("/pltbox")
def cb3():
    city, building_type, duration = _city_params()
    _, _, graphBOX = find_city(city, building_type, duration)
    return graphBOX


@base_app.route("/pltbar")
def cb4():
    graphBAR = plt_income(
        _flag('high'),
        _flag('price'),
        _flag('rent'),
        _flag('income'),
        _flag('times'),
    )
    return graphBAR


# buy_house_app
base_app_buying = Blueprint("base_app_buying", __name__)


@base_app_buying.route("/buy_or_rent")
def index_buying():
    return render_template("buyhouse.html")


@base_app_buying.route("/buy_or_rent/cb")
def cb_buyhouse():
    city, building_type, duration = _city_params()
    sq = request.args.get('sq')

    try:
        total_price, First_payment, loan_payment, rent_payment = Payment(
            city, building_type, duration, sq
        )
    except ValueError as exc:
        return jsonify(error="data_not_available", message=str(exc)), 400

    return jsonify(
        total_price=total_price,
        First_payment=First_payment,
        loan_payment=loan_payment,
        rent_payment=rent_payment
    )


@base_app_buying.route("/buy_or_rent/charts")
def get_charts():
    city, building_type, duration = _city_params()
    sq = request.args.get('sq', '30')
    income = request.args.get('income', '60000')
    consume = request.args.get('consume', '30000')
    invest_rate = request.args.get('invest_rate', '0.05')

    try:
        total_price, first_payment, loan_payment, rent_payment = Payment(city, building_type, duration, sq)

        # 移除 $ 符號並轉換為數字
        total_price_num = int(total_price.replace('$', '').replace(',', ''))
        rent_payment_num = int(rent_payment.replace('$', '').replace(',', ''))
        loan_payment_num = int(loan_payment.replace('$', '').replace(',', ''))
        income_num = int(income)
        consume_num = int(consume)
        invest_rate_num = float(invest_rate)

        # 驗證收入是否足夠
        if income_num < consume_num + loan_payment_num or income_num < consume_num + rent_payment_num:
            return jsonify(
                error="validation_failed",
                message="收入<消費+住房成本，你沒資格阿，你沒資格！"
            )

        fig_pie, fig_line = buy_or_rent(
            total_price_num, rent_payment_num, income_num,
            consume_num, invest_rate_num
        )

        return jsonify(
            pie_chart=json.loads(fig_pie.to_json()),
            line_chart=json.loads(fig_line.to_json())
        )
    except ValueError as exc:
        return jsonify(error="data_not_available", message=str(exc)), 400
    except Exception as e:
        return jsonify(error=str(e)), 500
