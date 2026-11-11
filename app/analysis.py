from datetime import date
from app.models import VehicleListing

'''calculations used in maintenance estimates and vehicle comparisons.'''

def calculate_vehicle_age(vehicle: VehicleListing, current_year: int | None = None) -> int:
    '''Calculate vehicle age using its model year.'''
    if current_year is None:
        current_year = date.today().year

    return current_year - vehicle.year

def calculate_average_annual_mileage(vehicle: VehicleListing, current_year: int | None = None) -> float | None:
    '''Estimate average annual mileage based on model year.'''
    vehicle_age = calculate_vehicle_age(vehicle, current_year)

    if vehicle_age <= 0:
        return None

    return round(vehicle.mileage / vehicle_age, 2)

def assess_annual_mileage(average_annual_mileage: float | None, benchmark: int = 12_000) -> str:
    '''Compare annual mileage against a reference benchmark.'''
    if average_annual_mileage is None:
        return 'Insufficient vehicle age for assessment.'
    if average_annual_mileage < benchmark * 0.75:
        return 'Below average.'
    if average_annual_mileage <= benchmark * 1.75:
        return 'Around average.'
    return 'Above average.'