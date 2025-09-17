import numpy as np
import numpy_financial as npf
import pandas as pd
import plotly as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

TERM_MONTHS = 360
ANNUAL_PRICE_GROWTH = 1.0338
BASE_LOAN_RATE = 2.25
DOWN_PAYMENT_RATIO = 0.2
LOAN_RATIO = 1.0 - DOWN_PAYMENT_RATIO


def _amortization_schedule(total_price: float) -> tuple[np.ndarray, np.ndarray]:
    """Return monthly payment amounts and outstanding principal balances."""
    loan_principal = total_price * LOAN_RATIO
    outstanding = loan_principal

    payments = np.empty(TERM_MONTHS, dtype=float)
    balances = np.empty(TERM_MONTHS, dtype=float)

    for month_index in range(TERM_MONTHS):
        month = month_index + 1
        bank_rate = BASE_LOAN_RATE * (ANNUAL_PRICE_GROWTH ** (month / 12))
        monthly_rate = bank_rate / 1200
        remaining_term = TERM_MONTHS - month_index
        payment = npf.pmt(monthly_rate, remaining_term, -outstanding)
        interest = outstanding * monthly_rate
        principal = payment - interest
        outstanding = max(outstanding - principal, 0.0)
        payments[month_index] = payment
        balances[month_index] = outstanding

    return payments, balances


def _compound_cashflows(cashflows: np.ndarray, invest_rate: float, initial: float = 0.0) -> np.ndarray:
    """Compound monthly cashflows with a given annualised investment rate."""
    if cashflows.size == 0:
        return np.array([], dtype=float)

    monthly_rate = (invest_rate + 1.0) ** (1 / 12)
    balances = np.empty_like(cashflows, dtype=float)
    total = float(initial)

    for idx, cash in enumerate(cashflows):
        total = (total + cash) * monthly_rate
        balances[idx] = total

    return balances


def buy_or_rent(total_price: int, rent_payment: int, income: int, consume: int, invest_rate: float):
    months = np.arange(1, TERM_MONTHS + 1)
    price_growth = ANNUAL_PRICE_GROWTH ** (months / 12)

    loan_payments, principal_left = _amortization_schedule(total_price)

    # Household cashflows indexed by the same time axis
    income_series = income * price_growth
    consume_series = consume * price_growth
    rent_series = rent_payment * price_growth
    house_price_series = total_price * price_growth

    loan_investment = income_series - consume_series - loan_payments
    rent_investment = income_series - consume_series - rent_series

    loan_assets = _compound_cashflows(loan_investment, invest_rate)
    rent_assets = _compound_cashflows(rent_investment, invest_rate, initial=total_price * DOWN_PAYMENT_RATIO)

    # Owning also accrues the property asset minus outstanding principal
    loan_assets = loan_assets + house_price_series - principal_left

    data = pd.DataFrame(
        {
            'date': [f"{month // 12}年{month % 12}月" for month in months],
            'growth_rate': price_growth,
            'principal_left': principal_left,
            'house_price': house_price_series,
            'income': income_series,
            'consume': consume_series,
            'loan_payment': loan_payments,
            'rent_payment': rent_series,
            'total_asset_loan': loan_assets,
            'total_asset_rent': rent_assets,
        }
    )

    fig_line = make_subplots(specs=[[{"secondary_y": True}]])
    fig_line.add_trace(
        go.Scatter(x=data['date'], y=data['total_asset_loan'], fill='tozeroy', name='自住總資產'),
        secondary_y=False,
    )
    fig_line.add_trace(
        go.Scatter(x=data['date'], y=data['total_asset_rent'], fill='tozeroy', name='租屋總資產'),
        secondary_y=False,
    )
    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        width=1000,
        legend=dict(
            x=0,
            y=1,
            traceorder="normal",
            font=dict(family="Montserrat", size=12, color="black"),
            bgcolor="LightSteelBlue",
            bordercolor="Blue",
            borderwidth=2,
        ),
    )
    fig_line.update_xaxes(nticks=10)

    monthly_loan_payment = int(round(loan_payments[0]))
    value1 = [consume, monthly_loan_payment, income - consume - monthly_loan_payment]
    value2 = [consume, rent_payment, income - consume - rent_payment]

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig.add_trace(
        go.Pie(labels=['每月支出', '房貸', '可投資資金'], values=value1, name="自住支出結構"),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Pie(labels=['每月支出', '租金', '可投資資金'], values=value2, name="租屋支出結構"),
        row=1,
        col=2,
    )
    fig.update_traces(hole=0.4, hoverinfo="label+percent+name")
    fig.update_layout(
        annotations=[
            dict(text='自住', x=0.18, y=0.5, font_size=20, showarrow=False),
            dict(text='租屋', x=0.82, y=0.5, font_size=20, showarrow=False),
        ]
    )

    return fig, fig_line
