# views.py
import pyotp
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.urls import reverse
from pyotp import TOTP
from django.core.mail import send_mail
from datetime import datetime, timedelta  # Import datetime and timedelta
from django.contrib.auth.decorators import login_required
from order.models import order


CustomUser = get_user_model()


def performlogin(request):
    if request.user.is_authenticated:
        if request.user.is_super:
            return redirect('adminPanel:adminPanel')
        else:
            return redirect('home:homePage')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect("adminPanel:adminPanel")
            else:
                login(request, user)
                return redirect("home:homePage")
        else:
            messages.error(request, 'Invalid login credentials or your are not authorised to access this page')

    return render(request, 'user/performlogin.html')


def user_registration(request):
    if request.user.is_authenticated:
        return redirect('home:homePage')
    class RegistrationForm(forms.ModelForm):
        password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
        password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

        class Meta:
            model = CustomUser
            fields = ['email', 'first_name', 'last_name', 'phone_number']

        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords do not match.")
            request.session['password'] = password2 
            return password2

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            
            #otp section
            totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
            otp = totp.now()
            request.session["otp_secret_key"] = totp.secret
            valid_date = datetime.now() + timedelta(seconds=60)
            request.session["otp_valid_date"] = str(valid_date)


            #store user details temporarily
            request.session['user_details'] = {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
            }

            # Send OTP via email
            subject = 'Your OTP for Login'
            message = f'Your OTP for login is: {otp}'
            from_email = 'o23211671@gmail.com'  
            print(otp)
            send_mail(subject, message, from_email, [user.email])

            return redirect(reverse('user:otpPage'))  # Redirect to OTP verification page
        else:
            messages.error(request, 'Registration failed. Please correct the errors in the form.')
    else:
        form = RegistrationForm()

    return render(request, 'user/user_registration.html', {'form': form})

def otpPage(request):
    error_message = None
    if request.method == 'POST':
        # Retrieve the OTP, secret, and expiry time stored in the session
        otp = request.POST.get('otp')
        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_date = request.session.get('otp_valid_date')

        # Verify the OTP
        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)

            # Check if the OTP is still valid
            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                current_otp=totp.now()
                #if totp.verify(otp):
                print(current_otp)
                if current_otp==otp:
                    print("OTP Verified")
                    # OTP verification successful
                    # Retrieve user details from the session
                    user_details = request.session.get('user_details', {})
                    user = CustomUser(**user_details)

                    # Set the user's password and save the user
                    user.set_password(request.session.get('password'))
                    user.save()
                    login(request,user)
                    del request.session['user_details']
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    # Redirect to the desired page
                    return redirect("home:homePage")
                else:
                    messages.error(request, 'Invalid OTP. Please try again.')
            else:
                messages.error(request, 'OTP has expired. Please request a new OTP.')
        else:
            messages.error(request, 'OTP verification failed. Please try again.')

    return render(request, 'user/otpPage.html')


def resendOtp(request):
    if request.method == "GET":
        # Generate a new OTP and update the session data
        totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
        otp = totp.now()

        user_details = request.session['user_details']
        email = user_details.get('email', "None")
        subject = 'Your OTP for Login'
        message = f'Your OTP for login is: {otp}'
        from_email = 'o23211671@gmail.com'  
        print(f"Your new one-time password is {otp}")

        send_mail(subject, message, from_email, [email])
        request.session["otp_secret_key"] = totp.secret
        valid_date = datetime.now() + timedelta(seconds=60)
        request.session["otp_valid_date"] = str(valid_date)
        print(f"Your new one-time password is {otp}")
        return redirect("user:otpPage")

    return render(request, "registration/verify_otp.html")


@login_required(login_url='user:performlogin')
def perform_logout(request):
    logout(request)
    request.session.flush()
    return redirect('home:homePage')


@login_required(login_url='user:performlogin')
def user_profile(request):
    user_orders = order.objects.filter(user=request.user,payment=True)
    return render(request,'user/user_profile.html',{'user_orders':user_orders})


def user_payment(request):
    user=request.user
    confirm_order =order.objects.filter(user=user,is_active=True,payment=False)
    return render(request,'user/user_payment.html',{'confirm_order':confirm_order})


def user_cancel_rental(request,id):
    o=order.objects.get(id=id)
    o.delete()
    return redirect('user:user_payment')