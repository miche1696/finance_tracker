from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserScopedManager(models.Manager):
    def get_queryset(self):
        # This will be overridden in views to filter by current user
        return super().get_queryset()
    
    def for_user(self, user):
        return super().get_queryset().filter(user=user)

class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100, verbose_name="Category Name")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'name']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"

class UserSubcategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subcategories')
    category = models.ForeignKey(UserCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100, verbose_name="Subcategory Name")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'category', 'name']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.user.username} - {self.category.name} > {self.name}"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    date = models.DateField(verbose_name="Date")
    vendor = models.CharField(max_length=255, verbose_name="Store / Vendor")
    exclude = models.BooleanField(default=False, verbose_name="Escludi Spesa Da analysts")
    indispensable = models.BooleanField(default=False, verbose_name="Spesa indispensabile")
    avoidable = models.BooleanField(default=False, verbose_name="Spesa evitabile")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="$ Amount")
    category = models.CharField(max_length=100, verbose_name="Expense Category")
    subcategory = models.CharField(max_length=100, blank=True, verbose_name="SubCategory")
    notes = models.TextField(blank=True, verbose_name="Notes (Optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserScopedManager()

    class Meta:
        ordering = ['-date', '-created_at']
        unique_together = ['user', 'date', 'vendor', 'amount']  # Prevent duplicate entries

    def __str__(self):
        return f"{self.user.username} - {self.date} – {self.vendor}: {self.amount}"
