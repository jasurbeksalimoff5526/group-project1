from django.urls import path
from .views import *

urlpatterns = [
    path("auth/", SignUpView.as_view(), name="signup"), 
    path("login/", LoginView.as_view(), name="login"), 
    path("logout/", logout_view, name="logout"),
    path("profile/<int:id>/", ProfileView.as_view(), name="profile"), 
    path("profile-update/", ProfileUpdateView.as_view(), name="profile_update"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"), 
]
