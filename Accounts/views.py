import base64
from collections import Counter
import pprint
import string
from urllib import parse
import cv2
from django.contrib import messages
import json
from os import path
import os
import random
from urllib.request import urlopen
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import numpy as np
from Accounts.models import User_Details,question_sheet, User_Rolls,rejected_review_allotment, TestSchedule,vacancy
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import QuestionForm, VacancyForm
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, transaction
import pandas as pd
from django.shortcuts import get_object_or_404
from Accounts.models import *
from datetime import date, datetime, timedelta
import requests
import json
from sqlalchemy import create_engine
from django.views import View
from .decorators import can_access_candidate_profile

from django.shortcuts import get_object_or_404



user1 = "SFPL_Connect"
password = "$%n5bF33%X"
db = "Sonata_ConnectHR"
server = "172.17.130.216"
engine = create_engine(f"mssql+pyodbc://{user1}:{password}@{server}/{db}?driver=ODBC+Driver+17+for+SQL+Server")
cursor = connection.cursor()




# Create your views here.
def Login(request):
    if request.method == "POST":
        # Get the post parameters
        username=request.POST.get('username')
        pass1 =request.POST.get('pass1')

        print(username,pass1)
        user=authenticate(request,username = username, password = pass1)
        if user is not None:
            if user.is_active:
                request.session.set_expiry(0)
                login(request, user)
                # Redirect to the 'next' parameter if available, or 'dashboard' if not
                print(request.session.get('next_param'))
                next_param = request.session.get('next_param')
                if next_param:
                    return redirect(next_param)
                else:
                    messages.success(request, "Successfully Logged In")
                    return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect('signIn')

    # return HttpResponse("404- Not found")
    return render(request, 'Sign-In.html')

def signIn(request):
    print(request.GET)
    next_param = request.GET.get('next')
    print("Next Param:", next_param)
    request.session['next_param'] = next_param
    return render(request, 'Sign-In.html')

@transaction.atomic
def signUp(request):
    if request.method == "POST":
        print('post')
        # Get the post parameters
        username=request.POST.get('user')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        name=request.POST.get('name')
        dob=request.POST.get('dob')
        mob=request.POST.get('mob')
        gender=request.POST.get('gender')
        
        if (pass1!= pass2):
            messages.error(request, "Passwords do not match")
            signup = True
            return render(request, 'Sign-in.html', {'signup': signup})
        try:
            myuser = User.objects.create_user(username, email, pass1)
            # myuser.save()
            # user_roll=User_Rolls(user_id=myuser.id,roll_id=0)
            # user_roll.save()
            
            print("User Data")
            print(username,email,pass1,pass2,name,dob,mob,gender)
            if candidate_details.objects.filter(email=email).count() >=1:
                candidate_profile = candidate_details.objects.get(email=email)
                candidate_profile.name=name
                # candidate_profile.email=email
                candidate_profile.gender=gender
                candidate_profile.dob=dob
                candidate_profile.mobile_no=mob
                candidate_profile.save()
                user_roll=User_Rolls(user_id=myuser.id,roll_id=0)
                doc = Document_Candidate()
                doc.candidate_id = candidate_profile.id
                
                verify = Verification_Document()
                verify.candidate_id = candidate_profile.id
                
                letter = OfferLetter()
                letter.candidate_id = candidate_profile.id
            else:
                candidate_profile = candidate_details()
                candidate_profile.name=name
                candidate_profile.email=email
                candidate_profile.gender=gender
                candidate_profile.dob=dob
                candidate_profile.mobile_no=mob
                candidate_profile.save()
                user_roll=User_Rolls(user_id=myuser.id,roll_id=0)
                doc = Document_Candidate()
                doc.candidate_id = candidate_profile.id
                
                verify = Verification_Document()
                verify.candidate_id = candidate_profile.id
                
                letter = OfferLetter()
                letter.candidate_id = candidate_profile.id
            myuser.save()
            user_roll.save()
            doc.save()
            verify.save()
            letter.save()
            #print(user_profile)
            print("account_created")
            messages.success(request, " Your account has been successfully created")
            return redirect('signIn')

        except Exception as e:
            print(e)
            messages.error(request,"Exception caught")
            signup = True       
            return render(request, 'Sign-in.html', {'signup': signup})

    else:
        print("failed")
        # return HttpResponse("404 - Not found")
        # messages.error(request, "failed")
        signup = True       
        return render(request, 'Sign-in.html', {'signup': signup})
    
def Logout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home_page')


def checkdublicate1(request, username):
    user_count = User.objects.filter(username=username).count()
    print(user_count)
    if user_count >= 1:
        return JsonResponse({'is_duplicate': True})
    else:
        return JsonResponse({'is_duplicate': False})

def checkdublicate2(request, email):
    user_count=User.objects.filter(email = email).count()
    print(user_count)
    if user_count >= 1:
        return JsonResponse({'is_duplicate': True})
    else:
        return JsonResponse({'is_duplicate': False})

def checkdublicate3(request, mobile):
    user_count=candidate_details.objects.filter(mobile_no = mobile).count()
    print(user_count)
    if user_count >= 1:
        return JsonResponse({'is_duplicate': True})
    else:
        return JsonResponse({'is_duplicate': False})
    
def checkdublicate4(request, email):
    user_count=candidate_details.objects.filter(email = email).count()
    print('same email count: ',user_count)
    if user_count >= 1:
        return JsonResponse({'is_duplicate': True})
    else:
        return JsonResponse({'is_duplicate': False})

@transaction.atomic
@login_required(login_url='signIn')
def dashboard(request):
    context={}
    user_id=request.user.id
    email=request.user.email
    context['id']=user_id
    user_roll=User_Rolls.objects.get(user_id=user_id)
    
    data=[]
    username=request.user.username
    context['username']=username
    #check if HR
    if user_roll.roll_id==1:
        sql_query = f'''
        EXEC dbo.dashboard_counter
        '''
        dash_df = pd.read_sql_query(sql_query, engine)
        dash_dict = dash_df.to_dict(orient='records')[0]
        print(dash_dict)
        context['counts'] = dash_dict
        return render(request, 'index copy.html',context)   
    # context={
            
    #         'username' : username,
    #         'new_user_count':new_user_count,
    #         'schedule_online_test_count' : schedule_online_test_count,
    #         'reject_candidates_count' : reject_candidates_count,
    #         'hold_candidates_count': hold_candidates_count,
    #         'scheduled_interview_count' : scheduled_interview_count,
    #         'hr_scheduled_interview_count' : hr_scheduled_interview_count,
    #         'vacancy_list_count' : vacancy_list_count,
    #         'Onboarding_candidates_count1':Onboarding_candidates_count1,
    #         'offline_test_count':offline_test_count,
    #         'shortlist_candidates_count' : shortlist_candidates_count,
            
    #         }
    # check if candidate:
    if user_roll.roll_id==0:
        vacancy_list = []
        try:
            # candidate instance
            today = datetime.today().date()
            candidate = candidate_details.objects.get(email=email)
            
            # fetching all applicaitions into a df
            application_df = pd.DataFrame(ApplicationDetails.objects.filter(candidate_id=candidate.id).values())
            # getting applied interview list
            interview_id_list = application_df['interview_id'].unique().tolist()
            print('interview_list',interview_id_list)
            # getting interviews into a df
            interview_df = pd.DataFrame(InterviewDetails.objects.filter(Q(interview_id__in=interview_id_list) |Q(interview_date__lte=today)).values())
            # list of vacancies of these interviews
            vacancy_list = interview_df['vacancy_id'].unique().tolist()
            print('vacancy_list',vacancy_list)
            # checking if candidate has updated his profile with mandatory details
            doc_can_id = Document_Candidate.objects.get(candidate_id = candidate.id)
            print('doc_can_id',doc_can_id)
            
            
                    
            if candidate.status == 1:
                print('status 1')
                
                app = ApplicationDetails.objects.get(candidate_id = candidate.id)

                if app.application_status >= 2  :
                    
                    if ((doc_can_id.aadhar_doc == "" or doc_can_id.aadhar_doc == None) | (doc_can_id.pan_doc == "" or doc_can_id.pan_doc == None) | (doc_can_id.dl_doc == "" or doc_can_id.dl_doc == None) | (doc_can_id.hsc_doc == "" or doc_can_id.hsc_doc == None)):
                        messages.error(request, "Please Update your documents first.")
                    else:
                        
                        # try:
                        #     profile = candidate_details.objects.get(id=app.candidate_id)
                        #     encoded_id = encode_id(app.candidate_id)
                        #     print(encoded_id)
                            
                        #     url = f"https://media.smsgupshup.com/GatewayAPI/rest?userid=2000209909&password=z24gzBUA&send_to={profile.mobile_no}&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=Your+documents+is+missing+please+upload+{profile.name}.%0APlease+click+on+the+below+link+to+access+your+update+documents+link.&isTemplate=true&header=Greetings+From+Sonata&buttonUrlParam={encoded_id}"
                        #     print(url)
                        #     payload = {}
                        #     headers = {}
                        #     response = requests.request("GET", url, headers=headers, data=payload)
                        #     return redirect('Test')
                        # except Exception as e:
                        #     messages.error(request, "Please Update your documents first.")
                        messages.success(request, "Documents Uploaded Successfully .")
                        # return redirect('profile_update',candidate_id=candidate.id)
                    
                # # whether has a post grad
                # if candidate.pg_Degree_Diploma is not None:
                #     vacancies = VacancyDetails.objects.filter(Q(qualification__in=['Post Graduation','Under Graduation','Intermediate', 'Secondary'])|Q(qualification=None)).exclude(vacancy_id__in=vacancy_list)
                # # whether graduated 
                # elif candidate.graduation_Degree_Diploma is not None:
                #     vacancies = VacancyDetails.objects.filter(Q(qualification__in=['Under Graduation','Intermediate', 'Secondary'])|Q(qualification=None)).exclude(vacancy_id__in=vacancy_list)
                # # whether 12 pass
                # elif candidate.intermediate_Degree_Diploma is not None:
                #     vacancies = VacancyDetails.objects.filter(Q(qualification__in=['Intermediate', 'Secondary'])|Q(qualification=None)).exclude(vacancy_id__in=vacancy_list)
                # # whether 10 pass
                # elif candidate.high_school_Degree_Diploma is not None:
                #     vacancies = VacancyDetails.objects.filter(Q(qualification__in=['Secondary'])|Q(qualification=None)).exclude(vacancy_id__in=vacancy_list)
                # # no educational qualifs
                # else:
                #     vacancies = VacancyDetails.objects.filter(qualification=None).exclude(vacancy_id__in=vacancy_list)
                vacancies = VacancyDetails.objects.filter(walk_in_id=1).exclude(vacancy_id__in=vacancy_list)
            # ed details not updated
            else:
                vacancies = VacancyDetails.objects.filter(walk_in_id=1).exclude(vacancy_id__in=vacancy_list)
        # some error
                

        except Exception as e:
            print('exc:', e)
            vacancy_idlist = InterviewDetails.objects.filter(interview_date__gte=today).values_list('vacancy_id')
            vacancies = VacancyDetails.objects.filter(vacancy_id__in = vacancy_idlist,walk_in_id=1)
        # vacancy_idlist = InterviewDetails.objects.filter(interview_date__gte=(datetime.now() - relativedelta(days=1))).values_list('vacancy_id')
        # vacancies = VacancyDetails.objects.filter(vacancy_id__in = vacancy_idlist,walk_in_id=1)
       
        for i in vacancies:
            d = {}
            d['id']=i.vacancy_id
            d['branch_name']=i.branch if i.branch else "-"
            d['required_skills']=i.required_skills.split(",") if i.required_skills else []
            d['job_role']=i.role if i.role else "-"
            d['no_of_vacancies']=i.capacity if i.capacity else "-"
            d['qualification_type']=i.qualification if i.qualification else "-"
            d['required_experience']=i.required_experience if i.required_experience else "-"
            d['salary']=int(i.salary) if int(i.salary) else "-"
            d['vacancy_date']=i.vacancy_date if i.vacancy_date else "-"
            data.append(d)
        context['vacancies']=data
        
        data1 = []
        today = datetime.today().date()
        print("todayyyyyyyyyy",today)
        # vacancy_idlist = InterviewDetails.objects.filter(interview_date__gte=(datetime.now() - relativedelta(days=1))).values_list('vacancy_id')
        # vacancies1 = VacancyDetails.objects.filter(vacancy_id__in = vacancy_idlist,walk_in_id=0)
        try:
            vacancy_idlist = InterviewDetails.objects.filter(interview_date__gt=today).values_list('vacancy_id')
            vacancies = VacancyDetails.objects.filter(vacancy_id__in = vacancy_idlist,walk_in_id=0).exclude(vacancy_id__in=vacancy_list)
        except:
            vacancy_idlist = InterviewDetails.objects.filter(interview_date__gt=today).values_list('vacancy_id')
            vacancies = VacancyDetails.objects.filter(vacancy_id__in = vacancy_idlist,walk_in_id=0)
        for i in vacancies:
            f = {}
            f['id']=i.vacancy_id
            f['branch_name']=i.branch if i.branch else "-"
            f['required_skills']=i.required_skills.split(",") if i.required_skills else []
            f['job_role']=i.role if i.role else "-"
            f['no_of_vacancies']=i.capacity if i.capacity else "-"
            f['qualification_type']=i.qualification if i.qualification else "-"
            f['required_experience']=i.required_experience if i.required_experience else "-"
            f['salary']=int(i.salary) if int(i.salary) else "-"
            f['vacancy_date']=i.vacancy_date if i.vacancy_date else "-"
            data1.append(f)
        context['vacancies1']=data1


    elif user_roll.roll_id==2:
        sql_query = f'''
        EXEC dbo.dashboard_counter
        '''
        dash_df = pd.read_sql_query(sql_query, engine)
        dash_dict = dash_df.to_dict(orient='records')[0]
        print(dash_dict)
        context['counts'] = dash_dict
        return render(request, 'interviewer_dashboard.html',context)
    elif user_roll.roll_id==3:
        sql_query = f'''
        EXEC dbo.dashboard_counter
        '''
        dash_df = pd.read_sql_query(sql_query, engine)
        dash_dict = dash_df.to_dict(orient='records')[0]
        print(dash_dict)
        context['counts'] = dash_dict
        return render(request,'HEADHR.html',context)
    context['id']=user_id
    context['candidate_id']=candidate_details.objects.get(email = email).id
    print('candid', context['candidate_id'])
    context['email']=email
    profile=candidate_details.objects.get(email=email)
    context['profile']=profile
    # context['doc_can_id'] =doc_can_id
    # profile=User_Details.objects.get(id=user_id)
    # context['profile']=profile
    connection.close()
    return render(request, 'candidate_dashboard.html',context)

from django.forms.models import model_to_dict


def profile(request):
    if request.method=="POST":
        refId = request.POST['refId']
        if len(refId) > 9:
            refId = refId[9:]
        print("<<<<<"+refId+">>>>>")
        try:
            # application = ApplicationDetails.objects.get(application_id=refId)
            user_profile = candidate_details.objects.get(id=refId)
        
            if(user_profile.status==0):
          
                messages.error(request, "Your profile is Incomplete.Kindly complete your profile for further processing.")
            redirect_url = reverse('applied_user_full_details',args=[refId])
            return redirect(redirect_url)
        except Exception as e:
            print(e)
            messages.error(request, "No records found")
            return redirect('signIn')
    else:
        return redirect('signIn')

from PIL import Image
import pytesseract
import re
# from Accounts.aadhaar_read import front_data
def profile_update(request,candidate_id):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    print('profile updaate hit')
    if candidate_id is not None:
        candidate_profile = candidate_details.objects.get(id=candidate_id)
        try:
            resume_obj = ResumeFiles.objects.get(candidate_id = candidate_profile.id)
            resume = resume_obj.resume
            mime_type = resume_obj.mime_type
            encoded_data = base64.b64encode(resume).decode('utf-8')
           
        except Exception as e:
            print(e)
            encoded_data = None
            mime_type = None
            
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = candidate_profile.id)
            aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
            ssc_doc = document_obj.ssc_doc if document_obj.ssc_doc else None
            hsc_doc = document_obj.hsc_doc if document_obj.hsc_doc else None
            graduate_doc = document_obj.graduate_doc if document_obj.graduate_doc else None
            pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
            dl_doc = document_obj.dl_doc  if document_obj.dl_doc else None
        except Exception as e:
            aadhar_doc = None
            ssc_doc = None
            hsc_doc = None
            graduate_doc = None     
            pan_doc = None
            dl_doc = None
    else:
        candidate_profile = None
    document_obj = Document_Candidate.objects.get(candidate_id = candidate_profile.id)
    if request.method == "POST":
        print('post hit')
        # try:
        candidate_profile = candidate_details.objects.get(id=candidate_profile.id)
        candidate_profile.name = request.POST['name']
        candidate_profile.email = request.POST['email']
        candidate_profile.mobile_no = request.POST['mobile_no']
        # candidate_profile.address = request.POST['address']
        candidate_profile.dob = datetime.strptime(request.POST['dob'],"%Y-%m-%d").replace(tzinfo=timezone.utc)
        candidate_profile.gender = request.POST['gender']
        candidate_profile.identity_Aadhar = request.POST['identity_Aadhar'] or None
        candidate_profile.identity_PAN = request.POST['identity_PAN'] or None
        candidate_profile.identity_DL_No = request.POST['identity_DL_No'] or None
        # candidate_profile.position_applied_for = request.POST['position_applied_for'] or None
        # candidate_profile.applied_date = request.POST['applied_date'] or None
        # candidate_profile.name = request.POST['name'] or None
        candidate_profile.present_city = request.POST['present_city'] or None
        candidate_profile.present_pin = request.POST['present_pin'] or None
        candidate_profile.present_state = request.POST['present_state'] or None
        candidate_profile.permanent_city = request.POST['permanent_city'] or None
        candidate_profile.permanent_pin = request.POST['permanent_pin'] or None
        candidate_profile.permanent_state = request.POST['permanent_state'] or None
        candidate_profile.high_school_Degree_Diploma = request.POST['high_school_Degree_Diploma'] or None
        # candidate_profile.high_school_subjects = request.POST['high_school_subjects'] or None
        candidate_profile.high_school_name_location = request.POST['high_school_name_location'] or None
        candidate_profile.high_school_marks_obtained = request.POST['high_school_marks_obtained'] or None
        candidate_profile.high_school_passing_year = request.POST['high_school_passing_year'] or None
        candidate_profile.intermediate_Degree_Diploma = request.POST['intermediate_Degree_Diploma'] or None
        # candidate_profile.intermediate_subjects = request.POST['intermediate_subjects'] or None
        candidate_profile.intermediate_name_location = request.POST['intermediate_name_location'] or None
        candidate_profile.intermediate_marks_obtained = request.POST['intermediate_marks_obtained'] or None
        candidate_profile.intermediate_passing_year = request.POST['intermediate_passing_year'] or None
        candidate_profile.graduation_Degree_Diploma = request.POST['graduation_Degree_Diploma'] or None
        # candidate_profile.graduation_subjects = request.POST['graduation_subjects'] or None
        candidate_profile.graduation_name_location = request.POST['graduation_name_location'] or None
        candidate_profile.graduation_marks_obtained = request.POST['graduation_marks_obtained'] or None
        candidate_profile.graduation_passing_year = request.POST['graduation_passing_year'] or None
        candidate_profile.pg_Degree_Diploma = request.POST['pg_Degree_Diploma'] or None
        # candidate_profile.pg_subjects = request.POST['pg_subjects'] or None
        candidate_profile.pg_name_location = request.POST['pg_name_location'] or None
        candidate_profile.pg_marks_obtained = request.POST['pg_marks_obtained'] or None
        candidate_profile.pg_passing_year = request.POST['pg_passing_year'] or None
        candidate_profile.professional_qualification_Degree_Diploma = request.POST['professional_qualification_Degree_Diploma'] or None
        # candidate_profile.professional_qualification_subjects = request.POST['professional_qualification_subjects'] or None
        candidate_profile.professional_qualification_name_location = request.POST['professional_qualification_name_location'] or None
        candidate_profile.professional_qualification_marks_obtained = request.POST['professional_qualification_marks_obtained'] or None
        candidate_profile.professional_qualification_passing_year = request.POST['professional_qualification_passing_year'] or None
        candidate_profile.others_qualification_Degree_Diploma = request.POST['others_qualification_Degree_Diploma'] or None
        # candidate_profile.others_qualification_subjects = request.POST['others_qualification_subjects'] or None
        candidate_profile.others_qualification_name_location = request.POST['others_qualification_name_location'] or None
        candidate_profile.others_qualification_marks_obtained = request.POST['others_qualification_marks_obtained'] or None
        candidate_profile.others_qualification_passing_year = request.POST['others_qualification_passing_year'] or None
        candidate_profile.training_workshop_title = request.POST['training_workshop_title'] or None
        candidate_profile.training_workshop_Institution_location = request.POST['training_workshop_Institution_location'] or None
        candidate_profile.training_workshop_skill = request.POST['training_workshop_skill'] or None
        candidate_profile.training_workshop_duration = request.POST['training_workshop_duration'] or None
        candidate_profile.training_workshop_start_date = request.POST['training_workshop_start_date'] or None
        candidate_profile.current_emp_start_date = request.POST['current_emp_start_date'] or None
        candidate_profile.current_employer = request.POST['current_employer'] or None
        candidate_profile.current_emp_salary = request.POST['current_emp_salary'] or None
        candidate_profile.current_emp_benefits = request.POST['current_emp_benefits'] or None
        candidate_profile.current_emp_position = request.POST['current_emp_position'] or None
        candidate_profile.current_emp_reason_for_leaving = request.POST['current_emp_reason_for_leaving'] or None
        candidate_profile.expected_salary = request.POST['expected_salary'] or None
        candidate_profile.current_emp_job_description = request.POST['current_emp_job_description'] or None
        candidate_profile.current_emp_supervisor_name = request.POST['current_emp_supervisor_name'] or None
        candidate_profile.father_name = request.POST['father_name'] or None
        candidate_profile.father_dob = request.POST['father_dob'] or None
        candidate_profile.father_profession = request.POST['father_profession'] or None
        candidate_profile.mother_name = request.POST['mother_name'] or None
        candidate_profile.mother_dob = request.POST['mother_dob'] or None
        candidate_profile.mother_profession = request.POST['mother_profession'] or None
        candidate_profile.spouse_name = request.POST['spouse_name'] or None
        candidate_profile.spouse_dob = request.POST['spouse_dob'] or None
        candidate_profile.spouse_profession = request.POST['spouse_profession'] or None
        candidate_profile.Children_name_1 = request.POST['Children_name_1'] or None
        candidate_profile.Children_name_2 = request.POST['Children_name_2'] or None
        candidate_profile.Children_dob_1 = request.POST['Children_dob_1'] or None
        candidate_profile.Children_dob_2 = request.POST['Children_dob_2'] or None
        candidate_profile.Children_1_profession = request.POST['Children_1_profession'] or None
        candidate_profile.Children_2_profession = request.POST['Children_2_profession'] or None
        candidate_profile.reason_to_apply_sonata = request.POST['reason_to_apply_sonata'] or None
        candidate_profile.willing_to_relocate = request.POST['willing_to_relocate'] or None
        candidate_profile.interviewed_by_Sonata_before = request.POST['interviewed_by_Sonata_before'] or None
        candidate_profile.locational_preferences = request.POST['locational_preferences'] or None
        candidate_profile.status = 1
        print("lfsdlkfjsdlkfj----------")
        # application.application_status=2
        candidate_profile.save()
        # application.save()
        
        try:
            resume_obj = ResumeFiles.objects.get(candidate_id = candidate_profile.id)
        except Exception as e:
            print(e)
            resume_obj = ResumeFiles()
            resume_obj.candidate_id = candidate_profile.id
        if 'resume_file' in request.FILES:
            #storing mime of th file in resume_repository
            file_name = request.FILES['resume_file'].name
            file_extension = os.path.splitext(file_name)[1]
            if file_extension.lower() == '.pdf':
                resume_obj.mime_type = 'application/pdf'
            elif file_extension.lower() in ['.jpg', '.jpeg', '.png']:
                resume_obj.mime_type = 'image/'+file_extension.lower()[1:]
            else:
                resume_obj.mime_type = 'unknown'
            resume_obj.resume = request.FILES['resume_file'].read()
            resume_obj.save()
        
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = candidate_profile.id)
        except Exception as e:
            print(e)
            document_obj = Document_Candidate()
            document_obj.candidate_id = candidate_profile.id
        
        if 'aadhar_doc' in request.FILES:
            document_obj.aadhar_doc = request.FILES['aadhar_doc']
            print( 'aadhar',document_obj.aadhar_doc)
            document_obj.save()
        
        if 'pan_doc' in request.FILES:
            document_obj.pan_doc = request.FILES['pan_doc']
            print( 'pan_doc',document_obj.pan_doc)
            document_obj.save()
        if 'dl_doc' in request.FILES:
            document_obj.dl_doc = request.FILES['dl_doc']
            print( 'dl_doc',document_obj.dl_doc)
            document_obj.save()
        if 'ssc_doc' in request.FILES:
            document_obj.ssc_doc = request.FILES['ssc_doc']
            print( 'ssc_doc',document_obj.ssc_doc)
            document_obj.save()
        if 'hsc_doc' in request.FILES:
            document_obj.hsc_doc = request.FILES['hsc_doc']
            print( 'hsc_doc',document_obj.hsc_doc)
            document_obj.save()
        if 'graduate_doc' in request.FILES:
            document_obj.graduate_doc = request.FILES['graduate_doc']
            print( 'graduate_doc',document_obj.graduate_doc)
            document_obj.save()

        messages.success(request,'Successfully Updated')
        redirect_url = reverse('view_candidate_profile', args=[candidate_profile.email])
        print(redirect_url)
        return redirect(redirect_url)
        # # except Exception as e:
        #     print(e)
        #     print("form not valid")
        #     messages.error(request, 'Something went wrong. Please try again.')           
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    context = {'candidate_profile':candidate_profile,
               'user_profile':model_to_dict(candidate_profile),
               'gender_choices': GENDER,
               'status':candidate_profile.status,
               'binary_data':encoded_data,
               'mime_type':mime_type,
               'gender_choices': GENDER,
               'document_obj':document_obj,
               'ssc_doc': ssc_doc,
               'hsc_doc': hsc_doc,
               'graduate_doc': graduate_doc,
               'aadhar_doc' : aadhar_doc,
               'pan_doc' : pan_doc,
               'dl_doc' : dl_doc,
               'is_hr':is_hr ,'is_hrhead':is_hrhead,
               }
    return render(request, 'edit_profile.html', context) 

