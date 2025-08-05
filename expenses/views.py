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
        ctx['calendar'] = get_month_calendar(year, month)
        ctx['year']     = year
        ctx['month']    = month
        return ctx


def expense_category_data(request):
    qs = Expense.objects.values('category').annotate(total=Sum('amount'))
    labels = [row['category'] for row in qs]
    data   = [float(row['total']) for row in qs]
    return JsonResponse({'labels': labels, 'data': data})
