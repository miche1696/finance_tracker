import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from expenses.models import Expense
from datetime import datetime

class Command(BaseCommand):
    help = 'Import expenses from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)
        parser.add_argument('--username', type=str, required=True, help='Username to assign expenses to')

    def handle(self, *args, **options):
        path = options['csv_path']
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist. Please create the user first.')
            )
            return
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            
            # Debug: Print column names to see what we're working with
            self.stdout.write(f"CSV columns: {list(reader.fieldnames)}")
            
            for row in reader:
                # Parse date from DD/MM/YY format to YYYY-MM-DD
                date_str = row['Date (MM-DD-YYYY)']
                if '/' in date_str:
                    # Handle DD/MM/YY format
                    day, month, year = date_str.split('/')
                    # Convert 2-digit year to 4-digit year (assuming 20xx for years 00-99)
                    if len(year) == 2:
                        year = '20' + year
                    # Reformat to MM-DD-YYYY for datetime parsing
                    date_str = f"{month}-{day}-{year}"
                
                try:
                    date_obj = datetime.strptime(date_str, '%m-%d-%Y').date()
                except ValueError as e:
                    self.stdout.write(
                        self.style.ERROR(f'Invalid date format: {row["Date (MM-DD-YYYY)"]} - {e}')
                    )
                    continue
                
                # Parse amount - handle multiple amount columns and find the non-zero one
                amount = 0.0
                amount_columns = ['$ Amount', 'INDISPENSABILE', 'EVITABILE']
                
                for col in amount_columns:
                    if col in row and row[col]:
                        amount_str = str(row[col]).replace('$', '').replace(',', '').replace('--', '0')
                        try:
                            temp_amount = float(amount_str)
                            if temp_amount > 0:
                                amount = temp_amount
                                break
                        except ValueError:
                            continue
                
                if amount == 0.0:
                    self.stdout.write(
                        self.style.WARNING(f'No valid amount found for: {row["Store / Vendor"]} on {date_obj}')
                    )
                    continue
                
                # Determine category based on flag columns
                category = row['Expense Category']
                if not category or category.strip() == '':
                    # Auto-determine category based on flags
                    if row['Holidays'].upper() == 'TRUE':
                        category = 'Holidays'
                    elif row['Regali'].upper() == 'TRUE':
                        category = 'Regali'
                    elif row['Mediche'].upper() == 'TRUE':
                        category = 'Mediche'
                    elif row['Abbigl.'].upper() == 'TRUE':
                        category = 'Abbigliamento'
                    elif row['Bollette'].upper() == 'TRUE':
                        category = 'Bollette'
                    elif row['Affitto'].upper() == 'TRUE':
                        category = 'Affitto'
                    else:
                        category = 'Other'
                
                # Handle vendor field - some rows have empty vendor
                vendor = row['Store / Vendor']
                if not vendor or vendor.strip() == '':
                    vendor = 'Unknown Vendor'
                
                Expense.objects.update_or_create(
                    date=date_obj,
                    vendor=vendor,
                    user=user,
                    exclude=(row['Escludi'].upper() in ['TRUE', '1', 'YES']),
                    indispensable=(row['INDISPENSABILE'].upper() in ['TRUE', '1', 'YES']),
                    avoidable=(row['EVITABILE'].upper() in ['TRUE', '1', 'YES']),
                    amount=amount,
                    category=category,
                    subcategory=row.get('SubCategory', ''),
                    notes=row.get('Notes (Optional)', '')
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Imported: {date_obj} - {vendor} - €{amount}')
                )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully imported expenses from {path}'))