def all_user_list(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    if request.method == "POST":
        roll_id = request.POST.get('roll_id',None)
        if roll_id != 'all':
            user_rolls = User_Rolls.objects.filter(roll_id=roll_id).values('user_id')
            userlist = User.objects.filter(id__in=user_rolls)
            return render(request,'all_user_list.html',{'userlist':userlist,"roll_id":roll_id})
               
    userlist = User.objects.all()
    return render(request,'all_user_list.html',{'userlist':userlist,'is_hr':is_hr ,'is_hrhead':is_hrhead})


def roll_assign(request):
    if request.method == "POST":
        user_id= request.POST.get('userid')
        role_id = request.POST.get('role_id')
        print(user_id)
        print(role_id)
        user_role_instance = User_Rolls.objects.filter(user_id = user_id).first()
        user_role_instance.roll_id = role_id 
        user_role_instance.save()
        
        u = User.objects.filter(id = user_role_instance.user_id).values('email')
        candidate = candidate_details.objects.filter(email__in = u)
        candidate.delete()
        
    return redirect("all_user_list")
         
# @login_required(login_url='signIn')
def applied_user_details(request):
    # userroll = User_Rolls.objects.filter(roll_id=0).values('user_id')
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    applicants = candidate_details.objects.filter(status=0, is_user=False, reviewed_by__isnull=True)
    
    print(applicants)
    return render(request, 'appliedUserDetails.html',{'applicants':applicants,'is_hr':is_hr ,'is_hrhead':is_hrhead})

@login_required(login_url='signIn')
def schedule_online_test(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    query = f"""SELECT cd.name,
                        cd.email, 
                        cd.mobile_no,
                        cd.id as candidate_id, 
                        ad.application_id,
                        ad.position_shortlisted_for,
                        ad.branch_shortlisted_for 
            FROM application_details ad 
            LEFT JOIN candidate_details cd ON ad.candidate_id = cd.id 
            WHERE ad.application_status = 5 or ad.application_status = 6"""
    # or ad.application_status = 4
    
    df = pd.read_sql(query, engine)

    print(df, "data")	
    applicants = candidate_details.objects.filter()
    distinct_positions_queryset = applicants.values_list("position_applied_for", flat=True).distinct()
    distinct_positions = [position for position in distinct_positions_queryset if position is not None]
    print(distinct_positions)

    print(applicants)
    data = df.to_dict('records')
    
    query = f"""SELECT cd.name,
                        cd.email, 
                        cd.mobile_no,
                        cd.id as candidate_id, 
                        ad.application_id,
                        ad.position_shortlisted_for,
                        ad.branch_shortlisted_for 
            FROM application_details ad 
            LEFT JOIN candidate_details cd ON ad.candidate_id = cd.id 
            WHERE ad.application_status = 2"""
                
    df2 = pd.read_sql(query, engine)
    
    print(df2, "data2")	
    candidate = candidate_details.objects.filter()
    distinct_positions_queryset = candidate.values_list("position_applied_for", flat=True).distinct()
    distinct_positions = [position for position in distinct_positions_queryset if position is not None]
    print(distinct_positions)

    print(applicants)
    data2 = df2.to_dict('records')

    
    query = f"""SELECT cd.name,
                        cd.email, 
                        cd.mobile_no,
                        cd.id as candidate_id, 
                        ad.application_id,
                        ad.position_shortlisted_for,
                        ad.branch_shortlisted_for 
            FROM application_details ad 
            LEFT JOIN candidate_details cd ON ad.candidate_id = cd.id 
            WHERE ad.application_status = 3"""
                
    df1 = pd.read_sql(query, engine)
    
    print(df1, "data1")	
    candidate = candidate_details.objects.filter()
    distinct_positions_queryset = candidate.values_list("position_applied_for", flat=True).distinct()
    distinct_positions = [position for position in distinct_positions_queryset if position is not None]
    print(distinct_positions)

    print(applicants)
    data1 = df1.to_dict('records')

    return render(request, 'schedule_test_userdetails.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'applicants':data, 'distinct_positions':distinct_positions,'applicants1':data1, 'applicants2':data2,})

@csrf_exempt
def api_exam_filter(request):
    if request.method == 'POST':
        selected_position = request.POST.get('position', None)
        selected_branch = request.POST.get('branch', None)

        applicants = User_Details.objects.filter(status=2)

        if selected_position and selected_position != "None":
            applicants = applicants.filter(position_shortlisted_for=selected_position)

        if selected_branch and selected_branch != "None":
            applicants = applicants.filter(branch_shortlisted_for=selected_branch)

        applicants = applicants.order_by('-id').values(
            'id', 'name', 'email', 'mobile_no'
        )

        data = list(applicants)

        return JsonResponse(data, safe=False)
    
def get_branch_exam_options(request):
    if request.method == 'GET':
        selected_position = request.GET.get('position', None)
        if selected_position is None:
            # Handle the case when no position is selected
            return JsonResponse({'branch_options': []})
        else:
            # Fetch branch options based on the selected position
            branch_options = User_Details.objects.filter(position_shortlisted_for=selected_position, status=2).values_list('branch_shortlisted_for', flat=True).distinct()
            print(branch_options)
            return JsonResponse({'branch_options': list(branch_options)})

@login_required(login_url='signIn')
def sceduled_user_details(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    query = f"""SELECT cd.name, cd.email, cd.mobile_no, cd.id as candidate_id, ad.application_id as id, ad.position_shortlisted_for FROM application_details ad 
                LEFT JOIN candidate_details cd 
                ON ad.candidate_id = cd.id 
                WHERE ad.application_status = 4 """
    
    applicants = pd.read_sql(query, engine)
    
    print(applicants)
    distinct_positions_queryset = applicants[['position_shortlisted_for']].drop_duplicates(keep='first')
    distinct_positions_queryset.dropna(inplace=True)
    distinct_positions = distinct_positions_queryset['position_shortlisted_for'].tolist()
    print(distinct_positions)
    applicants=applicants.to_dict('records')
    
    
    query = f"""SELECT cd.name, cd.email, cd.mobile_no, cd.id as candidate_id, ad.application_id as id, ad.position_shortlisted_for FROM application_details ad 
            LEFT JOIN candidate_details cd 
            ON ad.candidate_id = cd.id 
            WHERE ad.application_status = 5"""
    
    applicants1 = pd.read_sql(query, engine)
    
    print(applicants)
    distinct_positions_queryset = applicants1[['position_shortlisted_for']].drop_duplicates(keep='first')
    distinct_positions_queryset.dropna(inplace=True)
    distinct_positions1 = distinct_positions_queryset['position_shortlisted_for'].tolist()
    print(distinct_positions1)
    applicants1=applicants1.to_dict('records')
    
    return render(request, 'sceduledUserDetails.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'applicants':applicants,'distinct_positions':distinct_positions,'distinct_positions1':distinct_positions1,'applicants1':applicants1 })

@csrf_exempt
def api_interview_filter(request):
    if request.method == 'POST':
        selected_position = request.POST.get('position', None)
        selected_branch = request.POST.get('branch', None)

        applicants = User_Details.objects.filter(status=4)

        if selected_position and selected_position != "None":
            applicants = applicants.filter(position_shortlisted_for=selected_position)

        if selected_branch and selected_branch != "None":
            applicants = applicants.filter(branch_shortlisted_for=selected_branch)

        applicants = applicants.order_by('-id').values(
            'id', 'name', 'email', 'mobile_no'
        )

        data = list(applicants)

        return JsonResponse(data, safe=False)
    
def get_branch_interview_options(request):
    if request.method == 'GET':
        selected_position = request.GET.get('position', None)
        if selected_position is None:
            # Handle the case when no position is selected
            return JsonResponse({'branch_options': []})
        else:
            # Fetch branch options based on the selected position
            branch_options = User_Details.objects.filter(position_shortlisted_for=selected_position, status=4).values_list('branch_shortlisted_for', flat=True).distinct()
            print(branch_options)
            return JsonResponse({'branch_options': list(branch_options)})

@login_required(login_url='signIn')
def hold_user_details(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
        query = """
        SELECT 
            cd.name, 
            cd.email, 
            cd.mobile_no, 
            cd.id as candidate_id, 
            ad.application_id,
            ad.position_shortlisted_for,
            ad.branch_shortlisted_for
            
        FROM application_details ad 
        LEFT JOIN candidate_details cd ON ad.candidate_id = cd.id 
        WHERE ad.application_status = 11
    """
    
        df = pd.read_sql(query, engine)
        print(df, "data")

        data_list = df.to_dict(orient='records')
        print(data_list)

        applicants = ApplicationDetails.objects.filter(application_status=11)
        candidate = candidate_details.objects.all()  
        distinct_positions_queryset = applicants.values_list("position_shortlisted_for", flat=True).distinct()
        distinct_positions = [position for position in distinct_positions_queryset if position is not None]
        print(distinct_positions)
        context = {
            'applicants': applicants,
            'candidates': candidate,
            'distinct_positions': distinct_positions,
            'data_list': data_list,
            'is_hr':is_hr ,'is_hrhead':is_hrhead,
        }
        return render(request, 'holdUserDetails.html', context)
        
@csrf_exempt
def api_hold_filter(request):
    if request.method == 'POST':
        selected_position = request.POST.get('position', None)
        selected_branch = request.POST.get('branch', None)

        applicants = ApplicationDetails.objects.filter(status=11)

        if selected_position and selected_position != "None":
            applicants = applicants.filter(position_shortlisted_for=selected_position)

        if selected_branch and selected_branch != "None":
            applicants = applicants.filter(branch_shortlisted_for=selected_branch)

        applicants = applicants.order_by('-id').values(
            'id', 'name', 'email', 'mobile_no', 'position_shortlisted_for', 'branch_shortlisted_for'
        )

        data = list(applicants)

        return JsonResponse(data, safe=False)
    
def get_branch_hold_options(request):
    if request.method == 'GET':
        selected_position = request.GET.get('position', None)
        if selected_position is None:
            # Handle the case when no position is selected
            return JsonResponse({'branch_options': []})
        else:
            # Fetch branch options based on the selected position
            branch_options = User_Details.objects.filter(position_shortlisted_for=selected_position, status=12).values_list('branch_shortlisted_for', flat=True).distinct()
            print(branch_options)
            return JsonResponse({'branch_options': list(branch_options)})

@login_required(login_url='signIn')
def rejected_user_details(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    user_id=request.user.id
    alloted_applicants_ids = rejected_review_allotment.objects.filter(hr_id=user_id).values_list('candidate_id', flat=True)

    if alloted_applicants_ids.exists():
        
        applicants = User_Details.objects.all().filter(status=11).exclude(id__in = alloted_applicants_ids)
        distinct_positions_queryset = applicants.values_list("position_shortlisted_for", flat=True).distinct()
        distinct_positions = [position for position in distinct_positions_queryset if position is not None]
        print(distinct_positions)
    
 
    return render(request, 'rejectedUserDetails.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'applicants':applicants, 'distinct_positions':distinct_positions})



def api_rejected_filter(request):
    if request.method == 'POST':
        selected_position = request.POST.get('position', None)
        selected_branch = request.POST.get('branch', None)
        user_id=request.user.id
        alloted_applicants_ids = rejected_review_allotment.objects.filter(hr_id=user_id).values_list('candidate_id', flat=True)

        if alloted_applicants_ids.exists():
            applicants = User_Details.objects.filter(status=11).exclude(id__in = alloted_applicants_ids)

            if selected_position and selected_position != "None":
                applicants = applicants.filter(position_shortlisted_for=selected_position)

            if selected_branch and selected_branch != "None":
                applicants = applicants.filter(branch_shortlisted_for=selected_branch)

            applicants = applicants.order_by('-id').values(
                'id', 'name', 'email', 'mobile_no', 'position_shortlisted_for', 'branch_shortlisted_for'
            )

            data = list(applicants)

            return JsonResponse(data, safe=False)
    
def get_branch_rejected_options(request):
    if request.method == 'GET':
        selected_position = request.GET.get('position', None)
        if selected_position is None:
            # Handle the case when no position is selected
            return JsonResponse({'branch_options': []})
        else:
            # Fetch branch options based on the selected position
            user_id=request.user.id
            alloted_applicants_ids = rejected_review_allotment.objects.filter(hr_id=user_id).values_list('candidate_id', flat=True)

            if alloted_applicants_ids.exists():
                
                applicants = User_Details.objects.all().filter(status=11).exclude(id__in = alloted_applicants_ids)
                branch_options = applicants.filter(position_shortlisted_for=selected_position, status=11).values_list('branch_shortlisted_for', flat=True).distinct()
                print(branch_options)
                return JsonResponse({'branch_options': list(branch_options)})

from django.template.defaultfilters import date
from django.urls import reverse


def validate_inputs(data):
    status=True
    if data is None:
        status=False
    if data == '':
        status=False
    return status

@transaction.atomic
def scedule_interview(request,refId):
    
    try:
        application = ApplicationDetails.objects.get(pk=refId)
    except ApplicationDetails.DoesNotExist:
        messages.error(request, 'Application not found.')
        # return redirect('sceduled_user_details')  # You might need to adjust this URL name
        return redirect ('schedule_online_test')
        
    if request.method == 'POST':
        interview_panel_list = request.POST.get('interview_panel', None)
        interview_date = request.POST.get('interview_date', None)
        interview_time = request.POST.get('interview_time', None)

        interviews = InterviewDetails.objects.filter(interview_date=interview_date, panel_list=interview_panel_list).distinct().values_list("vacancy_id", flat=True)
        vc = VacancyDetails.objects.filter(vacancy_id__in=interviews, branch=application.branch_shortlisted_for, role=application.position_shortlisted_for).first()
        interview = InterviewDetails.objects.filter(vacancy_id=vc.vacancy_id).first() if vc else None

        if interview:
            application.vacancy_id = interview.interview_id
            print("Interview ID:", interview.interview_id)
            application.interview_id = interview.interview_id  

        application.application_status = 5  # Assuming 5 is the correct status
        application.interview_time = interview_time

        data = [interview_panel_list, interview_date, interview_time]
        is_valid = all(validate_inputs(i) for i in data)

        if is_valid:
            application.save()
            profile = candidate_details.objects.get(id=application.candidate_id)
            print("Candidate ID:", profile.id)
            url = f"https://media.smsgupshup.com/GatewayAPI/rest?userid=YOUR_USERID&password=YOUR_PASSWORD&send_to={profile.mobile_no}&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=Hello+{profile.name}%2C%0ACongratulations%21+Your+job+application+for+the+position+of+{application.position_shortlisted_for}+at+our+{application.branch_shortlisted_for}+branch+has+been+shortlisted+for+interview.%0AInterview+Details+%3A-%0ADate+%3A+{interview.interview_date}%0ATime+%3A+{application.interview_time}%0ALocation+%3A+{interview.interview_place}%0AWe+look+forward+to+your+presence.&isTemplate=true&header=Greetings+From+Sonata%21"
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            print(response.text)
            # return redirect('sceduled_user_details')  # You might need to adjust this URL name
            return redirect('schedule_online_test')
        else:
            messages.error(request, 'Please fill all the fields')
            return redirect('schedule_test_user_full_details', refId=refId)
            # return redirect('sceduled_user_full_details', refId=refId)  # You might need to adjust this URL name

def validate_inputs(input_value):
    return input_value is not None and input_value != ''

import base64

def encode_id(id_num):
    id_str = str(id_num)
    encoded_bytes = base64.b64encode(id_str.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8')
    return encoded_str

import binascii


def decode_id(encoded_str):
    try:
        # Add padding if missing
        while len(encoded_str) % 4 != 0:
            encoded_str += '='

        decoded_bytes = base64.b64decode(encoded_str.encode('utf-8'))
        decoded_str = decoded_bytes.decode('utf-8')
        return int(decoded_str)
    except (ValueError, UnicodeDecodeError, binascii.Error) as e:
        # Handle decoding errors (e.g., invalid Base64 or non-integer data)
        print('Error:', e)
        return None

@transaction.atomic
@login_required(login_url='signIn')
def schedule_test(request,refId):
    if request.method == 'POST':
        application_id=refId
        sheet_id=request.POST.get('exam_sheets',None)
        sheet_id=int(sheet_id) if sheet_id else None
        exam_date=request.POST.get('exam_date',None)
        exam_date=exam_date if exam_date != ''  else None
        is_online=True if request.POST['exam_mode']=='online' else False
        try:
            application = ApplicationDetails.objects.get(application_id=refId)
            # test_scedule=TestSchedule.objects.create(candidate_id=candidate_id,sheet_id=sheet_id,exam_date=exam_date,is_online=is_online,status='0')
            test_scedule=TestScheduleDetails.objects.create(application_id=application_id,sheet_id=sheet_id,test_date=exam_date,test_status='0',is_online=is_online,candidate_id=application.candidate_id)

            application.application_status = 3
            application.save()
            # print('mobile no', profile.mobile_no)
            test_scedule.save()
            
            # for creating the id of candidate
            doc = Document_Candidate()
            doc.candidate_id = application.candidate_id
            doc.save()
            # encoded_id = base64.urlsafe_b64encode(str(test_scedule.id).encode('utf-8')).decode('utf-8')
            encoded_id = encode_id(test_scedule.test_id)
            print(encoded_id)
            profile = candidate_details.objects.get(id=application.candidate_id)
            # url = f"https://media.smsgupshup.com/GatewayAPI/rest?userid=2000209909&password=z24gzBUA&send_to={profile.mobile_no}&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=Your+online+exam+has+been+scheduled+on+2023-07-04.%0APlease+click+on+the+below+link+to+access+your+exam+on+the+scheduled+date+and+time.&isTemplate=true&header=Greetings+From+Sonata&buttonUrlParam={encoded_id}"
            url = f"https://media.smsgupshup.com/GatewayAPI/rest?userid=2000209909&password=z24gzBUA&send_to={profile.mobile_no}&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=Your+online+exam+has+been+scheduled+on+{test_scedule.test_date}.%0APlease+click+on+the+below+link+to+access+your+exam+on+the+scheduled+date+and+time.&isTemplate=true&header=Greetings+From+Sonata&buttonUrlParam={encoded_id}"
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            messages.success(request,"Test Scheduled Successfully")
            # print(response.text)
        except Exception as e:
            print(e)
            print('error--------------------***')
            messages.error(request,"Something Went Wrong")
    return redirect('schedule_online_test')
        
def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

from datetime import date as date


@csrf_exempt
def exam(request,slug):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    context={}
    print('slug: ', slug)
    refId=decode_id(slug)
    context['refId']=refId
    context['slug']=slug
    print('refff id: ', refId)
    if request.method=='POST':
        if 'step1' in request.POST:
            print('stepppp one')
            # testschedule_obj=TestSchedule.objects.get(id=refId)
            testschedule_obj=TestScheduleDetails.objects.get(test_id=int(refId))
            print(testschedule_obj)
            if testschedule_obj.test_status != '1':
                testschedule_obj.test_status='1'

                aadharno=request.POST['aadharno']
                print(aadharno)
                # # identity_Aadhar=1
                # # aadarno=1
                # user_profile = User_Details.objects.get(id=testschedule_obj.candidate_id)
                # user_profile = candidate_details.objects.get(id=testschedule_obj.candidate_id)
                # print(user_profile)
                # identity_Aadhar=str(user_profile.identity_Aadhar)
                # print(identity_Aadhar)
                # aadharno=str(aadharno)
                # print(aadharno)
                # a=identity_Aadhar.find(aadarno)
                # if int(user_profile.identity_Aadhar) == int(aadarno):
                otp = request.session.get('otp')
                if str(otp) == str(aadharno):
                    testschedule_obj.save()
                    print("Status Changed"*10)
                    context['success']='success'
                    context['status']='success'
                    return JsonResponse(context)
                else:
                    context['status']='fail_1'
                    return JsonResponse(context)
                # testschedule_obj.save()

            if testschedule_obj.status=='1':
                context['tbl_id']=refId
                return render(request,'online_exam_details.html',context)
        if 'step2' in request.POST:
            print('steppp twoo')
            if 'step3' in request.POST:
                print('steppp 3')
       
                # d1=request.POST['d']
                print("list dataaaaaaaaaa")
                # print(d1)
                # print(type(d1))
                return True
            else:
                print("not step 3, just 2")
                
                # testschedule_obj=TestSchedule.objects.get(id=refId)
                testschedule_obj=TestScheduleDetails.objects.get(test_id=refId)
                if testschedule_obj.test_status != '2':
                    testschedule_obj.test_status='2'
                    current_time=datetime.now()
                    next_time = current_time + timedelta(minutes=45)
                    # end_time = next_time.strftime("%H:%M")
                    testschedule_obj.start_time=current_time.strftime("%H:%M:%S")
                    testschedule_obj.end_time=next_time.strftime("%H:%M")
                    testschedule_obj.save()
                    print("Status Changed",type(current_time.strftime("%H:%M:%S")),type(next_time.strftime("%H:%M")))
                if testschedule_obj.test_status == '2':
                    sheet_id=testschedule_obj.sheet_id
                    print(sheet_id,"sheet_id")
                    question=question_sheet.objects.filter(sheet_id=sheet_id)
                    # testschedule_obj=TestSchedule.objects.get(id=refId)
                    testschedule_obj=TestScheduleDetails.objects.get(test_id=refId)
                    # print(question.values())
                    context['question']=question
                    context['start_time']=testschedule_obj.start_time
                    context['end_time']=testschedule_obj.end_time
                    today=datetime.now().date()
                    print(testschedule_obj.start_time, testschedule_obj.end_time)
                    time_2=datetime.combine(today, testschedule_obj.end_time)
                    context['end_time']=time_2.strftime("%Y-%m-%d %H:%M:%S")
                    
                    
                    question_id_list=[]
                    for i in question:
                        question_id_list.append(i.question_id)
                    context['question_id_list']=question_id_list
                    context['cand_id'] = testschedule_obj.candidate_id
                    context['application_id'] = testschedule_obj.application_id


                    # Convert the start_time and end_time values to datetime.time objects
                    start_time_obj = datetime.strptime(str(testschedule_obj.start_time), '%H:%M:%S').time()
                    end_time_obj = datetime.strptime(str(testschedule_obj.end_time), '%H:%M:%S').time()
                    context['time_in_secs'] = calculate_time_difference(start_time_obj,end_time_obj)      
                    print(question_id_list)
                    # livefe(request)
                    context['is_hr'] = is_hr
                    context['is_hrhead'] = is_hrhead
                    return render(request,'question_sheet.html',context)
        if 'final_step' in request.POST:
            print('final step')
            question_id_list=request.POST['question_id_list']
            fetchdata=request.POST['fetchdata']
            d=request.POST['d']
            d=json.loads(d)
            print("DATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            print(question_id_list)
            # print()
            print(fetchdata,d)
            l1=[]
            l2=[]
            for i in d:
                if i!= 'submit':
                    l1.append(i)
                    l2.append(d[i])
            print(l1,l2)
            data={'question_id':l1,"answer":l2}
            print(type(d))
            data=pd.DataFrame.from_dict(data)
            print(data)
            data['test_id']=refId
            data['response_date']=datetime.now()
            data.reindex(columns=[['test_id','response_date','question_id','answer']])
            print(data)
            user1 = "SFPL_Connect"
            password = "$%n5bF33%X"
            db = "Sonata_ConnectHR"
            server = "172.17.130.216"
            engine = create_engine(f"mssql+pyodbc://{user1}:{password}@{server}/{db}?driver=ODBC+Driver+17+for+SQL+Server")
            # data.to_sql('Accounts_testresponse',con=engine, if_exists='append',index=False)
            data.to_sql('test_response',con=engine, if_exists='append',index=False)
            # testschedule_obj=TestSchedule.objects.get(id=refId)
            print('??????', refId)
            testschedule_obj=TestScheduleDetails.objects.get(test_id=refId)
            testschedule_obj.test_status='3'
            testschedule_obj.test_score=calculate_test_score(testschedule_obj.test_id)
            # testschedule_obj.test_score=10
            total = total_marks(testschedule_obj.test_id)
            percentage = float((testschedule_obj.test_score/total)*100)
            testschedule_obj.save()
            # user_details_obj=User_Details.objects.get(id=testschedule_obj.candidate_id)
            application = ApplicationDetails.objects.get(application_id=testschedule_obj.application_id)
            # user_profile = candidate_details.objects.get(id=application.candidate_id)
            # candidate_details_obj_1=ApplicationDetails.objects.get(candidate_id=application.candidate_id)
            application.application_status=4
            # user_details_obj.s
            application.save()
            user_details_obj=candidate_details.objects.get(id=application.candidate_id)

            context['status']='success'
            context['okk']="oooooookkkkkkkkkkkkkk"
            print(context['okk'])
            message=f""" 
                Dear User Your Exam is Submitted."""
        
            context['message']=message

            url = f"https://media.smsgupshup.com/GatewayAPI/rest?userid=2000209909&password=z24gzBUA&send_to={user_details_obj.mobile_no}&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=Your+test+score+has+been+evaluated.%0Ayou+have+scored+{testschedule_obj.test_score}+out+of+{total}+and+have+obtained+{percentage}%25.%0AFor+further+detailed+assessment+log+in+to+HRMS+portal+or+check+status+by+reference+ID.&isTemplate=true&header=Greetings+From+Sonata%21"
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            print(response.text)

            url = f"https://media.smsgupshup.com/GatewayAPI/rest?userid=2000209909&password=z24gzBUA&send_to=9682347116&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=Your+test+score+has+been+evaluated.%0Ayou+have+scored+{testschedule_obj.test_score}+out+of+{total}+and+have+obtained+{percentage}%25.%0AFor+further+detailed+assessment+log+in+to+HRMS+portal+or+check+status+by+reference+ID.&isTemplate=true&header=Greetings+From+Sonata%21"
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            print(response.text)

            # return render(request,'show_message_exam.html',context)
            return JsonResponse(context)

    else:
        print('get')
        try:
            # testschedule_obj=TestSchedule.objects.get(id=refId)
            testschedule_obj=TestScheduleDetails.objects.get(test_id=int(refId))
        except:
            refId=str(refId)
            # testschedule_obj=TestSchedule.objects.get(id=refId)
            testschedule_obj=TestScheduleDetails.objects.get(test_id=refId)
        # .values().first()
        print(type(testschedule_obj.test_status))
        if testschedule_obj.test_status == '0':

            print("(((((99999)))))")
            print(testschedule_obj)
            # today_date=date.today()
            today_date = date.today()
            # today_date=datetime.now()
            if testschedule_obj.test_date == today_date:
                print("today exam")
                # user_profile = User_Details.objects.get(id=testschedule_obj.candidate_id)
                application = ApplicationDetails.objects.get(application_id=testschedule_obj.application_id)
                print(application)
                user_profile = candidate_details.objects.get(id=application.candidate_id)
                print(user_profile)
                encoded_id = encode_id(testschedule_obj.test_id)
                otp = generateOTP()
                request.session['otp'] = otp
                url = f"https://media.smsgupshup.com/GatewayAPI/rest?userid=2000209909&password=z24gzBUA&send_to={user_profile.mobile_no}&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=Dear+{user_profile.name}%2C+Start+your+Exam+using%3A+{otp}&isTemplate=true&header=Greeting+from+Sonata+Finanace"

                payload = {}
                headers = {}

                response = requests.request("GET", url, headers=headers, data=payload)

                print(response.text)
                print(otp)
                messages.success(request,"Message Send Successfully")
                context['user_profile']=user_profile
                # context['refId']=refId
                context['table_id']=testschedule_obj.test_id
                return render(request,"exam_student_details.html",context)
            elif testschedule_obj.test_date < today_date:
                # messages.error(request, f"Your Exam Date is ENDED , Your Exam Date is :- {testschedule_obj.exam_date}")
                print("exam date is passed")
                message=f"""Your Exam Date is ENDED , Your Exam Date is :- {testschedule_obj.test_date} """
                context['message']=message
                context['red']="red"
                print(context)
                return render(request,'show_message_exam.html',context)
            elif testschedule_obj.test_date > today_date:
                print("time left to start exam")
                today_date_1=datetime.now()
                exam_date_time = str(testschedule_obj.test_date) + " " + "00:00:00"
                start=today_date_1
                ends = datetime.strptime(exam_date_time, '%Y-%m-%d %H:%M:%S')
                time_left=ends-start
                message=f""" 
                Your Exam Time Not Now, You have some Time left to start the exam. After- '{time_left}'  you can start your Exam."""

                context['message']=message
                context['green']="green"
                return render(request,'show_message_exam.html',context)
            else:
                print("exam else section")
                message=f""" 
                There is Some Techinical Error related to Exam please check after some time."""
        
                context['message']=message
                return render(request,'show_message_exam.html',context)

    
        elif testschedule_obj.test_status == '1':
            context['tbl_id']=refId
            today_date = date.today()
            if testschedule_obj.test_date == today_date:
                return render(request,'online_exam_details.html',context)
            elif testschedule_obj.test_date < today_date:
                # messages.error(request, f"Your Exam Date is ENDED , Your Exam Date is :- {testschedule_obj.exam_date}")
                print("exam date is passed")
                message=f"""Your Exam Date is ENDED , Your Exam Date is :- {testschedule_obj.test_date} """
                context['message']=message
                context['red']="red"
                print(context)
                return render(request,'show_message_exam.html',context)
            elif testschedule_obj.test_date > today_date:
                print("time left to start exam")
                today_date_1=datetime.now()
                exam_date_time = str(testschedule_obj.test_date) + " " + "00:00:00"
                start=today_date_1
                ends = datetime.strptime(exam_date_time, '%Y-%m-%d %H:%M:%S')
                time_left=ends-start
                message=f""" 
                Your Exam Time Not Now, You have some Time left to start the exam. After- '{time_left}'  you can start your Exam."""

                context['message']=message
                context['green']="green"
                return render(request,'show_message_exam.html',context)
            else:
                print("exam else section")
                message=f""" 
                There is Some Techinical Error related to Exam please check after some time."""
        
                context['message']=message
                return render(request,'show_message_exam.html',context)
            # return HttpResponse(f"<h3> not a valid user-{testschedule_obj.status}</h3>")
        elif testschedule_obj.test_status == '2':
            today_date=date.today()
            if testschedule_obj.test_date == today_date:
                sheet_id=testschedule_obj.sheet_id
                print(sheet_id,"sheet_id")
                question=question_sheet.objects.filter(sheet_id=sheet_id)
                # print(question.values())
                context['question']=question
                context['start_time']=testschedule_obj.start_time
                # context['end_time']=testschedule_obj.end_time
                today=datetime.now().date()
                time_2=datetime.combine(today, testschedule_obj.end_time)
                context['end_time']=time_2.strftime("%Y-%m-%d %H:%M:%S")
                question_id_list=[]
                for i in question:
                    question_id_list.append(i.question_id)
                context['question_id_list']=question_id_list
                print(question_id_list)
                context['cand_id'] = testschedule_obj.candidate_id
                context['application_id'] = testschedule_obj.application_id
                # Convert the start_time and end_time values to datetime.time objects
                start_time_obj = datetime.strptime(str(testschedule_obj.start_time), '%H:%M:%S').time()
                end_time_obj = datetime.strptime(str(testschedule_obj.end_time), '%H:%M:%S').time()
                context['time_in_secs'] = calculate_time_difference(start_time_obj,end_time_obj)
                # livefe(request)
                return render(request,'question_sheet.html',context)
            elif testschedule_obj.test_date < today_date:
                # messages.error(request, f"Your Exam Date is ENDED , Your Exam Date is :- {testschedule_obj.exam_date}")
                print("exam date is passed")
                message=f"""Your Exam Date is ENDED , Your Exam Date is :- {testschedule_obj.exam_date} """
                context['message']=message
                context['red']="red"
                print(context)
                return render(request,' .html',context)
            elif testschedule_obj.test_date > today_date:
                print("time left to start exam")
                today_date_1=datetime.now()
                exam_date_time = str(testschedule_obj.test_date) + " " + "00:00:00"
                start=today_date_1
                ends = datetime.strptime(exam_date_time, '%Y-%m-%d %H:%M:%S')
                time_left=ends-start
                message=f""" 
                Your Exam Time Not Now, You have some Time left to start the exam. After- '{time_left}'  you can start your Exam."""
            else:
                message=f""" 
                There is Some Techinical Error related to Exam please check after some time."""
        
                context['message']=message
                return render(request,'show_message_exam.html',context)
        elif testschedule_obj.test_status == '3':
            message=f""" 
                Dear User Your Exam is Submitted"""
        
            context['message']=message
            return render(request,'show_message_exam.html',context)

def total_marks(test_schedule_id):
    # test_schedule = TestSchedule.objects.get(id=test_schedule_id)
    test_schedule = TestScheduleDetails.objects.get(test_id=test_schedule_id)

    # Retrieve the corresponding question sheet for the test schedule
    q_sheet = question_sheet.objects.filter(sheet_id=test_schedule.sheet_id)

    total_marks=0
    for q in q_sheet:
        total_marks += 1
    
    return total_marks

def apply_response(answer,a,b,c,d):
    if answer == 'a':
        return a
    elif answer == 'b':
        return b
    elif answer == 'c':
        return c
    elif answer == 'd':
        return d

def calculate_test_score(test_schedule_id):
    print('test calculation has been started')
    try:
        # Retrieve the test schedule for the given ID
        # test_schedule = TestSchedule.objects.get(id=test_schedule_id)
        test_schedule = TestScheduleDetails.objects.get(test_id=test_schedule_id)
        print('fetched test_schedule obj:-------- ', pd.DataFrame(TestScheduleDetails.objects.filter(test_id=test_schedule_id).values()))
        # Retrieve all test actual answers for the given test schedule ID
        answer_df = pd.DataFrame(question_sheet.objects.filter(sheet_id=test_schedule.sheet_id).values())
        print('answer provided in df format:-------- ', answer_df)
        # fetching answers and converting them to options
        answer_df['response'] = answer_df.apply(lambda x: apply_response(x['option_a'],x['option_b'],x['option_c'],x['option_d'],x['answer']), axis=1)
        print('responses column added:------ ', answer_df)
        # fetching provided answers
        response_df = pd.DataFrame(TestResponseDetails.objects.filter(test_id=test_schedule_id).values())
        print('responses:--------', response_df)
        # combining responses with actual answers, keeping the correct ones and dropping the incorrect ones
        new_df = pd.merge(answer_df,response_df,left_on=['question_id','answer'], right_on=['question_id','answer'], how='left')
        print('combined result card:------- ', new_df)
        new_df = (new_df[['question_id','response_id']])
        print('combined result card, limited cols:------- ', new_df)
        new_df['response_id'] = new_df['response_id'].notnull().astype(int)
        print('combined result card, limited cols and int converted:------ ', new_df)
        obtained_score = new_df['response_id'].sum()
        print('obtained_score------',obtained_score)
        total_score = len(new_df)
        print('total_score----',total_score)
        percent_score = obtained_score / total_score * 100
        print('percent_score----',percent_score)
        return obtained_score
        # # Calculate the score based on the question sheet and test responses
        # score = 0
        # for response in test_responses:
        #     question_id = response.question_id
        #     candidate_response = response.response
        #     for q in q_sheet:
        #         print(q)
        #         if q.question_id == question_id:
        #             correct_option = f"option_{q.answer}"
        #             if correct_option == 'option_a':
        #                 correct_answer = q.option_a
        #             elif correct_option == 'option_b':
        #                 correct_answer = q.option_b
        #             elif correct_option == 'option_c':
        #                 correct_answer = q.option_c
        #             elif correct_option == 'option_d':
        #                 correct_answer = q.option_d

        #     if candidate_response == correct_answer:
        #         score += 1
        #     print("score: ",score)
        # return score

    except Exception as e:
        print("Error: ",e)

from django.utils import timezone
from datetime import datetime, timedelta

def calculate_time_difference(start_time, end_time):
    # Get the current date and time
    current_datetime = timezone.now()

    # Combine the current date with the start and end time values
    start_datetime = timezone.make_aware(datetime.combine(current_datetime.date(), start_time))
    end_datetime = timezone.make_aware(datetime.combine(current_datetime.date(), end_time))

    # Calculate the time difference
    time_diff = end_datetime - start_datetime

    # Extract the time difference in seconds
    time_diff_seconds = int(time_diff.total_seconds())
    print("time_in_secs", int(time_diff_seconds))

    return time_diff_seconds

def show_exam_result(request,id,application_id):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    context={}
    # candidate_id=id
    user_profile = candidate_details.objects.get(id=id)
    context['profile'] = user_profile
    # test_schedule_id=2
    try:
        test_details=TestScheduleDetails.objects.get(candidate_id=user_profile.id, application_id = application_id)
        offline_answersheet = test_details.offline_answersheet
        mime_type = test_details.mime_type
        encoded_data = base64.b64encode(offline_answersheet).decode('utf-8')
    except Exception as e :
        print(e)
        encoded_data = None
        mime_type = None
    
    question=question_sheet.objects.filter(sheet_id=test_details.sheet_id)
    print(question)
 
    response=TestResponseDetails.objects.filter(test_id=test_details.test_id)
    print(response)
    
    context['score']=test_details.test_score
    context['question']= question
    context['responses']= response
    context['binary_data'] = encoded_data
    context['mime_type'] = mime_type
    context['is_online']=test_details.is_online
    context['is_hr'] = is_hr
    context['is_hrhead'] = is_hrhead
    return render(request,'show_exam_result.html',context)
    # return HttpResponse('exam')
    
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.core.files.storage import default_storage

def camshot_picture(request, id):
    # pictures = Candidate_Camshot.objects.all()
    # row = []
    # for picture in pictures:
    #     picture.camshot_base64 = base64.b64encode(picture.camshot).decode('utf-8')
    #     row.append(picture.camshot_base64)

    if request.method == 'POST':
        image = request.POST.get('src')
        image_bytes = base64.b64decode(image[22:])
        camshot_obj = Candidate_Camshot()
        camshot_obj.application_id = id
        camshot_obj.camshot = image_bytes
        camshot_obj.save()
        print("saved camshot")
        # print(image)
        # camshot = NamedTemporaryFile()
        # urlopen(image).read()
        # camshot.write(urlopen(image).read())
        # camshot.flush()
        # camshot = File(camshot)
        # name = str(camshot.name).split('\\')[-1]
        # name += '.jpg'  # store image in jpeg format
        # camshot.name = name
        # with open('image.txt', 'w+') as file:
        #     file.write(str(name))
        # default_storage.save('C:\Users\Sonata\Desktop\gitpull_jobportal\New-folder--4-\Job_portal\media\a.jpg', ContentFile(urlopen(image).read()))
        return HttpResponse('Done!')
    # return render(request, 'camshot.html',{'pics':row})

def get_exam_sheet(request):
    sheets=question_sheet.objects.all().values_list('sheet_id').distinct()
    return JsonResponse(list(sheets),safe=False)

def sceduled_user_full_details(request,refId):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    application = ApplicationDetails.objects.get(pk=refId)
    
    position_shortlisted_for=application.position_shortlisted_for
    branch_shortlisted_for=application.branch_shortlisted_for
    print(position_shortlisted_for,branch_shortlisted_for,"position_shortlisted_for,branch_shortlisted_for *************")
    vacancies = VacancyDetails.objects.filter(role=position_shortlisted_for, branch=branch_shortlisted_for).values_list('vacancy_id')
    print(vacancies,"vacancies *************")
    dates= InterviewDetails.objects.filter(vacancy_id__in=vacancies).values_list('interview_date').distinct()
    print(dates,"dates *************")
    formatted_dates = [d[0].strftime('%Y-%m-%d') for d in dates]
    print('formatted_dates',formatted_dates)
    today_date = datetime.today().strftime('%Y-%m-%d')
    
    if refId is not None:
        profile = candidate_details.objects.get(id=application.candidate_id)
        camshots = Candidate_Camshot.objects.filter(application_id=application.application_id)
        # document_obj = Document_Candidate.objects.get(candidate_id = application.candidate_id)

        print(camshots)
        pics = []
        row=[]
        for picture in camshots:
            picture.camshot_base64 = base64.b64encode(picture.camshot).decode('utf-8')
            row.append(picture.camshot_base64)
            print(row)
            pics.append(row[0])
            row.pop(0)

        try:
            resume_obj = ResumeFiles.objects.get(candidate_id = profile.id)
            resume = resume_obj.resume
            mime_type = resume_obj.mime_type
            encoded_data = base64.b64encode(resume).decode('utf-8')
        except Exception as e :
            print(e)
            encoded_data = None
            mime_type = None
            
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = profile.id)
            aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
            ssc_doc = document_obj.ssc_doc if document_obj.ssc_doc else None
            hsc_doc = document_obj.hsc_doc if document_obj.hsc_doc else None
            graduate_doc = document_obj.graduate_doc if document_obj.graduate_doc else None
            pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
            dl_doc = document_obj.dl_doc if document_obj.dl_doc else None
        except Exception as e:
            aadhar_doc = None
            ssc_doc = None
            hsc_doc = None
            graduate_doc = None
            pan_doc = None
            dl_doc = None
            
        GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        )
    else:
        profile = None
        # document_obj = None
        
    context={
        'mime_type':mime_type,
        'user_profile':profile,
        'interview_dates':formatted_dates,
        'binary_data':encoded_data,
        'status':application.application_status,
        'camshot':row,'pics': pics, 
        'today_date':today_date,
        'application':application,
        'gender_choices': GENDER,
        'candidate_id': profile.id,
        'aadhar_doc' : aadhar_doc,
        'pan_doc' : pan_doc,
        'dl_doc' : dl_doc,
        'ssc_doc': ssc_doc,
        'hsc_doc': hsc_doc,
        'graduate_doc': graduate_doc,
        'is_hr':is_hr ,'is_hrhead':is_hrhead,
        # 'document_obj': document_obj,
    }
    return render(request,'sceduled_user_full_details.html',context)

# from urllib.parse import parse

def schedule_test_user_full_details(request,refId):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    if refId is not None:
        print(refId)
        application = ApplicationDetails.objects.get(application_id=refId)
        profile = candidate_details.objects.get(id=application.candidate_id)

        # document_obj = Document_Candidate.objects.get(candidate_id = profile.id)
        position_shortlisted_for=application.position_shortlisted_for
        branch_shortlisted_for=application.branch_shortlisted_for
        print(position_shortlisted_for,branch_shortlisted_for,"position_shortlisted_for,branch_shortlisted_for *************")
        vacancies = VacancyDetails.objects.filter(role=position_shortlisted_for, branch=branch_shortlisted_for).values_list('vacancy_id')
        print(vacancies,"vacancies *************")
        dates= InterviewDetails.objects.filter(vacancy_id__in=vacancies).values_list('interview_date').distinct()
        print(dates,"dates *************")
        formatted_dates = [d[0].strftime('%Y-%m-%d') for d in dates]
        print('formatted_dates',formatted_dates)
        today_date = datetime.today().strftime('%Y-%m-%d')
        test_details = {}
        
        camshots = Candidate_Camshot.objects.filter(application_id=application.application_id)
        print(camshots)
        pics = []
        row=[]
        for picture in camshots:
            picture.camshot_base64 = base64.b64encode(picture.camshot).decode('utf-8')
            row.append(picture.camshot_base64)
            print(row)
            pics.append(row[0])
            row.pop(0)
        
        try:
            test_details=TestScheduleDetails.objects.get(candidate_id=profile.id,application_id = application.application_id)
        except TestScheduleDetails.DoesNotExist:
    # handle the case when the object does not exist, e.g., create a new object, show an error message, etc.
            pass
        
        # for verification 
        try:
            verify_obj = Verification_Document.objects.get(candidate_id = application.candidate_id)
        except Exception as e:
            print(e)
            verify_obj = Verification_Document()
            verify_obj.candidate_id = application.candidate_id
        
        if 'aadhar_verify' in request.POST:
            verify_obj.aadhar_verify = request.POST.get('aadhar_verify',None)
            print( 'aadhar_verify',verify_obj.aadhar_verify)
            verify_obj.save()
        if 'ssc_verify' in request.POST:
            verify_obj.ssc_verify = request.POST.get('ssc_verify',None)
            print( 'ssc_verify',verify_obj.ssc_verify)
            verify_obj.save()
        if 'hsc_verify' in request.POST:
            verify_obj.hsc_verify = request.POST.get('hsc_verify',None)
            print( 'hsc_verify',verify_obj.hsc_verify)
            verify_obj.save()
        if 'graduate_verify' in request.POST:
            verify_obj.graduate_verify = request.POST.get('graduate_verify',None)
            print( 'graduate_verify',verify_obj.graduate_verify)
            verify_obj.save()
        if 'pan_verify' in request.POST:
            verify_obj.pan_verify = request.POST.get('pan_verify',None)
            print( 'pan_verify',verify_obj.pan_verify)
            verify_obj.save()
        if 'dl_verify' in request.POST:
            verify_obj.dl_verify = request.POST.get('dl_verify',None)
            print( 'dl_verify',verify_obj.dl_verify)
            verify_obj.save()
            
        if 'basicdetails_verify' in request.POST:
            verify_obj.basicdetails_verify = request.POST.get('basicdetails_verify',None)
            print( 'basicdetails_verify',verify_obj.basicdetails_verify)
            verify_obj.save()

        # for upload the document 
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = application.candidate_id)
        except Exception as e:
            print(e)
            document_obj = Document_Candidate()
            document_obj.candidate_id = application.candidate_id
        
        if 'aadhar_doc' in request.FILES:
            document_obj.aadhar_doc = request.FILES['aadhar_doc']
            print( 'aadhar',document_obj.aadhar_doc)
            document_obj.save()
        if 'pan_doc' in request.FILES:
            document_obj.pan_doc = request.FILES['pan_doc']
            print( 'pan_doc',document_obj.pan_doc)
            document_obj.save()
        if 'dl_doc' in request.FILES:
            document_obj.dl_doc = request.FILES['dl_doc']
            print( 'dl_doc',document_obj.dl_doc)
            document_obj.save()
        if 'ssc_doc' in request.FILES:
            document_obj.ssc_doc = request.FILES['ssc_doc']
            print( 'ssc_doc',document_obj.ssc_doc)
            document_obj.save()
        if 'hsc_doc' in request.FILES:
            document_obj.hsc_doc = request.FILES['hsc_doc']
            print( 'hsc_doc',document_obj.hsc_doc)
            document_obj.save()
        if 'graduate_doc' in request.FILES:
            document_obj.graduate_doc = request.FILES['graduate_doc']
            print( 'graduate_doc',document_obj.graduate_doc)
            document_obj.save()

        try:
            testschedule_obj = TestScheduleDetails.objects.get(application_id = application.application_id)
            testschedule_obj.test_status='3'
            testschedule_obj.test_score=calculate_test_score(testschedule_obj.test_id)
            test_score = testschedule_obj.test_score
            total = total_marks(testschedule_obj.test_id)
            if test_score is not None and total is not None:
                percetage = float((test_score/total)*100)
            else:
                percetage = None
        except TestScheduleDetails.DoesNotExist:
            percetage = None
            testschedule_obj = None
            test_score = None
        
        try:
            resume_obj = ResumeFiles.objects.get(candidate_id = profile.id)
            resume = resume_obj.resume
            mime_type = resume_obj.mime_type
            encoded_data = base64.b64encode(resume).decode('utf-8')
            resume_file = resume_obj.resumeFile if resume_obj.resumeFile else None
        except ResumeFiles.DoesNotExist :
          
            encoded_data = None
            mime_type = None
            # resume_obj = None
            resume_file = None
            
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = profile.id)
            aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
            ssc_doc = document_obj.ssc_doc if document_obj.ssc_doc else None
            hsc_doc = document_obj.hsc_doc if document_obj.hsc_doc else None
            graduate_doc = document_obj.graduate_doc if document_obj.graduate_doc else None
            pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
            dl_doc = document_obj.dl_doc if document_obj.dl_doc else None
        except Exception as e:
            aadhar_doc = None
            ssc_doc = None
            hsc_doc = None
            graduate_doc = None
            pan_doc = None
            dl_doc = None
            
        try:
            verify_obj = Verification_Document.objects.get(candidate_id = profile.id)
            aadhar_verify = verify_obj.aadhar_verify if verify_obj.aadhar_verify else None
            ssc_verify = verify_obj.ssc_verify if verify_obj.ssc_verify else None
            hsc_verify = verify_obj.hsc_verify if verify_obj.hsc_verify else None
            graduate_verify = verify_obj.graduate_verify if verify_obj.graduate_verify else None
            dl_verify = verify_obj.dl_verify if verify_obj.dl_verify else None
            pan_verify = verify_obj.pan_verify if verify_obj.pan_verify else None
            basicdetails_verify = verify_obj.basicdetails_verify if verify_obj.basicdetails_verify else None

        except Exception as e:
            aadhar_verify = None
            ssc_verify = None
            hsc_verify = None
            pan_verify = None
            dl_verify = None
            graduate_verify = None
            basicdetails_verify =None
        GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        )
        
    else:
        profile = None
        # document_obj = None
        
    context={
        'mime_type':mime_type,
        'user_profile':profile,
        'binary_data':encoded_data,
        'interview_dates':formatted_dates,
        'status':application.application_status,
        'today_date':today_date,
        'application':application,
        'gender_choices': GENDER,
        'candidate_id': profile.id,
        'aadhar_doc' : aadhar_doc,
        'pan_doc' : pan_doc,
        'dl_doc' : dl_doc,
        'ssc_doc' :ssc_doc,
        'hsc_doc' :hsc_doc,
        'graduate_doc' :graduate_doc,
        'percetage' : percetage,
        'resume_file':resume_file,
        'bypass' : application.bypass,
        'document_obj':document_obj,
        'testschedule_obj': testschedule_obj,
        'test_details':test_details,
        'aadhar_verify':aadhar_verify,
        'ssc_verify' : ssc_verify,
        'hsc_verify' : hsc_verify,
        'pan_verify' : pan_verify,
        'dl_verify' : dl_verify,
        'graduate_verify' : graduate_verify,
        'basicdetails_verify' : basicdetails_verify,
        'camshot':row,'pics': pics,
        'is_hr':is_hr ,'is_hrhead':is_hrhead,
        # 'resume_obj':resume_obj,        
    }
    return render(request,'schedule_test_user_full_details.html',context)

@csrf_exempt
def fetch_interview_positions(request):
    positions=VacancyDetails.objects.values('role').distinct()
    print('p--------',positions)
    positions= map(lambda x:x[0],positions)
    print(positions)
    return JsonResponse(list(positions),safe=False)

@csrf_exempt
def fetch_interview_branches(request):
    if request.method=="POST":
        position = request.POST.get('position')
        print('position',position)
        vacancy_list = InterviewDetails.objects.filter(interview_date__gte=(datetime.now() - relativedelta(days=1))).values_list('vacancy_id')
        branches = VacancyDetails.objects.filter(vacancy_id__in = vacancy_list,role = position ,walk_in_id = 0).values('branch').distinct()
        print('branches--',branches)
        branches_json = json.dumps(list(branches))
        return JsonResponse(branches_json, safe=False)
    # return render(request,'accepted_user_full_details.html',{'user_profile':profile,'status':profile.status})

@csrf_exempt
def fetch_interview_dates(request):
    if request.method=="POST":
        place=request.POST.get('place')
        print(request.GET)
        print(place)
        dates=VacancyDetails.objects.filter(interview_place=place).values_list('interview_date').distinct()
        print(dates)
        return JsonResponse(list(dates),safe=False)

def test_view(request):
    panel=VacancyDetails.objects.values_list('panel_list').distinct()
    panel_names = {}
    for item in panel:
        panel_ids = item[0].split(',')
        k=''
        panel_members = User.objects.filter(id__in=panel_ids)
        for i in panel_members:
            k=k+i.username+','
        panel_names[item[0]]=k[:-1]

    print(panel_names)
    return JsonResponse(panel_names,safe=False)

   
@csrf_exempt
def fetch_interview_panel(request):
    if request.method=="POST":
        date=request.POST.get('date')
        branch_name=request.POST.get('branch_name')
        role_name=request.POST.get('role_name')
        print(request.GET)

        panel=InterviewDetails.objects.filter(interview_date=date).values_list('panel_list').distinct()
        print("PANEL: ",panel)
        panel_names = []
        for item in panel:
            panel_ids = item[0].split(',')
            k=''
            panel_members = User.objects.filter(id__in=panel_ids)
            for i in panel_members:
                k=k+i.username+','
            panel_names.append((item[0],k[:-1]))
        print(panel_names)
       
        return JsonResponse(panel_names,safe=False)
    
    
def applied_user_full_details(request, refId):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    if refId is not None:
        # application = ApplicationDetails.objects.get(application_id=refId)
        profile = candidate_details.objects.get(id=refId)
        application = ApplicationDetails.objects.filter(candidate_id=profile.id).first()
        test_schedule = TestScheduleDetails.objects.filter(candidate_id=profile.id)
        interview = InterviewDetails.objects.filter(interview_id=application.interview_id).first()
        
        try:
            offerletter_obj = OfferLetter.objects.get(candidate_id = application.candidate_id)
        except Exception as e:
            print(e)
            offerletter_obj = OfferLetter()
            offerletter_obj.candidate_id = application.candidate_id

        if  request.method == 'POST':
            offerletter_obj.name = request.POST.get('name')
            offerletter_obj.posting_place = request.POST.get('posting_place')
            offerletter_obj.desgination = request.POST.get('desgination')
            offerletter_obj.department = request.POST.get('department')
            offerletter_obj.address = request.POST.get('address')
            offerletter_obj.joining_date = datetime.strptime(request.POST.get('joining_date'),"%Y-%m-%d").replace(tzinfo=timezone.utc)
            offerletter_obj.save()
            print('offerletter_obj', offerletter_obj)
        
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = application.candidate_id)
        except Exception as e:
            print(e)
            document_obj = Document_Candidate()
            document_obj.candidate_id = application.candidate_id
        
        if 'aadhar_doc' in request.FILES:
            document_obj.aadhar_doc = request.FILES['aadhar_doc']
            print( 'aadhar',document_obj.aadhar_doc)
            document_obj.save()
        if 'pan_doc' in request.FILES:
            document_obj.pan_doc = request.FILES['pan_doc']
            print( 'pan_doc',document_obj.pan_doc)
            document_obj.save()
        if 'dl_doc' in request.FILES:
            document_obj.dl_doc = request.FILES['dl_doc']
            print( 'dl_doc',document_obj.dl_doc)
            document_obj.save()
        if 'ssc_doc' in request.FILES:
            document_obj.ssc_doc = request.FILES['ssc_doc']
            print( 'ssc_doc',document_obj.ssc_doc)
            document_obj.save()
        if 'hsc_doc' in request.FILES:
            document_obj.hsc_doc = request.FILES['hsc_doc']
            print( 'hsc_doc',document_obj.hsc_doc)
            document_obj.save()
        if 'graduate_doc' in request.FILES:
            document_obj.graduate_doc = request.FILES['graduate_doc']
            print( 'graduate_doc',document_obj.graduate_doc)
            document_obj.save()
        
        try:
            resume_obj = ResumeFiles.objects.get(candidate_id=profile.id)
            resume = resume_obj.resume
            encoded_data = base64.b64encode(resume).decode('utf-8')
            mime_type = resume_obj.mime_type
        except ResumeFiles.DoesNotExist:
            encoded_data = None
            mime_type = None
        
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = profile.id)
            aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
            ssc_doc = document_obj.ssc_doc if document_obj.ssc_doc else None
            hsc_doc = document_obj.hsc_doc if document_obj.hsc_doc else None
            graduate_doc = document_obj.graduate_doc if document_obj.graduate_doc else None
            pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
            dl_doc = document_obj.dl_doc if document_obj.dl_doc else None
        except Exception as e:
            aadhar_doc = None
            ssc_doc = None
            hsc_doc = None
            graduate_doc = None
            pan_doc = None
            dl_doc = None
            
        try:
            offerletter_obj = OfferLetter.objects.get(candidate_id = profile.id)
            name = offerletter_obj.name if offerletter_obj.name else None
            posting_place = offerletter_obj.posting_place if offerletter_obj.posting_place else None
            desgination = offerletter_obj.desgination if offerletter_obj.desgination else None
            department = offerletter_obj.department if offerletter_obj.department else None
            address = offerletter_obj.address if offerletter_obj.address else None
            joining_date = offerletter_obj.joining_date if offerletter_obj.joining_date else None

        except Exception as e:
            name = None
            posting_place = None
            desgination = None
            department = None
            address = None 
            joining_date = None
    else:
        profile = None
        test_schedule = None
        interview = None
        encoded_data = None
        mime_type = None

    context = { 
        'user_profile': profile,
        'test_schedule': test_schedule,
        'interview': interview,
        'binary_data': encoded_data,
        'mime_type': mime_type,
        'status': application.application_status,
        'application':application,
        'candidate_id': profile.id,
        'aadhar_doc' : aadhar_doc,
        'pan_doc' : pan_doc,
        'dl_doc' : dl_doc,
        'ssc_doc': ssc_doc,
        'hsc_doc': hsc_doc,
        'graduate_doc': graduate_doc,
        'document_obj':document_obj,
        'posting_place': posting_place,
        'desgination' : desgination,
        'department' : department,
        'address' : address,
        'joining_date': joining_date,
        'name' : name,
        'offerletter_obj': offerletter_obj,
        'is_hr':is_hr ,'is_hrhead':is_hrhead,
    }

    return render(request, 'applied_user_full_detail.html', context)

# import os

# def test(request,slug):
#     file_extension = os.path.splitext(slug)[1]
#     print(file_extension)
#     return redirect('home_page')
from pyresparser import ResumeParser
@transaction.atomic
def upload_CV(request):
    if request.method == 'POST':
        resumes_data = []
        try:
            # candidate = User_Details()
            candidate = candidate_details()
            # candidate.name = request.POST.get('candidate_full_name')                         
            # candidate.email = request.POST.get('candidate_email')
            # candidate.mobile_no = request.POST.get('candidate_mobile_no')
            # candidate.referred_by = request.POST.get('referred_by') if request.POST.get('referred_by') else None
            candidate.is_user = False
            candidate.save()
            # userroll = User_Rolls(roll_id=0,candidate_id = candidate.id)
            # userroll.save()
            # resume_obj = Resume_Repository()
            resume_obj=ResumeFiles()
            resume_obj.candidate_id = candidate.id
            #storing mime of the file in resume_repository
            file_name = request.FILES['candidate_resume'].name
            print('file_name',file_name)
            file_extension = os.path.splitext(file_name)[1]

            if file_extension.lower() == '.pdf':
                resume_obj.mime_type = 'application/pdf'
            elif file_extension.lower() in ['.jpg', '.jpeg', '.png']:
                resume_obj.mime_type = 'image/'+file_extension.lower()[1:]
            else:
                resume_obj.mime_type = 'unknown'
            resume_obj.resume = request.FILES['candidate_resume'].read()
            resume_obj.resumeFile = request.FILES['candidate_resume']

            resume_obj.save()         
            
            # extracting resume entities
            parser = ResumeParser(os.path.join(settings.MEDIA_ROOT,resume_obj.resumeFile.name))
            data = parser.get_extracted_data()
            print('data',data)
            resumes_data.append(data)
            print('resumes_data',resumes_data)
            candidate.name = data.get('name')
            candidate.email = data.get('email')
            candidate.mobile_no = data.get('mobile_number').replace('-','')
             
            if data.get('degree') is not None:
                candidate.education      = ', '.join(data.get('degree'))
            else:
                candidate.education      = None
            candidate.company_names      = data.get('company_names')
            candidate.college_name       = data.get('college_name')
            candidate.designation        = data.get('designation')
            candidate.total_experience   = data.get('total_experience')
            if data.get('skills') is not None:
                candidate.skills         = ', '.join(data.get('skills'))
            else:
                candidate.skills         = None
            if data.get('experience') is not None:
                candidate.experience     = ', '.join(data.get('experience'))
            else:
                candidate.experience     = None
            
            candidate.is_user = False
            candidate.save()
 
            messages.success(request,"CV uploaded successfully")
        except Exception as e:
            print('error',e)
            messages.error(request,"Something Went Wrong. Please Try Again.")
    
    return redirect('applied_user_details')

from .forms import CandidateBasicDetailsForm


def accepted_user_full_details(request,refId):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    if refId is not None:
        print(refId)
        profile = candidate_details.objects.get(id=refId)
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = profile.id)
        except Exception as e:
            print(e)
            document_obj = Document_Candidate()
            document_obj.candidate_id = profile.id
        
        if 'aadhar_doc' in request.FILES:
            document_obj.aadhar_doc = request.FILES['aadhar_doc']
            print( 'aadhar',document_obj.aadhar_doc)
            document_obj.save()
        if 'pan_doc' in request.FILES:
            document_obj.pan_doc = request.FILES['pan_doc']
            print( 'pan_doc',document_obj.pan_doc)
            document_obj.save()
        if 'dl_doc' in request.FILES:
            document_obj.dl_doc = request.FILES['dl_doc']
            print( 'dl_doc',document_obj.dl_doc)
            document_obj.save()
        if 'ssc_doc' in request.FILES:
            document_obj.ssc_doc = request.FILES['ssc_doc']
            print( 'ssc_doc',document_obj.ssc_doc)
            document_obj.save()
        if 'hsc_doc' in request.FILES:
            document_obj.hsc_doc = request.FILES['hsc_doc']
            print( 'hsc_doc',document_obj.hsc_doc)
            document_obj.save()
        if 'graduate_doc' in request.FILES:
            document_obj.graduate_doc = request.FILES['graduate_doc']
            print( 'graduate_doc',document_obj.graduate_doc)
            document_obj.save()

        try:
            resume_obj = ResumeFiles.objects.get(candidate_id = profile.id)
            resume = resume_obj.resume
            mime_type = resume_obj.mime_type
            encoded_data = base64.b64encode(resume).decode('utf-8')
        except Exception as e :
            print(e)
            encoded_data = None
            mime_type = None
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = profile.id)
            aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
            ssc_doc = document_obj.ssc_doc if document_obj.ssc_doc else None
            hsc_doc = document_obj.hsc_doc if document_obj.hsc_doc else None
            graduate_doc = document_obj.graduate_doc if document_obj.graduate_doc else None
            pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
            dl_doc = document_obj.dl_doc if document_obj.dl_doc else None
        except Exception as e:
            aadhar_doc = None
            ssc_doc = None
            hsc_doc = None
            graduate_doc = None
            pan_doc = None
            dl_doc = None

    else:
        profile = None

    if request.method == 'POST':
        form = CandidateBasicDetailsForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            profile = candidate_details.objects.get(id = refId)
            profile.reviewed_by = request.user.id
            profile.status = 1
            print('//////')
            print(request.user.id)
            print(request.user)
            profile.save()
            print(profile.reviewed_by)
            application= ApplicationDetails.objects.get(candidate_id=profile.id)
            
       
            if profile.created_date:
                ref_id = profile.created_date.strftime("%d%m%y")
               
            else:
                ref_id = datetime.now().date().strftime("%d%m%y")
            first_name = profile.name
            if first_name and len(first_name)>=3:
                ref_id += first_name[:3].upper()
            else:
                ref_id += "REF"
            # ref_id+=str(application.application_id)
            ref_id+=str(refId)
            print(ref_id)
            print(refId)

            url = "https://media.smsgupshup.com/GatewayAPI/rest"
            payload = f'userid=2000209909&password=z24gzBUA&phone_number={profile.mobile_no}&method=OPT_IN&auth_scheme=plain&v=1.1&channel=WHATSAPP&format=json'
            headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            
            url = f"https://media.smsgupshup.com/GatewayAPI/rest?userid=2000209909&password=z24gzBUA&send_to={profile.mobile_no}&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=Kindly+Note+the+Reference+ID%3A+{ref_id}+for+future+communication%2C+Thank+You.&isTemplate=true&header=The+CV+has+been+recieved%21"
            payload = {}
            headers = {}
            response = requests.request("POST", url, headers=headers, data=payload)
            url = f"https://media.smsgupshup.com/GatewayAPI/rest?userid=2000209909&password=z24gzBUA&send_to={profile.mobile_no}&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=You+can+now+check+the+status+of+the+application+in+our+portal&isTemplate=true&header=Greetings+From+Sonata%21"
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            url = f"https://media.smsgupshup.com/GatewayAPI/rest?userid=2000209909&password=z24gzBUA&send_to={profile.mobile_no}&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=To+proceed+with+the+application+process%2C+please+update+your+profile+with+necessary+documents%0AReference+ID%3A+{ref_id}&isTemplate=true&header=Greetings+from+Sonata+Finance"
            print(url)
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            print("response.....",response.text)

            return redirect('applied_user_details')  # Replace 'success_page' with the desired URL name or path for the success page
    else:
        print('form not valid')
        form = CandidateBasicDetailsForm(instance=profile)
    return render(request,'accepted_user_full_detail.html',{'mime_type':mime_type,'user_profile':profile,'form':form,'binary_data':encoded_data,'document_obj':document_obj,        'aadhar_doc' : aadhar_doc,
        'pan_doc' : pan_doc,
        'dl_doc' : dl_doc,
        'ssc_doc': ssc_doc,
        'hsc_doc': hsc_doc,
        'graduate_doc': graduate_doc,
        'status':profile.status,
        'is_hr':is_hr ,'is_hrhead':is_hrhead,})

def rejected_user_full_details(request,refId):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    profile = candidate_details.objects.get(id=refId)
    hr_users = User_Rolls.objects.filter(roll_id=1).values_list('user_id', flat=True)
    hr_users_names = User.objects.filter(id__in=hr_users).values_list('username', flat=True)
    
    if refId is not None:
        print(refId)
        profile = candidate_details.objects.get(id=refId)
        try:
            resume_obj = ResumeFiles.objects.get(candidate_id = profile.id)
            resume = resume_obj.resume
            mime_type = resume_obj.mime_type
            encoded_data = base64.b64encode(resume).decode('utf-8')
        except Exception as e :
            print(e)
            encoded_data = None
            mime_type = None
        
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = profile.id)
            aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
            pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
            dl_doc = document_obj.dl_doc if document_obj.dl_doc else None
        except Exception as e:
            aadhar_doc = None
            pan_doc = None
            dl_doc = None
    else:
        profile = None
        
    context = {'user_profile':profile,
               'hr_usernames':hr_users_names,
               'status':profile.status,
               'binary_data':encoded_data,
               'mime_type':mime_type,
               'candidate_id': profile.id,
                'aadhar_doc' : aadhar_doc,
                'pan_doc' : pan_doc,
                'dl_doc' : dl_doc,
                'is_hr':is_hr ,'is_hrhead':is_hrhead,
               }
    return render(request,'rejected_user_full_detail.html', context)

