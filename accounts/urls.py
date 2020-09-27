from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView,LogoutView

app_name = 'accounts'

urlpatterns = [
    path('login/',LoginView.as_view(template_name='accounts/login.html'),name='login_url'),
    path('logout/',LogoutView.as_view(),name='logout_url'),
    path('signup/',SignupView.as_view(),name='signup_url'),
]
