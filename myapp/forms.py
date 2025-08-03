from django import forms

from .models import User,Post



class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['name','age','email','password']
        
class LoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)


class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','content']
        