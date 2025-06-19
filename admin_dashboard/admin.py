from django.contrib import admin
from .models import Dashboard
# Register your models here.
@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'fields', 'status','phone')
