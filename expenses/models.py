from django.db import models

class Expense(models.Model):
    date = models.DateField(verbose_name="Date")
    vendor = models.CharField(max_length=255, verbose_name="Store / Vendor")
    exclude = models.BooleanField(default=False, verbose_name="Escludi Spesa Da analysts")
    indispensable = models.BooleanField(default=False, verbose_name="Spesa indispensabile")
    avoidable = models.BooleanField(default=False, verbose_name="Spesa evitabile")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="$ Amount")
    category = models.CharField(max_length=100, verbose_name="Expense Category")
    subcategory = models.CharField(max_length=100, blank=True, verbose_name="SubCategory")
    notes = models.TextField(blank=True, verbose_name="Notes (Optional)")

    def __str__(self):
        return f"{self.date} – {self.vendor}: {self.amount}"
