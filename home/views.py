from django.shortcuts import render
from django.http import HttpResponseRedirect

from login.functions import signed_in_only
from picks.models import PickView
from picks.models import Week
from home.models import BlogEntry
from login.models import User


@signed_in_only
def index(request, week_number=0):
    page_warning = ''
    num_weeks = Week.objects.count()

    try:
        week = Week.objects.get(week_number=week_number)
    except Week.DoesNotExist:
        week = Week.objects.current_week()

    user = User.objects.get(user_id=request.session['user_id'])

    picks = PickView.objects.filter(user_id=request.session['user_id'], week_number=week.week_number)


    blog_entries = BlogEntry.objects.all().order_by('-entry_date')
    if not picks:
        page_warning = 'You have not made your picks for week ' + str(week.week_number) + ' yet.'

    return render(request, 'home/index.html',{
        'page_warning': page_warning,
        'request': request,
        'week': week,
        'picks': picks,
        'blog_entries': blog_entries,
        'num_weeks': num_weeks,
        'user': user
    })

