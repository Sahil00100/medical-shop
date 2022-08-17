from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from.models import Medicine
class UserForm(forms.Form):
    alphanumeric = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters are allowed.')
    numbers=RegexValidator(r'^[0-9]*$','only numbers allowed')
    #form elements
    firstname=forms.CharField(max_length=100,required=True,validators=[alphanumeric],widget=forms.TextInput(attrs={'placeholder':'Firstname','class':'form-control form-control-lg'}))  
    lastname=forms.CharField(max_length=100,required=True,validators=[alphanumeric],widget=forms.TextInput(attrs={'placeholder':'Lastname','class':'form-control'}))  
    email=forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder':'Email','class':'form-control'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control'}),required=True,label='Password')
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm password','class':'form-control'}),required=True,label='Confirm Password')
    
    
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            
            raise forms.ValidationError('Using this email already an account created,use another email')
                
        else:
            return email
    
    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        
        if password1 and password2 and password1!=password2:
           raise forms.ValidationError('Password incorrect! try again')
        else:
            return password2
    
    
    #creating and saving  user
    def create_user(self):
        print('user')
        user=User.objects.create_user(
            username=self.clean_email(),
            first_name=self.cleaned_data.get('firstname'),
            last_name=self.cleaned_data.get('lastname'),
            email=self.clean_email(),
            password=self.clean_password2()
        )
        user.save()
        return user
