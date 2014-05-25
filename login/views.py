from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError

from login.functions import clear_session
from login.models import User
from login import forms
from login.validators import validate_login
from login.validators import validate_login


def index(request, session_code=None):
    page_warning = ''
    if request.method == 'POST':
        # Get the bound login form
        form = forms.LoginForm(request.POST)
        # Validate the login form
        if form.is_valid():
            validate_login_response = validate_login(form.cleaned_data['user_email'], form.cleaned_data['user_password'])
            if validate_login_response['successful']:
                # Put the user id into session
                request.session['user_id'] = validate_login_response['user'].user_id
                return HttpResponseRedirect('/home/')
            else:
                return render(request, 'login/index.html', {
                    'page_warning': page_warning,
                    'page_error': validate_login_response['page_error'],
                    'form': form
                })
    else:
        if session_code == 'session_ended':
            page_warning = 'Your session timed out.  Please sign in again.'
        if session_code == 'logged_out':
            page_warning = 'You have logged out.'
        form = forms.LoginForm()

    # Renders the login form if it's a new request or bound form is not valid
    return render(request, 'login/index.html', {
        'page_warning': page_warning,
        'form': form
    })

def register(request):
    if request.method == 'POST':
        # Get the bound login form
        form = forms.RegisterForm(request.POST)
        # Validate the login form
        if form.is_valid():
            if (form.cleaned_data['user_password'] != form.cleaned_data['user_password_again']):
                return render(request, 'login/register.html', {
                    'page_error': 'The passwords you entered do not match.  Please enter the same password twice.',
                    'form': form
                })

            new_user = User(
                user_email = form.cleaned_data['user_email'],
                user_password = form.cleaned_data['user_password'],
                user_team_name = form.cleaned_data['user_team_name'],
                user_referring_email = form.cleaned_data['user_referring_email']
            )
            try:
                new_user.full_clean()
            except ValidationError as e:
                return render(request, 'login/register.html', {
                    'page_error': 'There was a problem during registration.  Try again.',
                    'form': form
                })
            else:
                new_user.save()
                request.session['user_id'] = new_user.user_id
                return HttpResponseRedirect('/home/')
    else:
        form = forms.RegisterForm()

    # Renders the register form if it's a new request
    return render(request, 'login/register.html', {
        'form': form
    })

def forgot_password(request):
    if request.method == 'POST':
        # Get the bound form
        form = forms.ForgotPasswordForm(request.POST)
        # Validate the form
        if form.is_valid():
            user = User.objects.get(user_email=form.cleaned_data['user_email'])

    else:
        form = forms.ForgotPasswordForm()

    return render(request, 'login/forgot_password.html', {
        'form': form
    })

def logout(request):
    clear_session(request)
    return HttpResponseRedirect('/login/logged_out')
