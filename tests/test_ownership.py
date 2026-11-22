import pytest
from app.ownership import calculate_annual_ownership_cost

def test_calculate_annual_ownership_cost():
    result = calculate_annual_ownership_cost(
        annual_maintenance = 1575.00,
        annual_fuel = 2410.71,
    )

    assert result is not None
    assert result['annual_maintenance'] == 1575.00
    assert result['annual_fuel'] == 2410.71
    assert result['total_annual_cost'] == 3985.71
    assert result['average_monthly_cost'] == 332.14

def test_calculate_annual_ownership_cost_zero_expenses():
    result = calculate_annual_ownership_cost(
        annual_maintenance = 0.0, annual_fuel = 0.0,
        )

    assert result is not None
    assert result['total_annual_cost'] == 0
    assert result['average_monthly_cost'] == 0

def test_calculate_annual_ownership_cost_negative_maintenance():
    with pytest.raises(ValueError, match ='Annual maintenance cannot be negative.'):
        calculate_annual_ownership_cost(
            annual_maintenance = -1, annual_fuel = 0.0,
            )

def test_calculate_annual_ownership_cost_negative_fuel():
    with pytest.raises(ValueError, match ='Annual fuel cost cannot be negative.'):
        calculate_annual_ownership_cost(
            annual_maintenance = 0.0, annual_fuel = -1,
             )   

def test_calculate_annual_ownership_cost_higher_expenses():
    result = calculate_annual_ownership_cost(
        annual_maintenance = 2575.00,
        annual_fuel = 3410.71,
        )
    
    assert result is not None
    assert result['annual_maintenance'] == 2575.00
    assert result['annual_fuel'] == 3410.71
    assert result['total_annual_cost'] == 5985.71
    assert result['average_monthly_cost'] == 498.81