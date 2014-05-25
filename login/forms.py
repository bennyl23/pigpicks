from django import forms

from login import validators


class LoginForm(forms.Form):
    user_email = forms.EmailField(
        max_length=60,
        label='Email',
        initial='',
        widget=forms.TextInput(
            attrs={'placeholder':'Enter email', 'class':'form-control', 'autofocus':'autofocus'}
        )
    )
    user_password = forms.CharField(
        max_length=60,
        label='Password',
        initial='',
        widget=forms.PasswordInput(
            attrs={'placeholder':'Enter password', 'class':'form-control'}
        )
    )


class RegisterForm(forms.Form):
    user_email = forms.EmailField(
        max_length=100,
        label='Email',
        initial='',
        widget=forms.TextInput(
            attrs={'placeholder':'Enter email', 'class':'form-control', 'autofocus':'autofocus'}
        ),
        validators=[validators.validate_user_email]
    )
    user_password = forms.CharField(
        min_length=8,
        max_length=60,
        label='Password',
        initial='',
        widget=forms.PasswordInput(
            attrs={'placeholder':'Enter password', 'class':'form-control'}
        ),
        error_messages={'min_length':'Password must be at least 8 characters.'}
    )
    user_password_again = forms.CharField(
        min_length=8,
        max_length=60,
        label='Re-enter Password',
        initial='',
        widget=forms.PasswordInput(
            attrs={'placeholder':'Re-enter password', 'class':'form-control'}
        ),
        error_messages={'min_length':'Password must be at least 8 characters.'}
    )
    user_team_name = forms.CharField(
        min_length=5,
        max_length=15,
        label='Team name (15 char max)',
        initial='',
        widget=forms.TextInput(
            attrs={'placeholder':'Enter your team name', 'class':'form-control'}
        ),
        validators=[validators.validate_user_team_name],
        error_messages={'min_length':'Team name must be at least 5 characters.'}
    )
    user_referring_email = forms.EmailField(
        max_length=100,
        label='Referring email',
        initial='',
        widget=forms.TextInput(
            attrs={'placeholder':'Enter email', 'class':'form-control'}
        ),
        validators=[validators.validate_referring_email]
    )


class ForgotPasswordForm(forms.Form):
    user_email = forms.EmailField(
        max_length=60,
        label='Email',
        initial='',
        widget=forms.TextInput(
            attrs={'placeholder':'Enter email', 'class':'form-control', 'autofocus':'autofocus'}
        ),
        validators=[validators.validate_referring_email]
    )
