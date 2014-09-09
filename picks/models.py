import datetime
from datetime import timedelta

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from picks.models_helpers import calc_winner_loser


# custom weeks manager
class WeeksManager(models.Manager):
    def current_week(self):
        """Return a week model instance for the current week"""
        try:
            week = Week.objects.get(
                week_start__lte=datetime.date.today(),
                week_end__gte=datetime.date.today()
            )
        except Week.DoesNotExist:
            week = Week.objects.get(week_number=1)

        return week


# custom picks manager
class PicksManager(models.Manager):
    def get_picks_by_matchup_nflteam(self, matchup_id, nfl_team_id):
        """Return a queryset of picks for a matchup_id and nfl_team_id"""
        return super(PicksManager, self).get_query_set().filter(matchup_id_id=matchup_id, nfl_team_id_id=nfl_team_id)


# custom PickView manager
class PickViewManager(models.Manager):
    def get_wins_count_by_user_week(self, user_id, week_number):
        """Return the number of wins for a user_id and week_number"""
        return super(PickViewManager, self).get_query_set().filter(user_id=user_id, week_number=week_number, won_pick=1).count()

    def has_no_losses(self, user_id, week_number):
        """Return true/false if user has losses for a week"""
        # get all completed matchups for the user and week
        matchups_completed = super(PickViewManager, self).get_query_set().filter(user_id=user_id, week_number=week_number, matchup_completed=True)
        if matchups_completed.exists():
            # get all completed matchups where the user lost
            if matchups_completed.filter(won_pick=False).exists():
                return False

            # user has won all completed matchups
            return True

        # user has no completed matchups
        return False

    def calc_margin_of_coverage(self, user_id, week_number, no_losses):
        """Return the margin of coverage for a user_id and week_number"""
        total_margin_of_coverage = 0
        if no_losses:
            picks = super(PickViewManager, self).get_query_set().filter(user_id=user_id, week_number=week_number)
            for pick in picks:
                moc = 0
                if pick.matchup_completed:
                    # user picked home team
                    if pick.nfl_team_id == pick.home_team_id:
                        moc = (pick.home_team_score + pick.spread) - pick.away_team_score
                    else:
                        away_team_spread = 0
                        if pick.spread < 0:
                            away_team_spread = pick.spread_abs
                        else:
                            away_team_spread = pick.spread - (pick.spread * 2)
                        moc = (pick.away_team_score + away_team_spread) - pick.home_team_score

                total_margin_of_coverage += moc

        return total_margin_of_coverage

    def calc_best_bet_moc(self, user_id, week_number):
        try:
            best_bet_pick = super(PickViewManager, self).get_query_set().get(user_id=user_id, week_number=week_number, best_bet=True)
        except PickView.DoesNotExist:
            return ''
        else:
            if best_bet_pick.matchup_completed:
                moc = 0
                # user picked home team
                if best_bet_pick.nfl_team_id == best_bet_pick.home_team_id:
                    moc = (best_bet_pick.home_team_score + best_bet_pick.spread) - best_bet_pick.away_team_score
                else:
                    away_team_spread = 0
                    if best_bet_pick.spread < 0:
                        away_team_spread = best_bet_pick.spread_abs
                    else:
                        away_team_spread = best_bet_pick.spread - (best_bet_pick.spread * 2)
                    moc = (best_bet_pick.away_team_score + away_team_spread) - best_bet_pick.home_team_score
            else:
                moc = ''

            return moc

# Tables
class Week(models.Model):
    week_number = models.PositiveSmallIntegerField(primary_key=True)
    week_start = models.DateTimeField()
    week_end = models.DateTimeField()
    picks_lock = models.DateTimeField()
    lines_entered = models.BooleanField(default=False)
    objects = WeeksManager()

    class Meta:
        db_table = 'weeks_t'

    def __unicode__(self):
        return unicode(self.week_number)


class NFLTeam(models.Model):
    nfl_team_id = models.AutoField(primary_key=True)
    nfl_team_location = models.CharField(max_length=50)
    nfl_team_name = models.CharField(max_length=50)
    nfl_team_location_short = models.CharField(max_length=3)

    class Meta:
        db_table = 'nflteam_t'

    def __unicode__(self):
        return unicode(self.nfl_team_name)


