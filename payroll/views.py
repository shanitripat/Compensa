from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib import messages
from django.http import HttpResponse
import csv

from .models import PayrollSubmission, PayrollEntry
from .forms import PayrollSubmissionForm, PayrollEntryForm



@login_required
def dashboard(request):
    """
    Dashboard view:
    - Normal users see all their entries across all submissions.
    - Superusers see all entries across all users.
    """
    if request.user.is_superuser:
        entries = PayrollEntry.objects.select_related('submission', 'submission__user').order_by('-submission__created_at')
    else:
        entries = PayrollEntry.objects.filter(
            submission__user=request.user
        ).select_related('submission').order_by('-submission__created_at')

    return render(request, 'payroll/dashboard.html', {
        'entries': entries,   # ✅ pass all entries, not just submissions
    })



@login_required
def new_submission(request):
    """
    Create a new payroll submission with multiple entries using a formset.
    Prefills user profile details if available.
    """
    # ✅ NEW: allow delete option in formset
    EntryFormSet = modelformset_factory(
        PayrollEntry,
        form=PayrollEntryForm,
        extra=5,
        can_delete=True  # ✅ NEW
    )
    formset = EntryFormSet(request.POST or None, queryset=PayrollEntry.objects.none())

    if request.method == 'POST':
        sub_form = PayrollSubmissionForm(request.POST)
        formset = EntryFormSet(request.POST, queryset=PayrollEntry.objects.none())
        if sub_form.is_valid() and formset.is_valid():
            submission = sub_form.save(commit=False)
            submission.user = request.user
            submission.save()
            for form in formset:
                # ✅ NEW: skip deleted rows
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    entry = form.save(commit=False)
                    entry.submission = submission
                    if entry.final_amount is None:
                        entry.final_amount = entry.days * entry.per_day
                    entry.save()
            messages.success(request, 'Submission saved successfully.')
            return redirect('dashboard')
    else:
        sub_form = PayrollSubmissionForm()
        formset = EntryFormSet(queryset=PayrollEntry.objects.none())

        # Prefill from Profile if exists
        try:
            profile = request.user.profile
            for form in formset.forms:
                form.initial.update({
                    'employee_id': profile.imp_code,
                    'name': profile.full_name,
                    'grade': profile.grade,
                    'location': profile.location,
                    'function_name': profile.function_name,
                    'line_manager': profile.line_manager,
                    'function_manager': profile.function_manager,
                    'functional_head': profile.functional_head,
                })
        except Exception:
            pass

    return render(request, 'payroll/new_submission.html', {
        'sub_form': sub_form,
        'formset': formset
    })


@login_required
def submission_detail(request, submission_id):
    """
    View details of a submission:
    - Normal users can only view their own submissions.
    - Superusers can view any submission.
    """
    if request.user.is_superuser:
        submission = get_object_or_404(PayrollSubmission, id=submission_id)
    else:
        submission = get_object_or_404(PayrollSubmission, id=submission_id, user=request.user)

    entries = submission.entries.all()
    total = sum(e.final_amount or 0 for e in entries)
    return render(request, 'payroll/submission_detail.html', {
        'submission': submission,
        'entries': entries,
        'total': total
    })


@login_required
def export_submission_csv(request, submission_id):
    """
    Export a single submission's entries to CSV:
    - Normal users can only export their own submissions.
    - Superusers can export any submission.
    """
    if request.user.is_superuser:
        submission = get_object_or_404(PayrollSubmission, id=submission_id)
    else:
        submission = get_object_or_404(PayrollSubmission, id=submission_id, user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="compensa_{submission.payroll_month}.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Employee ID','Name','Grade','Location','Payroll Name','Days','Per Day','Final Amount',
        'Holiday','Function Name','Line Manager','Function Manager','Functional Head','Payroll Month','Remarks'
    ])
    for e in submission.entries.all():
        writer.writerow([
            e.employee_id, e.name, e.grade, e.location, e.payroll_name, e.days, e.per_day, e.final_amount,
            e.holiday, e.function_name, e.line_manager, e.function_manager, e.functional_head,
            submission.payroll_month, e.remarks
        ])
    return response


@login_required
def export_all_submissions_csv(request):
    """
    Export all payroll entries across all users into one CSV file.
    Only superusers can access this.
    """
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to export all submissions.")
        return redirect('dashboard')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="compensa_all_submissions.csv"'
    writer = csv.writer(response)

    # Header row
    writer.writerow([
        'User','Employee ID','Name','Grade','Location','Payroll Name','Days','Per Day','Final Amount',
        'Holiday','Function Name','Line Manager','Function Manager','Functional Head','Payroll Month','Remarks'
    ])

    # Loop through all entries
    for entry in PayrollEntry.objects.select_related('submission', 'submission__user').all():
        writer.writerow([
            entry.submission.user.username,
            entry.employee_id,
            entry.name,
            entry.grade,
            entry.location,
            entry.payroll_name,
            entry.days,
            entry.per_day,
            entry.final_amount,
            entry.holiday,
            entry.function_name,
            entry.line_manager,
            entry.function_manager,
            entry.functional_head,
            entry.submission.payroll_month,
            entry.remarks,
        ])

    return response

@login_required
def delete_entry(request, entry_id):
    """
    Allow a user to delete their own payroll entry.
    Superusers can delete any entry.
    """
    entry = get_object_or_404(PayrollEntry, id=entry_id)

    # Only allow owner or superuser
    if request.user.is_superuser or entry.submission.user == request.user:
        entry.delete()
        messages.success(request, "Entry deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this entry.")

    return redirect('dashboard')

