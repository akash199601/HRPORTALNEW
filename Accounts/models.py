from django.db import models

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Any', 'Any'),
)

CANDIDATE_STATUS = ((1, 'Applied'), (2, 'Accepted'), (3, 'TestSceduled'), (4, 'InterviewSceduled'),(5,'InterviewCompleted'))

# Create your models here.
class User_Details(models.Model):
    name  = models.CharField(max_length=200,blank=True,null=True)
    address  = models.CharField(max_length=200,blank=True,null=True)
    gender = models.CharField(choices=GENDER, max_length=30,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    dob = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    mobile_no = models.BigIntegerField(blank=True,null=True)
    resume_file = models.CharField(max_length=300,blank=True,null=True)
    identity_Aadhar = models.CharField(max_length=12,blank=True,null=True)
    identity_PAN = models.CharField(max_length=10,blank=True,null=True)
    identity_DL_No = models.CharField(max_length=20,blank=True,null=True)
    is_HR = models.BooleanField(default=False)
    is_interviewer = models.BooleanField(default=False)
    vacancy_id = models.IntegerField(blank=True,null=True)
    status = models.IntegerField(default=0)
    referred_by = models.IntegerField(blank=True, null=True)

    position_applied_for=models.CharField(max_length=200,blank=True,null=True)
    applied_date=models.DateField(blank=True,null=True)
    # PERSONAL INFORMATION
    full_name=models.CharField(max_length=200,blank=True,null=True)
    # PRESENT ADDRESS
    present_city=models.CharField(max_length=200,blank=True,null=True)
    present_pin=models.BigIntegerField(blank=True,null=True)
    present_state=models.CharField(max_length=200,blank=True,null=True)
    permanent_city=models.CharField(max_length=200,blank=True,null=True)
    permanent_pin=models.BigIntegerField(blank=True,null=True)
    permanent_state=models.CharField(max_length=200,blank=True,null=True)
    #Education details

    #high school
    high_school_Degree_Diploma=models.CharField(max_length=300,blank=True,null=True)
    high_school_subjects=models.CharField(max_length=300,blank=True,null=True)
    high_school_name_location=models.CharField(max_length=300,blank=True,null=True)
    high_school_marks_obtained=models.CharField(max_length=100,blank=True,null=True)
    high_school_passing_year=models.CharField(max_length=100,blank=True,null=True)
    #Intermediate intermediate
    intermediate_Degree_Diploma=models.CharField(max_length=300,blank=True,null=True)
    intermediate_subjects=models.CharField(max_length=300,blank=True,null=True)
    intermediate_name_location=models.CharField(max_length=300,blank=True,null=True)
    intermediate_marks_obtained=models.CharField(max_length=100,blank=True,null=True)
    intermediate_passing_year=models.CharField(max_length=100,blank=True,null=True)
    #Graduation 
    graduation_Degree_Diploma=models.CharField(max_length=300,blank=True,null=True)
    graduation_subjects=models.CharField(max_length=300,blank=True,null=True)
    graduation_name_location=models.CharField(max_length=300,blank=True,null=True)
    graduation_marks_obtained=models.CharField(max_length=100,blank=True,null=True)
    graduation_passing_year=models.CharField(max_length=100,blank=True,null=True)
    #PG
    pg_Degree_Diploma=models.CharField(max_length=300,blank=True,null=True)
    pg_subjects=models.CharField(max_length=300,blank=True,null=True)
    pg_name_location=models.CharField(max_length=300,blank=True,null=True)
    pg_marks_obtained=models.CharField(max_length=100,blank=True,null=True)
    pg_passing_year=models.CharField(max_length=100,blank=True,null=True)
    #Professional Qualification    professional_qualification
    professional_qualification_Degree_Diploma=models.CharField(max_length=300,blank=True,null=True)
    professional_qualification_subjects=models.CharField(max_length=300,blank=True,null=True)
    professional_qualification_name_location=models.CharField(max_length=300,blank=True,null=True)
    professional_qualification_marks_obtained=models.CharField(max_length=100,blank=True,null=True)
    professional_qualification_passing_year=models.CharField(max_length=100,blank=True,null=True)
    #others
    others_qualification_Degree_Diploma=models.CharField(max_length=300,blank=True,null=True)
    others_qualification_subjects=models.CharField(max_length=300,blank=True,null=True)
    others_qualification_name_location=models.CharField(max_length=300,blank=True,null=True)
    others_qualification_marks_obtained=models.CharField(max_length=100,blank=True,null=True)
    others_qualification_passing_year=models.CharField(max_length=100,blank=True,null=True)

    #TRAINING PROGRAMS/WORKSHOP ATTENDED
    training_workshop_title=models.CharField(max_length=300,blank=True,null=True)
    training_workshop_Institution_location=models.CharField(max_length=300,blank=True,null=True)
    training_workshop_skill=models.CharField(max_length=300,blank=True,null=True)
    training_workshop_duration=models.CharField(max_length=100,blank=True,null=True)
    training_workshop_start_date=models.CharField(max_length=100,blank=True,null=True)

    #CURRENT EMPLOYMENT DETAILS
    current_emp_start_date=models.DateField(blank=True,null=True)
    current_employer=models.CharField(max_length=300,blank=True,null=True)
    current_emp_salary=models.CharField(max_length=100,blank=True,null=True)
    current_emp_benefits=models.CharField(max_length=300,blank=True,null=True)
    current_emp_position=models.CharField(max_length=200,blank=True,null=True)
    current_emp_reason_for_leaving=models.CharField(max_length=300,blank=True,null=True)
    expected_salary=models.CharField(max_length=100,blank=True,null=True)
    current_emp_job_description=models.CharField(max_length=300,blank=True,null=True)
    current_emp_supervisor_name=models.CharField(max_length=300,blank=True,null=True)
    
    #FAMILY DETAILS 
    father_name=models.CharField(max_length=200,blank=True,null=True)
    father_dob=models.DateField(blank=True,null=True)
    father_profession=models.CharField(max_length=200,blank=True,null=True)
    mother_name=models.CharField(max_length=200,blank=True,null=True)
    mother_dob=models.DateField(blank=True,null=True)
    mother_profession=models.CharField(max_length=200,blank=True,null=True)
    spouse_name=models.CharField(max_length=200,blank=True,null=True)
    spouse_dob=models.DateField(blank=True,null=True)
    spouse_profession=models.CharField(max_length=200,blank=True,null=True)
    Children_name_1=models.CharField(max_length=200,blank=True,null=True)
    Children_name_2=models.CharField(max_length=200,blank=True,null=True)
    Children_dob_1=models.DateField(blank=True,null=True)
    Children_dob_2=models.DateField(blank=True,null=True)
    Children_1_profession=models.CharField(max_length=200,blank=True,null=True)
    Children_2_profession=models.CharField(max_length=200,blank=True,null=True)

    reason_to_apply_sonata=models.CharField(max_length=300,blank=True,null=True)
    willing_to_relocate=models.BooleanField(default=True,blank=True,null=True)
    interviewed_by_Sonata_before=models.BooleanField(default=False,blank=True,null=True)
    locational_preferences=models.CharField(max_length=200,blank=True,null=True)

    reviewed_by = models.IntegerField(blank=True,null=True)
    is_wp = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True,null=True)
    hold_date = models.DateField(null=True)
    reject_reason = models.CharField(max_length=200,blank=True,null=True)

    # about interview and selection
    position_shortlisted_for = models.CharField(max_length=200,blank=True,null=True)
    branch_shortlisted_for = models.CharField(max_length=200,blank=True,null=True)

    interview_date = models.DateField(blank=True,null=True)
    interview_time = models.CharField(max_length=200,blank=True,null=True)
    interview_panel_list = models.CharField(max_length=200,blank=True,null=True)

