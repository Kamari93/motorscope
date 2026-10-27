from app import database
from app.database import initialize_database
from app.models import VehicleListing
from app.repositories import VehicleRepository

def test_add_and_retrieve_vehicle_listing(tmp_path, monkeypatch):
    # Pytest provides tmp_path, a temporary directory unique to the test.
    test_database_path = tmp_path / "test_motorscope.db"

    # temporarily replaces the configured path for the test. Pytest automatically restores it afterward.
    # makes our test repeatable and helps keep test data separate from real vehicle listings.
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


