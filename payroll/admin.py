from django.contrib import admin
from .models import PayrollSubmission, PayrollEntry

class PayrollEntryInline(admin.TabularInline):
    model = PayrollEntry
    extra = 0

@admin.register(PayrollSubmission)
class PayrollSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user','payroll_month','created_at')
    inlines = [PayrollEntryInline]

@admin.register(PayrollEntry)
class PayrollEntryAdmin(admin.ModelAdmin):
    list_display = ('submission','employee_id','name','payroll_name','days','per_day','final_amount')
    list_filter = ('payroll_name','function_name','location','grade')
    search_fields = ('employee_id','name','remarks')