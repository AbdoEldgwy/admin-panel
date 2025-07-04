from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('reset-password/', views.reset_password_view, name='reset'),
]