from django.urls import path
from auth_service.views import (
    LoginUser,
    RegisterUser,
    SendMail,
    VerifyOtp,
    PasswordReset,
    Logout,
    CurrentUser, 
    UpdateProfile,
    DeleteProfile,
    MfaSteStep2,
    MFaSteStep1
)

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('send-mail/', SendMail.as_view(), name='send_mail'),
    path('verify-otp/', VerifyOtp.as_view(), name='verify_otp'),
    path('password-reset/', PasswordReset.as_view(), name='password_reset'),
    path('logout/', Logout.as_view(), name="logout_user"),
    path('current-user/', CurrentUser.as_view(), name='current_user'),
    path("update-user/<int:pk>/", UpdateProfile.as_view(), name='update_user'),
    path("delete-user/<int:pk>/", DeleteProfile.as_view(), name='delete_user'),
    path('mfa-validate/', MFaSteStep1.as_view(), name="validate_user"),
    path('mfa-verify/', MfaSteStep2.as_view(), name="verify_user"),
]
