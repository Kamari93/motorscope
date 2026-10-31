from app import database
from app.database import initialize_database
from app.models import VehicleListing
from app.repositories import VehicleRepository
from app.services import VehicleService

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
    
    vehicle = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2012,
        mileage=145000,
        asking_price=6200.00,
    )

    vehicle_id = service.add_vehicle_listing(vehicle)

    assert service.delete_vehicle_listing(vehicle_id) is True
    assert service.get_vehicle_listing_by_id(vehicle_id) is None