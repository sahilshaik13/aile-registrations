from django import forms
from datetime import datetime

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    roll_number = forms.CharField(max_length=20)
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1999, datetime.now().year + 1)))
    mobile_number = forms.CharField(max_length=15)  # New field for mobile number
    email = forms.EmailField()  # New field for email address
    year = forms.ChoiceField(choices=[('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year')])
    semester = forms.ChoiceField(choices=[('1', '1st Semester'), ('2', '2nd Semester'), ('3', '3rd Semester'), ('4', '4th Semester'), ('5', '5th Semester'), ('6', '6th Semester'), ('7', '7th Semester'), ('8', '8th Semester')])
    course = forms.CharField(max_length=100)
    reason_to_join = forms.CharField(widget=forms.Textarea)
    expectations = forms.CharField(widget=forms.Textarea)