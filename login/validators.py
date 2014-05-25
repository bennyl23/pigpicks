from django.core.validators import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from login.models import User


# login validators
def validate_login(user_email, user_password):
    validate_login_response = {}
    validate_login_response['successful'] = True
    try:
        user = User.objects.get(
            user_email=user_email
        )
    except User.DoesNotExist:
        validate_login_response['successful'] = False
        validate_login_response['page_error'] = 'The email you entered is not in the system.  Please try again.'
    except User.MultipleObjectsReturned:
        validate_login_response['successful'] = False
        validate_login_response['page_error'] = 'There are multiple accounts that use the email you entered.  Please contact the commish.'
    except:
        validate_login_response['successful'] = False
        validate_login_response['page_error'] = 'There was an error during the sign in process.  Please try again.'
    else:
        # check the plain text password against the hash in the database
        if not check_password(user_password, user.user_password):
            validate_login_response['successful'] = False
            validate_login_response['page_error'] = 'The password you entered is incorrect.  Please try again.'
        else:
            validate_login_response['user'] = user
    finally:
        return validate_login_response

# register validators
def validate_user_email(value):
    existing_user_email = User.objects.filter(user_email=value)
    if len(existing_user_email):
        raise ValidationError('This email address is already registered.  Try another.')

def validate_user_team_name(value):
    existing_team_name = User.objects.filter(user_team_name=value)
    if len(existing_team_name):
        raise ValidationError('This team name is already being used.  Try another.')

def validate_referring_email(value):
    existing_referring_email = User.objects.filter(user_email=value)
    if (not existing_referring_email):
        raise ValidationError('This email could not be found.  Try again.')