from django.db import models
from django.contrib.auth.models import User

class PayrollSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payroll_month = models.CharField(max_length=20)  # e.g., "Dec'25"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.payroll_month}"

class PayrollEntry(models.Model):
    submission = models.ForeignKey(PayrollSubmission, on_delete=models.CASCADE, related_name='entries')
    employee_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    payroll_name = models.CharField(max_length=100)
    days = models.PositiveIntegerField()
    per_day = models.DecimalField(max_digits=10, decimal_places=2)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    holiday = models.CharField(max_length=50, blank=True)
    function_name = models.CharField(max_length=100)
    line_manager = models.CharField(max_length=100)
    function_manager = models.CharField(max_length=100)
    functional_head = models.CharField(max_length=100)
    remarks = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if (self.final_amount is None) and self.days and self.per_day:
            self.final_amount = self.days * self.per_day
        super().save(*args, **kwargs)