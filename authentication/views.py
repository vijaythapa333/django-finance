from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User # Default User Model
from validate_email import validate_email # To validate email, pip install validate-email
from django.contrib import messages
from django.core.mail import EmailMessage # To send emails
from django.urls import reverse

# To generate account activate link
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator

from django.contrib import auth # To work on login processes
from django.conf import settings

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
                user.is_active = False # Account will only be active after email verification
                user.save()

                # Send an Email to verify account
                ## Path/link to verify email
                ## - Getting the Domain we're on
                domain = get_current_site(request).domain # our Site URL

                ## - encode UID
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                ## - Token
                token = token_generator.make_token(user)
                ## - Relative URL to verification
                link = reverse('activate', kwargs={'uidb64': uidb64,'token': token})

                activate_url = 'http://'+domain+link

                email_body = 'Hi ' + user.username + ', \nPlease use this link to verify your account \n' + activate_url
                email_subject = 'Activate your account.'
                email = EmailMessage(
                    email_subject,
                    email_body,
                    # 'testvijayapps@gmail.com',
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                email.send(fail_silently=False)

                messages.success(request, 'Account Created! Check your email to verify account.')
                return render(request, 'authentication/register.html')
            
            else:
                messages.error(request, 'Account already created with this email.')
                return render(request, 'authentication/register.html')
        else:
                messages.error(request, 'Username unavailable. Select another username.')
                return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        # Converting ID into Human Readable Text
        
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            # Check whether the link is clicked previously or not
            if not token_generator.check_token(user, token):
                messages.success(request, "Account is already active. Please Login.") # Link Clicked already
                return redirect('login')
            

            # Check whether the user is active or not
            if user.is_active:
                messages.success(request, "Account is already active. Please Login.") # Account is already active
                return render('login')
            
            # Else Activate User
            user.is_active = True
            user.save()

            messages.success(request, "Account activated successfully. Login now.")
            return redirect('login')

        except Exception as e:
            messages.error(request, "Failed to activate user.")
            return redirect('register')
        

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        # Get Data from Login form
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            # Check Login Credentials
            user = auth.authenticate(username=username, password=password)

            if user:
                # Check whether the user is active or not
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "Welcome " +user.username+ " You're now logged in.")
                    return redirect('expenses')

                messages.error(request, 'Account is not active.')
                return redirect('login')
            
            messages.error(request, "Username or Password did not match.")
            return redirect('login')
        
        messages.error(request, "Please fill all fields.")
        return redirect('login')



class SetPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/set-newpassword.html')


class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('login')


class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'authentication/request-reset-email.html')
    
    def post(self, request):
        email = request.POST['email']

        # Check whether the email is valid or not
        if not validate_email(email):
            messages.error(request, "Please add a valid email address.")
            return render(request, 'authentication/request-reset-email.html')
        
        # Check whether the user exists or not
        user = User.objects.filter(email=email)
        
        if user.exists():
            # current_site = get_current_site(request) # our Site URL
            # email_subject = '[Reset your password.]'

            # email_body = render_to_string()
            
            # email = EmailMessage(
            #     email_subject,
            #     email_body,
            #     settings.EMAIL_HOST_USER,
            #     [email],
            # )
            # email.send(fail_silently=False)
            # I'll do it later
            pass


        messages.error(request, "Account not found with this email address.")
        return render(request, 'authentication/request-reset-email.html')

        return render(request, 'authentication/login.html')
