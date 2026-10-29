from app import database
from app.database import initialize_database
from app.models import VehicleListing
from app.repositories import VehicleRepository


def test_add_and_retrieve_listing(tmp_path, monkeypatch):
    # Pytest provides tmp_path, a temporary directory unique to the test.
    test_database_path = tmp_path / "test_motorscope.db"

    # temporarily replaces the configured path for the test. Pytest automatically restores it afterward.
    # makes our test repeatable and helps keep test data separate from real vehicle listings.
    monkeypatch.setattr(
        database,
        "DATABASE_PATH",  # redirect DATABASE_PATH to a temporary database so the test doesn’t modify the real data/motorscope.db.
        test_database_path,
    )

    # create the vehicle listings db table for testing
    initialize_database()

    # repo instance to connect to temp db for creation and retrieval 
    repo = VehicleRepository()

    vehicle = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2012,
        mileage=145000,
        asking_price=6200.00,
        listing_url="https://example.com/listing/123",
        source_site="Example Motors",
        notes="Service history not yet verified.",
    )

    listing_id = repo.add(vehicle)
    listings = repo.get_all()

    assert listing_id == 1
    assert len(listings) == 1

    saved_vehicle = listings[0]

    assert saved_vehicle.make == "Honda"
    assert saved_vehicle.model == "CR-V"
    assert saved_vehicle.year == 2012
    assert saved_vehicle.mileage == 145000
    assert saved_vehicle.asking_price == 6200.00
    assert saved_vehicle.listing_url == "https://example.com/listing/123"
    assert saved_vehicle.source_site == "Example Motors"
    assert saved_vehicle.notes == "Service history not yet verified."
    assert saved_vehicle.id == listing_id

def test_get_by_id_returns_vehicle_listing(tmp_path, monkeypatch):
    test_database_path = tmp_path / "test_motorscope.db"

    monkeypatch.setattr(
            database,
            "DATABASE_PATH", # redirect DATABASE_PATH to a temporary database so the test doesn’t modify the real data/motorscope.db.
            test_database_path,
        )

    # create the vehicle listings db table for testing
    initialize_database()
    
    # repo instance to connect to temp db for creation and retrieval 
    repo = VehicleRepository()

    vehicle = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2012,
        mileage=145000,
        asking_price=6200.00,
    )

    listing_id = repo.add(vehicle)
    listings = repo.get_all()

    assert listing_id == 1
    assert len(listings) == 1

    result = repo.get_vehicle_by_id(listing_id)

    assert result is not None
    assert result.make == 'Honda'
    assert result.model == 'CR-V'
    assert result.year == 2012
    assert result.id == listing_id
    

def test_get_by_id_returns_none_when_missing(tmp_path, monkeypatch):
    test_database_path = tmp_path / "test_motorscope.db"
    
    monkeypatch.setattr(
        database,
        "DATABASE_PATH", # redirect DATABASE_PATH to a temporary database so the test doesn’t modify the real data/motorscope.db.
        test_database_path,
    )
    
    # create the vehicle listings db table for testing
    initialize_database()
    
    # repo instance to connect to temp db for creation and retrieval 
    repo = VehicleRepository()

    result = repo.get_vehicle_by_id(999)

    assert result == None

def test_update_vehicle_listing(tmp_path, monkeypatch):
    test_database_path = tmp_path / "test_motorscope.db"
        
    monkeypatch.setattr(
        database,
        "DATABASE_PATH", # redirect DATABASE_PATH to a temporary database so the test doesn’t modify the real data/motorscope.db.
        test_database_path,
    )
    
    # create the vehicle listings db table for testing
    initialize_database()
    
    # repo instance to connect to temp db for creation and retrieval 
    repo = VehicleRepository()

    original = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2012,
        mileage=145000,
        asking_price=6200.00,
    )

    listing_id = repo.add(original)

    updated = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2012,
        mileage=145000,
        asking_price=5800.00,
        notes="Seller reduced the price.",
    )

    assert repo.update(listing_id, updated) is True
    result = repo.get_vehicle_by_id(listing_id)
    assert result is not None
    assert result.asking_price == 5800.00
    assert result.notes == 'Seller reduced the price.'


def test_update_returns_false_when_missing(tmp_path, monkeypatch):
    test_database_path = tmp_path / "test_motorscope.db"
            
    monkeypatch.setattr(
        database,
        "DATABASE_PATH", # redirect DATABASE_PATH to a temporary database so the test doesn’t modify the real data/motorscope.db.
        test_database_path,
    )
    
    # create the vehicle listings db table for testing
    initialize_database()
    
    # repo instance to connect to temp db for creation and retrieval 
    repo = VehicleRepository()

    listing_id = 999

    updated = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2012,
        mileage=145000,
        asking_price=5800.00,
        notes="Seller reduced the price.",
        )

    assert repo.update(listing_id, updated) is False

def test_delete_vehicle_listing(tmp_path, monkeypatch):
    test_database_path = tmp_path / "test_motorscope.db"
    monkeypatch.setattr(
        database,
        "DATABASE_PATH",  # redirect DATABASE_PATH to a temporary database so the test doesn’t modify the real data/motorscope.db.
        test_database_path,
    )

    initialize_database()
    repo = VehicleRepository()

    vehicle = VehicleListing(
        make="Honda",
        model="CR-V",
        year=2012,
        mileage=145000,
        asking_price=6200.00,
    )

    listing_id = repo.add(vehicle)
    
    assert repo.delete(listing_id) is True
    assert repo.get_vehicle_by_id(listing_id) is None

def test_delete_returns_false_when_missing(tmp_path, monkeypatch):
    test_database_path = tmp_path / "test_motorscope.db"
    monkeypatch.setattr(
        database,
        "DATABASE_PATH",  # redirect DATABASE_PATH to a temporary database so the test doesn’t modify the real data/motorscope.db.
        test_database_path,
    )

    initialize_database()
    repo = VehicleRepository()

    assert repo.delete(999) is False
