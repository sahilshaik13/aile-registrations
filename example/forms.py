from django import forms
from datetime import datetime

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    roll_number = forms.CharField(max_length=20)
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    mobile_number = forms.CharField(
        max_length=15,
        min_length=10,
        error_messages={
            'min_length': 'Mobile number must be at least 10 digits.',
            'max_length': 'Mobile number cannot exceed 15 digits.'
        }
    )
    email = forms.EmailField()
    year = forms.ChoiceField(choices=[
        ('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year')
    ])
    semester = forms.ChoiceField(choices=[
        ('1', '1st Semester'), ('2', '2nd Semester'), ('3', '3rd Semester'),
        ('4', '4th Semester'), ('5', '5th Semester'), ('6', '6th Semester'),
        ('7', '7th Semester'), ('8', '8th Semester')
    ])
    belongs_to_college = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.Select(attrs={'onchange': 'toggleCollegeNameField()'})
    )
    college_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'style': 'display: none;'})
    )
    
    course_choices = [
        ('CSE', 'CSE'), ('CSE IOT', 'CSE IOT'), ('CSE DS', 'CSE DS'),
        ('CSE AIML', 'CSE AIML'), ('IT', 'IT'), ('CIVIL', 'CIVIL'),
        ('MECH', 'MECH')
    ]
    
    course = forms.ChoiceField(
        choices=course_choices + [('other', 'Other')],
        widget=forms.Select(attrs={'onchange': 'toggleCourseField()'})
    )
    
    other_course = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'style': 'display: none;'})
    )
    
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

    def clean(self):
        cleaned_data = super().clean()
        belongs_to_college = cleaned_data.get('belongs_to_college')
        college_name = cleaned_data.get('college_name')
        course = cleaned_data.get('course')
        other_course = cleaned_data.get('other_course')

        # Validate college name only if user selected "No"
        if belongs_to_college == 'no' and not college_name:
            self.add_error('college_name', 'Please provide your college name.')

        # Validate other course only if user selected "Other" and does not belong to NSAKCET
        if belongs_to_college == 'no' and course == 'other' and not other_course:
            self.add_error('other_course', 'Please specify your course.')
        
        return cleaned_data