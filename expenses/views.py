from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Min, Max
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.management import call_command
from django.conf import settings
import os
import csv
import tempfile
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
            print(actual_queryset)
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


def delete_expense(request, expense_id):
    """Delete an expense with confirmation"""
    if request.method == 'POST':
        expense = get_object_or_404(Expense, id=expense_id, user=request.user)
        expense.delete()
        messages.success(request, f'Expense "{expense.vendor}" for ${expense.amount} has been deleted successfully.')
        return redirect('expenses:list')
    else:
        # If not POST, redirect to list view
        return redirect('expenses:list')


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:list')
    
    def get_object(self, queryset=None):
        """Get the expense object, ensuring it belongs to the current user"""
        return get_object_or_404(Expense, id=self.kwargs['expense_id'], user=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'Expense "{form.instance.vendor}" has been updated successfully.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        context['expense'] = self.object
        return context


def import_expenses(request):
    """Handle CSV file upload and import expenses"""
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            messages.error(request, 'Please select a CSV file to upload.')
            return render(request, 'expenses/import_expenses.html')
        
        csv_file = request.FILES['csv_file']
        
        # Validate file type
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid CSV file.')
            return render(request, 'expenses/import_expenses.html')
        
        try:
            # Save the uploaded file temporarily
            file_path = default_storage.save(f'temp_imports/{csv_file.name}', ContentFile(csv_file.read()))
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            
            # Call the management command and capture output
            from io import StringIO
            from django.core.management import call_command
            
            output = StringIO()
            call_command('import_expenses', full_path, username=request.user.username, stdout=output)
            
            # Clean up the temporary file
            default_storage.delete(file_path)
            
            # Get the command output
            command_output = output.getvalue()
            output.close()
            
            # Check if categories/subcategories were created
            if 'Created new category:' in command_output or 'Created new subcategory:' in command_output:
                messages.success(request, 'Expenses imported successfully! New categories and subcategories were automatically created.')
            else:
                messages.success(request, 'Expenses imported successfully!')
            
            return redirect('expenses:list')
            
        except Exception as e:
            # Clean up the temporary file if it exists
            if 'file_path' in locals():
                default_storage.delete(file_path)
            
            messages.error(request, f'Error importing expenses: {str(e)}')
            return render(request, 'expenses/import_expenses.html')
    
    return render(request, 'expenses/import_expenses.html')
