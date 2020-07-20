from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User # Default User Model
from validate_email import validate_email # To validate email, pip install validate-email
from django.contrib import messages

# Create your views here.

# Class Based Views

#Username Validations
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        # Check whether the username is alphanumeric or not
        if not validate_email(email):
            return JsonResponse({'email_error':'Invalid Email Address.'}, status=400) # Bad Request Error (400)
        
        # Check whether the username is availale or not
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Account already created with this email.'}, status=409) # Conflicting Resources Error (409)

        return JsonResponse({'email_valid':True})


#Username Validations
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        # Check whether the username is alphanumeric or not
        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username can only have alphanumeric characters'}, status=400) # Bad Request Error (400)
        
        # Check whether the username is availale or not
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Username unavailable.'}, status=409) # Conflicting Resources Error (409)

        return JsonResponse({'username_valid':True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        # GET user Data to Register
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # For displaying selected email and username when password error
        context = {
            'fieldValues': request.POST # Gets all values from POST request
        }

        # VALIDATE (Django Validation)
        # Check whether the email and username are available or not
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password)<6:
                    messages.error(request, 'Password must be atleast 6 characters long.')
                    return render(request, 'authentication/register.html', context)
                
                # CREATE USER ACCOUNT
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()

                messages.success(request, 'Account Created Successfully!')
                return render(request, 'authentication/register.html')
            
            else:
                messages.error(request, 'Account already created with this email.')
                return render(request, 'authentication/register.html')
        else:
                messages.error(request, 'Username unavailable. Select another username.')
                return render(request, 'authentication/register.html')

        

        


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')


class SetPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/set-newpassword.html')


class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')