class Matchup(models.Model):
    matchup_id = models.AutoField(primary_key=True)
    week_number = models.ForeignKey('Week', db_column='week_number')
    game_date = models.DateTimeField()
    away_team_id = models.ForeignKey('NFLTeam', related_name='matchup_away_team_id', db_column='away_team_id')
    home_team_id = models.ForeignKey('NFLTeam', related_name='matchup_home_team_id', db_column='home_team_id')
    spread = models.FloatField()
    away_team_score = models.PositiveSmallIntegerField(default=0, blank=True)
    home_team_score = models.PositiveSmallIntegerField(default=0, blank=True)
    matchup_completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'matchup_t'

    def __unicode__(self):
        return unicode('Week ' + str(self.week_number) + ': ' + str(self.away_team_id) + ' @ ' + str(self.home_team_id))

    def matchup_desc(self):
        return 'Week ' + str(self.week_number) + ': ' + str(self.away_team_id) + ' @ ' + str(self.home_team_id)

    def pick_locked(self):
        # note: subtract 2 hours because server is central time zone and game locks 1 hour before game date
        if (self.game_date - timedelta(hours=2)) <= timezone.now():
            return True

        return False

    def clean(self, *args, **kwargs):
        try:
            home_team_in_matchup = Matchup.objects.filter(Q(week_number=self.week_number) & (Q(home_team_id_id=self.home_team_id) | Q(away_team_id_id=self.home_team_id))).exclude(matchup_id=self.matchup_id)
            if home_team_in_matchup:
                raise ValidationError('The home team you selected is already in a matchup for the week selected.')

            away_team_in_matchup = Matchup.objects.filter(Q(week_number=self.week_number) & (Q(home_team_id_id=self.away_team_id) | Q(away_team_id_id=self.away_team_id))).exclude(matchup_id=self.matchup_id)
            if away_team_in_matchup:
                raise ValidationError('The away team you selected is already in a matchup for the week selected.')
        # this will run if the user did not enter week_number or did not select home_team_id or away_team_id
        except ObjectDoesNotExist:
            pass

    def save(self, *args, **kwargs):
        if self.matchup_completed == True:
            # get the winner and loser
            game_result_dict = calc_winner_loser(self)
            # update the winners
            Pick.objects.get_picks_by_matchup_nflteam(self.matchup_id, game_result_dict['winning_nfl_team_id']).update(won_pick=True)
            # update the losers (just in case)
            Pick.objects.get_picks_by_matchup_nflteam(self.matchup_id, game_result_dict['losing_nfl_team_id']).update(won_pick=False)
        else:
            # reset won_pick for all picks
            Pick.objects.get_picks_by_matchup_nflteam(self.matchup_id, self.home_team_id).update(won_pick=False)
            Pick.objects.get_picks_by_matchup_nflteam(self.matchup_id, self.away_team_id).update(won_pick=False)

        super(Matchup, self).save(*args, **kwargs)


class Pick(models.Model):
    pick_id = models.AutoField(primary_key=True)
    nfl_team_id = models.ForeignKey('NFLTeam', db_column='nfl_team_id')
    user_id = models.ForeignKey('login.User', db_column='user_id')
    matchup_id = models.ForeignKey('Matchup', db_column='matchup_id')
    won_pick = models.BooleanField(default=False)
    best_bet = models.BooleanField(default=False)
    objects = PicksManager()

    class Meta:
        managed = False
        db_table = 'pick_t'

    def __unicode__(self):
        return unicode(self.pick_id)


# Views
class MatchupView(models.Model):
    matchup_id = models.IntegerField(primary_key=True)
    week_number = models.PositiveSmallIntegerField()
    game_date = models.DateTimeField()
    home_team_id = models.PositiveSmallIntegerField()
    away_team_id = models.PositiveSmallIntegerField()
    spread = models.FloatField()
    spread_abs = models.FloatField()
    home_team_score = models.PositiveSmallIntegerField()
    away_team_score = models.PositiveSmallIntegerField()
    matchup_completed = models.BooleanField()
    home_team_location = models.CharField(max_length=50)
    home_team_location_short = models.CharField(max_length=3)
    home_team_name = models.CharField(max_length=50)
    away_team_location = models.CharField(max_length=50)
    away_team_location_short = models.CharField(max_length=3)
    away_team_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'matchup_v'

    def pick_locked(self):
        # note: subtract 2 hours because server is central time zone and game locks 1 hour before game date
        if (self.game_date - timedelta(hours=2)) <= timezone.now():
            return True

        return False

class PickView(models.Model):
    pick_id = models.IntegerField(primary_key=True)
    nfl_team_id = models.PositiveSmallIntegerField()
    user_id = models.IntegerField()
    won_pick = models.BooleanField()
    best_bet = models.BooleanField()
    user_email = models.EmailField(max_length=100)
    user_team_name = models.CharField(max_length=15)
    matchup_id = models.IntegerField()
    week_number = models.PositiveSmallIntegerField()
    game_date = models.DateTimeField()
    home_team_id = models.PositiveSmallIntegerField()
    away_team_id = models.PositiveSmallIntegerField()
    spread = models.FloatField()
    spread_abs = models.FloatField()
    home_team_score = models.PositiveSmallIntegerField()
    away_team_score = models.PositiveSmallIntegerField()
    matchup_completed = models.BooleanField()
    home_team_location = models.CharField(max_length=50)
    home_team_location_short = models.CharField(max_length=3)
    home_team_name = models.CharField(max_length=50)
    away_team_location = models.CharField(max_length=50)
    away_team_location_short = models.CharField(max_length=3)
    away_team_name = models.CharField(max_length=50)
    objects = PickViewManager()

    class Meta:
        managed = False
        db_table = 'picks_v'

    def pick_locked(self):
        # note: subtract 2 hours because server is central time zone and game locks 1 hour before game date
        if (self.game_date - timedelta(hours=2)) <= timezone.now():
            return True

        return False


class PicksRecordView(models.Model):
    user_id = models.IntegerField(primary_key=True)
    nfl_team_id = models.PositiveSmallIntegerField()
    nfl_team_name = models.CharField(max_length=50)
    nfl_team_location = models.CharField(max_length=50)
    nfl_team_location_short = models.CharField(max_length=3)
    team_wins = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'picks_record_v'

