from django.http import HttpResponseRedirect


def signed_in_only(function):
    def _decorator(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/session_ended')

        return function(request, *args, **kwargs)

    return _decorator

def clear_session(request):
    request.session.clear()

def check_reset_password_access(function):
    def _decorator(request, *args, **kwargs):
        if 'user_id' not in request.session and 'user_id_to_reset' not in request.session:
            return HttpResponseRedirect('/login/session_ended')

        return function(request, *args, **kwargs)

    return _decorator