class candidate_details(models.Model):
    name  = models.CharField(max_length=200,blank=True,null=True)
    address  = models.CharField(max_length=200,blank=True,null=True)
    gender = models.CharField(choices=GENDER, max_length=30,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    dob = models.DateTimeField(blank=True,null=True)
    mobile_no = models.BigIntegerField(blank=True,null=True)
    # resume_file = models.CharField(max_length=300,blank=True,null=True)
    identity_Aadhar = models.CharField(max_length=12,blank=True,null=True)
    identity_PAN = models.CharField(max_length=10,blank=True,null=True)
    identity_DL_No = models.CharField(max_length=20,blank=True,null=True)
    # is_HR = models.BooleanField(default=False)
    # is_interviewer = models.BooleanField(default=False)
    # vacancy_id = models.IntegerField(blank=True,null=True)
    status = models.IntegerField(default=0)
    referred_by = models.IntegerField(blank=True, null=True)

    position_applied_for=models.CharField(max_length=200,blank=True,null=True)
    applied_date=models.DateField(blank=True,null=True)
    # PERSONAL INFORMATION
    # full_name=models.CharField(max_length=200,blank=True,null=True)
    # PRESENT ADDRESS
    present_city=models.CharField(max_length=200,blank=True,null=True)
    present_pin=models.BigIntegerField(blank=True,null=True)
    present_state=models.CharField(max_length=200,blank=True,null=True)
    permanent_city=models.CharField(max_length=200,blank=True,null=True)
    permanent_pin=models.BigIntegerField(blank=True,null=True)
    permanent_state=models.CharField(max_length=200,blank=True,null=True)
    #Education details

    #high school
    high_school_Degree_Diploma=models.CharField(max_length=300,blank=True,null=True)
    high_school_subjects=models.CharField(max_length=300,blank=True,null=True)
    high_school_name_location=models.CharField(max_length=300,blank=True,null=True)
    high_school_marks_obtained=models.CharField(max_length=100,blank=True,null=True)
    high_school_passing_year=models.CharField(max_length=100,blank=True,null=True)
    #Intermediate intermediate
    intermediate_Degree_Diploma=models.CharField(max_length=300,blank=True,null=True)
    intermediate_subjects=models.CharField(max_length=300,blank=True,null=True)
    intermediate_name_location=models.CharField(max_length=300,blank=True,null=True)
    intermediate_marks_obtained=models.CharField(max_length=100,blank=True,null=True)
    intermediate_passing_year=models.CharField(max_length=100,blank=True,null=True)
    #Graduation 
    graduation_Degree_Diploma=models.CharField(max_length=300,blank=True,null=True)
    graduation_subjects=models.CharField(max_length=300,blank=True,null=True)
    graduation_name_location=models.CharField(max_length=300,blank=True,null=True)
    graduation_marks_obtained=models.CharField(max_length=100,blank=True,null=True)
    graduation_passing_year=models.CharField(max_length=100,blank=True,null=True)
    #PG
    pg_Degree_Diploma=models.CharField(max_length=300,blank=True,null=True)
    pg_subjects=models.CharField(max_length=300,blank=True,null=True)
    pg_name_location=models.CharField(max_length=300,blank=True,null=True)
    pg_marks_obtained=models.CharField(max_length=100,blank=True,null=True)
    pg_passing_year=models.CharField(max_length=100,blank=True,null=True)
    #Professional Qualification    professional_qualification
    professional_qualification_Degree_Diploma=models.CharField(max_length=300,blank=True,null=True)
    professional_qualification_subjects=models.CharField(max_length=300,blank=True,null=True)
    professional_qualification_name_location=models.CharField(max_length=300,blank=True,null=True)
    professional_qualification_marks_obtained=models.CharField(max_length=100,blank=True,null=True)
    professional_qualification_passing_year=models.CharField(max_length=100,blank=True,null=True)
    #others
    others_qualification_Degree_Diploma=models.CharField(max_length=300,blank=True,null=True)
    others_qualification_subjects=models.CharField(max_length=300,blank=True,null=True)
    others_qualification_name_location=models.CharField(max_length=300,blank=True,null=True)
    others_qualification_marks_obtained=models.CharField(max_length=100,blank=True,null=True)
    others_qualification_passing_year=models.CharField(max_length=100,blank=True,null=True)

    #TRAINING PROGRAMS/WORKSHOP ATTENDED
    training_workshop_title=models.CharField(max_length=300,blank=True,null=True)
    training_workshop_Institution_location=models.CharField(max_length=300,blank=True,null=True)
    training_workshop_skill=models.CharField(max_length=300,blank=True,null=True)
    training_workshop_duration=models.CharField(max_length=100,blank=True,null=True)
    training_workshop_start_date=models.CharField(max_length=100,blank=True,null=True)

    #CURRENT EMPLOYMENT DETAILS
    current_emp_start_date=models.DateField(blank=True,null=True)
    current_employer=models.CharField(max_length=300,blank=True,null=True)
    current_emp_salary=models.CharField(max_length=100,blank=True,null=True)
    current_emp_benefits=models.CharField(max_length=300,blank=True,null=True)
    current_emp_position=models.CharField(max_length=200,blank=True,null=True)
    current_emp_reason_for_leaving=models.CharField(max_length=300,blank=True,null=True)
    expected_salary=models.CharField(max_length=100,blank=True,null=True)
    current_emp_job_description=models.CharField(max_length=300,blank=True,null=True)
    current_emp_supervisor_name=models.CharField(max_length=300,blank=True,null=True)
    
    #FAMILY DETAILS 
    father_name=models.CharField(max_length=200,blank=True,null=True)
    father_dob=models.DateField(blank=True,null=True)
    father_profession=models.CharField(max_length=200,blank=True,null=True)
    mother_name=models.CharField(max_length=200,blank=True,null=True)
    mother_dob=models.DateField(blank=True,null=True)
    mother_profession=models.CharField(max_length=200,blank=True,null=True)
    spouse_name=models.CharField(max_length=200,blank=True,null=True)
    spouse_dob=models.DateField(blank=True,null=True)
    spouse_profession=models.CharField(max_length=200,blank=True,null=True)
    Children_name_1=models.CharField(max_length=200,blank=True,null=True)
    Children_name_2=models.CharField(max_length=200,blank=True,null=True)
    Children_dob_1=models.DateField(blank=True,null=True)
    Children_dob_2=models.DateField(blank=True,null=True)
    Children_1_profession=models.CharField(max_length=200,blank=True,null=True)
    Children_2_profession=models.CharField(max_length=200,blank=True,null=True)

    reason_to_apply_sonata=models.CharField(max_length=300,blank=True,null=True)
    willing_to_relocate=models.BooleanField(default=True,blank=True,null=True)
    interviewed_by_Sonata_before=models.BooleanField(default=False,blank=True,null=True)
    locational_preferences=models.CharField(max_length=200,blank=True,null=True)

    reviewed_by = models.IntegerField(blank=True,null=True)
    is_user = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True,null=True)

    class Meta:
        db_table = 'CANDIDATE_DETAILS'


