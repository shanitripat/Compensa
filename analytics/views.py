from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from payroll.models import PayrollEntry

@login_required
def analytics_dashboard(request):
    qs = PayrollEntry.objects.all()
    by_payroll = {}
    for e in qs:
        by_payroll.setdefault(e.payroll_name, 0)
        by_payroll[e.payroll_name] += float(e.final_amount or 0)

    labels = list(by_payroll.keys())
    data = list(by_payroll.values())
    return render(request, 'analytics/dashboard.html', {'labels': labels, 'data': data})
