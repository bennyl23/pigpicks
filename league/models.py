from django.db import models


class LeagueRecordView(models.Model):
    week_number = models.PositiveSmallIntegerField(primary_key=True)
    league_wins = models.PositiveSmallIntegerField()
    league_losses = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'league_record_v'


class WeekBreakdownView(models.Model):
    nfl_team_id = models.PositiveSmallIntegerField(primary_key=True)
    nfl_team_name = models.CharField(max_length=50)
    nfl_team_location = models.CharField(max_length=50)
    nfl_team_location_short = models.CharField(max_length=3)
    week_number = models.PositiveSmallIntegerField()
    num_picks = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'week_breakdown_v'


class StandingsView(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_team_name = models.CharField(max_length=15)
    week_number = models.PositiveSmallIntegerField()
    pick_wins = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'standings_v'
