import calendar
from datetime import date
from decimal import Decimal
from django.db.models import Sum
from .models import Expense

def get_month_calendar(year: int, month: int):
    # Build a matrix of dates for the month, weeks start on Monday
    cal = calendar.Calendar(firstweekday=0)
    # Aggregate totals per date
    qs = (
        Expense.objects
        .filter(date__year=year, date__month=month)
        .values('date')
        .annotate(total=Sum('amount'))
    )
    totals = {item['date']: item['total'] or Decimal('0.00') for item in qs}

    month_matrix = []
    for week in cal.monthdatescalendar(year, month):
        week_row = []
        for dt in week:
            if dt.month == month:
                week_row.append({
                    'day': dt.day,
                    'date': dt,
                    'total': totals.get(dt, Decimal('0.00'))
                })
            else:
                week_row.append({'day': 0, 'date': None, 'total': Decimal('0.00')})
        month_matrix.append(week_row)
    return month_matrix 