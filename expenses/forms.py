from django import forms
from django.contrib.auth.models import User
from .models import Expense, UserCategory, UserSubcategory

class ExpenseForm(forms.ModelForm):
    category = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'category-select'})
    )
    subcategory = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'subcategory-select'})
    )
    
    class Meta:
        model = Expense
        fields = ['date', 'vendor', 'exclude', 'indispensable', 'avoidable', 'amount', 'category', 'subcategory', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'vendor': forms.TextInput(attrs={'class': 'form-control'}),
            'exclude': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'indispensable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'avoidable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Get user's categories
            categories = UserCategory.objects.filter(user=user).order_by('name')
            category_choices = [('', 'Select Category...')]
            category_choices.extend([(cat.name, cat.name) for cat in categories])
            
            self.fields['category'].widget.choices = category_choices
            
            # Get user's subcategories
            subcategories = UserSubcategory.objects.filter(user=user).order_by('name')
            subcategory_choices = [('', 'Select Subcategory...')]
            subcategory_choices.extend([(sub.name, sub.name) for sub in subcategories])
            
            self.fields['subcategory'].widget.choices = subcategory_choices
            
            # Set initial values for category and subcategory if editing an existing expense
            if self.instance and self.instance.pk:
                if self.instance.category:
                    self.fields['category'].initial = self.instance.category
                if self.instance.subcategory:
                    self.fields['subcategory'].initial = self.instance.subcategory
    
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("Please select a category.")
        return category
    
    def clean_subcategory(self):
        subcategory = self.cleaned_data.get('subcategory')
        # Subcategory is optional, so we don't validate if it's empty
        return subcategory
    
    def save(self, commit=True):
        expense = super().save(commit=False)
        
        # Handle category - store as string in the expense model
        category_name = self.cleaned_data.get('category')
        if category_name:
            expense.category = category_name
            # Also create/update the UserCategory for consistency
            UserCategory.objects.get_or_create(
                user=expense.user,
                name=category_name
            )
        
        # Handle subcategory - store as string in the expense model
        subcategory_name = self.cleaned_data.get('subcategory')
        if subcategory_name and category_name:
            expense.subcategory = subcategory_name
            # Also create/update the UserSubcategory for consistency
            try:
                category_obj = UserCategory.objects.get(user=expense.user, name=category_name)
                UserSubcategory.objects.get_or_create(
                    user=expense.user,
                    category=category_obj,
                    name=subcategory_name
                )
            except UserCategory.DoesNotExist:
                # If category doesn't exist, just store the subcategory as string
                pass
        else:
            expense.subcategory = ''
        
        if commit:
            expense.save()
        return expense 