def review_allotment(request):
    if request.method == 'POST':
        try:
            applicatin_id = request.POST['applicatin_id']
            hr_username = request.POST['hr_username']
            hr_user = User.objects.get(username=hr_username)
            hr_user_id = hr_user.id
            allotment = RejectReviewAllotment.objects.get(applicatin_id=applicatin_id)
            allotment.application_id = applicatin_id
            allotment.alloted_to = hr_user_id
            allotment.save()
            messages.success(request, "Candidate alloted for reviewing")
        except Exception as e:
            print(e)
            messages.error(request, "Something went wrong")
            return redirect('rejected_applications')
    return redirect('rejected_applications')

@login_required(login_url='signIn')
def alloted_user_details(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    user_id=request.user.id
    alloted_applicants_ids = rejected_review_allotment.objects.filter(hr_id=user_id, review_status = False).values_list('candidate_id', flat=True)
    applicants = None
    if alloted_applicants_ids.exists():
        applicants = User_Details.objects.filter(id__in=alloted_applicants_ids)
        print(applicants)
        distinct_positions_queryset = applicants.values_list("position_shortlisted_for", flat=True).distinct()
        print(distinct_positions_queryset)
        distinct_positions = [position for position in distinct_positions_queryset if position is not None]
        print(distinct_positions)
    # print(applicants[0].name)    
    return render(request, 'alloted_user_details.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'applicants':applicants, 'distinct_positions':distinct_positions})

def api_alloted_filter(request):
    if request.method == 'POST':
        selected_position = request.POST.get('position', None)
        selected_branch = request.POST.get('branch', None)
        user_id=request.user.id
        alloted_applicants_ids = rejected_review_allotment.objects.filter(hr_id=user_id).values_list('candidate_id', flat=True)

        if alloted_applicants_ids.exists():
            applicants = User_Details.objects.filter(status=11).exclude(id__in = alloted_applicants_ids)

            if selected_position and selected_position != "None":
                applicants = applicants.filter(position_shortlisted_for=selected_position)

            if selected_branch and selected_branch != "None":
                applicants = applicants.filter(branch_shortlisted_for=selected_branch)

            applicants = applicants.order_by('-id').values(
                'id', 'name', 'email', 'mobile_no', 'position_shortlisted_for', 'branch_shortlisted_for'
            )

            data = list(applicants)

            return JsonResponse(data, safe=False)
    
def get_branch_alloted_options(request):
    if request.method == 'GET':
        selected_position = request.GET.get('position', None)
        if selected_position is None:
            # Handle the case when no position is selected
            return JsonResponse({'branch_options': []})
        else:
            # Fetch branch options based on the selected position
            user_id=request.user.id
            alloted_applicants_ids = rejected_review_allotment.objects.filter(hr_id=user_id, review_status = False).values_list('candidate_id', flat=True)
            applicants = None
            if alloted_applicants_ids.exists():
                applicants = User_Details.objects.filter(id__in=alloted_applicants_ids)
                branch_options = applicants.filter(position_shortlisted_for=selected_position, status=11).values_list('branch_shortlisted_for', flat=True).distinct()
                print(branch_options)
                return JsonResponse({'branch_options': list(branch_options)})

@login_required(login_url='signIn')
def reviewed_user_details(request):
    user_id=request.user.id
    alloted_applicants_ids = rejected_review_allotment.objects.filter(hr_id=user_id, review_status = True).values_list('candidate_id', flat=True)
    applicants = None
    if alloted_applicants_ids.exists():
        applicants = User_Details.objects.filter(id__in=alloted_applicants_ids)
    # print(applicants[0].name)    
    return render(request, 'reviewed_user_details.html',{'applicants':applicants})

def alloted_user_full_details(request,refId):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    if request.method == 'POST':
        applicant_id = request.POST.get('applicant_id')
        remarks = request.POST.get('remarks')
        try:
            review_obj = rejected_review_allotment.objects.get(candidate_id=applicant_id)
            review_obj.remarks = remarks
            review_obj.review_status = True
            review_obj.save()
            messages.error(request, "Review Submitted Successfully")
            return redirect('alloted_user_details')
        except Exception as e:
            print(e)
            messages.error(request, "Something went wrong")
            return redirect('alloted_user_details')
        
    if refId is not None:
        print(refId)    
        profile = candidate_details.objects.get(id=refId)
        try:
            resume_obj = ResumeFiles.objects.get(candidate_id = profile.id)
            resume = resume_obj.resume
            mime_type = resume_obj.mime_type
            encoded_data = base64.b64encode(resume).decode('utf-8')
        except Exception as e :
            print(e)
            encoded_data = None
            mime_type = None
        
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = profile.id)
            aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
            pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
            dl_doc = document_obj.dl_doc if document_obj.dl_doc else None
        except Exception as e:
            aadhar_doc = None
            pan_doc = None
            dl_doc = None
    else:
        profile = None

    reviewing_username = ''
    if profile.reviewed_by:
        reviewing_User = User.objects.get(id=profile.reviewed_by)
        reviewing_username = reviewing_User.username
    context = {'user_profile':profile,
               'reviewing_username':reviewing_username,
               'status':profile.status,
               'binary_data':encoded_data,
               'mime_type':mime_type,
               'candidate_id': profile.id,
               'aadhar_doc' : aadhar_doc,
               'pan_doc' : pan_doc,
               'dl_doc' : dl_doc,
               'is_hr':is_hr ,'is_hrhead':is_hrhead,
        }
    return render(request,'alloted_user_full_detail.html',context)

def hold_user_full_details(request,refId):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    if refId is not None:
        print(refId)
        profile = candidate_details.objects.get(id=refId)
        application = ApplicationDetails.objects.filter(candidate_id=profile.id).first()
        interview = InterviewDetails.objects.filter(interview_id=application.interview_id).first()

        # profile = ApplicationDetails.objects.get(candidate_id=refId)
        # candidate = candidate_details.objects.filter(id = profile.candidate_id)
        try:
            resume_obj = ResumeFiles.objects.get(candidate_id = profile.id)
            resume = resume_obj.resume
            mime_type = resume_obj.mime_type
            encoded_data = base64.b64encode(resume).decode('utf-8')
        except Exception as e :
            print(e)
            encoded_data = None
            mime_type = None
            
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = profile.id)
            aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
            pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
            dl_doc = document_obj.dl_doc if document_obj.dl_doc else None
        except Exception as e:
            aadhar_doc = None
            pan_doc = None
            dl_doc = None
            
        GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    else:
        profile = None
        interview = None
        encoded_data = None
        mime_type = None
    
    context = {
        'mime_type':mime_type,
        'user_profile':profile,
        'binary_data':encoded_data,
        'status':application.application_status,
        'application':application,
        'gender_choices': GENDER,
        'candidate_id': profile.id,
        'aadhar_doc' : aadhar_doc,
        'pan_doc' : pan_doc,
        'dl_doc' : dl_doc,
        'is_hr':is_hr ,'is_hrhead':is_hrhead
    }
    return render(request,'hold_user_full_detail.html',context)

