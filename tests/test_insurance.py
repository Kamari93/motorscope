from app.insurance import estimate_annual_insurance_cost
import pytest

def test_estimate_annual_insurance_cost():
    result = estimate_annual_insurance_cost(150)

    assert result == 1800

def test_estimate_annual_insurance_cost_negative_premium():
    with pytest.raises(ValueError, match = 'Monthly insurance premium cannot be negative.'):
        estimate_annual_insurance_cost(-150)