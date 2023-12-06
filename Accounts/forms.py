import datetime
from django import forms
from .models import ApplicationDetails, Document_Candidate, InterviewDetails, User_Rolls, VacancyDetails, candidate_details, question_sheet,User_Details, TestSchedule,vacancy
from django.contrib.auth.models import User


# class VacancyForm(forms.ModelForm):
#     QUALIFICATION_CHOICES = [
#         ('12th', '12th'),
#         ('Graduation', 'Graduation'),
#         ('Under Graduation', 'Under Graduation'),
#         ('Post Graduation', 'Post Graduation'),
#     ]
    
#     query = User_Rolls.objects.filter(roll_id=2).values_list('user_id', flat=True)
#     queryset = User.objects.filter(id__in=query).values_list('id', 'username')

#     INTERVIEW_PANEL_CHOICES = [(str(user[0]), user[1]) for user in queryset]
#     INTERVIEW_PANEL_CHOICES.insert(0, ('', '-------------'))

#     qualification_type = forms.ChoiceField(choices=QUALIFICATION_CHOICES, widget=forms.Select(attrs={'class': 'form-control','required': True}))
#     interview_panel_1 = forms.ChoiceField(choices=INTERVIEW_PANEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control panel-choice', 'id': 'panel-1', 'required': True}))
#     interview_panel_2 = forms.ChoiceField(choices=INTERVIEW_PANEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control panel-choice', 'id': 'panel-2', 'required': True}))
#     interview_panel_3 = forms.ChoiceField(choices=INTERVIEW_PANEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control panel-choice', 'id': 'panel-3', 'required': True}))
#     interview_panel_4 = forms.ChoiceField(choices=INTERVIEW_PANEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control panel-choice', 'id': 'panel-4', 'required': True}))

#     class Meta:
#         model = vacancy
#         fields = '__all__'
#         widgets = {
#             'branch_name': forms.TextInput(attrs={'class': 'form-control','maxLength':'30','required': True, 'id':'branch_name'}),
#             'no_of_vacancies': forms.NumberInput(attrs={'class': 'form-control','required': True, 'id':'no_of_vacancies'}),
#             'job_role': forms.TextInput(attrs={'class': 'form-control','required': True,'id':'job_role'}),
#             'required_experience': forms.NumberInput(attrs={'class': 'form-control','required': True,'id':'required_experience'}),
#             'required_skills': forms.TextInput(attrs={'class': 'form-control','required': True,'id':'required_skills','placeholder':'For Example- HTML, CSS, JS ,...'}),
#             'salary': forms.NumberInput(attrs={'class': 'form-control','required': True,'id':'salary'}),
#             'interview_place': forms.TextInput(attrs={'class': 'form-control','required': True,'id':'interview_place'}),
#             'interview_date': forms.DateInput(attrs={'class': 'form-control','type': 'date','required': True,'id':'interview_date'}),
#             'interview_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time','required': True}),
#             'job_responsibility': forms.Textarea(attrs={'class': 'form-control','required': True}),
#             'job_description': forms.Textarea(attrs={'class': 'form-control','required': True}),
#         }
#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         panel_fields = ['interview_panel_1', 'interview_panel_2', 'interview_panel_3', 'interview_panel_4']
#         panel_values = [self.cleaned_data[field] for field in panel_fields]
#         panel_list = ','.join(panel_values)
#         instance.panel_list = panel_list
#         instance.posted_on = datetime.datetime.today()
#         print("save:", instance.posted_on)
#         if commit:
#             instance.save()
#         return instance
    

