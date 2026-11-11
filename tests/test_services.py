from app import database
from app.database import initialize_database
from app.models import VehicleListing
from app.repositories import VehicleRepository
from app.services import VehicleService
import pytest

def test_add_and_get_vehicle_listing(tmp_path, monkeypatch):
    test_database_path = tmp_path / 'test_motorscope.db'
    monkeypatch.setattr(database, 'DATABASE_PATH', test_database_path)
    initialize_database()

    service = VehicleService(VehicleRepository())

    vehicle = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2012,
        mileage=145000,
        asking_price=6200.00,
    )

    vehicle_id = service.add_vehicle_listing(vehicle)
    vehicles = service.get_all_vehicle_listings()

    assert vehicle_id == 1
    assert len(vehicles) == 1

    result = service.get_vehicle_listing_by_id(vehicle_id)

    assert result is not None
    assert result.id == vehicle_id
    assert result.mileage == 145000
    assert result.asking_price == 6200.00

def test_delete_vehicle(tmp_path, monkeypatch):
    test_database_path = tmp_path / 'test_motorscope.db'
    monkeypatch.setattr(database, 'DATABASE_PATH', test_database_path)
    initialize_database()
    
    service = VehicleService(VehicleRepository())
    
    vehicle=VehicleListing(
        make="Honda",
        model="CR-V",
        year=2012,
        mileage=145000,
        asking_price=6200.00,
    )

    vehicle_id = service.add_vehicle_listing(vehicle)

    assert service.delete_vehicle_listing(vehicle_id) is True
    assert service.get_vehicle_listing_by_id(vehicle_id) is None

def test__add_vehicle_rejects_negative_mileage(tmp_path, monkeypatch):
    test_database_path = tmp_path / 'test_motorscope.db'
    monkeypatch.setattr(database, 'DATABASE_PATH', test_database_path)
    initialize_database()
    
    service = VehicleService(VehicleRepository())

    vehicle = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2015,
        mileage=-100,
        asking_price=12000,
    )

    with pytest.raises(ValueError, match='Mileage cannot be negative.'):
        service.add_vehicle_listing(vehicle)

def test__add_vehicle_empty_make(tmp_path, monkeypatch):
    test_database_path = tmp_path / 'test_motorscope.db'
    monkeypatch.setattr(database, 'DATABASE_PATH', test_database_path)
    initialize_database()
    
    service = VehicleService(VehicleRepository())

    vehicle = VehicleListing(
        make="",
        model="CR-V",
        year=2015,
        mileage=11000,
        asking_price=12000,
    )

    with pytest.raises(ValueError, match='Vehicle make cannot be empty.'):
        service.add_vehicle_listing(vehicle)

def test__add_vehicle_empty_model(tmp_path, monkeypatch):
    test_database_path = tmp_path / 'test_motorscope.db'
    monkeypatch.setattr(database, 'DATABASE_PATH', test_database_path)
    initialize_database()
    
    service = VehicleService(VehicleRepository())

    vehicle = VehicleListing(
        make="Honda",
        model="",
        year=2015,
        mileage=11000,
        asking_price=12000,
    )

    with pytest.raises(ValueError, match='Vehicle model cannot be empty.'):
        service.add_vehicle_listing(vehicle)

def test__add_vehicle_invalid_year(tmp_path, monkeypatch):
    test_database_path = tmp_path / 'test_motorscope.db'
    monkeypatch.setattr(database, 'DATABASE_PATH', test_database_path)
    initialize_database()
    
    service = VehicleService(VehicleRepository())

    vehicle = VehicleListing(
        make="Honda",
        model="CR-V",
        year=1885,
        mileage=11000,
        asking_price=12000,
    )

    with pytest.raises(ValueError, match='Vehicle year is invalid.'):
        service.add_vehicle_listing(vehicle)

def test__add_vehicle_negative_mileage(tmp_path, monkeypatch):
    test_database_path = tmp_path / 'test_motorscope.db'
    monkeypatch.setattr(database, 'DATABASE_PATH', test_database_path)
    initialize_database()
    
    service = VehicleService(VehicleRepository())

    vehicle = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2015,
        mileage=-11000,
        asking_price=12000,
    )

    with pytest.raises(ValueError, match='Mileage cannot be negative.'):
        service.add_vehicle_listing(vehicle)

