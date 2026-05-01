from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['description', 'amount', 'category', 'date', 'user']
    list_filter = ['category', 'date', 'user']
    search_fields = ['description', 'notes']
    date_hierarchy = 'date'
