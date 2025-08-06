from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Min, Max
from datetime import date
from .models import Expense, UserCategory, UserSubcategory
from .filters import ExpenseFilter
from .utils import get_month_calendar
from .forms import ExpenseForm

# Create your views here.


class ExpenseListView(LoginRequiredMixin, FilterView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    filterset_class = ExpenseFilter
    
    def get_queryset(self):
        return Expense.objects.for_user(self.request.user)
    
    def get_filterset_queryset(self, queryset):
        # Ensure the filterset uses the user-scoped queryset
        return queryset
    
    def get_filterset(self, queryset=None):
        filterset = super().get_filterset(queryset)
        if filterset:
            # Get the actual queryset for setting filter choices
            actual_queryset = self.get_queryset()
            
            # Set the choices for vendor and category filters
            vendors = list(actual_queryset.values_list('vendor', flat=True).distinct().order_by('vendor'))
            categories = list(actual_queryset.values_list('category', flat=True).distinct().order_by('category'))
            
            # Only set choices if we have data
            if vendors:
                filterset.filters['vendor'].choices = [(v, v) for v in vendors]
            if categories:
                filterset.filters['category'].choices = [(c, c) for c in categories]
        
        return filterset
    

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the base queryset (unfiltered) for calculating stats and choices
        base_queryset = self.get_queryset()
        
        # Get the filtered queryset for the current filters
        filtered_queryset = context.get('object_list', base_queryset)
        
        # Calculate total amount from filtered results
        context['total_amount'] = filtered_queryset.aggregate(total=Sum('amount'))['total'] or 0
        
        # Calculate min/max amounts for slider from base queryset (all available data)
        amount_stats = base_queryset.aggregate(
            min_amount=Min('amount'),
            max_amount=Max('amount')
        )
        context['min_amount'] = amount_stats['min_amount'] or 0
        context['max_amount'] = amount_stats['max_amount'] or 1000
        
        # Get unique vendors and categories from base queryset (all available options)
        vendors = list(base_queryset.values_list('vendor', flat=True).distinct().order_by('vendor'))
        categories = list(base_queryset.values_list('category', flat=True).distinct().order_by('category'))
        
        context['vendors'] = vendors
        context['categories'] = categories
        
        # Update filter choices only if we have data
        if vendors:
            context['filter'].filters['vendor'].choices = [(v, v) for v in vendors]
        if categories:
            context['filter'].filters['category'].choices = [(c, c) for c in categories]
        

        
        return context


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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
        
        ctx['calendar'] = get_month_calendar(year, month, self.request.user)
        ctx['year'] = year
        ctx['month'] = month
        ctx['prev_year'] = prev_year
        ctx['prev_month'] = prev_month
        ctx['next_year'] = next_year
        ctx['next_month'] = next_month
        return ctx


def expense_category_data(request):
    qs = Expense.objects.for_user(request.user).values('category').annotate(total=Sum('amount'))
    labels = [row['category'] for row in qs]
    data   = [float(row['total']) for row in qs]
    return JsonResponse({'labels': labels, 'data': data})

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            category, created = UserCategory.objects.get_or_create(
                user=request.user,
                name=name
            )
            return JsonResponse({
                'success': True,
                'id': category.id,
                'name': category.name,
                'created': created
            })
        return JsonResponse({'success': False, 'error': 'Category name is required'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def add_subcategory(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category_name = request.POST.get('category', '').strip()
        
        if name and category_name:
            try:
                category = UserCategory.objects.get(user=request.user, name=category_name)
                subcategory, created = UserSubcategory.objects.get_or_create(
                    user=request.user,
                    category=category,
                    name=name
                )
                return JsonResponse({
                    'success': True,
                    'id': subcategory.id,
                    'name': subcategory.name,
                    'created': created
                })
            except UserCategory.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Category not found'})
        return JsonResponse({'success': False, 'error': 'Subcategory name and category are required'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('expenses:list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after successful registration
        login(self.request, self.object)
        messages.success(self.request, 'Account created successfully! Welcome to Finance Tracker.')
        return response
