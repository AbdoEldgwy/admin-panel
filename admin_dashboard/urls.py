from django.urls import path
from . import views
from . import gemini_views
app_name='AdminDashboard'
urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('admin_dashboard/candidate/', views.candidate, name='candidate'),
    path('admin_dashboard/candidate/<slug:slug>/', views.candidate_details, name='candidate_details'),
    path('admin_dashboard/candidate/<int:candidate_id>/edit/', views.edit_candidate, name='edit_candidate'),
    path('admin_dashboard/candidate/<int:candidate_id>/delete/', views.delete_candidate, name='delete_candidate'),
    path('admin_dashboard/candidates/delete_selected/', views.delete_selected_candidates, name='delete_selected_candidates'),
    path('admin_dashboard/ai-filter/', gemini_views.ai_filter, name='ai_filter'),

]
