from django.urls import path
from .views import (
    ExpenseListView, ExpenseCreateView, ExpenseCalendarView, ExpenseChartView,
    add_category, add_subcategory, delete_expense, ExpenseUpdateView, import_expenses,
    get_expenses_by_date
)

app_name = 'expenses'
urlpatterns = [
    path('', ExpenseListView.as_view(), name='list'),
    path('add/', ExpenseCreateView.as_view(), name='add'),
    path('edit/<int:expense_id>/', ExpenseUpdateView.as_view(), name='edit'),
    path('calendar/', ExpenseCalendarView.as_view(), name='calendar'),
    path('calendar/day/<str:date_str>/', get_expenses_by_date, name='expenses-by-date'),
    path('chart/', ExpenseChartView.as_view(), name='chart'),
    path('import/', import_expenses, name='import'),
    path('add-category/', add_category, name='add-category'),
    path('add-subcategory/', add_subcategory, name='add-subcategory'),
    path('delete/<int:expense_id>/', delete_expense, name='delete'),
] 