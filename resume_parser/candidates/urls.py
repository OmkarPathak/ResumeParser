from django.urls import path
from . import views

app_name = 'candidates'

urlpatterns = [
    path('onboarding/', views.candidate_onboarding, name='candidate_onboarding'),
    path('', views.candidate_list, name='candidate_list'),
    path('upload/', views.upload_candidate, name='upload_candidate'),
    path('<int:pk>/', views.candidate_detail, name='candidate_detail'),
    path('<int:pk>/edit/', views.candidate_update, name='candidate_update'),
    path('<int:candidate_id>/submit/', views.submit_candidate, name='submit_candidate'),
    path('job/<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),
    path('application/<int:application_id>/schedule-interview/', views.schedule_interview, name='schedule_interview'),
    path('interview/<int:pk>/update/', views.update_interview, name='update_interview'),
    path('<int:pk>/delete/', views.delete_candidate, name='delete_candidate'),
    path('settings/', views.candidate_settings, name='candidate_settings'),
]
