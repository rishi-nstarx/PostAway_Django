from django.contrib import admin
from django.urls import path, include
from .views import SignUp, SignIn, signOut, EditProfile, ChangePassword, ForgotPassword, ResetPassword

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('signin/', SignIn.as_view(), name='signin'),
    path('signout/', signOut, name='signout'),
    path('edit_profile/', EditProfile.as_view(), name='edit_profile'),
    path('change_password/', ChangePassword.as_view(), name='change_password'),
    path('forgot_password/', ForgotPassword.as_view(), name='forgot_password'),
    path('reset_password/<uidb64>/', ResetPassword.as_view(), name='reset_password')
]