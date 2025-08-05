from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'vendor', 'amount', 'category', 'subcategory', 'exclude')
    list_filter = ('date', 'category', 'exclude')
    search_fields = ('vendor', 'notes')