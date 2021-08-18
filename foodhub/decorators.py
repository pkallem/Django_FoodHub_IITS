from django.http import HttpResponse
from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import CreateUserForm, ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from .models import *
from django.shortcuts import redirect, render

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
 
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'noaccess.html')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return view_func(request, *args, **kwargs)
            # return redirect('home')
        
        if group == 'admin':
            # return redirect('restaurant')
            Oser = get_user_model()
            restaurants = Oser.objects.filter(is_staff=True)
            products = Product.objects.all()
            context = {'products':products, 'restaurants':restaurants}
            return render(request, 'myrestaurant.html', context)

    return wrapper_function

