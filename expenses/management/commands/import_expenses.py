import csv
from django.core.management.base import BaseCommand
from expenses.models import Expense
from datetime import datetime

class Command(BaseCommand):
    help = 'Import expenses from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)

    def handle(self, *args, **options):
        path = options['csv_path']
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                Expense.objects.update_or_create(
                    date=datetime.strptime(row['Date'], '%m-%d-%Y').date(),
                    vendor=row['Store / Vendor'],
                    exclude=(row['Escludi Spesa Da analysts'].lower() in ['true','1','yes']),
                    indispensable=(row['Spesa indispensabile'].lower() in ['true','1','yes']),
                    avoidable=(row['Spesa evitabile'].lower() in ['true','1','yes']),
                    amount=row['$ Amount'].replace(',', ''),
                    category=row['Expense Category'],
                    subcategory=row.get('SubCategory',''),
                    notes=row.get('Notes (Optional)','')
                )
        self.stdout.write(self.style.SUCCESS('Imported expenses from %s' % path))
