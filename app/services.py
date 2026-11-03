from app.models import VehicleListing
from app.repositories import VehicleRepository
from datetime import date

'''Coordinate vehicle listing operations and business rules'''

class VehicleService:
    def __init__(self, repository: VehicleRepository) -> None:
        '''Constructor utilizing dependency injection'''
        self.repo = repository

    @staticmethod
    def _validate_vehicle(vehicle: VehicleListing) -> None:
        '''Validate vehicle listing data.'''
        if not vehicle.make.strip():
            raise ValueError('Vehicle make cannot be empty.')
        if not vehicle.model.strip():
            raise ValueError('Vehicle model cannot be empty.')
        if vehicle.year < 1886 or vehicle.year > date.today().year + 1:
            raise ValueError('Vehicle year is invalid.')
        if vehicle.mileage < 0:
            raise ValueError('Mileage cannot be negative.')
        if vehicle.asking_price < 0:
            raise ValueError('Asking price cannot be negative.')
        
    def add_vehicle_listing(self, vehicle: VehicleListing) -> int:
        '''Save a vehicle listing and return its ID.'''
        self._validate_vehicle(vehicle)
        return self.repo.add(vehicle)

    def get_all_vehicle_listings(self) -> list[VehicleListing]:
        '''Return all saved vehicle listings.'''
        return self.repo.get_all()

    def get_vehicle_listing_by_id(self, vehicle_id: int) -> VehicleListing | None:
        '''Return a specific listing, if it exists.'''
        return self.repo.get_vehicle_by_id(vehicle_id)

    def update_vehicle_listing(self, listing_id: int, vehicle: VehicleListing) -> bool:
        '''Update an existing listing.'''
        self._validate_vehicle(vehicle)
        return self.repo.update(listing_id, vehicle)

    def delete_vehicle_listing(self, listing_id: int) -> bool:
        '''Delete an existing listing.'''
        return self.repo.delete(listing_id)