def test__add_vehicle_negative_asking_price(tmp_path, monkeypatch):
    test_database_path = tmp_path / 'test_motorscope.db'
    monkeypatch.setattr(database, 'DATABASE_PATH', test_database_path)
    initialize_database()
    
    service = VehicleService(VehicleRepository())

    vehicle = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2015,
        mileage=11000,
        asking_price=-12000,
    )

    with pytest.raises(ValueError, match='Asking price cannot be negative.'):
        service.add_vehicle_listing(vehicle)

def test__update_vehicle_invalid_data(tmp_path, monkeypatch):
    test_database_path = tmp_path / 'test_motorscope.db'
    monkeypatch.setattr(database, 'DATABASE_PATH', test_database_path)
    initialize_database()
    
    service = VehicleService(VehicleRepository())

    existing = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2015,
        mileage=11000,
        asking_price=12000,
    )

    existing_id = service.add_vehicle_listing(existing)

    updated = VehicleListing(
            make="Honda",
            model="CR-V",
            year=2015,
            mileage=11000,
            asking_price=-12000,
            id=existing_id,
        )

    with pytest.raises(ValueError, match='Asking price cannot be negative.'):
        service.update_vehicle_listing(existing_id, updated)

def test__invalid_data_never_reaches_repo(tmp_path, monkeypatch):
    test_database_path = tmp_path / 'test_motorscope.db'
    monkeypatch.setattr(database, 'DATABASE_PATH', test_database_path)
    initialize_database()
    
    service = VehicleService(VehicleRepository())

    invalid_vehicle = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2015,
        mileage=11000,
        asking_price=-12000,
    )

    with pytest.raises(ValueError, match='Asking price cannot be negative.'):
            service.add_vehicle_listing(invalid_vehicle)
    
    assert len(service.get_all_vehicle_listings()) == 0
    assert service.get_vehicle_listing_by_id(1) is None

def test_analyze_existing_vehicle_listing(tmp_path, monkeypatch):
    test_database_path = tmp_path / 'test_motorscope.db'
    monkeypatch.setattr(database, 'DATABASE_PATH', test_database_path)
    initialize_database()

    service = VehicleService(VehicleRepository())

    vehicle = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2012,
        mileage=145000,
        asking_price=6200.00,
    )

    vehicle_id = service.add_vehicle_listing(vehicle)

    analyzed_vehicle = service.analyze_vehicle_listing(vehicle_id, 2026)

    assert analyzed_vehicle is not None
    assert analyzed_vehicle['vehicle_age'] == 14
    assert analyzed_vehicle['average_annual_mileage'] == 10_357.14
    assert analyzed_vehicle['mileage_assessment'] == 'Around average.'

def test_analyze_vehicle_listing_returns_none_id_not_exist(tmp_path, monkeypatch):
    test_database_path = tmp_path / 'test_motorscope.db'
    monkeypatch.setattr(database, 'DATABASE_PATH', test_database_path)
    initialize_database()

    service = VehicleService(VehicleRepository())

    analyzed_vehicle = service.analyze_vehicle_listing(99)

    assert analyzed_vehicle is None

def test_analyze_vehicle_listing_model_year_is_current_year(tmp_path, monkeypatch):
    test_database_path = tmp_path / 'test_motorscope.db'
    monkeypatch.setattr(database, 'DATABASE_PATH', test_database_path)
    initialize_database()
    
    service = VehicleService(VehicleRepository())

    vehicle = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2026,
        mileage=145000,
        asking_price=26_000.00,
    )
    
    vehicle_id = service.add_vehicle_listing(vehicle)
    
    analyzed_vehicle = service.analyze_vehicle_listing(vehicle_id, 2026)

    assert analyzed_vehicle is not None
    assert analyzed_vehicle['vehicle_age'] == 0
    assert  analyzed_vehicle['average_annual_mileage'] is None
    assert analyzed_vehicle['mileage_assessment'] == 'Insufficient vehicle age for assessment.'


def test_analyze_vehicle_listing_assess_annual_mileage(tmp_path, monkeypatch):
    test_database_path = tmp_path / 'test_motorscope.db'
    monkeypatch.setattr(database, 'DATABASE_PATH', test_database_path)
    initialize_database()
    
    service = VehicleService(VehicleRepository())
    
    vehicle = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2012,
        mileage=315_000,
        asking_price=6200.00,
    )
    
    vehicle_id = service.add_vehicle_listing(vehicle)
    
    analyzed_vehicle = service.analyze_vehicle_listing(vehicle_id, 2026)

    assert analyzed_vehicle['mileage_assessment'] == 'Above average.'
