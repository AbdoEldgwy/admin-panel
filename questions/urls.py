from django.urls import path
from . import views

app_name = 'Questions'

urlpatterns = [
    path('', views.question_feed, name='questions'),
    path('field/<slug:field_slug>/', views.edit_question, name='edit_question'),
    path('delete/<int:question_id>/', views.delete_question, name='delete_question'),
]
