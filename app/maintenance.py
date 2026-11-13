def estimate_annual_maintenance_cost(vehicle_age: int, annual_mileage: float, base_cost: float = 600) -> float:
    '''Estimate annual maintenance costs based on age and mileage.'''
    '''the $600, $50, and $0.05 values are configurable assumptions rather than established industry averages.'''

    # add additional maintenance cost to vehvicles over 5 years old since older vehicles tend to have more accumulated wear on components. Vehicles five years old or younger receive no age adjustment
    # $50 per year beyond 5 years
    age_adjustment = max(0, vehicle_age - 5) * 50

    # add additional maintenance cost to vehicles who accumulate over 12k miles a year since higher mileage generally means more frequent servicing and replacement of wear items. There is no mileage adjustment for vehicles under 12k miles annually.
    # $0.05 per mile above 12,000 annually
    mileage_adjustment = max(0, annual_mileage - 12_000) * 0.05 

    return base_cost + age_adjustment + mileage_adjustment