def acceot_hold_candidate(request,refId=None):
    print(refId)
    if refId:
        application_obj = ApplicationDetails.objects.get(candidate_id=refId)
        application_obj.application_status=6
        application_obj.checked_by = request.user.id 
        application_obj.save()
        interview = InterviewDetails.objects.filter(pk = application_obj.interview_id).first()
        vacancy_obj = VacancyDetails.objects.get(pk=interview.vacancy_id)
        vacancy_obj.capacity = vacancy_obj.capacity - 1
        vacancy_obj.save()
    return redirect("shortlist_candidates")


# intwedate time place

@csrf_exempt
def accept_user(request, refId):
    if request.method == 'POST':
        # Retrieve the position and place from the POST data
        position = request.POST.get('position')
        place = request.POST.get('place')
        
        print(refId, position, place)
        # Get the user details object
        user_details = get_object_or_404(User_Details, id=refId)
        
        # Update the fields
        user_details.status = 2
        user_details.reviewed_by = request.user.id
        user_details.position_shortlisted_for = position
        user_details.branch_shortlisted_for = place
        user_details.save()
        
        # Return a JSON response indicating success
        return JsonResponse({'status': 'success'})
    
    # Return a JSON response indicating failure for non-POST requests
    return JsonResponse({'status': 'failure', 'message': 'Invalid request method.'})


    return redirect("applied_user_details")

