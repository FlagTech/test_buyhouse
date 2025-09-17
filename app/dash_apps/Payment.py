import numpy_financial as npf
from typing import Optional

from app.dash_apps.city import find_city


def _currency_to_int(value: str) -> Optional[int]:
    digits = ''.join(ch for ch in str(value) if ch.isdigit())
    return int(digits) if digits else None


def Payment(city: str = '臺北市', building_type: str = '住宅大樓(11層含以上有電梯)',
            year: str = '五年以下', sq=30):

    price, rent, _ = find_city(city, building_type, year)

    price_per_ping = _currency_to_int(price)
    rent_per_ping = _currency_to_int(rent)

    if price_per_ping is None or rent_per_ping is None:
        raise ValueError(f"{city} 缺少房價或租金資料，無法計算付款資訊")

    try:
        sq_int = int(sq)
    except (TypeError, ValueError):
        raise ValueError("坪數格式錯誤") from None

    # 房屋總價與頭期款
    total_price = price_per_ping * sq_int
    first_payment = int(total_price * 0.2)

    # 每期租金
    rent_payment = rent_per_ping * sq_int

    # 利率
    rate = 1.75
    loan_amount = total_price * 0.8
    term = 360

    # 計算貸款年金
    loan_payment = abs(int(npf.pmt(rate / 1200, term, -loan_amount)))

    total_price_str = '$' + f"{int(total_price):,}"
    first_payment_str = '$' + f"{first_payment:,}"
    loan_payment_str = '$' + f"{loan_payment:,}"
    rent_payment_str = '$' + f"{rent_payment:,}"

    return total_price_str, first_payment_str, loan_payment_str, rent_payment_str
