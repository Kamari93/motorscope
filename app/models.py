from dataclasses import dataclass

''' defines what a vehicle listing looks like.'''
@dataclass
class VehicleListing:
    make: str
    model: str
    year: int
    mileage: int
    asking_price: float
    # optional and default to None
    listing_url: str | None = None
    source_site: str | None = None
    notes: str | None = None
    id: int | None = None
