from app.models import VehicleListing
from app.services import VehicleService

'''The CLI will communicate with VehicleService, not directly with the repository or database.'''
'''The CLI passes a vehicle object to the service. The service delegates persistence to the repository. This keeps database logic out of the user interface.'''

def display_menu() -> None:
    """Display the main MotorScope menu."""
    print("\n========== MotorScope ==========")
    print("1. Add vehicle listing")
    print("2. View all listings")
    print("3. View listing details")
    print("4. Update listing")
    print("5. Delete listing")
    print("0. Exit")
    print("================================")

def prompt_int(msg: str) -> int:
    '''Prompt the user for an integer.'''
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print('Please enter a valid whole number.')

def prompt_float(msg: str) -> float:
    '''Prompt the user for a float.'''
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print('Please enter a valid number.')

def prompt_optional_int(msg: str, current_val: int) -> int:
    '''Prompt for an integer or retain the existing value.'''
    while True:
        value = input(msg).strip()
        if not value:
            return current_val
        try:
            return int(input(msg))
        except ValueError:
            print('Please enter a valid whole number.')

def prompt_optional_float(msg:str, current_val: float) -> float:
    '''Prompt for a float or retain the existing value.'''
    while True:
        value = input(msg).strip()
        if not value:
            return current_val
        try:
            return float(input(msg))
        except ValueError:
            print('Please enter a valid number.')

def add_vehicle(service: VehicleService) -> None:
    '''Collect vehicle information and save a listing.'''
    print("\n--- Add Vehicle Listing ---")

    vehicle = VehicleListing(
        make = input('Make: ').strip(),
        model = input('Model: ').strip(),
        year = prompt_int('Year: '),
        mileage = prompt_int('Mileage: '),
        asking_price = prompt_float('Asking Price: '),
        listing_url = input('Listing URL (optional): ').strip() or None,
        source_site = input('Source Site (optional): ').strip() or None,
        notes = input('Notes (optional): ').strip() or None,

    )

    # listing_id = service.add_vehicle_listing(vehicle)
    # print(f'\nVehicle listing saved successfully. ID: {listing_id}')

    try:
        listing_id = service.add_vehicle_listing(vehicle)
        print(f'\nVehicle listing saved successfully. ID: {listing_id}')
    except ValueError as e:
        print(f'Invalid vehicle information: {e}')

def view_all_vehicles(service: VehicleService) -> None:
    '''Display all saved vehicle listings.'''
    print("\n--- Vehicle Listings ---")

    vehicles = service.get_all_vehicle_listings()

    if not vehicles:
        print('No vehicle listings found.')
        return 

    for vehicle in vehicles:
        print(
            f'ID: {vehicle.id} | '
            f'{vehicle.year} {vehicle.make} {vehicle.model} | '
            f'{vehicle.mileage:,} miles | '
            f'${vehicle.asking_price:,.2f}'
        )

def view_vehicle(service: VehicleService) -> None:
    '''Display details for a specific listing.'''
    listing_id = prompt_int('Enter listing ID: ')

    vehicle = service.get_vehicle_listing_by_id(listing_id)

    if not vehicle:
        print('Vehicle listing not found.')
        return

    print("\n--- Vehicle Details ---")
    print(f'ID: {vehicle.id}')
    print(f'Vehicle: {vehicle.year} {vehicle.make} {vehicle.model}')
    print(f'Mileage: {vehicle.mileage:,}')
    print(f'Asking Price: {vehicle.asking_price:,.2f}')
    print(f'Listing URL: {vehicle.listing_url or 'Not Provided'}')
    print(f'Source: {vehicle.source_site or 'Not Provided'}')
    print(f'Notes: {vehicle.notes or 'None'}')

def update_vehicle(service: VehicleService) -> None:
    '''Update an existing vehicle listing.'''
    listing_id = prompt_int('Enter listing ID: ')
    
    existing = service.get_vehicle_listing_by_id(listing_id)
    
    if not existing:
        print('Vehicle listing not found.')
        return

    print("\nPress Enter to keep an existing value.")

    make = input(f'Make [{existing.make}]: ').strip() or existing.make
    model = input(f'Model [{existing.model}]: ').strip() or existing.model

    # year_input = input(f'Year [{existing.year}]: ').strip()
    # year = int(year_input) if year_input else existing.year
    year = prompt_optional_int(f'Year [{existing.year}]: ', existing.year)

    # mileage_input = input(f'Mileage [{existing.mileage}]: ').strip()
    # mileage = int(mileage_input) if mileage_input else existing.mileage
    mileage = prompt_optional_int(f'Mileage [{existing.mileage}]: ', existing.mileage)

    # price_input = input(f'Asking Price [{existing.asking_price}]: ').strip()
    # asking_price = float(price_input) if price_input else existing.asking_price
    asking_price = prompt_optional_float(f'Asking Price [{existing.asking_price}]: ', existing.asking_price)

    listing_url = (
        input(f'Listing URL [{existing.listing_url or 'None'}]: ').strip() or 
        existing.listing_url
    )

    source_site = (
        input(f'Souce Site [{existing.source_site or 'None'}]: ').strip() or 
        existing.source_site
        )

    notes = input(f'Notes [{existing.notes or 'None'}]: ').strip() or existing.notes

    updated_vehicle = VehicleListing(
        make = make,
        model = model,
        year = year,
        mileage = mileage,
        asking_price = asking_price,
        listing_url = listing_url,
        source_site = source_site,
        notes = notes,
        id = listing_id
    )

    # if service.update_vehicle_listing(listing_id, updated_vehicle):
    #     print('Vehicle listing updated successfully.')
    # else:
    #     print('Unable to update vehicle listing.')

    try:
        if service.update_vehicle_listing(listing_id, updated_vehicle):
            print('Vehicle listing updated successfully.')
        else:
            print('Unable to update vehicle listing.')
    except ValueError as e:
        print(f'Invalid vehicle information: {e}')

def delete_vehicle(service: VehicleService) -> None:
    '''Delete a vehicle listing.'''
    listing_id = prompt_int('Enter listing ID: ')
    
    vehicle = service.get_vehicle_listing_by_id(listing_id)
    
    if not vehicle:
        print('Vehicle listing not found.')
        return

    print(f'\nYou are about to delete: {vehicle.year} {vehicle.make} {vehicle.model}')
    confirm = input('Are you sure? (y/n)').strip().lower()

    if confirm == 'y':
        if service.delete_vehicle_listing(listing_id):
            print('Vehicle listing deleted successfully.')
        else:
            print('Unable to delete vehicle listing.')
    else:
        print('Deletion cancelled.')

def run_cli(service: VehicleService) -> None:
    '''Run the MotorScope command-line interface.'''
    while True:
        display_menu()
        choice = input('Choose an option: ').strip()

        if choice == '1':
            add_vehicle(service)
        elif choice == '2':
            view_all_vehicles(service)
        elif choice == '3':
            view_vehicle(service)
        elif choice == '4':
            update_vehicle(service)
        elif choice == '5':
            delete_vehicle(service)
        elif choice == '0':
            print('Thank you for using MotorScope!')
            break
        else:
            print('Invalid option. Please try again.')