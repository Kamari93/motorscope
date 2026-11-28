def estimate_annual_insurance_cost(monthly_premium: float) -> float:
    '''Calculate annual insurance expenses from a monthly premium.'''

    if monthly_premium < 0:
        raise ValueError('Monthly insurance premium cannot be negative.')

    return round(monthly_premium * 12, 2)