class Interview(models.Model):
    INTERVIEW_STATUS=((0,'ShortlistedCV'),(1,'Scheduled'),(2,'Hold'),(3,'Rejected'),(4,'Attended'),(5,'Selected'),(6,'NotSelected'))
    candidate_id = models.IntegerField(blank=True,null=True)
    interview_date = models.DateField(blank=True,null=True)
    position = models.CharField(max_length=200,blank=True,null=True)
    interview_time = models.TimeField(blank=True,null=True)
    interview_panel_list = models.CharField(max_length=200,blank=True,null=True)
    interview_status = models.CharField(max_length=200,blank=True,null=True)
    interview_score = models.DecimalField(blank=True,null=True,max_digits=5, decimal_places=2)


class Rolls(models.Model):
    roll_name = models.CharField(max_length=255,blank=True,null=True)
    roll_id = models.IntegerField(blank=True,null=True)

class User_Rolls(models.Model):
    user_id = models.IntegerField(blank=True,null=True)
    roll_id = models.IntegerField(blank=True,null=True, default=0)
    

class rejected_review_allotment(models.Model):
    candidate_id = models.IntegerField(blank=True,null=True)
    hr_id = models.IntegerField(blank=True,null=True)
    remarks = models.CharField(max_length=200, blank=True, null=True)
    alloted_datetime = models.DateTimeField(blank=True,null=True,auto_now_add=True)
    review_status = models.BooleanField(default=False)
    
