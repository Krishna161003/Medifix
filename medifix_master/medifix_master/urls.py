from django.contrib import admin
from django.urls import path, include
from administration import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name="home"),
    path('register/', views.signup_view, name="register"),
    path('camp_organizer_request/', views.camp_organizer_request, name="camp_organizer_request"),
    path('camp_register/', views.register_camp_org, name="camp_register"),
    path('my_camps/', views.user_camps, name="my_camps"),
    path('approve/<str:username>/', views.approve_application, name='approve_application'),
    path('deny/<str:username>/', views.deny_application, name='deny_application'),
    path('organizer/<str:username>/', views.camp_organizer_profile_detail, name='organizer_user_profile_detail'),
    path('create/', views.create_camp_view, name='create_camp'),
    path('create-doctor/', views.create_doctor, name='create_doctor'),
    path('doctors/', views.list_doctors_for_user, name='list_user_doctors'),
    path('camp_services/', views.list_camp_services_for_user, name='list_user_camp_services'),
    path('create_camp_service/', views.create_camp_service, name='create_camp_service'),
    path('camp/<int:camp_id>/', views.camp_details_view, name='camp_details'),
    path('camp/<int:pk>/delete/', views.camp_delete, name='camp_delete'),
    path('all_camps/', views.all_camps, name='all_camps'),
    path('register_appointment/<int:camp_id>/', views.register_appointment, name='register_appointment'),
    path('appointment_detail/<int:camp_id>/<int:user>/', views.view_campregistration_details, name="view_campregistration_details"),
]
