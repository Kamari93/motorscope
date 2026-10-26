import sqlite3
from pathlib import Path

'''manages database connections and table initialization.'''

DATABASE_PATH = "data/motorscope.db" # defines where the local database will live

def get_connection() -> sqlite3.Connection:
    '''Connect to the MotorScope database.'''
    # Convert DATABASE_PATH from a string to a Path object
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True) # create data dir if it doesn't already exists
    connection = sqlite3.connect(DATABASE_PATH) # open connection to db
    connection.row_factory = sqlite3.Row # allows access to returned db columns by name ie row["model"]

    return connection

def initialize_database() -> None:
    '''Create the vehicle listings db table if it doesn't exist.'''
    with get_connection() as connection:
        connection.execute(
            '''
            CREATE TABLE IF NOT EXISTS vehicle_listings (
            id INTEGER PRIMARY KEY,
            make TEXT NOT NULL,
            Model TEXT NOT NULL,
            year INTEGER NOT NULL,
            mileage INTEGER NOT NULL,
            asking_price REAL NOT NULL,
            listing_url TEXT,
            source_site TEXT,
            notes TEXT
            )
            '''
        )
