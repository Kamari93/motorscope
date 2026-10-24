from app.models import VehicleListing

def test_create_vehicle_listing():
    vehicle = VehicleListing(
        make = "Honda",
        model = "CR-V",
        year = 2012,
        mileage = 145000,
        asking_price = 6200.00,
    )

    assert vehicle.make == "Honda"
    assert vehicle.model == "CR-V"
    assert vehicle.year == 2012
    assert vehicle.mileage == 145000
    assert vehicle.asking_price == 6200.00

def test_optional_fields_default_to_none():
    vehicle = VehicleListing(
        make = "Honda",
        model = "CR-V",
        year = 2012,
        mileage = 145000,
        asking_price = 6200.00,
    )

    assert vehicle.listing_url == None
    assert vehicle.source_site == None
    assert vehicle.notes == None

def test_create_vehicle_listing_with_optional_fields():
    vehicle = VehicleListing(
        make = "Honda",
        model = "CR-V",
        year = 2012,
        mileage = 145000,
        asking_price = 6200.00,
        listing_url = "https://example.com/listings/456",
        source_site = "Example Motors",
        notes = "Clean title and no reported accidents",
        )

    assert vehicle.listing_url == "https://example.com/listings/456"
    assert vehicle.source_site == "Example Motors"
    assert vehicle.notes == "Clean title and no reported accidents"