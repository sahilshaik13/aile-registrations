from django import forms

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    roll_number = forms.CharField(max_length=20)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
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
        widget=forms.Select(attrs={'onchange': 'toggleCollegeFields()'})
    )
    
    college_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'style': 'display: none;'})
    )

    department = forms.ChoiceField(
        choices=[('be', 'BE'), ('polytechnic', 'Polytechnic')],
        required=False,
        widget=forms.Select(attrs={'onchange': 'updateCourseOptions()'})
    )

    course = forms.ChoiceField(choices=[], widget=forms.Select())

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

    # Predefined course lists including "Other"
    BE_COURSES = [
        ('CSE', 'CSE'), ('CSE IOT', 'CSE IOT'), ('CSE DS', 'CSE DS'),
        ('CSE AIML', 'CSE AIML'), ('IT', 'IT'), ('CIVIL', 'CIVIL'),
        ('MECH', 'MECH'), ('other', 'Other')
    ]

    POLYTECHNIC_COURSES = [
        ('CSE', 'CSE'), ('CSE AIML', 'CSE AIML'),
        ('ECE', 'ECE'), ('EEE', 'EEE'),
        ('CIVIL', 'CIVIL'), ('MECH', 'MECH'), ('other', 'Other')
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get department from initial data if available
        department = kwargs.get('initial', {}).get('department', None)

        # Set course options based on department selection
        if department == 'polytechnic':
            self.fields['course'].choices = self.POLYTECHNIC_COURSES
        else:
            self.fields['course'].choices = self.BE_COURSES

    def clean(self):
        cleaned_data = super().clean()
        belongs_to_college = cleaned_data.get('belongs_to_college')
        college_name = cleaned_data.get('college_name')
        department = cleaned_data.get('department')
        course = cleaned_data.get('course')
        other_course = cleaned_data.get('other_course')

        # Ensure valid department selection when user belongs to NSAKCET
        if belongs_to_college == 'yes' and department not in ['be', 'polytechnic']:
            self.add_error('department', 'Invalid department selection.')

        # Validate college name only if user selected "No"
        if belongs_to_college == 'no' and not college_name:
            self.add_error('college_name', 'Please provide your college name.')

        # Validate course selection based on department
        valid_courses = self.POLYTECHNIC_COURSES if department == 'polytechnic' else self.BE_COURSES
        valid_course_values = [c[0] for c in valid_courses]

        if course not in valid_course_values:
            self.add_error('course', 'Invalid course selection.')

        # Validate other course only if user selected "Other" and does not belong to NSAKCET
        if belongs_to_college == 'no' and course == 'other' and not other_course:
            self.add_error('other_course', 'Please specify your course.')

        return cleaned_data