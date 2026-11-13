from app.maintenance import estimate_annual_maintenance_cost

def test_estimate_annual_maintenance_cost_mileage_below_threshold():
    result = estimate_annual_maintenance_cost(
        vehicle_age = 14,
        annual_mileage = 10_357,
    )

    assert result == 1050.00

def test_estimate_annual_maintenance_cost_age_below_threshold():
    result = estimate_annual_maintenance_cost(
        vehicle_age = 4,
        annual_mileage = 13_357,
    )

    assert result == 667.85

def test_estimate_annual_maintenance_cost_above_age_mileage_tresholds():
    result = estimate_annual_maintenance_cost(
            vehicle_age = 9,
            annual_mileage = 17_357,
    )
    
    assert result == 1067.85

def test_estimate_annual_maintenance_cost_custom_base_maintenance_cost():
    result = estimate_annual_maintenance_cost(
                vehicle_age = 9,
                annual_mileage = 17_357,
                base_cost = 700,
        )

    assert result == 1167.85