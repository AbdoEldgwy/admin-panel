from django.urls import path
from . import views

app_name = 'Jobs'
urlpatterns = [
    path('',views.post_job,name='post_job'),
]