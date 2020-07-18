from .views import RegistrationView, LoginView, ResetPasswordView, SetPasswordView
from django.urls import path 


urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('set-password/', SetPasswordView.as_view(), name="set-password"),
    path('reset-password/', ResetPasswordView.as_view(), name="reset-password"),
]
