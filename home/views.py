from django.shortcuts import render
from django.http import HttpResponseRedirect

from login.functions import signed_in_only
from login.models import User


@signed_in_only
def index(request):
    try:
        user = User.objects.get(user_id=request.session['user_id'])
        return render(request, 'home/index.html', {
            'request': request,
            'user_email': user.user_email
        })
    except:
        pass

