import csv
from route_planner.models import Truckstop

def import_truckstops(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:

            existing_truckstop = Truckstop.objects.filter(
                opis_id=row['OPIS Truckstop ID'],
                name=row['Truckstop Name'],
                address=row['Address'],
                city=row['City'],
                state=row['State']
            ).first()

            if not existing_truckstop:

                Truckstop.objects.create(
                    opis_id=row['OPIS Truckstop ID'],
                    name=row['Truckstop Name'],
                    address=row['Address'],
                    city=row['City'],
                    state=row['State'],
                    rack_id=row['Rack ID'],
                    retail_price=row['Retail Price']
                )
            else:
                print(f"Truckstop {row['Truckstop Name']} already exists.")

    print("Data imported successfully!")

