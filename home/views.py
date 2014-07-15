from django.shortcuts import render
from django.http import HttpResponseRedirect

from login.functions import signed_in_only
from picks.models import PickView
from picks.models import Week
from home.models import BlogEntry


@signed_in_only
def index(request):
    page_warning = ''
    week = Week.objects.current_week()
    picks = PickView.objects.filter(user_id=request.session['user_id'], week_number=week.week_number)
    blog_entries = BlogEntry.objects.all().order_by('-entry_date')
    if not picks:
        page_warning = 'You have not made your picks for week ' + str(week.week_number) + ' yet.'

    return render(request, 'home/index.html',{
        'page_warning': page_warning,
        'request': request,
        'week': week,
        'picks': picks,
        'blog_entries': blog_entries
    })

