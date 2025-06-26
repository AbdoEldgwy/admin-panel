from django.urls import path
from . import views

app_name = 'InterviewScheduling'

urlpatterns = [
    path('', views.interview_scheduling_view, name='interview_scheduling'),
    path('start/<int:session_id>/', views.start_session, name='start_session'),
    path('delete/<int:session_id>/', views.delete_session, name='delete_session'),
]