class VacancyForm(forms.Form):
    QUALIFICATION_CHOICES = [
        ('Secondary', 'Secondary'),
        ('Intermediate', 'Intermediate'),
        ('Under Graduation', 'Under Graduation'),
        ('Post Graduation', 'Post Graduation'),
    ]
    
    WALK_IN_CHOICES = [
        ('1','Yes'),
        ('0','No'),
    ]
    
    query = User_Rolls.objects.filter(roll_id=2).values_list('user_id', flat=True)
    queryset = User.objects.filter(id__in=query).values_list('id', 'username')
    INTERVIEW_PANEL_CHOICES = [(str(user[0]), user[1]) for user in queryset]
    INTERVIEW_PANEL_CHOICES.insert(0, ('', '-------------'))

    qualification = forms.ChoiceField(choices=QUALIFICATION_CHOICES, widget=forms.Select(attrs={'class': 'form-control','required': True}))
    walk_in_id = forms.ChoiceField(choices=WALK_IN_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    branch = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','maxLength':'30','required': True, 'id':'branch_name'}))
    role = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','required': True,'id':'job_role'}))
    salary = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','required': True,'id':'salary'}))

    interview_panel_1 = forms.ChoiceField(choices=INTERVIEW_PANEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control panel-choice', 'id': 'panel-1', 'required': True}))
    interview_panel_2 = forms.ChoiceField(choices=INTERVIEW_PANEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control panel-choice', 'id': 'panel-2', 'required': True}))
    interview_panel_3 = forms.ChoiceField(choices=INTERVIEW_PANEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control panel-choice', 'id': 'panel-3', 'required': True}))
    interview_panel_4 = forms.ChoiceField(choices=INTERVIEW_PANEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control panel-choice', 'id': 'panel-4', 'required': True}))
    no_of_vacancies = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','required': True, 'id':'no_of_vacancies'}))
    required_experience = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','required': True,'id':'required_experience'}))
    required_skills = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','required': True,'id':'required_skills','placeholder':'For Example- HTML, CSS, JS ,...'}))
    interview_place = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','required': True,'id':'interview_place'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','required': True,'id':'address'}))
    interview_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date','required': True,'id':'interview_date'})) 
    interview_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control','type': 'time','required': True,'id':'interview_time'}))
    job_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','required': True,'id':'job_description'}))
    job_responsibility = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','required': True,'id':'job_responsibility'}))


class InterviewAndVacancyForm(forms.ModelForm):
    class Meta:
        model = InterviewDetails
        fields = '__all__'  # You can specify the fields you want to include instead of '__all__'

    # Add additional fields from the VacancyDetails model
    branch = forms.CharField(max_length=50, required=False)
    vacancy_description = forms.CharField(max_length=50, required=False)
    vacancy_status = forms.CharField(max_length=50, required=False)
    capacity = forms.IntegerField(required=False)
    role = forms.CharField(max_length=255, required=False)
    salary = forms.IntegerField(required=False)
    qualification = forms.CharField(max_length=255, required=False)
    vacancy_date = forms.DateTimeField(required=False)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = question_sheet
        fields = '__all__'
        widgets = {
            'sheet_id': forms.NumberInput(attrs={'class': 'form-control','required': True}),
            'question_id': forms.NumberInput(attrs={'class': 'form-control','required': True}),
            'question_text': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'question_a': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'question_b': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'question_c': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'question_d': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'answer': forms.TextInput(attrs={'class': 'form-control','required': True}),
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

class SkipValidationChoiceField(forms.ChoiceField):
    def validate(self, value):
        pass  # Skip the validation step

class CandidateBasicDetailsForm(forms.ModelForm):
    GENDER = (
        ('', 'Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    PLACES=(('','Select Place'),)

    position = forms.ChoiceField(choices=[], required=True)
    place = SkipValidationChoiceField(choices=PLACES, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        date=datetime.datetime.today()
        vacancy_idlist = InterviewDetails.objects.filter(interview_date__gte=date).values_list('vacancy_id')
        positions = VacancyDetails.objects.filter(vacancy_id__in=vacancy_idlist).values_list('role', flat=True).distinct()
        print("position..", positions)
        self.fields['position'].choices = [('', 'Select Position')] + [(pos, pos) for pos in positions]
        print("ppppp....", self.fields['position'].choices)
        
    def clean_place(self):
        place = self.cleaned_data.get('place')
        return place
    class Meta:
        model = candidate_details
        fields = ['name', 'email', 'dob', 'mobile_no', 'position', 'place','gender']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'id':'full_name','placeHolder':'As a 10th Marksheet'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True, 'id':'email'}),          
            'dob':forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True, 'id':'dob','placeHolder':'As a 10th Marksheet'}),
            'mobile_no': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'id':'mobile_no', 'pattern':'[0-9]{10}', 'maxlength':'10', 'minlength':'10' ,'oninput':"javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);"}),
            'position': forms.Select(attrs={'class': 'form-control', 'id':'id_position'}),
            'place': forms.Select(attrs={'class': 'form-control', 'id':'place'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob:
            today = datetime.date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise forms.ValidationError("Applicant must be at least 18 years old.")
        return dob

    def save(self, commit=True):
        instance = super().save(commit=False)

        place_value = self.cleaned_data.get('place') 
        position=self.cleaned_data.get('position')
        # instance.position_applied_for=position
        # instance.branch_shortlisted_for=place_value
        ApplicationDetails.objects.create(candidate_id=instance.id,position_shortlisted_for=position,branch_shortlisted_for=place_value,application_status=2)
        if commit:
            instance.save()
        return instance



class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document_Candidate
        fields = '__all__'