from django.contrib import admin
from .models import Expense, UserCategory, UserSubcategory

@admin.register(UserCategory)
class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'user__username')
    list_select_related = ('user',)

@admin.register(UserSubcategory)
class UserSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'name', 'created_at')
    list_filter = ('user', 'category', 'created_at')
    search_fields = ('name', 'category__name', 'user__username')
    list_select_related = ('user', 'category')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'vendor', 'amount', 'category', 'subcategory', 'exclude')
    list_filter = ('user', 'date', 'category', 'exclude')
    search_fields = ('vendor', 'notes', 'user__username')
    list_select_related = ('user',)
    
    def get_queryset(self, request):
        # Admin can see all expenses, but regular users will be filtered in views
        return super().get_queryset(request)