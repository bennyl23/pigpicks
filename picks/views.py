from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone
from datetime import timedelta

from login.functions import signed_in_only
from picks.models import Matchup
from picks.models import MatchupView
from picks.models import Pick
from picks.models import PickView
from picks.models import Week

from picks.functions import build_matchup_dict
from picks.functions import save_picks


@signed_in_only
def index(request, week_number=0):
    page_error = ''
    page_warning = ''
    lock_picks = False
    num_weeks = Week.objects.count()
    num_picks_made = 0
    request.session['picks_list'] = []

    if request.method == 'POST':
        week = Week.objects.get(week_number=int(request.POST.get('week_number')))
        matchups = MatchupView.objects.filter(week_number=week.week_number).order_by('game_date', 'matchup_id')
        for matchup in matchups:
            try:
                matchup_id_field_val = int(request.POST.get(str(matchup.matchup_id)))
            except ValueError as e:
                matchup_id_field_val = 0

            # matchup_id form field will have a value if selected
            if matchup_id_field_val != 0:
                num_picks_made += 1

                user_pick = {}
                user_pick['user_id_id'] = request.session['user_id']
                user_pick['matchup_id_id'] = matchup.matchup_id
                user_pick['nfl_team_id_id'] = matchup_id_field_val

                # Add to the picks list in session
                request.session['picks_list'].append(user_pick)

        if num_picks_made > 5:
            page_error = 'You have made too many picks.  Try again.'
        elif num_picks_made < 5:
            page_error = 'You have made too few picks.  Try again.'

        if (page_error == ''):
            # Redirect to best bet page if picks submission successful
            return HttpResponseRedirect('/picks/bestbet/')
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

        if lock_picks == False and (week.picks_lock < timezone.now()):
            lock_picks = True
            page_warning = 'Week ' + str(week.week_number) + ' picks have been locked.'

        matchups = MatchupView.objects.filter(week_number=week.week_number).order_by('game_date', 'matchup_id')

    matchups_list = []
    # loop over the matchups and check if the user picked either team in the matchup
    for matchup in matchups:
        # if user made picks and there was an error, select the picks the user just made rather than the picks in the db
        if request.method == 'POST':
            try:
                nfl_team_id_form_post = int(request.POST.get(str(matchup.matchup_id)))
            except ValueError as e:
                nfl_team_id_form_post = 0
            matchup_dict = build_matchup_dict(matchup, nfl_team_id_form_post)
        else:
            try:
                pick = Pick.objects.get(user_id_id=request.session['user_id'], matchup_id_id=matchup.matchup_id)
            except Pick.DoesNotExist:
                matchup_dict = build_matchup_dict(matchup, 0)
            else:
                matchup_dict = build_matchup_dict(matchup, pick.nfl_team_id_id)

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
def bestbet(request):
    week = Week.objects.current_week()
    lock_picks = False
    page_warning = ''
    page_error = ''

    if lock_picks == False and (week.picks_lock < timezone.now()):
        lock_picks = True
        page_warning = 'Week ' + str(week.week_number) + ' picks have been locked.'

    if request.method == 'POST' and lock_picks == False:
        best_bet_field_val = request.POST.get('bestbet')
        if not best_bet_field_val:
            page_error = 'Please select your best bet.'
        else:
            best_bet_field_val = int(best_bet_field_val)
            picks_list = []
            for pick in request.session['picks_list']:
                user_pick = {}
                user_pick['user_id_id'] = pick['user_id_id']
                user_pick['matchup_id_id'] = pick['matchup_id_id']
                user_pick['nfl_team_id_id'] = pick['nfl_team_id_id']
                if best_bet_field_val == pick['matchup_id_id']:
                    user_pick['best_bet'] = True
                else:
                    user_pick['best_bet'] = False
                # Add the pick to the list if it isn't locked.  Locked picks do not get deleted before save.
                if not Matchup.objects.get(matchup_id=pick['matchup_id_id']).pick_locked():
                    picks_list.append(user_pick)

            save_picks_response = save_picks(picks_list, week.week_number, request.session['user_id'])
            if save_picks_response == '':
                return HttpResponseRedirect('/picks/confirmation/')
            else:
                page_error = save_picks_response

    matchups_list = []

    # If lock_picks is true, the user will never get to the best bet page, but just in case
    if lock_picks == False:
        # See if the user made picks already and if their best bet is locked
        try:
            best_bet_pick = PickView.objects.get(week_number=week.week_number, user_id=request.session['user_id'], best_bet=True)
        except PickView.DoesNotExist:
            pass
        else:
            # if their best bet pick is locked, save the picks and go to the confirmation page
            if best_bet_pick.pick_locked():
                picks_list = []
                for pick in request.session['picks_list']:
                    user_pick = {}
                    user_pick['user_id_id'] = pick['user_id_id']
                    user_pick['matchup_id_id'] = pick['matchup_id_id']
                    user_pick['nfl_team_id_id'] = pick['nfl_team_id_id']
                    if best_bet_pick.matchup_id == pick['matchup_id_id']:
                        user_pick['best_bet'] = True
                    else:
                        user_pick['best_bet'] = False
                    # Add the pick to the list if it isn't locked.  Locked picks do not get deleted before save.
                    if not Matchup.objects.get(matchup_id=pick['matchup_id_id']).pick_locked():
                        picks_list.append(user_pick)

                save_picks_response = save_picks(picks_list, week.week_number, request.session['user_id'])
                if save_picks_response == '':
                    return HttpResponseRedirect('/picks/confirmation/')
                else:
                    page_error = save_picks_response

        try:
            for pick in request.session['picks_list']:
                matchup = MatchupView.objects.get(matchup_id=pick['matchup_id_id'])
                matchup_dict = build_matchup_dict(matchup, pick['nfl_team_id_id'])
                matchups_list.append(matchup_dict)
        except:
            page_error = 'An error has occured.  Go back and try again.'

    return render(request, 'picks/bestbet.html',{
        'request': request,
        'week': week,
        'matchups': matchups_list,
        'lock_picks': lock_picks,
        'page_warning': page_warning,
        'page_error': page_error
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
