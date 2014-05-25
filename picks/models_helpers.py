import math


def calc_winner_loser(matchup):
    """Calculate the winner and loser of a matchup and return the team id's in a dictionary"""
    winning_nfl_team_id = 0
    losing_nfl_team_id = 0
    # spread < 0 means home team is favored
    if matchup.spread < 0:
        # home favorite covered
        if (matchup.home_team_score - matchup.away_team_score) > math.fabs(matchup.spread):
            winning_nfl_team_id = matchup.home_team_id
            losing_nfl_team_id = matchup.away_team_id
        # away underdog covered
        else:
            winning_nfl_team_id = matchup.away_team_id
            losing_nfl_team_id = matchup.home_team_id
    # spread > 0 means away team is favored
    else:
        # away favorite covered
        if (matchup.away_team_score - matchup.home_team_score) > math.fabs(matchup.spread):
            winning_nfl_team_id = matchup.away_team_id
            losing_nfl_team_id = matchup.home_team_id
        # home underdog covered
        else:
            winning_nfl_team_id = matchup.home_team_id
            losing_nfl_team_id = matchup.away_team_id

    game_result_dict = {}
    game_result_dict['winning_nfl_team_id'] = winning_nfl_team_id
    game_result_dict['losing_nfl_team_id'] = losing_nfl_team_id
    return game_result_dict
