from django.shortcuts import render, HttpResponse, redirect
from django.views import View

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

from dotenv import load_dotenv
load_dotenv()
import os

from .models import Users
from django.utils.decorators import method_decorator
from .utils import create_jwt, decode_jwt, custom_login_required
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


import bcrypt
salt = bcrypt.gensalt(rounds=12)



# Create your views here.

@custom_login_required
def signOut(request):
    response = redirect('signin')
    response.delete_cookie('auth_token')
    return response


class SignUp(View):

    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        try:
            form_data = request.POST
            image = request.FILES.get('image', None)
            username = form_data['username']
            first_name = form_data['first_name']
            last_name = form_data['last_name']
            email = form_data['email']
            password = bcrypt.hashpw(form_data['password'].encode('utf-8'), salt)

            user = Users(username=username, first_name=first_name, last_name=last_name, email=email, password=password.decode('utf-8'))
            if image:
                user.profile_picture = image
            user.save()
            return redirect('signin')
        except Exception as e:
            print(e)
            return redirect('signup')


class SignIn(View):

    def get(self, request):
        return render(request, 'signin.html')
    
    def post(self, request):
        try:
            form_data = request.POST
            username = form_data['username']
            password = form_data['password'].encode('utf-8')

            user = Users.objects.get(username=username)

            if not (user.username==username and bcrypt.checkpw(password, user.password.encode('utf-8'))):
                raise Exception("The credentials are not correct!")
            
            token = create_jwt(user)
            response = redirect('home')
            response.set_cookie('auth_token', token, httponly=True, samesite='LAX')
            return response

        
        except Exception as e:
            print(e)
            return render(request, 'signin.html', {'error': str(e)})
    

class EditProfile(View):
    @method_decorator(custom_login_required)
    def get(self, request):
        token = request.COOKIES.get('auth_token')
        if token is None or not decode_jwt(token):
            return redirect('signin')
        payload = decode_jwt(token)
        user_id = payload.get('id')
        user = Users.objects.get(id=user_id)
        return render(request, 'edit_profile.html', {"user":user})
    
    @method_decorator(custom_login_required)
    def post(self, request):
        token = request.COOKIES.get('auth_token')
        if token is None or not decode_jwt(token):
            return redirect('signin')
        payload = decode_jwt(token)
        user_id = payload.get('id')
        user = Users.objects.get(id=user_id)

        try:
            form_data = request.POST
            user.profile_picture = request.FILES.get('image', None)
            print(request.FILES.get('image'))
            user.username = form_data['username']
            user.first_name = form_data['first_name']
            user.last_name = form_data['last_name']
            user.email = form_data['email']
            # if image:
            #     user.profile_picture = image
            # user.update()
            user.save()
            return redirect('home')
        except Exception as e:
            print(e)
            return redirect('edit_profile')
        

class ChangePassword(View):

    @method_decorator(custom_login_required)
    def get(self, request):
        token = request.COOKIES.get('auth_token')
        if token is None or not decode_jwt(token):
            return redirect('signin')
        return render(request, 'change_password.html')
    
    @method_decorator(custom_login_required)
    def post(self, request):
        token = request.COOKIES.get('auth_token')
        if token is None or not decode_jwt(token):
            return redirect('signin')
        payload = decode_jwt(token)
        user_id = payload.get('id')
        user = Users.objects.get(id=user_id)

        check = bcrypt.checkpw(request.POST['oldpassword'].encode('utf-8'), user.password.encode('utf-8'))

        if not check:
            raise Exception('Old password was incorrect.')
        new_hashed_password = bcrypt.hashpw(request.POST['newpassword'].encode('utf-8'), salt)
        user.password = new_hashed_password.decode('utf-8')
        user.save()
        return signOut(request)
    

class ForgotPassword(View):
    
    def get(self, request):
        return render(request, 'forgot_password.html')
    
    def post(self, request):
        user_credential = request.POST['username-email']
        user = Users.objects.get(username=user_credential)
        if not user:
            user = Users.objects.get(email=user_credential)

        user_id = user.id
        uid = urlsafe_base64_encode(str(user_id).encode('utf-8'))
        reset_url = f"http://{request.get_host()}/users/reset_password/{uid}/"

        # Email configuration
        smtp_server = os.getenv('EMAIL_HOST')
        smtp_port = os.getenv('EMAIL_PORT')
        sender_email = os.getenv('EMAIL_HOST_USER')
        receiver_email = user.email
        password = os.getenv('EMAIL_HOST_PASSWORD')

        subject = 'Password Reset Link'
        body = f'Use this link to reset your password: {reset_url}'
        
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = user.email
        msg['Subject'] = subject

        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Connect to the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            server.quit()
            
        return redirect('signin')
    

class ResetPassword(View):
    def get(self, request, uidb64):
        return render(request, 'reset_password.html', {"uidb64":uidb64})
        

    def post(self, request, uidb64):
        user_id = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = Users.objects.get(id=user_id)
        new_hashed_password = bcrypt.hashpw(request.POST['newpassword'].encode('utf-8'), salt)
        user.password = new_hashed_password.decode('utf-8')
        user.save()
        return redirect('signin')




        