class question_sheet(models.Model):
    sheet_id = models.IntegerField(blank=True,null=True)
    question_id = models.IntegerField(blank=True,null=True)
    question_text = models.CharField(max_length=500, blank=True, null=True)
    option_a = models.CharField(max_length=500, blank=True, null=True)
    option_b = models.CharField(max_length=500, blank=True, null=True)
    option_c = models.CharField(max_length=500, blank=True, null=True)
    option_d = models.CharField(max_length=500, blank=True, null=True)
    answer = models.CharField(max_length=500, blank=True, null=True)
   
class exam_response(models.Model):
    candidate_id =  models.IntegerField(blank=True,null=True)
    sheet_id = models.IntegerField(blank=True,null=True)
    question_id  = models.IntegerField(blank=True,null=True)
    response = models.CharField(max_length=500, blank=True, null=True)
    
class TestSchedule(models.Model):
    sheet_id = models.IntegerField(blank=True,null=True)
    candidate_id = models.IntegerField(blank=True,null=True)
    exam_date = models.DateField(blank=True,null=True)
    is_online = models.BooleanField(blank=True,null=True)
    score = models.IntegerField(blank=True,null=True)
    status = models.CharField(max_length=255,blank=True,null=True)
    start_time = models.TimeField(blank=True,null=True)
    end_time = models.TimeField(blank=True,null=True)
    offline_answersheet = models.BinaryField(blank=True,null=True)

