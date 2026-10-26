import sqlite3
from pathlib import Path
from contextlib import contextmanager # decorator lets us implement the connection lifecycle using yield
from collections.abc import Generator # tells static type checkers that the annotated object can yield elements one by one when passed to the next() function

'''manages database connections and table initialization.'''

# Convert DATABASE_PATH from a string to a Path object
DATABASE_PATH = Path("data/motorscope.db") # defines where the local database will live

@contextmanager # makes get_connection a context manager that commits successful operations, rolls back failed ones, and always closes the connection
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    '''Provide a database connection and manage its lifecycle.'''
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True) # create data dir if it doesn't already exists
    connection = sqlite3.connect(DATABASE_PATH) # open connection to db
    connection.row_factory = sqlite3.Row # allows access to returned db columns by name ie row["model"]

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    #  ensures the connection closes even if an operation fails
    finally:
        connection.close()


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


# DATABASE_PATH = "data/motorscope.db" # defines where the local database will live
# def get_connection() -> sqlite3.Connection:
#     '''Connect to the MotorScope database.'''
#     # Convert DATABASE_PATH from a string to a Path object
#     Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True) # create data dir if it doesn't already exists
#     connection = sqlite3.connect(DATABASE_PATH) # open connection to db
#     connection.row_factory = sqlite3.Row # allows access to returned db columns by name ie row["model"]

#     return connection