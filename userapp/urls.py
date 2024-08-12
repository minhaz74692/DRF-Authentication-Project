from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from userapp import views

urlpatterns = [
    path('sign-up/', views.UserRegistration.as_view()),
    path('log-in/', views.LoginView.as_view()),
    path('users/', views.UserList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)