# bypass for direct Interview
def bypass_user(request,refId=None):
    if request.method == "POST":
        print(refId)
        applicants_obj = ApplicationDetails.objects.get(application_id=refId)
        applicants_obj.application_status=4
        applicants_obj.checked_by = request.user.id 
        applicants_obj.bypass = request.POST['bypass']
        applicants_obj.bypass_date = datetime.date(datetime.now())
        applicants_obj.save()
    return redirect("schedule_test_user_full_details",refId=refId)

def hold_user(request,refId=None):
    if request.method == "POST":
        print(refId)
        applicants_obj = ApplicationDetails.objects.get(application_id=refId)
        applicants_obj.application_status=11
        applicants_obj.checked_by = request.user.id
        applicants_obj.hold_date= request.POST["hold_date"]
        applicants_obj.hold_reason = request.POST['hold_reason']
        applicants_obj.save()

    return redirect("shortlist_candidates")

def reject(request,refId=None):
  
    if request.method == "POST":
        applicants_obj = ApplicationDetails.objects.get(application_id = refId)
        applicants_obj.application_status=12
        applicants_obj.checked_by = request.user.id
        applicants_obj.reject_reason = request.POST['reject_reason']
        applicants_obj.reject_date = datetime.date(datetime.now())
        applicants_obj.save()
    return redirect("schedule_online_test")

def reject_user(request,refId=None):
  
    if request.method == "POST":
        applicants_obj = ApplicationDetails.objects.get(application_id = refId)
        applicants_obj.application_status=12
        applicants_obj.checked_by = request.user.id
        applicants_obj.reject_reason = request.POST['reject_reason']
        applicants_obj.reject_date = datetime.date(datetime.now())
        applicants_obj.save()
    return redirect("shortlist_candidates")

def reject_user_initial(request,application_id):
    if request.method == "POST":
        applicants_obj = ApplicationDetails.objects.get(application_id=application_id)
        applicants_obj.application_status=12
        applicants_obj.checked_by = request.user.id
        applicants_obj.reject_reason = request.POST['reject_reason']
        applicants_obj.reject_date = datetime.date(datetime.now())
        applicants_obj.save()
  
    return redirect("sceduled_user_details")


