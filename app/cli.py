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
    print("6. Analyze vehicle listing")
    print("7. Estimate annual maintenance")
    print("8. Estimate annual fuel expense")
    print("9. Estimate annual ownership expense")
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
        new_value = input(msg).strip()
        if not new_value:
            return current_val
        try:
            return int(new_value)
        except ValueError:
            print('Please enter a valid whole number.')

def prompt_optional_float(msg:str, current_val: float) -> float:
    '''Prompt for a float or retain the existing value.'''
    while True:
        new_value = input(msg).strip()
        if not new_value:
            return current_val
        try:
            return float(new_value)
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

def analyze_vehicle(service: VehicleService) -> None:
    '''Display analytical information for a vehicle listing.'''
    listing_id = prompt_int('Enter listing ID: ')

    analysis = service.analyze_vehicle_listing(listing_id)

    if analysis is None:
        print('Vehicle listing not found.')
        return

    print("\n--- Vehicle Analysis ---")
    print(f'Vehicle Age: {analysis['vehicle_age']} years')

    average_mileage = analysis['average_annual_mileage']

    if average_mileage is None:
        print('Average Annual Mileage: Insufficient data')
    else:
        print(f'Average Annual Mileage: {average_mileage:,.0f} miles')

    print(f'Mileage Assessment: {analysis['mileage_assessment']}')

def estimate_maintenance_cost(service: VehicleService):
    '''Display estimated annual maintenance costs.'''
    listing_id = prompt_int('Enter listing ID: ')

    try:
        estimate = service.estimate_annual_maintenance(listing_id)
        if estimate is None:
            print('Unable to estimate maintenance for this listing.')
            return 
    except ValueError as e:
            print(f'Invalid input: {e}')
            return 

    # if estimate is None:
    #     print('Unable to estimate maintenance for this listing.')
    #     return 

    print("\n--- Maintenance Estimate ---")
    print(f'Vehicle Age: {estimate['vehicle_age']} years')
    print(
        f'Average Annual Mileage: '
        f'{estimate['average_annual_mileage']:,.0f} miles'
    )
    print(
        f'Estimated Annual Maintenance: '
        f'${estimate['estimated_annual_maintenance']:,.2f}'
    )

def estimate_fuel_cost(service: VehicleService):
    '''Display estimated annual fuel costs.'''
    listing_id = prompt_int('Enter listing ID: ')
    mpg = prompt_float('Enter vehicle MPG: ')
    fuel_price = prompt_float('Enter fuel price per gallon: ')

    try:
        estimate = service.estimate_annual_fuel_cost(listing_id, mpg, fuel_price)
        if estimate is None:
            print('Unable to estimate fuel expenses for this listing.')
            return
    except ValueError as e:
        print(f'Invalid input: {e}')
        return 

    # if estimate is None:
    #     print('Unable to estimate fuel expenses for this listing.')
    #     return

    print("\nAnnual Fuel Cost Estimate")
    print("----------------------------")
    print(f'Vehicle Age: {estimate['vehicle_age']} years')
    print(f'Average annual mileage: {estimate['average_annual_mileage']:,.0f} miles')
    print(f'Estimated annual fuel cost: ${estimate['estimated_annual_fuel']:,.2f}')

def estimate_ownership_cost(service: VehicleService):
    '''Display the combined ownership estimate'''
    listing_id = prompt_int('Enter listing ID: ')
    mpg = prompt_float('Enter vehicle MPG: ')
    fuel_price = prompt_float('Enter fuel price per gallon: ')

    try:
        estimate = service.estimate_annual_ownership_cost(listing_id, mpg, fuel_price)
        if estimate is None:
            print('Unable to estimate ownership costs for this listing.')
            return
    except ValueError as e:
            print(f'Invalid input: {e}')
            return 

    # if estimate is None:
    #     print('Unable to estimate ownership costs for this listing.')
    #     return

    print('\nAnnual Ownership Cost Estimate')
    print("----------------------------")
    print(f'Vehicle Age: {estimate['vehicle_age']} years')
    print(f'Average annual mileage: {estimate['average_annual_mileage']:,.0f} miles')
    print(f'Annual maintenance: ${estimate['annual_maintenance']:,.2f}')
    print(f'Estimated annual fuel cost: ${estimate['annual_fuel']:,.2f}')
    print(f'Total annual cost: ${estimate['total_annual_cost']:,.2f}')
    print(f'Average monthly cost: ${estimate['average_monthly_cost']:,.2f}')



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
        elif choice == '6':
            analyze_vehicle(service)
        elif choice == '7':
            estimate_maintenance_cost(service)
        elif choice == '8':
            estimate_fuel_cost(service)
        elif choice == '9':
            estimate_ownership_cost(service)
        elif choice == '0':
            print('Thank you for using MotorScope!')
            break
        else:
            print('Invalid option. Please try again.')