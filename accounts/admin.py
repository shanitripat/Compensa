from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'imp_code', 'grade', 'location', 'function_name')
    search_fields = ('full_name', 'imp_code', 'function_name')
    list_filter = ('grade', 'location', 'function_name')
