from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User


def login_view(request):

    if request.method == 'GET':

        user = None if request.user.is_anonymous else request.user

        context = {
            'login': LoginForm,
            'user': user,
        }

        return render(request, 'users/login.html', context=context)
    
    if request.method == 'POST':

        form = LoginForm(data=request.POST)

        if form.is_valid():

            user = authenticate(
                username = form.cleaned_data.get('username'),
                password = form.cleaned_data.get('password')
            )
            
            if user:
                login(request, user=user)
                return redirect('/products/')
            else:
                form.add_error('username', 'username or password is incorrect')

        return render(request, 'users/login.html', context={'login': form, 'user': user,})


def registration_view(request):

    user = None if request.user.is_anonymous else request.user

    if request.method == 'GET':

        context = {
            'registration': RegistrationForm,
            'user': user,
        }

        return render(request, 'users/registration.html', context=context)
    
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            if form.cleaned_data.get('password') == form.cleaned_data.get('confirm__password'):
                
                user = User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('confirm__password')
                )

                login(request, user=user)
                return redirect('/products/')
            
            else:
                form.add_error('confirm__password', 'passwords are different')
        
        return render(request, 'users/registration.html', context={'registration': form, 'user': None,})


def logout_view(request):
    logout(request)
    return redirect('/products/')