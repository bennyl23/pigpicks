from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User as DjangoUser

from login.functions import clear_session
from login.functions import check_reset_password_access
from login.models import User
from login import forms
from login.validators import validate_login
from login.validators import validate_new_password

# REMOVE THIS!!!
from login.functions import insert_users


def index(request, session_code=None):
    page_warning = ''
    if request.method == 'POST':
        # Get the bound login form
        form = forms.LoginForm(request.POST)
        # Validate the login form
        if form.is_valid():
            validate_login_response = validate_login(form.cleaned_data['user_email'], form.cleaned_data['user_password'])
            if validate_login_response['successful']:
                # Check if this user needs to reset their password
                if validate_login_response['user'].user_reset_password == True:
                    # Send the user to the reset password page
                    request.session['user_id_to_reset'] = validate_login_response['user'].user_id
                    return HttpResponseRedirect('/login/reset_password')

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

    # REMOVE THIS!!!
    insert_users()

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
            validate_new_password_response = validate_new_password(form.cleaned_data['user_password'], form.cleaned_data['user_password_again'])
            if not validate_new_password_response['successful']:
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
            user_temp_password = DjangoUser.objects.make_random_password(length=8)

            text_only_template = get_template('login/forgot_password_email.txt')
            html_template = get_template('login/forgot_password_email.html')

            content = Context({'user_email':user.user_email, 'user_temp_password':user_temp_password})

            # render the email templates
            text_content = text_only_template.render(content)
            html_content = html_template.render(content)

            # set email parameters and send
            subject = 'Forgot Password'
            from_email = 'Pig Picks Five<ben@pigpicksfive.com>'
            to_emails = user.user_email
            email_msg = EmailMultiAlternatives(subject, text_content, from_email, [to_emails])
            email_msg.attach_alternative(html_content, "text/html")
            email_msg.send()

            # update the user with the new temp password and set their reset password flag
            user.user_password = user_temp_password
            user.user_reset_password = True
            user.save()

            reset_email_sent_message = 'An email has been sent to ' + str(user.user_email) + ' with instructions on how to reset your password.'
            return render(request, 'login/forgot_password.html', {
                'reset_email_sent_message': reset_email_sent_message,
                'form': form
            })

    else:
        form = forms.ForgotPasswordForm()

    return render(request, 'login/forgot_password.html', {
        'form': form
    })

@check_reset_password_access
def reset_password(request):
    page_error = ''
    user_logged_in = False

    if 'user_id' in request.session:
        user_logged_in = True

    if request.method == 'POST':
        form = forms.ResetPasswordForm(request.POST)
        if form.is_valid():
            validate_new_password_response = validate_new_password(form.cleaned_data['user_password'], form.cleaned_data['user_password_again'])
            if validate_new_password_response['successful']:
                try:
                    # update the user
                    if 'user_id' in request.session:
                        user = User.objects.get(user_id=request.session['user_id'])
                    else:
                        user = User.objects.get(user_id=request.session['user_id_to_reset'])
                    user.user_password = form.cleaned_data['user_password']
                    user.user_reset_password = False
                    user.save()
                    # put the user_id into session
                    request.session['user_id'] = user.user_id
                    return HttpResponseRedirect('/home/')
                except:
                    page_error = 'There was a problem resetting your password.  If your session timed out you will have to log in with your temporary password and try again.'
            else:
                return render(request, 'login/reset_password.html', {
                    'page_error': 'The passwords you entered do not match.  Please enter the same password twice.',
                    'user_logged_in': user_logged_in,
                    'form': form
                })
    else:
        form = forms.ResetPasswordForm()

    return render(request, 'login/reset_password.html', {
        'page_error': page_error,
        'user_logged_in': user_logged_in,
        'form': form
    })


def logout(request):
    clear_session(request)
    return HttpResponseRedirect('/login/logged_out')
