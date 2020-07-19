from .views import RegistrationView, UsernameValidationView, EmailValidationView, LoginView, ResetPasswordView, SetPasswordView
from django.urls import path 
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name="validate-email"),
    path('login/', LoginView.as_view(), name="login"),
    path('set-password/', SetPasswordView.as_view(), name="set-password"),
    path('reset-password/', ResetPasswordView.as_view(), name="reset-password"),
]
