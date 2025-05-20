import re
import csv
import json
from tqdm import tqdm
from django.core.management.base import BaseCommand
from search.models import Restaurant, MenuItem


class Command(BaseCommand):
    help = "Import restaurant data from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the restaurants.csv file')
    
    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
            for row in tqdm(reader, desc='Importing restaurants'):
                try:
                    name = row['name']
                    location = row['location']

                    # lat_long split
                    lat_str, long_str = row['lat_long'].split(',')
                    latitude = float(lat_str.strip())
                    longitude = float(long_str.strip())

                    # parse full_details JSON
                    full_details = json.loads(row['full_details'])

                    address = full_details.get('location', {}).get('address')
                    city = full_details.get('location', {}).get('city')
                    cuisines = full_details.get('cuisines')
                    price_range = full_details.get('price_range')
                    average_cost = full_details.get('average_cost_for_two')
                    rating = full_details.get('user_rating',{}).get('aggregate_rating')
                    votes = full_details.get('user_rating',{}).get('votes')

                    restaurant = Restaurant.objects.create(
                        name=name,
                        location=location,
                        latitude=latitude,
                        longitude=longitude,
                        address=address,
                        city=city,
                        cuisines=cuisines,
                        price_range=price_range or None,
                        average_cost_for_two=average_cost or None,
                        user_rating=float(rating) if rating else None,
                        user_rating_votes=int(votes) if votes else None,
                    )

                    # parse menu items from items JSON string
                    items_json = row['items'].replace('""', '"').strip()
                    items_dict = json.loads(items_json)

                    for item_name, price_str in items_dict.items():
                        try:
                            # price = float(price_str.strip().replace("₹", "").replace("Rs.", "").replace(" ", ""))
                            price = self.extract_price(price_str)
                            MenuItem.objects.create(
                              restaurant=restaurant,
                              name=item_name.strip(),
                              price=price
                            )
                        except ValueError:
                            self.stdout.write(self.style.WARNING(f'Invalid price for "{item_name}": {price_str}'))
                    
                    self.stdout.write(self.style.SUCCESS(f'Imported: {restaurant.name}'))
                
                except Exception as e:
                    self.stderr.write(f'Error processing row ID {row["id"]}: {e}')
    
    def extract_price(self, value):
        # pulls first number that looks like price
        match = re.search(r'\d+(\.\d+)?', value)
        if match:
            return float(match.group())
        return None