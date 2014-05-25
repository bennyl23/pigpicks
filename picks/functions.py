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