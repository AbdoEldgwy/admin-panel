from django.urls import path
from . import views
app_name='home'
urlpatterns = [
    path('', views.home,name='home'),
    path('job_page/', views.job_page,name='job_page'),
    path('job_page/<str:job_slug>/',views.job_details,name='job_slug'),
]