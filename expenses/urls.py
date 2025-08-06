from django.urls import path
from .views import (
    ExpenseListView, ExpenseCreateView, ExpenseChartView, ExpenseCalendarView, 
    expense_category_data, add_category, add_subcategory
)

app_name = 'expenses'
urlpatterns = [
    path('', ExpenseListView.as_view(), name='list'),
    path('add/', ExpenseCreateView.as_view(), name='add'),
    path('chart/', ExpenseChartView.as_view(), name='chart'),
    path('chart-data/', expense_category_data, name='chart-data'),
    path('calendar/', ExpenseCalendarView.as_view(), name='calendar'),
    path('add-category/', add_category, name='add-category'),
    path('add-subcategory/', add_subcategory, name='add-subcategory'),
] 