class TestResponse(models.Model):
    test_schedule_id = models.IntegerField(blank=True,null=True)
    question_id = models.IntegerField(blank=True,null=True)
    response = models.CharField(max_length=255,blank=True,null=True)

class Resume_Repository(models.Model):
    candidate_id = models.IntegerField(blank=True,null=True)
    resume = models.BinaryField(blank=True,null=True)
    mime_type = models.CharField(max_length=100,null=True,blank=True)
    
class Candidate_Camshot(models.Model):
    application_id = models.IntegerField()
    camshot = models.BinaryField()
    
    class Meta:
         db_table = 'Accounts_candidate_camshot' 
class interview_assignment(models.Model):
    candidate_id=models.IntegerField()
    interviewer_id=models.IntegerField()
    field_1=models.IntegerField()
    field_2=models.IntegerField()
    field_3=models.IntegerField()
    field_4=models.IntegerField()
    field_5=models.IntegerField()
    field_6=models.IntegerField()
    field_7=models.IntegerField()
    field_8=models.IntegerField()
    field_9=models.IntegerField()
    field_10=models.IntegerField()
    field_11=models.IntegerField()
    field_12=models.IntegerField()
    field_13=models.IntegerField()
    field_14=models.IntegerField()
    field_15=models.IntegerField()
    field_16=models.IntegerField()
    field_17=models.IntegerField()
    field_18=models.IntegerField()
    field_19=models.IntegerField()
    field_20=models.IntegerField()
    total_A=models.IntegerField()
    total_B=models.IntegerField()
    total=models.IntegerField()
    score=models.FloatField()

    class Meta:
         db_table = 'interview_assignment' 
class State(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=50)
    
    class Meta:
         db_table = 'allstates' 
