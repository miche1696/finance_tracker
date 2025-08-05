from django.urls import path
from .views import ExpenseListView, ExpenseCreateView, ExpenseChartView, ExpenseCalendarView, expense_category_data

app_name = 'expenses'
urlpatterns = [
    path('', ExpenseListView.as_view(), name='list'),
    path('add/', ExpenseCreateView.as_view(), name='add'),
    path('chart/', ExpenseChartView.as_view(), name='chart'),
    path('chart-data/', expense_category_data, name='chart-data'),
    path('calendar/', ExpenseCalendarView.as_view(), name='calendar'),
] 