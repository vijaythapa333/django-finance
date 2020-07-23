from .views import RegistrationView, UsernameValidationView, EmailValidationView, VerificationView, LoginView, ResetPasswordView, SetPasswordView, LogoutView, RequestResetEmailView
from django.urls import path 
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name="validate-email"),
    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name="activate"),
    path('request-reset-email/', RequestResetEmailView.as_view(), name="request-reset-email"),
    path('login/', LoginView.as_view(), name="login"),
    path('set-password/', SetPasswordView.as_view(), name="set-password"),
    path('reset-password/', ResetPasswordView.as_view(), name="reset-password"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
