from picks.models import Pick
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

def build_matchup_dict(matchup, nfl_team_id):
    """Return a dictionary of a MatchupView, including the nfl_team_id the user selected for that matchup"""
    matchup_dict = {}
    matchup_dict['matchup_id'] = matchup.matchup_id
    matchup_dict['game_date'] = matchup.game_date
    matchup_dict['spread'] = matchup.spread
    matchup_dict['spread_abs'] = matchup.spread_abs
    matchup_dict['pick_locked'] = matchup.pick_locked()
    matchup_dict['nfl_team_id'] = nfl_team_id
    matchup_dict['home_team_id'] = matchup.home_team_id
    matchup_dict['home_team_name'] = matchup.home_team_name
    matchup_dict['home_team_location'] = matchup.home_team_location
    matchup_dict['home_team_location_short'] = matchup.home_team_location_short
    matchup_dict['away_team_id'] = matchup.away_team_id
    matchup_dict['away_team_name'] = matchup.away_team_name
    matchup_dict['away_team_location'] = matchup.away_team_location
    matchup_dict['away_team_location_short'] = matchup.away_team_location_short
    return matchup_dict

def save_picks(picks, week_number, user_id):
    response = ''

    # first, delete any existing picks for the user (as long as they aren't locked)
    # note: adding 2 hours to the timezone because server is central time and picks lock 1 hour before game date
    Pick.objects.filter(matchup_id__week_number=week_number, user_id_id=user_id, matchup_id__game_date__gte=(timezone.now() + timedelta(hours=2))).delete()
    for pick_dict in picks:
        pick = Pick(**pick_dict)
        try:
            pick.full_clean()
        except ValidationError as e:
            response = 'There was a problem saving your picks.  Try again.'
        else:
            pick.save()

    return response