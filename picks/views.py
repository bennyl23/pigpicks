from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.utils import timezone

from login.functions import signed_in_only
from picks.models import Matchup
from picks.models import MatchupView
from picks.models import Pick
from picks.models import PickView
from picks.models import Week

from picks.functions import build_matchup_dict


@signed_in_only
def index(request, week_number=0):
    page_error = ''
    page_warning = ''
    lock_picks = False
    num_weeks = Week.objects.count()
    num_picks_made = 0

    if request.method == 'POST':
        week = Week.objects.get(week_number=int(request.POST.get('week_number')))
        matchups = MatchupView.objects.filter(week_number=week.week_number).order_by('game_date', 'matchup_id')
        picks_list = []
        for matchup in matchups:
            try:
                matchup_id_field_val = int(request.POST.get(str(matchup.matchup_id)))
            except ValueError as e:
                matchup_id_field_val = 0

            # matchup_id form field will have a value if selected
            if matchup_id_field_val != 0:
                num_picks_made += 1
                # Add the pick to the list if it isn't locked.  Locked picks do not get deleted before save.
                if not Matchup.objects.get(matchup_id=matchup.matchup_id).pick_locked():
                    user_pick = {}
                    user_pick['user_id_id'] = request.session['user_id']
                    user_pick['matchup_id_id'] = matchup.matchup_id
                    user_pick['nfl_team_id_id'] = matchup_id_field_val
                    picks_list.append(user_pick)

        if num_picks_made > 5:
            page_error = 'You have made too many picks.  Try again.'
        elif num_picks_made < 5:
            page_error = 'You have made too few picks.  Try again.'
        else:
            # first, delete any existing picks for the user (as long as they aren't locked)
            Pick.objects.filter(matchup_id__week_number=week.week_number, user_id_id=request.session['user_id'], matchup_id__game_date__gt=timezone.now()).delete()
            for pick_dict in picks_list:
                pick = Pick(**pick_dict)
                try:
                    pick.full_clean()
                except ValidationError as e:
                    page_error = 'There was a problem saving your picks.  Try again.'
                else:
                    pick.save()

        if (page_error == ''):
            # Redirect to confirmation page if picks submission successful
            return HttpResponseRedirect('/picks/confirmation/')
    else:
    # not a form post
        # if no week number passed in, use the current week
        if week_number == 0:
            week = Week.objects.current_week()
        else:
            try:
                week = Week.objects.get(week_number=week_number)
            except Week.DoesNotExist:
                page_warning = 'We have not entered matchups for week ' + str(week_number) + ' yet.'
                week = Week(week_number=week_number)
                lock_picks = True

        if lock_picks == False and week.picks_lock < timezone.now():
            lock_picks = True
            page_warning = 'Week ' + str(week.week_number) + ' picks have been locked.'

        matchups = MatchupView.objects.filter(week_number=week.week_number).order_by('game_date', 'matchup_id')

    matchups_list = []
    # loop over the matchups and check if the user picked either team in the matchup
    for matchup in matchups:
        try:
            pick = Pick.objects.get(user_id_id=request.session['user_id'], matchup_id_id=matchup.matchup_id)
        except Pick.DoesNotExist:
            matchup_dict = build_matchup_dict(matchup, 0)
        else:
            matchup_dict = build_matchup_dict(matchup, pick.nfl_team_id_id)
        finally:
            matchups_list.append(matchup_dict)

    if not matchups_list:
        page_warning = 'We have not entered matchups for week ' + str(week.week_number) + ' yet.'
    elif not week.lines_entered:
        page_warning = 'We have not entered lines for week ' + str(week.week_number) + ' yet.'

    # Render the picks page if first time in or error after posting picks form
    return render(request, 'picks/index.html',{
        'request': request,
        'week': week,
        'num_weeks': num_weeks,
        'matchups': matchups_list,
        'lock_picks': lock_picks,
        'page_error': page_error,
        'page_warning': page_warning
    })

@signed_in_only
def confirmation(request):
    week = Week.objects.current_week()
    picks = PickView.objects.filter(week_number=week.week_number, user_id=request.session['user_id'])
    page_warning = ''
    if not picks:
        page_warning = 'You have not made picks for week ' + str(week.week_number) + ' yet.'
    return render(request, 'picks/confirmation.html',{
        'page_warning': page_warning,
        'request': request,
        'week': week,
        'picks': picks
    })
