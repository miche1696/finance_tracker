import django_filters
from .models import Expense


class ExpenseFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()
    category = django_filters.CharFilter(lookup_expr='icontains')
    amount = django_filters.NumericRangeFilter()

    class Meta:
        model = Expense
        fields = ['date', 'category', 'amount'] 