from django import forms
from datetime import datetime

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    roll_number = forms.CharField(max_length=20)
    dob = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date'
        })
    )
    mobile_number = forms.CharField(max_length=15)
    email = forms.EmailField()
    year = forms.ChoiceField(choices=[('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year')])
    semester = forms.ChoiceField(choices=[
        ('1', '1st Semester'), 
        ('2', '2nd Semester'), 
        ('3', '3rd Semester'), 
        ('4', '4th Semester'), 
        ('5', '5th Semester'), 
        ('6', '6th Semester'), 
        ('7', '7th Semester'), 
        ('8', '8th Semester')
    ])
    course = forms.ChoiceField(choices=[
        ('CSE', 'CSE'),
        ('CSE IOT', 'CSE IOT'),
        ('CSE DS', 'CSE DS'),
        ('CSE AIML', 'CSE AIML'),
        ('IT', 'IT'),
        ('CIVIL', 'CIVIL'),
        ('MECH', 'MECH')
    ])
    reason_to_join = forms.CharField(
        widget=forms.Textarea(attrs={'maxlength': '500', 'oninput': 'updateCounter(this, "reasonCounter")'}),
        max_length=500,
        help_text="Please provide your reason for joining (max 500 characters)."
    )
    expectations = forms.CharField(
        widget=forms.Textarea(attrs={'maxlength': '500', 'oninput': 'updateCounter(this, "expectationsCounter")'}),
        max_length=500,
        help_text="What do you hope to learn or gain from this experience? (max 500 characters)"
    )