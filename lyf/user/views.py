# views.py
import re
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
from payments.models import user_wallet

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

        referrer_code = forms.CharField(required=False)

        class Meta:
            model = CustomUser
            fields = ['email', 'first_name', 'last_name', 'phone_number','referrer_code']

        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 == password2 and len(password1)>=8 and re.match(r'^(?=.*\d)(?=.*[@$!%*?&])', password1):
                request.session['password'] = password2 
            else:
                raise forms.ValidationError("Your password doesn't meet eligibility criteria.")
            return password2

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            
            referrer_code = form.cleaned_data['referrer_code']

            if referrer_code:
                try:
                    referrer_user=CustomUser.objects.get(referral_code=referrer_code)
                    referrer_id = referrer_user.id
                    request.session['referrer_id']=referrer_id

                except:
                    messages.error(request,'Invalid referral')


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
                'referral_code':user.referral_code,
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
                    user_details = request.session.get('user_details', {})
                    referrer_id = request.session.get('referrer_id')
                    if referrer_id is not None:
                        referrer=CustomUser.objects.get(id=referrer_id)
                        user = CustomUser(**user_details)
                        user.referrer=referrer
                        user.set_password(request.session.get('password'))
                        user.save()
                        login(request,user)
                        #user_wallet creation
                        user_wallet.objects.create(
                            user=request.user,
                            balance_amount=100,
                        )
                        #credit to referrar
                        referrer=CustomUser.objects.get(id=referrer_id)
                        referral_wallet=user_wallet.objects.get(user=referrer)
                        referral_wallet.balance_amount = referral_wallet.balance_amount + 100
                        referral_wallet.save()
                        del request.session['referrer_id']
                        messages.success(request,'₹100 credited to your wallet.')

                    else:
                        user = CustomUser(**user_details)
                        user.set_password(request.session.get('password'))
                        user.save()
                        login(request,user)
                        user_wallet.objects.create(
                            user=request.user
                        )

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
    request.session['user_logged_out'] = True
    return redirect('home:homePage')


@login_required(login_url='user:performlogin')
def user_profile(request):
    user_orders = order.objects.filter(user=request.user,payment=True)
    return render(request,'user/user_profile.html',{'user_orders':user_orders})

@login_required(login_url='user:performlogin')
def user_payment(request):
    user=request.user
    confirm_order =order.objects.filter(user=user,is_active=True,payment=False)
    return render(request,'user/user_payment.html',{'confirm_order':confirm_order})

@login_required(login_url='user:performlogin')
def user_cancel_rental(request,id):
    o=order.objects.get(id=id)
    o.status='cancelled'
    o.to_date=datetime.now()
    o.save()
    messages.error(request,'Rental cancelled')
    return redirect('user:user_payment')

@login_required(login_url='user:performlogin')
def user_invoice(request,id):
    ord=order.objects.filter(id=id)
    return render(request,'user/invoice.html',{'ord':ord})


def password_forget_maiil(request):
    if request.method=='POST':
        useremail=request.POST.get('useremail')
        try:
            user=CustomUser.objects.get(email=useremail)
            request.session['current_user']=useremail
            totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
            otp = totp.now()
            request.session["otp_secret_key_for"] = totp.secret
            valid_date = datetime.now() + timedelta(seconds=60)
            request.session["otp_valid_date_for"] = str(valid_date)

            subject = 'Your OTP for Login'
            message = f'Your OTP for login is: {otp}'
            from_email = 'o23211671@gmail.com'
            print(otp)
            send_mail(subject, message, from_email, [useremail])
            return redirect(reverse('user:password_forget_maiil'))
        except CustomUser.DoesNotExist:
            messages.error(request, 'Enter a registered email')

    return render(request,'user/user_forgot.html')

def forgot_otp_verify(request):
    if request.method=='POST':
        entered_otp =request.POST.get('otp')
        otp_secret_key_for = request.session.get('otp_secret_key_for')
        otp_valid_date_for = request.session.get('otp_valid_date_for')

        # Verify the OTP
        if otp_secret_key_for and otp_valid_date_for is not None:
            valid_until = datetime.fromisoformat(otp_valid_date_for)

            # Check if the OTP is still valid
            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key_for, interval=60)
                current_otp=totp.now()
                if current_otp==entered_otp:
                    del request.session['otp_secret_key_for']
                    del request.session['otp_valid_date_for']
                    return redirect('user:password_change')
                else:
                    messages.error(request,'Invalid OTP')
                    return redirect('user:forgot_otp_verify')
    return render(request,'user/user_forgot.html')



def password_change(request):
    if request.method=='POST':
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1==password2 and len(password1)>=8 and re.match(r'^(?=.*\d)(?=.*[@$!%*?&])', password1):
            current_user_mail=request.session['current_user']
            current_user=CustomUser.objects.get(email=current_user_mail)
            current_user.set_password(password1)
            current_user.save()
            del request.session['current_user']
            return redirect('user:performlogin')
        else:
            messages.error(request,'password should contain atleast one digit, special character and should be minimum of 8 letters')
    return render(request,'user/password_again.html')


@login_required(login_url='user:performlogin')
def user_edit(request):
    user_email = request.user.email
    details = CustomUser.objects.get(email=user_email)

    if request.method == 'POST':
        first_name = request.POST.get('firstname').strip()
        last_name = request.POST.get('lastname').strip()
        phone_number = request.POST.get('mobile').strip()
        password1 = request.POST.get('password1').strip()
        password2 = request.POST.get('password2').strip()

        if first_name:
            details.first_name = first_name
            details.save()

        if last_name:
            details.last_name = last_name
            details.save()

        if phone_number:
            details.phone_number = phone_number
            details.save()


        if not (first_name and last_name and phone_number):
            messages.error(request, 'Invalid Data')



        if password1 and password2:
            if password1 == password2 and len(password1) >= 8 and re.match(r'^(?=.*\d)(?=.*[@$!%*?&])', password1):
                details.set_password(password1)
                details.save()
                messages.success(request, 'User details updated successfully')
                messages.success(request, 'Please login again with your new password')
                request.session.flush()
                return redirect('user:perform_logout')
            else:
                messages.error(request, 'Passwords do not match or do not meet the criteria')
                return redirect('user:user_edit')
        messages.success(request,'User details updated successfully')

    return render(request, 'user/user_edit.html', {'details': details})



@login_required(login_url='user:performlogin')
def user_referral(request):
    user = request.user
    referred_users = user.referred_users.all()

    context = {
        'referred_users': referred_users,
        'user_refer': user,
    }
    return render(request, 'user/user_referrals.html', context)
    
    
    