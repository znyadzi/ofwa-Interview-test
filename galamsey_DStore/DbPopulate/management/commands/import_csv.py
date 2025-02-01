import csv
from django.core.management.base import BaseCommand, CommandError
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
                    _, created = GSiteData.objects.get_or_create(
                        Town=row[0],
                        Region=row[1],
                        Number_of_Galamsay_Sites=int(row[2]) # Convert to integer
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully imported site data for {row[0]}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'The data for {row[0]} already exists'))
        except FileNotFoundError:
            raise CommandError(f"File '{csv_file}' not found.")
        except IndexError:
            raise CommandError("CSV file format incorrect. Ensure it has at least three columns: Town, Region, Number_of_Galamsay_Sites.")
        except ValueError:
            raise CommandError("Invalid 'Number_of_Galamsay_Sites' value. Ensure it's an integer.")