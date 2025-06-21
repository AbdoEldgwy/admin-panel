from django.urls import path
from .views import interview_scheduling

app_name = 'InterviewScheduling'
urlpatterns = [
    path('', interview_scheduling, name='interview_scheduling'),
]