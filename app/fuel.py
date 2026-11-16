def estimate_annual_fuel_cost(annual_mileage: float, mpg: float, fuel_price: float = 3.0,) -> float:
    '''Estimate annual fuel expenses.'''

    if annual_mileage < 0:
        raise ValueError('Annual mileage cannot be negative.')

    if mpg <= 0:
        raise ValueError('MPG must be greater than zero.')

    if fuel_price < 0:
        raise ValueError('Fuel price cannot be negative.')

    total_gallons = annual_mileage / mpg

    return round(total_gallons * fuel_price, 2)