from app.cli import run_cli
from app.database import initialize_database
from app.repositories import VehicleRepository
from app.services import VehicleService

def main() -> None:
    '''Initialize and launch MotorScope.'''
    initialize_database()
    repo = VehicleRepository()
    service = VehicleService(repo)

    run_cli(service)

if __name__ == '__main__':
    main()