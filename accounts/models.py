from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    imp_code = models.CharField(max_length=50, unique=True)
    grade = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    function_name = models.CharField(max_length=100)
    line_manager = models.CharField(max_length=100)
    function_manager = models.CharField(max_length=100, null=True, blank=True)
    functional_head = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"{self.full_name} ({self.imp_code})"
