"""
URL configuration for gradadmin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_dashboard/',include('admin_dashboard.urls',namespace='AdminDashboard')),
    path('admin_dashboard/questions/',include('questions.urls',namespace='Questions')),
    path('accounts/',include('accounts.urls',namespace='accounts')),
    path('interview_scheduling/',include('interview_scheduling.urls',namespace='InterviewScheduling')),
    path('admin_dashboard/jobs/', include('Job.urls', namespace='Jobs')),
    path('admin/', admin.site.urls),
    path('',include('home.urls',namespace='Home')),
    path("api-auth/", include("rest_framework.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
