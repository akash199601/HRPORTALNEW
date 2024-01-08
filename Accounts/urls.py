from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [

    path('', views.home_page, name="home_page"),
  
    path('dashboard', views.dashboard, name="dashboard"),
    path('signup',views.signUp,name="signup"),
    path('signIn',views.signIn, name='signIn'),
    path('Login', views.Login, name="Login"),
    path('Logout',views.Logout,name="Logout"),
    path('profile',views.profile,name="profile"),
    path('profile_update/<int:candidate_id>',views.profile_update,name="profile_update"),
    path('upload_CV',views.upload_CV,name="upload_CV"),
    path('applied_user_details',views.applied_user_details,name="applied_user_details"),
    path('Onboarding_candidates',views.Onboarding_candidates,name="Onboarding_candidates"),
    path('shortlist_candidates',views.shortlist_candidates,name="shortlist_candidates"),
    path('assessed_candidates_details/<int:id>',views.assessed_candidates_details,name="assessed_candidates_details"),
    path('sceduled_user_details',views.sceduled_user_details,name="sceduled_user_details"),
    path('schedule_online_test',views.schedule_online_test,name="schedule_online_test"),
    path('hold_user_details',views.hold_user_details,name="hold_user_details"),
    path('rejected_user_details',views.rejected_user_details,name="rejected_user_details"),
    path('sceduled_user_full_details/<int:refId>',views.sceduled_user_full_details,name="sceduled_user_full_details"),
    path('scedule_interview/<int:refId>',views.scedule_interview,name="scedule_interview"),
    path('schedule_test/<int:refId>',views.schedule_test,name="schedule_test"),
    path('fetch_interview_dates',views.fetch_interview_dates,name="fetch_interview_dates"),
    path('fetch_interview_panel',views.fetch_interview_panel,name="fetch_interview_panel"),
    path('fetch_interview_positions',views.fetch_interview_positions,name="fetch_interview_positions"),
    path('fetch_interview_branches',views.fetch_interview_branches,name="fetch_interview_branches"),
    path('get_exam_sheet',views.get_exam_sheet,name="get_exam_sheet"),
    path('exam/<slug>',views.exam,name="exam"),
    path('test_view/',views.test_view,name="test_view"),

    path('applied_user_full_details/<int:refId>',views.applied_user_full_details,name="applied_user_full_details"),
    path('assessed_candidate_full_details/<int:application_id>',views.assessed_candidate_full_details,name="assessed_candidate_full_details"),
    path('accepted_user_full_details/<int:refId>',views.accepted_user_full_details,name="accepted_user_full_details"),
    path('rejected_user_full_details/<int:refId>',views.rejected_user_full_details,name="rejected_user_full_details"),
    path('alloted_user_full_details/<int:refId>',views.alloted_user_full_details,name="alloted_user_full_details"),
    path('hold_user_full_details/<int:refId>',views.hold_user_full_details,name="hold_user_full_details"),
    path('acceot_hold_candidate/<int:refId>',views.acceot_hold_candidate,name="acceot_hold_candidate"),
    path('schedule_test_user_full_details/<int:refId>',views.schedule_test_user_full_details,name="schedule_test_user_full_details"),
    path('accept_user/<int:refId>',views.accept_user,name="accept_user"),
    path('hold_user/<int:refId>',views.hold_user,name="hold_user"),
    path('reject/<int:refId>',views.reject,name="reject"),
    path('reject_user/<int:refId>',views.reject_user,name="reject_user"),
    path('bypass_user/<int:refId>',views.bypass_user,name="bypass_user"),
    path('reject_user_initial/<int:application_id>',views.reject_user_initial,name="reject_user_initial"),
    path('select_candidate/<int:refId>',views.select_candidate,name="select_candidate"),
    path('vacancy_lists/',views.vacancy_lists,name="vacancy_lists"),
    path('vacancy_card_details/<int:pk>',views.vacancy_card_details,name="vacancy_card_details"),
    path('candidate_vacancy_card_details/<int:pk>',views.candidate_vacancy_card_details,name="candidate_vacancy_card_details"),

    path('applied_vacancy_card_details/<int:pk>',views.applied_vacancy_card_details,name="applied_vacancy_card_details"),

    # path('test/<slug>',views.test,name="test"),

    
    path('candidate_login', views.candidate_login, name="candidate_login"),
    path('HR_login', views.HR_login, name="HR_login"),
    path('interviewer_login', views.interviewer_login, name="interviewer_login"),
    path('postjob', views.postjob, name="postjob"),
    path('update_job/<int:vacancy_id>', views.update_job, name="update_job"),
    path('application_status/', views.application_status, name="application_status"),
    path('sceduled_interview_details',views.sceduled_interview_details,name="sceduled_interview_details"),
    path('sceduled_interview_full_details/<int:refId>',views.sceduled_interview_full_details,name="sceduled_interview_full_details"), 
    path('review_allotment', views.review_allotment, name="review_allotment"),
    path('alloted_user_details', views.alloted_user_details, name="alloted_user_details"),
    path('reviewed_user_details', views.reviewed_user_details, name="reviewed_user_details"),
    path('ques_sheet/', views.ques_sheet, name="ques_sheet"),
    path('post_question/', views.post_question, name="post_question"),

    path('question_sheet/', views.question_sheet, name="question_sheet"),
    path('view_candidate_profile/<str:email>', views.view_candidate_profile, name="view_candidate_profile"),
    path('sonata_online_exam/<int:refId>', views.sonata_online_exam, name="sonata_online_exam"),
    path('online_exam_details/<int:refId>/<int:tbl_id>/', views.online_exam_details, name="online_exam_details"),
    path('start_online_exam/<int:refId>/<int:tbl_id>/', views.start_online_exam, name="start_online_exam"),
    
    path('offline_test_details/', views.offline_test_details, name="offline_test_details"),
    path('update_test_score/<int:refId>/', views.update_test_score, name="update_test_score"),  
    path('camshot_picture/<int:id>', views.camshot_picture, name="camshot_picture"),
    path('interview_Api/', views.interview_Api, name='interview_Api'),
    path('number_of_interviewer/', views.number_of_interviewer, name='number_of_interviewer'),
    path('show_exam_result/<int:id>/<int:application_id>/', views.show_exam_result, name='show_exam_result'),
    path('quest_sheet_list/', views.quest_sheet_list,name="quest_sheet_list"),
    path('search',views.search,name="search"),

    # path('get-calender/<user_id>/', views.get_scheduled_interview_count_matrix_by_time_slot_and_week, name="get_calender"),
    # path('get-calender/<user_id>/<date>', views.get_scheduled_interview_count_matrix_by_time_slot_and_week, name="get_calender"),
    
    # path('heading', views.heading, name="heading"),
    # path('change_password', views.change_password, name="change_password"),
    # path('verify_otp', views.verify_otp, name="verify_otp"),
    path('get-calender/<user_id>/', views.get_scheduled_interview_count_matrix_by_time_slot_and_week, name="get_calender"),
    path('get-calender/<user_id>/<date>', views.get_scheduled_interview_count_matrix_by_time_slot_and_week, name="get_calender"),
    path('get-calender', views.get_calender, name="get_calender"),
    
    path('heading', views.heading, name="heading"),
    path('change_password', views.change_password, name="change_password"),
    path('verify_otp', views.verify_otp, name="verify_otp"),
    
    path('upload-cv_render/', views.upload_cv_render, name='upload_CV_render'),
    path('success/', views.success_page, name='success_page'),
    path('rejected/', views.rejected, name="rejected"),
    path('exam_snapshot_dashboard', views.exam_snapshot_dashboard, name="exam_snapshot_dashboard"),
    path('exam_user_full_details/<int:refId>/', views.exam_user_full_details, name="exam_user_full_details"),
    path('quest_sheetlist_details/<sheet_id>/',views.quest_sheetlist_details,name="quest_sheetlist_details"),
    path('edit_question/<int:id>/', views.edit_question, name="edit_question"),
    path('all_user_list/', views.all_user_list, name="all_user_list"),
    path('roll_assign/',views.roll_assign,name="roll_assign"),
    path('delete_question/<int:id>/', views.delete_question, name="delete_question"),

    path('forget_password_send_otp/', views.forget_password_send_otp, name="forget_password_send_otp"),
    path('forget_password_verify_otp/<str:reset_key>', views.forget_password_verify_otp, name="forget_password_verify_otp"),
    path('search_exam', views.search_exam, name='search_exam'),
    path('check-duplicate-username/<str:username>/', views.checkdublicate1, name='check_duplicate_username'),
    path('check-duplicate-email/<str:email>/', views.checkdublicate2, name='check_duplicate_email'),
    path('check-duplicate-mobile/<str:mobile>/', views.checkdublicate3, name='check_duplicate_mobile'),
    path('check-duplicate-email2/<str:email>/', views.checkdublicate4, name='check_duplicate_email2'),
    path('reschedule_interview_user/', views.reschedule_interview_user, name='reschedule_interview_user'), 
    path('api_reschedule_interviews/', views.api_reschedule_interviews, name='api_reschedule_interviews'),
    path('api_exam_snapshot/', views.api_exam_snapshot, name='api_exam_snapshot'),
    path('get_branch_options/', views.get_branch_options, name='get_branch_options'),
    path('get_branch_vacancy_options/', views.get_branch_vacancy_options, name='get_branch_vacancy_options'),
    path('get_branch_exam_options/', views.get_branch_exam_options, name='get_branch_exam_options'),
    path('api_exam_filter/', views.api_exam_filter, name='api_exam_filter'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
    path('api_vacancy_filter/', views.api_vacancy_filter, name='api_vacancy_filter'),
    path('get_branch_interview_options/', views.get_branch_interview_options, name='get_branch_interview_options'),
    path('api_interview_filter/', views.api_interview_filter, name='api_interview_filter'),
    path('get_branch_shortlist_options/', views.get_branch_shortlist_options, name='get_branch_shortlist_options'),
    path('api_shortlist_filter/', views.api_shortlist_filter, name='api_shortlist_filter'),
    path('get_branch_onboarding_options/', views.get_branch_onboarding_options, name='get_branch_onboarding_options'),
    path('api_onboarding_filter/', views.api_onboarding_filter, name='api_onboarding_filter'),
    path('get_branch_hold_options/', views.get_branch_hold_options, name='get_branch_hold_options'),
    path('api_hold_filter/', views.api_hold_filter, name='api_hold_filter'),
    path('get_branch_rejected_options/', views.get_branch_rejected_options, name='get_branch_rejected_options'),
    path('api_rejected_filter/', views.api_rejected_filter, name='api_rejected_filter'),
    path('get_branch_alloted_options/', views.get_branch_alloted_options, name='get_branch_alloted_options'),
    path('api_alloted_filter/', views.api_alloted_filter, name='api_alloted_filter'),
    path('candidate_application_status/<str:email>', views.applied_vacancy, name='candidate_application_status'),
    path('view_application/<int:id>', views.view_application, name='view_application'),
    path('apply_for_vacancy/<int:id>', views.apply_for_vacancy, name="apply_for_vacancy"),


    path('rejected_applications/', views.rejected_applications, name="rejected_applications"),
    path('rejected_application/<int:application_id>', views.rejected_application, name="rejected_application"),
    
    path('alloted_applications/', views.alloted_applications, name="alloted_applications"),
    path('alloted_application/<int:application_id>', views.alloted_application, name="alloted_application"),

    path('reviewed_applications/', views.reviewed_applications, name="reviewed_applications"),
    path('reviewed_application/<int:application_id>', views.reviewed_application, name="reviewed_application"),
    
    path('Contact_Us_Page',views.Contact_Us_Page,name="Contact_Us_Page"),
    path('show_contact',views.show_contact,name="show_contact"),
    
    path('upload_documents/<int:candidate_id>',views.upload_documents,name="upload_documents"),
    path('indexCopy',views.indexCopy,name="indexCopy"),
    
    path('verifyDocument/<int:refId>/',views.verifyDocument, name="verifyDocument"),
    
    path('pdf/<int:refId>/',views.pdf,name="pdf"),
    
    path('candidate_list',views.candidate_list,name="candidate_list"),
    path('create_candidates_excel',views.create_candidates_excel,name="create_candidates_excel"),
    
]