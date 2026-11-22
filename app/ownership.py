def calculate_annual_ownership_cost(annual_maintenance: float, annual_fuel: float) -> dict:
    '''Calculate estimated annual vehicle ownership expenses.'''

    if annual_maintenance < 0:
         raise ValueError('Annual maintenance cannot be negative.')

    if annual_fuel < 0:
          raise ValueError('Annual fuel cost cannot be negative.')

    total_annual_cost = annual_maintenance + annual_fuel

    average_monthly_cost = total_annual_cost / 12

    return {
         'annual_maintenance': round(annual_maintenance, 2),
         'annual_fuel': round(annual_fuel, 2),
         'total_annual_cost': round(total_annual_cost, 2),
         'average_monthly_cost': round(average_monthly_cost, 2)
    }