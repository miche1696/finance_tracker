import calendar
from datetime import date
from decimal import Decimal
from django.db.models import Sum
from .models import Expense

def get_month_calendar(year: int, month: int, user=None):
    # Build a matrix of dates for the month, weeks start on Monday
    cal = calendar.Calendar(firstweekday=0)
    # Aggregate totals per date
    if user:
        qs = Expense.objects.for_user(user).filter(date__year=year, date__month=month)
    else:
        qs = Expense.objects.filter(date__year=year, date__month=month)
    qs = qs.values('date').annotate(total=Sum('amount'))
    totals = {item['date']: item['total'] or Decimal('0.00') for item in qs}

    # Get all expenses for the month to include in calendar cells
    if user:
        all_expenses = Expense.objects.for_user(user).filter(date__year=year, date__month=month)
    else:
        all_expenses = Expense.objects.filter(date__year=year, date__month=month)
    
    # Group expenses by date
    expenses_by_date = {}
    for expense in all_expenses:
        if expense.date not in expenses_by_date:
            expenses_by_date[expense.date] = []
        expenses_by_date[expense.date].append(expense)

    month_matrix = []
    for week in cal.monthdatescalendar(year, month):
        week_row = []
        for dt in week:
            if dt.month == month:
                week_row.append({
                    'day': dt.day,
                    'date': dt,
                    'total': totals.get(dt, Decimal('0.00')),
                    'expenses': expenses_by_date.get(dt, [])
                })
            else:
                week_row.append({'day': 0, 'date': None, 'total': Decimal('0.00'), 'expenses': []})
        month_matrix.append(week_row)
    return month_matrix 