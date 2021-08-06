from foodhub.decorators import unauthenticated_user
from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from .decorators import admin_only, allowed_users, unauthenticated_user
from django.contrib.auth.models import Group
from .models import *

@login_required(login_url='login')
@admin_only
# @allowed_users(allowed_roles=['customer'])
def homePage(request):
    Oser = get_user_model()
    restaurants = Oser.objects.filter(is_staff=True)
    products = Product.objects.all()
    context = {'products':products, 'restaurants':restaurants}
    return render(request,'index.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
@admin_only
def restaurantPage(request):
    context = {}
    system = request.POST.get('system', None)
    products = Product.objects.all()
    context['system'] = system
    context['products'] = products
    return render(request, 'restaurant.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Account has been successfully created for ' + str(username))
            return redirect('login')

    context = {'form':form}
    return render(request, 'register.html', context)

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect.')

    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')