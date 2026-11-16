from app.fuel import estimate_annual_fuel_cost
import pytest

def test_estimate_annual_fuel_cost():
    result = estimate_annual_fuel_cost(
        annual_mileage = 12_000,
        mpg = 28,
    )

    assert result == 1285.71


def test_estimate_annual_fuel_cost_higher_annual_mileage():
    result = estimate_annual_fuel_cost(
        annual_mileage = 18_000,
        mpg = 28,
    )

    assert result == 1928.57

def test_estimate_annual_fuel_cost_better_mpg():
    result = estimate_annual_fuel_cost(
        annual_mileage = 15_000,
        mpg = 31,
    )
    
    assert result == 1451.61

def test_estimate_annual_fuel_cost_custom_fuel_price():
    result = estimate_annual_fuel_cost(
        annual_mileage = 15_000,
        mpg = 28,
        fuel_price = 4.0,
    )

    assert result == 2142.86

def test_estimate_annual_fuel_cost_negative_mileage():
    with pytest.raises(ValueError, match = 'Annual mileage cannot be negative.'):
        estimate_annual_fuel_cost(
        annual_mileage = -15_000,
        mpg = 28,
        fuel_price = 4.0,
    )

def test_estimate_annual_fuel_cost_zero_mpg():
    with pytest.raises(ValueError, match = 'MPG must be greater than zero.'):
        estimate_annual_fuel_cost(
        annual_mileage = 15_000,
        mpg = 0,
        fuel_price = 4.0,
    )

def test_estimate_annual_fuel_cost_negative_mpg():
    with pytest.raises(ValueError, match = 'MPG must be greater than zero.'):
        estimate_annual_fuel_cost(
        annual_mileage = 15_000,
        mpg = -3,
        fuel_price = 4.0,
    )

def test_estimate_annual_fuel_cost_negative_fuel_price():
    with pytest.raises(ValueError, match = 'Fuel price cannot be negative.'):
        estimate_annual_fuel_cost(
        annual_mileage = 15_000,
        mpg = 28,
        fuel_price = -4.0,
    )