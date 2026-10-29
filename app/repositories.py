import sqlite3
from app.models import VehicleListing
from app.database import get_connection

'''handles saving and retrieving listings'''

class VehicleRepository:
    """Manage vehicle listing persistence."""
    def add(self, vehicle: VehicleListing) -> int:
        '''Save a vehicle listing and return its database ID.'''
        with get_connection() as connection:
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

    def get_all(self) -> list[VehicleListing]:
        '''Retrieve all vehicle listings.'''
        with get_connection() as connection:
            rows = connection.execute(
                '''
                SELECT
                    id,
                    make,
                    model,
                    year,
                    mileage,
                    asking_price,
                    listing_url,
                    source_site,
                    notes
                FROM vehicle_listings 
                ORDER BY id
                '''
            ).fetchall()
        
        return [
            # convert each row back into a vehicle object
            VehicleListing(
                make = row['make'],
                model = row['model'],
                year = row['year'],
                mileage = row['mileage'],
                asking_price = row['asking_price'],
                listing_url = row['listing_url'],
                source_site = row['source_site'],
                notes = row['notes'],
                id = row['id'],
            )
            for row in rows
        ]

    def get_vehicle_by_id(self, listing_id: int) -> VehicleListing | None:
        '''Retrieve a vehicle listing by its ID.'''
        with get_connection() as connection:
            row = connection.execute(
                '''
                SELECT
                    id,
                    make,
                    model,
                    year,
                    mileage,
                    asking_price,
                    listing_url,
                    source_site,
                    notes
                FROM vehicle_listings
                WHERE id = ?
                ''',
                (listing_id, ),
            ).fetchone()

        if row is None:
            return None

        return VehicleListing(
            make = row['make'],
            model = row['model'],
            year = row['year'],
            mileage = row['mileage'],
            asking_price = row['asking_price'],
            listing_url = row['listing_url'],
            source_site = row['source_site'],
            notes = row['notes'],
            id = row['id'],
        )

    def update(self, listing_id: int, vehicle: VehicleListing) -> bool:
        '''Update an existing listing and report whether it existed.'''
        with get_connection() as connection:
            cursor = connection.execute(
                '''
                UPDATE vehicle_listings
                SET
                    make = ?,
                    model = ?,
                    year = ?,
                    mileage = ?,
                    asking_price = ?,
                    listing_url = ?,
                    source_site = ?,
                    notes = ?
                WHERE id = ?
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
                    listing_id,
                ),
            )

        # return True if a row was updated and False if the specified ID from WHERE kwd wasn’t found
        return cursor.rowcount > 0

    def delete(self, listing_id: int) -> bool:
        '''Delete a listing and report whether it existed.'''
        with get_connection() as connection:
           cursor = connection.execute(
               '''
                DELETE FROM vehicle_listings
                WHERE id = ?
               ''',
               (listing_id, ),
        )

        # return True if a row was affected, otherwise return False.
        return cursor.rowcount > 0