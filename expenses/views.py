from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Sum
from datetime import date
from .models import Expense
from .filters import ExpenseFilter
from .utils import get_month_calendar

# Create your views here.


class ExpenseListView(LoginRequiredMixin, FilterView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    filterset_class = ExpenseFilter


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    fields = ['date', 'vendor', 'exclude', 'indispensable', 'avoidable', 'amount', 'category', 'subcategory', 'notes']
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:list')


class ExpenseChartView(LoginRequiredMixin, TemplateView):
    template_name = 'expenses/chart.html'


class ExpenseCalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'expenses/calendar.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        year  = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))
        
        # Calculate previous month/year
        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year
        
        # Calculate next month/year
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        
        ctx['calendar'] = get_month_calendar(year, month)
        ctx['year'] = year
        ctx['month'] = month
        ctx['prev_year'] = prev_year
        ctx['prev_month'] = prev_month
        ctx['next_year'] = next_year
        ctx['next_month'] = next_month
        return ctx


def expense_category_data(request):
    qs = Expense.objects.values('category').annotate(total=Sum('amount'))
    labels = [row['category'] for row in qs]
    data   = [float(row['total']) for row in qs]
    return JsonResponse({'labels': labels, 'data': data})
