from django.shortcuts import render

from login.functions import signed_in_only


@signed_in_only
def index(request):
    return render(request, 'rules/index.html',{
        'request': request
    })
