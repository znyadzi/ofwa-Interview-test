import csv
from django.core.management.base import BaseCommand, CommandError
from django.db.models.functions import RowNumber

from ...models import GSiteData

class Command(BaseCommand):
    help = 'Import data from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        try:
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row if it exists

                for row in reader:
                    try:
                        # Try to convert Number_of_Galamsay_Sites to an integer
                        number_of_sites = int(row[2])

                        # Create or update the GSiteData entry
                        _, created = GSiteData.objects.get_or_create(
                            Town=row[0],
                            Region=row[1],
                            defaults={'Number_of_Galamsay_Sites': number_of_sites}
                        )
                        if created:
                            self.stdout.write(f'Successfully created record for {row[0]}')
                        if not created:
                            # If the entry already exists, update it
                            GSiteData.objects.filter(
                                Town=row[0],
                                Region=row[1]
                            ).update(Number_of_Galamsay_Sites=number_of_sites)
                            self.stdout.write(f'Updated the record for {row[0]}')

                    except ValueError:
                        # Skip rows where Number_of_Galamsay_Sites is not an integer
                        print(
                            f"Skipping row: Town={row[0]}, Region={row[1]}. Number_of_Galamsay_Sites is not an integer.")
                        continue

        except FileNotFoundError:
            raise CommandError(f"File '{csv_file}' not found.")
        except IndexError:
            raise CommandError("CSV file format incorrect. Ensure it has at least three columns: Town, Region, Number_of_Galamsay_Sites.")
        except ValueError:
            raise CommandError("Invalid 'Number_of_Galamsay_Sites' value. Ensure it's an integer.")