from django.urls import path, include
from . import views


urlpatterns = [
    path('fastexcel/', views.upload_file),
]