import sqlite3
from app.models import VehicleListing
from app.database import get_connection

'''handles saving and retrieving listings'''

class VehicleRepository:
    """Manage vehicle listing persistence."""
    def add(self, vehicle: VehicleListing) -> int:
        '''Save a vehicle listing and return its database ID.'''
        with get_connection as connection:
            cursor = connection.execute(
                '''
                INSERT INTO vehicle_listings (
                make,
                model,
                year,
                mileage,
                asking_price,
                listing_url,
                source_site,
                notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    vehicle.make,
                    vehicle.model,
                    vehicle.year,
                    vehicle.mileage,
                    vehicle.asking_price,
                    vehicle.listing_url,
                    vehicle.source_site,
                    vehicle.notes,
                ),
            )
            
            return int(cursor.lastrowid)