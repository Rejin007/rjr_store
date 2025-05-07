from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import *
from .form import *
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.conf.urls.static import static
import os
from django.contrib.staticfiles import finders
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import uuid
from django.contrib.auth import authenticate,login,logout as djangologout
import secrets
from django.contrib.auth import get_user_model


# Create your views here.
def homepage(request):
    return render(request,"home.html")

def about(req):
    return render(req,"about.html")

def contact(req):
    return render(req,"contact.html")

def loginpage(req):
    title = "login"
    form = LoginForm(req.POST)
    if req.method == 'POST':

        form = LoginForm(req,data=req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            cookie_box = form.cleaned_data.get('cookie_box')
            input_code = form.cleaned_data.get('otp')
            user = authenticate(username = username,password = password)
            # OTP.objects.filter(created_at__lt=timezone.now()).delete()  # delete otp when any store in db
                
            if user is not None:
                try:
                    latest_otp = OTP.objects.filter(user = user).latest('created_at')
                    if latest_otp.is_expired(): # if otp is expired
                        latest_otp.delete()
                        raise OTP.DoesNotExist
                except OTP.DoesNotExist:
                    otp_code = generate_otp()       # to generate otp
                    OTP.objects.create(user = user,code = otp_code)  # create in db otp
                    user_email = user.email     
                    otp = otp_code
                    send_otp(user_email,otp)
                    return render(req,"login.html",{
                        "title":title,
                        "form":form,
                        "otp_send":True,
                        "username":username,
                        "password":password
                        })
                if input_code and input_code == latest_otp.code and not latest_otp.is_expired(): # login if all contition is true
                    login(req,user)                             # for login
                    latest_otp.delete()                         # after login delete otp from db;
                    return redirect("app:homepage")
                    # if cookie_box is True:  
                    #     pass
                    #     # for save cookies
                    #     # set_cookies(req,username)
                    #     # get_cookies(req)
                    #     return redirect("app:homepage")
                    # else:                                       # for save session
                    #     return render(req,"login.html")
                    
                else:
                    pass
            else:
                pass
        else:
            pass

    return render(req,"login.html")

def generate_otp(length=6):
    otp = ''.join([str(secrets.randbelow(10))for _ in range(length)])
    return otp

def send_otp(user_email,otp):
    subject = "your otp code"
    message = f"Your OTP Code is {otp}. It Will Expire in 5-Minutes"
    
    from_  = settings.EMAIL_HOST_USER
    send_mail(subject,message,from_,[user_email])

def refresh(req):

    if OTP.objects.exists():
        OTP.objects.all().delete()  # delete otp when any store in db
    return redirect("app:loginpage")

def forgotrefresh(req):

    if OTP.objects.exists():
        OTP.objects.all().delete()  # delete otp when any store in db
    return redirect("app:forgotpassword")

def logout(req):
    djangologout(req)
    response = redirect("app:homepage")
    response.delete_cookie("username")

    return response 
 
def register(req):
    countries = Countries.objects.all()
    if req.method == 'POST':
        form = Register(req.POST)
        signupform = Signupform(req.POST)
        if form.is_valid() and signupform.is_valid():
            password = form.cleaned_data.get('password')
            confirmpassword = form.cleaned_data.get('confirmpassword')
            if password==confirmpassword:
                signupform.save()
                user = form.save(commit=False)
                user.set_password(password)
                user.is_active = False
                try:
                    user.save()
                    user = User.objects.get(email=user.email)
                    mail(req,user)
                    return HttpResponseRedirect('https://mail.google.com/')
                except Exception as e:
                    print(form.errors)
            else:
                print(form.errors)
        else:
            print(form.errors)
    else:
        form = Register()
            
    return render(req,"register.html",{'countries': countries})

def mail(req,user):
   
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    site = get_current_site(req)
    domain = site.domain
    # print(user.id,"*******",uid,"*******",token)
    message = render_to_string(
        "mail.html",
        {'uid':uid,
        'token':token,
        'user':user,
        'domain':domain
        }
    )
    # print("email = ",user.email)
    subject = 'verification mail from RJR'
    recipient_list=[user.email]
    email = EmailMessage(subject,message,'rejinrjr144@gmail.com',to=recipient_list)
    email.content_subtype='html'
    email.send()

def activate(req,uidb64,token):

    pk = urlsafe_base64_decode(uidb64).decode()
    user = get_object_or_404(User,pk = pk)

    if default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('app:loginpage')

def forgotpassword(req):
    title = "Reset password"
    if req.method == 'POST':
        form = PasswordresetForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            input_code = form.cleaned_data.get('otp')
            user = get_user_model().objects.get( email=email) # filter by emailinput is equal to email in db
            try:
                latest_otp = OTP.objects.filter(user = user).latest('created_at') #get latest otp from db(user is User model pk no = user eg : username/email we entered)
                if latest_otp.is_expired(): # check if otp is expired 
                    latest_otp.delete()
                    raise OTP.DoesNotExist
            except OTP.DoesNotExist:
                otp_code = generate_otp()       # to generate otp
                OTP.objects.create(user = user,code = otp_code)  # create in db otp
                user_email = user.email     
                otp = otp_code
                send_otp(user_email,otp)
                return render(req,"forgot.html",{
                    "title":title,
                    "form":form,
                    "otp_sends":True,
                    "username":username,
                    "password":password,
                    "email":email,
                    "confirm_password":confirm_password
                    })
            
            if input_code and input_code == latest_otp.code and not latest_otp.is_expired() and password == confirm_password: # login if all contition is true
                User = get_user_model()     #നിങ്ങൾ Django-ൽ ഉപയോഗിക്കുന്ന original/correct User model automatically തിരഞ്ഞെടുത്ത് കൊടുക്കുന്ന function ആണു്
                user = User.objects.get(email = email)  # Or use email/id
                user.set_password(password) # for reset password
                user.username
                user.save()
                latest_otp.delete()
                return redirect('app:loginpage')
            else:
                return render(req,"forgot.html")
            
        else:
            # print(form.errors)
            return render(req,"forgot.html")

    return render(req,"forgot.html",{"title":title})

def address(req):
    countries = Countries.objects.all()
    return render(req,"adress.html",{'countries': countries})

def states(req,id):
    states = States.objects.filter(country_id=id).values('id','state_name')
    return JsonResponse(list(states),safe=False)
def districts(req,id):
    districts = Districts.objects.filter(state_id=id).values('id','district_name')
    return JsonResponse(list(districts),safe=False)
def get_products(req):
    products = Products.objects.all()
    return render(req,"products.html",{'products': products})
def get_product(req,slug):
    product = Products.objects.get(slug=slug)
    return render(req,"product.html",{'product': product})
def cartload(req):
    return render(req,"cart.html")