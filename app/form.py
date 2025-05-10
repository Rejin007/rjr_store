from django import forms
from django.contrib.auth.models import User
from .models import *  
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class Register(forms.ModelForm):
    username = forms.CharField(label="username",max_length=50,required=True)
    email = forms.CharField(label="email",max_length=50,required=True)
    password = forms.CharField(label="password",max_length=50,required=True,widget=forms.PasswordInput)
    confirmpassword = forms.CharField(label="confirmpassword",max_length=50,required=True,widget=forms.PasswordInput)
    first_name = forms.CharField(label="firstname",max_length=50,required=True)
    last_name = forms.CharField(label="lastname",max_length=50,required=True)
    otp = forms.CharField(label="otp",max_length=6,required=False)
    
    
    class Meta:
        model = User
        fields = ['username','email','password','first_name','last_name']
        # def clean(self):
        #     cleaned_data = super().clean()
        #     password = cleaned_data.get("password")
        #     confirm_password = cleaned_data.get("confirmpassword")

        #     if password != confirm_password:
        #         raise ValidationError("Passwords do not match.")

        #     return cleaned_data
        
        
class Signupform(forms.ModelForm):
    username = forms.CharField(label="username",max_length=50,required=True)
    email = forms.CharField(label="email",max_length=50,required=True)
    first_name = forms.CharField(label="first_name",max_length=50,required=True)
    last_name = forms.CharField(label="last_name",max_length=50,required=True)
    phonenumber = forms.CharField(label="phone_number",max_length=50,required=True)
    gender = forms.ChoiceField(label="gender",choices=GENDER_CHOICES,widget=forms.RadioSelect,required=True)
    # dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="dob", required=True)
    dob = forms.DateField(label="dob",required=True)
    country = forms.ModelChoiceField(queryset=Countries.objects.all(),
                                     empty_label="select country",
                                     label="country",
                                     required=True)
    state = forms.ModelChoiceField(queryset=States.objects.none(),
                                     label="state",
                                     required=True)
    district = forms.ModelChoiceField(queryset=Districts.objects.none(),
                                     label="district",
                                     required=True)
    terms = forms.BooleanField(label="terms",required=True)
    
    def __init__ (self,*args,**kwargs):
        super(Signupform,self).__init__(*args,**kwargs)
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset=States.objects.filter(country_id=country_id)
            except(ValueError,TypeError):
                pass
            if 'state' in self.data:
                try:
                    state_id = int(self.data.get('state'))
                    self.fields['district'].queryset=Districts.objects.filter(state_id=state_id)
                except(ValueError,TypeError):
                    pass
    
    class Meta:
        model = Signup
        fields = ['username','email','first_name','last_name','phonenumber','gender','dob','country','state','district','terms']
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="username",max_length=50,required=True)
    password  = forms.CharField(label="password",max_length=50,required=True,widget=forms.PasswordInput)
    otp = forms.CharField(label="otp",max_length=6,required=False)
    cookie_box = forms.BooleanField(label="cookie_box",required=False,widget=forms.CheckboxInput)
    
class PasswordresetForm(forms.ModelForm):
    username = forms.CharField(label="username",max_length=50,required=True)
    email = forms.CharField(label="email",max_length=50,required=True)
    password  = forms.CharField(label="password",max_length=50,required=True,widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="confirm_password",max_length=50,required=True,widget=forms.PasswordInput)
    otp = forms.CharField(label="otp",max_length=6,required=False)

    class Meta:
        model = User
        fields = ['password']  
        
class Adress(forms.ModelForm):
    Name = forms.CharField(label="Name",max_length=50,required=True)
    Email = forms.EmailField(label="Email",max_length=50,required=True)
    Mobile_Number = forms.CharField(label="Mobile_Number",max_length=20,required=True)
    Street = forms.CharField(label="Street",max_length=50,required=True)
    Appartment_Suit_House_Number = forms.CharField(label="Appartment_Suit_House_Number",max_length=50,required=True)
    Pin_code = forms.CharField(label="Pin_code",max_length=20,required=True)
    country = forms.CharField(label="country",max_length=50,required=True)
    states = forms.CharField(label="states",max_length=50,required=True)
    district = forms.CharField(label="district",max_length=50,required=True)
    comment = forms.CharField(label="comment",max_length=50,required=True)
    
    class Meta:
        model = Adresses
        fields = ['Name','Email','Mobile_Number','Street','Appartment_Suit_House_Number','Pin_code','country','states','district','comment',]
    
    