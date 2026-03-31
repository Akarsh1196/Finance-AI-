def calculate_future_value(monthly_investment, annual_return_pct, years):
    r = annual_return_pct / 100 / 12
    n = years * 12

    fv = monthly_investment * (((1 + r) ** n - 1) / r) * (1 + r)
    return round(fv, 2)


def simulate_all(monthly_investment, years):
    return {
        'SIP (Mutual Fund)': calculate_future_value(monthly_investment, 12, years),
        'FD (Fixed Deposit)': calculate_future_value(monthly_investment, 6.5, years),
        'Real Estate': calculate_future_value(monthly_investment, 8, years),
    }


# 🆕 Goal-based SIP calculation
def required_monthly_investment(target_amount, annual_return_pct, years):
    r = annual_return_pct / 100 / 12
    n = years * 12

    if r == 0:
        return target_amount / n

    sip = target_amount / (((1 + r) ** n - 1) / r * (1 + r))
    return round(sip, 2)