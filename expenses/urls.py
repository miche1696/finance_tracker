from django.urls import path
from .views import (
    ExpenseListView, ExpenseCreateView, ExpenseCalendarView, 
    add_category, add_subcategory, delete_expense, ExpenseUpdateView, import_expenses
)

app_name = 'expenses'
urlpatterns = [
    path('', ExpenseListView.as_view(), name='list'),
    path('add/', ExpenseCreateView.as_view(), name='add'),
    path('edit/<int:expense_id>/', ExpenseUpdateView.as_view(), name='edit'),
    path('calendar/', ExpenseCalendarView.as_view(), name='calendar'),
    path('import/', import_expenses, name='import'),
    path('add-category/', add_category, name='add-category'),
    path('add-subcategory/', add_subcategory, name='add-subcategory'),
    path('delete/<int:expense_id>/', delete_expense, name='delete'),
] 