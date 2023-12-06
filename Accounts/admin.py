from django.contrib import admin

# Register your models here.

from .models import *


@admin.register(Rolls)
class RollsAdmin(admin.ModelAdmin):
    list_display = ('roll_name', 'roll_id')
    list_filter = ('roll_name', 'roll_id')
    search_fields = ('roll_name', 'roll_id')


@admin.register(User_Rolls)
class User_RollsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'roll_id', )
    list_filter = ( 'roll_id', )
    search_fields = ('user_id', 'roll_id', )


@admin.register(User_Details)
class User_DetailsAdmin(admin.ModelAdmin):
    list_display=['name']

class vacancyAdmin(admin.ModelAdmin):
    list_display = [
    'branch_name',
    'no_of_vacancies',
    'job_role',
    'salary',
    'qualification_type',
    'interview_place',
    'interview_date',
    'interview_time',
    'interview_panel_1',
    'interview_panel_2',
    'interview_panel_3',
    'interview_panel_4',
    'job_responsibility',
    'job_description'
    ]
    search_fields=[
    'branch_name',
    'no_of_vacancies',
    'job_role',
    'salary',
    'qualification_type',
    'interview_place',
    'interview_date',
    'interview_time',
    'interview_panel_1',
    'interview_panel_2',
    'interview_panel_3',
    'interview_panel_4',
    'job_responsibility',
    'job_description'
]
    
admin.site.register(question_sheet)
admin.site.register(exam_response)
admin.site.register(ContactUsTable)
admin.site.register(vacancy)