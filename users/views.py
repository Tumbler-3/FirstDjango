from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from django.views.generic import ListView


class LoginView(ListView):
    template_name='users/login.html'

    def get_context_data(self, **kwargs):
        context = {
            'login': kwargs['login'],
            'user': kwargs['user'],
        }
        return context
    
    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.get_context_data(
            login=LoginForm,
            user=None if request.user.is_anonymous else request.user
        ))
    
    def post(self, request, **kwargs):
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

        return render(request, self.template_name, context=self.get_context_data(
            form=form,
            user=None if request.user.is_anonymous else request.user
        ))


class RegistrationView(ListView):
    template_name='users/registration.html'

    def get_context_data(self, **kwargs):
        context = {
            'registration': kwargs['registration'],
            'user': kwargs['user'],
        }
        return context
    
    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.get_context_data(
            registration=RegistrationForm,
            user=None if request.user.is_anonymous else request.user,
        ))

    def post(self, request, **kwargs):
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
        
        return render(request, self.template_name, context=self.get_context_data(
            registration=form,
            user=None,
        ))


def logout_view(request):
    logout(request)
    return redirect('/products/')