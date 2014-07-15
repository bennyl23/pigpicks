from django.shortcuts import render

from login.functions import signed_in_only
from rules.models import Rule


@signed_in_only
def index(request):
    page_warning = ''
    try:
        rule = Rule.objects.first()
    except Rule.DoesNotExist:
        page_warning = 'There are no rules entered at this time.'
    return render(request, 'rules/index.html',{
        'request': request,
        'rule': rule,
        'page_warning': page_warning
    })
