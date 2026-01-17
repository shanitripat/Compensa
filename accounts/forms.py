from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

# Example dropdown choices – you can later move these into the database for dynamic management
FUNCTION_NAMES = [
    ('Service Delivery', 'Service Delivery'),
]

LINE_MANAGERS = [
    ('Aman Bakshi', 'Aman Bakshi'),
    ('Amardeep Singh', 'Amardeep Singh'),
    ('Sumit Chauhan', 'Sumit Chauhan'),
    ('Abhishek Das', 'Abhishek Das'),
    
]

FUNCTION_MANAGERS = [
    ('Yougesh Bhatt', 'Yougesh Bhatt'),
]

FUNCTION_HEADS = [
    ('Rajneesh Gupta', 'Rajneesh Gupta'),
]
GRADES = [ ('PT1', 'PT1'), ('PT2', 'PT2'), ] 

LOCATIONS = [ ('IN-GGN', 'IN-GGN'), 
             ('IN-BLR', 'IN-BLR'), ]

class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, required=True, label="Full Name")
    imp_code = forms.CharField(max_length=50, required=True, label="Imp Code")
    grade = forms.ChoiceField(choices=GRADES, required=True, label="Grade")
    location = forms.ChoiceField(choices=LOCATIONS, required=True, label="Location")
    function_name = forms.ChoiceField(choices=FUNCTION_NAMES, required=True, label="Function Name")
    line_manager = forms.ChoiceField(choices=LINE_MANAGERS, required=True, label="Line Manager")
    function_manager = forms.ChoiceField(choices=FUNCTION_MANAGERS, required=True, label="Function Manager")
    functional_head = forms.ChoiceField(choices=FUNCTION_HEADS, required=True, label="Function Head")

    class Meta:
        model = User
        fields = [
            'username', 'password1', 'password2',
            'full_name', 'imp_code', 'grade', 'location', 'function_name',
            'line_manager', 'function_manager', 'functional_head'
        ]
