from app.models import VehicleListing
from app.analysis import calculate_vehicle_age, calculate_average_annual_mileage, assess_annual_mileage

def test_calculate_vehicle_age():
    vehicle = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2016,
        mileage=120000,
        asking_price=12000,
    )

    assert calculate_vehicle_age(vehicle, 2026) == 10

def test_calculate_average_annual_mileage():
    vehicle = VehicleListing(
            make="Honda",
            model="CR-V",
            year=2016,
            mileage=120000,
            asking_price=12000,
        )

    assert calculate_average_annual_mileage(vehicle, 2026) == 12_000

def test_return_none_for_model_year_is_current_year():
    vehicle = VehicleListing(
            make="Honda",
            model="CR-V",
            year=2026,
            mileage=100,
            asking_price=20_000,
        )

    assert calculate_average_annual_mileage(vehicle, 2026) == None

def test_below_average_annual_mileage():
    vehicle = VehicleListing(
            make="Honda",
            model="CR-V",
            year=2016,
            mileage=89_000,
            asking_price=12000,
        )

    average_annual_mileage = calculate_average_annual_mileage(vehicle, 2026)
    assert assess_annual_mileage(average_annual_mileage, 12_000) == 'Below average.'

def test_about_average_annual_mileage():
    vehicle = VehicleListing(
            make="Honda",
            model="CR-V",
            year=2016,
            mileage=111_000,
            asking_price=12000,
        )
    
    average_annual_mileage = calculate_average_annual_mileage(vehicle, 2026)
    assert assess_annual_mileage(average_annual_mileage, 12_000) == 'Around average.'

def test_above_average_annual_mileage():
    vehicle = VehicleListing(
            make="Honda",
            model="CR-V",
            year=2016,
            mileage=270_000,
            asking_price=12000,
        )
    
    average_annual_mileage = calculate_average_annual_mileage(vehicle, 2026)
    assert assess_annual_mileage(average_annual_mileage, 12_000) == 'Above average.'

def test_insufficient_average_annual_mileage():
    vehicle = VehicleListing(
            make="Honda",
            model="CR-V",
            year=2026,
            mileage=10,
            asking_price=20_000,
        )
    
    average_annual_mileage = calculate_average_annual_mileage(vehicle, 2026)
    assert assess_annual_mileage(average_annual_mileage, 12_000) == 'Insufficient vehicle age for assessment.'