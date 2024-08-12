from django.urls import path, include
from userapp import views
from django.contrib import admin
from rest_framework.authtoken import views

urlpatterns = [
    path('', include('userapp.urls')),
    path('admin/', admin.site.urls),
]