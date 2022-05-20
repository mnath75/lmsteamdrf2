
from django.urls import path
from .views import (ValidatePhoneSendOTP,ValidateOTP,Register,LoginAPI,ChangePasswordView,
                    ForgotPasswordChange,UpdateProfileView,UserView)
from knox import views as knox_views

urlpatterns = [

    path('validate_phone/',ValidatePhoneSendOTP.as_view()),
    path('validate_otp/',ValidateOTP.as_view()),
    path('Register/',Register.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
    path('change_password/<int:pk>/', ChangePasswordView.as_view()),
    path('change_forgot_password/', ForgotPasswordChange.as_view()),
    #path('user_profile/', UserView.as_view()),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view()),
]
