from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Posts, ContactModel


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class PostsModelForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['user_post', 'title', 'body_post', 'image', 'link']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = '__all__'
