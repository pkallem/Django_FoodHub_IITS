from foodhub.models import Product
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        