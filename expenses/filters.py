import django_filters
from .models import Expense


class ExpenseFilter(django_filters.FilterSet):
    date_after = django_filters.DateFilter(field_name='date', lookup_expr='gte', label='Date After', method='filter_date_after')
    date_before = django_filters.DateFilter(field_name='date', lookup_expr='lte', label='Date Before', method='filter_date_before')
    amount_min = django_filters.NumberFilter(field_name='amount', lookup_expr='gte', label='Min Amount', method='filter_amount_min')
    amount_max = django_filters.NumberFilter(field_name='amount', lookup_expr='lte', label='Max Amount', method='filter_amount_max')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def filter_date_after(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(date__gte=value)

    def filter_date_before(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(date__lte=value)

    def filter_amount_min(self, queryset, name, value):
        if not value or value == '':
            return queryset
        return queryset.filter(amount__gte=value)

    def filter_amount_max(self, queryset, name, value):
        if not value or value == '':
            return queryset
        return queryset.filter(amount__lte=value)

    class Meta:
        model = Expense
        fields = ['date_after', 'date_before', 'amount_min', 'amount_max'] 