from operator import itemgetter

from django.db.models import Sum

from picks.models import PickView
from league.models import StandingsView


def build_league_picks_list(picks):
    """Return a list of PickViews, including the number of wins the user has that week"""
    picks_list = []

    for pick in picks:
        pick_dict = {}
        pick_dict["pick_id"] = pick.pick_id
        pick_dict["nfl_team_id"] = pick.nfl_team_id
        pick_dict["user_id"] = pick.user_id
        pick_dict["won_pick"] = pick.won_pick
        pick_dict["best_bet"] = pick.best_bet
        pick_dict["user_email"] = pick.user_email
        pick_dict["user_team_name"] = pick.user_team_name
        pick_dict["matchup_id"] = pick.matchup_id
        pick_dict["week_number"] = pick.week_number
        pick_dict["game_date"] = pick.game_date
        pick_dict["home_team_id"] = pick.home_team_id
        pick_dict["away_team_id"] = pick.away_team_id
        pick_dict["spread"] = pick.spread
        pick_dict["spread_abs"] = pick.spread_abs
        pick_dict["home_team_score"] = pick.home_team_score
        pick_dict["away_team_score"] = pick.away_team_score
        pick_dict["matchup_completed"] = pick.matchup_completed
        pick_dict["home_team_location"] = pick.home_team_location
        pick_dict["home_team_location_short"] = pick.home_team_location_short
        pick_dict["home_team_name"] = pick.home_team_name
        pick_dict["away_team_location"] = pick.away_team_location
        pick_dict["away_team_location_short"] = pick.away_team_location_short
        pick_dict["away_team_name"] = pick.away_team_name
        pick_dict["pick_locked"] = pick.pick_locked()
        pick_dict["no_losses"] = PickView.objects.has_no_losses(pick.user_id, pick.week_number)
        pick_dict["wins_count"] = PickView.objects.get_wins_count_by_user_week(pick.user_id, pick.week_number)
        pick_dict["margin_of_coverage"] = PickView.objects.calc_margin_of_coverage(pick.user_id, pick.week_number, pick_dict["no_losses"])
        pick_dict["best_bet_moc"] = PickView.objects.calc_best_bet_moc(pick.user_id, pick.week_number)
        picks_list.append(pick_dict)

    return picks_list

def build_standings_list():
    users_weeks_results = StandingsView.objects.all().order_by('user_team_name', 'week_number')
    standings_list = []
    for user_week_result in users_weeks_results:
        standings_dict = {}
        standings_dict['user_id'] = user_week_result.user_id
        standings_dict['user_team_name'] = user_week_result.user_team_name
        standings_dict['week_number'] = user_week_result.week_number
        week_points = user_week_result.week_points
        if week_points == None:
            week_points = 0
        standings_dict['week_points'] = week_points
        total_wins = PickView.objects.filter(user_id=user_week_result.user_id, won_pick=True).count()
        standings_dict['total_wins'] = total_wins
        total_points = StandingsView.objects.filter(user_id=user_week_result.user_id).aggregate(Sum('week_points')).get('week_points__sum')
        if total_points == None:
            total_points = 0
        standings_dict['total_points'] = total_points
        standings_dict['position'] = ''
        standings_list.append(standings_dict)

    standings_list = sorted(standings_list, key=itemgetter('total_points'), reverse=True)

    # set the standings position
    position_count = 0
    last_user_id = ''
    total_count = 0
    last_total_points = ''
    for standings_dict in standings_list:

        if last_user_id != standings_dict['user_id']:
            total_count += 1

        if last_total_points == '':
            position_count += 1
        elif last_total_points > standings_dict['total_points']:
            position_count = total_count

        standings_dict['position'] = position_count
        last_user_id = standings_dict['user_id']
        last_total_points = standings_dict['total_points']

    return standings_list



