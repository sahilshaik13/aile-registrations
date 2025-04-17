from django import forms

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, label='Name')
    roll_number = forms.CharField(max_length=20, label='Roll Number')
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)), label='Date of Birth')
    year = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(1, 6)], label='Year')
    semester = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(1, 3)], label='Semester')
    course = forms.CharField(max_length=100, label='Course')
    reason_to_join = forms.CharField(widget=forms.Textarea, label='Why do you want to join AppIgnite')
    expectations = forms.CharField(widget=forms.Textarea, label='What do you expect from AppIgnite')