class citywithstate(models.Model):
    id= models.IntegerField(primary_key=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'citywithstate'
class vacancy(models.Model):
    branch_name = models.CharField(max_length=200,blank=True,null=True)
    no_of_vacancies = models.IntegerField(blank=True,null=True)
    job_role = models.CharField(max_length=200,blank=True,null=True)
    required_experience = models.DecimalField(max_digits=200, decimal_places=2,blank=True,null=True)
    required_skills = models.CharField(max_length=200,blank=True,null=True)
    salary = models.IntegerField(blank=True,null=True)
    qualification_type = models.CharField(max_length=200,blank=True,null=True)
    interview_place=models.CharField(max_length=200,blank=True,null=True)
    interview_date = models.DateField(blank=True,null=True)
    interview_time = models.TimeField(blank=True,null=True)
    interview_panel_1=models.IntegerField(blank=True,null=True)
    interview_panel_2=models.IntegerField(blank=True,null=True)
    interview_panel_3=models.IntegerField(blank=True,null=True)
    interview_panel_4=models.IntegerField(blank=True,null=True)
    panel_list=models.CharField(max_length=100,blank=True,null=True)
    job_responsibility=models.TextField(blank=True,null=True)
    job_description=models.TextField(blank=True,null=True)
    posted_on = models.DateField(blank=True,null=True)

# class CandidateDetails(models.Model):
#     candidate_id = models.AutoField(primary_key=True)
#     vacancy_id = models.IntegerField(null=True, blank=True)
#     hold_date = models.DateTimeField(null=True, blank=True)
#     reject_reason = models.CharField(max_length=255, null=True, blank=True)
#     position_shortlisted_for = models.CharField(max_length=255, null=True, blank=True)
#     branch_shortlisted_for = models.CharField(max_length=255, null=True, blank=True)
#     interview_date = models.DateTimeField(null=True, blank=True)
#     interview_panel_list = models.CharField(max_length=255, null=True, blank=True)
#     interview_time = models.TimeField(null=True, blank=True)
#     name = models.CharField(max_length=50, null=True, blank=True)
#     email = models.EmailField(max_length=50, null=True, blank=True)
#     is_user = models.BooleanField(null=True, blank=True)

#     class Meta:
#         db_table = 'candidate_details'
class ApplicationDetails(models.Model):
    application_id = models.AutoField(primary_key=True)
    interview_id = models.IntegerField(null=True, blank=True)
    position_shortlisted_for = models.CharField(max_length=255, null=True, blank=True)
    branch_shortlisted_for = models.CharField(max_length=255, null=True, blank=True)
    hold_date = models.DateTimeField(null=True, blank=True)
    reject_reason = models.CharField(max_length=255, null=True, blank=True)
    hold_reason = models.CharField(max_length=255, null=True, blank=True)
    reject_date = models.DateTimeField(null=True, blank=True)
    candidate_id = models.IntegerField(null=True, blank=True)
    application_date = models.DateTimeField(null=True, blank=True)
    application_status = models.IntegerField(null=True, blank=True)
    checked_by = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'application_details'
class TestScheduleDetails(models.Model):
    test_id = models.AutoField(primary_key=True)
    application_id = models.IntegerField(null=True, blank=True)
    test_status = models.CharField(max_length=50, null=True, blank=True, default=0)
    test_score = models.IntegerField(null=True, blank=True)
    test_date = models.DateField(null=True, blank=True)
    is_online = models.BooleanField(default=False)
    candidate_id = models.IntegerField(null=True, blank=True)
    sheet_id = models.IntegerField(null=True, blank=True)
    # start_time = models.DateTimeField(null=True, blank=True)
    # end_time = models.DateTimeField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    offline_answersheet = models.BinaryField(null=True, blank=True)

    class Meta:
        db_table = 'test_schedule'
class TestResponseDetails(models.Model):
    response_id = models.AutoField(primary_key=True)
    test_id = models.IntegerField(null=True, blank=True)
    response_date = models.DateTimeField(null=True, blank=True)
    question_id = models.IntegerField(null=True, blank=True)
    answer = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'test_response'
class InterviewDetails(models.Model):
    interview_id = models.AutoField(primary_key=True)
    vacancy_id = models.IntegerField(null=True, blank=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_time = models.TimeField(null=True, blank=True)
    interview_place = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    panel_member_a = models.IntegerField(null=True, blank=True)
    panel_member_b = models.IntegerField(null=True, blank=True)
    panel_member_c = models.IntegerField(null=True, blank=True)
    optional_member = models.IntegerField(null=True, blank=True)
    panel_list = models.CharField(max_length=255, null=True, blank=True)
    posted_on = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'interview_details'
class InterviewResponse(models.Model):
    response_id = models.AutoField(primary_key=True)
    application_id = models.IntegerField(null=True, blank=True)
    interviewer_id = models.IntegerField(null=True, blank=True)
    field_1 = models.CharField(max_length=255, null=True, blank=True)
    field_2 = models.CharField(max_length=255, null=True, blank=True)
    field_3 = models.CharField(max_length=255, null=True, blank=True)
    field_4 = models.CharField(max_length=255, null=True, blank=True)
    field_5 = models.CharField(max_length=255, null=True, blank=True)
    field_6 = models.CharField(max_length=255, null=True, blank=True)
    field_7 = models.CharField(max_length=255, null=True, blank=True)
    field_8 = models.CharField(max_length=255, null=True, blank=True)
    field_9 = models.CharField(max_length=255, null=True, blank=True)
    field_10 = models.CharField(max_length=255, null=True, blank=True)
    field_11 = models.CharField(max_length=255, null=True, blank=True)
    field_12 = models.CharField(max_length=255, null=True, blank=True)
    field_13 = models.CharField(max_length=255, null=True, blank=True)
    field_14 = models.CharField(max_length=255, null=True, blank=True)
    field_15 = models.CharField(max_length=255, null=True, blank=True)
    field_16 = models.CharField(max_length=255, null=True, blank=True)
    field_17 = models.CharField(max_length=255, null=True, blank=True)
    field_18 = models.CharField(max_length=255, null=True, blank=True)
    field_19 = models.CharField(max_length=255, null=True, blank=True)
    field_20 = models.CharField(max_length=255, null=True, blank=True)
    total_A = models.IntegerField(null=True, blank=True)
    total_B = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'interview_response'
class VacancyDetails(models.Model):
    vacancy_id = models.AutoField(primary_key=True)
    walk_in_id = models.IntegerField(null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    vacancy_description = models.CharField(max_length=50, null=True, blank=True)
    vacancy_status = models.CharField(max_length=50, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    vacancy_date = models.DateTimeField(null=True, blank=True)
    job_responsibility = models.CharField(max_length=255, null=True, blank=True)
    job_description = models.TextField(null=True, blank=True)
    required_experience = models.CharField(max_length=255, null=True, blank=True)
    required_skills = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'vacancy_details'
class ResumeFiles(models.Model):
    id = models.AutoField(primary_key=True)
    candidate_id = models.IntegerField(null=True, blank=True)
    resume = models.BinaryField(null=True, blank=True)
    mime_type = models.CharField(max_length=100, null=True, blank=True)
    resumeFile = models.FileField(upload_to='media/',null=True,blank=True)
    class Meta:
        db_table = 'resume_files'

class RejectReviewAllotment(models.Model):
    id = models.AutoField(primary_key=True)
    application_id = models.IntegerField()
    alloted_to = models.IntegerField(null=True, blank=True)
    is_reviewed = models.BooleanField(null=True, blank=True)
    result = models.BooleanField(null=True, blank=True)
    remark = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'REJECT_REVIEW_ALLOTMENT'
class ContactUsTable(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(null=True,blank=True,max_length=50)
    mobile_no = models.BigIntegerField()
    message = models.TextField(max_length=200,null=True,blank=True)
    
    class Meta:
        db_table = 'CONTACT_TABLE'
    
class Forgot_Password_Table(models.Model):
    ID = models.IntegerField()
    username = models.CharField(max_length=50,null=True,blank=True)
    reset_key = models.CharField(max_length=50,null=True,blank=True)
    
    class Meta:
        db_table='FORGOT_PASSWORD_TABLE'
        
class Document_Candidate(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    aadhar_doc = models.FileField(upload_to='media/',null=True, blank=True)
    pan_doc = models.FileField(upload_to='media/',null=True, blank=True)
    dl_doc = models.FileField(upload_to='media/',null=True, blank=True)
    candidate_id = models.IntegerField(null=True, blank=True)
    ssc_doc = models.FileField(upload_to='media/',null=True, blank=True)
    hsc_doc = models.FileField(upload_to='media/',null=True, blank=True)
    graduate_doc = models.FileField(upload_to='media/',null=True, blank=True)
    class Meta:
        db_table = 'UPLOAD_DOCUMENTS'


class WhatsAppConversations(models.Model):
    MessageID = models.AutoField(primary_key=True)
    UserID = models.IntegerField()
    CustomerInfoID = models.IntegerField()
    ConversationID = models.IntegerField()
    message_date = models.DateField()
    message_time = models.TimeField()
    MessageText = models.TextField()
    Direction = models.CharField(max_length=15)
    AttachmentURLs = models.TextField()  # You can use JSONField if you want to store JSON data
    MessageType = models.CharField(max_length=20)
    Status = models.CharField(max_length=20)
    IsRead = models.BooleanField()
    SequenceNumber = models.IntegerField()

    class Meta:
        managed = False
        db_table = "WhatsAppConversations"

class LeadRepositoryDem(models.Model):
    CustomerInfoID = models.IntegerField()
    mobile = models.IntegerField()
    name = models.TextField()
    opt_in_status = models.BooleanField(default=False)
    is_lead = models.BooleanField(default=False)
    is_bot_enabled = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = "LeadRepositoryDem"


class LeadQueue(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField()
    lead_id = models.BigIntegerField()
    stage = models.CharField(max_length=10)
    status = models.IntegerField()
    last_messate_sent_datetime = models.DateTimeField()
    message_send_scheduled_datetime = models.DateTimeField()
    last_message_sent_response = models.CharField(max_length=255)
    last_message_sent_exception = models.CharField(max_length=255)
    task_id = models.IntegerField()
    counter = models.IntegerField()
    queue_start_datetime = models.DateTimeField()
    field1 = models.CharField(max_length=255)
    field2 = models.CharField(max_length=255)
    field3 = models.CharField(max_length=255)
    field4 = models.CharField(max_length=255)
    field5 = models.CharField(max_length=255)
    field6 = models.CharField(max_length=255)
    field7 = models.CharField(max_length=255)
    field8 = models.CharField(max_length=255)
    field9 = models.CharField(max_length=255)
    field10 = models.CharField(max_length=255)
    field11 = models.CharField(max_length=255)
    field12 = models.CharField(max_length=255)
    field13 = models.CharField(max_length=255)
    field14 = models.CharField(max_length=255)
    field15 = models.CharField(max_length=255)
    field16 = models.CharField(max_length=255)
    field17 = models.CharField(max_length=255)
    field18 = models.CharField(max_length=255)
    field19 = models.CharField(max_length=255)
    field20 = models.CharField(max_length=255)
    mobile = models.BigIntegerField()
    document_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "LeadQueue"


class LeadDocumentRepository(models.Model):
    lead_id = models.IntegerField()
    uploaded_file = models.FileField(upload_to='Lead_Documents/', blank=True, null=True)
    file_status = models.IntegerField()
    file_type = models.IntegerField()
    reject_reason = models.CharField(max_length=50)
    file_url = models.CharField(max_length=500)
    download_status = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = "lead_document_repository"