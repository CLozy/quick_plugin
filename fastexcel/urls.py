from django.urls import path, include
from . import views
from .forms import  SignUpForm


urlpatterns = [
    path('', views.landing_page),
    path('accounts/register/', views.MyRegistrationView.as_view(form_class = SignUpForm), name='registration_register'),
    path('accounts/login/', views.MyLoginView.as_view() , name='auth_login'),
    path('accounts/', include('registration.backends.default.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_file),
]