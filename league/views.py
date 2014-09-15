from django.shortcuts import render
from django.utils import timezone

from login.functions import signed_in_only
from picks.models import Week
from picks.models import PickView
from league.models import WeekBreakdownView
from league.functions import build_league_picks_list
from league.functions import build_standings_list
from datetime import timedelta


@signed_in_only
def index(request, week_number=0):
    page_warning = ''
    lock_picks = False
    num_weeks = Week.objects.count()

    if week_number == 0:
        week = Week.objects.current_week()
    else:
        try:
            week = Week.objects.get(week_number=week_number)
        except Week.DoesNotExist:
            page_warning = 'There are no picks for week ' + str(week_number) + ' yet.'
            week = Week(week_number=week_number)
            lock_picks = True

    if lock_picks == False and (week.picks_lock - timedelta(hours=1)) < timezone.now():
        lock_picks = True

    picks = PickView.objects.filter(week_number=week.week_number).order_by('user_team_name', 'game_date', 'nfl_team_id')

    at_least_one_matchup_finished = False
    if picks.filter(matchup_completed=True).exists():
        at_least_one_matchup_finished = True

    league_win_percentage = 0.0

    picks_list = build_league_picks_list(picks)
    if not picks.exists():
        page_warning = 'There are no picks for week ' + str(week.week_number) + ' yet.'
    else:
        league_win_percentage = round((float(picks.filter(won_pick=True).count()) / float(picks.count())) * 100, 1)

    return render(request, 'league/index.html',{
        'request': request,
        'week': week,
        'num_weeks': num_weeks,
        'picks': picks_list,
        'league_win_percentage': league_win_percentage,
        'at_least_one_matchup_finished': at_least_one_matchup_finished,
        'session_user_id': request.session['user_id'],
        'lock_picks': lock_picks,
        'page_warning': page_warning
    })

@signed_in_only
def breakdown(request, week_number=0):
    page_warning = ''
    lock_picks = False
    num_weeks = Week.objects.count()

    if week_number == 0:
        week = Week.objects.current_week()
    else:
        try:
            week = Week.objects.get(week_number=week_number)
        except Week.DoesNotExist:
            page_warning = 'There are no picks for week ' + str(week_number) + ' yet.'
            week = Week(week_number=week_number)
            lock_picks = True

    if lock_picks == False and (week.picks_lock - timedelta(hours=1)) < timezone.now():
        lock_picks = True
    else:
        page_warning = 'The breakdown will show on ' + str(week.picks_lock.strftime('%A, %b %d at %I:%M %p')) + '.'

    teams = WeekBreakdownView.objects.filter(week_number=week.week_number).order_by('-num_picks', 'nfl_team_location', 'nfl_team_name')
    user_picks = PickView.objects.filter(week_number=week.week_number, user_id=request.session['user_id']).values_list('nfl_team_id', flat=True)

    return render(request, 'league/breakdown.html',{
        'request': request,
        'week': week,
        'num_weeks': num_weeks,
        'session_user_id': request.session['user_id'],
        'lock_picks': lock_picks,
        'page_warning': page_warning,
        'teams': teams,
        'user_picks': user_picks
    })

@signed_in_only
def standings(request):
    standings_list = build_standings_list()
    weeks = Week.objects.all().order_by('week_number')

    return render(request, 'league/standings.html',{
        'request': request,
        'weeks': weeks,
        'standings': standings_list,
        'session_user_id': request.session['user_id']
    })