def vacancy_lists(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    # Open Vacancies
    sql_query = f"""
    SELECT * FROM VACANCY_DETAILS vd 
    LEFT JOIN INTERVIEW_DETAILS id ON vd.vacancy_id = id.vacancy_id 
    where walk_in_id = 0
    order by vacancy_date desc
                """
    vacancies = pd.read_sql_query(sql_query, engine)
    print(';;;;;;;;;;;;;;;;;;;')
    print(vacancies)
    
    if not vacancies.empty:
        vacancies['vacancy_date'] = vacancies['vacancy_date'].dt.strftime('%d-%m-%Y')
        vacancies['interview_date'] = vacancies['interview_date'].dt.strftime('%d-%m-%Y')

        print(str(request.user))
        print(type(str(request.user)))
        distinct_positions = vacancies[['role']]['role'].unique().tolist()
        print(vacancies)
        today = datetime.today().date()
        # vacancies = vacancies.sort_values(by=['vacancy_date'], ascending=False, inplace=True)
        vacancies.drop_duplicates(subset="vacancy_id", keep="first", inplace=True)
        vacancies.drop_duplicates(keep="first", inplace=True)
        vacancies = vacancies.to_dict("records")
        vacancy_list = InterviewDetails.objects.filter(interview_date__gt=today).values_list('vacancy_id')
        vacancies = VacancyDetails.objects.filter(vacancy_id__in = vacancy_list,walk_in_id = 0).order_by('-vacancy_date')                 

        pprint.pprint(vacancies)

        data = []
        for i in vacancies:
            d = {}
            d['id']=i.vacancy_id
            d['walk_in_id']=i.walk_in_id if i.walk_in_id else "-"
            d['branch_name']=i.branch if i.branch else "-"
            d['required_skills']=i.required_skills.split(",") if i.required_skills else []
            d['job_role']=i.role if i.role else "-"
            d['no_of_vacancies']=i.capacity if i.capacity else "-"
            d['qualification_type']=i.qualification if i.qualification else "-"
            d['required_experience']=i.required_experience if i.required_experience else "-"
            d['salary']=i.salary if i.salary else "-"
            d['vacancy_date']=i.vacancy_date if i.vacancy_date else "-"
            # d['interview_date'] = i.interview_date if i.interview_date else "-"
            data.append(d)
    else:
        data = []
        distinct_positions = []
    # Closed Vacancies
    sql_query = f"""
    SELECT * FROM VACANCY_DETAILS vd 
    LEFT JOIN INTERVIEW_DETAILS id ON vd.vacancy_id = id.vacancy_id 
    where walk_in_id = 0 or walk_in_id = 1
    order by vacancy_date desc
                """
    vacancies = pd.read_sql_query(sql_query, engine)
    print(vacancies)
    if not vacancies.empty:
        vacancies['vacancy_date'] = vacancies['vacancy_date'].dt.strftime('%d-%m-%Y')
        vacancies['interview_date'] = vacancies['interview_date'].dt.strftime('%d-%m-%Y')

        print(str(request.user))
        print(type(str(request.user)))
        distinct_positions = vacancies[['role']]['role'].unique().tolist()
        print(vacancies)
        # vacancies = vacancies.sort_values(by=['vacancy_date'], ascending=False, inplace=True)
        vacancies.drop_duplicates(subset="vacancy_id", keep="first", inplace=True)
        vacancies.drop_duplicates(keep="first", inplace=True)
        vacancies = vacancies.to_dict("records")
        vacancy_list = InterviewDetails.objects.filter(interview_date__lte=today).values_list('vacancy_id')
        vacancies = VacancyDetails.objects.filter(vacancy_id__in = vacancy_list).order_by('-vacancy_date')
        pprint.pprint(vacancies)

        data2 = []
        for i in vacancies:
            e = {}
            e['id']=i.vacancy_id
            e['walk_in_id']=i.walk_in_id if i.walk_in_id else "-"
            e['branch_name']=i.branch if i.branch else "-"
            e['required_skills']=i.required_skills.split(",") if i.required_skills else []
            e['job_role']=i.role if i.role else "-"
            e['no_of_vacancies']=i.capacity if i.capacity else "-"
            e['qualification_type']=i.qualification if i.qualification else "-"
            e['required_experience']=i.required_experience if i.required_experience else "-"
            e['salary']=i.salary if i.salary else "-"
            e['vacancy_date']=i.vacancy_date if i.vacancy_date else "-"
            # d['interview_date'] = i.interview_date if i.interview_date else "-"
            data2.append(e)
    else:
        data2 = []
        distinct_positions = []
    
        #for walk-in positions 
    sql_query = f"""
    SELECT * FROM VACANCY_DETAILS vd 
    LEFT JOIN INTERVIEW_DETAILS id ON vd.vacancy_id = id.vacancy_id 
    where walk_in_id = 1
    order by vacancy_date desc
                """
    vacancies1 = pd.read_sql_query(sql_query, engine)
    vacancy_list = []
    print('vacancies1',vacancies1)
    if not vacancies1.empty:
        vacancies1['vacancy_date'] = vacancies1['vacancy_date'].dt.strftime('%d-%m-%Y')
        vacancies1['interview_date'] = vacancies1['interview_date'].dt.strftime('%d-%m-%Y')
        print(str(request.user))
        print(type(str(request.user)))
        distinct_positions = vacancies1[['role']]['role'].unique().tolist()
        print(vacancies1)
        # vacancies = vacancies.sort_values(by=['vacancy_date'], ascending=False, inplace=True)
        vacancies1.drop_duplicates(subset="vacancy_id", keep="first", inplace=True)
        vacancies1.drop_duplicates(keep="first", inplace=True)
        vacancies1 = vacancies1.to_dict("records")
        vacancy_list = InterviewDetails.objects.filter(interview_date__gt=today).values_list('vacancy_id')
        vacancies1 = VacancyDetails.objects.filter(vacancy_id__in = vacancy_list,walk_in_id=1).order_by('-vacancy_date')
        pprint.pprint(vacancies1)

        data1 = []
        for i in vacancies1:
            k = {}
            k['id']=i.vacancy_id
            k['walk_in_id']=i.walk_in_id if i.walk_in_id else "-"
            k['branch_name']=i.branch if i.branch else "-"
            k['required_skills']=i.required_skills.split(",") if i.required_skills else []
            k['job_role']=i.role if i.role else "-"
            k['no_of_vacancies']=i.capacity if i.capacity else "-"
            k['qualification_type']=i.qualification if i.qualification else "-"
            k['required_experience']=i.required_experience if i.required_experience else "-"
            k['salary']=i.salary if i.salary else "-"
            k['vacancy_date']=i.vacancy_date if i.vacancy_date else "-"
            # k['interview_date'] = i.interview_date if i.interview_date else "-"
            data1.append(k)
    else:
        data1 = []
        distinct_positions = []
   
    pprint.pprint(data)
    context = {'vacancy':data,'vacancy1':data1,'vacancy2':data2, 'distinct_positions':distinct_positions,'is_hr':is_hr ,'is_hrhead':is_hrhead}    
    return render(request,'vacancy_lists.html',context)

def get_branch_vacancy_options(request):
    if request.method == 'GET':
        selected_position = request.GET.get('position', None)
        if selected_position is None:
            # Handle the case when no position is selected
            return JsonResponse({'branch_options': []})
        else:
            # Fetch branch options based on the selected position
            branch_options = VacancyDetails.objects.filter(role=selected_position).values_list('branch', flat=True).distinct()
            print(branch_options)
            return JsonResponse({'branch_options': list(branch_options)})

def vacancy_card_details(request,pk):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    
    sql_query = f"""
    SELECT * FROM "VACANCY_DETAILS" VD LEFT JOIN "INTERVIEW_DETAILS" ID ON VD.vacancy_id = ID.vacancy_id WHERE VD.vacancy_id={pk};
                """
    vacancy_df = pd.read_sql_query(sql_query, engine)
    # change the format of date to dd-mm-yyyy
    vacancy_df['interview_date'] = vacancy_df['interview_date'].dt.strftime('%d-%m-%Y')

    vacancy_df.fillna("-", inplace=True)
    vacancy_obj = vacancy_df.to_dict("records")[0]  
    return render(request,'vacancy_card_details.html',{'vacancy':vacancy_obj,'is_hr':is_hr ,'is_hrhead':is_hrhead})

from dateutil.relativedelta import relativedelta

def home_page(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    d = datetime.now()
    print('date', d)
    today = datetime.today().date()
    print("today_date", today)
    data =[]
    vacancy_idlist = InterviewDetails.objects.filter(interview_date__gt=today).values_list('vacancy_id')
    vacancy_list = VacancyDetails.objects.filter(vacancy_id__in = vacancy_idlist,walk_in_id=1).order_by('-vacancy_date')                 
    for i in vacancy_list:
        
        d = {}
        d['id']=i.vacancy_id
        d['walk_in_id']=i.walk_in_id if i.walk_in_id else "-"
        d['branch_name']=i.branch if i.branch else "-"
        d['required_skills']=i.required_skills.split(",") if i.required_skills else []
        d['job_role']=i.role if i.role else "-"
        d['no_of_vacancies']=i.capacity if i.capacity else "-"
        d['qualification_type']=i.qualification if i.qualification else "-"
        d['required_experience']=i.required_experience if i.required_experience else "-"
        d['salary']=int(i.salary) if int(i.salary) else "-"
        d['vacancy_date']=i.vacancy_date if i.vacancy_date else "-"
        data.append(d)
        
    data1 =[]
    vacancy_idlist = InterviewDetails.objects.filter(interview_date__gt=today).values_list('vacancy_id')
    vacancy_list1 = VacancyDetails.objects.filter(vacancy_id__in = vacancy_idlist,walk_in_id=0).order_by('-vacancy_date')                 
    for i in vacancy_list1:
        
        e = {}
        e['id']=i.vacancy_id
        e['walk_in_id']=i.walk_in_id if i.walk_in_id else "-"
        e['branch_name']=i.branch if i.branch else "-"
        e['required_skills']=i.required_skills.split(",") if i.required_skills else []
        e['job_role']=i.role if i.role else "-"
        e['no_of_vacancies']=i.capacity if i.capacity else "-"
        e['qualification_type']=i.qualification if i.qualification else "-"
        e['required_experience']=i.required_experience if i.required_experience else "-"
        e['salary']=int(i.salary) if int(i.salary) else "-"
        e['vacancy_date']=i.vacancy_date if i.vacancy_date else "-"
        data1.append(e)
    return render(request,'index_homepage.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'vacancy_list1':data1,'vacancy_list':data})

def candidate_login(request):
    return render(request,'candidate_login.html')
def HR_login(request):
    return render(request,'HR_login.html')

def interviewer_login(request):
    return render(request,'interview_login.html')


@transaction.atomic
def postjob(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    query = User_Rolls.objects.filter(roll_id=2).values_list('user_id', flat=True)
    queryset1 = User.objects.filter(id__in=query).values_list('username', flat=True)
    print(queryset1)
    queryset = []
    for query in queryset1:
        queryset.append(query)
        print(queryset)

    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            walk_in_id = form.cleaned_data['walk_in_id']
            branch = form.cleaned_data['branch']
            salary = form.cleaned_data['salary']
            role = form.cleaned_data['role']
            qualification = form.cleaned_data['qualification']

            interview_panel_1 = form.cleaned_data['interview_panel_1']
            interview_panel_2 = form.cleaned_data['interview_panel_2']
            interview_panel_3 = form.cleaned_data['interview_panel_3']
            interview_panel_4 = form.cleaned_data['interview_panel_4']
            panel_list = f"{interview_panel_1},{interview_panel_2},{interview_panel_3},{interview_panel_4}"
            no_of_vacancies = form.cleaned_data['no_of_vacancies']
            required_experience = form.cleaned_data['required_experience']
            required_skills = form.cleaned_data['required_skills']
            interview_place = form.cleaned_data['interview_place']
            address = form.cleaned_data['address']
            interview_date = form.cleaned_data['interview_date']
            interview_time= form.cleaned_data['interview_time']
            job_description = form.cleaned_data['job_description']
            job_responsibility= form.cleaned_data['job_responsibility']

            posted_on = datetime.today()
            vacancy_date = posted_on

            vacancy=VacancyDetails(walk_in_id=walk_in_id,branch=branch, salary=salary, role=role, qualification=qualification,vacancy_date=vacancy_date, capacity=no_of_vacancies, job_description=job_description, job_responsibility=job_responsibility, required_experience=required_experience, required_skills=required_skills)
            vacancy.save()
            vacancy_id = vacancy.pk
            InterviewDetails(vacancy_id=vacancy_id,
                             posted_on = posted_on,
                             interview_time=interview_time,
                             panel_member_a=interview_panel_1, panel_member_b=interview_panel_2, panel_member_c=interview_panel_3 , optional_member=interview_panel_4 , panel_list=panel_list, address=address,  interview_place=interview_place, interview_date=interview_date).save()
            
            # raise Exception("Test Exception")
            required_skills = request.POST.get('required_skills')
            required_skills=required_skills.split(",")
            print(required_skills)
            posted_on = datetime.today()
            print(posted_on)
            interview_panel_1 = request.POST.get('interview_panel_1')
            interview_panel_2 = request.POST.get('interview_panel_2')
            interview_panel_3 = request.POST.get('interview_panel_3')
            interview_panel_4 = request.POST.get('interview_panel_4')
            interview_date = request.POST.get('interview_date')
            interview_place = request.POST.get('interview_place')
            address = request.POST.get('address')
            messages.success(request, "Vacancy added successfully")
            print(interview_panel_1, interview_panel_2, interview_panel_3, interview_panel_4)
            interviewer_1 = User.objects.get(id=int(interview_panel_1))
            interviewer_2 = User.objects.get(id=int(interview_panel_2))
            interviewer_3 = User.objects.get(id=int(interview_panel_3))
            interviewer_4 = User.objects.get(id=int(interview_panel_4))
            usernames = [interviewer_1.username, interviewer_2.username, interviewer_3.username, interviewer_4.username]
            to_email = [interviewer_1.email, interviewer_2.email, interviewer_3.email, interviewer_4.email]
            # Loop through each interviewer and send the email
            # for username, email in zip(usernames, to_email):
            #     message = f"Dear {username}, Your Interview has been scheduled on the following Date: {interview_date} at {interview_place}."
            #     from_email = settings.EMAIL_HOST_USER
            #     send_mail("Interview Scheduled", message, from_email, [email])
            #     print("Interview Scheduled", message, from_email, [email])
            # messages.success(request, "Email Sended to all Interviewers")
            
            if 'url' in request.GET:
                refId=request.GET['id']
                return redirect(request.GET['url'], refId=refId)
            return redirect('vacancy_lists')
        else:
            messages.error(request, "Something went wrong")
            print("form not valid")
            return render(request,'postjob.html',{'form':form, 'queryset': queryset,'is_hr':is_hr ,'is_hrhead':is_hrhead})
    else:
        form = VacancyForm()
    return render(request,'postjob.html',{'form':form, 'queryset': queryset,'is_hr':is_hr ,'is_hrhead':is_hrhead})

@transaction.atomic
def update_job(request, vacancy_id=None):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    # Get the existing VacancyDetails instance
    vacancy = get_object_or_404(VacancyDetails, pk=vacancy_id)
    # Get the existing InterviewDetails instance associated with the VacancyDetails
    interview_details = get_object_or_404(InterviewDetails, vacancy_id=vacancy_id)

    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            # Update the VacancyDetails instance with the new data
            vacancy.walk_in_id = form.cleaned_data['walk_in_id']
            vacancy.branch = form.cleaned_data['branch']
            vacancy.salary = form.cleaned_data['salary']
            vacancy.role = form.cleaned_data['role']
            vacancy.qualification = form.cleaned_data['qualification']
            vacancy.capacity = form.cleaned_data['no_of_vacancies']
            vacancy.required_experience = form.cleaned_data['required_experience']
            vacancy.required_skills = form.cleaned_data['required_skills']
            vacancy.job_description= form.cleaned_data['job_description']
            vacancy.job_responsibility = form.cleaned_data['job_responsibility']                  
            vacancy.save()

            # Update the InterviewDetails instance with the new data
            interview_panel_1 = form.cleaned_data['interview_panel_1']
            interview_panel_2 = form.cleaned_data['interview_panel_2']
            interview_panel_3 = form.cleaned_data['interview_panel_3']
            interview_panel_4 = form.cleaned_data['interview_panel_4']
            panel_list = f"{interview_panel_1},{interview_panel_2},{interview_panel_3},{interview_panel_4}"

            interview_details.interview_time = form.cleaned_data['interview_time']
            interview_details.panel_member_a = interview_panel_1
            interview_details.panel_member_b = interview_panel_2
            interview_details.panel_member_c = interview_panel_3
            interview_details.optional_member = interview_panel_4
            interview_details.panel_list = panel_list
            interview_details.required_experience = form.cleaned_data['required_experience']
            interview_details.required_skills = form.cleaned_data['required_skills']
            interview_details.interview_place = form.cleaned_data['interview_place']
            interview_details.address = form.cleaned_data['address']
            interview_details.interview_date = form.cleaned_data['interview_date']
            interview_details.job_description = form.cleaned_data['job_description']
            interview_details.job_responsibility = form.cleaned_data['job_responsibility']
            interview_details.save()

            # Redirect to some view or template after successful update
            return redirect('vacancy_lists')
    else:
        # Pre-populate the form with existing data
        initial_data = {
            'walk_in_id': vacancy.walk_in_id,
            'branch': vacancy.branch,
            'salary': vacancy.salary,
            'role': vacancy.role,
            'qualification': vacancy.qualification,
            'interview_panel_1': interview_details.panel_member_a,
            'interview_panel_2': interview_details.panel_member_b,
            'interview_panel_3': interview_details.panel_member_c,
            'interview_panel_4': interview_details.optional_member,
            'no_of_vacancies': vacancy.capacity,
            'required_experience': vacancy.required_experience,
            'required_skills': vacancy.required_skills,
            'interview_place': interview_details.interview_place,
            'address': interview_details.address,
            'interview_date': interview_details.interview_date,
            'interview_time': interview_details.interview_time,
            'job_description': vacancy.job_description,
            'job_responsibility': vacancy.job_responsibility,  
            'is_hr':is_hr ,
            'is_hrhead':is_hrhead,          
        }
        form = VacancyForm(initial=initial_data)

    context = {
        'form': form,
        'update':True
    }
    return render(request, 'postjob.html', context)
    
def application_status(request):

    # User_Details_obj=User_Details.objects.filter(email=request.user.email)
    print("User_Details_obj")
    # print(User_Details_obj.pk)
    # print(User_Details_obj.values())
    # print(User_Details_obj.pk)
    if not candidate_details.objects.filter(email=request.user.email).exists():
        User_Details_obj=candidate_details(email=request.user.email)
        User_Details_obj.save()
        redirect_url = reverse('view_candidate_profile', args=[User_Details_obj.email])
        return redirect(redirect_url) 
    else:
        df=pd.DataFrame(candidate_details.objects.filter(email=request.user.email).values()).to_dict(orient="records")
        print(df)
        print("df",df[0]['id'])
        redirect_url = reverse('view_candidate_profile', args=[df[0]['email']])
        return redirect(redirect_url)
  
def applied_vacancy_card_details(request,pk):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    user_id=request.user.id
    email=request.user.email
    user_roll=User_Rolls.objects.get(user_id=user_id)


    candidate = candidate_details.objects.filter(email = request.user.email).values('id')
    print('candidate',candidate)
    int = InterviewDetails.objects.filter(vacancy_id = pk).values('interview_id')
    print('interview_id',int)
    # app = ApplicationDetails.objects.filter(interview_id__in = int,candidate_id__in = candidate)
    # print('application_details',app.application_id)
    df =pd.DataFrame(ApplicationDetails.objects.filter(interview_id__in = int,candidate_id__in = candidate).values()).to_dict(orient="records")
    print(df)
    print("df",df[0]['application_id'])
   
    sql_query = f"""
                SELECT * FROM "VACANCY_DETAILS" VD LEFT JOIN "INTERVIEW_DETAILS" ID ON VD.vacancy_id = ID.vacancy_id LEFT JOIN "APPLICATION_DETAILS" AD
                ON ID.interview_id = AD.interview_id WHERE VD.vacancy_id={pk} and AD.application_id = {df[0]['application_id']};
                """
    vacancy_df = pd.read_sql_query(sql_query, engine)

    # change the format of date to dd-mm-yyyy
    vacancy_df['interview_date'] = vacancy_df['interview_date'].dt.strftime('%d-%m-%Y')
    vacancy_df.fillna("-", inplace=True)
    vacancy_obj = vacancy_df.to_dict("records")[0]   
    candidate = vacancy_df['candidate_id']
    print('candidate', candidate)    
    # interview = vacancy_df['interview_id'].astype(int)
    # print('interview', interview)
    
    application = ApplicationDetails.objects.filter(candidate_id=candidate).first()
    return render(request,'applied_vacancy_card_details.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'vacancy':vacancy_obj,'application':application,'status': application.application_status,'user_roll':user_roll,'email':email})

def new_form(request,refId):
    user_profile_obj = User_Details.objects.get(id=refId)
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    context = {'user_profile':user_profile_obj,
               'gender_choices': GENDER}
    return render(request,'form_ui.html',context)    
from datetime import datetime

@login_required(login_url='signIn')
def sceduled_interview_details(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    context={}
    #------
    # extracts panel member user ids from panel_list column
    def panel_id_extractor(request,interview_panel_list):
        print("Type of interview panel list ",request.user.id,type(interview_panel_list))
        print(interview_panel_list)
        panel_id_list=[]
        try:
            # comma seperated ids in a string
            panel_id_list=interview_panel_list.split(',')
            panel_id_list_int = [int(x) for x in panel_id_list]
            return panel_id_list_int
        except Exception as e:
            print('panel_id_extractor: ', str(e))
            return panel_id_list

    # checks if interviewer is in panel
    def panel_checker(request,panel_id_list):
        print(panel_id_list)
        if request.user.id in panel_id_list:
            return 1
        else:
            return 0

    # current date
    date = datetime.today().strftime('%Y-%m-%d')
    # fetching applications whose interview has been scheduled
    sql_query = f"""SET NOCOUNT ON;SELECT application_id,interview_id FROM application_details WHERE application_status = 5;SET NOCOUNT OFF"""
    application_df=pd.read_sql_query(sql_query,engine)
    application_df.dropna(inplace=True)
    # list of interviews(ids) of those applications
    interview_id_list = application_df['interview_id'].unique().tolist()
    print(interview_id_list)
    # secure interview instances of those applications
    if application_df.empty:
        return render(request, 'sceduled_Interview_Details.html',context)
    if len(interview_id_list) == 1:
        sql_query = f"""SET NOCOUNT ON;SELECT * FROM INTERVIEW_DETAILS WHERE interview_date = '{date}' and interview_id = {interview_id_list[0]};SET NOCOUNT OFF"""
    else:
        sql_query = f"""SET NOCOUNT ON;SELECT * FROM INTERVIEW_DETAILS WHERE interview_date = '{date}' and interview_id in {tuple(interview_id_list)};SET NOCOUNT OFF"""
    interview_df=pd.read_sql_query(sql_query,engine)
    print(interview_df.dtypes)
    print(interview_df)

    try:
        #check in which panels he is present, first we find the panel member ids in each of the interviews
        interview_df['panel_id_list'] = interview_df.apply(lambda x: panel_id_extractor(request,x['panel_list']), axis=1)
        print(interview_df)
        #then we check whether current interviewer is present in any of those panels
        interview_df['panel_flag'] = interview_df.apply(lambda x: panel_checker(request,x['panel_id_list']), axis=1)
        print(interview_df)
        #interviews only where the current interviewer is present in the panel
        interview_id_list = interview_df[interview_df['panel_flag']==1]['interview_id'].to_list()
        print(interview_id_list)

        # secure applications of these interviews(what the f)
        if len(interview_id_list) == 0:
            return render(request, 'sceduled_Interview_Details.html',context)
        if len(interview_id_list) == 1:
            sql_query = f"""SET NOCOUNT ON;SELECT * FROM application_details WHERE interview_id = {interview_id_list[0]} and application_status = 5;SET NOCOUNT OFF"""
        else:
            sql_query = f"""SET NOCOUNT ON;SELECT * FROM application_details WHERE interview_id in {tuple(interview_id_list)} and application_status = 5 ;SET NOCOUNT OFF"""
        application_df=pd.read_sql_query(sql_query,engine)
        sql_query = f"""SET NOCOUNT ON;SELECT * FROM candidate_details ;SET NOCOUNT OFF"""
        candidate_df=pd.read_sql_query(sql_query,engine)
        applicants=pd.merge(application_df,candidate_df,left_on='candidate_id',right_on='id',how='left')

        context['applicants']=applicants.to_dict(orient='records')
        print('dwaaaaaaa')
        print(context['applicants'])
        context['is_hr'] = is_hr
        context['is_hrhead'] = is_hrhead
        return render(request, 'sceduled_Interview_Details.html',context)
    except Exception as e:
        print('error', e)
        return render(request, 'sceduled_Interview_Details.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead})
    
def search_exam(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass  
    if request.method == "POST":
        searched = request.POST['searched']        
        applicants = User_Details.objects.filter(Q(name__contains=searched),status__gte=4)
        print(applicants)
        return render(request, 'exam_user_details.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'searched':searched,'applicants':applicants})
    else:
        return render(request, 'exam_user_details.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'applicants':applicants})

def search(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass   
    if request.method == "POST":
        searched = request.POST['searched']       
        applicants = User_Details.objects.filter(Q(name__contains=searched),status=5)
        return render(request, 'sceduled_Interview_Details.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'searched':searched,'applicants':applicants})
    else:
        return render(request, 'sceduled_Interview_Details.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'applicants':applicants})

def sceduled_interview_full_details(request,refId):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    if refId is not None:
        print(refId)
        # profile = User_Details.objects.get(id=refId)
        application=ApplicationDetails.objects.get(application_id=refId)
        profile = candidate_details.objects.get(id=application.candidate_id)
        interview_assignment_obj = InterviewResponse.objects.filter(application_id = refId)
        data_num = 0
        for i in interview_assignment_obj:
            data_num+=1
        try:
            # resume_obj = Resume_Repository.objects.get(candidate_id = profile.id)
            resume_obj = ResumeFiles.objects.get(candidate_id = profile.id)
            resume = resume_obj.resume
            mime_type = resume_obj.mime_type
            encoded_data = base64.b64encode(resume).decode('utf-8')
        except Exception as e :
            print(e)
            encoded_data = None
            mime_type = None
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = profile.id)
            aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
            ssc_doc = document_obj.ssc_doc if document_obj.ssc_doc else None
            hsc_doc = document_obj.hsc_doc if document_obj.hsc_doc else None
            graduate_doc = document_obj.graduate_doc if document_obj.graduate_doc else None
            pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
            dl_doc = document_obj.dl_doc if document_obj.dl_doc else None
        except Exception as e:
            aadhar_doc = None
            ssc_doc = None
            hsc_doc = None
            graduate_doc = None
            pan_doc = None
            dl_doc = None
    else:
        profile = None
        
    GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    )
    for obj in interview_assignment_obj:
        if obj.interviewer_id == request.user.id:
            messages.error(request, "You already assessed this Candidate.")
            if 'HTTP_REFERER' in request.META:
                return redirect(request.META['HTTP_REFERER'])
    
    # test_schedule=TestSchedule.objects.filter(candidate_id=profile.id).values().first()
    test_schedule=TestScheduleDetails.objects.filter(candidate_id=profile.id).values().first()
    places=vacancy.objects.values_list('interview_place').distinct()
    places= map(lambda x:x[0],places)
    # return render(request,'sceduled_interview_full_details.html',{'user_profile':profile,'interveiw_places':places,'test_schedule':test_schedule,'status':profile.status})
    return render(request,'sceduled_Interview_full_Details.html',{'application':application,'user_profile':profile,'interveiw_places':places,
                                                                  'test_schedule':test_schedule,'binary_data':encoded_data,'status':application.application_status,
                                                                  'mime_type':mime_type, 'data_num': data_num, 'application_id': refId,'gender_choices':GENDER,'candidate_id': profile.id,'aadhar_doc' : aadhar_doc,'pan_doc' : pan_doc,'dl_doc' : dl_doc, 
                                                                  'ssc_doc': ssc_doc,'hsc_doc': hsc_doc,'graduate_doc': graduate_doc,'bypass' : application.bypass,'is_hr':is_hr ,'is_hrhead':is_hrhead})

# @csrf_exempt
# class interview_Api(View):
#     def get(self, request, userid):
#         context = {}
#         login_status = False
#         context['login_status'] = login_status
#         return render(request, 'get_loc.html', context)
# function for attendance check
@csrf_exempt
def interview_Api(request):
    context = {}   
    if request.method=='POST':
        interview_assignment_obj=InterviewResponse()
        
        interview_assignment_obj.application_id=request.POST.get('application_id')
        interview_assignment_obj.interviewer_id=request.user.id
        interview_assignment_obj.field_1 = int(request.POST.get('self_confidence'))
        interview_assignment_obj.field_2 = int(request.POST.get('verbal'))
        interview_assignment_obj.field_3 = int(request.POST.get('written'))
        interview_assignment_obj.field_4 = int(request.POST.get('non_verbal'))
        interview_assignment_obj.field_5 = int(request.POST.get('competency'))
        interview_assignment_obj.field_6 = int(request.POST.get('maturity'))
        interview_assignment_obj.field_7 = int(request.POST.get('commitment_towards_social_mission'))
        interview_assignment_obj.field_8 = int(request.POST.get('culture_fit'))
        interview_assignment_obj.field_9 = int(request.POST.get('stability'))
        interview_assignment_obj.field_10 = int(request.POST.get('leadership'))

        interview_assignment_obj.field_11 = int(request.POST.get('consistency'))
        interview_assignment_obj.field_12 = int(request.POST.get('planning_organizing'))
        interview_assignment_obj.field_13 = int(request.POST.get('team_work'))
        interview_assignment_obj.field_14 = int(request.POST.get('initiactive_drive'))
        interview_assignment_obj.field_15 = int(request.POST.get('decision_making'))
        interview_assignment_obj.field_16 = int(request.POST.get('deligation'))
        interview_assignment_obj.field_17 = int(request.POST.get('analytical_ability'))
        interview_assignment_obj.field_18 = int(request.POST.get('application_of_concept'))
        interview_assignment_obj.field_19 = int(request.POST.get('academic_background'))
        interview_assignment_obj.field_20 = int(request.POST.get('gd_case_study'))
        interview_assignment_obj.total_A=interview_assignment_obj.field_1+interview_assignment_obj.field_2+interview_assignment_obj.field_3+interview_assignment_obj.field_4+interview_assignment_obj.field_5+interview_assignment_obj.field_6+interview_assignment_obj.field_7+interview_assignment_obj.field_8+interview_assignment_obj.field_9+interview_assignment_obj.field_10
        interview_assignment_obj.total_B=interview_assignment_obj.field_11+interview_assignment_obj.field_12+interview_assignment_obj.field_13+interview_assignment_obj.field_14+interview_assignment_obj.field_15+interview_assignment_obj.field_16+interview_assignment_obj.field_17+interview_assignment_obj.field_18+interview_assignment_obj.field_19+interview_assignment_obj.field_20
        interview_assignment_obj.total=interview_assignment_obj.total_A+interview_assignment_obj.total_B
        score=int(interview_assignment_obj.total)/100
        score=score*100
        interview_assignment_obj.score=score
        interview_assignment_obj.save()
        print("InterviewResponse ID: ",interview_assignment_obj.response_id)

        application_obj=ApplicationDetails.objects.get(application_id=interview_assignment_obj.application_id)
        user_details_obj=candidate_details.objects.get(id=application_obj.candidate_id)
        context['success'] = 'success'
        context['user_profile'] = user_details_obj
        context['application_id']=application_obj.application_id
    return redirect(sceduled_interview_details)

@csrf_exempt
def number_of_interviewer(request):
    context={}
    if request.method=='POST':
        application_id=request.POST.get('application_id')
        sql_query = f"""SET NOCOUNT ON;SELECT count(response_id) FROM interview_response WHERE application_id = {int(application_id)};SET NOCOUNT OFF"""
        df=pd.read_sql_query(sql_query,engine)
        print("DFFFFFFFFFFFFFFFFff")
        print(df)
        print(df.iat[0,0])
        context['success']='success'
        context['data_num']=int(df.iat[0,0])
        if( df.iat[0,0] >= 3 ):
            # user_details_obj=User_Details.objects.get(id=candidate_id)
            user_details_obj=ApplicationDetails.objects.get(application_id=application_id)
            user_details_obj.application_status='6'
            user_details_obj.save()
        return JsonResponse(context)

@csrf_exempt
def post_question(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    context={}
    if request.method == 'POST':
        if 'step1' in request.POST:
            sheet_id = request.POST['sheet_id']
            question_sheet_obj=question_sheet.objects.filter(sheet_id=sheet_id).values().last()
            print('DDDDDDDDDDDDDDD')
            print(question_sheet_obj['question_id'])
            context['question_id_new']=question_sheet_obj['question_id']+1
            context['status']='success'
            return JsonResponse(context)
        if 'step2' in request.POST:
            question_sheet_obj=question_sheet()
            question_sheet_obj.sheet_id=request.POST.get('sheet_id')
            question_sheet_obj.question_id=request.POST.get('question_id')
            question_sheet_obj.question_text=request.POST.get('question_text')
            question_sheet_obj.option_a=request.POST.get('option_a')
            question_sheet_obj.option_b=request.POST.get('option_b')
            question_sheet_obj.option_c=request.POST.get('option_c')
            question_sheet_obj.option_d=request.POST.get('option_d')
            question_sheet_obj.answer=request.POST.get('answer')
            question_sheet_obj.save()
        return redirect(quest_sheet_list)
    context['is_hr'] = is_hr
    context['is_hrhead'] = is_hrhead
    return render(request,'post_question.html',context)
            
def ques_sheet(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    question = question_sheet.objects.filter()
    return render(request, 'question_sheet.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'question':question})

from django.db.models import Count
# show cards for question sheet list

def quest_sheet_list(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    sheets = question_sheet.objects.all().values('sheet_id').distinct()
    questions = question_sheet.objects.values('sheet_id').annotate(Count('sheet_id')) 
    return render(request, 'quest_sheet_list.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'sheets':sheets,'questions':questions})

def quest_sheetlist_details(request,sheet_id):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    quest_details = question_sheet.objects.filter(sheet_id=sheet_id)
    print(quest_details)
    return render(request, 'quest_sheetlist_details.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'quest_details':quest_details})

def edit_question(request,id):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    print(id)
    error = ""
    edit_ques = question_sheet.objects.get(id=id)
    if request.method == "POST":
        # print(question_id)
        
        edit_ques = question_sheet.objects.get(id=id)
        # edit_quest = question_sheet.objects.filter(question_id=edit_ques.question_id)

        question_text = request.POST['question_text']
        option_a = request.POST['option_a']
        option_b = request.POST['option_b']
        option_c = request.POST['option_c']
        option_d = request.POST['option_d']
        answer = request.POST['answer']
            
        edit_ques.question_text=question_text
        edit_ques.option_a=option_a
        edit_ques.option_b=option_b
        edit_ques.option_c=option_c
        edit_ques.option_d=option_d
        edit_ques.answer=answer
        edit_ques.save()
        
        try:            
            error= "no"
            redirect_url = reverse('quest_sheetlist_details', args=[edit_ques.sheet_id])
            return redirect(redirect_url)
        except:
            error="yes"
    return render(request, 'edit_question.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'edit_ques':edit_ques})

def delete_question(request,id):
    del_quest = question_sheet.objects.get(id=id)
    print(del_quest)
 
    try:
        del_quest.delete()
        messages.success(request, "Question Deleted Successfully.")
        redirect_url = reverse('quest_sheetlist_details', args=[del_quest.sheet_id])
        return redirect(redirect_url)   
    except:
        messages.error(request, "Failed to Delete Question")
        redirect_url = reverse('quest_sheetlist_details', args=[del_quest.sheet_id])
        return redirect(redirect_url)    
    
# @can_access_candidate_profile
def view_candidate_profile(request, email):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
        
    print("Email:", email)
    
    context = {}
    try:
        user_profile = candidate_details.objects.get(email=email)
        # Assuming you have a "status" attribute in your User_Details model
        status = user_profile.status
        # Resume handling
        try:
            resume_obj = ResumeFiles.objects.get(candidate_id=user_profile.id)
            resume = resume_obj.resume
            mime_type = resume_obj.mime_type
            encoded_data = base64.b64encode(resume).decode('utf-8')
        except ResumeFiles.DoesNotExist:
            encoded_data = None
            mime_type = None        
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = user_profile.id)
            aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
            ssc_doc = document_obj.ssc_doc if document_obj.ssc_doc else None
            hsc_doc = document_obj.hsc_doc if document_obj.hsc_doc else None
            graduate_doc = document_obj.graduate_doc if document_obj.graduate_doc else None
            pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
            dl_doc = document_obj.dl_doc  if document_obj.dl_doc else None
        except Exception as e:
            aadhar_doc = None
            ssc_doc = None
            hsc_doc = None
            graduate_doc = None     
            pan_doc = None
            dl_doc = None
            
        try:
            verify_obj = Verification_Document.objects.get(candidate_id = user_profile.id)
            aadhar_verify = verify_obj.aadhar_verify if verify_obj.aadhar_verify else None
            ssc_verify = verify_obj.ssc_verify if verify_obj.ssc_verify else None
            hsc_verify = verify_obj.hsc_verify if verify_obj.hsc_verify else None
            graduate_verify = verify_obj.graduate_verify if verify_obj.graduate_verify else None
            dl_verify = verify_obj.dl_verify if verify_obj.dl_verify else None
            pan_verify = verify_obj.pan_verify if verify_obj.pan_verify else None
            basicdetails_verify = verify_obj.basicdetails_verify if verify_obj.basicdetails_verify else None

        except Exception as e:
            aadhar_verify = None
            ssc_verify = None
            hsc_verify = None
            pan_verify = None
            dl_verify = None
            graduate_verify = None
            basicdetails_verify =None
                   
    except Exception as e:
        # Handle the case when the user profile does not exist.
        # You can redirect the user to a custom 404 page or display an error message.
        return render(request, 'profile_not_found.html',{'e':e})
                                    
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )   
    context = {
        'user_profile': user_profile,
        'gender_choices': GENDER,
        'email': email,
        'status': status,
        'binary_data': encoded_data,
        'mime_type': mime_type,
        'candidate_id': user_profile.id,
        'ssc_doc': ssc_doc,
        'hsc_doc': hsc_doc,
        'graduate_doc': graduate_doc,
        'aadhar_doc' : aadhar_doc,
        'pan_doc' : pan_doc,
        'dl_doc' : dl_doc,
        'document_obj':document_obj,
        'aadhar_verify':aadhar_verify,
        'ssc_verify' : ssc_verify,
        'hsc_verify' : hsc_verify,
        'pan_verify' : pan_verify,
        'dl_verify' : dl_verify,
        'graduate_verify' : graduate_verify,
        'basicdetails_verify' : basicdetails_verify,
        'is_hr':is_hr ,'is_hrhead':is_hrhead,
    }

    # Check if the user has access; the can_access_candidate_profile decorator
    # will handle the unauthorized case, so no need to render 'unauthorized.html' here.

    return render(request, 'view_candidate_profile.html', context)

def upload_documents(request,candidate_id):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    context = {}
    if candidate_id is not None:
        candidate_profile = candidate_details.objects.get(id=candidate_id)
    else:
        candidate_profile = None
    if request.method == 'POST' and request.FILES :
        document_obj = Document_Candidate.objects.get(candidate_id = candidate_profile.id)
        # if len(request.FILES) !=0:
        document_obj.aadhar_doc = request.FILES.get('aadhar_doc') or None   
        document_obj.pan_doc = request.FILES.get('pan_doc') or None
        document_obj.dl_doc = request.FILES.get('dl_doc') or None
        document_obj.ssc_doc = request.FILES.get('ssc_doc') or None
        document_obj.hsc_doc = request.FILES.get('hsc_doc') or None
        document_obj.graduate_doc = request.FILES.get('graduate_doc') or None
        
        document_obj.save()   
        context = {
            'document_obj':document_obj,
            'is_hr':is_hr ,'is_hrhead':is_hrhead,
        }
    return render(request, 'upload_documents.html', context)
    # context = {}
    # if candidate_id is not None:
    #     candidate_profile = candidate_details.objects.get(id=candidate_id)
    # else:
    #     candidate_profile = None

    # document_obj = Document_Candidate.objects.get(candidate_id = candidate_profile.id)
    # if request.method == 'POST' and request.FILES :
    #     try:
    #     # form = DocumentForm(request.POST, request.FILES)
    #     # if form.is_valid:
            
    #         aadhar_doc = request.FILES.get('aadhar_doc') 
    #         print('Aadhar',document_obj.aadhar_doc) 
    #         pan_doc = request.FILES.get('pan_doc') 
    #         print('PAN', document_obj.pan_doc) 
    #         dl_doc = request.FILES.get('dl_doc') 
    #         print('DL..', document_obj.dl_doc)
    #         ssc_doc = request.FILES.get('ssc_doc') 
    #         print('SSC..', document_obj.ssc_doc)
    #         hsc_doc = request.FILES.get('hsc_doc')
    #         print('HSC..', document_obj.hsc_doc)
    #         graduate_doc = request.FILES.get('graduate_doc') 
    #         print('GRADUATE..',document_obj.graduate_doc)
           
    #         # initial_data = {
    #         # 'aadhar_doc': document_obj.aadhar_doc, 
    #         # 'pan_doc' : document_obj.pan_doc,
    #         # 'dl_doc' : document_obj.dl_doc ,
    #         # 'ssc_doc' : document_obj.ssc_doc, 
    #         # 'hsc_doc' : document_obj.hsc_doc ,
    #         # 'graduate_doc' : document_obj.graduate_doc,
    #         # }
    #         document_obj = Document_Candidate.objects.filter(candidate_id = candidate_profile.id).update(aadhar_doc=aadhar_doc,pan_doc=pan_doc,dl_doc=dl_doc,ssc_doc=ssc_doc,hsc_doc=hsc_doc,graduate_doc=graduate_doc)
    #         # document_obj.save()
            
    #         return render(request,'upload_documents.html')
    #         # context = document_obj.to_dict(orient = 'record')
    #     except Exception as e:    
    #     # print('document',  document_obj.save())
    #         print(e)
    #         print("form not valid")
    #         messages.error(request, 'Something went wrong. Please try again.')
    #     # return render(request,'upload_documents.html')

    # else:
    #     initial_data = {
    #         'aadhar_doc': document_obj.aadhar_doc, 
    #         'pan_doc' : document_obj.pan_doc,
    #         'dl_doc' : document_obj.dl_doc ,
    #         'ssc_doc' : document_obj.ssc_doc, 
    #         'hsc_doc' : document_obj.hsc_doc ,
    #         'graduate_doc' : document_obj.graduate_doc,
    #     }
    #     # form = DocumentForm()
        
    # context = {
    #     'document_obj' : document_obj,
    #     'initial' : initial_data,
    # }
    # return render(request,'upload_documents.html',context)

def sonata_online_exam(request,refId):
    context={}
    if refId is not None:
        # refId decoding here
        testschedule_obj=TestSchedule.objects.filter(candidate_id=refId).first()
        # .values().first()
        print(type(testschedule_obj.status))
        if testschedule_obj.status == '0':

            print("(((((99999)))))")
            print(testschedule_obj)
            today_date=date.today()
            if testschedule_obj.exam_date == today_date:
                print("today exam")
                user_profile = User_Details.objects.get(id=refId)
                context['user_profile']=user_profile
                context['refId']=refId
                context['table_id']=testschedule_obj.id
                return render(request,"exam_student_details.html",context)
            elif testschedule_obj.exam_date < today_date:
                # messages.error(request, f"Your Exam Date is ENDED , Your Exam Date is :- {testschedule_obj.exam_date}")
                print("exam date is passed")
                message=f"""Your Exam Date is ENDED , Your Exam Date is :- {testschedule_obj.exam_date} """
                context['message']=message
                context['red']="red"
                print(context)
                return render(request,'show_message_exam.html',context)
            elif testschedule_obj.exam_date > today_date:
                print("time left to start exam")
                today_date_1=datetime.now()
                exam_date_time = str(testschedule_obj.exam_date) + " " + "00:00:00"
                start=today_date_1
                ends = datetime.strptime(exam_date_time, '%Y-%m-%d %H:%M:%S')
                time_left=ends-start
                message=f""" 
                Your Exam Time Not Now, You have some Time left to start the exam. After- '{time_left}'  you can start your Exam."""

                context['message']=message
                context['green']="green"
                return render(request,'show_message_exam.html',context)
            else:
                print("exam else section")
                message=f""" 
                There is Some Techinical Error related to Exam please check after some time."""
        
                context['message']=message
                return render(request,'show_message_exam.html',context)
        else:
           return HttpResponse(f"<h3> not a valid user-{testschedule_obj.status}</h3>")


def online_exam_details(request,refId,tbl_id):
    context={}
    if refId is not None and tbl_id is not None:
        testschedule_obj=TestSchedule.objects.get(id=tbl_id)
        if testschedule_obj.status != '1':
            testschedule_obj.status='1'
            testschedule_obj.save()
            print("Status Changed")

        if testschedule_obj.status=='1':
            context['refId']=refId
            context['tbl_id']=tbl_id
            return render(request,'online_exam_details.html',context)
        
@csrf_exempt
def start_online_exam(request,refId,tbl_id):
    context={}
    context['refId']=refId
    context['tbl_id']=tbl_id
    if request.method=='POST':
       
        # d1=request.POST['d']
        print("list dataaaaaaaaaa")
        # print(d1)
        return True
    else:
        print("else me gaya")
        if refId is not None and tbl_id is not None:
            testschedule_obj=TestSchedule.objects.get(id=tbl_id)
            if testschedule_obj.status != '2':
                testschedule_obj.status='2'
                testschedule_obj.save()
                print("Status Changed")
            if testschedule_obj.status == '2':
                sheet_id=testschedule_obj.sheet_id
                print(sheet_id,"sheet_id")
                question=question_sheet.objects.filter(sheet_id=sheet_id)
                # print(question.values())
                context['question']=question
                question_id_list=[]
                for i in question:
                    question_id_list.append(i.question_id)
                context['question_id_list']=question_id_list
                print(question_id_list)
                return render(request,'question_sheet.html',context)


@login_required(login_url='signIn')
def offline_test_details(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    query = """
        SELECT 
            cd.name, 
            cd.email, 
            cd.mobile_no, 
            cd.id as candidate_id, 
            ts.application_id
            
        FROM test_schedule ts
        LEFT JOIN candidate_details cd ON ts.candidate_id = cd.id 
        WHERE ts.is_online = 0 and ts.test_status = 0
    """
    
    df = pd.read_sql(query, engine)
    print(df, "data")
    data_list = df.to_dict(orient='records')
    print(data_list)
    
    applicants= TestScheduleDetails.objects.filter(is_online = False).values_list('application_id', flat=True)
    print("Applicants:", applicants)

    candidate = candidate_details.objects.all()
    
    generated_urls = []
    for application_id in applicants:
        url = reverse('update_test_score', kwargs={'refId': application_id})
        generated_urls.append(url)

    print("Generated URLs:", generated_urls)
    
    
    context = {
        'applicants': applicants,
        'candidates': candidate,
        'data_list': data_list,
        'is_hr':is_hr ,'is_hrhead':is_hrhead,
    }
    
    return render(request, 'offline_test_details.html',context)


@login_required(login_url='signIn')
def update_test_score(request, refId=None):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
        
    id=refId
    if id:
        instance = TestScheduleDetails.objects.filter(application_id=id, is_online=False).first()
        applicant = ApplicationDetails.objects.get(application_id = instance.application_id)
    else:
        instance = None
        applicant = None
    
    if request.method == 'POST':
        if instance is not None:
            try:
                instance.test_score = request.POST['score']
                print('score',instance.test_score)
                            
                file_name = request.FILES['offline_answersheet'].name
                file_extension = os.path.splitext(file_name)[1]

                if file_extension.lower() == '.pdf':
                    instance.mime_type = 'application/pdf'
                elif file_extension.lower() in ['.jpg', '.jpeg', '.png']:
                    instance.mime_type = 'image/'+file_extension.lower()[1:]
                else:
                    instance.mime_type = 'unknown'
                instance.offline_answersheet = request.FILES['offline_answersheet'].read()

                print('file',instance.offline_answersheet)
                instance.test_status = 3
                print('status',instance.test_status)
                instance.save()
                application = ApplicationDetails.objects.get(application_id = instance.application_id)
                application.application_status = 4
                application.save()
                messages.success(request, "Score updated successfully")
                return redirect('schedule_online_test')
            except Exception as e:
                print(e)
                messages.error(request, "Something went wrong")
                return redirect('schedule_online_test')
    else:
        candidate = candidate_details.objects.filter(id=instance.candidate_id).first()
        
    try:
        resume_obj = ResumeFiles.objects.get(candidate_id = candidate.id)
        resume = resume_obj.resume
        mime_type = resume_obj.mime_type
        encoded_data = base64.b64encode(resume).decode('utf-8')
    except Exception as e :
        print(e)
        encoded_data = None
        mime_type = None
        
    try:
        document_obj = Document_Candidate.objects.get(candidate_id = candidate.id)
        aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
        pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
        dl_doc = document_obj.dl_doc if document_obj.dl_doc else None
    except Exception as e:
        aadhar_doc = None
        pan_doc = None
        dl_doc = None
        
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    context = {'user_profile':candidate,
                'status':candidate.status,
                'test':instance,
                'binary_data':encoded_data,
                'mime_type':mime_type,
                'gender_choices':GENDER,
                'application':applicant,
                'candidate_id': candidate.id,
                'aadhar_doc' : aadhar_doc,
                'pan_doc' : pan_doc,
                'dl_doc' : dl_doc,
                'is_hr':is_hr ,'is_hrhead':is_hrhead,
                }
    return render(request, 'update_test_score.html',context)

from django.db.models import Sum
@login_required(login_url='signIn')
def Onboarding_candidates(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    query = """
        SELECT 
            cd.name, 
            cd.email, 
            cd.mobile_no, 
            cd.id as candidate_id, 
            ad.application_id,
            ad.position_shortlisted_for,
            ad.branch_shortlisted_for
            
        FROM application_details ad 
        LEFT JOIN candidate_details cd ON ad.candidate_id = cd.id 
        WHERE ad.application_status = 7
    """
    # query1 ="""
    #         SELECT application_id , SUM(score) score
    #         FROM INTERVIEW_RESPONSE
    #         where application_id = {app_id}
    #         GROUP BY application_id    
    # """
    
    
    df = pd.read_sql(query, engine)
    print(df, "data")
    # df['application_id'] = df['application_id'].astype('int')
    # app_id =  df['application_id']
    # print('............',  app_id) 
    data_list = df.to_dict(orient='records')
    print(data_list)
    
   
    # df = pd.read_sql(query1, engine)
    # df['score'] = df['score'].astype('int')
    # score1 = df['score']
    # print('scoreeee', score1)
    
    # value = InterviewResponse.objects.filter(application_id=app_id).aggregate(total1=Sum('score'))['total1']
    # print('value' , value)
    applicants = ApplicationDetails.objects.filter(application_status=7)
    candidate = candidate_details.objects.all()  
    distinct_positions_queryset = applicants.values_list("position_shortlisted_for", flat=True).distinct()
    distinct_positions = [position for position in distinct_positions_queryset if position is not None]
    print(distinct_positions)
    context = {
        'applicants': applicants,
        'candidates': candidate,
        'distinct_positions': distinct_positions,
        'data_list': data_list,
        'is_hr':is_hr ,'is_hrhead':is_hrhead,
    }
   
    return render(request, 'Onboarding_candidates.html', context)

@csrf_exempt
def api_onboarding_filter(request):
    if request.method == 'POST':
        selected_position = request.POST.get('position', None)
        selected_branch = request.POST.get('branch', None)

        applicants = User_Details.objects.filter(status=7)

        if selected_position and selected_position != "None":
            applicants = applicants.filter(position_shortlisted_for=selected_position)

        if selected_branch and selected_branch != "None":
            applicants = applicants.filter(branch_shortlisted_for=selected_branch)

        applicants = applicants.order_by('-id').values(
            'id', 'name', 'email', 'mobile_no', 'position_shortlisted_for', 'branch_shortlisted_for'
        )

        data = list(applicants)

        return JsonResponse(data, safe=False)
    
def get_branch_onboarding_options(request):
    if request.method == 'GET':
        selected_position = request.GET.get('position', None)
        if selected_position is None:
            # Handle the case when no position is selected
            return JsonResponse({'branch_options': []})
        else:
            # Fetch branch options based on the selected position
            branch_options = User_Details.objects.filter(position_shortlisted_for=selected_position, status=7).values_list('branch_shortlisted_for', flat=True).distinct()
            print(branch_options)
            return JsonResponse({'branch_options': list(branch_options)})

@login_required(login_url='signIn')
def shortlist_candidates(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    sql_query = """
                SELECT vacancy_id FROM "APPLICATION_DETAILS" AD  
            LEFT JOIN "INTERVIEW_DETAILS" ID 
            ON AD.interview_id = ID.interview_id
            WHERE AD.application_status=6
            AND ID.vacancy_id IS NOT NULL"""
    
    df = pd.read_sql(sql_query, engine)
    vacancy_list = df['vacancy_id'].tolist()
    vacancies = VacancyDetails.objects.filter(vacancy_id__in=vacancy_list)
    distinct_positions_queryset = vacancies.values_list("role", flat=True).distinct()
    distinct_positions = [position for position in distinct_positions_queryset if position is not None]

    return render(request, 'shortlist_candidates.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'rows':vacancies, 'distinct_positions':distinct_positions})

def get_branch_shortlist_options(request):
    if request.method == 'GET':
        selected_position = request.GET.get('position', None)
        if selected_position is None:
            # Handle the case when no position is selected
            return JsonResponse({'branch_options': []})
        else:
            # Fetch branch options based on the selected position
            branch_options = vacancy.objects.filter(job_role=selected_position).values_list('branch_name', flat=True).distinct()
            print(branch_options)
            return JsonResponse({'branch_options': list(branch_options)})

@csrf_exempt
def api_shortlist_filter(request):
    if request.method == 'POST':
        selected_position = request.POST.get('position', None)
        selected_branch = request.POST.get('branch', None)

        vacancy_details = vacancy.objects.all()

        if selected_position and selected_position != "None":
            vacancy_details = vacancy_details.filter(job_role=selected_position)

        if selected_branch and selected_branch != "None":
            vacancy_details = vacancy_details.filter(branch_name=selected_branch)

        rows=[]
        for vacancy_obj in vacancy_details:
            assessed_candidates_count = User_Details.objects.filter(vacancy_id = vacancy_obj.id,status=6).count()
            row = {
                'vacancy_id': vacancy_obj.id,
                'vacancy_branch_name': vacancy_obj.branch_name,
                'vacancy_job_role': vacancy_obj.job_role,
                'no_of_vacancies': vacancy_obj.no_of_vacancies,
                'assessed_candidates_count': assessed_candidates_count
            }
            rows.append(row)
        print(rows)

        return JsonResponse(rows, safe=False)

@login_required(login_url='signIn')
def assessed_candidates_details(request,id=None):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    sql_query= """
                SELECT * FROM "candidate_details" CD
            LEFT JOIN "APPLICATION_DETAILS" AD
            ON AD.candidate_id = CD.id
            LEFT JOIN "INTERVIEW_DETAILS" ID
            ON ID.interview_id = AD.interview_id
            WHERE  AD.application_status=6 AND
            AD.interview_id is NOT NULL AND ID.vacancy_id = {id}
            """

    df = pd.read_sql(sql_query.format(id=id), engine)
    applicants = df.to_dict('records')
    rows = []
    for applicant in applicants:
        try:
            applicant_interview = InterviewDetails.objects.filter(vacancy_id = applicant.vacancy_id).first()
            application = ApplicationDetails.objects.filter(interview_id = applicant_interview.interview_id)
            response = InterviewResponse.objects.filter(application_id = application.application_id)
            interview_score = response.score
            print('score----------------',interview_score)
        except Exception as e:
            print(e)
            interview_score = None
        row = {
        'applicant': applicant,
        'interview_score': interview_score,
        
        }
        rows.append(row)
    # print(rows)
    return render(request, 'assessed_candidates_details.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'applicants':rows,'interview_score':interview_score})

@login_required(login_url='signIn')
def assessed_candidate_full_details(request,application_id):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    if application_id is not None:
        print(application_id)
        application = ApplicationDetails.objects.get(application_id=application_id)
        profile = candidate_details.objects.get(id=application.candidate_id)
        interview_score = InterviewResponse.objects.filter(application_id=application.application_id).aggregate(total1=Sum('score'))['total1']
        interview_details = InterviewDetails.objects.filter(interview_id = application.interview_id)
        print('interview_details---' , interview_details)

        try:
            resume_obj = ResumeFiles.objects.get(candidate_id = application.candidate_id)
            resume = resume_obj.resume
            mime_type = resume_obj.mime_type
            encoded_data = base64.b64encode(resume).decode('utf-8')
        except Exception as e :
            print(e)
            encoded_data = None
            mime_type = None    # applicant_interview = Interview.objects.filter(candidate_id = profile.id).first()
            
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = profile.id)
            aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
            ssc_doc = document_obj.ssc_doc if document_obj.ssc_doc else None
            hsc_doc = document_obj.hsc_doc if document_obj.hsc_doc else None
            graduate_doc = document_obj.graduate_doc if document_obj.graduate_doc else None 
            pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
            dl_doc = document_obj.dl_doc if document_obj.dl_doc else None
        except Exception as e:
            aadhar_doc = None
            pan_doc = None
            dl_doc = None
            ssc_doc = None
            hsc_doc = None
            graduate_doc = None

        GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        )
    
    else:
        profile=None
    
    context = {
        'mime_type':mime_type,
        'user_profile':profile,
        'binary_data':encoded_data,
        'status':application.application_status,
        'application':application,
        'gender_choices': GENDER,
        'interview_score':interview_score,
        'interview_details':interview_details,
        'candidate_id': profile.id,
        'aadhar_doc' : aadhar_doc,
        'pan_doc' : pan_doc,
        'dl_doc' : dl_doc,
        'ssc_doc': ssc_doc,
        'hsc_doc': hsc_doc,
        'graduate_doc': graduate_doc,
        'is_hr':is_hr ,'is_hrhead':is_hrhead,
    }  
    return render(request,'assessed_candidate_full_details.html',context)

@login_required(login_url='signIn')
def select_candidate(request,refId=None):
    print(refId)
    if refId:
        applicants_obj = ApplicationDetails.objects.get(application_id=refId)
        applicants_obj.application_status=7
        applicants_obj.checked_by = request.user.id
        applicants_obj.save()
        interview= InterviewDetails.objects.filter(pk=applicants_obj.interview_id).first()
        vacancy_obj = VacancyDetails.objects.get(pk=interview.vacancy_id)
        vacancy_obj.capacity = vacancy_obj.capacity - 1
        vacancy_obj.save()
        
        # if applicants_obj.application_status == 7 :
        # candidate = candidate_details.objects.get(id=applicants_obj.candidate_id)
        # doc_can_id = Document_Candidate.objects.get(candidate_id = candidate.id)    
        # if ((doc_can_id.aadhar_doc != None) | (doc_can_id.pan_doc != None) | (doc_can_id.dl_doc != None)):
        #    print("Documents Uploaded Successfully .")  
        # else:
        try:
            applicants_obj = ApplicationDetails.objects.get(application_id=refId)
            candidate = candidate_details.objects.get(id=applicants_obj.candidate_id)
            doc_can_id = Document_Candidate.objects.get(candidate_id = candidate.id)
            if ((doc_can_id.aadhar_doc == "" or doc_can_id.aadhar_doc == None) | (doc_can_id.pan_doc == "" or doc_can_id.pan_doc == None) | (doc_can_id.dl_doc == "" or doc_can_id.dl_doc == None)):
                applicants_obj.application_status = 7 
                candidate.save()
                applicants_obj.save()
                encoded_id = encode_id(applicants_obj.candidate_id)
                print(encoded_id)
                url = f"https://media.smsgupshup.com/GatewayAPI/rest?userid=2000209909&password=z24gzBUA&send_to={candidate.mobile_no}&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=To+proceed+with+the+application+process%2C+please+update+your+profile+with+necessary+documents%0AReference+ID%3A+{encoded_id}&isTemplate=true&header=Greetings+from+Sonata+Finance"
                print(url)
                payload = {}
                headers = {}
                response = requests.request("GET", url, headers=headers, data=payload)
                print("response.....",response.text)
             #   return redirect('profile_update',candidate_id=candidate.id)
            else:
                pass
        except Exception as e:
               print(e)
             #   messages.error(request, "Please Update your documents first.")
        return redirect("shortlist_candidates")

    return redirect("shortlist_candidates")


def get_scheduled_interview_count_matrix_by_time_slot_and_week(request, user_id=None, date=None):
    user_profile = User_Details.objects.get(id=user_id)
    branch = user_profile.branch_shortlisted_for
    roll = user_profile.position_shortlisted_for
    print(branch, roll)

    time_slots = ['10-12', '12-2', '2-4', '4-6']

    start_date = datetime.now()
    if date:
        start_date = datetime.strptime(date, "%Y-%m-%d")

    start_of_week = start_date - timedelta(days=start_date.weekday())
    dates_of_week = [start_of_week + timedelta(days=i) for i in range(7)]

    candidates = User_Details.objects.filter(
        branch_shortlisted_for=branch,
        position_shortlisted_for=roll,
        interview_date__in=dates_of_week
    ).select_related()

    count_matrix = []

    for date in dates_of_week:
        count_dict = []
        count_dict.append( {'date': date.strftime("%Y-%m-%d")})

        for slot in time_slots:
            count = candidates.filter(interview_date=date, interview_time=slot).count()
            count_dict.append({slot:count})

        count_matrix.append(count_dict)

    return JsonResponse(count_matrix, safe=False)


@csrf_exempt
def get_calender(request):

    print(request.GET)
    date=request.GET.get('date',None)
    interviewer_id=request.GET.get('interviewer_id','')
    time_slots=['10-12','12-2','2-4','4-6']
    print(date,'date---------------------')
    print(interviewer_id,'interviewer_id---------------------')
    start_date = datetime.now()
    if date:
        start_date = datetime.strptime(date, "%Y-%m-%d")

    print(start_date,'start_date')
    start_of_week = start_date - timedelta(days=start_date.weekday())
    dates_of_week = [start_of_week + timedelta(days=i) for i in range(7)]
    print(dates_of_week,'dates_of_week')
    candidates=User_Details.objects.filter(
        Q(interview_date__in=dates_of_week) &
        Q(interview_panel_list__contains=f',{interviewer_id},') |  # Match ID with commas on both sides
        Q(interview_panel_list__startswith=f'{interviewer_id},') |  # Match ID at the beginning
        Q(interview_panel_list__endswith=f',{interviewer_id}')  |# Match ID at the end
        Q(interview_panel_list=f'{interviewer_id}')  # Single ID in the field
        )
    print(candidates.count(),'candidates.count()')
    for candidate in candidates:
        print(candidate.interview_panel_list,'candidate.interview_panel_list')
        print(candidate.interview_date,'candidate.interview_date')
    count_matrix = []
    for date in dates_of_week:
        count_dict = []
        count_dict.append( {'date': date.strftime("%Y-%m-%d")})

        for slot in time_slots:
            count = candidates.filter(interview_date=date, interview_time=slot).count()
            count_dict.append({slot:count})

        count_matrix.append(count_dict)

    return JsonResponse(count_matrix, safe=False)

def heading(request):
    if request.user.is_authenticated:
        print("redirect to dashboard")
        return redirect('dashboard')
    else:
        print("error")
        return redirect('home_page')

from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
import math

@login_required(login_url='signIn')
def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            currentPassword = request.POST.get("currentPassword")
            newPassword = request.POST.get("newPassword")
            confirmPassword = request.POST.get("confirmPassword")
            print(currentPassword, newPassword, confirmPassword)
            if check_password(currentPassword, user.password):
                print("verification complete")
                if newPassword == confirmPassword:
                    # user.password = make_password(newPassword)
                    print("password change request accepted")
                    # messages.success(request, "Successfully Changed Password\n Re-login Now")
                    # user.save()
                    request.session["newPassword"] = newPassword
                    otp = generateOTP()
                    request.session["otp"] = otp
                    subject = "Change Password OTP verification"
                    message = f"Dear {user.username}, Your OTP is: {otp}"
                    from_email = settings.EMAIL_HOST_USER
                    send_mail(subject, message, from_email, [user.email])
                    print("otp", otp, from_email, [user.email])
                    return redirect("verify_otp")
                else:
                    print("Password mismatch")
                    messages.error(request, "Password mismatch")
                    return render(request, "change_password.html")
            else:
                print("wrong old password")
                messages.error(request, "wrong old password")
                return render(request, "change_password.html")
        else:
            return render(request, "change_password.html")

@login_required(login_url='signIn')
def verify_otp(request):
    if request.method == "POST":
        otp_token = request.session.get("otp")
        otp = request.POST.get("otp")
        print(otp,otp_token)

        if str(otp) == str(otp_token):
            newPassword = request.session.get("newPassword")
            print(newPassword)
            user = request.user
            print(user)
            user.password = make_password(newPassword)
            messages.success(request, "Successfully Changed Password\n Re-login Now")
            user.save()
            return redirect("dashboard")
        else:
            messages.error(request, "OTP mismatch")
            return render(request, "verify_otp.html")
    else:
        email = request.user.email
        email_init = email.split('@')[0]
        length = len(email_init)
        email_last = email.split('@')[-1]
        email_final = email[0:3] + (length-3)*'*'+email_last
        return render(request, "verify_otp.html", {'email': email_final})

def upload_cv_render(request):
    return render(request, 'upload_cv.html')

def success_page(request):
    return render(request,'upload_cv')

@login_required(login_url='signIn')
def rejected(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    user_id = request.user.id
    
    sql_query = f'''
        EXEC dbo.dashboard_counter
        '''
    dash_df = pd.read_sql_query(sql_query, engine)
    dash_dict = dash_df.to_dict(orient='records')[0]
    print(dash_dict)
    # context['counts'] = dash_dict
    
    sql_query = f'''
        select count(*) id from "APPLICATION_DETAILS" AD 
        RIGHT JOIN "REJECT_REVIEW_ALLOTMENT" RRA ON AD.application_id = RRA.application_id
        LEFT JOIN "CANDIDATE_DETAILS" CD ON CD.id= AD.candidate_id
        WHERE RRA.is_reviewed=0 or RRA.is_reviewed is NULL  and RRA.alloted_to={user_id}
        '''
    d_df = pd.read_sql_query(sql_query, engine)
    rejected_review_allotment = d_df.to_dict(orient='records')[0]
    print(rejected_review_allotment['id'])
    
    
    sql_query = f'''
        select count(*) id from "APPLICATION_DETAILS" AD 
        RIGHT JOIN "REJECT_REVIEW_ALLOTMENT" RRA ON AD.application_id = RRA.application_id
        LEFT JOIN "CANDIDATE_DETAILS" CD ON CD.id= AD.candidate_id
        WHERE RRA.is_reviewed=1
        '''
    d_df = pd.read_sql_query(sql_query, engine)
    reviewed_rejected_candidates = d_df.to_dict(orient='records')[0]
    print(rejected_review_allotment['id'])
    
    context={
        'username': request.user.username,
        'rejected_review_allotment_count':rejected_review_allotment,
        'reviewed_rejected_candidates_count':reviewed_rejected_candidates,
        'counts' :dash_dict,
        'is_hr':is_hr ,'is_hrhead':is_hrhead,
    }
    
    return render(request, "rejected_hr_dashboard.html", context)

@login_required(login_url='signIn')
def exam_snapshot_dashboard(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    query = """
        SELECT 
            cd.name, 
            cd.email, 
            cd.mobile_no, 
            cd.id as candidate_id, 
            ts.application_id
            
        FROM test_schedule ts
        LEFT JOIN candidate_details cd ON ts.candidate_id = cd.id 
        WHERE ts.is_online = 1
    """
    
    df = pd.read_sql(query, engine)
    print(df, "data")
    data_list = df.to_dict(orient='records')
    print(data_list)
    
    applicants= TestScheduleDetails.objects.filter(is_online = True).values_list('application_id', flat=True)
    print("Applicants:", applicants)

    candidate = candidate_details.objects.all()
    
    generated_urls = []
    for application_id in applicants:
        url = reverse('exam_user_full_details', kwargs={'refId': application_id})
        generated_urls.append(url)

    print("Generated URLs:", generated_urls)
    
    context = {
        'applicants': applicants,
        'candidates': candidate,
        'data_list': data_list,
        'is_hr':is_hr ,'is_hrhead':is_hrhead,
    }
    return render(request, "exam_user_details.html",context)

@login_required(login_url="signIn")
def exam_user_full_details(request, refId):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    print(refId)
    profile = ApplicationDetails.objects.get(application_id=refId)
    print(profile)
    if refId is not None:   
        candidate = candidate_details.objects.get(id=profile.candidate_id)
        print(candidate)
        # pics = Candidate_Camshot.objects.filter(candidate_id = refId).first
        # print(pics)
        # pics.camshot_base64 = base64.b64encode(pics.camshot).decode('utf-8')
        camshots = Candidate_Camshot.objects.filter(application_id=profile.application_id)
        print(camshots)
        pics = []
        row=[]
        for picture in camshots:
            picture.camshot_base64 = base64.b64encode(picture.camshot).decode('utf-8')
            row.append(picture.camshot_base64)
            print(row)
            pics.append(row[0])
            row.pop(0)
        try:
            resume_obj = ResumeFiles.objects.get(candidate_id = candidate.id)
            print(resume_obj)
            resume = resume_obj.resume
            mime_type = resume_obj.mime_type
            encoded_data = base64.b64encode(resume).decode('utf-8')
        except Exception as e :
            print(e)
            encoded_data = None
            mime_type = None
        
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = candidate.id)
            aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
            pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
            dl_doc = document_obj.dl_doc if document_obj.dl_doc else None
        except Exception as e:
            aadhar_doc = None
            pan_doc = None
            dl_doc = None
            
        GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        )
    else:
        candidate = None
    
    context = {
        'mime_type':mime_type,
        'user_profile':profile,
        'binary_data':encoded_data,
        'status':profile.application_status,
        'camshot':row,'pics': pics, 
        'candidate':candidate,
        'gender_choices': GENDER,
        # 'candidate_id': profile.id,
        'aadhar_doc' : aadhar_doc,
        'pan_doc' : pan_doc,
        'dl_doc' : dl_doc,
        'is_hr':is_hr ,'is_hrhead':is_hrhead,
        }
    return render(request, "exam_user_full_details.html", context)

def generate_activation_key():
    chars = string.ascii_letters + string.digits
    activation_key = ''.join(random.choice(chars) for _ in range(25))
    return activation_key

def forget_password_send_otp(request):
    if request.method == "POST":
        username = request.POST.get('username')
        user = User.objects.filter(username = username).first()
        forgot = Forgot_Password_Table.objects.create()
        forgot.username = username
        print(user)
        if user is not None:
            global key
            global session_username
            request.session['username'] = username           
            reset_key = generate_activation_key()
            request.session['reset_key'] = reset_key            
            print('session key ----------',request.session['reset_key'])
            forgot.reset_key = reset_key
            forgot.save()
            reset_link = f"http://localhost:8000/forget_password_verify_otp/{reset_key}"
            message = f"Dear {username}, Your Forget Password link is: {reset_link}"
            from_email = settings.EMAIL_HOST_USER
            send_mail("Forget Password Mail", message, from_email, [user.email])
            print("Forget Password Mail", message, from_email, [user.email])
       
            messages.success(request, "Email Sended")
            return render(request, "Sign-In.html",{'pk':0})
        else:
            print("No user is registered with this username")
            messages.error(request, "No user is registered with this username")
            return render(request,"forget_password_send_otp.html")
    return render(request,"forget_password_send_otp.html")

def forget_password_verify_otp(request,reset_key):
    if request.method == "POST":
        otp_token = request.session.get('reset_key',reset_key)
        otp = Forgot_Password_Table.objects.get(reset_key=otp_token)
        print(reset_key, otp_token)
        if str(reset_key) == str(otp_token):
            password_1 = request.POST.get('password_1')
            password_2 = request.POST.get('password_2')
            if str(password_1) == str(password_2):
                # username = request.session.get('username')
                # print(username)
                user = User.objects.filter(username = otp.username).first()
                print("username...", user)
                user.password = make_password(password_1)
                user.save()
                messages.success(request, "Password Reset Successfully")
                return redirect('signIn')
            else:
                print("password_mismatched")
                messages.error(request, "Password Mismatched")
                return render(request,"forget_password_verify_otp.html")
        else:
            print("wrong Link")
            messages.error(request, "Verification Failed")
            return render(request,"forget_password_verify_otp.html")
    return render(request,"forget_password_verify_otp.html")

def reschedule_interview_user(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    sql_query = f'''SELECT a.*, c.name, c.email, c.mobile_no, i.interview_date, c.id 
    FROM Sonata_ConnectHR.dbo.APPLICATION_DETAILS a
    JOIN Sonata_ConnectHR.dbo.INTERVIEW_DETAILS i ON a.interview_id = i.interview_id
    JOIN Sonata_ConnectHR.dbo.CANDIDATE_DETAILS c ON a.candidate_id = c.id
    WHERE CAST(i.interview_date AS DATE) < CAST(GETDATE() AS DATE);'''
    df = pd.read_sql_query(sql_query, engine)
    applicants = df.to_dict(orient='records')
    return render(request, 'reschedule_user_details.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'applicants':applicants})

@csrf_exempt
def api_reschedule_interviews(request):
    if request.method == 'POST':
        from_date_str = request.POST['from_date']
        to_date_str = request.POST['to_date']
        print(from_date_str, to_date_str)

        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

        # Filter the applicants queryset based on the date range (strictly less than to_date)
        applicants = User_Details.objects.filter(status=5, interview_date__lt=to_date, interview_date__gte=from_date).order_by("interview_date")

         # Convert queryset data to a list of dictionaries
        data = [{'id': x.id, 'name': x.name, 'email': x.email, 'mobile_no': x.mobile_no, 'interview_date': x.interview_date.strftime('%Y-%m-%d')} for x in applicants]

        # Return the queryset data as JSON response
        return JsonResponse(data, safe=False)

@csrf_exempt
def api_exam_snapshot(request):
    if request.method == 'POST':
        from_date_str = request.POST['from_date']
        to_date_str = request.POST['to_date']
        selected_position = request.POST['position']
        selected_branch = request.POST['branch']

        if selected_position == "None":
            print("done")
            selected_position = None;
        
        if selected_branch == "None":
            print("done")
            selected_branch = None;

        print(from_date_str, to_date_str, selected_position, selected_branch)

        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

        candidate_ids = TestSchedule.objects.filter(exam_date__lt=to_date, exam_date__gte=from_date).values('candidate_id').distinct()
        if selected_position is not None:
            if selected_branch is not None:
                user_details = User_Details.objects.filter(
                    status__gte=4,
                    id__in=candidate_ids,
                    position_shortlisted_for=selected_position,
                    branch_shortlisted_for=selected_branch
                ).values('id', 'name', 'email', 'mobile_no')
            else:
                user_details = User_Details.objects.filter(
                    status__gte=4,
                    id__in=candidate_ids,
                    position_shortlisted_for=selected_position
                ).values('id', 'name', 'email', 'mobile_no')
        else:
            user_details = User_Details.objects.filter(
                status__gte=4,
                id__in=candidate_ids
            ).values('id', 'name', 'email', 'mobile_no')

        data = list(user_details)

        return JsonResponse(data, safe=False)
    
def get_branch_options(request):
    if request.method == 'GET':
        selected_position = request.GET.get('position', None)
        if selected_position is None:
            # Handle the case when no position is selected
            return JsonResponse({'branch_options': []})
        else:
            # Fetch branch options based on the selected position
            branch_options = User_Details.objects.filter(position_shortlisted_for=selected_position, status__gte=4).values_list('branch_shortlisted_for', flat=True).distinct()
            print(branch_options)
            return JsonResponse({'branch_options': list(branch_options)})
        
def unauthorized(request):
    return render(request, 'unauthorized.html')

@csrf_exempt
def api_vacancy_filter(request):
    if request.method == 'POST':
        selected_position = request.POST.get('position', None)
        selected_branch = request.POST.get('branch', None)

        vacancy_details = VacancyDetails.objects.all()

        if selected_position and selected_position != "None":
            vacancy_details = vacancy_details.filter(job_role=selected_position)

        if selected_branch and selected_branch != "None":
            vacancy_details = vacancy_details.filter(branch_name=selected_branch)

        vacancy_details = vacancy_details.order_by('-id').values(
            'id', 'job_role', 'branch_name', 'no_of_vacancies',
            'qualification_type', 'salary', 'required_experience', 'required_skills', 'posted_on'
        )

        data = list(vacancy_details)
        print(data)

        return JsonResponse(data, safe=False)

@login_required(login_url='signIn')
def applied_vacancy(request, email):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    candidates_details = candidate_details.objects.get(email=email)
    data=[]
    
    interview_ids = ApplicationDetails.objects.filter(candidate_id=candidates_details.id).values("interview_id").distinct()
    print('interviw ids', interview_ids)
    distinct_vacancy_ids = InterviewDetails.objects.filter(interview_id__in=interview_ids).filter(interview_date__gte=(datetime.now() - relativedelta(days=1))).values("vacancy_id").distinct()
    
    vacancy = VacancyDetails.objects.filter(vacancy_id__in=distinct_vacancy_ids)
    print(vacancy, 'dwdaw')
    # vacancy_idlist = InterviewDetails.objects.filter(interview_date__gte=(datetime.now() - relativedelta(days=1))).values_list('vacancy_id')
    # vacancy = VacancyDetails.objects.filter(vacancy_id__in = vacancy_idlist)
    for i in vacancy:
        d = {}
        d['id']=i.vacancy_id
        d['branch_name']=i.branch if i.branch else "-"
        d['required_skills']=i.required_skills.split(",") if i.required_skills else []
        d['job_role']=i.role if i.role else "-"
        d['no_of_vacancies']=i.capacity if i.capacity else "-"
        d['qualification_type']=i.qualification if i.qualification else "-"
        d['required_experience']=i.required_experience if i.required_experience else "-"
        d['salary']=int(i.salary) if int(i.salary) else "-"
        d['vacancy_date']=i.vacancy_date if i.vacancy_date else "-"
        data.append(d)
    
    print(vacancy)
    print('---------------------', data)
    return render(request, 'application_status.html', {"vacancies": data,'is_hr':is_hr ,'is_hrhead':is_hrhead})

@login_required(login_url='signIn')
def apply_for_vacancy(request, id):
    email=request.user.email
    candidate = candidate_details.objects.get(email=email)
    vacancy = VacancyDetails.objects.get(vacancy_id = id)
    interview = InterviewDetails.objects.get(vacancy_id =id)
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    context = {'user_profile':candidate, 'gender_choices': GENDER}

    if candidate.status==1:
        print("TRUE")
        application = ApplicationDetails()
        application.interview_id = interview.interview_id
        application.candidate_id = candidate.id
        application.position_shortlisted_for = vacancy.role
        application.branch_shortlisted_for = vacancy.branch
        application.application_status = 2
        application.save()
        
        # doc = Document_Candidate()
        # doc.candidate_id = candidate.id
        # doc.save()
        messages.success(request, "Applied Successfully!")
        return redirect('dashboard')

    else:
        print("FALSE")
        messages.error(request, "Please Update your profile first.")
        return redirect('profile_update',candidate_id=candidate.id)

@login_required(login_url='signIn')
def view_application(request, id):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    vacancy = VacancyDetails.objects.get(vacancy_id = id)
    interview = InterviewDetails.objects.get(vacancy_id=id)
    user_id=request.user.email
    candidate = candidate_details.objects.get(email=user_id)
    application = ApplicationDetails.objects.get(candidate_id=candidate.id, interview_id=interview.interview_id)
    return render(request, 'view_application.html', {'is_hr':is_hr ,'is_hrhead':is_hrhead,'vacancy': vacancy, 'candidate':candidate, 'status':application.application_status})


def rejected_applications(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    sql_query = """
        select * from "APPLICATION_DETAILS" AD 
        LEFT JOIN "CANDIDATE_DETAILS" CD ON CD.id= AD.candidate_id
        WHERE AD.application_status = 12 
        """
    rejected_application_df = pd.read_sql_query(sql_query, connection)

    rejected_application_dict= rejected_application_df.to_dict('records')
    
    print('-----------------',rejected_application_dict)
    
    rows = []
    for applicant in rejected_application_dict:
        print("applicant ...", applicant['application_id'])
        try:
            rejected_review_allotment= RejectReviewAllotment()
            rejected_review_allotment.application_id = applicant['application_id']
            rejected_review_allotment.save()
        except Exception as e:
            print("Sachin ",e)
            
        row = {
            'applicant': applicant,
            }
        rows.append(row)

    return render(request, 'rejected_applications.html', {'is_hr':is_hr ,'is_hrhead':is_hrhead,'data':rejected_application_dict, 'count':len(rejected_application_dict),'applicant':rows})

def rejected_application(request,application_id):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    print ("application_id---------",application_id )
    
    application = ApplicationDetails.objects.get(application_id=application_id)
    print('application-------------',application)
    
    profile = candidate_details.objects.get(id=application.candidate_id)
    print('profile-----------',profile)
    hr_users = User_Rolls.objects.filter(roll_id=1).values_list('user_id', flat=True)
    print('hr_user--------',hr_users)
    hr_users = User.objects.filter(id__in=hr_users).exclude(id=application.checked_by)
    print('hr_users')

    current_user_roll= User_Rolls.objects.get(user_id=request.user.id)

    is_hr_head = True if current_user_roll.roll_id == 3 else False
    if request.method == 'POST':
        print(request.POST)
        hr_user_id= request.POST.get('hr_id')
        rejected_review_allotment= RejectReviewAllotment.objects.get(application_id=application_id)
        rejected_review_allotment.alloted_to=int(hr_user_id)
        rejected_review_allotment.save()
        return redirect('rejected_applications')
    

    if application_id is not None:
        profile = candidate_details.objects.get(id=application.candidate_id)
        try:
            resume_obj = ResumeFiles.objects.get(candidate_id = profile.id)
            resume = resume_obj.resume
            mime_type = resume_obj.mime_type
            encoded_data = base64.b64encode(resume).decode('utf-8')
        except Exception as e :
            print(e)
            encoded_data = None
            mime_type = None
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = profile.id)
            aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
            pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
            dl_doc = document_obj.dl_doc if document_obj.dl_doc else None
        except Exception as e:
            aadhar_doc = None
            pan_doc = None
            dl_doc = None
    else:
        profile = None
    
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    
    context = {'user_profile':profile,
               'application':application,
               'hr_users':hr_users,
               'status':profile.status,
               'binary_data':encoded_data,
               'mime_type':mime_type,
               'is_hr_head':is_hr_head,
               'gender_choices':GENDER,
               'candidate_id': profile.id,
               'aadhar_doc' : aadhar_doc,
               'pan_doc' : pan_doc,
               'dl_doc' : dl_doc,
               'is_hr':is_hr ,'is_hrhead':is_hrhead,
               }
    return render(request,'rejected_user_full_detail.html', context)


@login_required(login_url='signIn')
def alloted_applications(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    sql_query = f"""
        select * from "APPLICATION_DETAILS" AD 
        RIGHT JOIN "REJECT_REVIEW_ALLOTMENT" RRA ON AD.application_id = RRA.application_id
        LEFT JOIN "CANDIDATE_DETAILS" CD ON CD.id= AD.candidate_id
        WHERE RRA.is_reviewed=0 or RRA.is_reviewed is NULL  and RRA.alloted_to={request.user.id}
        """
    
    print(request.user.id,"request.user.id")
    rejected_application_df = pd.read_sql_query(sql_query, connection)

    rejected_application_dict= rejected_application_df.to_dict('records')
    return render(request, 'review_alloted_applications.html', {'is_hr':is_hr ,'is_hrhead':is_hrhead,'data':rejected_application_dict, 'count':len(rejected_application_dict)})


@login_required(login_url='signIn')
def alloted_application(request,application_id):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    if request.method == 'POST':
        result = request.POST.get('review')
        remarks = request.POST.get('remarks')

        review_mode= RejectReviewAllotment.objects.get(application_id=application_id)
        review_mode.is_reviewed=1
        review_mode.result=True if  result=="right" else False
        review_mode.remark=remarks
        review_mode.save()
        return redirect('alloted_applications')

    application = ApplicationDetails.objects.get(application_id=application_id)

    reviewer_name = User.objects.filter(id = application.checked_by)
    profile = candidate_details.objects.get(id=application.candidate_id)
    hr_users = User_Rolls.objects.filter(roll_id=1).values_list('user_id', flat=True)
    hr_users_names = User.objects.filter(id__in=hr_users).values_list('username', flat=True)
    
    if application_id is not None:
        profile = candidate_details.objects.get(id=application.candidate_id)
        try:
            resume_obj = ResumeFiles.objects.get(candidate_id = profile.id)
            resume = resume_obj.resume
            mime_type = resume_obj.mime_type
            encoded_data = base64.b64encode(resume).decode('utf-8')
        except Exception as e :
            print(e)
            encoded_data = None
            mime_type = None
            
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = profile.id)
            aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
            ssc_doc = document_obj.ssc_doc if document_obj.ssc_doc else None
            hsc_doc = document_obj.hsc_doc if document_obj.hsc_doc else None
            graduate_doc = document_obj.graduate_doc if document_obj.graduate_doc else None 
            pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
            dl_doc = document_obj.dl_doc if document_obj.dl_doc else None
        except Exception as e:
            aadhar_doc = None
            pan_doc = None
            dl_doc = None
            ssc_doc = None
            hsc_doc = None
            graduate_doc = None
    else:
        profile = None
    
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    
    context = {'user_profile':profile,
               'application':application,
               'hr_usernames':hr_users_names,
               'status':profile.status,
               'binary_data':encoded_data,
               'mime_type':mime_type,
               'reviewer_name':reviewer_name,
               'gender_choices':GENDER,
               'candidate_id': profile.id,
               'aadhar_doc' : aadhar_doc,
               'pan_doc' : pan_doc,
               'dl_doc' : dl_doc,
               'ssc_doc': ssc_doc,
               'hsc_doc': hsc_doc,
               'graduate_doc': graduate_doc,
               'is_hr':is_hr ,'is_hrhead':is_hrhead,
               }
    return render(request,'alloted_user_full_detail.html', context)

@login_required(login_url='signIn')
def reviewed_applications(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    sql_query = f"""
        select * from "APPLICATION_DETAILS" AD 
        RIGHT JOIN "REJECT_REVIEW_ALLOTMENT" RRA ON AD.application_id = RRA.application_id
        LEFT JOIN "CANDIDATE_DETAILS" CD ON CD.id= AD.candidate_id
        WHERE RRA.is_reviewed=1;
        """
    
    print(request.user.id,"request.user.id")
    rejected_application_df = pd.read_sql_query(sql_query, connection)
    rejected_application_dict= rejected_application_df.to_dict('records')
    return render(request, 'reviewed_applications.html', {'is_hr':is_hr ,'is_hrhead':is_hrhead,'data':rejected_application_dict, 'count':len(rejected_application_dict)})

@login_required(login_url='signIn')
def reviewed_application(request,application_id):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    application = ApplicationDetails.objects.get(application_id=application_id)
    profile = candidate_details.objects.get(id=application.candidate_id)
    RRA = RejectReviewAllotment.objects.get(application_id=application_id)
    rejected_user= User.objects.get(id=application.checked_by)
    reviewed_user= User.objects.get(id=RRA.alloted_to)
   
    if application_id is not None:
        profile = candidate_details.objects.get(id=application.candidate_id)
        try:
            resume_obj = ResumeFiles.objects.get(candidate_id = profile.id)
            resume = resume_obj.resume
            mime_type = resume_obj.mime_type
            encoded_data = base64.b64encode(resume).decode('utf-8')
        except Exception as e :
            print(e)
            encoded_data = None
            mime_type = None
        try:
            document_obj = Document_Candidate.objects.get(candidate_id = profile.id)
            aadhar_doc = document_obj.aadhar_doc if document_obj.aadhar_doc else None
            pan_doc = document_obj.pan_doc if document_obj.pan_doc else None
            dl_doc = document_obj.dl_doc if document_obj.dl_doc else None
        except Exception as e:
            aadhar_doc = None
            pan_doc = None
            dl_doc = None
    else:
        profile = None
    
    GENDER = (
        ('Male','Male'),
        ('Female','Female'),
    )
    context = {'user_profile':profile,
               'application':application,
               'status':profile.status,
               'binary_data':encoded_data,
               'mime_type':mime_type,
               'reviewd_user':reviewed_user,
               'rejected_user':rejected_user,
               'gender_choices':GENDER,
               'candidate_id': profile.id,
               'aadhar_doc' : aadhar_doc,
               'pan_doc' : pan_doc,
               'dl_doc' : dl_doc,
               'is_hr':is_hr ,'is_hrhead':is_hrhead,
               }
    return render(request,'reviewed_user_full_details.html', context)

def Contact_Us_Page(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')
        message = request.POST.get('message')
        contact_data = ContactUsTable.objects.create(name=name, email=email,mobile_no=mobile_no,message=message)
        contact_data.save()
        print(contact_data)
        
        return redirect('home_page')
    else:
        return render(request,'contact_us_page.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead})


def show_contact(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    contact = ContactUsTable.objects.all()
    print("contact", contact)
    return render(request,'contact_us_full_details.html',{'is_hr':is_hr ,'is_hrhead':is_hrhead,'contact':contact})


def indexCopy(request):
    is_hr=False
    is_hrhead = False
    if str(request.user) != 'AnonymousUser':
        user_id=request.user.id
        try:
            user_roll=User_Rolls.objects.get(user_id=user_id)
            is_hr=True if user_roll.roll_id==1 else False
            is_hrhead=True if user_roll.roll_id==3 else False
        except:
            pass
    context={}
    username=request.user.username
    context['username']=username
    context['is_hr'] = is_hr
    context['is_hrhead'] = is_hrhead
    return render(request, 'index copy.html',context)


from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
def verifyDocument(request, refId):
    if refId:
        try:
            application = ApplicationDetails.objects.get(application_id=refId)
        except ApplicationDetails.DoesNotExist:
            raise Http404("ApplicationDetails not found")
        profile = get_object_or_404(ApplicationDetails, application_id=refId)
        document_obj, created = Document_Candidate.objects.get_or_create(candidate_id=application.candidate_id)
        
        if request.method == 'POST' and 'verify' in request.POST:
            verify = request.POST.get('verify', None)
            print('verify', verify)
            
            if verify:
                document_obj.verify = verify
                document_obj.save()
            
    return redirect('schedule_test_user_full_details', refId=refId)



from django.template.loader import get_template

from xhtml2pdf import pisa

def pdf(request ,refId):
    # products = Product.objects.all()
    
    profile = candidate_details.objects.get(id = refId)
    application_obj = ApplicationDetails.objects.get(candidate_id = profile.id)
    interview_obj = InterviewDetails.objects.get(interview_id = application_obj.interview_id)
    offerletter_obj =  OfferLetter.objects.get(candidate_id = application_obj.candidate_id)
    template_path = 'pdf.html'

    context = {'profile':profile,
               'interview_obj':interview_obj,
               'offerletter_obj': offerletter_obj}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="products_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from openpyxl import Workbook
from openpyxl.styles import *
import decimal

def is_valid_queryparam(param):
    return param != '' and param is not None

def candidate_list(request):
    # cd = candidate_details.objects.all().order_by('name')
    
    sql_query = f"""
        SELECT CD.name,CD.email,CD.mobile_no,AD.branch_shortlisted_for,AD.position_shortlisted_for,AD.application_status FROM CANDIDATE_DETAILS AS CD
        LEFT JOIN APPLICATION_DETAILS AS AD
        ON AD.candidate_id = CD.id;
        """
    
    df = pd.read_sql(sql_query, engine)
    
    data_list = df.to_dict(orient='records')
    
    application_status = request.POST.get('application_status')
   
    
    request.session['application_status'] = application_status

    
    if is_valid_queryparam(application_status):
        data_list = [data for data in data_list if data.get(application_status) == application_status]

    
        
    page = request.POST.get('page',1)
    paginator = Paginator(data_list,40)
    
    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
        
    context = {
        'candidate_list' : data_list,
        'application_status' : application_status,
    }
    return render(request, 'reports.html', context)

def set_header_style(header):
    header.fill = PatternFill("solid", fgColor="246ba1")
    header.font = Font(bold=True, color="F7F6FA")
    header.alignment = Alignment(horizontal="center", vertical="center")

def create_candidates_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=All Candidates List.xlsx'


    sql_query = f"""
        SELECT CD.name,CD.email,CD.mobile_no,AD.branch_shortlisted_for,AD.position_shortlisted_for,AD.application_status FROM CANDIDATE_DETAILS AS CD
        LEFT JOIN APPLICATION_DETAILS AS AD
        ON AD.candidate_id = CD.id;
        """

    # # Get all candidates from the database
    # columns = ['name','email','mobile_no',]
    
    # # Retrieve all candidate details from the database
    # candidate_objects = candidate_details.objects.all().values(*columns)
    df = pd.read_sql(sql_query, engine)
    
    data_list = df.to_dict(orient='records')
    # Convert the QuerySet to a DataFrame
    df = pd.DataFrame.from_records(data_list)

    # Make sure all datetime values are timezone unaware
    for column in df.columns:
        if pd.api.types.is_datetime64tz_dtype(df[column]):
            df[column] = df[column].apply(lambda x: x.replace(tzinfo=None))

    # Create a new Excel writer object
    writer = pd.ExcelWriter(response, engine='openpyxl')

    # Write the DataFrame to the Excel writer
    df.to_excel(writer, index=False, sheet_name='All Candidates List')

    # Get the worksheet of the DataFrame
    worksheet = writer.sheets['All Candidates List']

    # Apply custom header style
    set_header_style(worksheet.row_dimensions[0])

    writer.close()
    return response
